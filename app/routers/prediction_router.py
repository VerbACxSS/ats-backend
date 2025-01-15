import logging
from typing import List

from fastapi import APIRouter, HTTPException

from ..models.PredictionRequest import PredictionRequest, Model
from ..models.PredictionResponse import PredictionResult, Paragraph, PredictedParagraph
from ..services.prediction_service import PredictionService
from ..services.cleaner_service import CleanerService
from ..services.similarity_service import SimilarityService
from ..services.readability_service import ReadabilityService

# Initialize logging
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

router = APIRouter()

cleaner_service = CleanerService()
prediction_service = PredictionService()
similarity_service = SimilarityService()
readability_service = ReadabilityService()


@router.post("/", response_model=List[PredictionResult])
async def predict(request: PredictionRequest):
    try:
        LOGGER.info(request)

        prediction_results = []

        for paragraph in request.paragraphs:
            cleaned_paragraph = cleaner_service.clean_text(paragraph)

            # Skip empty paragraphs
            if len(cleaned_paragraph) == 0:
                continue

            # Predict simplified paragraph
            simplified_paragraphs = []
            if request.model == Model.mt5_small:
                simplified_paragraphs = prediction_service.predict_mt5_small(cleaned_paragraph)
            elif request.model == Model.umt5_small:
                simplified_paragraphs = prediction_service.predict_umt5_small(cleaned_paragraph)
            elif request.model == Model.gpt2_small_italian:
                simplified_paragraphs = prediction_service.predict_gpt2_small_italian(cleaned_paragraph)
            else:
                raise HTTPException(status_code=400, detail="Model not supported")

            predicted_paragraphs = []
            for simplified_paragraph in simplified_paragraphs:
                predicted_paragraphs.append(PredictedParagraph(
                    text=simplified_paragraph,
                    similarityScore=similarity_service.perform_similarity_analysis(cleaned_paragraph, simplified_paragraph),
                    readabilityMetrics=readability_service.perform_readability_analysis(simplified_paragraph)
                ))

            # sort by similarity score
            predicted_paragraphs.sort(key=lambda x: x.similarityScore, reverse=True)

            print(cleaned_paragraph)
            print(predicted_paragraphs)

            prediction_results.append(PredictionResult(
                cleanedParagraph=Paragraph(text=cleaned_paragraph, readabilityMetrics=readability_service.perform_readability_analysis(cleaned_paragraph)),
                simplifiedParagraphs=predicted_paragraphs
            ))

        return prediction_results
    except Exception as exception:
        print(exception)
        LOGGER.error('An exception occurred:\n{}'.format(exception))
        raise HTTPException(status_code=500, detail="Prediction Exception")
