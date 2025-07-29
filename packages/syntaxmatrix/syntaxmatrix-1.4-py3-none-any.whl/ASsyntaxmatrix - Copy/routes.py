import os, time, uuid, werkzeug, queue, html, pandas as pd
from PyPDF2.errors import EmptyFileError
from io import BytesIO
from PyPDF2 import PdfReader
from flask import render_template, render_template_string, request, Response, session, redirect, url_for, flash, jsonify, send_from_directory 
from markupsafe  import Markup
from .themes import DEFAULT_THEMES
from . import db
from .utils import * 
from syntaxmatrix.db import add_pdf_chunk
from .file_processor import *  
from syntaxmatrix.plottings import datatable_box
from .history_store import SQLHistoryStore, PersistentHistoryStore
from .kernel_manager import SyntaxMatrixKernelManager, execute_code_in_kernel
from syntaxmatrix.vector_db import *  # insert_embedding, delete_embeddings_for_file
from urllib.parse import quote 

from .auth import register_user, authenticate, login_required, admin_required, superadmin_required
from syntaxmatrix.vectorizer import embed_text


_stream_q = queue.Queue() 

def get_contrast_color(hex_color: str) -> str:
    """
    Returns a contrasting color (#000000 or #ffffff) based on the brightness of hex_color.
    """
    hex_color = hex_color.strip().lstrip('#')
    if len(hex_color) == 3:
        r = int(hex_color[0]*2, 16)
        g = int(hex_color[1]*2, 16)
        b = int(hex_color[2]*2, 16)
    elif len(hex_color) == 6:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    else:
        return '#000000'
    brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
    return '#ffffff' if brightness < 0.5 else '#000000'

def render_chat_history(smx):
    plottings_html = smx.get_plottings()
    messages = session.get("chat_history", [])
    chat_html = ""
    if not messages and not plottings_html:
        chat_html += f"""
        <div id="deepseek-header" style="text-align:center; margin-top:10px; margin-bottom:5px;">
          <h2>{smx.bot_icon}{smx.project_title}.</h2>
        </div>
        """
    elif plottings_html:
        {f'''
            <div id="system-output-container">       
                {plottings_html}
            </div>           
        ''' if plottings_html.strip() else ""}
            
    for role, message in messages:
        timestamp = ""
        if smx.ui_mode == "card":
            timestamp = f"""<span style="float: right; font-size: 0.8em; color: {smx.theme['text_color']};">{time.strftime('%H:%M')}</span>"""
        chat_icon = smx.user_icon if role.lower() == "user" else smx.bot_icon
        chat_html += f"""
        <div class='chat-message {role.lower()}'>
          <span>{chat_icon}{timestamp}</span>
          <p>{message}</p>
        </div>
        """
    return chat_html

