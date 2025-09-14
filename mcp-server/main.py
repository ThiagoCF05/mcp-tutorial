# server.py
from dotenv import load_dotenv

load_dotenv()

from fastmcp import FastMCP
from src.config import PUBLIC_KEY, JWT_ISSUER, JWT_AUDIENCE, JWT_ALGORITHM
from src.tools import query_fundamental_analysis
from src.utils import get_verifier

mcp = FastMCP(
    name="Fundamental Analysis SQL Database", 
    auth=get_verifier(public_key_path=PUBLIC_KEY, jwt_issuer=JWT_ISSUER, jwt_audience=JWT_AUDIENCE, jwt_algorithm=JWT_ALGORITHM)
)

mcp.tool(query_fundamental_analysis)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8080, path="/mcp", host="0.0.0.0")