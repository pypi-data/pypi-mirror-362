from __future__ import annotations
import os, webbrowser, uuid, secrets

from flask import Flask, session, request, has_request_context
from .history_store import SQLHistoryStore as s_Store, InMemoryHistoryStore as i_Store
from collections import OrderedDict
from syntaxmatrix.llm_store import save_settings, load_settings, delete_key
from . import db, routes
from .themes import DEFAULT_THEMES
from .plottings import render_plotly, pyplot
from .file_processor import process_admin_pdf_files
from google import genai
from openai import OpenAI
from .vector_db import query_embeddings
from .vectorizer import embed_text
from syntaxmatrix.settings.prompts import SMX_PROFILE, SMX_INSTRUCTIONS
from typing import List
from .auth import init_auth_db
from syntaxmatrix.history_store import InMemoryHistoryStore as i_Store

from dotenv import load_dotenv
load_dotenv(override=False, verbose=False)

# ──────── framework‐local storage paths ────────
# this ensures the key & data always live under the package dir,
# regardless of where the developer `cd` into before launching.
_FRAMEWORK_DIR = os.path.dirname(__file__)
_SECRET_PATH   = os.path.join(_FRAMEWORK_DIR, ".smx_secret_key")
_HISTORY_DIR   = os.path.join(_FRAMEWORK_DIR, "smx_history")
os.makedirs(_HISTORY_DIR, exist_ok=True)

EDA_OUTPUT = {}  # global buffer for EDA output by session