def setup_routes(smx):
    # Prevent duplicate route registration.
    if "home" in smx.app.view_functions:
        return
    
    DATA_FOLDER = os.path.join(os.getcwd(), "uploads", "data")
    os.makedirs(DATA_FOLDER, exist_ok=True)

    MEDIA_FOLDER = os.path.join(os.getcwd(), "uploads", "media")
    if not os.path.exists(MEDIA_FOLDER):
      os.makedirs(MEDIA_FOLDER)

    def head_html():
        # Determine a contrasting mobile text color based on the sidebar background.
        mobile_text_color = smx.theme["nav_text"]
        if smx.theme.get("sidebar_background", "").lower() in ["#eeeeee", "#ffffff"]:
            mobile_text_color = smx.theme.get("text_color", "#333")
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
              background: {smx.theme["background"]};
              color: {smx.theme["text_color"]};
            }}
            /* Responsive typography using clamp */
            html {{
              font-size: clamp(11px, 1.5vw, 18px);
            }}
            /* Desktop Navbar */
            nav {{
              display: flex;
              justify-content: space-between;
              align-items: center;
              background: {smx.theme["nav_background"]};
              padding: 10px 20px;
              position: fixed;
              top: 0;
              left: 0;
              right: 0;
              z-index: 1000;
            }}
            .nav-left {{
              display: flex;
              align-items: center;
            }}
            .nav-left .logo {{
              font-size: clamp(1.3rem, 2vw, 1.5rem);
              font-weight: bold;
              color: {smx.theme["nav_text"]};
              margin-right: 20px;
            }}
            .nav-left .nav-links a {{
              font-size: clamp(1rem, 1.2vw, 1.2rem);
              color: {smx.theme["nav_text"]};
              text-decoration: none;
              margin-right: 15px;
            }}
            .nav-right a {{
              font-size: clamp(1rem, 1.2vw, 1.2rem);
              color: {smx.theme["nav_text"]};
              text-decoration: none;
            }}
            /* Hamburger button (hidden on desktop) */
            #hamburger-btn {{
              display: none;
              width: clamp(140px, 20vw, 240px);
              font-size: 2rem;
              background: none;
              border: none;
              color: {smx.theme["nav_text"]};
              cursor: pointer;
            }}
            /* Mobile nav menu */
            #mobile-nav {{
              position: fixed;
              top: 40px; 
              right: -260px; 
              width: 14vw;
              font-size: 1rem;
              height: calc(100% - 60px);
              background: {smx.theme["sidebar_background"]};
              box-shadow: -2px 0 5px rgba(0,0,0,0.3);
              transition: right 0.3s ease;
              padding: 20px 5px 10px; 10px;
              display: flex;
              flex-direction: column;
              gap: 10px;
              z-index: 900;
              color: {mobile_text_color};
            }}
            #mobile-nav a {{
              font-size: inherit;
              color: {mobile_text_color};
              text-decoration: none;
            }}
            #mobile-nav.active {{
              right: 0;
            }}
            #mobile-nav a:hover {{
              background-color: rgba(0, 0, 0, 0.05);
              transform: scale(1.2);
            }}
            /* Responsive adjustments for mobile */
            @media (max-width: 768px) {{
              .nav-left .nav-links, .nav-right {{
                display: none;
              }}
              #hamburger-btn {{
                display: block;
              }}
            }}
            /* Sidebar styles */
            #sidebar {{
              position: fixed;
              top: 40px;
              left: -240px;
              width: 14vw;
              height: calc(100% - 10px);
              background: {smx.theme["sidebar_background"]};
              overflow-y: auto;
              padding: 10px; 5px;
              font-size: 0.8rem;
              gap: 10px;
              box-shadow: 2px 0 5px rgba(0,0,0,0.3);
              transition: left 0.3s ease;
              z-index: 999;
              color: {get_contrast_color(smx.theme["sidebar_background"])};
            }}
            #sidebar a {{
              color: {get_contrast_color(smx.theme["sidebar_background"])};
              text-decoration: none;
            }}
            #sidebar.open {{
                left: 0;
            }}
            #sidebar-toggle-btn {{
              position: fixed;
              top: 52px;
              left: 0;
              width: 2rem;
              height: 2rem;
              padding: 1px;
              cursor: pointer;
              border: 1px solid {get_contrast_color(smx.theme["sidebar_background"])};
              border-radius: 8px;
              z-index: 1000;
              background: {smx.theme["nav_text"]};
              color: {smx.theme["nav_text"]};
              transition: background-color 0.2s ease, transform 0.2s ease;
            }}
            #sidebar-toggle-btn:hover {{
              background-color: rgba(0, 0, 0, 0.05);
              transform: scale(1.2);
            }}
            #chat-history {{
              width: 100%;
              max-width: 980px;
              margin: 50px auto 10px auto;
              padding: 10px 5px;
              background: {smx.theme["chat_background"]};
              border-radius: 20px;
              overflow-y: auto;
              min-height: 360px;
            }}
             #chat-history-default {{
              width: 100%;
              max-width: 950px;
              margin: 50px auto 10px auto;
              padding: 10px 5px;
              background: {smx.theme["chat_background"]};
              border-radius: 10px;
              box-shadow: 0 2px 4px rgba(0,0,0,0.5);
              overflow-y: auto;
              min-height: 350px;
            }}
            #nc:hover {{
                background-color:#d6dbdf;
                transform:scale(1.2);
                transition: all 0.3s ease;
            }}
            #widget-container {{
              max-width: 850px;
              margin: 0 auto 40px auto;
            }}
            { _chat_css() }
            .closeable-div {{
              position: relative;
              padding: 20px;
              border: 1px solid #ccc;
              max-width: 70%;
              background-color: #fff;
            }}
            .close-btn {{
              position: absolute;
              top: 5px;
              right: 5px;
              cursor: pointer;
              font-size: 16px;
              padding: 2px 6px;
              color: #000;
            }}
            .close-btn:hover {{
              color: #ff0000;
            }}
          </style>
          <style>
            @keyframes spin {{
              0% {{ transform: rotate(0deg); }}
              100% {{ transform: rotate(360deg); }}
            }}
          </style>
          <style>
            .dropdown:hover .dropdown-content {{
                display: block;
            }}
          </style>
          <style>
            :root {{
                --sidebar-w: 14vw;         /* set to your real sidebar width (e.g. 6vw) */
            }}

            /* ---------- Smooth chat-pane slide (0.6 s) ---------- */
            :root {{
                --sidebar-w: 6vw;
            }}

            /* Everything that lives inside the chat area gets the transition once */
            #chat-history,
            #chat-form,
            #widget-container {{
                transition: transform 0.5s ease;
            }}

            /* When the body bears .sidebar-open, slide the whole lot right */
            body.sidebar-open #chat-history,
            body.sidebar-open #chat-form,
            body.sidebar-open #widget-container {{
                transform: translateX(var(--sidebar-w));
            }}
            
            #widget-container,
            #smx-widgets {{         
                position: sticky;                                         
                bottom: 0;            
                z-index: 1000;        
                background: inherit; 
            }}
          </style>
          <!-- Add MathJax -->
          <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
          <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
          <title>{smx.favicon}-{smx.page}</title>
        </head>
        <body>
          <script>
          // Toggle mobile nav menu on hamburger click
            document.addEventListener("DOMContentLoaded", function() {{
            var hamburger = document.getElementById("hamburger-btn");
            var mobileNav = document.getElementById("mobile-nav");
            hamburger.addEventListener("click", function() {{
              mobileNav.classList.toggle("active");
            }});
          }});
          </script>
        """
    
    def footer_html():
        # Returns a simple footer styled with theme variables.
        return f"""
        <footer style="width:100%; padding:10px; background:{smx.theme['nav_background']}; color:{smx.theme['nav_text']}; text-align:center; margin-top:20px;">
          <p style="margin:0; font-size: clamp(0.8rem, 1vw, 1rem);">
            &copy; {time.strftime('%Y')} {smx.site_title}. All rights reserved.
          </p>
        </footer>
        """

    def _chat_css():
        if smx.ui_mode == "bubble":
            return f"""
            .chat-message {{
              position: relative;
              max-width: 70%;
              margin: 10px 0;
              padding: 12px 18px;
              border-radius: 20px;
              animation: fadeIn 0.9s forwards;
              clear: both;
              font-size: 0.9em;
            }}
            .chat-message.user {{
              background: pink;
              float: right;
              margin-right: 15px;
              border-bottom-left-radius: 2px;
            }}
            .chat-message.user::before {{
              content: '';
              position: absolute;
              left: -8px;
              top: 12px;
              width: 0;
              height: 0;
              border: 8px solid transparent;
              border-right-color: pink;
              border-right: 0;
            }}
            .chat-message.bot {{
              background: #ffffff;
              float: left;
              margin-left: 15px;
              border-bottom-left-radius: 2px;
              border: 1px solid {smx.theme['chat_border']};
            }}
            .chat-message.bot::after {{
              content: '';
              position: absolute;
              right: -8px;
              top: 12px;
              width: 0;
              height: 0;
              border: 8px solid transparent;
              border-left-color: #ffffff;
              border-right: 0;
            }}
            .chat-message p {{
              margin: 0;
              padding: 0;
              word-wrap: break-word;
            }}
            """
        elif smx.ui_mode == "default":
            return f"""
            .chat-message {{
              display: block;
              width: 90%;
              margin: 15px auto;
              padding: 15px 20px;
              border-radius: 10px;
              background: linear-gradient(135deg, #ffffff, #f0f8ff);
              box-shadow: 0 2px 5px rgba(0,0,0,0.1);
              animation: fadeIn 0.9s forwards;
            }}
            .chat-message.user {{
              border: 1px solid {smx.theme['chat_border']};
              text-align: left;
            }}
            .chat-message.bot {{
              border: 1px solid {smx.theme['chat_border']};
              text-align: right;
            }}
            .chat-message p {{
              margin: 0;
              word-wrap: break-word;
            }}
            """
        elif smx.ui_mode == "card":
            return f"""
            .chat-message {{
              display: block;
              margin: 20px auto;
              padding: 20px 24px;
              border-radius: 16px;
              background: linear-gradient(135deg, #fff, #f7f7f7);
              box-shadow: 0 4px 12px rgba(0,0,0,0.15);
              max-width: 80%;
              animation: fadeIn 0.9s forwards;
              position: relative;
            }}
            .chat-message.user {{
              margin-left: auto;
              border: 2px solid {smx.theme['nav_background']};
            }}
            .chat-message.bot {{
              margin-right: auto;
              border: 2px solid {smx.theme['chat_border']};
            }}
            .chat-message p {{
              margin: 0;
              font-size: em;
              line-height: 1.2;
            }}
            .chat-message strong {{
              display: block;
              margin-bottom: 8px;
              color: {smx.theme['nav_background']};
              font-size: 0.9em;
            }}
            """
        elif smx.ui_mode == "smx":
            return f"""
            .chat-message {{
              display: block;
              margin: 15px auto;
              padding: 16px 22px;
              border-radius: 12px;
              animation: fadeIn 0.9s forwards;
              max-width: 85%;
              background: #ffffff;
              border: 2px solid {smx.theme['nav_background']};
              position: relative;
            }}
            .chat-message.user {{
              background: #f9f9f9;
              border-color: {smx.theme['chat_border']};
              text-align: left;
            }}
            .chat-message.bot {{
              background: #e9f7ff;
              border-color: {smx.theme['nav_background']};
              text-align: right;
            }}
            .chat-message p {{
              margin: 0;
              word-wrap: break-word;
              font-size: 0.5em;
            }}
            """
        else:
            return f"""
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
              border: 1px solid {smx.theme["chat_border"]};
              text-align: left;
              max-width: 80%;
            }}
            """
        
    def _generate_nav():
        from .settings.string_navbar import string_navbar_items
        logo = f'<a href="/" style="color: inherit; text-decoration: none;">{smx.site_logo}</a>'
        nav_links = ""
        for page in smx.pages:
            nav_links += f'<a href="/page/{page}">{page}</a>'
        for st in string_navbar_items:
          nav_links += f'<a href="/{st.lower()}">{st}</a>'
        theme_link = ''
        if smx.theme_toggle_enabled:
            theme_link = '<a href="/toggle_theme">Theme</a>'
        
        # Authentication links (login/register or logout)
        if session.get("user_id"):
            # Logged-in user
            auth_links = (
                f'<span class="nav-auth">Logged in as {session.get("username")}</span> '
                f'<form action="{url_for("logout")}" method="post" style="display:inline;margin-left:0.5rem;">'
                  '<button type="submit" class="nav-link">Logout</button>'
                '</form>'
            )
        else:
            # Anonymous
            auth_links = (
                f'<a href="{url_for("login")}" class="nav-link">Login</a>'
                ' | '
                f'<a href="{url_for("register")}" class="nav-link">Register</a>'
            )

        desktop_nav = f"""
        <div class="nav-left">
          <span class="logo">{logo}</span>
          <div class="nav-links">
            {nav_links}
          </div>
        </div>
        <div class="nav-right">
          {theme_link}
        </div>
        <div class="nav-right">
          {auth_links}
        </div>
        """
        hamburger_btn = '<button id="hamburger-btn">&#9776;</button>'
        mobile_nav = f"""
        <div id="mobile-nav">
          {nav_links}
          {theme_link}
          {auth_links}
        </div>
        """
        return f"""
        <nav>
          {desktop_nav}
          {hamburger_btn}
        </nav>
        {mobile_nav}
        """
    
    def _render_widgets():
        """
        Renders the default system widget (the user_query text area with inner icons)
        and then any additional developer-defined widgets.
        Developer file upload triggered by the paper clip now supports multiple files.
        """
        form_html = """
        <form id="chat-form" onsubmit="submitChat(event)"
              style="width:100%; max-width:800px; margin:100px auto 20px auto; padding:0 10px; box-sizing:border-box;">
          <input type="hidden" id="action-field" name="action" value="submit_query">
        """

        horizontal_buttons_html = ""

        for key, widget in smx.widgets.items():
            """<span class="icon-default" style="cursor:pointer; transition:transform 0.2s ease;" title="Attach"
                          onclick="document.getElementById('user-file-upload').click();">
                          ➕ 📎
                    </span>"""
            # For the 'user_query' text input with injected icons and submit button.
            if widget["type"] == "text_input" and widget["key"] == "user_query":
                form_html += f"""
                <div style="position: relative; margin-bottom:15px; padding:10px 5px; width:100%; box-sizing:border-box;">
                  <textarea
                    id="user_query"
                    name="{key}"
                    rows="2"
                    placeholder="{widget.get('placeholder','')}"
                    style="
                      position: absolute;
                      bottom:0; left:0;
                      width:100%;
                      padding:12px 15px 50px 15px;
                      font-size:1em;
                      border:1px solid #ccc;
                      border-radius:24px;
                      box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
                      overflow:hidden; resize:none; box-sizing:border-box;
                    "
                    oninput="this.style.height='auto'; this.style.height=(this.scrollHeight)+'px'; checkInput(this)"
                    autofocus
                  >{session.get(key, '')}</textarea>

                  <!-- Inline icons -->
                  <div style="position:absolute; bottom:15px; left:15px; display:flex; gap:20px;">
                    <!-- “+” opens the hidden PDF‐upload input -->
                    <span class="icon-default"
                          title="Upload PDF files for this chat"
                          style="cursor:pointer; transition:transform 0.2s ease;"
                          onclick="document.getElementById('user_files').click()">
                      📜
                    </span>
                    <!--
                    <span class="icon-default"
                          title="Internet"
                          style="cursor:pointer; transition:transform 0.2s ease;">
                      🌐
                    </span>
                    <span class="icon-default"
                          title="Search"
                          style="cursor:pointer; transition:transform 0.2s ease;">
                      🔍
                    </span> 
                    -->
                  </div>

                  <!-- Hidden file‐upload input bound to smx.file_uploader('user_files',…) -->
                  <input
                    type="file"
                    id="user_files"
                    name="user_files"
                    multiple
                    style="display:none"
                    onchange="uploadUserFileAndProcess(this, 'user_files')"
                  />

                  <!-- Send button -->
                  <button
                    class="icon-default"
                    title="Submit query
                    type="submit"
                    id="submit-button"
                    name="submit_query"
                    value="clicked"
                    onclick="document.getElementById('action-field').value='submit_query'"
                    disabled
                    style="
                      text-align:center;
                      position:absolute;
                      bottom:15px; right:15px;
                      width:2rem; height:2rem;
                      border-radius:50%; border:none;
                      opacity:0.5;
                      background:{smx.theme['nav_background']};
                      color:{smx.theme['nav_text']};
                      cursor:pointer; 
                      font-size:1.2rem;
                      display:flex; 
                      align-items:center; justify-content:center;
                      transition:transform 0.2s ease;
                    "
                  >⇧</button>
                </div>
                """
            elif widget["type"] == "button" and widget["key"] == "submit_query":
                continue # Handled inline in the user_query textarea above.
            elif widget["type"] == "file_upload" and widget["key"] == "user_files":
                continue # Handled inline in the user_query textarea above.
            
            elif widget["type"] == "button":
                horizontal_buttons_html += f"""
                <div style="width:850px;text-align:center;">
                <button
                    class="icon-default"
                    type="submit"
                    name="{key}"
                    value="clicked"
                    onclick="document.getElementById('action-field').value='{key}'"
                    style="
                        with:2rem;
                        font-size:0.8rem;
                        padding:5px 10px;
                        border:none;
                        border-radius:30px;
                        background:{smx.theme['nav_background']};
                        color:{smx.theme['nav_text']};
                        cursor:pointer;
                        /*transition: background 0.3s;*/
                        transition:transform 0.2s ease;"
                    "
                    onmouseover="this.style.backgroundColor='#e0e0e0';"
                    onmouseout="this.style.backgroundColor='{smx.theme['nav_background']}';"
                >
                    {widget['label']}
                </button>
                </div>
                """
            elif widget["type"] == "text_input":
                form_html += f"""
                <div style="margin-bottom:15px;">
                  <label for="{key}" style="display:block; margin-bottom:5px;">{widget['label']}</label>
                  <input type="text" id="{key}" name="{key}" placeholder="{widget.get('placeholder','')}"
                        value="{session.get(key, '')}"
                        style="
                            width:calc(100% - 20px);
                            padding:12px; 
                            font-size:1em;
                            border:1px solid #ccc;
                            border-radius:8px;
                            box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
                            box-sizing:border-box;
                        "
                  >
                </div>
                """
            elif widget["type"] == "file_upload":
                uploaded = request.files.getlist(key)
                if uploaded:
                    sid = smx.get_session_id()
                    for f in uploaded:
                        raw = f.read()
                        reader = PdfReader(BytesIO(raw))
                        text = "".join(page.extract_text() or "" for page in reader.pages)
                        chunks = recursive_text_split(text)
                        smx.add_user_chunks(sid, chunks)
                    # invoke the one callback you registered
                    if widget.get("callback"):
                        widget["callback"]()

            elif widget["type"] == "dropdown":
                options_html = "".join([
                    f"<option value='{opt}'{' selected' if opt == widget['value'] else ''}>{opt}</option>"
                    for opt in widget["options"]
                ])
         
                dropdown_html = f"""
                <div style="margin:10px 0;">
                    <label for="{key}" style="font-weight:bold;">{widget['label']}</label>
                    <select name="{key}" id="{key}" onchange="widget_event_dropdown('{key}')"
                        style="padding:4px 16px; border-radius:5px; font-size:1.06em; min-width:180px; margin-left:4px;">
                        {options_html}
                    </select>
                </div>
                """
                form_html += dropdown_html

        if horizontal_buttons_html:
            form_html += f"""
            <div style="display:flex; justify-content:center; align-items:center; gap:10px; margin-bottom:15px;">
                {horizontal_buttons_html}
            </div>
            """
        form_html += "</form>"
        
        form_html += """
        <script>
          function checkInput(textarea) {
            var submitBtn = document.getElementById("submit-button");
            if (!submitBtn) return;
            if (textarea.value.trim() === "") {
              submitBtn.disabled = true;
              submitBtn.style.opacity = "0.5";
            } else {
              submitBtn.disabled = false;
              submitBtn.style.opacity = "1";
            }
          }
          // Animate icons on hover
          var icons = document.getElementsByClassName('icon-default');
          for (var i = 0; i < icons.length; i++) {
            icons[i].addEventListener('mouseover', function() {
              this.style.transform = "scale(1.2)";
            });
            icons[i].addEventListener('mouseout', function() {
              this.style.transform = "scale(1)";
            });
          }
          
          // AJAX function to upload multiple user files
          function uploadUserFile(inputElement) {
            if (inputElement.files.length > 0) {
              var formData = new FormData();
              for (var i = 0; i < inputElement.files.length; i++) {
                  formData.append("user_files", inputElement.files[i]);
              }
              fetch('/upload_user_file', {
                  method: "POST",
                  body: formData
              })
              .then(response => response.json())
              .then(data => {
                  if(data.error) {
                      alert("Error: " + data.error);
                  } else {
                      alert("Uploaded files: " + data.uploaded_files.join(", "));
                      // Optionally, store or display file paths returned by the server.
                  }
              })
              .catch(err => {
                  console.error(err);
                  alert("Upload failed.");
              });
            }
          }
        </script>
        <script>
          // When picking files, the action is stashed to the widget key
          // then fire submitChat with submitter.id = that key.
          function uploadUserFileAndProcess(inputEl, actionKey) {
            if (!inputEl.files.length) return;
            // set action-field so process_chat knows which widget to invoke
            document.getElementById('action-field').value = actionKey;
            // pass submitter.id = actionKey so we don't override it below
            submitChat({ preventDefault(){}, submitter:{ id: actionKey } });
          }

          // Override only when clicking the “Send” button.
          async function submitChat(e) {
            e.preventDefault();
            document.getElementById('loading-spinner').style.display = 'block';

            // Only reset to 'submit_query' when it really came from the send‑button
            if (e.submitter && e.submitter.id === 'submit-button') {
              document.getElementById('action-field').value = 'submit_query';
            }

            const form = document.getElementById('chat-form');
            const formData = new FormData(form);
            const action = document.getElementById('action-field').value;
            if (!formData.has(action)) {
              formData.append(action, 'clicked');
            }

            try {
              const response = await fetch('/process_chat', {
                method: 'POST',
                body: formData
              });
              const data = await response.json();
              document.getElementById("chat-history").innerHTML = data.chat_html;

              let outputContainer = document.getElementById('system-output-container');
              if (outputContainer) {
                  if (data.system_output_html.trim() === "") {
                      outputContainer.remove();  // Remove if now empty
                  } else {
                      outputContainer.innerHTML = data.system_output_html;
                  }
              } else if (data.system_output_html.trim() !== "") {
                  outputContainer = document.createElement('div');
                  outputContainer.id = 'system-output-container';
                  outputContainer.style = "max-width:850px; margin:20px auto; padding:10px; background:#fff; border:1px solid #ccc; border-radius:8px; margin-top:150px;";
                  outputContainer.innerHTML = data.system_output_html;

                  const scripts = outputContainer.querySelectorAll('script');
                  scripts.forEach(oldScript => {
                    const newScript = document.createElement('script');
                    if (oldScript.src) {
                      newScript.src = oldScript.src;
                    } else {
                      newScript.textContent = oldScript.textContent;
                    }
                    oldScript.parentNode.replaceChild(newScript, oldScript);
                  });

                  document.body.prepend(outputContainer);
              }

              // Clear the user query textarea only on a real “Send”
              if (document.getElementById('action-field').value === 'submit_query') {
                const ta = document.querySelector('textarea[name="user_query"]');
                ta.value = "";
                checkInput(ta);
              }

              const chatHistory = document.getElementById("chat-history");
              chatHistory.scrollTop = chatHistory.scrollHeight;
              window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
            } catch (err) {
              console.error("Error processing chat:", err);
            } finally {
              document.getElementById('loading-spinner').style.display = 'none';
            }
          }

          // wire up Enter→Send
          document.addEventListener("DOMContentLoaded", () => {
            const ta = document.querySelector('textarea[name="user_query"]');
            if (ta) {
              ta.addEventListener("keydown", evt => {
                if (evt.key === "Enter" && !evt.shiftKey) {
                  document.getElementById('action-field').value = 'submit_query';
                  submitChat(evt);
                  evt.preventDefault();
                }
              });
            }
          });
        </script>
        <script>
          function widget_event_dropdown(key) {
              var value = document.getElementById(key).value;
              fetch('/widget_event', {
                  method: 'POST',
                  headers: {'Content-Type': 'application/json'},
                  body: JSON.stringify({widget_key: key, widget_value: value})
              })
              .then(response => response.json())
              .then(data => {
                  let outputContainer = document.getElementById('system-output-container');
                  if (outputContainer) {
                      if (data.system_output_html.trim() === "") {
                          outputContainer.remove();
                      } else {
                          outputContainer.innerHTML = data.system_output_html;
                      }
                  } else if (data.system_output_html.trim() !== "") {
                      outputContainer = document.createElement('div');
                      outputContainer.id = 'system-output-container';
                      outputContainer.innerHTML = data.system_output_html;

                      const scripts = outputContainer.querySelectorAll('script');
                      scripts.forEach(oldScript => {
                        const newScript = document.createElement('script');
                        if (oldScript.src) {
                          newScript.src = oldScript.src;
                        } else {
                          newScript.textContent = oldScript.textContent;
                        }
                        oldScript.parentNode.replaceChild(newScript, oldScript);
                      });

                      document.body.prepend(outputContainer);
                  }
                  // Update widgets if changed
                  if (data.widgets_html) {
                      document.getElementById('widget-container').innerHTML = data.widgets_html;
                  }
              });
          }
          </script>
        """      
        return form_html
      
    def _render_session_sidebar():
        current = session.get("current_session", {"title": "Current"})
        current_display = current.get("title", "Current")
        past_sessions = session.get("past_sessions", [])
        sidebar_html = '<div id="sidebar">'
        sidebar_html += (
            '<div style="margin:8px auto; text-align:right;">'
            '<button id="nc" type="button" onclick="createNewChat()" title="New Chat" style="width:4rem; height:2rem; font-size:1rem; border:none; border-radius:4px; cursor:pointer;">..𓂃🖊</button>'
            '</div>'
        )
        if current_display == "Current":
            sidebar_html += f'''
                <div class="session-item active" style="margin-bottom: 15px; color: {smx.theme["nav_text"]};">
                  <span class="session-title" style="font-size:0.8rem;cursor:default;">{current_display}</span>
                </div>
            '''
        if past_sessions:
            sidebar_html += f'''
                <hr style="margin:10px 0;">
                <div style="color: {smx.theme["nav_background"]};font-size:0.7rem;"><strong>Chats</strong></div>
                <ul style="list-style-type:none; padding:0; margin:0;">
            '''
            for s in past_sessions:
      
                safe_title_raw  = s["title"]
                # Tooltip – needs HTML-escaping
                safe_title_html = html.escape(safe_title_raw)

                # Data for JS call – encode once, decode on click
                encoded_title   = quote(safe_title_raw, safe='')

                display_title = (
                    safe_title_raw if len(safe_title_raw) <= 15 else safe_title_raw[:15] + "…"
                )
                active_class  = (
                    " active" if s["id"] == current.get("id") and current_display != "Current"
                    else ""
                )
                sidebar_html += f"""
                <li class="session-item{active_class}" data-session-id="{s['id']}" 
                    style="margin-top:4px; padding:0;">
                    <span class="session-title" title="{safe_title_html}"
                          style="float:left;"
                          onclick="setSession('{s['id']}', this)">{display_title} 
                    </span>
                    <span class="icon-default session-ellipsis" title="Options"
                          style="margin-left:auto;font-size:18px;cursor:pointer;transition:transform 0.2s ease; border:1px solid purple;border-radius:4px;"
                          onclick="event.stopPropagation(); toggleSessionMenu('{s['id']}')">
                          &vellip;&vellip;
                    </span>
                    <div class="session-menu" id="menu-{s['id']}">
                        <div class="menu-item" title="Rename chat"
                            onclick="openRenameModal('{s['id']}', decodeURIComponent('{encoded_title}'))">
                            ✏️
                        </div>
                        <div class="menu-item" title="Delete chat"
                            onclick="openDeleteModal('{s['id']}')">
                            🗑️
                        </div>
                    </div>
                </li>
                """
            sidebar_html += '</ul>'
        sidebar_html += '</div>'
        misc_sidebar_css = f"""
        <style>
          .session-item {{
              position: relative;
              padding: 5px 10px;
              border-radius: 4px;
              cursor: pointer;
              display: flex;
              justify-content: space-between;
              align-items: center;
              transition: background 0.3s;
          }}
          .session-item:hover {{
              background-color: {smx.theme.get('sidebar_hover', '#cccccc')};
          }}
          .session-item.active {{
              background-color: {smx.theme.get('sidebar_active', '#aaaaaa')};
          }}
          .session-title {{
              flex-grow: 1;
          }}
          .session-ellipsis {{
              display: none;
              margin-left: 5px;
          }}
          .session-item:hover .session-ellipsis {{
              display: inline-block;
          }}
          .session-menu {{
              display: none;
              position: absolute;
              right: 0;
              top: 50%;
              transform: translateY(-50%);
              background: #fff;
              border: 1px solid #ccc;
              min-width: 100px;
              z-index: 10;
              padding: 5px;
          }}
          .menu-item {{
              padding: 3px 5px;
              cursor: pointer;
          }}
          .menu-item:hover {{
              background: #eee;
          }}
        </style>
        """
        return sidebar_html + misc_sidebar_css

    # def clear_chat_history():
    #     session["chat_history"] = []
    #     session.modified = True
    # # smx.clear_chat_history = clear_chat_history
    

    # ──────────────────────────────────────────────────────────────────────────────────────── 
    # HOME ROUTES
    # ──────────────────────────────────────────────────────────────────────────────────────── 
    # ── HOME VIEW DETAILS -----------------------------
    @smx.app.route("/", methods=["GET", "POST"])
    def home():
        smx.page = ""
        if session.get("app_token") != smx.app_token or session.pop("needs_end_chat", False):      
            current_history = session.get("chat_history", [])
            current_session = session.get("current_session", {"id": str(uuid.uuid4()), "title": "Current", "history": []})
            past_sessions = session.get("past_sessions", [])
            
            if current_history:
                exists = any(s["id"] == current_session["id"] for s in past_sessions)
                if not exists:
                    generated_title = smx.generate_contextual_title(current_history)
                    current_session["title"] = generated_title
                    current_session["history"] = current_history.copy()
                    past_sessions.insert(0, current_session)
                else:
                    for s in past_sessions:
                        if s["id"] == current_session["id"]:
                            s["history"] = current_history.copy()
                            break
                        
                session["past_sessions"] = past_sessions
            session["current_session"] = {"id": str(uuid.uuid4()), "title": "Current", "history": []}
            session["chat_history"] = []
            session["app_token"] = smx.app_token
        
        if request.method == "POST":
            action = request.form.get("action")

            if action == "clear_chat":
                session["chat_history"] = []

            elif action == "new_session":
                current_history = session.get("chat_history", [])
                current_session = session.get("current_session", {"id": str(uuid.uuid4()), "title": "Current", "history": []})
                past_sessions = session.get("past_sessions", [])
                exists = any(s["id"] == current_session["id"] for s in past_sessions)
                if current_history:
                    if not exists:
                        generated_title = smx.generate_contextual_title(current_history)
                        current_session["title"] = generated_title
                        current_session["history"] = current_history.copy()
                        past_sessions.insert(0, current_session)
                    else:
                        for s in past_sessions:
                            if s["id"] == current_session["id"]:
                                s["history"] = current_history.copy()
                                break
                    session["past_sessions"] = past_sessions
                    # — Persist the just‐ended “Current” chat into chats.db for logged-in users —
                    if session.get("user_id"):
                        user_id = session["user_id"]
                        cid     = current_session["id"]
                        title   = current_session["title"]
                        SQLHistoryStore.save(user_id, cid, current_history, title)

                session["current_session"] = {"id": str(uuid.uuid4()), "title": "Current", "history": []}
                session["chat_history"] = []
            session["app_token"] = smx.app_token
        nav_html = _generate_nav()
        chat_html = render_chat_history(smx)
        widget_html = _render_widgets()
        sidebar_html = _render_session_sidebar()
        
        new_chat_js = """
        <script>
          function createNewChat() {
            var form = document.createElement("form");
            form.method = "POST";
            form.action = "/";
            var input = document.createElement("input");
            input.type = "hidden";
            input.name = "action";
            input.value = "new_session";
            form.appendChild(input);
            document.body.appendChild(form);
            form.submit();
          }
        </script>
        """
        scroll_and_toggle_js = """
        <script>
          async function submitChat(e) {
            e.preventDefault();
            e.preventDefault();
            document.getElementById('loading-spinner').style.display = 'block';
            // If the event came from a button click and the clicked button is the default submit button,
            // or if it came from a keydown event (where event.submitter is undefined), reset the action field.
            if ((e.submitter && e.submitter.id === "submit-button") || !e.submitter) {
              document.getElementById("action-field").value = "submit_query";
            }

            const form = document.getElementById('chat-form');
            const formData = new FormData(form);
            const action = document.getElementById('action-field').value;
            if (!formData.has(action)) {
              formData.append(action, 'clicked');
            }
            try {
              const response = await fetch('/process_chat', {
                method: 'POST',
                body: formData
              });
              const data = await response.json();
              document.getElementById("chat-history").innerHTML = data.chat_html;
              let outputContainer = document.getElementById('system-output-container');
              if (outputContainer) {
                outputContainer.innerHTML = data.system_output_html;
              } else if(data.system_output_html.trim() !== "") {
                outputContainer = document.createElement('div');
                outputContainer.id = 'system-output-container';
                outputContainer.style = "max-width:850px; margin:20px auto; padding:10px; background:#fff; border:1px solid #ccc; border-radius:8px; margin-top:150px;";
                outputContainer.innerHTML = data.system_output_html;

                const scripts = outputContainer.querySelectorAll('script');
                scripts.forEach(oldScript => {
                  const newScript = document.createElement('script');
                  if (oldScript.src) {
                    newScript.src = oldScript.src;
                  } else {
                    newScript.textContent = oldScript.textContent;
                  }
                  oldScript.parentNode.replaceChild(newScript, oldScript);
                });

                document.body.prepend(outputContainer);
              }
              if (action === 'submit_query') {
                const userQuery = document.querySelector('textarea[name="user_query"]');
                userQuery.value = "";
                checkInput(userQuery);
              }
              const chatHistory = document.getElementById("chat-history");
              chatHistory.scrollTop = chatHistory.scrollHeight;
              window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
            } catch (error) {
              console.error("Error processing chat:", error);
            } finally {
              document.getElementById('loading-spinner').style.display = 'none';
            }
          }

          document.addEventListener("DOMContentLoaded", function(){
            const textArea = document.querySelector('textarea[name="user_query"]');
            if(textArea) {
              textArea.addEventListener("keydown", function(event) {
                // When Enter is pressed without the Shift key, set the action-field to 'submit_query'
                if(event.key === "Enter" && !event.shiftKey){
                  event.preventDefault();
                  document.getElementById("action-field").value = "submit_query";
                  submitChat(event);
                }
              });
            }
          });
        </script>
        """
        close_eda_btn_js = """
        <script>
          function closeEdaPanel() {
              fetch('/clear_eda_panel', { method: 'POST' })
                  .then(response => response.json())
                  .then(data => {
                      // Remove or empty the EDA panel from the DOM
                      const eda = document.getElementById('system-output-container');
                      if (eda) eda.remove();  // or: eda.innerHTML = '';
                  });
          }
        </script>
        """ 

        stream_js = """
          <script>
              evt.onmessage = e => {
              if (e.data === "[END]") {
                // remove the temporary streaming bubble BEFORE
                //     /process_chat rewrites #chat-history
                if (bubble) {
                  bubble.remove();
                  bubble = null;
                }
                return;                       // done with this stream
              }

              // First token of a new reply → create the bubble
              if (!bubble) {
                bubble = document.createElement("div");
                bubble.className = "chat-message bot";
                document.getElementById("chat-history").appendChild(bubble);
              }

              // Append the incoming token text
              bubble.innerHTML += e.data.replace(/\n/g, "<br>");
              bubble.scrollIntoView({ behavior: "smooth" });
            };
          </script>
        """

        page_html = f"""<!DOCTYPE html>
        <html>
        <head>
          {head_html()}
        </head>
        <body>
          {nav_html}
          <button
            id="sidebar-toggle-btn"
            data-icon-open="{url_for('static', filename='icons/svg_497526.svg')}"
            data-icon-close="{url_for('static', filename='icons/svg_497528.svg')}"
          >
            <img
              id="sidebar-toggle-icon"
              src="{url_for('static', filename='icons/svg_497526.svg')}"
              alt="Toggle Sidebar"
              style="width:1rem; height:1.5rem;"
            />
          </button>

          <div id="sidebar-container">{sidebar_html}</div>         
          <div id="loading-spinner" style="display:none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 1000;">
              <div class="spinner" style="border: 8px solid #f3f3f3; border-top: 8px solid {smx.theme['nav_background']}; border-radius: 50%; width: 60px; height: 60px; animation: spin 1s linear infinite;"></div>
          </div>
          <div id="chat-history">{chat_html}</div>
         
          <div id="widget-container">{widget_html}</div>

          {scroll_and_toggle_js}
          {close_eda_btn_js}
          {new_chat_js}
          {stream_js}
