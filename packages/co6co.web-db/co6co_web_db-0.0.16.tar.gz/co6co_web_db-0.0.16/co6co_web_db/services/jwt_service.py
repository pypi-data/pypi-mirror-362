import jwt
import datetime
from sanic.request import Request
from typing import Any
from co6co.utils import log


class JWT_service:
    def __init__(self, secret: str, issuer: str = "JWT+SERVICE") -> None:
        self._secret = secret
        self._issuer = issuer
        pass

    def encode(self, data, expire_seconds: int = 86400) -> str:
        """
        加密数据： 
        """
        dic = {
            'exp': datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=expire_seconds),  # 过期时间
            'iat': datetime.datetime.now(datetime.timezone.utc),  # 开始时间
            'iss': self._issuer,  # 签名
            'data': data  # 内容一般放用户ID 和开始时间
        }
        return jwt.encode(dic, self._secret, algorithm="HS256")  # 加密字符

    def decode(self, token: str) -> Any | None:
        try:
            if token == None or token == "":
                log.warn("token is None!")
                return None
            # 解密签名  //
            return jwt.decode(token, self._secret, issuer=self._issuer, algorithms=['HS256'])
        except Exception as e:
            log.warn("校验失败:", e)
            return None


async def createToken(SECRET: str, data: dict, expire_seconds: int = 86400):
    """
    登录时生成tooken
    """
    svc = JWT_service(SECRET)
    result = svc.encode(data, expire_seconds)
    return result


def decodeToken(token: str, SECRET: str):
    """
    解密 token
    """
    svc = JWT_service(SECRET)
    if token == None:
        log.warn("token is None")
        return None
    result = svc.decode(token)
    if result == None or 'data' not in result:
        return None
    return result["data"]


async def validToken(request: Request, SECRET: str):
    """
    验证token 是否有效
    request.app.config.SECRET
    """
    result = decodeToken(request.token, SECRET)
    if result == None:
        return False
    await setCurrentUser(request, result)
    return True


async def setCurrentUser(request: Request, data: dict):
    """
    设置当前用户
    """
    request.ctx.current_user = data
    return True
