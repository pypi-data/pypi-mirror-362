"""
GitHub API服务类
对应Java中的GitHubApiService.java
"""
import asyncio
import logging
from typing import Dict, Any
import aiohttp
from aiohttp import ClientTimeout, ClientError
from ..config.github_config import GitHubApiConfig

logger = logging.getLogger(__name__)

class GitHubApiService:
    """GitHub API服务类"""
    
    def __init__(self, config: GitHubApiConfig):
        self.config = config
        self._session = None
        logger.info("GitHub API服务初始化完成")
        logger.info(f"认证状态: {config.get_auth_status()}")
        logger.info(f"速率限制: {config.get_rate_limit_info()}")
        logger.info(f"基础URL: {config.base_url}")
        logger.info(f"超时时间: {config.timeout}ms")
        logger.info(f"重试配置: 最大{config.retry.max_attempts}次, 延迟{config.retry.delay}ms")
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        timeout = ClientTimeout(total=self.config.get_timeout_seconds())
        self._session = aiohttp.ClientSession(timeout=timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self._session:
            await self._session.close()
    
    def _create_headers(self) -> Dict[str, str]:
        """创建HTTP请求头"""
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Repository-Info-Service/1.0"
        }
        
        if self.config.has_token():
            headers["Authorization"] = f"token {self.config.token}"
            logger.debug("已添加GitHub Token认证头")
        else:
            logger.debug("未配置Token，使用未认证模式")
        
        return headers
    
    async def get_repository_info(self, repo_full_name: str) -> Dict[str, Any]:
        """
        获取GitHub仓库信息
        
        Args:
            repo_full_name: 仓库全名，格式：owner/repo
            
        Returns:
            API响应的JSON数据
            
        Raises:
            Exception: 当所有重试都失败时
        """
        url = f"{self.config.base_url}/repos/{repo_full_name}"
        max_attempts = self.config.retry.max_attempts
        delay = self.config.get_retry_delay_seconds()
        
        for attempt in range(1, max_attempts + 1):
            try:
                logger.debug(f"第{attempt}次尝试获取仓库信息: {repo_full_name}")
                
                headers = self._create_headers()
                
                async with self._session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.debug(f"成功获取仓库信息: {repo_full_name}, 状态码: {response.status}")
                        return data
                    else:
                        await self._handle_http_error(response, repo_full_name, attempt, max_attempts)
                        
            except ClientError as e:
                logger.error(f"获取仓库信息时发生网络异常: {repo_full_name}, 第{attempt}次尝试: {str(e)}")
                
                if attempt == max_attempts:
                    raise Exception(f"获取仓库信息失败: {repo_full_name}")
                
                # 等待后重试
                await asyncio.sleep(delay * attempt)
                
            except Exception as e:
                logger.error(f"获取仓库信息时发生未知异常: {repo_full_name}, 第{attempt}次尝试: {str(e)}")
                
                if attempt == max_attempts:
                    raise Exception(f"获取仓库信息失败: {repo_full_name}")
                
                # 等待后重试
                await asyncio.sleep(delay * attempt)
        
        raise Exception(f"获取仓库信息失败，已达到最大重试次数: {repo_full_name}")
    
    async def _handle_http_error(self, response: aiohttp.ClientResponse, repo_full_name: str, 
                               attempt: int, max_attempts: int):
        """处理HTTP错误"""
        status = response.status
        
        logger.warning(f"获取仓库信息失败: {repo_full_name}, 状态码: {status}, 第{attempt}次尝试")
        
        if status == 403:
            logger.error(f"GitHub API速率限制 - 仓库: {repo_full_name}, 认证状态: {self.config.get_auth_status()}")
            if not self.config.has_token():
                logger.error("建议配置GitHub Token以提高速率限制（从60次/小时提升到5000次/小时）")
        elif status == 401:
            logger.error(f"GitHub Token认证失败 - 仓库: {repo_full_name}, 请检查Token是否有效")
        elif status == 404:
            logger.warning(f"仓库不存在: {repo_full_name}")
        
        # 最后一次尝试失败，抛出异常
        if attempt == max_attempts:
            raise Exception(f"API返回状态码: {status}")
        
        # 等待后重试
        delay = self.config.get_retry_delay_seconds()
        await asyncio.sleep(delay * attempt)
    
    def get_config_info(self) -> str:
        """获取当前配置信息（用于监控和调试）"""
        return (f"GitHub API配置 - 认证状态: {self.config.get_auth_status()}, "
                f"速率限制: {self.config.get_rate_limit_info()}, "
                f"超时: {self.config.timeout}ms")
