import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.pipelines.config.config import PreprocessorConfig


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