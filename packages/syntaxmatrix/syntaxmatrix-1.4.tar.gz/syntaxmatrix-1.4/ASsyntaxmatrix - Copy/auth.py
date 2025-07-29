import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional, Dict
from functools import wraps
from flask import session, redirect, url_for, flash, request

from dotenv import load_dotenv

load_dotenv(override=False, verbose=False)


# 1) Database path under data/
AUTH_DB_PATH = os.path.join(os.getcwd(), "data", "auth.db")
os.makedirs(os.path.dirname(AUTH_DB_PATH), exist_ok=True)

def _get_conn():
    conn = sqlite3.connect(AUTH_DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_auth_db():
    """Create users table and seed the superadmin from env vars."""
    conn = _get_conn()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """)
    # seed the CEO superadmin
    superadmin_email = "ceo@syntaxmatrix.com"
    superadmin_username = "ceo"
    supperadmin_password = "S3cr3tP@ss"
    if superadmin_username and supperadmin_password:
        hashed = generate_password_hash(supperadmin_password)
        conn.execute("""
          INSERT INTO users (email, username, password, role)
          VALUES (?, ?, ?, 'superadmin')
          ON CONFLICT(username) DO UPDATE SET password=excluded.password, role='superadmin';
        """, (superadmin_email, superadmin_username, hashed))
    conn.commit()
    conn.close()

def register_user(email:str, username:str, password:str, role:str = "user") -> bool:
    """Return True if registration succeeded, False if username taken."""
    hashed = generate_password_hash(password)
    conn = _get_conn()
    try:
        conn.execute(
            "INSERT INTO users (email, username, password, role) VALUES (?, ?, ?, ?)",
            (email, username, hashed, role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate(email:str, password:str) -> Optional[Dict]:
    """Return user dict if creds match, else None."""
    conn = _get_conn()
    cur = conn.execute(
        "SELECT id, email, username, password, role FROM users WHERE email = ?",
        (email,)
    )
    row = cur.fetchone()
    conn.close()
    if row and check_password_hash(row[3], password):
        return {"id": row[0], "email":row[1], "username": row[2], "role": row[4]}
    return None

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to access this page.")
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to access this page.")
            return redirect(url_for("login", next=request.path))
        if session.get("role") not in ("admin", "superadmin"):
            flash("You do not have permission to access this page.")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated

def superadmin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to access this page.")
            return redirect(url_for("login", next=request.path))
        if session.get("role") != "superadmin":
            flash("You do not have permission to access this page.")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated