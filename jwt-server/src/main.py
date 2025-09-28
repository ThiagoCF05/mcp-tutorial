import jwt
import os
from fastapi import FastAPI, HTTPException
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from config import PRIVATE_KEY, JWT_ALGORITHM, JWT_ISSUER, JWT_AUDIENCE
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="JWT Server", version="1.0.0")

with open(PRIVATE_KEY, "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,  # Set password if your key is encrypted
        backend=default_backend(),
    )


@app.post("/token")
async def create_access_token(username: str, password: str):
    # In a real application, validate username and password against a database
    if username == os.getenv("USERNAME") and password == os.getenv("PASSWORD"):
        scope = ["read:data"]
        to_encode = {
            "sub": username,
            "scope": scope,
            "iss": JWT_ISSUER,
            "aud": JWT_AUDIENCE,
        }
        encoded_jwt = jwt.encode(to_encode, private_key, algorithm=JWT_ALGORITHM)
        return {"access_token": encoded_jwt, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
