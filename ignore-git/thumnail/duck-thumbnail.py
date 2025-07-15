import imgkit
from pathlib import Path

# ==== PARAMETERS ====
logo_path = Path("logo.jpg").resolve().as_uri()  # Converts to full file:// path
username = "Requestedreads"
content = """
When I was 17, my family moved two states away without telling me. They left a note that said, <strong>“You’ll figure it out.”</strong><br><br>
Twelve years later, after I finally made it without them, they reached out trying to reconnect.
"""

# ==== HTML TEMPLATE ====
html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {{
      margin: 0;
      font-family: 'Segoe UI', 'Arial', sans-serif;
      background: #fff;
      display: inline-block;
    }}

    .card {{
      width: 800px;
      padding: 24px 28px;
      border-radius: 20px;
      border: 1px solid #e0e0e0;
      background: #fff;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }}

    .header {{
      display: flex;
      align-items: center;
    }}

    .avatar-img {{
      width: 60px;
      height: 60px;
      border-radius: 50%;
      object-fit: cover;
      margin-right: 14px;
    }}

    .user-info {{
      display: flex;
      flex-direction: column;
    }}

    .username {{
      font-weight: 700;
      font-size: 1.4rem;
      display: flex;
      align-items: center;
      color: #111;
    }}

    .verified {{
      width: 20px;
      height: 20px;
      margin-left: 6px;
    }}

    .emojis {{
      font-size: 1.2rem;
      margin-top: 2px;
      color: #444;
    }}

    .content {{
      margin-top: 24px;
      font-size: 1.45rem;
      line-height: 1.6;
      color: #1a1a1a;
    }}

    .footer {{
      margin-top: 26px;
      font-size: 1.1rem;
      display: flex;
      justify-content: space-between;
      color: #888;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <img src="{logo_path}" class="avatar-img" alt="Avatar">
      <div class="user-info">
        <div class="username">{username}
          <img src="https://upload.wikimedia.org/wikipedia/commons/e/e4/Twitter_Verified_Badge.svg" class="verified">
        </div>
        <div class="emojis">🫖🤍🧠🧠💎☀️❤️💀👏</div>
      </div>
    </div>
    <div class="content">{content}</div>
    <div class="footer">
      <span>❤️ 99+   💬 99+</span>
      <span>📤 Share</span>
    </div>
  </div>
</body>
</html>
"""

# ==== GENERATE IMAGE ====
output_path = "thumbnail_output.png"
imgkit.from_string(html, output_path, options={
    'quiet': '',
    'encoding': 'UTF-8',
    'width': '800',  # Set the width to match the card width
    'height': '400',  # Set the height to match the card height
})

# Print the output path
print(f"Image saved at: {Path(output_path).resolve()}")
