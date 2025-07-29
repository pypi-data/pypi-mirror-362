from pydantic import BaseModel, Field


class DetectionRequest(BaseModel):
    image: bytes = Field(..., description="Base64 encoded image data")


class DetectionResponse(BaseModel):
    result: float = Field(
        ...,
        description="Detection result score. A number between 0 and 1, where 1 indicates a high confidence in the detection.",
    )


class DetectionError(BaseModel):
    error: str = Field(
        ...,
        description="Error message describing the issue with the detection request.",
    )
    details: str | None = Field(
        ..., description="Optional additional details about the error."
    )
