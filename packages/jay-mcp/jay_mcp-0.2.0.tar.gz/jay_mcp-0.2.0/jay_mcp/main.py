"""
GitHub仓库信息查询主应用
对应Java中的GitHubRepositoryController.java
"""
import asyncio
import logging
import re
from datetime import datetime
from typing import List
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse

from .models.github_repo_info import GitHubRepoInfo
from .services.github_api_service import GitHubApiService
from .config.github_config import GitHubApiConfig
from .utils.response import R

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="GitHub仓库信息查询API",
    description="提供GitHub仓库信息批量查询功能",
    version="1.0.0"
)

# 仓库名称格式验证正则表达式
REPO_PATTERN = re.compile(r"^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$")

# GitHub API配置
github_config = GitHubApiConfig()

@app.get("/github/repositories/batch-info", 
         response_model=R[List[GitHubRepoInfo]],
         summary="批量获取GitHub仓库信息",
         description="并行查询多个GitHub仓库的基本信息")
async def batch_get_repo_info(
    repos: List[str] = Query(..., description="仓库列表，格式：owner/repo", example=["facebook/react", "vuejs/vue"])
):
    """批量获取GitHub仓库信息"""
    
    logger.info(f"开始批量查询GitHub仓库信息，仓库数量: {len(repos)}")
    
    # 参数验证
    if not repos:
        return R.fail("仓库列表不能为空")
    
    if len(repos) > 50:
        return R.fail("单次查询仓库数量不能超过50个")
    
    # 验证仓库名称格式
    invalid_repos = [repo for repo in repos if not REPO_PATTERN.match(repo)]
    if invalid_repos:
        return R.fail(f"仓库名称格式不正确: {', '.join(invalid_repos)}，正确格式为: owner/repo")
    
    try:
        # 使用异步上下文管理器
        async with GitHubApiService(github_config) as github_service:
            logger.info(f"GitHub API配置: {github_service.get_config_info()}")
            
            # 创建异步任务列表
            tasks = [fetch_single_repo_info(github_service, repo) for repo in repos]
            
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
            
            # 统计成功和失败的数量
            success_count = sum(1 for r in processed_results if r.status == "SUCCESS")
            failure_count = len(processed_results) - success_count
            
            logger.info(f"批量查询完成，成功: {success_count}, 失败: {failure_count}")
            
            return R.ok(processed_results)
            
    except Exception as e:
        logger.error(f"批量查询GitHub仓库信息时发生异常: {str(e)}")
        return R.fail(f"查询过程中发生异常: {str(e)}")

@app.get("/github/repositories/config-info",
         response_model=R[str],
         summary="获取GitHub API配置信息",
         description="查看当前GitHub API的认证状态和配置信息")
async def get_config_info():
    """获取GitHub API配置信息"""
    try:
        async with GitHubApiService(github_config) as github_service:
            config_info = github_service.get_config_info()
            logger.info(f"查询GitHub API配置信息: {config_info}")
            return R.ok(config_info)
    except Exception as e:
        logger.error(f"获取GitHub API配置信息时发生异常: {str(e)}")
        return R.fail(f"获取配置信息失败: {str(e)}")

async def fetch_single_repo_info(github_service: GitHubApiService, repo_full_name: str) -> GitHubRepoInfo:
    """查询单个仓库信息"""
    owner, repo = repo_full_name.split("/")
    
    try:
        logger.debug(f"开始查询仓库: {repo_full_name}")
        
        # 调用GitHub API
        data = await github_service.get_repository_info(repo_full_name)
        
        # 解析响应数据
        return parse_github_api_response(owner, repo, data)
        
    except Exception as e:
        logger.error(f"查询仓库 {repo_full_name} 时发生异常: {str(e)}")
        return GitHubRepoInfo.failure(owner, repo, f"查询异常: {str(e)}")

def parse_github_api_response(owner: str, repo: str, data: dict) -> GitHubRepoInfo:
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
