from fastmcp.server.auth.providers.jwt import JWTVerifier
from cryptography.hazmat.primitives import serialization


def get_verifier(
    public_key_path: str, jwt_issuer: str, jwt_audience: str, jwt_algorithm: str
) -> JWTVerifier:
    """
    Returns a JWTVerifier instance.

    Args:
        public_key_path (str): The path to the public key file.
        jwt_issuer (str): The issuer of the JWT.
        jwt_audience (str): The audience of the JWT.
        jwt_algorithm (str): The algorithm used to sign the JWT.

    Returns:
        JWTVerifier: A JWTVerifier instance.
    """
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
        )

    public_key_str = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return JWTVerifier(
        public_key=public_key_str,
        issuer=jwt_issuer,
        audience=jwt_audience,
        algorithm=jwt_algorithm,
    )
