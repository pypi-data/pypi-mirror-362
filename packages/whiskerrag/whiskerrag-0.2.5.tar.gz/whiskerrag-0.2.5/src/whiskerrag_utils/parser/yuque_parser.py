import re
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from whiskerrag_types.interface.parser_interface import BaseParser, ParseResult
from whiskerrag_types.model.knowledge import Knowledge, KnowledgeTypeEnum
from whiskerrag_types.model.multi_modal import Image, Text
from whiskerrag_types.model.splitter import YuqueSplitConfig
from whiskerrag_utils.registry import RegisterTypeEnum, register


@register(RegisterTypeEnum.PARSER, KnowledgeTypeEnum.YUQUEDOC)
class YuqueParser(BaseParser[Text]):
    async def parse(
        self,
        knowledge: Knowledge,
        content: Text,
    ) -> ParseResult:
        split_config = knowledge.split_config
        if not isinstance(split_config, YuqueSplitConfig):
            raise TypeError("knowledge.split_config must be of type YuqueSplitConfig")
        separators = split_config.separators or [
            # First, try to split along Markdown headings (starting with level 2)
            "\n#{1,6} ",
            # Note the alternative syntax for headings (below) is not handled here
            # Heading level 2
            # ---------------
            # End of code block
            "```\n",
            # Horizontal lines
            "\n\\*\\*\\*+\n",
            "\n---+\n",
            "\n___+\n",
            # Note that this splitter doesn't handle horizontal lines defined
            # by *three or more* of ***, ---, or ___, but this is not handled
            "\n\n",
            "\n",
            " ",
            "",
        ]
        if "" not in separators:
            separators.append("")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=split_config.chunk_size,
            chunk_overlap=split_config.chunk_overlap,
            separators=separators,
            keep_separator=False,
        )
        result: ParseResult = []
        # extract all image urls and alt text
        image_pattern = r"!\[(.*?)\]\((.*?)\)"
        all_image_matches = re.findall(image_pattern, content.content)

        # create image objects
        for img_idx, (alt_text, img_url) in enumerate(all_image_matches):
            if img_url.strip():  # ensure url is not empty
                img_metadata = content.metadata.copy()
                img_metadata["_img_idx"] = img_idx
                img_metadata["_img_url"] = img_url.strip()
                img_metadata["_alt_text"] = alt_text.strip() if alt_text.strip() else ""
                image_obj = Image(url=img_url.strip(), metadata=img_metadata)
                result.append(image_obj)

        # split text
        split_texts = splitter.split_text(content.content)

        for idx, text in enumerate(split_texts):
            metadata = content.metadata.copy()
            metadata["_idx"] = idx
            result.append(Text(content=text, metadata=metadata))

        return result

    async def batch_parse(
        self,
        knowledge: Knowledge,
        content_list: List[Text],
    ) -> List[ParseResult]:
        return [await self.parse(knowledge, content) for content in content_list]
