import sys
from functools import wraps
from abc import ABC, abstractmethod
from typing import Dict, Literal, Optional, Callable, List

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.pipelines.logger.log import MlFlowLogger


class BaseLogger(ABC):
    @classmethod
    @abstractmethod
    def observe(cls, func: Callable):
        raise NotImplementedError("Method should be implemented in child class")


class PipelineLogger(BaseLogger):
    @staticmethod
    def _log_vectorizer(*args):
        if args[0].vectorizer.config.vectorizer != "sentence-transformers":
            MlFlowLogger.log_artifact(args[0].vectorizer.strategy.vectorizer, "vectorizer.pkl") 
       
    @staticmethod
    def _log_corpus(vectorized_corpus):
        MlFlowLogger.log_artifact(vectorized_corpus, "corpus.pkl")
        
    @classmethod
    def observe(cls, func: Callable):
        @wraps(func)
        def decorator(*args, **kwargs):
            vectorized_corpus = func(*args, **kwargs)
            
            if args[0].config.logger:
                cls._log_vectorizer(*args)
                cls._log_corpus(vectorized_corpus)
                
            return vectorized_corpus
        return decorator
