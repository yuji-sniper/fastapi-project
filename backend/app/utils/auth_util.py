from fastapi import Request


def get_request_token(request: Request) -> str:
    """
    Extract the API token from the Authorization header.
    """
    authorization_header = request.headers.get("Authorization")
    
    if authorization_header and " " in authorization_header:
        return authorization_header.split(" ")[1]
    
    return ""
