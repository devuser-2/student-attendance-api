from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        print("TOKEN RECEIVED:", credentials.credentials)

        token = credentials.credentials

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload.get("sub")

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))