# syntaxmatrix/llm_store.py
import os
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet, InvalidToken
from .workspace_db import SessionLocal, Workspace


# ── ensure a stable encryption key, no env var needed ──────────
KEY_PATH = os.path.join(os.getcwd(), "uploads", "fernet.key")
if os.path.exists(KEY_PATH):
    __FERNET = Fernet(open(KEY_PATH, "rb").read())
else:
    key = Fernet.generate_key()
    os.makedirs(os.path.dirname(KEY_PATH), exist_ok=True)
    open(KEY_PATH, "wb").write(key)
    __FERNET = Fernet(key)

def _session_and_ws() -> tuple[Session, Workspace]:
    sess = SessionLocal()
    ws  = sess.query(Workspace).filter_by(name="default").first()
    if ws is None:
        ws = Workspace(name="default")
        sess.add(ws)
        sess.commit()
    return sess, ws

# ------------------------------------------------------------------
# 2. Public helpers
# ------------------------------------------------------------------
def save_settings(provider: str, model: str, api_key: str):
    try:
        sess, ws = _session_and_ws()
        ws.llm_provider = provider
        ws.llm_model = model
        if api_key and api_key != "********":          
            ws.llm_api_key = __FERNET.encrypt(api_key.encode())
        sess.commit()
        sess.close()
        return True
    except:
        return False

def load_settings() -> dict:
    sess, ws = _session_and_ws()
    try:
        key = (
            __FERNET.decrypt(ws.llm_api_key).decode()
            if ws.llm_api_key
            else ""
        )
    except InvalidToken:
        key = ""
    result = {
        "provider": ws.llm_provider,
        "model": ws.llm_model,
        "api_key": key,
    }
    sess.close()
    return result

def delete_key() -> bool:
    sess, ws = _session_and_ws()
    if ws.llm_api_key:
        ws.llm_api_key = b""
        sess.commit()
        sess.close()
        return True
    sess.close()
    return False