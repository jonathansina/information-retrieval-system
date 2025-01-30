import sys
import asyncio
from typing import List, Optional

import pandas as pd
from alive_progress import alive_bar

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import AugmenterConfig
from src.augmentation.translator import Translator
from src.augmentation.paraphraser import Paraphraser


class BaseAugmenter:
    def __init__(self, config: AugmenterConfig, trasnlator: Translator, paraphraser: Paraphraser):
        self.config = config
        self.translator = trasnlator
        self.paraphraser = paraphraser

    async def _augment_query(self, text) -> List[str]:
        translated_text = await self.translator.translate(text, self.config.source_langugae, self.config.destination_language)
        paraphrased_sentences = self.paraphraser.paraphrase(translated_text)

        translated_sentences = await asyncio.gather(
            *[self.translator.translate(sentence, self.config.destination_language, self.config.source_langugae) for sentence in paraphrased_sentences]
        )
        
        return translated_sentences
    
    async def augment(self, dataset: pd.DataFrame, save: Optional[bool] = False) -> pd.DataFrame:
        augmented_dataset = []

        with alive_bar(dataset.shape[0]) as bar:   
            for _, row in dataset.iterrows():
                question = row["question"]
                paraphrased_questions = await self._augment_query(question)

                for pq in paraphrased_questions:
                    augmented_dataset.append({"question": pq, "answer": row["answer"], "category": row["category"]})
                    
                bar()
                
        augmented_dataframe = pd.DataFrame(augmented_dataset)
        
        if save:
            augmented_dataframe.to_csv(self.config.save_path, index=False)
            
        return augmented_dataframe
    
    
if __name__ == "__main__":
    from src.config.default import AUGMENTER_DEFAULT_CONFIG, PARAPHRASER_DEFAULT_CONFIG
    from src.augmentation.factory import AugmenterFactory
    
    augmenter = AugmenterFactory.create(AUGMENTER_DEFAULT_CONFIG, PARAPHRASER_DEFAULT_CONFIG)
    asyncio.run(augmenter.augment(pd.read_csv("../../data/digikala_faq.csv"), save=True))
    
