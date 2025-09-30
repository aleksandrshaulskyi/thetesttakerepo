from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

from settings import settings

from application.ports import SemanticFilterPort


class SemanticFilter(SemanticFilterPort):

    def __init__(self) -> None:
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    async def process(self, data: list) -> list:
        print('Selecting semantically close candidate queries to sieve those that will most likely not succeed.')
        search_sentence = settings.search_sentence
        search_sentence_vectors = self.model.encode(search_sentence, convert_to_tensor=True)

        candidates = await self.extract_candidates(data=data)
        candidates_vectors = self.model.encode(candidates, convert_to_tensor=True)

        cosine_scores = cos_sim(search_sentence_vectors, candidates_vectors)[0]

        results = sorted(
            zip(candidates, cosine_scores),
            key=lambda x: x[1],
            reverse=True,
        )

        selected_candidates = []

        for candidate, score in results:
            if score > settings.acceptable_threshold:
                selected_candidates.append(await self.get_candidate_data(candidate, data))

        print(f'Selected {len(selected_candidates)} candidate queries.')

        return selected_candidates

    async def extract_candidates(self, data: list) -> list:
        return [item.get('query') for item in data]
    
    async def get_candidate_data(self, query: str, data: list) -> dict:
        index = next(index for index, item in enumerate(data) if item.get('query') == query)
        return data[index]
