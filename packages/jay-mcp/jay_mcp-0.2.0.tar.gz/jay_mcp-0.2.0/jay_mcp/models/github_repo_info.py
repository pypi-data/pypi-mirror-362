"""
GitHub仓库信息数据模型
对应Java中的GitHubRepoInfo.java
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class GitHubRepoInfo(BaseModel):
    """GitHub仓库信息数据模型"""
    
    owner: Optional[str] = Field(None, description="仓库所有者", example="facebook")
    repo: Optional[str] = Field(None, description="仓库名称", example="react")
    full_name: Optional[str] = Field(None, description="仓库全名", example="facebook/react")
    
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="最后更新时间")
    pushed_at: Optional[datetime] = Field(None, description="最后推送时间")
    
    stargazers_count: Optional[int] = Field(None, description="星标数量", example=220000)
    language: Optional[str] = Field(None, description="主要编程语言")
    html_url: Optional[str] = Field(None, description="仓库HTML链接")
    forks_count: Optional[int] = Field(None, description="Fork数量")
    watchers_count: Optional[int] = Field(None, description="观察者数量")
    
    status: Optional[str] = Field(None, description="查询状态", example="SUCCESS")
    error_message: Optional[str] = Field(None, description="错误信息")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }
    
    @classmethod
    def success(cls, owner: str, repo: str) -> 'GitHubRepoInfo':
        """创建成功的仓库信息对象"""
        return cls(
            owner=owner,
            repo=repo,
            full_name=f"{owner}/{repo}",
            status="SUCCESS"
        )
    
    @classmethod
    def failure(cls, owner: str, repo: str, error_message: str) -> 'GitHubRepoInfo':
        """创建失败的仓库信息对象"""
        return cls(
            owner=owner,
            repo=repo,
            full_name=f"{owner}/{repo}",
            status="FAILED",
            error_message=error_message
        )
