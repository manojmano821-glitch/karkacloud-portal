import os
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "karkacloud_ultra_integrated_2026"

# Database
users_db = {}

# 25-Question Free Mock Test
FREE_QUIZ = [
    {"q": "The first session of INC was held at?", "o": ["Bombay", "Madras", "Delhi", "Calcutta"], "a": "Bombay"},
    {"q": "Who is the 'Prophet of South India'?", "o": ["Periyar", "Rajaji", "Kamaraj", "Anna"], "a": "Periyar"},
    {"q": "Which Article deals with Abolition of Untouchability?", "o": ["Article 14", "Article 15", "Article 16", "Article 17"], "a": "Article 17"}
]

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Karka Cloud | Full Premium Portal</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --primary: #6366f1; --accent: #f59e0b; --bg: #f8fafc; --dark: #1e293b; --red: #ff0000; }
        body { font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; background: var(--bg); overflow-x: hidden; }
        
        /* 24/7 LIVE INDIA NEWS TICKER */
        .live-news-bar { background: var(--red); color: white; padding: 12px 0; font-weight: 800; font-size: 0.85rem; position: sticky; top: 0; z-index: 2000; border-bottom: 2px solid #fff; }
        .ticker-wrap { width: 100%; overflow: hidden; white-space: nowrap; }
        .ticker-items { display: inline-block; animation: ticker 35s linear infinite; padding-left: 100%; }
        @keyframes ticker { 0% { transform: translateX(0); } 100% { transform: translateX(-100%); } }

        .nav { background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); margin: 10px 15px; padding: 15px; border-radius: 20px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 45px; z-index: 1000; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
        .logo { font-size: 1.3rem; font-weight: 800; color: #334155; text-decoration: none; }
        .logo span { color: var(--accent); }

        .banner { background: linear-gradient(135deg, #a855f7, #6366f1); color: white; padding: 35px 25px; border-radius: 25px; margin: 15px; box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3); }
        .container { padding: 0 15px 40px; max-width: 1050px; margin: auto; }
        
        .section-title { margin: 25px 10px 10px; font-size: 0.9rem; font-weight: 800; text-transform: uppercase; color: #64748b; border-left: 4px solid var(--primary); padding-left: 10px; }
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }
        .card { background: white; padding: 25px; border-radius: 22px; text-align: center; box-shadow: 0 8px 15px rgba(0,0,0,0.03); border: 1px solid rgba(255,255,255,0.8); position: relative; text-decoration: none; color: inherit; }
        .lock-icon { position: absolute; top: 10px; right: 10px; color: #cbd5e1; font-size: 0.9rem; }

        .pay-box { background: var(--dark); color: white; padding: 40px 25px; border-radius: 35px; margin: 40px auto; text-align: center; border: 4px solid #334155; }
        .qr-img { width: 220px; border-radius: 20px; border: 6px solid white; margin: 15px 0; }
        
        /* Quiz & PDF Viewer */
        .option { display: block; width: 100%; padding: 15px; margin: 10px 0; border-radius: 12px; border: 1.5px solid #e2e8f0; background: #f8fafc; text-align: left; cursor: pointer; }
        .pdf-frame { height: 75vh; border-radius: 20px; overflow: hidden; border: 2px solid #ddd; margin-top: 15px; }
    </style>
</head>
<body>

    {% if not user_name %}
    <div style="height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; background:#fff; padding:30px; text-align:center;">
        <h1 style="color:var(--primary); font-weight:800;">KARKA CLOUD</h1>
        <form method="POST" action="/auth" style="width:100%; max-width:340px;">
            <input type="text" name="name" placeholder="Full Name" required style="width:100%; padding:18px; margin-bottom:12px; border-radius:18px; border:1.5px solid #e2e8f0; box-sizing:border-box;">
            <input type="email" name="email" placeholder="Gmail ID" required style="width:100%; padding:18px; margin-bottom:12px; border-radius:18px; border:1.5px solid #e2e8f0; box-sizing:border-box;">
            <input type="password" name="pwd" placeholder="Password" required style="width:100%; padding:18px; margin-bottom:12px; border-radius:18px; border:1.5px solid #e2e8f0; box-sizing:border-box;">
            <button type="submit" name="act" value="reg" style="width:100%; padding:18px; background:var(--primary); color:white; border:none; border-radius:18px; font-weight:800; cursor:pointer;">Register & Enter</button>
        </form>
    </div>
    {% else %}

    <div class="live-news-bar">
        <div class="ticker-wrap"><div class="ticker-items">Breaking News: TNPSC Group 2 Result Expected Soon | New Premium Weekly Mock Test Live Now | Download Unit 8 & 9 Study Materials Internally | India's GDP Forecast hits 7.5% for 2026.</div></div>
    </div>

    <div class="nav">
        <a href="/" class="logo">K <span>KARKA</span></a>
        <div style="font-weight:800; font-size:0.8rem; color:#64748b;">Hi, {{ user_name }}!</div>
    </div>

    <div class="banner">
        <h1>Welcome, {{ user_name }}!</h1>
        <p>Goal: TNPSC 2026 Officer. <br>Your Dashboard is Fully Loaded!</p>
    </div>

    <div class="container">
        <div class="section-title">Free Resources</div>
        <div class="grid">
            <a href="/free-pdfs" class="card"><i class="fas fa-file-pdf" style="color:#2563eb; font-size:1.5rem;"></i><h4>Free PDFs</h4><span>3 Sample Units</span></a>
            <a href="/mock-test" class="card"><i class="fas fa-edit" style="color:#16a34a; font-size:1.5rem;"></i><h4>Free Quiz</h4><span>25 Qns / Analysis</span></a>
        </div>

        <div class="section-title">Premium Access (Locked)</div>
        <div class="grid">
            <div class="card"><i class="fas fa-lock lock-icon"></i><i class="fas fa-crown" style="color:var(--accent); font-size:1.5rem;"></i><h4>Premium PDFs</h4><span>5yrs All Materials</span></div>
            <div class="card"><i class="fas fa-lock lock-icon"></i><i class="fas fa-stopwatch" style="color:#ef4444; font-size:1.5rem;"></i><h4>Weekly Mock</h4><span>Real Exam Mode</span></div>
            <div class="card"><i class="fas fa-lock lock-icon"></i><i class="fas fa-database" style="color:var(--primary); font-size:1.5rem;"></i><h4>5yr Q-Bank</h4><span>All Solved Papers</span></div>
            <div class="card"><i class="fas fa-lock lock-icon"></i><i class="fas fa-bolt" style="color:#facc15; font-size:1.5rem;"></i><h4>Maths Tricks</h4><span>1000+ Shortcuts</span></div>
        </div>

        <div class="pay-box">
            <h2 style="color:var(--accent); margin:0;">Unlock Premium Portal</h2>
            <img src="https://res.cloudinary.com/dxfq3iotg/image/upload/v1736854744/manojqr.jpg" class="qr-img">
            <p style="font-weight:800;">UPI ID: manojmano821-5@okicici</p>
            <button style="background:var(--accent); color:white; border:none; padding:15px 40px; border-radius:15px; font-weight:800; cursor:pointer;">I HAVE PAID ₹499 ✅</button>
        </div>

        <div style="text-align:center; margin-top:20px; padding-bottom:40px;"><a href="/logout" style="color:#ef4444; font-weight:800; text-decoration:none; font-size:0.8rem;">Logout Account</a></div>
    </div>
    {% endif %}

    {% if page == 'free_pdfs' %}
    <div style="position:fixed; inset:0; background:white; z-index:3000; overflow-y:auto; padding:25px;">
        <a href="/" style="font-weight:800; color:var(--primary); text-decoration:none;"><i class="fas fa-arrow-left"></i> BACK</a>
        <h2 style="margin-top:20px;">Internal PDF Viewer</h2>
        <div class="pdf-frame"><iframe src="https://www.tnpsc.gov.in/static_pdf/syllabus/General_Tamil.pdf#toolbar=0"></iframe></div>
    </div>
    {% endif %}

    {% if page == 'mock' %}
    <div style="position:fixed; inset:0; background:white; z-index:3000; overflow-y:auto; padding:25px;">
        <a href="/reset-test" style="font-weight:800; color:#ef4444; text-decoration:none;"><i class="fas fa-times-circle"></i> EXIT</a>
        {% if q_idx < 3 %}
        <div style="margin-top:30px; background:#f8fafc; padding:30px; border-radius:30px; border:1px solid #ddd;">
            <p style="font-size:1.1rem; font-weight:800;">Question {{ q_idx + 1 }}: {{ question.q }}</p>
            <form method="POST" action="/submit-answer">
                {% for opt in question.options %}
                <button type="submit" name="answer" value="{{ opt }}" class="option">{{ opt }}</button>
                {% endfor %}
            </form>
        </div>
        {% else %}
        <div style="text-align:center; padding:50px; background:#f0fdf4; border-radius:30px; margin-top:50px;">
            <h2>Quiz Analysis Completed!</h2>
            <p style="font-size:2rem; font-weight:800;">Score: {{ score }} / 3</p>
            <a href="/reset-test" style="display:inline-block; padding:15px 40px; background:var(--dark); color:white; border-radius:15px; text-decoration:none; font-weight:800;">Back to Dashboard</a>
        </div>
        {% endif %}
    </div>
    {% endif %}

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT, user_name=session.get('user_name'))

@app.route('/free-pdfs')
def free_pdfs():
    if not session.get('user_name'): return redirect(url_for('home'))
    return render_template_string(HTML_LAYOUT, user_name=session.get('user_name'), page='free_pdfs')

@app.route('/mock-test')
def mock_test():
    if not session.get('user_name'): return redirect(url_for('home'))
    if 'q_idx' not in session: session['q_idx'], session['score'] = 0, 0
    idx = session['q_idx']
    q = FREE_QUIZ[idx] if idx < 3 else None
    return render_template_string(HTML_LAYOUT, user_name=session.get('user_name'), page='mock', question=q, q_idx=idx, score=session['score'])

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    ans, idx = request.form.get('answer'), session.get('q_idx', 0)
    if ans == FREE_QUIZ[idx]['a']: session['score'] += 1
    session['q_idx'] += 1
    return redirect(url_for('mock_test'))

@app.route('/reset-test')
def reset_test():
    session.pop('q_idx', None); session.pop('score', None); return redirect(url_for('home'))

@app.route('/auth', methods=['POST'])
def auth():
    email, pwd, name, act = request.form.get('email'), request.form.get('pwd'), request.form.get('name'), request.form.get('act')
    if act == 'reg':
        users_db[email] = {"pwd": pwd, "name": name}
        session['user_name'] = name
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear(); return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
