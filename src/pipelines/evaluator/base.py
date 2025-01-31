import sys
from typing import List, Tuple, Dict, Any

import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.pipelines.config.config import EvaluatorConfig


class BaseEvaluator:
    def __init__(self, config: EvaluatorConfig):
        self.config = config
        
    def evaluate(self, search_result: List[List[int]]) -> float:
        true_classes = self.config.evaluation_dataset["category"]
        report, confusion_matrix = self._get_classification_result(search_result, true_classes)
        mrr_score = self._get_mean_reciprocal_rank(search_result, true_classes)
        
        return {
            "mrr_score": mrr_score,
            "classification_report": report,
            "confusion_matrix": confusion_matrix
        }
        
    def _get_classification_result(self, search_result: List[List[int]], true_classes: List[int]) -> Tuple[Dict[str, Any], np.ndarray]:
        first_neighbor_indices = [neighbors[0] for neighbors in search_result]
        predicted_classes = self.config.training_dataset["category"][first_neighbor_indices]
        
        confusion_matrix = self._get_confusion_matrix(true_classes, predicted_classes)
        report = classification_report(true_classes, predicted_classes, zero_division=1, output_dict=True)
        return report, confusion_matrix
        
    def _get_mean_reciprocal_rank(self, search_result: List[List[int]], true_classes: List[int]) -> float:
        reciprocal_ranks = []
        for query_idx, neighbors in enumerate(search_result):
            for rank, neighbor_idx in enumerate(neighbors):
                if self.config.training_dataset["category"][neighbor_idx] == true_classes[query_idx]:
                    reciprocal_ranks.append(1 / (rank + 1))
                    break
            else:
                reciprocal_ranks.append(0)
        return sum(reciprocal_ranks) / len(reciprocal_ranks)
    
    def _get_confusion_matrix(self, true_classes: List[int], predicted_classes: List[int]) -> np.ndarray:
        return confusion_matrix(true_classes, predicted_classes)
