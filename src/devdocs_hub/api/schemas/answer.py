from pydantic import BaseModel, ConfigDict


class AnswerChunk(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    document_id: int
    position: int
    content: str


class AnswerResponse(BaseModel):
    answer: str
    chunks: list[AnswerChunk]
