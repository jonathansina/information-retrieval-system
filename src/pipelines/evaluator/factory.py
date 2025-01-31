import sys

import pandas as pd

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.pipelines.evaluator.base import BaseEvaluator


class EvaluatorFactory: 
    @classmethod
    def create(self, traininng_dataset: pd.DataFrame, evaluation_dataset: pd.DataFrame) -> BaseEvaluator:
        return BaseEvaluator(traininng_dataset, evaluation_dataset)