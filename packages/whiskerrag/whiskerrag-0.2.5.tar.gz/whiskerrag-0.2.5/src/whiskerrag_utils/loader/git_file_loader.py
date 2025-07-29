from typing import List, Union

from whiskerrag_types.interface.loader_interface import BaseLoader
from whiskerrag_types.model import (
    GithubFileSourceConfig,
    Knowledge,
    KnowledgeSourceEnum,
)
from whiskerrag_types.model.knowledge import KnowledgeTypeEnum
from whiskerrag_types.model.knowledge_source import GithubRepoSourceConfig
from whiskerrag_types.model.multi_modal import Image, Text
from whiskerrag_utils.loader.git_repo_manager import get_repo_manager
from whiskerrag_utils.registry import RegisterTypeEnum, register


@register(RegisterTypeEnum.KNOWLEDGE_LOADER, KnowledgeSourceEnum.GITHUB_FILE)
class GithubFileLoader(BaseLoader[Union[Text, Image]]):
    """
    从Git仓库加载单个文件的加载器
    """

    def __init__(self, knowledge: Knowledge):
        """
        初始化GithubFileLoader

        Args:
            knowledge: Knowledge实例，包含文件源配置

        Raises:
            ValueError: 无效的文件配置
        """
        if not isinstance(knowledge.source_config, GithubFileSourceConfig):
            raise ValueError("source_config should be GithubFileSourceConfig")

        self.knowledge = knowledge
        self.path = knowledge.source_config.path
        self.repo_manager = get_repo_manager()

        # 从文件配置中提取仓库配置
        self.repo_config = GithubRepoSourceConfig(
            **knowledge.source_config.model_dump(exclude={"path"}),
        )

    async def load(self) -> List[Union[Text, Image]]:
        """
        加载指定的文件

        Returns:
            List[Union[Text, Image]]: 文件内容列表
        """
        # 获取仓库路径
        repo_path = self.repo_manager.get_repo_path(self.repo_config)

        # 构建完整文件路径
        import os

        full_path = os.path.join(repo_path, self.path)

        if not os.path.exists(full_path):
            raise ValueError(f"File not found: {self.path}")

        # 读取文件内容
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            # 如果不是文本文件，尝试二进制读取并转换为base64
            with open(full_path, "rb") as f:
                import base64

                content = base64.b64encode(f.read()).decode("utf-8")

        # 根据知识类型返回相应的对象
        if self.knowledge.knowledge_type == KnowledgeTypeEnum.IMAGE:
            return [
                Image(
                    b64_json=content,
                    metadata=self.knowledge.metadata,
                )
            ]
        else:
            return [
                Text(
                    content=content,
                    metadata=self.knowledge.metadata,
                )
            ]

    async def decompose(self) -> List[Knowledge]:
        """
        文件加载器不需要分解，返回空列表

        Returns:
            List[Knowledge]: 空列表
        """
        return []

    async def on_load_finished(self) -> None:
        """
        加载完成后的生命周期方法
        这里不清理仓库，因为可能还有其他文件需要访问
        """
        pass
