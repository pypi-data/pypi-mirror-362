import logging
import os
import shutil
import tempfile
from typing import Any, Dict, Optional, Tuple

from whiskerrag_types.model.knowledge_source import GithubRepoSourceConfig

logger = logging.getLogger(__name__)


def _check_git_installation() -> bool:
    """Check if git is installed in the system"""
    try:
        import subprocess

        subprocess.run(["git", "--version"], check=True, capture_output=True, text=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def _lazy_import_git() -> Tuple[Any, Any, Any]:
    """Lazy import git modules to avoid direct dependency"""
    try:
        from git import Repo
        from git.exc import GitCommandNotFound, InvalidGitRepositoryError

        return Repo, GitCommandNotFound, InvalidGitRepositoryError
    except ImportError as e:
        raise ImportError(
            "GitPython is required for Git repository loading. "
            "Please install it with: pip install GitPython"
        ) from e


class GitRepoManager:
    """manage git repo download and cache"""

    def __init__(self) -> None:
        self.repos_dir = os.path.join(tempfile.gettempdir(), "repo_download")
        self._repos_cache: Dict[str, str] = {}  # cache for downloaded repos
        os.makedirs(self.repos_dir, exist_ok=True)

    def get_repo_path(self, config: GithubRepoSourceConfig) -> str:
        """
        获取仓库路径，如果不存在则下载

        Args:
            config: 仓库配置信息

        Returns:
            str: 仓库本地路径
        """
        # 生成唯一标识：repo_name + branch + commit_id
        repo_key = self._generate_repo_key(config)

        if repo_key in self._repos_cache:
            repo_path = self._repos_cache[repo_key]
            if os.path.exists(repo_path):
                logger.info(f"Using cached repository: {repo_path}")
                return repo_path
            else:
                # 缓存中的路径不存在，清理缓存
                del self._repos_cache[repo_key]

        # 下载仓库
        repo_path = self._download_repo(config)
        self._repos_cache[repo_key] = repo_path
        return repo_path

    def _generate_repo_key(self, config: GithubRepoSourceConfig) -> str:
        """生成仓库的唯一标识"""
        parts = [config.repo_name]
        if config.branch:
            parts.append(config.branch)
        if config.commit_id:
            parts.append(config.commit_id)
        return "_".join(parts).replace("/", "_")

    def _download_repo(self, config: GithubRepoSourceConfig) -> str:
        """
        下载仓库到本地

        Args:
            config: 仓库配置信息

        Returns:
            str: 下载后的仓库路径
        """
        if not _check_git_installation():
            raise ValueError("Git is not installed in the system")

        # 构建克隆URL
        clone_url = self._build_clone_url(config)

        # 确定本地路径
        repo_name = config.repo_name.replace("/", "_")
        repo_saved_path = os.path.join(self.repos_dir, repo_name)

        # 如果路径已存在，先清理
        if os.path.exists(repo_saved_path):
            try:
                shutil.rmtree(repo_saved_path)
            except Exception as e:
                logger.warning(
                    f"Failed to clean existing directory {repo_saved_path}: {e}"
                )
                # 使用带时间戳的路径避免冲突
                import time

                repo_saved_path = f"{repo_saved_path}_{int(time.time())}"

        # 克隆仓库
        self._clone_repo(clone_url, repo_saved_path, config.branch, config.commit_id)

        logger.info(f"Successfully downloaded repository to {repo_saved_path}")
        return repo_saved_path

    def _build_clone_url(self, config: GithubRepoSourceConfig) -> str:
        """
        构建克隆URL，只区分GitHub和GitLab两种模式

        Args:
            config: 仓库配置信息

        Returns:
            str: 克隆URL
        """
        base_url = config.url.rstrip("/")
        repo_name = config.repo_name

        # 移除 base_url 中的协议部分，避免重复
        if base_url.startswith("https://"):
            url_no_scheme = base_url[8:]  # 移除 "https://"
        elif base_url.startswith("http://"):
            url_no_scheme = base_url[7:]  # 移除 "http://"
        else:
            url_no_scheme = base_url

        if config.auth_info:
            return f"https://{config.auth_info}@{url_no_scheme}/{repo_name}.git"
        else:
            return f"https://{url_no_scheme}/{repo_name}.git"

    def _clone_repo(
        self,
        clone_url: str,
        repo_path: str,
        branch: Optional[str] = None,
        commit_id: Optional[str] = None,
    ) -> None:
        """
        克隆仓库

        Args:
            clone_url: 克隆URL
            repo_path: 本地路径
            branch: 分支名
            commit_id: 提交ID
        """
        Repo, GitCommandNotFound, InvalidGitRepositoryError = _lazy_import_git()

        try:
            # 克隆仓库
            if branch:
                repo = Repo.clone_from(
                    clone_url,
                    repo_path,
                    multi_options=["--filter=blob:limit=5m"],
                    branch=branch,
                )
            else:
                repo = Repo.clone_from(
                    clone_url,
                    repo_path,
                    multi_options=["--filter=blob:limit=5m"],
                )

            # 如果指定了commit_id，切换到指定提交
            if commit_id:
                repo.git.checkout(commit_id)

        except GitCommandNotFound:
            raise ValueError("Git command not found. Please ensure git is installed.")
        except InvalidGitRepositoryError as e:
            raise ValueError(f"Invalid git repository: {str(e)}")
        except Exception as e:
            if "Authentication failed" in str(e):
                raise ValueError("Authentication failed. Please check your token.")
            raise ValueError(f"Failed to clone repository: {str(e)}")

    def get_repo(self, config: GithubRepoSourceConfig) -> Any:
        """
        获取GitPython Repo对象

        Args:
            config: 仓库配置信息

        Returns:
            Repo: GitPython Repo对象
        """
        repo_path = self.get_repo_path(config)
        Repo, _, _ = _lazy_import_git()
        return Repo(repo_path)

    def cleanup_repo(self, config: GithubRepoSourceConfig) -> None:
        """
        清理指定的仓库

        Args:
            config: 仓库配置信息
        """
        repo_key = self._generate_repo_key(config)
        if repo_key in self._repos_cache:
            repo_path = self._repos_cache[repo_key]
            try:
                if os.path.exists(repo_path):
                    shutil.rmtree(repo_path)
                    logger.info(f"Cleaned up repository: {repo_path}")
            except Exception as e:
                logger.error(f"Error cleaning up repository {repo_path}: {e}")
            finally:
                del self._repos_cache[repo_key]


# 全局仓库管理器实例
_repo_manager = GitRepoManager()


def get_repo_manager() -> GitRepoManager:
    """获取全局仓库管理器实例"""
    return _repo_manager