class SyntaxMUI:
    def __init__(
            self, 
            host="127.0.0.1", 
            port="5050", 
            user_icon="👩🏿‍🦲",
            bot_icon='<img src="./static/icons/favicon.jpg" alt="bot icon" width="30"/>',
            favicon='❄️',
            site_title="smx", 
            site_logo='<img src="./static/icons/logoBigFull.png" alt="SMX Logo" width="120"/>',
            project_title="smxAI Engine", 
            theme_name="light"
        ):
        self.app = Flask(__name__)   
        self.get_app_secrete()      
        self.host = host
        self.port = port
        self.user_icon = user_icon
        self.bot_icon = bot_icon
        self.favicon = favicon
        self.site_title = site_title
        self.site_logo = site_logo
        self.project_title = project_title
        self.page = ""
        self.ui_mode = "default"
        self.theme_toggle_enabled = False
        self.profile = SMX_PROFILE
        self.instructions = SMX_INSTRUCTIONS    
        db.init_db()
        self.pages = db.get_pages()
        db.init_pdf_chunks_table()
        self.pdf_chunks = db.get_pdf_chunks()
        db.init_askai_table() 
        init_auth_db() 
        self.widgets = OrderedDict()
        self.theme = DEFAULT_THEMES.get(theme_name, DEFAULT_THEMES["light"])     
        self.system_output_buffer = ""  # Ephemeral buffer initialized  
        self.app_token = str(uuid.uuid4())  # NEW: Unique token for each app launch.
        self.admin_pdf_chunks = {}   # In-memory store for admin PDF chunks
        self.user_file_chunks = {}  # In-memory store of user‑uploaded chunks, scoped per chat session
        self.llm_client = self.load_llm_settings()
        self.llm = self.get_llm()
        routes.setup_routes(self)
    
    def init_app(app):
        import os, secrets
        if not app.secret_key:
            app.secret_key = secrets.token_urlsafe(32)   
    
    def get_app_secrete(self):
        if os.path.exists(_SECRET_PATH):
            self.app.secret_key = open(_SECRET_PATH, "r", encoding="utf-8").read().strip()
        else:
            new_key = secrets.token_urlsafe(32)
            open(_SECRET_PATH, "w", encoding="utf-8").write(new_key)
            self.app.secret_key = new_key

    def set_profile(self, profile):
        self.profile = profile
    
    def set_instructions(self, instructions):
        self.instructions = instructions
     
    def load_llm_settings(self):
        return load_settings()
    
    def save_llm_settings(self, provider:str, model:str, api_key:str):
        return save_settings(provider, model, api_key)
    
    def delete_llm_key(self):
        return delete_key()

    def get_llm(self):
        provider = self.llm_client["provider"].lower()
        model = self.llm_client["model"] 
        api_key = self.llm_client["api_key"]
        
        self.provider = provider
        self.model = model
        self.api_key = api_key

        if provider == "openai":
            return OpenAI(api_key=api_key)
        elif provider == "google":
            return OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        elif provider == "xai":
            return OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
        elif provider == "deepseek":
            return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def _get_visual_context(self):
        """Return the concatenated summaries for prompt injection."""
        if not self._recent_visual_summaries:
            return ""
        joined = "\n• " + "\n• ".join(self._recent_visual_summaries)
        return f"\n\nRecent visualizations:{joined}"

    def set_plottings(self, fig_or_html, note=None):
        sid = session.get("current_session", {}).get("id", "default")
        if not fig_or_html or (isinstance(fig_or_html, str) and fig_or_html.strip() == ""):
            EDA_OUTPUT[sid] = ""
            return

        html = None

        # ---- Plotly Figure support ----
        try:
            import plotly.graph_objs as go
            if isinstance(fig_or_html, go.Figure):
                html = fig_or_html.to_html(full_html=False)
        except ImportError:
            pass

        # ---- Matplotlib Figure support ----
        if html is None and hasattr(fig_or_html, "savefig"):
            html = pyplot(fig_or_html)

        # ---- Bytes (PNG etc.) support ----
        if html is None and isinstance(fig_or_html, bytes):
            import base64
            img_b64 = base64.b64encode(fig_or_html).decode()
            html = f"<img src='data:image/png;base64,{img_b64}'/>"

        # ---- HTML string support ----
        if html is None and isinstance(fig_or_html, str):
            html = fig_or_html

        if html is None:
            raise TypeError("Unsupported object type for plotting.")

        if note:
            html += f"<div style='margin-top:10px; text-align:center; color:#888;'><strong>{note}</strong></div>"

        wrapper = f'''
        <div style="
            position:relative; max-width:650px; margin:30px auto 20px auto;
            padding:20px 28px 10px 28px; background:#fffefc;
            border:2px solid #2da1da38; border-radius:16px;
            box-shadow:0 3px 18px rgba(90,130,230,0.06); min-height:40px;">
            <button id="eda-close-btn" onclick="closeEdaPanel()" style="
                position: absolute; top: 20px; right: 12px;
                font-size: 1.25em; background: transparent;
                border: none; color: #888; cursor: pointer;
                z-index: 2; transition: color 0.2s;">&times;</button>
            {html}
        </div>
        '''
        EDA_OUTPUT[sid] = wrapper

    def get_plottings(self):
        sid = session.get("current_session", {}).get("id", "default")
        return EDA_OUTPUT.get(sid, "")
    
    def load_sys_chunks(self, directory: str = "uploads/sys"):
        """
        Process all PDFs in `directory`, store chunks in DB and cache in-memory.
        Returns mapping { file_name: [chunk, ...] }.
        """
        mapping = process_admin_pdf_files(directory)
        self.admin_pdf_chunks = mapping
        return mapping

    def smpv_search(self, q_vec: List[float], top_k: int = 5):
        """
        Embed the input text and return the top_k matching PDF chunks.
        Each result is a dict with keys:
        - 'id'       : the embedding record UUID
        - 'score'    : cosine similarity score (0–1)
        - 'metadata' : dict, e.g. {'file_name': ..., 'chunk_index': ...}
        """
        # 2) Fetch nearest neighbors from our sqlite vector store
        results = query_embeddings(q_vec, top_k=top_k)
        return results

    def set_ui_mode(self, mode):
        if mode not in ["default", "card", "bubble", "smx"]:
            raise ValueError("UI mode must be one of: 'default', 'card', 'bubble', 'smx'.")
        self.ui_mode = mode

    @staticmethod
    def list_ui_modes():
        return "default", "card", "bubble", "smx"
    
    @staticmethod
    def list_themes():
        return list(DEFAULT_THEMES.keys())
    
    def set_theme(self, theme_name, theme):
        if theme_name in DEFAULT_THEMES:
            self.theme = DEFAULT_THEMES[theme_name]
        elif isinstance(theme, dict):
            self.theme["custom"] = theme
            DEFAULT_THEMES[theme_name] = theme
        else:
            self.theme = DEFAULT_THEMES["light"]
            raise ValueError("Theme must be 'light', 'dark', or a custom dict.")
    
    def enable_theme_toggle(self):
        self.theme_toggle_enabled = True
    
    def disable_theme_toggle(self):
        self.theme_toggle_enabled = False
    
    def columns(self, components):
        col_html = "<div style='display:flex; gap:10px;'>"
        for comp in components:
            col_html += f"<div style='flex:1;'>{comp}</div>"
        col_html += "</div>"
        return col_html
    
    def set_favicon(self, icon):
        self.favicon = icon

    def set_site_title(self, title):
        self.site_title = title
    
    def set_site_logo(self, logo):
        self.site_logo = logo

    def set_project_title(self, project_title):
        self.project_title = project_title

    def set_user_icon(self, icon):
        self.user_icon = icon

    def set_bot_icon(self, icon):
        self.bot_icon = icon

    def text_input(self, key, label, placeholder="Ask me anything"):
        if key not in self.widgets:
            self.widgets[key] = {"type": "text_input", "key": key, "label": label, "placeholder": placeholder}

    def get_text_input_value(self, key, default=""):
        q = session.get(key, default)
        intent = self._classify_query(q)
        return q, intent

    def clear_text_input_value(self, key):
        session[key] = ""
        session.modified = True
    
    def button(self, key, label, callback=None, stream=False):
        self.widgets[key] = {
            "type": "button", "key": key,
            "label": label,  "callback": callback,
            "stream": stream       
        }

    def file_uploader(self, key, label, accept_multiple_files=False, callback=None):
        if key not in self.widgets:
            self.widgets[key] = {
                "type": "file_upload",
                "key": key, "label": label,
                "accept_multiple": accept_multiple_files,
               "callback": callback
        }

    def get_file_upload_value(self, key):
        return session.get(key, None)
    
    def dropdown(self, key, options, label=None, callback=None):
        self.widgets[key] = {
            "type": "dropdown",
            "key": key,
            "label": label if label else key,
            "options": options,
            "callback": callback,
            "value": options[0] if options else None
        }

    def get_widget_value(self, key):
        return self.widgets[key]["value"] if key in self.widgets else None

    # ──────────────────────────────────────────────────────────────
    # Session-safe chat-history helpers
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def _sid() -> str:
        sid = session.get("_smx_sid")
        if not sid:
            # use the new _sid helper on the store instead of the old ensure_session_id
            sid = i_Store._sid(request.cookies.get("_smx_sid"))
        session["_smx_sid"] = sid
        session.modified = True
        return sid
    
    def get_chat_history(self) -> list[tuple[str, str]]:
        # now load the history for the _current_ chat session
        sid = self._sid()
        cid = self.get_session_id()
        return i_Store.load(sid, cid)
    
    def set_chat_history(self, history: list[tuple[str, str]], *, max_items: int | None = None) -> list[tuple[str, str]]:
        sid = self._sid()
        cid = self.get_session_id()
        i_Store.save(sid, cid, history)
        

        if session.get("user_id"):
            user_id = session["user_id"]
            cid = session["current_session"]["id"]
            title = session["current_session"]["title"]
            # persist both title + history 
            i_Store.save(user_id, cid, session["chat_history"], title)

        return history if max_items is None else history[-max_items:]

    def clear_chat_history(self):
        """
        Clear both the UI slice *and* the server-side history bucket
        for this session_id + chat_id.
        """
        if has_request_context():
            # Clear the in-memory store
            sid = self._sid()                 # your per-browser session ID
            cid = self.get_session_id()       # current chat UUID
            i_Store.save(sid, cid, [])         # wipe server history

            # Clear the cookie slice shown in the UI
            session["chat_history"] = []
            # Also clear out the “current_session” and past_sessions histories
            if "current_session" in session:
                session["current_session"]["history"] = []
            if "past_sessions" in session:
                session["past_sessions"] = [
                    {**s, "history": []} if s.get("id") == cid else s
                    for s in session["past_sessions"]
                ]
            session.modified = True
        else:
            self._fallback_chat_history = []

    
    def bot_message(self, content, max_length=20):
        history = self.get_chat_history()
        history.append(("Bot", content))
        self.set_chat_history(history)

    def plt_plot(self, fig):
        summary = describe_matplotlib(fig)
        self._add_visual_summary(summary)          
        html = pyplot(fig)
        self.bot_message(html)

    def plotly_plot(self, fig):
        try:
            summary = describe_plotly(fig)
            self._add_visual_summary(summary)      
            html = render_plotly(fig)
            self.bot_message(html)
        except Exception as e:
            self.error(f"Plotly rendering failed: {e}")

    def write(self, content):
        self.bot_message(content)

    def markdown(self, md_text):
        try:
            import markdown
            html = markdown.markdown(md_text)
        except ImportError:
            html = md_text
        self.write(html)
    
    def latex(self, math_text):
        self.write(f"\\({math_text}\\)")
    
    def error(self, content):
        self.bot_message(f'<div style="color:red; font-weight:bold;">{content}</div>')

    def warning(self, content):
        self.bot_message(f'<div style="color:orange; font-weight:bold;">{content}</div>')

    def success(self, content):
        self.bot_message(f'<div style="color:green; font-weight:bold;">{content}</div>')

    def info(self, content):
        self.bot_message(f'<div style="color:blue;">{content}</div>')

    def get_session_id(self):
        """Return current chat’s UUID (so we can key uploaded chunks)."""
        return session.get("current_session", {}).get("id")

    def add_user_chunks(self, session_id, chunks):
        """Append these text‐chunks under that session’s key."""
        self.user_file_chunks.setdefault(session_id, []).extend(chunks)

    def get_user_chunks(self, session_id):
        """Get any chunks that this session has uploaded."""
        return self.user_file_chunks.get(session_id, [])

    def clear_user_chunks(self, session_id):
        """Remove all stored chunks for a session (on chat‑clear or delete)."""
        self.user_file_chunks.pop(session_id, None)
    
    # ////////////////////////////////////////////////////////////

    @staticmethod
    def generate_contextual_title(chat_history):
            
        def get_generated_title(conversation):
            gemini_api_key = os.environ.get("GEMINI_API_KEY")
            model = "gemma-3n-e4b-it"

            llm = genai.Client(api_key=gemini_api_key)        
            response = llm.models.generate_content(
                model=model,
                contents=f"""
                    Generate a contextual title (5 short words max) from the given Conversation History: \n{conversation}.
                    The title should be concise, relevant, and capture the essence of the conversation, and with no preamble. 
                    return only the title.
                """
            )
            return response.text
        
        conversation = "\n".join([f"{role}: {msg}" for role, msg in chat_history])      
        title = get_generated_title(conversation)
        return title
    
    def stream_write(self, chunk: str, end=False):
        """Push a token to the SSE queue and, when end=True,
        persist the whole thing to chat_history."""
        from .routes import _stream_q
        _stream_q.put(chunk)              # live update
        if end:                           # final flush → history
            self.bot_message(chunk)       # persists the final message
    
    def _classify_query(self, query: str) -> str:
        
        provider = self.llm_client['provider']
        model = self.llm_client['model']
        api_key = self.llm_client['api_key']

        prompt = [
                {
                    "role": "system",
                    "content": (
                        "You’re an intent router. Classify questions into exactly one of: "
                        "`none`, `user_docs`, `system_docs`, `hybrid`.  "
                        "Use `system_docs` if the user is asking about factual or technical details "
                        "that live in the company’s knowledge base.  "
                        "Use `user_docs` if the user is asking about content the user personally uploaded.  "
                        "Use `hybrid` if the user query needs both the system_docs and the user_docs. "
                        "Use `none` only for greetings or purely conversational chat, or where just your training knowledge is enough."
                    )
                },
                    # few-shot examples
                {"role": "user","content": "Hi there!"},
                { "role": "assistant", "content": "none" },

                { "role": "user", "content": "Summarize my uploaded marketing deck." },
                { "role": "assistant", "content": "user_docs" },

                { "role": "user", "content": "What’s the SLA for our email-delivery service?" },
                { "role": "assistant", "content": "system_docs" },

                { "role": "user", "content": "What are my colleaues' surnames, in the contact list I sent you?" },
                { "role": "assistant", "content": "hybrid" },

                { "role": "user", "content": query }
        ]

        response = self.llm.chat.completions.create(
            model=self.model,
            messages=prompt,
            temperature=0,
            max_tokens=200
        )
        intent = response.choices[0].message.content.strip().lower()
        return intent

    def process_query(self, query, context, history, stream=False):
        
        prompt = [
                {"role": "system", "content": self.profile},
                {"role": "user",   "content": self.instructions},
                {"role": "assistant",
                "content": f"Query: {query}\n\nContext1: {context}\n\n"
                            f"History: {history}\n\nAnswer: "}
            ]

        try:
            response = self.llm.chat.completions.create(
                model=self.model,
                messages=prompt,
                temperature=0.1,
                max_tokens=1024,
                stream=stream
            )

            if stream:
                # -------- token streaming --------
                parts = []
                for chunk in response:
                    token = getattr(chunk.choices[0].delta, "content", "")
                    if not token:
                        continue
                    parts.append(token)
                    self.stream_write(token)    

                self.stream_write("[END]")   # close the SSE bubble  
                answer = "".join(parts)          
                return answer      
            else:
                # -------- one-shot buffered --------
                answer = response.choices[0].message.content  
                return answer 
        except Exception as e:
            return f"Error: {str(e)}"


    def ai_generate_code(self, question, df):
        from syntaxmatrix.utils import strip_describe_slice, drop_bad_classification_metrics

        context = f"Columns: {list(df.columns)}\nDtypes: {df.dtypes.astype(str).to_dict()}\n"
        prompt = (
            f"You are an expert Python data analyst. Given the dataframe `df` with the following context:\n{context}\n"
            f"Write clean, working Python code that answers the question below. "
            f"DO NOT explain, just output the code only (NO comments or text):\n"
            f"Question: {question}\n"
            f"Output only the working code needed. Assume df is already defined."
            f"Produce at least one visible result"
            f"(syntaxmatrix.display.show(), display(), plt.show())."
        )
        response = self.llm.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=1024,
        )
        code = response.choices[0].message.content
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()

        code = strip_describe_slice(code)
        code = drop_bad_classification_metrics(code, df)
        return code.strip()


    def run(self):
        url = f"http://{self.host}:{self.port}/"
        webbrowser.open(url)
        self.app.run(host=self.host, port=self.port, debug=False)
    