import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.augmenter.base import BaseAugmenter
from src.augmenter.translator import Translator
from src.augmenter.paraphraser import Paraphraser
from src.config.config import AugmenterConfig, ParaphraserConfig


class AugmenterFactory:
    @classmethod
    def create(cls, augmenter_config: AugmenterConfig, paraphraser_config: ParaphraserConfig) -> BaseAugmenter:
        translator = Translator()
        paraphraser = Paraphraser(paraphraser_config)
        
        return BaseAugmenter(augmenter_config, translator, paraphraser)