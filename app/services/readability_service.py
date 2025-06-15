from italian_ats_evaluator import TextAnalyzer

from ..models.PredictionResponse import ReadabilityMetrics

class ReadabilityService:
    def perform_readability_analysis(self, text: str) -> ReadabilityMetrics:
        result = TextAnalyzer(text=text)

        return ReadabilityMetrics(
            vdb=result.vdb.n_vdb_tokens / result.basic.n_tokens * 100.0,
            tokens=result.basic.n_tokens,
            gulpease=result.readability.gulpease,
            fleschVacca=result.readability.flesch_vacca
        )
