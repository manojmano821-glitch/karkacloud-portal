import os
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "karkacloud_premium_2026"

# In-memory database (Render restart aana data clear aagum, but testing-ku perfect)
users = {}

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="ta">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --blue: #007aff; --gold: #f39c12; --white: #ffffff; --dark: #1c1c1e; }
        body { font-family: 'Segoe UI', sans-serif; margin: 0; background: #f2f2f7; color: var(--dark); }
        .nav { background: var(--white); padding: 15px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .logo { font-size: 1.5rem; font-weight: 800; color: var(--blue); }
        .logo span { color: var(--gold); }
        .container { max-width: 500px; margin: 40px auto; padding: 20px; }
        .card { background: var(--white); padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); text-align: center; transition: 0.3s; }
        input { width: 90%; padding: 15px; margin: 10px 0; border: 1px solid #eee; border-radius: 12px; background: #f9f9f9; font-size: 1rem; }
        .btn { background: var(--blue); color: white; border: none; padding: 15px; width: 100%; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 1rem; margin-top: 10px; }
        .btn-gold { background: var(--gold); }
        .feature-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px; }
        .feature-item { background: #fff; padding: 15px; border-radius: 15px; border-bottom: 3px solid var(--gold); }
        .news-ticker { background: var(--dark); color: var(--gold); padding: 10px; font-size: 0.9rem; overflow: hidden; white-space: nowrap; }
        .animate-flicker { animation: flicker 2s infinite; }
        @keyframes flicker { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    </style>
</head>
<body>
    <div class="news-ticker">
        <marquee>📢 24/7 TNPSC News: New Notification Expected Soon! | Current Affairs PDF Uploaded | Mock Test 12 is Live!</marquee>
    </div>
    <div class="nav"><div class="logo">KARKA <span>CLOUD</span></div></div>
    
    <div class="container">
        {% if not logged_in %}
            <div class="card">
                <h2 style="color: var(--blue);">Student Access</h2>
                <p>Register or Login to access Premium Materials</p>
                <form method="POST" action="/auth">
                    <input type="email" name="email" placeholder="Gmail ID" required>
                    <input type="password" name="password" placeholder="Create Password" required>
                    <button class="btn" name="action" value="login">Login</button>
                    <button class="btn btn-gold" name="action" value="reg">Register New Account</button>
                </form>
            </div>
        {% else %}
            <div class="card">
                <h2 class="animate-flicker">Welcome to Premium Dashboard</h2>
                <div class="feature-grid">
                    <div class="feature-item"><i class="fas fa-file-pdf"></i><br>TNPSC PDFs</div>
                    <div class="feature-item"><i class="fas fa-edit"></i><br>Mock Tests</div>
                    <div class="feature-item"><i class="fas fa-video"></i><br>Video Classes</div>
                    <div class="feature-item"><i class="fas fa-newspaper"></i><br>Daily News</div>
                </div>
                <a href="/logout"><button class="btn" style="background:#ff3b30; margin-top:20px;">Logout</button></a>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT, logged_in=session.get('user'))

@app.route('/auth', methods=['POST'])
def auth():
    email = request.form.get('email')
    password = request.form.get('password')
    action = request.form.get('action')
    
    if action == 'reg':
        users[email] = password
        session['user'] = email
        return redirect(url_for('home'))
    else:
        if email in users and users[email] == password:
            session['user'] = email
            return redirect(url_for('home'))
        return "Invalid Credentials! <a href='/'>Try again</a>"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
