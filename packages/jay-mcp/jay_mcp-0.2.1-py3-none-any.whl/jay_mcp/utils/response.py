"""
响应工具类
对应Java中的R.java
"""
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')

class R(BaseModel, Generic[T]):
    """统一响应格式"""
    code: str = "200"
    data: Optional[T] = None
    message: Optional[str] = None
    
    @classmethod
    def ok(cls, data: T = None) -> 'R[T]':
        """成功响应"""
        return cls(code="200", data=data)
    
    @classmethod
    def fail(cls, message: str, code: str = "500") -> 'R[T]':
        """失败响应"""
        return cls(code=code, message=message)
    
    @classmethod
    def result(cls, code: str, message: str, data: T = None) -> 'R[T]':
        """自定义响应"""
        return cls(code=code, message=message, data=data)
