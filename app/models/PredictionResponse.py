from typing import List

from pydantic import BaseModel


class ReadabilityMetrics(BaseModel):
    vdb: float
    tokens: int
    gulpease: float
    fleschVacca: float


class Paragraph(BaseModel):
    text: str
    readabilityMetrics: ReadabilityMetrics


class PredictedParagraph(Paragraph):
    similarityScore: float


class PredictionResult(BaseModel):
    cleanedParagraph: Paragraph
    simplifiedParagraphs: List[PredictedParagraph]
