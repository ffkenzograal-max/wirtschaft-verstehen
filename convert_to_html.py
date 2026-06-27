import os
import sys
import re

def check_dependencies():
    try:
        import markdown
    except ImportError:
        pass # UV runs with --with markdown, so it's handled

def convert_all():
    import markdown
    
    files = ["README.md", "chapter_1.md", "chapter_2.md", "chapter_3.md", "chapter_4.md", "chapter_5.md"]
    
    # Styled HTML Template - Premium WU Wien Corporate style with Sidebar
    html_header = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Понимание экономики (Wirtschaft verstehen) - WU Wien</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script>
      window.MathJax = {
        tex: {
          inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
          displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
        }
      };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        :root {
            --bg-color: #f8fafc;
            --text-color: #334155;
            --text-dark: #0f172a;
            --primary-color: #00407A; /* WU Corporate Blue */
            --primary-light: #e0f2fe;
            --accent-color: #0284c7;
            --border-color: #e2e8f0;
            
            --note-bg: #f0f9ff;
            --note-border: #0ea5e9;
            --note-text: #0369a1;
            
            --tip-bg: #f0fdf4;
            --tip-border: #22c55e;
            --tip-text: #15803d;
            
            --warn-bg: #fffbeb;
            --warn-border: #f59e0b;
            --warn-text: #b45309;
            
            --danger-bg: #fef2f2;
            --danger-border: #ef4444;
            --danger-text: #b91c1c;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.65;
            margin: 0;
            padding: 0;
            display: flex;
            min-height: 100vh;
        }

        /* Sidebar Navigation */
        .sidebar {
            width: 280px;
            background-color: #0f172a;
            color: #f1f5f9;
            padding: 30px 20px;
            box-sizing: border-box;
            position: fixed;
            top: 0;
            bottom: 0;
            left: 0;
            overflow-y: auto;
            border-right: 1px solid rgba(255,255,255,0.1);
            display: flex;
            flex-direction: column;
            z-index: 100;
        }

        .sidebar-logo {
            font-family: 'Outfit', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            color: #fff;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            text-align: center;
        }
        
        .sidebar-logo span {
            color: #38bdf8;
        }

        .sidebar-menu {
            list-style: none;
            padding: 0;
            margin: 0;
            flex-grow: 1;
        }

        .sidebar-item {
            margin-bottom: 8px;
        }

        .sidebar-link {
            display: block;
            padding: 12px 15px;
            color: #94a3b8;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
            transition: all 0.2s;
        }

        .sidebar-link:hover, .sidebar-link.active {
            color: #fff;
            background-color: rgba(255,255,255,0.08);
            padding-left: 20px;
        }
        
        .sidebar-link.active {
            border-left: 4px solid #38bdf8;
            background-color: rgba(2, 132, 199, 0.15);
        }

        /* Main Content Area */
        .main-wrapper {
            margin-left: 280px;
            flex-grow: 1;
            display: flex;
            justify-content: center;
            padding: 40px;
            box-sizing: border-box;
        }

        .container {
            max-width: 850px;
            width: 100%;
            background-color: #fff;
            padding: 50px 60px;
            box-sizing: border-box;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
            border: 1px solid var(--border-color);
        }

        /* Reading progress bar */
        .progress-bar-container {
            position: fixed;
            top: 0;
            left: 280px;
            right: 0;
            height: 4px;
            background: #e2e8f0;
            z-index: 1000;
        }

        .progress-bar {
            height: 100%;
            background: #0ea5e9;
            width: 0%;
            transition: width 0.1s ease;
        }

        h1, h2, h3, h4 {
            font-family: 'Outfit', sans-serif;
            color: var(--text-dark);
            margin-top: 1.6em;
            margin-bottom: 0.6em;
            font-weight: 600;
        }

        h1 {
            font-size: 2.4rem;
            border-bottom: 3px solid var(--primary-color);
            padding-bottom: 12px;
            margin-top: 0;
            color: var(--primary-color);
        }

        h2 {
            font-size: 1.7rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 8px;
            margin-top: 2em;
        }

        h3 {
            font-size: 1.35rem;
            margin-top: 1.8em;
        }

        a {
            color: var(--accent-color);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.15s;
        }

        a:hover {
            color: var(--primary-color);
            text-decoration: underline;
        }

        p {
            font-size: 1.05rem;
            margin-bottom: 1.5em;
            text-align: justify;
        }

        ul, ol {
            padding-left: 24px;
            margin-bottom: 1.5em;
        }

        li {
            margin-bottom: 10px;
            font-size: 1.05rem;
        }

        /* Highlighting keywords like in textbook */
        strong {
            color: var(--text-dark);
            font-weight: 600;
        }

        code {
            font-family: Consolas, Monaco, monospace;
            background-color: #f1f5f9;
            padding: 3px 6px;
            border-radius: 4px;
            color: #e11d48;
            font-size: 0.9em;
        }

        pre {
            background-color: #0f172a;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            border: 1px solid #1e293b;
        }

        pre code {
            color: #f1f5f9;
            background-color: transparent;
            padding: 0;
        }

        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 35px auto;
            border-radius: 8px;
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
            border: 1px solid var(--border-color);
            padding: 5px;
            background: #fff;
        }

        /* Beautiful cards for Callouts / Alerts */
        .callout {
            margin: 25px 0;
            padding: 20px 24px;
            border-left: 5px solid #64748b;
            border-radius: 6px;
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        }

        .callout-title {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .callout-content p:last-child {
            margin-bottom: 0;
        }

        .callout-note {
            background-color: var(--note-bg);
            border-left-color: var(--note-border);
            color: #0c4a6e;
        }
        .callout-note .callout-title {
            color: var(--note-text);
        }

        .callout-tip {
            background-color: var(--tip-bg);
            border-left-color: var(--tip-border);
            color: #052e16;
        }
        .callout-tip .callout-title {
            color: var(--tip-text);
        }

        .callout-warning {
            background-color: var(--warn-bg);
            border-left-color: var(--warn-border);
            color: #451a03;
        }
        .callout-warning .callout-title {
            color: var(--warn-text);
        }

        .callout-danger {
            background-color: var(--danger-bg);
            border-left-color: var(--danger-border);
            color: #450a0a;
        }
        .callout-danger .callout-title {
            color: var(--danger-text);
        }

        /* Beautiful Premium Tables */
        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 35px 0;
            font-size: 0.95rem;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.05);
        }

        th, td {
            padding: 14px 18px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }

        th {
            background-color: #f1f5f9;
            color: var(--text-dark);
            font-weight: 600;
            border-bottom: 2px solid var(--border-color);
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover td {
            background-color: #f8fafc;
        }

        hr {
            border: 0;
            height: 1px;
            background: var(--border-color);
            margin: 50px 0;
        }
        
        .math {
            font-size: 1.1rem;
            background: #f8fafc;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            overflow-x: auto;
            text-align: center;
            margin: 20px 0;
        }

        @media (max-width: 1024px) {
            body {
                flex-direction: column;
            }
            .sidebar {
                width: 100%;
                position: relative;
                height: auto;
                border-right: none;
                border-bottom: 1px solid rgba(255,255,255,0.1);
                padding: 15px 20px;
            }
            .sidebar-logo {
                margin-bottom: 15px;
                padding-bottom: 5px;
                border-bottom: none;
            }
            .sidebar-menu {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                justify-content: center;
            }
            .sidebar-item {
                margin-bottom: 0;
            }
            .sidebar-link {
                padding: 8px 12px;
            }
            .sidebar-link.active {
                border-left: none;
                border-bottom: 3px solid #38bdf8;
            }
            .main-wrapper {
                margin-left: 0;
                padding: 20px 10px;
            }
            .container {
                padding: 30px 20px;
                border-radius: 0;
                box-shadow: none;
                border: none;
            }
            .progress-bar-container {
                left: 0;
            }
        }
    </style>
</head>
<body>
    <div class="progress-bar-container">
        <div class="progress-bar" id="readingProgress"></div>
    </div>
    
    <div class="sidebar">
        <div class="sidebar-logo">WU Wien <span>Пособие</span></div>
        <ul class="sidebar-menu">
            <li class="sidebar-item"><a href="README.html" class="sidebar-link" id="link-README">📖 Введение и Содержание</a></li>
            <li class="sidebar-item"><a href="chapter_1.html" class="sidebar-link" id="link-chapter_1">Раздел 1: Введение</a></li>
            <li class="sidebar-item"><a href="chapter_2.html" class="sidebar-link" id="link-chapter_2">Раздел 2: Общество и среда</a></li>
            <li class="sidebar-item"><a href="chapter_3.html" class="sidebar-link" id="link-chapter_3">Раздел 3: Управление фирмой</a></li>
            <li class="sidebar-item"><a href="chapter_4.html" class="sidebar-link" id="link-chapter_4">Раздел 4: Цифровизация</a></li>
            <li class="sidebar-item"><a href="chapter_5.html" class="sidebar-link" id="link-chapter_5">Раздел 5: Заключение</a></li>
            <li class="sidebar-item"><a href="quiz.html" class="sidebar-link" id="link-quiz">🎓 Интерактивный тест (Selbsttest)</a></li>
        </ul>
    </div>

    <div class="main-wrapper">
        <div class="container">
"""

    html_footer = """
        </div>
    </div>
    
    <script>
        // Set active link in sidebar based on current URL filename
        const filename = window.location.pathname.split("/").pop();
        if (filename) {
            const cleanName = filename.split(".")[0];
            const activeLink = document.getElementById("link-" + cleanName);
            if (activeLink) {
                activeLink.classList.add("active");
            }
        } else {
            document.getElementById("link-README").classList.add("active");
        }

        // Reading progress tracker
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            document.getElementById("readingProgress").style.width = scrolled + "%";
        });
    </script>
