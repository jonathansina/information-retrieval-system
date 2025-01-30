import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.pipelines.config.config import (
    PipelineConfig,
    VectorizerConfig, 
    VocabularyConfig, 
    PreprocessorConfig,
    SimilaritySearchConfig
)


tokenizer_param = {
    "join_verb_parts": True,
    "join_abbreviations": True,
    "separate_emoji": True,
    "replace_links": True,
    "replace_ids": True,
    "replace_numbers": True,
    "replace_hashtags": True
}

normalizer_param = {
    "correct_spacing": True,
    "remove_diacritics": True,
    "remove_specials_chars": True,
    "decrease_repeated_chars": True,
    "persian_style": True,
    "persian_numbers": True,
    "unicodes_replacement": True,
    "seperate_mi": True
}

informal_normalizer_param = {
    "seperation_flag": False
}

lemmatizer_param = {
    "joined_verb_parts": True
}

metrics_param ={
    "algorithm": "auto",
    "leaf_size": 30,
    "p": 2,
    "n_jobs": -1
}

sentence_transformer_param = {
    "model_name_or_path": "sentence-transformers/LaBSE",
    "token": ...
}

tf_idf_param = {
    "max_features": 10000,
    "ngram_range": (1, 2),
    "max_df": 0.85,
    "min_df": 0.01
}


PREPROCESSOR_DEFAULT_CONFIG = PreprocessorConfig(
    tokenizer_param=tokenizer_param,
    informal_normalizer=True,
    normalizer=True,
    stemmer=False, 
    lemmatizer=True,
    informal_normalizer_param=informal_normalizer_param,
    normalizer_param=normalizer_param,
    lemmatizer_param=lemmatizer_param,
)


VECTORIZER_DEFAULT_CONFIG = VectorizerConfig(
    vectorizer="tf-idf", 
    vectorizer_param=tf_idf_param
)


SIMILARITY_SEARCH_DEFAULT_CONFIG = SimilaritySearchConfig(
    top_k=4, 
    metrics="cosine",
    metrics_param={}
)


VOCABULARY_DEFAULT_CONFIG = VocabularyConfig(
    save=True,
    save_path="../../../data/vocabulary.txt"
)


PIPELINE_DEFAULT_CONFIG = PipelineConfig(
    preprocessor_config=PREPROCESSOR_DEFAULT_CONFIG,
    vectorizer_config=VECTORIZER_DEFAULT_CONFIG,
    similarity_config=SIMILARITY_SEARCH_DEFAULT_CONFIG,
    vocabulary_config=VOCABULARY_DEFAULT_CONFIG
)