# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from octogen.api import OctogenAPI, AsyncOctogenAPI
from tests.utils import assert_matches_type
from octogen.api.types import (
    SearchToolOutput,
    CatalogUploadFileResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCatalog:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_agent_search(self, client: OctogenAPI) -> None:
        catalog = client.catalog.agent_search(
            text="text",
        )
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_agent_search_with_all_params(self, client: OctogenAPI) -> None:
        catalog = client.catalog.agent_search(
            text="text",
            limit=0,
        )
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_agent_search(self, client: OctogenAPI) -> None:
        response = client.catalog.with_raw_response.agent_search(
            text="text",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        catalog = response.parse()
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_agent_search(self, client: OctogenAPI) -> None:
        with client.catalog.with_streaming_response.agent_search(
            text="text",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            catalog = response.parse()
            assert_matches_type(SearchToolOutput, catalog, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_file(self, client: OctogenAPI) -> None:
        catalog = client.catalog.retrieve_file(
            "file_id",
        )
        assert_matches_type(object, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_file(self, client: OctogenAPI) -> None:
        response = client.catalog.with_raw_response.retrieve_file(
            "file_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        catalog = response.parse()
        assert_matches_type(object, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_file(self, client: OctogenAPI) -> None:
        with client.catalog.with_streaming_response.retrieve_file(
            "file_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            catalog = response.parse()
            assert_matches_type(object, catalog, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_file(self, client: OctogenAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            client.catalog.with_raw_response.retrieve_file(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_style_and_tags_search(self, client: OctogenAPI) -> None:
        catalog = client.catalog.style_and_tags_search(
            type="type",
            styles=["string"],
            tags=["string"],
        )
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_style_and_tags_search_with_all_params(self, client: OctogenAPI) -> None:
        catalog = client.catalog.style_and_tags_search(
            type="type",
            styles=["string"],
            tags=["string"],
            compact_mode="compact",
            limit=0,
        )
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_style_and_tags_search(self, client: OctogenAPI) -> None:
        response = client.catalog.with_raw_response.style_and_tags_search(
            type="type",
            styles=["string"],
            tags=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        catalog = response.parse()
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_style_and_tags_search(self, client: OctogenAPI) -> None:
        with client.catalog.with_streaming_response.style_and_tags_search(
            type="type",
            styles=["string"],
            tags=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            catalog = response.parse()
            assert_matches_type(SearchToolOutput, catalog, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_text_search(self, client: OctogenAPI) -> None:
        catalog = client.catalog.text_search(
            text="text",
        )
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_text_search_with_all_params(self, client: OctogenAPI) -> None:
        catalog = client.catalog.text_search(
            text="text",
            exclusion_facets=[
                {
                    "name": "brand_name",
                    "values": ["string"],
                }
            ],
            facets=[
                {
                    "name": "brand_name",
                    "values": ["string"],
                }
            ],
            limit=0,
            price_max=0,
            price_min=0,
            ranking_embedding_columns=["embedding"],
            ranking_text="ranking_text",
            retrieval_embedding_columns=["embedding"],
        )
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_text_search(self, client: OctogenAPI) -> None:
        response = client.catalog.with_raw_response.text_search(
            text="text",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        catalog = response.parse()
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_text_search(self, client: OctogenAPI) -> None:
        with client.catalog.with_streaming_response.text_search(
            text="text",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            catalog = response.parse()
            assert_matches_type(SearchToolOutput, catalog, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_upload_file(self, client: OctogenAPI) -> None:
        catalog = client.catalog.upload_file(
            file=b"raw file contents",
        )
        assert_matches_type(CatalogUploadFileResponse, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_upload_file(self, client: OctogenAPI) -> None:
        response = client.catalog.with_raw_response.upload_file(
            file=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        catalog = response.parse()
        assert_matches_type(CatalogUploadFileResponse, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_upload_file(self, client: OctogenAPI) -> None:
        with client.catalog.with_streaming_response.upload_file(
            file=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            catalog = response.parse()
            assert_matches_type(CatalogUploadFileResponse, catalog, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCatalog:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_agent_search(self, async_client: AsyncOctogenAPI) -> None:
        catalog = await async_client.catalog.agent_search(
            text="text",
        )
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_agent_search_with_all_params(self, async_client: AsyncOctogenAPI) -> None:
        catalog = await async_client.catalog.agent_search(
            text="text",
            limit=0,
        )
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_agent_search(self, async_client: AsyncOctogenAPI) -> None:
        response = await async_client.catalog.with_raw_response.agent_search(
            text="text",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        catalog = await response.parse()
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_agent_search(self, async_client: AsyncOctogenAPI) -> None:
        async with async_client.catalog.with_streaming_response.agent_search(
            text="text",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            catalog = await response.parse()
            assert_matches_type(SearchToolOutput, catalog, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_file(self, async_client: AsyncOctogenAPI) -> None:
        catalog = await async_client.catalog.retrieve_file(
            "file_id",
        )
        assert_matches_type(object, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_file(self, async_client: AsyncOctogenAPI) -> None:
        response = await async_client.catalog.with_raw_response.retrieve_file(
            "file_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        catalog = await response.parse()
        assert_matches_type(object, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_file(self, async_client: AsyncOctogenAPI) -> None:
        async with async_client.catalog.with_streaming_response.retrieve_file(
            "file_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            catalog = await response.parse()
            assert_matches_type(object, catalog, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_file(self, async_client: AsyncOctogenAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            await async_client.catalog.with_raw_response.retrieve_file(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_style_and_tags_search(self, async_client: AsyncOctogenAPI) -> None:
        catalog = await async_client.catalog.style_and_tags_search(
            type="type",
            styles=["string"],
            tags=["string"],
        )
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_style_and_tags_search_with_all_params(self, async_client: AsyncOctogenAPI) -> None:
        catalog = await async_client.catalog.style_and_tags_search(
            type="type",
            styles=["string"],
            tags=["string"],
            compact_mode="compact",
            limit=0,
        )
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_style_and_tags_search(self, async_client: AsyncOctogenAPI) -> None:
        response = await async_client.catalog.with_raw_response.style_and_tags_search(
            type="type",
            styles=["string"],
            tags=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        catalog = await response.parse()
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_style_and_tags_search(self, async_client: AsyncOctogenAPI) -> None:
        async with async_client.catalog.with_streaming_response.style_and_tags_search(
            type="type",
            styles=["string"],
            tags=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            catalog = await response.parse()
            assert_matches_type(SearchToolOutput, catalog, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_text_search(self, async_client: AsyncOctogenAPI) -> None:
        catalog = await async_client.catalog.text_search(
            text="text",
        )
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_text_search_with_all_params(self, async_client: AsyncOctogenAPI) -> None:
        catalog = await async_client.catalog.text_search(
            text="text",
            exclusion_facets=[
                {
                    "name": "brand_name",
                    "values": ["string"],
                }
            ],
            facets=[
                {
                    "name": "brand_name",
                    "values": ["string"],
                }
            ],
            limit=0,
            price_max=0,
            price_min=0,
            ranking_embedding_columns=["embedding"],
            ranking_text="ranking_text",
            retrieval_embedding_columns=["embedding"],
        )
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_text_search(self, async_client: AsyncOctogenAPI) -> None:
        response = await async_client.catalog.with_raw_response.text_search(
            text="text",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        catalog = await response.parse()
        assert_matches_type(SearchToolOutput, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_text_search(self, async_client: AsyncOctogenAPI) -> None:
        async with async_client.catalog.with_streaming_response.text_search(
            text="text",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            catalog = await response.parse()
            assert_matches_type(SearchToolOutput, catalog, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_upload_file(self, async_client: AsyncOctogenAPI) -> None:
        catalog = await async_client.catalog.upload_file(
            file=b"raw file contents",
        )
        assert_matches_type(CatalogUploadFileResponse, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_upload_file(self, async_client: AsyncOctogenAPI) -> None:
        response = await async_client.catalog.with_raw_response.upload_file(
            file=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        catalog = await response.parse()
        assert_matches_type(CatalogUploadFileResponse, catalog, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_upload_file(self, async_client: AsyncOctogenAPI) -> None:
        async with async_client.catalog.with_streaming_response.upload_file(
            file=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            catalog = await response.parse()
            assert_matches_type(CatalogUploadFileResponse, catalog, path=["response"])

        assert cast(Any, response.is_closed) is True
