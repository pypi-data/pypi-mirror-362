"""
Tools for Jay MCP server
"""

import asyncio
import logging
import re
from datetime import datetime
from typing import List, Dict, Any

from mcp.server.fastmcp import FastMCP

from .services.github_api_service import GitHubApiService
from .config.github_config import GitHubApiConfig
from .models.github_repo_info import GitHubRepoInfo

# 配置日志
logger = logging.getLogger(__name__)

# 仓库名称格式验证正则表达式
REPO_PATTERN = re.compile(r"^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$")

# GitHub API配置
github_config = GitHubApiConfig()


def register_tools(mcp: FastMCP) -> None:
    """
    Register all tools with the MCP server

    Args:
        mcp: FastMCP server instance
    """

    @mcp.tool()
    async def batch_get_repo_info(repos: List[str]) -> List[Dict[str, Any]]:
        """
        Batch retrieve GitHub repository information including stars, forks, language, and creation date.

        Use this tool when you need to:
        - Get GitHub repository statistics (stars, forks, watchers)
        - Find repository details (language, creation date, last update)
        - Compare multiple repositories
        - Search for repository information
        - Analyze GitHub projects

        批量获取GitHub仓库信息，包括星标数、分叉数、编程语言、创建时间等详细信息。

        Args:
            repos: List of repository names in "owner/repo" format, e.g. ["facebook/react", "microsoft/vscode"]
                  仓库列表，格式：owner/repo，例如 ["facebook/react", "vuejs/vue"]

        Returns:
            List of dictionaries containing detailed repository information:
            - full_name: Repository full name (owner/repo)
            - stargazers_count: Number of stars
            - forks_count: Number of forks
            - watchers_count: Number of watchers
            - language: Primary programming language
            - created_at: Repository creation date
            - updated_at: Last update time
            - pushed_at: Last push time
            - html_url: Repository URL
            - status: Query status (SUCCESS/FAILED)
            包含仓库详细信息的字典列表

        Raises:
            ValueError: When parameter validation fails (empty list, invalid format, too many repos)
        """
        logger.info(f"开始批量查询GitHub仓库信息，仓库数量: {len(repos)}")

        # 参数验证
        if not repos:
            raise ValueError("仓库列表不能为空")

        if len(repos) > 50:
            raise ValueError("单次查询仓库数量不能超过50个")

        # 验证仓库名称格式
        invalid_repos = [repo for repo in repos if not REPO_PATTERN.match(repo)]
        if invalid_repos:
            raise ValueError(f"仓库名称格式不正确: {', '.join(invalid_repos)}，正确格式为: owner/repo")

        try:
            # 直接调用异步函数（现在工具本身是异步的）
            results = await _batch_get_repo_info_async(repos)

            # 统计成功和失败的数量
            success_count = sum(1 for r in results if r.status == "SUCCESS")
            failure_count = len(results) - success_count

            logger.info(f"批量查询完成，成功: {success_count}, 失败: {failure_count}")

            # 转换为字典列表返回
            return [repo_info.dict() for repo_info in results]

        except Exception as e:
            logger.error(f"批量查询GitHub仓库信息时发生异常: {str(e)}")
            raise ValueError(f"查询过程中发生异常: {str(e)}")


async def _batch_get_repo_info_async(repos: List[str]) -> List[GitHubRepoInfo]:
    """
    异步批量获取仓库信息

    Args:
        repos: 仓库列表

    Returns:
        GitHubRepoInfo对象列表
    """
    # 使用异步上下文管理器
    async with GitHubApiService(github_config) as github_service:
        logger.info(f"GitHub API配置: {github_service.get_config_info()}")

        # 创建异步任务列表
        tasks = [_fetch_single_repo_info(github_service, repo) for repo in repos]

        # 并行执行所有任务
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 处理结果，将异常转换为失败的GitHubRepoInfo对象
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                owner, repo = repos[i].split("/")
                processed_results.append(GitHubRepoInfo.failure(owner, repo, str(result)))
            else:
                processed_results.append(result)

        return processed_results


async def _fetch_single_repo_info(github_service: GitHubApiService, repo_full_name: str) -> GitHubRepoInfo:
    """查询单个仓库信息"""
    owner, repo = repo_full_name.split("/")

    try:
        logger.debug(f"开始查询仓库: {repo_full_name}")

        # 调用GitHub API
        data = await github_service.get_repository_info(repo_full_name)

        # 解析响应数据
        return _parse_github_api_response(owner, repo, data)

    except Exception as e:
        logger.error(f"查询仓库 {repo_full_name} 时发生异常: {str(e)}")
        return GitHubRepoInfo.failure(owner, repo, f"查询异常: {str(e)}")


def _parse_github_api_response(owner: str, repo: str, data: dict) -> GitHubRepoInfo:
    """解析GitHub API响应"""
    repo_full_name = f"{owner}/{repo}"

    try:
        repo_info = GitHubRepoInfo.success(owner, repo)

        # 解析时间字段
        created_at = data.get("created_at")
        updated_at = data.get("updated_at")
        pushed_at = data.get("pushed_at")

        if created_at:
            repo_info.created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        if updated_at:
            repo_info.updated_at = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
        if pushed_at:
            repo_info.pushed_at = datetime.fromisoformat(pushed_at.replace('Z', '+00:00'))

        # 提取基本信息字段
        repo_info.stargazers_count = data.get("stargazers_count")
        repo_info.language = data.get("language")
        repo_info.html_url = data.get("html_url")
        repo_info.forks_count = data.get("forks_count")
        repo_info.watchers_count = data.get("watchers_count")

        logger.debug(f"成功解析仓库信息: {repo_full_name}, stars: {repo_info.stargazers_count}, forks: {repo_info.forks_count}")

        return repo_info

    except Exception as e:
        logger.error(f"解析GitHub API响应时发生异常，仓库: {owner}/{repo}, 异常: {str(e)}")
        return GitHubRepoInfo.failure(owner, repo, f"响应解析异常: {str(e)}")
