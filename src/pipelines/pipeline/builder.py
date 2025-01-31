import sys
from typing import Literal

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.pipelines.logger.log import MlFlowLogger
from src.pipelines.type_hint import ControllerType
from src.pipelines.pipeline.base import BasePipeline
from src.pipelines.pipeline.factory import PipelineFactory
from src.pipelines.evaluator.factory import EvaluatorFactory
from src.pipelines.vectorizer.factory import VectorizerFactory
from src.pipelines.preprocessor.factory import PreprocessorFactory
from src.pipelines.similarity.factory import SimilaritySearchFactory
from src.pipelines.vocabulary.factory import VocabularyBuilderFactory
from src.pipelines.config.config import PipelineComponents, PipelineConfig


class PipelineBuilder:
    def __init__(self, controller_type: ControllerType):
        self.controller_type = controller_type
        self.reset()
        
    def reset(self) -> None:
        self._components = PipelineComponents()
        
    def with_config(self, config: PipelineConfig) -> "PipelineBuilder":
        if self.controller_type == ControllerType.TRAINING:
            config.vectorizer_config.mode = "train"
        
        elif self.controller_type == ControllerType.INFERENCE:
            config.vectorizer_config.mode = "inference"
            
        self._components.config = config
        return self
    
    def with_preprocessor(self):
        preprocessor = PreprocessorFactory.create(self._components.config.preprocessor_config)
        
        self._components.preprocessor = preprocessor
        return self
    
    def with_vectorizer(self) -> "PipelineBuilder":
        vectorizer = VectorizerFactory.create(self._components.config.vectorizer_config)
        
        self._components.vectorizer = vectorizer
        return self

    def with_vocabulary(self) -> "PipelineBuilder":        
        vocabulary = VocabularyBuilderFactory.create(
            config=self._components.config.vocabulary_config,
            tokenizer_param=self._components.config.preprocessor_config.tokenizer_param
        )
        
        self._components.vocabulary = vocabulary
        return self
    
    def with_similarity(self) -> "PipelineBuilder":
        similarity = SimilaritySearchFactory.create(self._components.config.similarity_config)
        
        self._components.similarity = similarity
        return self
    
    def with_evaluator(self) -> "PipelineBuilder":
        evaluator = EvaluatorFactory.create(
            traininng_dataset=self._components.config.training_dataset, 
            evaluation_dataset=self._components.config.evaluation_dataset
        )
        
        self._components.evaluator = evaluator
        return self
    
    def with_logger(self, run_name: str, experiment_name: str, mode: Literal["production", "development"]) -> "PipelineBuilder":
        logger = MlFlowLogger(
            run_name=run_name, 
            experiment_name=experiment_name,
            mode=mode
        )
        logger.start_run()

        self._components.logger = logger
        return self
    
    def build(self) -> BasePipeline:
        pipeline = PipelineFactory.create(
            controller_type=self.controller_type,
            config=self._components.config
        )
        
        pipeline.evaluator = self._components.evaluator
        pipeline.vectorizer = self._components.vectorizer
        pipeline.similarity = self._components.similarity
        pipeline.vocabulary = self._components.vocabulary
        pipeline.preprocessor = self._components.preprocessor

        return pipeline


if __name__ == "__main__":
    from src.pipelines.config.default import PIPELINE_DEFAULT_CONFIG

    pipeline = (
        PipelineBuilder(controller_type=ControllerType.TRAINING)
        # .with_logger("information-retrieval", "IRS", "development")
        .with_config(PIPELINE_DEFAULT_CONFIG)
        .with_preprocessor()
        .with_vectorizer()
        .with_vocabulary()
        .with_similarity()
        .with_evaluator()
        .build()
    )

    score = pipeline.run()