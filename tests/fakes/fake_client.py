from devdocs_hub.application.protocols import Response
from devdocs_hub.ingestion.errors import FetchError


class FakeClient:
    def __init__(self, raises: bool = False, response: str | None = None):
        self.raises = raises
        self.res = response

    async def get(self, url: str) -> Response:
        if self.raises:
            raise FetchError

        return Response(self.res) if self.res else Response(url)

