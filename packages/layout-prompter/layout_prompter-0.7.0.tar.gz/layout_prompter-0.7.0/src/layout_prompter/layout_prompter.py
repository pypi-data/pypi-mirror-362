from functools import cached_property
from typing import (
    Any,
    List,
    Optional,
    Type,
    cast,
)

import pydantic_numpy.typing as pnd
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableSerializable
from langchain_core.runnables.config import RunnableConfig
from PIL import Image
from pydantic import BaseModel

from layout_prompter.models import LayoutSerializedOutputData, ProcessedLayoutData
from layout_prompter.modules.rankers import LayoutRanker
from layout_prompter.modules.selectors import (
    ContentAwareSelector,
    ContentAwareSelectorOutput,
    LayoutSelector,
)
from layout_prompter.modules.serializers import LayoutSerializer, LayoutSerializerInput
from layout_prompter.typehints import PilImage
from layout_prompter.utils import Configuration


class LayoutPrompterConfiguration(Configuration):
    """Configuration for LayoutPrompter."""

    output_schema: Type[LayoutSerializedOutputData]
    num_return: int = 10
    return_candidates: bool = False
    return_saliency_maps: bool = False


class LayoutPrompterOutput(BaseModel):
    ranked_outputs: List[LayoutSerializedOutputData]
    selected_candidates: Optional[List[ProcessedLayoutData]] = None

    query_saliency_map: Optional[pnd.NpNDArray] = None
    candidate_saliency_maps: Optional[List[pnd.NpNDArray]] = None

    @cached_property
    def query_saliency_map_image(self) -> PilImage:
        assert self.query_saliency_map is not None
        return Image.fromarray(self.query_saliency_map)

    @cached_property
    def candidate_saliency_map_images(self) -> List[PilImage]:
        assert self.candidate_saliency_maps is not None
        return [
            Image.fromarray(content_map) for content_map in self.candidate_saliency_maps
        ]


class LayoutPrompter(RunnableSerializable):
    selector: LayoutSelector
    serializer: LayoutSerializer
    llm: BaseChatModel
    ranker: LayoutRanker

    def invoke(
        self,
        input: ProcessedLayoutData,
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> LayoutPrompterOutput:
        # Load configuration
        conf = LayoutPrompterConfiguration.from_runnable_config(config)

        if isinstance(self.selector, ContentAwareSelector):
            assert conf.return_saliency_maps == self.selector.return_saliency_maps, (
                "The `return_saliency_maps` configuration must match the selector's setting."
            )

        # Get candidates based on the input query
        selector_output = self.selector.select_examples(input)
        candidates = selector_output.selected_examples

        # Define the input for the serializer based on the input query and selected candidates
        serializer_input = LayoutSerializerInput(query=input, candidates=candidates)

        # Construct the few-shot layout examples as prompt messages
        messages = self.serializer.invoke(input=serializer_input, config=config)
        batched_messages = [messages] * conf.num_return

        # Generate batched layouts
        outputs = cast(
            List[LayoutSerializedOutputData],
            self.llm.with_structured_output(conf.output_schema).batch(batched_messages),
        )

        # Rank the generated layouts
        ranked_outputs = self.ranker.invoke(outputs)

        if conf.return_saliency_maps:
            assert isinstance(selector_output, ContentAwareSelectorOutput)
            assert selector_output.query_saliency_map is not None
            assert selector_output.candidate_saliency_maps is not None

            return LayoutPrompterOutput(
                ranked_outputs=ranked_outputs,
                selected_candidates=candidates if conf.return_candidates else None,
                query_saliency_map=selector_output.query_saliency_map,
                candidate_saliency_maps=selector_output.candidate_saliency_maps,
            )

        return LayoutPrompterOutput(
            ranked_outputs=ranked_outputs,
            selected_candidates=candidates if conf.return_candidates else None,
        )
