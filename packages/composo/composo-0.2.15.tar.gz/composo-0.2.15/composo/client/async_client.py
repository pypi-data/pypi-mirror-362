"""
Asynchronous Composo client
"""

import asyncio
from typing import List, Dict, Any, Optional, Union
from .base import BaseClient
from .types import MessagesType, ToolsType, ResultType
from ..models import EvaluationResponse, BinaryEvaluationResponse
from tenacity import stop_after_attempt, wait_exponential, wait_random, AsyncRetrying


class AsyncComposo(BaseClient):
    """Asynchronous Composo client for high-performance batch evaluations"""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://platform.composo.ai",
        num_retries: int = 1,
        model_core: Optional[str] = None,
        max_concurrent_requests: int = 5,
        timeout: float = 60.0,
    ):
        super().__init__(api_key, base_url, num_retries, model_core, timeout)
        self.max_concurrent_requests = max_concurrent_requests
        self._semaphore = asyncio.Semaphore(max_concurrent_requests)

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - close HTTP client"""
        await self.aclose()

    async def _make_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make async HTTP request with retry logic using tenacity (exponential backoff base 2 + jitter)"""
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(self.num_retries),
            wait=wait_exponential(multiplier=1, min=1, max=60)
            + wait_random(
                0, 1
            ),  # multiplier = 1 means 2x the wait time for each attempt
            reraise=True,
        ):
            with attempt:
                return await self._apost(
                    endpoint="/api/v1/evals/reward",
                    data=request_data,
                    headers=self._build_headers(),
                )

    async def _make_binary_request(
        self, request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Make async binary evaluation HTTP request with retry logic"""

        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(self.num_retries),
            wait=wait_exponential(multiplier=1, min=1, max=60)
            + wait_random(
                0, 1
            ),  # multiplier = 1 means 2x the wait time for each attempt
            reraise=True,  # re-raise the exception if the request fails
        ):
            with attempt:
                return await self._apost(
                    endpoint="/api/v1/evals/binary",
                    data=request_data,
                    headers=self._build_headers(),
                )

    async def _evaluate_single_criterion(
        self,
        messages: MessagesType,
        system: Optional[str],
        tools: ToolsType,
        result: ResultType,
        single_criterion: str,
    ) -> EvaluationResponse:
        """Evaluate a single criterion with semaphore control"""
        async with self._semaphore:
            evaluation_request = self._prepare_evaluation_request(
                messages, system, tools, result, single_criterion
            )
            request_data = evaluation_request.model_dump(exclude_none=True)

            # Patch: always use 'system' field, not 'system_message'
            if "system_message" in request_data:
                request_data["system"] = request_data.pop("system_message")
            else:
                request_data["system"] = None

            # Check if this is binary evaluation
            if self._is_binary_criteria(single_criterion):
                response_data = await self._make_binary_request(request_data)
                # Convert binary response to score format
                binary_response = BinaryEvaluationResponse(**response_data)
                score = 1.0 if binary_response.passed else 0.0
                return EvaluationResponse(
                    score=score, explanation=binary_response.explanation
                )
            else:
                response_data = await self._make_request(request_data)
                return EvaluationResponse.from_dict(response_data)

    async def _evaluate_multiple_criteria(
        self,
        messages: MessagesType,
        system: Optional[str],
        tools: ToolsType,
        result: ResultType,
        criteria: List[str],
    ) -> List[EvaluationResponse]:
        """Evaluate multiple criteria concurrently"""
        tasks = [
            self._evaluate_single_criterion(
                messages, system, tools, result, single_criterion
            )
            for single_criterion in criteria
        ]
        return await asyncio.gather(*tasks)

    async def evaluate(
        self,
        messages: MessagesType,
        system: Optional[str] = None,
        tools: ToolsType = None,
        result: ResultType = None,
        criteria: Optional[Union[str, List[str]]] = None,
    ) -> Union[EvaluationResponse, List[EvaluationResponse]]:
        """
        Evaluate messages with optional criteria

        Args:
            messages: List of chat messages
            system: Optional system message
            tools: Optional tool definitions
            result: Optional LLM result to append to messages
            criteria: Optional evaluation criteria (str or list of str)

        Returns:
            EvaluationResponse or list of EvaluationResponse (if criteria is a list)
        """
        # Convert single criteria to list if needed
        if isinstance(criteria, str):
            criteria = [criteria]
        elif criteria is None:
            criteria = []

        # Handle empty criteria case
        if not criteria:
            # Use default evaluation when no criteria provided
            evaluation_request = self._prepare_evaluation_request(
                messages, system, tools, result, None
            )
            request_data = evaluation_request.model_dump(exclude_none=True)

            # Patch: always use 'system' field, not 'system_message'
            if "system_message" in request_data:
                request_data["system"] = request_data.pop("system_message")
            else:
                request_data["system"] = None

            response_data = await self._make_request(request_data)
            return EvaluationResponse.from_dict(response_data)

        # Always evaluate multiple criteria
        results = await self._evaluate_multiple_criteria(
            messages, system, tools, result, criteria
        )

        # Return single result if only one criteria was provided
        if len(criteria) == 1:
            return results[0]
        else:
            return results
