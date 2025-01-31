from typing import Dict, Any, List
from abc import ABC, abstractmethod

import numpy as np
from sklearn.neighbors import NearestNeighbors


class SimilaritySearchStrategy(ABC):
    @abstractmethod
    def search(self, query_vector, corpus_vectors):
        raise NotImplementedError("The method should be implemented in the subclass.")
    

class KNNSimilarityStrategy(SimilaritySearchStrategy):
    def __init__(self, config: Dict[str, Any]):
        self.nn = NearestNeighbors(**config)
        
    def search(self, query_vector: np.ndarray, corpus_vectors: np.ndarray) -> List[List[int]]:
        self.nn.fit(corpus_vectors)
        indices = self.nn.kneighbors(query_vector, return_distance=False)
        return indices.tolist()