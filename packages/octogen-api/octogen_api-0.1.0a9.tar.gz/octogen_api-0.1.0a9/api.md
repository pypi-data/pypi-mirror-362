# Catalog

Types:

```python
from octogen.api.types import (
    AggregateOffer,
    Audience,
    Brand,
    BreadcrumbList,
    Category,
    ColorInfo,
    ContextEnum,
    Facet,
    FulfillmentInfo,
    Image,
    Offer,
    Offers,
    Organization,
    ProductEnrichment,
    Promotion,
    QuantitativeValue,
    Rating,
    Review,
    SearchToolOutput,
    ThreeDModel,
    VideoObject,
    CatalogUploadFileResponse,
)
```

Methods:

- <code title="get /catalog/agent_search">client.catalog.<a href="./src/octogen/api/resources/catalog.py">agent_search</a>(\*\*<a href="src/octogen/api/types/catalog_agent_search_params.py">params</a>) -> <a href="./src/octogen/api/types/search_tool_output.py">SearchToolOutput</a></code>
- <code title="get /catalog/file/{file_id}">client.catalog.<a href="./src/octogen/api/resources/catalog.py">retrieve_file</a>(file_id) -> object</code>
- <code title="post /catalog/style_and_tags_search">client.catalog.<a href="./src/octogen/api/resources/catalog.py">style_and_tags_search</a>(\*\*<a href="src/octogen/api/types/catalog_style_and_tags_search_params.py">params</a>) -> <a href="./src/octogen/api/types/search_tool_output.py">SearchToolOutput</a></code>
- <code title="post /catalog/text_search">client.catalog.<a href="./src/octogen/api/resources/catalog.py">text_search</a>(\*\*<a href="src/octogen/api/types/catalog_text_search_params.py">params</a>) -> <a href="./src/octogen/api/types/search_tool_output.py">SearchToolOutput</a></code>
- <code title="post /catalog/file_upload">client.catalog.<a href="./src/octogen/api/resources/catalog.py">upload_file</a>(\*\*<a href="src/octogen/api/types/catalog_upload_file_params.py">params</a>) -> <a href="./src/octogen/api/types/catalog_upload_file_response.py">CatalogUploadFileResponse</a></code>
