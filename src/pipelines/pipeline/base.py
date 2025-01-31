import sys
from abc import ABC, abstractmethod

import pandas as pd

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.pipelines.type_hint import ControllerType
from src.pipelines.config.config import PipelineConfig
from src.pipelines.evaluator.base import  BaseEvaluator
from src.pipelines.vectorizer.base import BaseVectorizer
from src.pipelines.vocabulary.base import VocabularyBuilder
from src.pipelines.pipeline.registry import PipelineRegistry
from src.pipelines.preprocessor.base import BasePreprocessor
from src.pipelines.similarity.base import BaseSimilaritySearch


class BasePipeline(ABC):
    def __init__(self, config: PipelineConfig):
        self.config: PipelineConfig = config
        self.evaluator: BaseEvaluator = None
        self.vectorizer: BaseVectorizer = None
        self.vocabulary: VocabularyBuilder = None
        self.preprocessor: BasePreprocessor = None
        self.similarity: BaseSimilaritySearch = None

    @abstractmethod
    def run(self) -> float:
        raise NotImplementedError("Method should implemented in child class")


@PipelineRegistry.register(ControllerType.TRAINING)
class TrainingPipeline(BasePipeline):
    def run(self) -> float:
        preprocessed_dataset = self.preprocessor.process(self.config.training_dataset["question"])
        corpus = self.vocabulary.build(preprocessed_dataset)
        vectorized_corpus = self.vectorizer.vectorize(corpus)
        
        self.vectorizer.config.mode = "inference"
        preprocessed_queries = self.preprocessor.process(self.config.evaluation_dataset["query"])
        vectorized_queries = self.vectorizer.vectorize(preprocessed_queries)

        search_result = self.similarity.search(vectorized_queries, vectorized_corpus)
        
        print(self.evaluator.evaluate(search_result))
        
        return vectorized_corpus


@PipelineRegistry.register(ControllerType.INFERENCE)
class InferencePipeline(BasePipeline):
    def run(self, query: str) -> float:
        series_query = pd.Series([query])
        preprocessed_query = self.preprocessor.process(series_query)
        query_vector = self.vectorizer.vectorize(preprocessed_query)

        print(query_vector)