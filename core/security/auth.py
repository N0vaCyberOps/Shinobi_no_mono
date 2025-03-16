"""
Moduł uwierzytelniania API z wykorzystaniem OAuth2 i JWT.
Zgodny ze standardem RFC 6749.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from core.utils.config_manager import ConfigManager

class AuthHandler:
    def __init__(self):
        self._config = ConfigManager.get_security_config()
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self._secret = self._config["jwt_secret"]
        self._algorithm = self._config["jwt_algorithm"]

    def create_access_token(self, username: str) -> str:
        """Generowanie tokenu JWT z ważnością 1 godziny."""
        expire = datetime.utcnow() + timedelta(hours=1)
        payload = {
            "sub": username,
            "exp": expire,
            "scope": "user"
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    async def get_current_user(
        self, 
        token: str = Depends(oauth2_scheme)
    ) -> str:
        """Walidacja tokenu i ekstrakcja użytkownika."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidłowe dane uwierzytelniające",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
            username: Optional[str] = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        return username