+         <script src="{ url_for('static', filename='js/sidebar.js') }"></script>
        </body>
        </html>"""
        return render_template_string(page_html)
    
    @smx.app.route("/system_output")
    def system_output():
        return session.get("system_output", "")
    
    @smx.app.route("/toggle_theme", methods=["GET"])
    def toggle_theme():
        current = session.get("theme", "light")
        themes_list = list(DEFAULT_THEMES.keys())
        try:
            current_index = themes_list.index(current)
        except ValueError:
            current_index = 0
        new_index = (current_index + 1) % len(themes_list)
        new_theme = themes_list[new_index]
        session["theme"] = new_theme
        smx.set_theme(new_theme, DEFAULT_THEMES[new_theme])
        return redirect(url_for("home"))
    
    @smx.app.route("/rename_session", methods=["POST"])
    def rename_session():
        sess_id = request.form.get("session_id")
        new_title = request.form.get("new_title","").strip()
        if not sess_id or not new_title:
            return "Invalid request", 400

        if session.get("current_session",{}).get("id") == sess_id:
            session["current_session"]["title"] = new_title

        past = session.get("past_sessions", [])
        for s in past:
            if s["id"] == sess_id:
                s["title"] = new_title
        session["past_sessions"] = past

         # — Persist the new title for logged-in users —
        if session.get("user_id"):
            from .history_store import SQLHistoryStore
            # load the current history so we don’t overwrite it
            history = SQLHistoryStore.load(session["user_id"], sess_id)
            SQLHistoryStore.save(
                session["user_id"],
                sess_id,
                history,
                new_title
            )

        session.modified = True

        return jsonify({ "new_title": new_title }), 200
    
    @smx.app.route("/delete_session", methods=["POST"])
    def delete_session():
        sess_id = request.form.get("session_id")
        if not sess_id:
            return "Invalid request", 400

        past = session.get("past_sessions", [])
        past = [s for s in past if s["id"] != sess_id]
        session["past_sessions"] = past

        # — Remove it from persistent storage as well —
        from .history_store import PersistentHistoryStore as p_Store
        # use the same session ID that smx.get_session_id() gives when saving/loading
        sid = smx.get_session_id()
        p_Store.delete(sid, sess_id)

        # if the current session is deleted, spin up a fresh “Current”:
        if session.get("current_session",{}).get("id") == sess_id:
            session["current_session"] = { "id": str(uuid.uuid4()), "title": "Current", "history": [] }
            session["chat_history"]   = []

        session.modified = True

        # send back just the new chat-history HTML
        chat_html = render_chat_history(smx)
        return jsonify({ "chat_html": chat_html }), 200

    @smx.app.route("/process_chat", methods=["POST"])
    def process_chat():
        # 1) Handle any registered widgets, including file_uploads:
        for key, widget in smx.widgets.items():
            if widget["type"] == "text_input":
                session[key] = request.form.get(key, widget.get("placeholder", ""))

            elif widget["type"] == "file_upload":
                # if the user attached files under this widget…
                uploaded = request.files.getlist(key)
                if not uploaded:
                    continue

                sid = smx.get_session_id()
                total_chunks = 0

                for f in uploaded:
                    try:
                        raw = f.read()
                        # skip zero‑length reads
                        if not raw:
                            continue

                        reader = PdfReader(BytesIO(raw))
                        text = "".join(page.extract_text() or "" for page in reader.pages)
                        chunks = recursive_text_split(text)
                        smx.add_user_chunks(sid, chunks)
                        total_chunks += len(chunks)

                    except EmptyFileError:
                        # this was an empty file, skip it
                        continue
                    except Exception as e:
                        # log it but don’t interrupt /process_chat
                        smx.warning(f"Could not process uploaded PDF '{getattr(f, 'filename', '')}': {e}")
                
                # notify the user
                if request.form.get("action") == key:
                    smx.success(f"✅ Uploaded {len(uploaded)} file(s) and stored {total_chunks} chunks.")

            elif widget["type"] == "button":
                if key in request.form and widget.get("callback"):
                    widget["callback"]()

        action = request.form.get("action")
        if action == "clear_chat":
            session["chat_history"] = []
            # also drop any file‑chunks
            sid = smx.get_session_id()
            smx.clear_user_chunks(sid)
            
        # Update the current session's history with any modifications.
        # 2) Persist session → past_sessions
        if "current_session" in session:
            session["current_session"]["history"] = session.get("chat_history", [])
            past_sessions = session.get("past_sessions", [])
            for s in past_sessions:
                if s["id"] == session["current_session"]["id"]:
                    s["history"] = session["chat_history"]
            session["past_sessions"] = past_sessions
        session.modified = True

        # 3) Now build the combined chat + system_output
        system_output_buffer_html = smx.system_output_buffer.strip()
        chat_html = render_chat_history(smx)
        plottings_html = smx.get_plottings()

        return {"chat_html": chat_html, "system_output_buffer_html": system_output_buffer_html, "system_output_html": plottings_html}
    
    @smx.app.route("/load_session", methods=["POST"])
    def load_session():
        # --- Execute "Ending Chat" for the current session ---
        current_history = session.get("chat_history", [])
        current_session = session.get(
            "current_session",
            {"id": str(uuid.uuid4()), "title": "Current", "history": []}
        )
        past_sessions = session.get("past_sessions", [])
        exists = any(s["id"] == current_session["id"] for s in past_sessions)

        if current_history:
            if not exists:
                generated_title = smx.generate_contextual_title(current_history)
                current_session["title"] = generated_title
                current_session["history"] = current_history.copy()
                past_sessions.insert(0, current_session)
            else:
                for s in past_sessions:
                    if s["id"] == current_session["id"]:
                        s["history"] = current_history.copy()
                        break
                    
            session["past_sessions"] = past_sessions
            # — Persist the just-ended “Current” chat into chats.db for logged-in users —
            if session.get("user_id"):
                SQLHistoryStore.save(
                    session["user_id"],
                    current_session["id"],
                    current_history,
                    current_session["title"]
                )

        # --- Load the target session (the clicked chat) ---
        sess_id = request.form.get("session_id")
        target = next((s for s in past_sessions if s["id"] == sess_id), None)
        if target:
            session["current_session"] = target
            session["chat_history"]   = target["history"]
            
            session.modified = True

        # Return both refreshed panes
        chat_html    = render_chat_history(smx)
        sidebar_html = _render_session_sidebar()
        return jsonify({
            "chat_html":    chat_html,
            "sidebar_html": sidebar_html
        })
    
    @smx.app.route("/upload_user_file", methods=["POST"])
    def upload_user_file():
        import uuid
        from flask import jsonify
        # Define the upload folder for user files.
        upload_folder = os.path.join(os.getcwd(), "uploads", "user")
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            
        # Retrieve list of files uploaded.
        uploaded_files = request.files.getlist("user_files")
        if not uploaded_files:
            return jsonify({"error": "No files provided"}), 400
        
        saved_files = []
        for file in uploaded_files:
            if file.filename == "":
                continue  # Skip files with empty filenames.
            # Create a unique filename.
            unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
            filepath = os.path.join(upload_folder, unique_filename)
            try:
                file.save(filepath)
                saved_files.append(unique_filename)
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        if not saved_files:
            return jsonify({"error": "No valid files uploaded"}), 400
        
        return jsonify({"message": "Your files have been uploaded successfully", "uploaded_files": saved_files})

    @smx.app.route("/stream")
    def stream():
        def event_stream():
            while True:
                data = _stream_q.get()        
                yield f"data:{data}\n\n"
        return Response(event_stream(),
                        mimetype="text/event-stream")
    
    @smx.app.route("/clear_eda_panel", methods=["POST"])
    def clear_eda_panel_api():
        smx.set_plottings("")
        return {"success": True}

    @smx.app.route("/widget_event", methods=["POST"])
    def widget_event():
        data = request.get_json()
        key = data.get("widget_key")
        value = data.get("widget_value")
        if key in smx.widgets:
            smx.widgets[key]["value"] = value
            callback = smx.widgets[key].get("callback")
            if callback:
                callback()  # This should call your plotting function!
        # Re-render
        widgets_html = _render_widgets()
        plottings_html = smx.get_plottings()
        return {"system_output_html": plottings_html, "widgets_html": widgets_html}
    
    # Override the generic page renderer to inject a gallery on the "service" page
    @smx.app.route('/page/<page_name>')
    def view_page(page_name):
        smx.page = '-' + page_name.lower()
        nav_html = _generate_nav()
        content = smx.pages.get(page_name, f"No content found for page '{page_name}'.")
        
        # only on the service page, build a gallery
        media_html = ''
        if page_name.lower() == 'service':
            media_folder = os.path.join(os.getcwd(), 'uploads', 'media')
            if os.path.isdir(media_folder):
                files = sorted(os.listdir(media_folder))
                # wrap each file in an <img> tag (you can special‑case videos if you like)
                thumbs = []
                for fn in files:
                    src = url_for('serve_media', filename=fn)
                    thumbs.append(f'<img src="{src}" alt="{fn}" style="max-width:150px; margin:5px;"/>')
                if thumbs:
                    media_html = f'''
                      <section id="media-gallery" style="margin-top:20px;">
                        <h3>Media Gallery</h3>
                        <div style="display:flex; flex-wrap:wrap; gap:10px;">
                          {''.join(thumbs)}
                        </div>
                      </section>
                    '''

        page_html = f"""
        <!DOCTYPE html>
        <html>
        <head>{head_html()}</head>
        <body>
          {nav_html}
          <div style="margin-top:20px; width:100%; padding:10px; box-sizing:border-box;">
            <div style="text-align:center; margin-top:20px; border:1px solid #ccc; padding:10px; 
                        border-radius:8px; background-color:#f9f9f9;">
              <h2>{page_name}</h2>
              <div>{content}</div>
              {media_html}
              <a class="button" href="/">Return to Home</a>
            </div>
          </div>
          {footer_html()}
        </body>
        </html>
        """
        return render_template_string(page_html)
    
    @smx.app.route("/admin", methods=["GET", "POST"])
    @login_required
    def admin_panel():
        
        # ── LLM provider → models mapping (v1.4 widget) ───────────────
        # LLM_MODEL_MAP = {
        #     "openai":[
        #         "gpt-4o-mini", 
        #         "gpt-4o-mini-search-preview", 
        #         "gpt-4o-mini-audio-preview", 
        #         "gpt-4o", 
        #         "gpt-4.1-mini"
        #       ],
        #     "google":[
        #         "gemma-3-27b-it", 
        #         "gemma-3n-e4b-it",
        #         "gemini-1.5-flash", 
        #         "gemini-1.5-pro",
        #         "gemini-2.0-flash", 
        #         "gemini-2.5-pro"
        #       ],
        #     "anthropic":[
        #         "claude-3-haiku", 
        #         "claude-3-sonnet"
        #       ],
        #     "meta":[
        #         "llama-3-8b", 
        #         "llama-3-70b"
        #       ],
        #     "xai":[
        #         "grok-1.5"
        #       ],
        #     "deepseek":[
        #         "deepseek-chat", 
        #         "deepseek-math"
        #       ]
        # }
        
        if request.method == "POST":
            action = request.form.get("action")
            if action == "upload_files":
                files = request.files.getlist("upload_files")
                upload_folder = os.path.join(os.getcwd(), "uploads", "sys")
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                # 1) save ONLY the freshly-added PDFs
                new_pdf_paths = []
                for f in files:
                    if f and f.filename.lower().endswith(".pdf"):
                        dest = os.path.join(upload_folder, f.filename)
                        f.save(dest)
                        new_pdf_paths.append(dest)

                # 2) chunk ONLY those new PDFs and append to the DB
                processed_files = {}
                for path in new_pdf_paths:
                    file_name = os.path.basename(path)
                    try:
                        text     = extract_pdf_text(path)
                        cleaned  = " ".join(text.split())
                        chunks   = recursive_text_split(cleaned)
                        for idx, chunk in enumerate(chunks):
                            # 1) store the chunk
                            add_pdf_chunk(file_name, idx, chunk)
                            # 2) embed it
                            emb = embed_text(chunk)
                            # 3) persist into embeddings table
                            insert_embedding(
                                vector=emb,
                                metadata={"file_name": file_name, "chunk_index": idx},
                                chunk_text=chunk
                            )
                        processed_files[file_name] = chunks
                    except Exception as e:
                        smx.warning(f"⚠️ Failed to process {file_name}: {e}")

                # 3) merge with the in-memory cache of system chunks
                smx.admin_pdf_chunks.update(processed_files)

                total_chunks = sum(len(c) for c in processed_files.values())
                session["upload_msg"] = (
                    f"Uploaded {len(new_pdf_paths)} new PDF(s); "
                    f"Generated {total_chunks} chunk(s)."
                )

            elif action == "delete_sys_file":
              file_name = request.form.get("sys_file", "").strip()
              if file_name:
                  # where our system PDFs live
                  sys_dir = os.path.join(os.getcwd(), "uploads", "sys")
                  remove_admin_pdf_file(sys_dir, file_name)
                  smx.admin_pdf_chunks.pop(file_name, None)
                  session["upload_msg"] = f"Deleted {file_name} and its chunks."

            elif action == "add_page":
                page_name = request.form.get("page_name", "").strip()
                page_content = request.form.get("page_content", "").strip()
                if page_name and page_name not in smx.pages:
                    db.add_page(page_name, page_content)

            elif action == "delete_page":
                del_page = request.form.get("delete_page", "").strip()
                if del_page in smx.pages:
                    db.delete_page(del_page)

            elif action == "save_llm":
                save = False
                k = request.form.get("api_key","").strip()
                if k and k != "********":                    
                    save = smx.save_llm_settings(
                    request.form["provider"],
                    request.form["model"],
                    k.rstrip("*")   # ‘*****’ means keep
                )
                if save: 
                    flash(f"LLM settings saved ✓: <br>{request.form['model']}")
                else: 
                    flash(f"ERROR: settings not saved.")
            
            elif action == "delete_llm":
                deleted = smx.delete_llm_key()
                flash("LLM API key removed ") if deleted else flash("Smotheing is wrong!")
                return redirect(url_for("admin_panel"))
        
        smx.pages = db.get_pages()
        upload_msg = session.pop("upload_msg", "")
        alert_script = f"<script>alert('{upload_msg}');</script>" if upload_msg else ""
        # Generate individual page cards for the Manage Pages section.
        page_cards = ""
        for p in smx.pages:
            page_cards += f"""
                <div style="border: 1px solid #ddd; border-radius: 4px; padding:10px; margin-bottom:10px;">
                    <strong>{p}</strong>
                    <div style="text-align: right; margin-top: 10px;">
                        <a class="button" href="/admin/edit/{p}">Edit</a>
                        <form method="post" style="display:inline;">
                            <input type="hidden" name="delete_page" value="{p}">
                            <button type="submit" name="action" value="delete_page" style="margin-left:5px;">X</button>
                        </form>
                    </div>
                </div>
            """
        # scan for system PDFs
        sys_dir = os.path.join(os.getcwd(), "uploads", "sys")
        sys_files = []
        if os.path.isdir(sys_dir):
            sys_files = [f for f in os.listdir(sys_dir) if f.lower().endswith(".pdf")]

        # build HTML for the Manage System PDFs card
        sys_files_html = ""
        for f in sys_files:
            sys_files_html += f"""
              <li style="margin-bottom:8px;">
                {f}
                <form method="post" style="display:inline; margin-left:10px;">
                  <input type="hidden" name="sys_file" value="{f}">
                  <button type="submit" name="action" value="delete_sys_file">X</button>
                </form>
              </li>"""
        sys_files_card = f"""
        <div class="card">
          <h3>Manage System PDFs</h3>
          <div class="scrollable-list">
            <ul style="list-style:none; padding-left:0; margin:0;">
              {sys_files_html or "<li>No PDFs found.</li>"}
            </ul>
          </div>
        </div>
        """
        llm = smx.load_llm_settings()
        return render_template_string(f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <title>{smx.favicon}{smx.site_title} Admin Dashboard</title>
          <style>
            body {{
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                background: #f4f7f9;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            h1 {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .card {{
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 20px;
                margin-bottom: 20px;
            }}
            .grid {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
            }}
            .grid > .card {{
                flex: 1 1 calc(33.333% - 20px);
                min-width: 280px;
            }}
            input, textarea, select {{
                padding: 10px;
                font-size: 1em;
                margin: 5px 0 15px;
                width: 100%;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
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
            a.button {{
                display: inline-block;
                padding: 10px 20px;
                background: #007acc;
                color: #fff;
                border-radius: 4px;
                text-decoration: none;
                margin-right: 10px;
            }}
            a.button:hover {{
                background: #005fa3;
            }}
            .scrollable-list {{
              max-height: 125px;     
              overflow-y: auto;      
              padding-right: 10px;    
              margin-top: 10px;       
            }}
            /* Striped backgrounds for the SYSTEM PDF list */
            .scrollable-list ul {{
              list-style: none;
              padding-left: 0;
              margin: 0;
            }}
            .scrollable-list ul li:nth-child(odd) {{
              background-color: #bde6f7;
            }}
            .scrollable-list ul li:nth-child(even) {{
              background-color: #d1d6d8;
            }}
            .scrollable-list ul li {{
              padding: 3px;
            }}

            /* Striped backgrounds for the PAGES list */
            .scrollable-pages > div:nth-child(odd) {{
              background-color: #f9f9f9;
            }}
            .scrollable-pages > div:nth-child(even) {{
              background-color: #ffffff;
            }}
            .scrollable-pages > div {{
              padding: 8px;
            }}
            .btn-delete {{
                background-color:red;
            }}
          </style>
        </head>
        <body>
        {{% for m in get_flashed_messages() %}}
          <div style="color:green;">
            {{{{ m }}}}
          </div>
        {{% endfor %}}
          <div class="container">
            <h1>Admin</h1>
            {alert_script}
            
            <div class="card">
              <h3>LLM Settings</h3>
              <form method="post" style="display:inline-block; margin-right:8px;">
                <input type="hidden" name="action" value="save_llm">
                <label>Provider</label>
                <select id="prov" name="provider" onchange="updModels()">
                  <option value="openai"   {{ 'selected' if llm['provider']=='openai'   else '' }}>OpenAI</option>
                  <option value="google"   {{ 'selected' if llm['provider']=='google'   else '' }}>Google</option>
                  <option value="xai"      {{ 'selected' if llm['provider']=='xai'      else '' }}>xAI</option>
                  <option value="deepseek" {{ 'selected' if llm['provider']=='deepseek' else '' }}>Deepseek</option>
                </select>
                 <label style="margin-top:6px;">Model</label>
                <select id="model" name="model"></select>

                <label style="margin-top:6px;">API Key</label>
                <input type="password" name="api_key"
                      placeholder="{ '********' if llm['api_key'] else 'api_key' }"
                      value="">
                <button type="submit" style="margin-top:6px;">Save</button>
              </form>
              <style>
                th, td {{
                    width: 20px;
                    padding:3px;
                }}
              </style>
              <!-- DELETE-KEY form (just the ✕) -->
              {{% if llm['api_key'] %}}
                <form method="post" style="display:inline-block;">
                  <table>
                    <tr>
                      <th>Provider</th>
                      <th>Model</th>
                      <th>Key</th>
                      <th></th>
                    </tr>
                    <tr>
                      <td>{llm['provider']}</td>
                      <td>{llm['model']}</td>
                      <td>******</td>
                      <td>
                          <input type="hidden" name="action" value="delete_llm">
                          <button class="btn-delete" type="submit" 
                                  title="Delete stored API key"
                                  onclick="return confirm('Remove stored API key?');">x</button>
                    </tr>
                  </table>
              </form>
              {{% endif %}}            
            </div>

            <script>
              const MAP = {{
                openai: [
                          "gpt-4o-mini",
                          "gpt-4o-mini-search-preview", 
                          "gpt-4o",
                          "gpt-4o-search-preview",
                          "gpt-4.1-nano",
                          "gpt-4.1-mini",
                          "gpt-4.1"
                ],
                google: [
                          "gemini-2.0-flash-lite",
                          "gemini-2.0-flash",
                          "gemini-2.5-flash-lite-preview-06-17", 
                          "gemini-2.5-flash-preview-04-17", 
                          "gemini-2.5-flash","gemini-2.5-pro"
                ],
                xai: [
                        "grok-3-mini",
                        "grok-3-mini-fast",
                        "grok-3"
                ],
                deepseek: [
                            "deepseek-chat",
                            "deepseek-reasoner"
                ]
              }};

              function updModels(){{
                const p=document.getElementById('prov').value;
                const sel=document.getElementById('model');
                sel.innerHTML='';
                MAP[p].forEach(m=>{{
                  const o=document.createElement('option');
                  o.value=o.text=m;
                  sel.appendChild(o);
                }});
              }}
              document.addEventListener("DOMContentLoaded",updModels);
            </script>

            <div class="grid">
                <!-- Upload PDF Card -->
                <div class="card">
                  <h3>Upload PDF Files</h3>
                  <form method="post" enctype="multipart/form-data">
                        <input type="file" name="upload_files" accept=".pdf" multiple>
                        <div style="text-align:right;">
                            <button type="submit" name="action" value="upload_files">Upload</button>
                        </div>
                  </form>
                </div>
                <!--
                <form method="post" enctype="multipart/form-data">
                    <label for="pdf_path">PDF Files Directory:</label>
                    <input type="text" name="pdf_path" value="uploads/sys" placeholder="Enter directory path">
                    <button type="submit" name="action" value="process_pdfs">Process PDFs</button>
                </form>
                -->
                <div class="card">
                  {sys_files_card}
                </div>
                <!-- Add New Page Card -->
                <div class="card">
                  <h3>Add New Page</h3>
                  <form method="post">
                        <input type="text" name="page_name" placeholder="Page Name" required>
                        <textarea name="page_content" placeholder="Page Content"></textarea>
                        <div style="text-align:right;">
                            <button type="submit" name="action" value="add_page">Add Page</button>
                        </div>
                  </form>
                </div>

                <!-- Manage Pages Card -->
                <div class="card">
                  <h3>Manage Pages</h3>
                  <div class="scrollable-list">
                        {page_cards}
                  </div>
                </div>

                <!-- Media Files Card -->
                <div class="card">
                  <h3>Upload Media Files</h3>
                  <form id="media-upload-form" method="post" enctype="multipart/form-data" action="/admin/upload_media">
                      <input type="file" name="media_files" accept="image/*,video/*" multiple>
                      <div style="text-align:right;">
                          <button type="submit">Upload Media</button>
                      </div>
                  </form>
                  <div id="media-upload-result"></div>
                </div>
                <!-- Theme Toggle Card -->
            </div>
            <div style="text-align: center; margin-top:20px;">
              <a class="button" href="/">Return to Home</a>
            </div>
          </div>
          <script>
            document.getElementById("media-upload-form").addEventListener("submit", function(e) {{
                e.preventDefault();
                var formData = new FormData(this);
                fetch("/admin/upload_media", {{ method: "POST", body: formData }})
                  .then(response => response.json())
                  .then(data => {{
                      var resultDiv = document.getElementById("media-upload-result");
                      if (data.file_paths && data.file_paths.length > 0) {{
                          resultDiv.innerHTML = "<p>Uploaded Media Files:</p><ul>" + 
                              data.file_paths.map(path => `<li>${{path}}</li>`).join("") + "</ul><p>Copy the path you need and insert it into your HTML.</p>";
                      }} else {{
                          resultDiv.innerHTML = "<p>No files were uploaded.</p>";
                      }}
                  }})
                  .catch(err => {{
                      console.error("Error uploading media:", err);
                      document.getElementById("media-upload-result").innerHTML = "<p>Error uploading files.</p>";
                  }});
            }});
          </script>
        </body>
        </html>
        """, llm=llm)
    
    @smx.app.route("/admin/chunks", methods=["GET"])
    def list_chunks():
        # Retrieve all chunks from the database
        chunks = db.get_all_pdf_chunks()
        # Render them in a simple HTML table (for demo purposes)
        html = "<h2>PDF Chunk Records</h2><table border='1'><tr><th>ID</th><th>Source File</th><th>Index</th><th>Text Snippet</th><th>Actions</th></tr>"
        for chunk in chunks:
            snippet = chunk['chunk_text'][:100] + "..."
            html += f"<tr><td>{chunk.get('id', 'N/A')}</td><td>{chunk['source_file']}</td><td>{chunk['chunk_index']}</td>"
            html += f"<td>{snippet}</td>"
            html += f"<td><a href='/admin/chunks/edit/{chunk.get('id')}'>Edit</a> "
            html += f"<a href='/admin/chunks/delete/{chunk.get('id')}'>Delete</a></td></tr>"
        html += "</table>"
        return html

    @smx.app.route("/admin/chunks/edit/<int:chunk_id>", methods=["GET", "POST"])
    def edit_chunk(chunk_id):
        if request.method == "POST":
            new_text = request.form.get("chunk_text")
            db.update_pdf_chunk(chunk_id, new_text)
            return redirect(url_for("list_chunks"))
        # For GET, load the specific chunk and render an edit form.
        conn = sqlite3.connect(db.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, source_file, chunk_index, chunk_text FROM pdf_chunks WHERE id = ?", (chunk_id,))
        chunk = cursor.fetchone()
        conn.close()
        if not chunk:
            return "Chunk not found", 404
        # Render a simple HTML form
        html = f"""
        <h2>Edit Chunk {chunk[0]} (from {chunk[1]}, index {chunk[2]})</h2>
        <form method="post">
            <textarea name="chunk_text" rows="10" cols="80">{chunk[3]}</textarea><br>
            <button type="submit">Save Changes</button>
        </form>
        """
        return html

    @smx.app.route("/admin/chunks/delete/<int:chunk_id>", methods=["GET"])
    def delete_chunk(chunk_id):
        db.delete_pdf_chunk(chunk_id)
        return redirect(url_for("list_chunks"))

    # ---- EDIT PAGE ------------------------------------------------
    @smx.app.route("/admin/edit/<page_name>", methods=["GET", "POST"])
    def edit_page(page_name):
        if request.method == "POST":
            new_page_name = request.form.get("page_name", "").strip()
            new_content = request.form.get("page_content", "").strip()
            if page_name in smx.pages and new_page_name:
                db.update_page(page_name, new_page_name, new_content)
                return redirect(url_for("admin_panel"))
        # Load the full content for the page to be edited.
        content = smx.pages.get(page_name, "")
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <title>Edit Page - {{ page_name }}</title>
          <style>
            body {
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                background: #f4f7f9;
                padding: 20px;
            }
            .editor {
                max-width: 800px;
                margin: 0 auto;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            input, textarea {
                width: 100%;
                margin: 10px 0;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            button {
                padding: 10px 20px;
                background: #007acc;
                border: none;
                color: #fff;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background: #005fa3;
            }
            a.button {
                padding: 10px 20px;
                background: #aaa;
                border: none;
                color: #fff;
                border-radius: 4px;
                text-decoration: none;
            }
            a.button:hover {
                background: #888;
            }
          </style>
        </head>
        <body>
          <div class="editor">
            <h1>Edit Page - {{ page_name }}</h1>
            <form method="post">
                <input type="text" name="page_name" value="{{ page_name }}" required>
                <textarea name="page_content" rows="20">{{ content }}</textarea>
                <div style="margin-top:15px;">
                  <button type="submit">Update Page</button>
                  <a class="button" href="{{ url_for('admin_panel') }}">Cancel</a>
                </div>
            </form>
          </div>
        </body>
        </html>
        """, page_name=page_name, content=content)
    
    # ──────────────────────────────────────────────────────────────────────────────────────── 
    # ACCOUNTS
    # ──────────────────────────────────────────────────────────────────────────────────────── 
    # ----Register ----------------------------------------
    @smx.app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
          email = request.form["email"].strip()
          username = request.form["username"].strip()
          password = request.form["password"]
          role = request.form.get("role", "user")
          if not email or not password:
              flash("email and password required.")
          else:
              success = register_user(email, username, password, role)
              if success:
                  flash("Registration successful—please log in.")
                  return redirect(url_for("login"))
              else:
                  flash("Email already taken.")
        return render_template("register.html")

    # ----- Login --------------------------------------------
    @smx.app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
          email = request.form["email"]
          password = request.form["password"]
          user = authenticate(email, password)
          if user:
              # put only the minimal info in session
              session["user_id"] = user["id"]
              session["email"] = user["email"]
              session["username"] = user["username"]
              session["role"] = user["role"]

              # ensure the just-logged-in user’s “Current” chat is closed on next GET
              session["needs_end_chat"] = True
              
              # — Load past chats from chats.db for this user —
              chat_ids = SQLHistoryStore.list_chats(user["id"])
              past = []
              for cid in chat_ids:
                  # load title *and* history; title was persisted earlier
                  title, history = SQLHistoryStore.load_with_title(user["id"], cid)
                  past.append({
                      "id": cid,
                      "title": title or "Untitled",
                      "history": history
                  })

              # Any chats still titled "Current" now have their full history available:
              # generate & persist a proper title for each one          
              for entry in past:
                  if entry["title"] == "Current" and entry["history"]:
                      new_title = smx.generate_contextual_title(entry["history"])
                      # update DB and in-memory entry
                      SQLHistoryStore.save(user["id"], entry["id"], entry["history"], new_title)
                      entry["title"] = new_title

              # Now store past into session
              session["past_sessions"] = past     

              flash("Logged in successfully.")
              return redirect(url_for("home"))
          else:
              flash("Invalid username or password.")
        return render_template("login.html")

      # ----- Logout -------------------------------------------
    @smx.app.route("/logout", methods=["POST"])
    def logout():
        """Clear session and return to login."""
        session.clear()
        flash("You have been logged out.")
        return redirect(url_for("login"))

    # --- UPLOAD MEDIA --------------------------------------
    @smx.app.route("/admin/upload_media", methods=["POST"])
    def upload_media():               
        # Retrieve uploaded media files (images, videos, etc.).
        uploaded_files = request.files.getlist("media_files")
        file_paths = []
        for file in uploaded_files:
            if file.filename:
                filepath = os.path.join(MEDIA_FOLDER, file.filename)
                file.save(filepath)
                # This path can be copied by the developer. Adjust if you have a web server serving these files.
                file_paths.append(f"/uploads/media/{file.filename}")
        return jsonify({"file_paths": file_paths})
    
    # Serve the raw media files
    @smx.app.route('/uploads/media/<path:filename>')
    def serve_media(filename):
        media_dir = os.path.join(os.getcwd(), 'uploads', 'media')
        return send_from_directory(media_dir, filename)
    
    # ──────────────────────────────────────────────────────────────────────────────────────── 
    # DASHBOARD
    # ──────────────────────────────────────────────────────────────────────────────────────── 
    # ── DASHBOARD VIEW DETAILS -----------------------------
    @smx.app.route("/dashboard", methods=["GET", "POST"])
    @superadmin_required
    @admin_required
    def dashboard():
        DATA_FOLDER = os.path.join(os.getcwd(), "uploads", "data")
        os.makedirs(DATA_FOLDER, exist_ok=True)

        section = request.args.get("section", "explore")
        datasets = [f for f in os.listdir(DATA_FOLDER) if f.lower().endswith(".csv")]
        selected_dataset = request.form.get("dataset") or request.args.get("dataset")
        if not selected_dataset and datasets:
            selected_dataset = datasets[0]

        selected_dataset = selected_dataset or ""

        # Handle file upload
        if request.method == "POST" and "dataset_file" in request.files:
            f = request.files["dataset_file"]
            if f.filename.lower().endswith(".csv"):
                path = os.path.join(DATA_FOLDER, f.filename)
                f.save(path)
                flash(f"Uploaded {f.filename}")
                return redirect(url_for("dashboard", section=section, dataset=f.filename))

        # Load dataframe if available
        df = pd.read_csv(os.path.join(DATA_FOLDER, selected_dataset)) if selected_dataset else None

        # --- Jupyter kernel management ---
        session_id = session.get('smx_kernel_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            session['smx_kernel_id'] = session_id

        km, kc = SyntaxMatrixKernelManager.start_kernel(session_id)

        # --- Handle Ask AI ---
        ai_outputs = []
        askai_question = None
        refined_question = None
        ai_code = None

        if request.method == "POST" and "askai_question" in request.form:
            askai_question = request.form["askai_question"].strip()
            if df is not None:      
                
                refined_question = refine_eda_question(askai_question, df)
                ai_code = smx.ai_generate_code(refined_question, df)
                intent = classify(refined_question)
                ai_code = auto_inject_template(ai_code, intent, df)
                ai_code = fix_scatter_and_summary(ai_code)
                ai_code = fix_importance_groupby(ai_code)
                ai_code = inject_auto_preprocessing(ai_code)
                ai_code = patch_plot_code(ai_code, df, refined_question)
                ai_code = patch_pairplot(ai_code, df)
                ai_code = get_plotting_imports(ai_code)
                ai_code = ensure_image_output(ai_code)      
                ai_code = fix_numeric_sum(ai_code)
                ai_code = ensure_accuracy_block(ai_code)
                ai_code = ensure_output(ai_code)
                ai_code = fix_plain_prints(ai_code)
                ai_code = fix_to_datetime_errors(ai_code)

                # Always make sure 'df' is in the kernel before running user code
                 # Always make sure 'df' is in the kernel before running user code
                df_init_code = (
                    f"import pandas as pd\n"
                    f"df = pd.read_csv(r'''{os.path.join(DATA_FOLDER, selected_dataset)}''')"
                )
                execute_code_in_kernel(kc, df_init_code)

                outputs, errors = execute_code_in_kernel(kc, ai_code)
                ai_outputs = [Markup(o) for o in outputs + errors]
          
            else:
                ai_outputs = [Markup("<div style='color:red;'>No dataset loaded.</div>")]  

        # --- EDA/static cells ---
        data_cells = []
        if df is not None:
            preview_cols = df.columns[:8]
            data_cells.append({
                "title": "Data Preview",
                "output": Markup(datatable_box(df[preview_cols].head(8))),
                "code": f"df[{list(preview_cols)}].head(8)"
            })
            data_cells.append({
                "title": "Summary Statistics",
                "output": Markup(datatable_box(df.describe())),
                "code": "df.describe()"
            })
            nulls = df.isnull().sum()
            nulls_pct = (df.isnull().mean() * 100).round(1)
            missing_df = pd.DataFrame({
                "Missing Values": nulls,
                "Missing (%)": nulls_pct
            })
            missing = missing_df[missing_df["Missing Values"] > 0]
            data_cells.append({
                "title": "Missing Values",
                "output": Markup(datatable_box(missing)) if not missing.empty else "<em>No missing values detected.</em>",
                "code": (
                    "nulls = df.isnull().sum()\n"
                    "nulls_pct = (df.isnull().mean() * 100).round(1)\n"
                    "missing_df = pd.DataFrame({'Missing Values': nulls, 'Missing (%)': nulls_pct})\n"
                    "missing_df[missing_df['Missing Values'] > 0]"
                )
            })
            dtype_df = pd.DataFrame({
                "Type": df.dtypes.astype(str),
                "Non-Null Count": df.notnull().sum(),
                "Unique Values": df.nunique()
            })
            data_cells.append({
                "title": "Column Types",

                "output": Markup(datatable_box(dtype_df)),
                "code": (
                    "pd.DataFrame({\n"
                    "    'Type': df.dtypes.astype(str),\n"
                    "    'Non-Null Count': df.notnull().sum(),\n"
                    "    'Unique Values': df.nunique()\n"
                    "})"
                )
            })
        return render_template(
            "dashboard.html",
            section=section,
            datasets=datasets,
            selected_dataset=selected_dataset,
            ai_outputs=ai_outputs,
            ai_code=ai_code,  # AI-generated code for toggle
            askai_question=askai_question,  # User's question
            refined_question=refined_question,  # Refined question
            data_cells=data_cells,
        )

    # ── UPLOAD DATASET --------------------------------------
    @smx.app.route("/dashboard/upload", methods=["POST"])
    def upload_dataset():
        # DATA_FOLDER = os.path.join(os.getcwd(), "uploads", "data")
        # os.makedirs(DATA_FOLDER, exist_ok=True)
        if "dataset_file" not in request.files:
            flash("No file part.")
            return redirect(url_for("dashboard"))
        file = request.files["dataset_file"]
        if file.filename == "":
            flash("No selected file.")
            return redirect(url_for("dashboard"))
        if file and file.filename.lower().endswith(".csv"):
            filename = werkzeug.utils.secure_filename(file.filename)
            file.save(os.path.join(DATA_FOLDER, filename))
            flash(f"Uploaded: {filename}")
        else:
            flash("Only CSV files are supported.")
        return redirect(url_for("dashboard"))
    
    # ── DELETE A DATASET --------------------------------------
    @smx.app.route("/dashboard/delete_dataset/<path:dataset_name>", methods=["POST"])
    def delete_dataset(dataset_name):
        file_path   = os.path.join(DATA_FOLDER, dataset_name)

        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                flash(f"Deleted {dataset_name}")
            except Exception as exc:
                flash(f"Could not delete {dataset_name}: {exc}", "error")
        else:
            flash(f"{dataset_name} not found.", "error")

        # go back to the dashboard; dashboard() will auto-select the next file
        return redirect(url_for("dashboard"))
    
   
    @smx.app.errorhandler(500)
    def internal_error(err):
        return render_template("error.html", message=str(err)), 500
