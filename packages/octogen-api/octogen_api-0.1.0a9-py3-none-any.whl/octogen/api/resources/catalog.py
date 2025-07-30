# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Mapping, Iterable, Optional, cast
from typing_extensions import Literal

import httpx

from ..types import (
    catalog_text_search_params,
    catalog_upload_file_params,
    catalog_agent_search_params,
    catalog_style_and_tags_search_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven, FileTypes
from .._utils import extract_files, maybe_transform, deepcopy_minimal, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.facet_param import FacetParam
from ..types.search_tool_output import SearchToolOutput
from ..types.catalog_upload_file_response import CatalogUploadFileResponse

__all__ = ["CatalogResource", "AsyncCatalogResource"]


class CatalogResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CatalogResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/octogen-ai/octogen-py-api#accessing-raw-response-data-eg-headers
        """
        return CatalogResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CatalogResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/octogen-ai/octogen-py-api#with_streaming_response
        """
        return CatalogResourceWithStreamingResponse(self)

    def agent_search(
        self,
        *,
        text: str,
        limit: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchToolOutput:
        """
        Search for products using an LLM to generate a TextSearchQuery object that is
        used to search for products in the e-commerce catalog. The LLM will generate the
        fields of the TextSearchQuery object based on input query text.

        Args:
          text: Query text to be input to an LLM to generate a TextSearchQuery object

          limit: The maximum number of results to return from the search.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/catalog/agent_search",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "text": text,
                        "limit": limit,
                    },
                    catalog_agent_search_params.CatalogAgentSearchParams,
                ),
            ),
            cast_to=SearchToolOutput,
        )

    def retrieve_file(
        self,
        file_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Retrieve a file from Google Cloud Storage by file ID.

        Args: file_id: The unique identifier of the file

        Returns: StreamingResponse with the file content and appropriate content type

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return self._get(
            f"/catalog/file/{file_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def style_and_tags_search(
        self,
        *,
        type: str,
        styles: List[str],
        tags: List[str],
        compact_mode: Optional[Literal["compact", "medium"]] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchToolOutput:
        """
        Search for products using the Octogen's search agent.

        Args: type: The type of product to search for styles: List of styles to search
        for tags: List of tags to search for limit: Maximum number of results to return.
        The default is 10.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/catalog/style_and_tags_search",
            body=maybe_transform(
                {
                    "styles": styles,
                    "tags": tags,
                },
                catalog_style_and_tags_search_params.CatalogStyleAndTagsSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "type": type,
                        "compact_mode": compact_mode,
                        "limit": limit,
                    },
                    catalog_style_and_tags_search_params.CatalogStyleAndTagsSearchParams,
                ),
            ),
            cast_to=SearchToolOutput,
        )

    def text_search(
        self,
        *,
        text: str,
        exclusion_facets: Optional[Iterable[FacetParam]] | NotGiven = NOT_GIVEN,
        facets: Optional[Iterable[FacetParam]] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        price_max: Optional[float] | NotGiven = NOT_GIVEN,
        price_min: Optional[float] | NotGiven = NOT_GIVEN,
        ranking_embedding_columns: Optional[List[Literal["embedding", "style_embedding", "tags_embedding"]]]
        | NotGiven = NOT_GIVEN,
        ranking_text: Optional[str] | NotGiven = NOT_GIVEN,
        retrieval_embedding_columns: Optional[List[Literal["embedding", "style_embedding", "tags_embedding"]]]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchToolOutput:
        """Search for products in the Octogen e-commerce catalog.

        The search is performed
        using text embedding similarity on the input query text with the pre-computed
        product embeddings. The additional parameters are used filters to narrow down
        the search results. The number of results is determined by the limit parameter.

        Args:
          text: The text is converted to a vector embedding and used to search for products in
              the e-commerce catalog with pre-computed product embeddings. It will be matched
              against the embeddings from retrieval_embedding_columns during retrieval.

          exclusion_facets: Facets that will be excluded from the search results.

          facets: The search results will be filtered by the specified facets.

          limit: The maximum number of results to return from the search. The default is 10.

          price_max: The products will be filtered to have a price less than or equal to the
              specified value.

          price_min: The products will be filtered to have a price greater than or equal to the
              specified value.

          ranking_embedding_columns: The columns to use for the ranking embeddings. If not specified, defaults to
              ['embedding']. Pick the column that best corresponds to the `ranking_text`
              parameter.

          ranking_text: The text is converted to a vector embedding and used to rank the search results.
              It will be matched against the embeddings from ranking_embedding_columns during
              ranking.

          retrieval_embedding_columns: The columns to use for the retrieval embeddings. If not specified, defaults to
              ['embedding']. Pick the column that best corresponds to the `text` parameter.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/catalog/text_search",
            body=maybe_transform(
                {
                    "text": text,
                    "exclusion_facets": exclusion_facets,
                    "facets": facets,
                    "limit": limit,
                    "price_max": price_max,
                    "price_min": price_min,
                    "ranking_embedding_columns": ranking_embedding_columns,
                    "ranking_text": ranking_text,
                    "retrieval_embedding_columns": retrieval_embedding_columns,
                },
                catalog_text_search_params.CatalogTextSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SearchToolOutput,
        )

    def upload_file(
        self,
        *,
        file: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CatalogUploadFileResponse:
        """
        Upload an image file to Google Cloud Storage.

        Args: file: The file to upload

        Returns: FileUploadResponse with the file ID and URL

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal({"file": file})
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/catalog/file_upload",
            body=maybe_transform(body, catalog_upload_file_params.CatalogUploadFileParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CatalogUploadFileResponse,
        )


class AsyncCatalogResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCatalogResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/octogen-ai/octogen-py-api#accessing-raw-response-data-eg-headers
        """
        return AsyncCatalogResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCatalogResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/octogen-ai/octogen-py-api#with_streaming_response
        """
        return AsyncCatalogResourceWithStreamingResponse(self)

    async def agent_search(
        self,
        *,
        text: str,
        limit: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchToolOutput:
        """
        Search for products using an LLM to generate a TextSearchQuery object that is
        used to search for products in the e-commerce catalog. The LLM will generate the
        fields of the TextSearchQuery object based on input query text.

        Args:
          text: Query text to be input to an LLM to generate a TextSearchQuery object

          limit: The maximum number of results to return from the search.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/catalog/agent_search",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "text": text,
                        "limit": limit,
                    },
                    catalog_agent_search_params.CatalogAgentSearchParams,
                ),
            ),
            cast_to=SearchToolOutput,
        )

    async def retrieve_file(
        self,
        file_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Retrieve a file from Google Cloud Storage by file ID.

        Args: file_id: The unique identifier of the file

        Returns: StreamingResponse with the file content and appropriate content type

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return await self._get(
            f"/catalog/file/{file_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def style_and_tags_search(
        self,
        *,
        type: str,
        styles: List[str],
        tags: List[str],
        compact_mode: Optional[Literal["compact", "medium"]] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchToolOutput:
        """
        Search for products using the Octogen's search agent.

        Args: type: The type of product to search for styles: List of styles to search
        for tags: List of tags to search for limit: Maximum number of results to return.
        The default is 10.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/catalog/style_and_tags_search",
            body=await async_maybe_transform(
                {
                    "styles": styles,
                    "tags": tags,
                },
                catalog_style_and_tags_search_params.CatalogStyleAndTagsSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "type": type,
                        "compact_mode": compact_mode,
                        "limit": limit,
                    },
                    catalog_style_and_tags_search_params.CatalogStyleAndTagsSearchParams,
                ),
            ),
            cast_to=SearchToolOutput,
        )

    async def text_search(
        self,
        *,
        text: str,
        exclusion_facets: Optional[Iterable[FacetParam]] | NotGiven = NOT_GIVEN,
        facets: Optional[Iterable[FacetParam]] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        price_max: Optional[float] | NotGiven = NOT_GIVEN,
        price_min: Optional[float] | NotGiven = NOT_GIVEN,
        ranking_embedding_columns: Optional[List[Literal["embedding", "style_embedding", "tags_embedding"]]]
        | NotGiven = NOT_GIVEN,
        ranking_text: Optional[str] | NotGiven = NOT_GIVEN,
        retrieval_embedding_columns: Optional[List[Literal["embedding", "style_embedding", "tags_embedding"]]]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchToolOutput:
        """Search for products in the Octogen e-commerce catalog.

        The search is performed
        using text embedding similarity on the input query text with the pre-computed
        product embeddings. The additional parameters are used filters to narrow down
        the search results. The number of results is determined by the limit parameter.

        Args:
          text: The text is converted to a vector embedding and used to search for products in
              the e-commerce catalog with pre-computed product embeddings. It will be matched
              against the embeddings from retrieval_embedding_columns during retrieval.

          exclusion_facets: Facets that will be excluded from the search results.

          facets: The search results will be filtered by the specified facets.

          limit: The maximum number of results to return from the search. The default is 10.

          price_max: The products will be filtered to have a price less than or equal to the
              specified value.

          price_min: The products will be filtered to have a price greater than or equal to the
              specified value.

          ranking_embedding_columns: The columns to use for the ranking embeddings. If not specified, defaults to
              ['embedding']. Pick the column that best corresponds to the `ranking_text`
              parameter.

          ranking_text: The text is converted to a vector embedding and used to rank the search results.
              It will be matched against the embeddings from ranking_embedding_columns during
              ranking.

          retrieval_embedding_columns: The columns to use for the retrieval embeddings. If not specified, defaults to
              ['embedding']. Pick the column that best corresponds to the `text` parameter.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/catalog/text_search",
            body=await async_maybe_transform(
                {
                    "text": text,
                    "exclusion_facets": exclusion_facets,
                    "facets": facets,
                    "limit": limit,
                    "price_max": price_max,
                    "price_min": price_min,
                    "ranking_embedding_columns": ranking_embedding_columns,
                    "ranking_text": ranking_text,
                    "retrieval_embedding_columns": retrieval_embedding_columns,
                },
                catalog_text_search_params.CatalogTextSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SearchToolOutput,
        )

    async def upload_file(
        self,
        *,
        file: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CatalogUploadFileResponse:
        """
        Upload an image file to Google Cloud Storage.

        Args: file: The file to upload

        Returns: FileUploadResponse with the file ID and URL

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal({"file": file})
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/catalog/file_upload",
            body=await async_maybe_transform(body, catalog_upload_file_params.CatalogUploadFileParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CatalogUploadFileResponse,
        )


class CatalogResourceWithRawResponse:
    def __init__(self, catalog: CatalogResource) -> None:
        self._catalog = catalog

        self.agent_search = to_raw_response_wrapper(
            catalog.agent_search,
        )
        self.retrieve_file = to_raw_response_wrapper(
            catalog.retrieve_file,
        )
        self.style_and_tags_search = to_raw_response_wrapper(
            catalog.style_and_tags_search,
        )
        self.text_search = to_raw_response_wrapper(
            catalog.text_search,
        )
        self.upload_file = to_raw_response_wrapper(
            catalog.upload_file,
        )


class AsyncCatalogResourceWithRawResponse:
    def __init__(self, catalog: AsyncCatalogResource) -> None:
        self._catalog = catalog

        self.agent_search = async_to_raw_response_wrapper(
            catalog.agent_search,
        )
        self.retrieve_file = async_to_raw_response_wrapper(
            catalog.retrieve_file,
        )
        self.style_and_tags_search = async_to_raw_response_wrapper(
            catalog.style_and_tags_search,
        )
        self.text_search = async_to_raw_response_wrapper(
            catalog.text_search,
        )
        self.upload_file = async_to_raw_response_wrapper(
            catalog.upload_file,
        )


class CatalogResourceWithStreamingResponse:
    def __init__(self, catalog: CatalogResource) -> None:
        self._catalog = catalog

        self.agent_search = to_streamed_response_wrapper(
            catalog.agent_search,
        )
        self.retrieve_file = to_streamed_response_wrapper(
            catalog.retrieve_file,
        )
        self.style_and_tags_search = to_streamed_response_wrapper(
            catalog.style_and_tags_search,
        )
        self.text_search = to_streamed_response_wrapper(
            catalog.text_search,
        )
        self.upload_file = to_streamed_response_wrapper(
            catalog.upload_file,
        )


class AsyncCatalogResourceWithStreamingResponse:
    def __init__(self, catalog: AsyncCatalogResource) -> None:
        self._catalog = catalog

        self.agent_search = async_to_streamed_response_wrapper(
            catalog.agent_search,
        )
        self.retrieve_file = async_to_streamed_response_wrapper(
            catalog.retrieve_file,
        )
        self.style_and_tags_search = async_to_streamed_response_wrapper(
            catalog.style_and_tags_search,
        )
        self.text_search = async_to_streamed_response_wrapper(
            catalog.text_search,
        )
        self.upload_file = async_to_streamed_response_wrapper(
            catalog.upload_file,
        )