</body>
</html>
"""

    print("[+] Starting Premium Markdown to HTML conversion...")
    for f_name in files:
        if not os.path.exists(f_name):
            print(f"    [!] Skipping missing file {f_name}")
            continue
            
        out_name = f_name.replace(".md", ".html")
        
        with open(f_name, "r", encoding="utf-8") as f:
            md_content = f.read()
            
        # Convert links inside MD files from .md to .html so navigation works locally
        md_content = md_content.replace(".md)", ".html)")
        md_content = md_content.replace(".md#", ".html#")
        
        # PRE-PROCESS: Split adjacent blockquotes to prevent markdown library from merging them
        md_lines = md_content.split('\n')
        new_md_lines = []
        in_blockquote = False
        for idx, line in enumerate(md_lines):
            stripped = line.strip()
            is_callout_start = re.match(r'^>\s*\[!(NOTE|TIP|WARNING|IMPORTANT)\]', stripped)
            
            if is_callout_start and in_blockquote:
                # Insert HTML comment to force markdown parser to split blockquotes
                new_md_lines.append('')
                new_md_lines.append('<!-- -->')
                new_md_lines.append('')
            
            if stripped.startswith('>'):
                in_blockquote = True
            elif stripped == '':
                # Keep state if it's just an empty line
                pass
            else:
                in_blockquote = False
                
            new_md_lines.append(line)
        md_content = '\n'.join(new_md_lines)

        # PRE-PROCESS: Protect math blocks from being mangled by markdown parser (e.g. underscores converted to <em>)
        placeholders = {}
        counter = 0

        # Protect block math $$ ... $$
        def replace_block(match):
            nonlocal counter
            token = f"<!-- BLOCK_MATH_{counter} -->"
            placeholders[token] = f'<div class="math">$${match.group(1).strip()}$$</div>'
            counter += 1
            return token
        
        # Protect inline math \( ... \)
        def replace_inline(match):
            nonlocal counter
            token = f"MATHINLINE{counter}TOKEN"
            placeholders[token] = f"\\({match.group(1).strip()}\\)"
            counter += 1
            return token

        # Extract block math first
        md_content = re.sub(r'\$\$(.*?)\$\$', replace_block, md_content, flags=re.DOTALL)
        # Extract inline math
        md_content = re.sub(r'\\\((.*?)\\\)', replace_inline, md_content)
        
        # Convert Markdown to HTML with extensions
        html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'toc'])
        
        # Post-process blockquotes into beautiful textbook callout cards
        # Use a ROBUST regex that matches ALL content between <blockquote> and </blockquote>
        # regardless of whether it contains <p>, <ul>, <ol>, or multiple elements
        
        # Map of callout types to their styles
        callout_config = {
            'WARNING':   ('callout-warning', '⚠️', 'Разбор экзамена / Ловушка'),
            'IMPORTANT': ('callout-warning', '⚠️', 'Важно'),
            'NOTE':      ('callout-note', '📘', 'Определение / Понятие'),
            'TIP':       ('callout-tip', '💡', 'Пример / Цифры и факты'),
        }
        
        def parse_callout(match):
            inner = match.group(1).strip()
            
            # Detect callout type from [!TYPE] marker
            type_match = re.search(r'\[!(WARNING|IMPORTANT|NOTE|TIP)\]', inner)
            if not type_match:
                # No callout marker — return as styled blockquote
                return f'<div class="callout" style="background:#f1f5f9;">{inner}</div>'
            
            callout_type = type_match.group(1)
            css_class, icon, default_title = callout_config[callout_type]
            
            # Remove the [!TYPE] marker from the content
            inner = re.sub(r'\[!' + callout_type + r'\]\s*', '', inner, count=1).strip()
            
            # Remove wrapping <p> and </p> if the content starts with <p>
            inner = re.sub(r'^<p>\s*', '', inner)
            # Remove the first closing </p> only (there might be more elements after)
            inner = re.sub(r'</p>', '', inner, count=1)
            
            # Extract title from first <strong> tag
            title_m = re.search(r'<strong>(.*?)</strong>', inner)
            title = title_m.group(1) if title_m else default_title
            
            # Remove the title markup from the body
            body = re.sub(r'<strong>.*?</strong>\s*:?\s*(?:<br\s*/?>)?\s*', '', inner, count=1).strip()
            
            # Clean up any leading <br> tags
            body = re.sub(r'^(?:<br\s*/?>)+\s*', '', body).strip()
            
            # Clean up any remaining </p><p> sequences into line breaks
            body = re.sub(r'</p>\s*<p>', '<br/><br/>', body)
            # Clean trailing </p>
            body = re.sub(r'</p>\s*$', '', body).strip()
            # Clean leading <p>
            body = re.sub(r'^<p>\s*', '', body).strip()
            
            return f'<div class="callout {css_class}"><div class="callout-title">{icon} {title}</div><div class="callout-content">{body}</div></div>'
        
        # Match ALL blockquotes — greedy match of everything between <blockquote> and </blockquote>
        html_content = re.sub(r'<blockquote>\s*(.*?)\s*</blockquote>', parse_callout, html_content, flags=re.DOTALL)
        
        # Restore math placeholders
        for token, math_content in placeholders.items():
            html_content = html_content.replace(token, math_content)
        
        final_html = html_header + html_content + html_footer
        
        with open(out_name, "w", encoding="utf-8") as out_f:
            out_f.write(final_html)
            
        print(f"    [OK] Converted {f_name} -> {out_name}")
        
    print("[+] All files converted to HTML successfully!")

if __name__ == "__main__":
    check_dependencies()
    convert_all()
