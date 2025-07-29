"""
GitHub API配置类
对应Java中的GitHubApiConfig
"""
import os
from typing import Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class RetryConfig(BaseModel):
    """重试配置"""
    max_attempts: int = 3
    delay: int = 1000  # 毫秒

class GitHubApiConfig(BaseSettings):
    """GitHub API配置"""
    
    # GitHub API配置
    base_url: str = "https://api.github.com"
    token: Optional[str] = None
    timeout: int = 30000  # 毫秒
    
    # 重试配置
    retry: RetryConfig = RetryConfig()
    
    class Config:
        env_prefix = "GITHUB_"
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 从环境变量读取token
        if not self.token:
            self.token = os.getenv("GITHUB_TOKEN")
    
    def has_token(self) -> bool:
        """检查是否配置了Token"""
        return self.token is not None and len(self.token.strip()) > 0
    
    def get_auth_status(self) -> str:
        """获取认证状态"""
        if self.has_token():
            return f"已认证 (Token: {self.token[:8]}...)"
        return "未认证 (使用公共API)"
    
    def get_rate_limit_info(self) -> str:
        """获取速率限制信息"""
        if self.has_token():
            return "5000次/小时 (已认证)"
        return "60次/小时 (未认证)"
    
    def get_timeout_seconds(self) -> float:
        """获取超时时间（秒）"""
        return self.timeout / 1000.0
    
    def get_retry_delay_seconds(self) -> float:
        """获取重试延迟（秒）"""
        return self.retry.delay / 1000.0
