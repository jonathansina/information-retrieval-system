import sys
from functools import wraps
from typing import Dict, Callable
from abc import ABC, abstractmethod

import pandas as pd
from mlflow.entities import Metric

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.pipelines.logger.log import MlFlowLogger


class BaseLogger(ABC):
    @classmethod
    @abstractmethod
    def observe(cls, func: Callable):
        raise NotImplementedError("Method should be implemented in child class")


class EvaluatorLogger(BaseLogger):
    @staticmethod
    def _log_metric(key: str, value: str):
        metric = Metric(key, value, timestamp=0, step=0)
        MlFlowLogger.log_batch_metrics([metric])
    
    @staticmethod
    def _log_report(report: Dict[str, Dict[str, float]]):
        MlFlowLogger.log_table(pd.DataFrame(report), "IR Report/report.json")
        
    @classmethod
    def observe(cls, func: Callable):
        @wraps(func)
        def decorator(*args, **kwargs):
            metrics = func(*args, **kwargs)
            
            if args[0].config.logger:
                cls._log_metric("MRR Score", metrics["mrr_score"])
                cls._log_report(metrics["classification_report"])
                
            return metrics
        return decorator


class PipelineLogger(BaseLogger):
    @staticmethod
    def _log_vectorizer(*args):
        if args[0].vectorizer.config.vectorizer != "sentence-transformer":
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
