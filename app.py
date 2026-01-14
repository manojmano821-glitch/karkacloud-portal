import os
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "karkacloud_final_secure_2026"

# Database structure: {email: {"pwd": pwd, "name": name}}
users_db = {}

# Premium Tricks Data
TRICKS_LIST = [
    {"title": "Square of 5-Ending Numbers", "desc": "Example: 25x25. 5x5=25-nu pinnaadi pottutu, 2 x (2+1)=6-nu munaadi podunga. Answer 625!"},
    {"title": "Multiply any number by 11", "desc": "Example: 24x11. 2 and 4 naduvula (2+4=6) pottukaunga. Answer 264."},
    {"title": "Fast Multiplication Trick", "desc": "Thanglish: Rendu numbers-ai kooti naduvula pottukanum! Simple logic."}
]

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="ta">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --primary: #6366f1; --accent: #f59e0b; --bg: #f0f2f5; }
        body { font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; background: var(--bg); }
        .nav { background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); margin: 10px 15px; padding: 12px 20px; border-radius: 20px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 10px; z-index: 1000; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
        .logo { font-size: 1.3rem; font-weight: 800; color: #444; text-decoration: none; }
        .logo span { color: var(--accent); }
        .welcome-banner { background: linear-gradient(135deg, #a855f7, #6366f1); color: white; padding: 30px 20px; border-radius: 25px; margin: 15px; box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3); }
        .welcome-banner h1 { margin: 0; font-size: 1.6rem; font-weight: 800; }
        .container { padding: 0 15px 40px; }
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }
        .card { background: white; padding: 20px; border-radius: 20px; text-decoration: none; color: inherit; box-shadow: 0 8px 15px rgba(0,0,0,0.03); display: flex; flex-direction: column; align-items: center; text-align: center; border: 1px solid rgba(255,255,255,0.8); transition: 0.3s; }
        .icon-box { width: 50px; height: 50px; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-bottom: 12px; }
        .icon-gold { background: #fffbeb; color: #d97706; }
        .upgrade-box { background: #1e293b; color: white; padding: 30px 20px; border-radius: 25px; margin-top: 30px; text-align: center; border: 3px solid #334155; }
        .btn-upgrade { background: var(--accent); color: white; border: none; padding: 14px 40px; border-radius: 15px; font-weight: 700; cursor: pointer; width: 100%; margin-top: 15px; }
        .auth-screen { height: 95vh; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #fff; padding: 20px; }
        .auth-input { width: 100%; max-width: 320px; padding: 16px; margin: 8px 0; border: 1.5px solid #e2e8f0; border-radius: 15px; background: #f8fafc; }
    </style>
</head>
<body>
    {% if not user_name %}
    <div class="auth-screen">
        <div style="font-size: 2rem; font-weight: 800; color: var(--primary); margin-bottom: 25px;"><i class="fas fa-cloud"></i> KARKA</div>
        <form method="POST" action="/auth" style="width: 100%; display: flex; flex-direction: column; align-items: center;">
            <input type="text" name="name" class="auth-input" placeholder="Full Name (for Dashboard)" required>
            <input type="email" name="email" class="auth-input" placeholder="Gmail ID" required>
            <input type="password" name="pwd" class="auth-input" placeholder="Set Password" required>
            <button type="submit" name="act" value="reg" style="width:100%; max-width:320px; background:var(--primary); color:white; border:none; padding:16px; border-radius:15px; font-weight:700; cursor:pointer;">Launch My Career 🚀</button>
        </form>
    </div>
    {% else %}
    <div class="nav">
        <a href="/" class="logo">K <span>KARKA</span> <i class="fas fa-cloud"></i></a>
        <div style="font-weight: 600; font-size: 0.8rem; color: #64748b;">Hi, {{ user_name }}!</div>
    </div>
    <div class="welcome-banner">
        <h1>Vanakkam, {{ user_name }}!</h1>
        <p>Your goal: TNPSC 2026. <br><b>Stay focused and keep learning!</b></p>
    </div>
    <div class="container">
        <h3 style="margin:20px 10px; font-size:0.9rem; color:#64748b;">PREMIUM TRICKS</h3>
        <div class="grid">
            <a href="/tricks" class="card"><div class="icon-box icon-gold"><i class="fas fa-calculator"></i></div><h4>Maths Tricks</h4><span style="font-size:0.7rem;">1000+ Shortcuts</span></a>
            <div class="card"><div class="icon-box icon-gold" style="background:#f5f3ff; color:#7c3aed;"><i class="fas fa-brain"></i></div><h4>Memory Hacks</h4><span style="font-size:0.7rem;">Mnemonics 2026</span></div>
        </div>
        <div class="upgrade-box">
            <h2>Premium Upgrade</h2>
            <div style="font-size: 1.8rem; font-weight: 800; margin: 10px 0;">₹499</div>
            <button class="btn-upgrade" onclick="alert('Redirecting...')">UPGRADE NOW 🚀</button>
        </div>
        <div style="text-align:center; margin-top:30px;"><a href="/logout" style="color:#94a3b8; text-decoration:none; font-size:0.8rem;">Logout</a></div>
    </div>
    {% endif %}
    {% if page == 'tricks' %}
    <div style="position: fixed; inset: 0; background: #fff; z-index: 2000; overflow-y: auto; padding: 25px;">
        <a href="/" style="font-size: 1rem; color: var(--primary); text-decoration: none; font-weight: 700;"><i class="fas fa-arrow-left"></i> BACK</a>
        <h2 style="margin-top: 25px;">1000+ Maths Shortcut Tricks</h2>
        {% for trick in tricks_list %}
        <div style="background: #f8fafc; padding: 20px; border-radius: 20px; margin-bottom: 15px; border-left: 5px solid var(--accent);">
            <h4 style="margin: 0 0 10px; color: var(--primary);">{{ trick.title }}</h4>
            <p style="margin: 0; font-size: 0.9rem; line-height: 1.6;">{{ trick.desc }}</p>
        </div>
        {% endfor %}
        <div style="text-align: center; padding: 30px;"><button style="background:var(--accent); color:white; border:none; padding:15px 40px; border-radius:15px; font-weight:700;">Pay ₹499 to Unlock All</button></div>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT, user_name=session.get('user_name'))

@app.route('/tricks')
def tricks():
    if not session.get('user_name'): return redirect(url_for('home'))
    return render_template_string(HTML_LAYOUT, user_name=session.get('user_name'), page='tricks', tricks_list=TRICKS_LIST)

@app.route('/auth', methods=['POST'])
def auth():
    email = request.form.get('email')
    pwd = request.form.get('pwd')
    name = request.form.get('name')
    act = request.form.get('act')
    if act == 'reg':
        users_db[email] = {"pwd": pwd, "name": name}
        session['user_name'] = name
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
