from typing import Optional
from uuid import uuid4

from fastapi import Cookie


def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid4())
    return session_id