from dataclasses import dataclass
from typing import Optional, Dict, Any


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