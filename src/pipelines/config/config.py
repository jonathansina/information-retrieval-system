from dataclasses import dataclass
from typing import Optional, Dict, Any, Literal, Type


@dataclass
class PreprocessorConfig:
    tokenizer_param: Dict[str, Any]
    normalizer: Optional[bool] = False
    stemmer: Optional[bool] = False
    lemmatizer: Optional[bool] = False
    informal_normalizer: Optional[bool] = False
    normalizer_param: Optional[Dict[str, Any]] = None
    lemmatizer_param: Optional[Dict[str, Any]] = None
    informal_normalizer_param: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.lemmatizer and self.stemmer:
            raise ValueError("Stemmer and Lemmatizer can not be used together.")


@dataclass
class VectorizerConfig:
    vectorizer: Literal["tf-idf", "bow", "sentence-transformer"]
    vectorizer_param: Dict[str, Any]
    mode: Optional[Literal["train", "inference"]] = None
    
    def __post_init__(self):
        if self.mode:
            raise ValueError("Mode can not be set in initialization.")


@dataclass
class SimilaritySearchConfig:
    top_k: int
    metrics: Literal["jaccard", "cosine", "euclidean", "minowski"]
    metrics_param: Dict[str, Any]


@dataclass
class VocabularyConfig:
    save: Optional[bool] = False
    save_path: Optional[str] = None
    
    def __post_init__(self):
        if self.save and not self.save_path:
            raise ValueError("Save path should be provided.")


@dataclass
class PipelineComponents:
    preprocessor: Optional[Type[Any]] = None
    vectorizer: Optional[Type[Any]] = None
    similarity: Optional[Type[Any]] = None
    vocabulary: Optional[Type[Any]] = None
    
    
@dataclass
class PipelineConfig:
    preprocessor_config: PreprocessorConfig
    vectorizer_config: VectorizerConfig
    similarity_config: SimilaritySearchConfig
    vocabulary_config: VocabularyConfig