import os, hashlib, html
from pathlib import Path

def color_from_nick(nick):
    return f"hsl({int(hashlib.md5(nick.encode()).hexdigest(), 16) % 360}, 70%, 70%)"

def convert_log_to_html(log_path):
    lines = Path(log_path).read_text(encoding="utf-8").splitlines()
    html_lines = ['<html><head><meta charset="UTF-8"><style>body{font-family:monospace;background:#111;color:#eee;padding:1em;} .system{color:#aaa;} .timestamp{color:#888;} .message{color:#dfd;}</style></head><body>']

    for line in lines:
        if line.startswith("****"):
            html_lines.append(f'<div class="system">{html.escape(line)}</div>')
        elif line.startswith("May "):
            try:
                timestamp_end = line.index(">")
                prefix = line[:timestamp_end+1]
                message = line[timestamp_end+1:].strip()
                nick = prefix[prefix.index("<")+1:prefix.index(">")]
                timestamp = prefix[:prefix.index("<")].strip()
                nick_color = color_from_nick(nick)
                html_lines.append(
                    f'<div><span class="timestamp">{html.escape(timestamp)}</span> '
                    f'<span class="user" style="color:{nick_color}">&lt;{html.escape(nick)}&gt;</span> '
                    f'<span class="message">{html.escape(message)}</span></div>'
                )
            except:
                html_lines.append(f'<div>{html.escape(line)}</div>')
        else:
            html_lines.append(f'<div>{html.escape(line)}</div>')
    html_lines.append("</body></html>")
    
    output = Path(log_path).with_suffix(".html")
    output.write_text("\n".join(html_lines), encoding="utf-8")
    print(f"Converted: {output}")

# Tots els logs de la carpeta
for file in Path(".").glob("*.log.txt"):
    convert_log_to_html(file)