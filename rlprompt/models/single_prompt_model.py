import torch
from typing import Optional, List, Union, Any, Dict
from .base_model import BaseModel


class SinglePromptModel(BaseModel):
    def __init__(
        self,
        model: BaseModel,
        prompt_length: int,
        prompt_batch_size: int,
        source_str: str,
    ):
        super().__init__()
        self._model = model
        self.prompt_length = prompt_length
        self.prompt_batch_size = prompt_batch_size
        self.source_str = source_str

    def _get_prompt_source(
            self, batch_size: Optional[int] = None) -> List[str]:
        if batch_size is None: batch_size = self.prompt_batch_size
        return [self.source_str for _ in range(batch_size)]

    def generate(
        self,
        source_texts: List[str],
        do_sample: bool,
        top_k: Optional[int],
        top_p: Optional[float],
        num_beams: Optional[int],
        match_prompt_to_source: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        if match_prompt_to_source: 
            prompt_source = \
                    self._get_prompt_source(batch_size=len(source_texts))
        else:
            prompt_source = self._get_prompt_source()
        return self._model.generate(source_texts=prompt_source,
                                    do_sample=do_sample,
                                    top_k=top_k,
                                    top_p=top_p,
                                    num_beams=num_beams,
                                    **kwargs)

    def teacher_forcing(
        self,
        source_texts: List[str],
        sample_ids: torch.LongTensor,
        **kwargs
    ) -> Dict[str, Any]:
        prompt_source = self._get_prompt_source()
        return self._model.teacher_forcing(source_texts=prompt_source,
                                           sample_ids=sample_ids,
                                           **kwargs)
