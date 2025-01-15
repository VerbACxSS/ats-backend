from italian_ats_evaluator import SimplificationAnalyzer

class SimilarityService:
    def perform_similarity_analysis(self, text1: str, text2: str) -> float:
        return SimplificationAnalyzer(text1, text2).similarity.semantic_similarity
