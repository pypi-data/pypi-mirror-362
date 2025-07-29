# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal

import httpx

from .jobs import (
    JobsResource,
    AsyncJobsResource,
    JobsResourceWithRawResponse,
    AsyncJobsResourceWithRawResponse,
    JobsResourceWithStreamingResponse,
    AsyncJobsResourceWithStreamingResponse,
)
from ...types import (
    vrp_demo_params,
    vrp_sync_params,
    vrp_solve_params,
    vrp_suggest_params,
    vrp_evaluate_params,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform, strip_not_given, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.options_param import OptionsParam
from ...types.weights_param import WeightsParam
from ...types.on_route_request import OnRouteRequest
from ...types.solvice_status_job import SolviceStatusJob
from ...types.vrp.on_route_response import OnRouteResponse

__all__ = ["VrpResource", "AsyncVrpResource"]


class VrpResource(SyncAPIResource):
    @cached_property
    def jobs(self) -> JobsResource:
        return JobsResource(self._client)

    @cached_property
    def with_raw_response(self) -> VrpResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/solvice/vrp-solver-sdk-python#accessing-raw-response-data-eg-headers
        """
        return VrpResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VrpResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/solvice/vrp-solver-sdk-python#with_streaming_response
        """
        return VrpResourceWithStreamingResponse(self)

    def demo(
        self,
        *,
        geolocation: Optional[str] | NotGiven = NOT_GIVEN,
        jobs: Optional[int] | NotGiven = NOT_GIVEN,
        radius: Optional[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OnRouteRequest:
        """
        Demo of random generated VRP instance

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v2/vrp/demo",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "geolocation": geolocation,
                        "jobs": jobs,
                        "radius": radius,
                    },
                    vrp_demo_params.VrpDemoParams,
                ),
            ),
            cast_to=OnRouteRequest,
        )

    def evaluate(
        self,
        *,
        jobs: Iterable[vrp_evaluate_params.Job],
        resources: Iterable[vrp_evaluate_params.Resource],
        hook: Optional[str] | NotGiven = NOT_GIVEN,
        label: Optional[str] | NotGiven = NOT_GIVEN,
        options: Optional[OptionsParam] | NotGiven = NOT_GIVEN,
        relations: Optional[Iterable[vrp_evaluate_params.Relation]] | NotGiven = NOT_GIVEN,
        weights: Optional[WeightsParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SolviceStatusJob:
        """
        Will trigger the evaluation run asynchronously.

        Args:
          jobs: List of Jobs

          resources: List of Resources

          hook: Webhook endpoint to receive POST request with the id.

          options: Options to tweak the routing engine

          weights: OnRoute Weights

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v2/vrp/evaluate",
            body=maybe_transform(
                {
                    "jobs": jobs,
                    "resources": resources,
                    "hook": hook,
                    "label": label,
                    "options": options,
                    "relations": relations,
                    "weights": weights,
                },
                vrp_evaluate_params.VrpEvaluateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SolviceStatusJob,
        )

    def solve(
        self,
        *,
        jobs: Iterable[vrp_solve_params.Job],
        resources: Iterable[vrp_solve_params.Resource],
        millis: Optional[str] | NotGiven = NOT_GIVEN,
        hook: Optional[str] | NotGiven = NOT_GIVEN,
        label: Optional[str] | NotGiven = NOT_GIVEN,
        options: Optional[OptionsParam] | NotGiven = NOT_GIVEN,
        relations: Optional[Iterable[vrp_solve_params.Relation]] | NotGiven = NOT_GIVEN,
        weights: Optional[WeightsParam] | NotGiven = NOT_GIVEN,
        instance: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SolviceStatusJob:
        """
        Will trigger the solver run asynchronously.

        Args:
          jobs: List of Jobs

          resources: List of Resources

          hook: Webhook endpoint to receive POST request with the id.

          options: Options to tweak the routing engine

          weights: OnRoute Weights

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"instance": instance}), **(extra_headers or {})}
        return self._post(
            "/v2/vrp/solve",
            body=maybe_transform(
                {
                    "jobs": jobs,
                    "resources": resources,
                    "hook": hook,
                    "label": label,
                    "options": options,
                    "relations": relations,
                    "weights": weights,
                },
                vrp_solve_params.VrpSolveParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"millis": millis}, vrp_solve_params.VrpSolveParams),
            ),
            cast_to=SolviceStatusJob,
        )

    def suggest(
        self,
        *,
        jobs: Iterable[vrp_suggest_params.Job],
        resources: Iterable[vrp_suggest_params.Resource],
        millis: Optional[str] | NotGiven = NOT_GIVEN,
        hook: Optional[str] | NotGiven = NOT_GIVEN,
        label: Optional[str] | NotGiven = NOT_GIVEN,
        options: Optional[OptionsParam] | NotGiven = NOT_GIVEN,
        relations: Optional[Iterable[vrp_suggest_params.Relation]] | NotGiven = NOT_GIVEN,
        weights: Optional[WeightsParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SolviceStatusJob:
        """
        Will return the suggest moves for an unassigned job.

        Args:
          jobs: List of Jobs

          resources: List of Resources

          hook: Webhook endpoint to receive POST request with the id.

          options: Options to tweak the routing engine

          weights: OnRoute Weights

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v2/vrp/suggest",
            body=maybe_transform(
                {
                    "jobs": jobs,
                    "resources": resources,
                    "hook": hook,
                    "label": label,
                    "options": options,
                    "relations": relations,
                    "weights": weights,
                },
                vrp_suggest_params.VrpSuggestParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"millis": millis}, vrp_suggest_params.VrpSuggestParams),
            ),
            cast_to=SolviceStatusJob,
        )

    def sync(
        self,
        operation: Literal["SOLVE", "SUGGEST", "EVALUATE"],
        *,
        jobs: Iterable[vrp_sync_params.Job],
        resources: Iterable[vrp_sync_params.Resource],
        millis: Optional[str] | NotGiven = NOT_GIVEN,
        hook: Optional[str] | NotGiven = NOT_GIVEN,
        label: Optional[str] | NotGiven = NOT_GIVEN,
        options: Optional[OptionsParam] | NotGiven = NOT_GIVEN,
        relations: Optional[Iterable[vrp_sync_params.Relation]] | NotGiven = NOT_GIVEN,
        weights: Optional[WeightsParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OnRouteResponse:
        """
        Synchronous (solve, evaluate, suggest) operation for low latency results

        Args:
          jobs: List of Jobs

          resources: List of Resources

          hook: Webhook endpoint to receive POST request with the id.

          options: Options to tweak the routing engine

          weights: OnRoute Weights

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not operation:
            raise ValueError(f"Expected a non-empty value for `operation` but received {operation!r}")
        return self._post(
            f"/v2/vrp/sync/{operation}",
            body=maybe_transform(
                {
                    "jobs": jobs,
                    "resources": resources,
                    "hook": hook,
                    "label": label,
                    "options": options,
                    "relations": relations,
                    "weights": weights,
                },
                vrp_sync_params.VrpSyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"millis": millis}, vrp_sync_params.VrpSyncParams),
            ),
            cast_to=OnRouteResponse,
        )


class AsyncVrpResource(AsyncAPIResource):
    @cached_property
    def jobs(self) -> AsyncJobsResource:
        return AsyncJobsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncVrpResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/solvice/vrp-solver-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncVrpResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVrpResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/solvice/vrp-solver-sdk-python#with_streaming_response
        """
        return AsyncVrpResourceWithStreamingResponse(self)

    async def demo(
        self,
        *,
        geolocation: Optional[str] | NotGiven = NOT_GIVEN,
        jobs: Optional[int] | NotGiven = NOT_GIVEN,
        radius: Optional[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OnRouteRequest:
        """
        Demo of random generated VRP instance

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v2/vrp/demo",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "geolocation": geolocation,
                        "jobs": jobs,
                        "radius": radius,
                    },
                    vrp_demo_params.VrpDemoParams,
                ),
            ),
            cast_to=OnRouteRequest,
        )

    async def evaluate(
        self,
        *,
        jobs: Iterable[vrp_evaluate_params.Job],
        resources: Iterable[vrp_evaluate_params.Resource],
        hook: Optional[str] | NotGiven = NOT_GIVEN,
        label: Optional[str] | NotGiven = NOT_GIVEN,
        options: Optional[OptionsParam] | NotGiven = NOT_GIVEN,
        relations: Optional[Iterable[vrp_evaluate_params.Relation]] | NotGiven = NOT_GIVEN,
        weights: Optional[WeightsParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SolviceStatusJob:
        """
        Will trigger the evaluation run asynchronously.

        Args:
          jobs: List of Jobs

          resources: List of Resources

          hook: Webhook endpoint to receive POST request with the id.

          options: Options to tweak the routing engine

          weights: OnRoute Weights

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v2/vrp/evaluate",
            body=await async_maybe_transform(
                {
                    "jobs": jobs,
                    "resources": resources,
                    "hook": hook,
                    "label": label,
                    "options": options,
                    "relations": relations,
                    "weights": weights,
                },
                vrp_evaluate_params.VrpEvaluateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SolviceStatusJob,
        )

    async def solve(
        self,
        *,
        jobs: Iterable[vrp_solve_params.Job],
        resources: Iterable[vrp_solve_params.Resource],
        millis: Optional[str] | NotGiven = NOT_GIVEN,
        hook: Optional[str] | NotGiven = NOT_GIVEN,
        label: Optional[str] | NotGiven = NOT_GIVEN,
        options: Optional[OptionsParam] | NotGiven = NOT_GIVEN,
        relations: Optional[Iterable[vrp_solve_params.Relation]] | NotGiven = NOT_GIVEN,
        weights: Optional[WeightsParam] | NotGiven = NOT_GIVEN,
        instance: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SolviceStatusJob:
        """
        Will trigger the solver run asynchronously.

        Args:
          jobs: List of Jobs

          resources: List of Resources

          hook: Webhook endpoint to receive POST request with the id.

          options: Options to tweak the routing engine

          weights: OnRoute Weights

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"instance": instance}), **(extra_headers or {})}
        return await self._post(
            "/v2/vrp/solve",
            body=await async_maybe_transform(
                {
                    "jobs": jobs,
                    "resources": resources,
                    "hook": hook,
                    "label": label,
                    "options": options,
                    "relations": relations,
                    "weights": weights,
                },
                vrp_solve_params.VrpSolveParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"millis": millis}, vrp_solve_params.VrpSolveParams),
            ),
            cast_to=SolviceStatusJob,
        )

    async def suggest(
        self,
        *,
        jobs: Iterable[vrp_suggest_params.Job],
        resources: Iterable[vrp_suggest_params.Resource],
        millis: Optional[str] | NotGiven = NOT_GIVEN,
        hook: Optional[str] | NotGiven = NOT_GIVEN,
        label: Optional[str] | NotGiven = NOT_GIVEN,
        options: Optional[OptionsParam] | NotGiven = NOT_GIVEN,
        relations: Optional[Iterable[vrp_suggest_params.Relation]] | NotGiven = NOT_GIVEN,
        weights: Optional[WeightsParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SolviceStatusJob:
        """
        Will return the suggest moves for an unassigned job.

        Args:
          jobs: List of Jobs

          resources: List of Resources

          hook: Webhook endpoint to receive POST request with the id.

          options: Options to tweak the routing engine

          weights: OnRoute Weights

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v2/vrp/suggest",
            body=await async_maybe_transform(
                {
                    "jobs": jobs,
                    "resources": resources,
                    "hook": hook,
                    "label": label,
                    "options": options,
                    "relations": relations,
                    "weights": weights,
                },
                vrp_suggest_params.VrpSuggestParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"millis": millis}, vrp_suggest_params.VrpSuggestParams),
            ),
            cast_to=SolviceStatusJob,
        )

    async def sync(
        self,
        operation: Literal["SOLVE", "SUGGEST", "EVALUATE"],
        *,
        jobs: Iterable[vrp_sync_params.Job],
        resources: Iterable[vrp_sync_params.Resource],
        millis: Optional[str] | NotGiven = NOT_GIVEN,
        hook: Optional[str] | NotGiven = NOT_GIVEN,
        label: Optional[str] | NotGiven = NOT_GIVEN,
        options: Optional[OptionsParam] | NotGiven = NOT_GIVEN,
        relations: Optional[Iterable[vrp_sync_params.Relation]] | NotGiven = NOT_GIVEN,
        weights: Optional[WeightsParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OnRouteResponse:
        """
        Synchronous (solve, evaluate, suggest) operation for low latency results

        Args:
          jobs: List of Jobs

          resources: List of Resources

          hook: Webhook endpoint to receive POST request with the id.

          options: Options to tweak the routing engine

          weights: OnRoute Weights

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not operation:
            raise ValueError(f"Expected a non-empty value for `operation` but received {operation!r}")
        return await self._post(
            f"/v2/vrp/sync/{operation}",
            body=await async_maybe_transform(
                {
                    "jobs": jobs,
                    "resources": resources,
                    "hook": hook,
                    "label": label,
                    "options": options,
                    "relations": relations,
                    "weights": weights,
                },
                vrp_sync_params.VrpSyncParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"millis": millis}, vrp_sync_params.VrpSyncParams),
            ),
            cast_to=OnRouteResponse,
        )


class VrpResourceWithRawResponse:
    def __init__(self, vrp: VrpResource) -> None:
        self._vrp = vrp

        self.demo = to_raw_response_wrapper(
            vrp.demo,
        )
        self.evaluate = to_raw_response_wrapper(
            vrp.evaluate,
        )
        self.solve = to_raw_response_wrapper(
            vrp.solve,
        )
        self.suggest = to_raw_response_wrapper(
            vrp.suggest,
        )
        self.sync = to_raw_response_wrapper(
            vrp.sync,
        )

    @cached_property
    def jobs(self) -> JobsResourceWithRawResponse:
        return JobsResourceWithRawResponse(self._vrp.jobs)


class AsyncVrpResourceWithRawResponse:
    def __init__(self, vrp: AsyncVrpResource) -> None:
        self._vrp = vrp

        self.demo = async_to_raw_response_wrapper(
            vrp.demo,
        )
        self.evaluate = async_to_raw_response_wrapper(
            vrp.evaluate,
        )
        self.solve = async_to_raw_response_wrapper(
            vrp.solve,
        )
        self.suggest = async_to_raw_response_wrapper(
            vrp.suggest,
        )
        self.sync = async_to_raw_response_wrapper(
            vrp.sync,
        )

    @cached_property
    def jobs(self) -> AsyncJobsResourceWithRawResponse:
        return AsyncJobsResourceWithRawResponse(self._vrp.jobs)


class VrpResourceWithStreamingResponse:
    def __init__(self, vrp: VrpResource) -> None:
        self._vrp = vrp

        self.demo = to_streamed_response_wrapper(
            vrp.demo,
        )
        self.evaluate = to_streamed_response_wrapper(
            vrp.evaluate,
        )
        self.solve = to_streamed_response_wrapper(
            vrp.solve,
        )
        self.suggest = to_streamed_response_wrapper(
            vrp.suggest,
        )
        self.sync = to_streamed_response_wrapper(
            vrp.sync,
        )

    @cached_property
    def jobs(self) -> JobsResourceWithStreamingResponse:
        return JobsResourceWithStreamingResponse(self._vrp.jobs)


class AsyncVrpResourceWithStreamingResponse:
    def __init__(self, vrp: AsyncVrpResource) -> None:
        self._vrp = vrp

        self.demo = async_to_streamed_response_wrapper(
            vrp.demo,
        )
        self.evaluate = async_to_streamed_response_wrapper(
            vrp.evaluate,
        )
        self.solve = async_to_streamed_response_wrapper(
            vrp.solve,
        )
        self.suggest = async_to_streamed_response_wrapper(
            vrp.suggest,
        )
        self.sync = async_to_streamed_response_wrapper(
            vrp.sync,
        )

    @cached_property
    def jobs(self) -> AsyncJobsResourceWithStreamingResponse:
        return AsyncJobsResourceWithStreamingResponse(self._vrp.jobs)
