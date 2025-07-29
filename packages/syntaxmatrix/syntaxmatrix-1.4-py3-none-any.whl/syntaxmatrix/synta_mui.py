# syntaxmatrix/synta_mui.py
import os
import webbrowser
import time
from flask import Flask, request, render_template_string, redirect, url_for, session, has_request_context
from collections import OrderedDict
from . import db  # Relative import for database functions

# Built-in themes.
DEFAULT_THEMES = {
    "light": {
        "background": "#f4f7f9",
        "text_color": "#333",
        "nav_background": "#007acc",
        "nav_text": "#fff",
        "chat_background": "#eef2f7",
        "chat_border": "#e0e0e0",
        "widget_background": "#dddddd",
        "widget_border": "#007acc",
        "sidebar_background": "#eeeeee",
        "sidebar_text": "#333"
    },
    "dark": {
        "background": "#1e1e1e",
        "text_color": "#ccc",
        "nav_background": "#333",
        "nav_text": "#fff",
        "chat_background": "#2e2e2e",
        "chat_border": "#555",
        "widget_background": "#444",
        "widget_border": "#007acc",
        "sidebar_background": "#2a2a2a",
        "sidebar_text": "#ccc"
    }
}

ICON = "👀"

class SyntaxMUI:
    def __init__(self, title=ICON + "SMX UI", project_title=ICON + "SyntaxMatrix UI", host="127.0.0.1", port=5000, theme="light"):
        self.app = Flask(__name__)
        self.app.secret_key = "syntaxmatrix_secret"
        self.title = title
        self.host = host
        self.port = port
        self.project_title = project_title

        # Initialize DB and load pages.
        db.init_db()
        self.pages = db.get_pages()

        # Default UI mode: "default" or "bubble".
        self.ui_mode = "default"

        # Widgets dictionary for main UI.
        self.widgets = OrderedDict()
        # New: Sidebar widget dictionary.
        self.sidebar_widgets = OrderedDict()

        # Default widget position: "top" or "bottom"
        self.widget_position = "bottom"

        # Set theme.
        if theme in DEFAULT_THEMES:
            self.theme = DEFAULT_THEMES[theme]
        elif isinstance(theme, dict):
            self.theme = theme
        else:
            self.theme = DEFAULT_THEMES["light"]

        self.setup_routes()

    def set_ui_mode(self, mode):
            """Set the UI mode: 'default', 'bubble', or 'card'."""
            if mode not in ["default", "bubble", "card"]:
                raise ValueError("UI mode must be 'default', 'bubble', or 'card'.")
            self.ui_mode = mode
    
    def set_project_title(self, project_title):
        self.project_title = project_title

    def set_ui_mode(self, mode):
        """Set the UI mode: 'default' or 'bubble'."""
        if mode not in ["default", "card", "bubble"]:
            raise ValueError("UI mode list: 'default', 'card', 'bubble'.")
        self.ui_mode = mode

    def set_theme(self, theme):
        """Set the UI theme. Accepts 'light', 'dark', or a custom dict."""
        if theme in DEFAULT_THEMES:
            self.theme = DEFAULT_THEMES[theme]
        elif isinstance(theme, dict):
            self.theme = theme
        else:
            raise ValueError("Theme must be 'light', 'dark', or a custom dict.")

    def enable_theme_toggle(self):
        """Enable the dynamic theme toggle widget. When enabled, a 'Toggle Theme' link appears in the nav."""
        self.theme_toggle_enabled = True

    def columns(self, *components):
        col_html = "<div style='display:flex; gap:10px;'>"
        for comp in components:
            col_html += f"<div style='flex:1;'>{comp}</div>"
        col_html += "</div>"
        return col_html
    
      # Public API for sidebar widgets.
    def sidebar_text_input(self, key, label, placeholder=""):
        if key not in self.sidebar_widgets:
            self.sidebar_widgets[key] = {"type": "text_input", "key": key, "label": label, "placeholder": placeholder}

    def sidebar_button(self, key, label, callback=None):
        if key not in self.sidebar_widgets:
            self.sidebar_widgets[key] = {"type": "button", "key": key, "label": label, "callback": callback}

    def get_sidebar_value(self, key, default=""):
        return session.get(key, default)

    def clear_sidebar_value(self, key):
        session[key] = ""
        session.modified = True

    def setup_routes(self):
        def head_html():
           return f"""
           <!DOCTYPE html>
            <html>
            <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background: {self.theme["background"]};
                    color: {self.theme["text_color"]};
                }}
                nav {{
                    background: {self.theme["nav_background"]};
                    padding: 10px 20px;
                    text-align: left;
                }}
                nav a {{
                    color: {self.theme["nav_text"]};
                    text-decoration: none;
                    margin: 0 15px;
                    font-size: 1.1em;
                }}
                """

        @self.app.route("/", methods=["GET", "POST"])
        def home():
            if request.method == "POST":
                # Process main UI widgets.
                for key, widget in self.widgets.items():
                    if widget["type"] == "text_input":
                        session[key] = request.form.get(key, widget.get("placeholder", ""))
                    elif widget["type"] == "file_upload":
                        if key in request.files:
                            file_obj = request.files[key]
                            try:
                                content = file_obj.read().decode("utf-8", errors="replace")
                            except Exception:
                                content = "<binary data>"
                            session[key] = {"filename": file_obj.filename, "content": content}
                    elif widget["type"] == "button":
                        if key in request.form and widget.get("callback"):
                            widget["callback"]()
                # Process sidebar widgets.
                for key, widget in self.sidebar_widgets.items():
                    if widget["type"] == "text_input":
                        session[key] = request.form.get(key, widget.get("placeholder", ""))
                    elif widget["type"] == "button":
                        if key in request.form and widget.get("callback"):
                            widget["callback"]()
                return redirect(url_for("home"))

            # Refresh pages.
            self.pages = db.get_pages()
            if "theme" in session:
                self.set_theme(session["theme"])
            nav_html = self._generate_nav()
            chat_html = self._render_chat_history()
            widget_html = self._render_widgets()
            sidebar_html = self._render_sidebar()

            # Updated scroll script: scroll the entire window to the bottom.           
            scroll_js = """
            <script>
              window.onload = function() {
                var chatContainer = document.getElementById("chat-history");
                if(chatContainer) {
                    chatContainer.scrollTop = chatContainer.scrollHeight - 100;
                }
                window.scrollTo(0, document.body.scrollHeight - 100);
              };
             
            </script>
            """

            # Define chat_css based on UI mode
           # Updated chat CSS with card mode
            # In setup_routes() where chat_css is defined for bubble mode:
            if self.ui_mode == "bubble":
                chat_css = f"""
                .chat-message {{
                    position: relative;
                    max-width: 70%;
                    margin: 10px 0;
                    padding: 12px 18px;
                    border-radius: 20px;
                    animation: fadeIn 0.9s forwards;
                    clear: both;
                }}
                .chat-message.user {{
                    background: #dcf8c6;
                    float: right;
                    margin-right: 15px;
                    border-bottom-right-radius: 2px;
                }}
                .chat-message.user::after {{
                    content: '';
                    position: absolute;
                    right: -8px;
                    top: 12px;
                    width: 0;
                    height: 0;
                    border: 8px solid transparent;
                    border-left-color: #dcf8c6;
                    border-right: 0;
                }}
                .chat-message.bot {{
                    background: #ffffff;
                    float: left;
                    margin-left: 15px;
                    border-bottom-left-radius: 2px;
                    border: 1px solid {self.theme['chat_border']};
                }}
                .chat-message.bot::before {{
                    content: '';
                    position: absolute;
                    left: -8px;
                    top: 12px;
                    width: 0;
                    height: 0;
                    border: 8px solid transparent;
                    border-right-color: #ffffff;
                    border-left: 0;
                }}
                .chat-message p {{
                    margin: 0;
                    padding: 0;
                    word-wrap: break-word;
                }}
                """
            elif self.ui_mode == "card":
                chat_css = f"""
                .chat-message {{
                    display: block;
                    margin: 15px 0;
                    padding: 18px 22px;
                    border-radius: 12px;
                    animation: fadeIn 0.9s forwards;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    max-width: 80%;
                    position: relative;
                }}
                .chat-message.user {{
                    background: {self.theme['chat_background']};
                    margin-left: auto;
                    border: 1px solid {self.theme['chat_border']};
                    border-right: 4px solid {self.theme['nav_background']};
                }}
                .chat-message.bot {{
                    background: {self.theme['chat_background']};
                    border: 1px solid {self.theme['chat_border']};
                    border-left: 4px solid {self.theme['nav_background']};
                }}
                .chat-message p {{
                    margin: 0;
                    font-size: 0.95em;
                    line-height: 1;
                }}
                .chat-message strong {{
                    display: block;
                    margin-bottom: 8px;
                    color: {self.theme['nav_background']};
                    font-size: 0.9em;
                }}
                """
            elif self.ui_mode == "default":  # Default mode
                chat_css = f"""
                .chat-message {{
                    display: block;
                    width: 90%;
                    margin-bottom: 10px;
                    padding: 12px 18px;
                    border-radius: 8px;
                    animation: fadeIn 0.9s forwards;
                }}
                .chat-message.user {{
                    background: #e1f5fe;
                    text-align: right;
                    margin-left: auto;
                    max-width: 50%;
                }}
                .chat-message.bot {{
                    background: #ffffff;
                    border: 1px solid {self.theme["chat_border"]};
                    text-align: left;
                    max-width: 80%;
                }}
                """

            page_html = f"""
            {head_html()}

                /* Sidebar Styles */
                #sidebar {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    bottom: 0;
                    width: 240px;
                    background: {self.theme["sidebar_background"]};
                    color: {self.theme["sidebar_text"]};
                    overflow-y: auto;
                    padding: 15px;
                    box-shadow: 2px 0 5px rgba(0,0,0,0.1);
                }}
                #sidebar h3 {{
                    margin-top: 0;
                }}
                #sidebar form {{
                    margin-bottom: 15px;
                }}
                #sidebar input[type="text"] {{
                    width: 100%;
                    padding: 8px;
                    margin-bottom: 5px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }}
                #sidebar button {{
                    width: 100%;
                    padding: 8px;
                    border: none;
                    border-radius: 4px;
                    background: {self.theme["nav_background"]};
                    color: {self.theme["nav_text"]};
                    cursor: pointer;
                }}
                #sidebar button:hover {{
                    background: #005fa3;
                }}

                #chat-history {{
                    width: 100%;
                    max-width: 850px;
                    margin: 10px auto 25px auto;
                    padding: 10px;
                    padding-bottom: 10px;
                    background: {self.theme["chat_background"]};
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                    overflow-y: auto;
                    min-height: 350px;
                }}
                {chat_css}
                @keyframes fadeIn {{
                    from {{ opacity: 0; }}
                    to {{ opacity: 1; }}
                }}
            </style>
            <title>{self.title}</title>
            </head>
            <body>
            <nav>{nav_html}</nav>
            <div id="chat-history">{chat_html}</div>
            <div id="widget-container">{widget_html}</div>
            {scroll_js}
            </body>
            </html>
            """
            return render_template_string(page_html)

        @self.app.route("/page/<page_name>")
        def view_page(page_name):
            nav_html = self._generate_nav()
            if page_name in self.pages:
                content = self.pages[page_name]

            view_page_html = f"""
            {head_html()}

                @keyframes fadeIn {{
                    from {{ opacity: 0; }}
                    to {{ opacity: 1; }}
                }}
                
            </style>
            <title>{ICON}{page_name}</title>
            </head>
            <body>
            <nav>{nav_html}</nav>
            </body>
            <h1 style='text-align:center;'>{ICON}{page_name}</h1><div style='max-width:800px;margin:20px auto;padding:20px;background:#fff;border-radius:8px;'>{content}</div><div><a class='button' href='/'>Return to Home</a></div"
            </html>
            """
            return render_template_string(view_page_html)

        @self.app.route("/admin", methods=["GET", "POST"])
        def admin_panel():
            if request.method == "POST":
                action = request.form.get("action")
                if action == "add_page":
                    page_name = request.form.get("page_name", "").strip()
                    page_content = request.form.get("page_content", "").strip()
                    if page_name and page_name not in self.pages:
                        db.add_page(page_name, page_content)
                elif action == "update_page":
                    old_name = request.form.get("old_name", "").strip()
                    new_name = request.form.get("new_name", "").strip()
                    new_content = request.form.get("new_content", "").strip()
                    if old_name in self.pages and new_name:
                        db.update_page(old_name, new_name, new_content)
                elif action == "delete_page":
                    del_page = request.form.get("delete_page", "").strip()
                    if del_page in self.pages:
                        db.delete_page(del_page)
                return redirect(url_for("admin_panel"))

            self.pages = db.get_pages()
            return render_template_string(f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>{ICON}Admin Panel</title>
                    <style>
                      body {{
                          font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                          background: #f4f7f9;
                          padding: 20px;
                      }}
                      form {{
                          margin-bottom: 20px;
                          background: #fff;
                          padding: 15px;
                          border-radius: 8px;
                          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                      }}
                      input, textarea, select {{
                          padding: 10px;
                          font-size: 1em;
                          margin: 5px 0;
                      title    width: 100%;
                          border: 1px solid #ccc;
                          border-radius: 4px;
                      }}
                      button {{
                          padding: 10px 20px;
                          font-size: 1em;
                          background: #007acc;
                          color: #fff;
                          border: none;
                          border-radius: 4px;
                          cursor: pointer;
                      }}
                      button:hover {{
                          background: #005fa3;
                      }}
                    </style>
                </head>
                <body>
                    <h1>Admin Panel</h1>
                    <form method="post">
                        <h3>Add a Page</h3>
                        <input type="text" name="page_name" placeholder="Page Name" required>
                        <textarea name="page_content" placeholder="Page Content"></textarea>
                        <button type="submit" name="action" value="add_page">Add Page</button>
                    </form>
                    <form method="post">
                        <h3>Update an Existing Page</h3>
                        <select name="old_name">
                            {''.join(f'<option value="{p}">{p}</option>' for p in self.pages)}
                        </select>
                        <input type="text" name="new_name" placeholder="New Page Name" required>
                        <textarea name="new_content" placeholder="New Page Content"></textarea>
                        <button type="submit" name="action" value="update_page">Update Page</button>
                    </form>
                    <form method="post">
                        <h3>Delete a Page</h3>
                        <select name="delete_page">
                            {''.join(f'<option value="{p}">{p}</option>' for p in self.pages)}
                        </select>
                        <button type="submit" name="action" value="delete_page">Delete Page</button>
                    </form>
                    <p><a href="/">Return to Home</a></p>
                </body>
                </html>
            """)

        @self.app.route("/toggle_theme", methods=["GET"])
        def toggle_theme():
            current = session.get("theme", "light")
            new_theme = "dark" if current == "light" else "light"
            session["theme"] = new_theme
            # Update the instance theme accordingly.
            self.set_theme(new_theme)
            return redirect(url_for("home"))

    def _generate_nav(self):
        nav_items = [f'<a class="href="/">{ICON}SMX</a>']
        for page in self.pages:
            nav_items.append(f'<a href="/page/{page}">{page}</a>')
        nav_items.append(f'<a href="/admin">Admin</a>')
        try:
            if self.theme_toggle_enabled:
                nav_items.append(f'<a href="/toggle_theme">Theme</a>')
        except:
            pass
        return " | ".join(nav_items)

    def _render_chat_history(self):
        chat_html = f"<h2 style='text-align:center;'>{self.project_title}</h2>"
        messages = session.get("chat_history", [])
        if messages:
            for role, message in messages:
                # Add timestamp for card mode
                timestamp = ""
                if self.ui_mode == "card":
                    timestamp = f"""<span style="float: right; font-size: 0.8em; 
                        color: {self.theme['text_color']};">{time.strftime('%H:%M')}</span>"""
                
                chat_html += f"""
                <div class='chat-message {role.lower()}'>
                    <strong>{role.capitalize()}</strong>{timestamp}
                    <p>{message}</p>
                </div>
                """
        return chat_html

    def _render_widgets(self):
        if self.ui_mode == "default":
            widget_html = f"""
            <form method="POST" style="max-width:800px; margin:0 auto; display:block; align-items:center; justify-content:center; flex-wrap:wrap;margin-bottom:60px; padding:12px;border:1px solid black; background:light-gray;">
                <div style='margin-bottom:10px;'>
                    <input type="text" name="user_query" 
                        value="{session.get('user_query', '')}" 
                        placeholder="Enter your RAG query" 
                        style="width: calc(100% - 20px); box-sizing: border-box; padding:12px; font-size:1em; border:1px solid #ccc; border-radius:4px;">
                </div>
                <div style="text-align:center;">
                    <button type="submit" name="submit_query" value="clicked" 
                            style="padding:10px 20px; margin-right:10px; border:none; border-radius:20px; background:{self.theme['nav_background']}; color:{self.theme['nav_text']}; cursor:pointer;">
                        Send
                    </button>
                    <button type="submit" name="clear_chat" value="clicked" 
                            style="padding:10px 20px; border:none; border-radius:20px; background:{self.theme['nav_background']}; color:{self.theme['nav_text']}; cursor:pointer;">
                        Clear
                    </button>
                </div>
            </form>
            """

        else:  # bubble mode: all elements on one horizontal row.
            widget_html = f"""
            <form method="POST" style="max-width:800px; margin:0 auto; display:flex; align-items:center; justify-content:center; flex-wrap:wrap;margin-bottom:60px; padding:12px;border:1px solid red; background:{self.theme['nav_background']};">
                <div style="flex:1; min-width:200px; margin:10px; padding: 0 10px;"> 
                    <input type="text" name="user_query" 
                        value="{session.get('user_query')}" 
                        placeholder="Enter query" 
                        style="width: calc(100% - 20px); box-sizing: border-box; padding:12px; font-size:1em; border:1px solid #ccc; border-radius:4px;">
                </div>
                <button type="submit" name="submit_query" value="clicked" 
                        style="padding:10px 20px; margin-right:10px; border:none; border-radius:20px; background:{self.theme['nav_background']}; color:{self.theme['nav_text']}; cursor:pointer;">
                    Send
                </button>
                <button type="submit" name="clear_chat" value="clicked" 
                        style="padding:10px 20px; border:none; border-radius:20px; background:{self.theme['nav_background']}; color:{self.theme['nav_text']}; cursor:pointer;">
                    Clear
                </button>
            </form>
            """
        return widget_html
    
    def _render_sidebar(self):
        sidebar_html = "<h3>Sidebar Menu</h3>"
        # Render sidebar widgets if any.
        for key, widget in self.sidebar_widgets.items():
            if widget["type"] == "text_input":
                value = session.get(key, widget.get("placeholder", ""))
                sidebar_html += f"""
                <form method="POST" style="margin-bottom:10px;">
                  <label for="{key}" style="display:block; margin-bottom:5px;">{widget["label"]}</label>
                  <input type="text" id="{key}" name="{key}" value="{value}" style="width:100%; padding:8px; border:1px solid #ccc; border-radius:4px;">
                  <button type="submit" name="{key}" value="submitted" style="margin-top:5px; width:100%; padding:8px; border:none; border-radius:4px; background:{self.theme['nav_background']}; color:{self.theme['nav_text']};">Submit</button>
                </form>
                """
            elif widget["type"] == "button":
                sidebar_html += f"""
                <form method="POST" style="margin-bottom:10px;">
                  <button type="submit" name="{key}" value="clicked" style="width:100%; padding:8px; border:none; border-radius:4px; background:{self.theme['nav_background']}; color:{self.theme['nav_text']};">
                    {widget["label"]}
                  </button>
                </form>
                """
        return sidebar_html

    # Public API: Widget registration.
    def text_input(self, key, label, placeholder=""):
        if key not in self.widgets:
            self.widgets[key] = {"type": "text_input", "key": key, "label": label, "placeholder": placeholder}

    def button(self, key, label, callback=None):
        if key not in self.widgets:
            self.widgets[key] = {"type": "button", "key": key, "label": label, "callback": callback}

    def file_uploader(self, key, label, accept_multiple_files=False):
        if key not in self.widgets:
            self.widgets[key] = {"type": "file_upload", "key": key, "label": label, "accept_multiple": accept_multiple_files}

    def get_text_input_value(self, key, default=""):
        return session.get(key, default)

    def clear_text_input_value(self, key):
        session[key] = ""
        session.modified = True

    def get_file_upload_value(self, key):
        return session.get(key, None)

    # Chat history management.
    def get_chat_history(self):
        return session.get("chat_history", [])

    def set_chat_history(self, history):
        session["chat_history"] = history
        session.modified = True

    def clear_chat_history(self):
        session["chat_history"] = []
        session.modified = True

    def set_widget_position(self, position):
        if position not in ["top", "bottom"]:
            raise ValueError("Invalid position. Choose 'top' or 'bottom'.")
        self.widget_position = position

    def write(self, content):
        if "content_buffer" not in session:
            session["content_buffer"] = ""
        session["content_buffer"] += str(content)
        session.modified = True

    def run(self):
        url = f"http://{self.host}:{self.port}/"
        webbrowser.open(url)
        self.app.run(host=self.host, port=self.port, debug=False)
