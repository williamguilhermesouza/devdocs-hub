from devdocs_hub.application.protocols import Response
from devdocs_hub.ingestion.errors import FetchError


class FakeClient:
    def __init__(self, raises: bool = False):
        self.raises = raises

    async def get(self, url: str) -> Response:
        if self.raises:
            raise FetchError

        return Response(url)

