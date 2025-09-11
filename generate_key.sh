openssl genrsa -out mcp-tutorial.pem 2048
openssl rsa -pubout -in mcp-tutorial.pem -out mcp-tutorial.pub.pem