import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.generate.config.config import ParaphraserConfig, AugmenterConfig


PARAPHRASER_DEFAULT_CONFIG = ParaphraserConfig(
    model_name="humarin/chatgpt_paraphraser_on_T5_base",
    device="cpu",
    max_length=128,
    temperature=0.8,
    repetition_penalty=1.0,
    num_return_sequences=10,
    no_repeat_ngram_size=2,
    num_beams=10,
    num_beam_groups=5,
    diversity_penalty=4.0
)

AUGMENTER_DEFAULT_CONFIG = AugmenterConfig(
    source_langugae="fa",
    destination_language="en", 
    save_path="../../data/augmented_dataset.csv"
)