# from typing import Optional

# from langchain_core.runnables.config import RunnableConfig

# from layout_prompter.models import ProcessedLayoutData
# from layout_prompter.models.layout_data import LayoutData
# from layout_prompter.transforms import (
#     DiscretizeBboxes,
#     LabelDictSort,
#     ShuffleElements,
# )

from .base import Processor


class GenTypeSizeProcessor(Processor):
    name: str = "gen-type-size-processor"

    # def _invoke(
    #     self, layout_data: LayoutData, config: Optional[RunnableConfig] = None, **kwargs
    # ) -> ProcessedLayoutData:
    #     chain = ShuffleElements() | LabelDictSort()

    #     breakpoint()
