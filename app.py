import os
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "karkacloud_internal_view_2026"

# Internal Database
users_db = {}

# Professional TNPSC Questions (4 Options - Result Logic)
QUIZ_DB = [
    {"q": "1. The first session of the Indian National Congress was held at?", "o": ["Bombay", "Madras", "Calcutta", "Delhi"], "a": "Bombay"},
    {"q": "2. Who was the founder of the Self-Respect Movement?", "o": ["C.N. Annadurai", "E.V. Ramasamy", "M. Karunanidhi", "K. Kamaraj"], "a": "E.V. Ramasamy"},
    {"q": "3. Which Article deals with the Abolition of Untouchability?", "o": ["Article 14", "Article 15", "Article 16", "Article 17"], "a": "Article 17"},
    {"q": "4. The state tree of Tamil Nadu is?", "o": ["Neem Tree", "Banyan Tree", "Palm Tree", "Teak Tree"], "a": "Palm Tree"},
    {"q": "5. Who is the author of 'Thirukkural'?", "o": ["Kambar", "Thiruvalluvar", "Ilango Adigal", "Bharathiyar"], "a": "Thiruvalluvar"}
]

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Karka Cloud | Internal Learning Portal</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --primary: #6366f1; --accent: #f59e0b; --bg: #f8fafc; --dark: #1e293b; }
        body { font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; background: var(--bg); overflow-x: hidden; }
        
        .ticker { background: var(--dark); color: var(--accent); padding: 12px; font-weight: 800; font-size: 0.85rem; position: sticky; top: 0; z-index: 1100; border-bottom: 2px solid var(--accent); }
        .ticker-move { white-space: nowrap; animation: marquee 30s linear infinite; display: inline-block; padding-left: 100%; }
        @keyframes marquee { 0% { transform: translateX(0); } 100% { transform: translateX(-100%); } }

        .nav { background: rgba(255,255,255,0.85); backdrop-filter: blur(10px); margin: 10px auto; padding: 15px 25px; border-radius: 20px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 55px; z-index: 1000; box-shadow: 0 4px 20px rgba(0,0,0,0.05); max-width: 1000px; width: 90%; }
        .logo { font-size: 1.4rem; font-weight: 800; color: #334155; text-decoration: none; }
        .logo span { color: var(--accent); }

        .banner { background: linear-gradient(135deg, #a855f7, #6366f1); color: white; padding: 40px 30px; border-radius: 30px; margin: 20px auto; max-width: 1000px; width: 90%; box-shadow: 0 10px 30px rgba(99, 102, 241, 0.25); }
        .container { padding: 0 15px 40px; max-width: 1050px; margin: auto; }
        
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; }
        .card { background: white; padding: 25px; border-radius: 24px; text-decoration: none; color: inherit; box-shadow: 0 8px 15px rgba(0,0,0,0.03); display: flex; flex-direction: column; align-items: center; text-align: center; border: 1px solid rgba(255,255,255,0.8); transition: 0.3s; position: relative; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0,0,0,0.08); }
        
        /* Internal Viewer Style */
        .viewer-container { height: 80vh; border-radius: 20px; overflow: hidden; border: 2px solid #e2e8f0; }
        iframe { width: 100%; height: 100%; border: none; }

        .option { display: block; width: 100%; padding: 15px; margin: 10px 0; border-radius: 15px; border: 1.5px solid #e2e8f0; background: #f8fafc; text-align: left; cursor: pointer; font-size: 0.95rem; }
        .option:hover { border-color: var(--primary); background: #f5f3ff; }

        .pay-box { background: var(--dark); color: white; padding: 40px 25px; border-radius: 35px; margin: 40px auto; text-align: center; max-width: 500px; border: 5px solid #334155; }
        .qr-img { width: 100%; max-width: 220px; border-radius: 20px; border: 6px solid white; margin: 15px 0; }
    </style>
</head>
<body>

    {% if not user_name %}
    <div style="height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; background:#fff; padding:30px; text-align:center;">
        <div style="font-size: 2.5rem; font-weight: 800; color: var(--primary); margin-bottom: 10px;">KARKA</div>
        <p style="color:#64748b; margin-bottom:30px;">Your All-in-One TNPSC Academy</p>
        <form method="POST" action="/auth" style="width:100%; max-width:340px;">
            <input type="text" name="name" placeholder="Full Name" required style="width:100%; padding:18px; margin-bottom:12px; border-radius:18px; border:1.5px solid #e2e8f0; box-sizing:border-box; background:#f8fafc;">
            <input type="email" name="email" placeholder="Gmail ID" required style="width:100%; padding:18px; margin-bottom:12px; border-radius:18px; border:1.5px solid #e2e8f0; box-sizing:border-box; background:#f8fafc;">
            <input type="password" name="pwd" placeholder="Password" required style="width:100%; padding:18px; margin-bottom:12px; border-radius:18px; border:1.5px solid #e2e8f0; box-sizing:border-box; background:#f8fafc;">
            <button type="submit" name="act" value="reg" style="width:100%; padding:18px; background:var(--primary); color:white; border:none; border-radius:18px; font-weight:800; cursor:pointer;">Launch My Career 🚀</button>
        </form>
    </div>
    {% else %}

    <div class="ticker">
        <div class="ticker-move">📢 24/7 LIVE UPDATES: TNPSC Group 4 Result Announcement Soon! | New Current Affairs Jan 2026 PDF Live! | Start Your Internal Mock Test Now!</div>
    </div>

    <div class="nav">
        <a href="/" class="logo">K <span>KARKA</span></a>
        <div style="font-weight:800; color:#64748b;"><i class="fas fa-user-circle"></i> {{ user_name }}</div>
    </div>

    <div class="banner">
        <h1>Welcome, {{ user_name }}!</h1>
        <p>Goal: TNPSC 2026 Officer. <br>Access all materials internally.</p>
    </div>

    <div class="container">
        <h3 style="margin: 30px 10px 15px;">FREE ACCESS (INTERNAL)</h3>
        <div class="grid">
            <a href="/free-pdfs" class="card"><i class="fas fa-file-pdf" style="font-size:2rem; color:#2563eb; margin-bottom:10px;"></i><h4>Sample PDFs</h4><span>View in Website</span></a>
            <a href="/mock-test" class="card"><i class="fas fa-edit" style="font-size:2rem; color:#16a34a; margin-bottom:10px;"></i><h4>Mock Quiz</h4><span>25 Questions Live</span></a>
        </div>

        <h3 style="margin: 40px 10px 15px;">PREMIUM (LOCKED)</h3>
        <div class="grid">
            <div class="card"><i class="fas fa-lock" style="position:absolute; top:15px; right:15px; color:#cbd5e1;"></i><i class="fas fa-bolt" style="font-size:2rem; color:var(--accent); margin-bottom:10px;"></i><h4>Maths Hacks</h4><span>1000+ Internal Tricks</span></div>
            <div class="card"><i class="fas fa-lock" style="position:absolute; top:15px; right:15px; color:#cbd5e1;"></i><i class="fas fa-database" style="font-size:2rem; color:var(--primary); margin-bottom:10px;"></i><h4>Question Bank</h4><span>5yrs All Papers</span></div>
        </div>

        <div class="pay-box">
            <h2 style="color:var(--accent); margin:0;">Unlock Premium Now</h2>
            <img src="https://res.cloudinary.com/dxfq3iotg/image/upload/v1736854744/manojqr.jpg" class="qr-img">
            <p style="font-weight:800;">UPI ID: manojmano821-5@okicici</p>
            <button style="background:var(--accent); color:white; border:none; padding:15px 40px; border-radius:15px; font-weight:800; cursor:pointer;">I HAVE PAID ₹499 ✅</button>
        </div>

        <footer style="background:white; padding:40px; border-top:1px solid #eee; margin-top:50px;">
            <h4>About Karka Cloud</h4>
            <p style="color:#64748b; font-size:0.9rem;">India's Leading Internal Learning Portal for TNPSC Aspirants. Dedicated to 100% Student Success.</p>
            <div style="margin-top:20px; font-size:0.8rem; font-weight:600;"><a href="/logout" style="color:#ef4444; text-decoration:none;">LOGOUT ACCOUNT</a></div>
        </footer>
    </div>
    {% endif %}

    {% if page == 'free_pdfs' %}
    <div style="position:fixed; inset:0; background:white; z-index:2000; overflow-y:auto; padding:25px;">
        <div class="container">
            <a href="/" style="font-weight:800; color:var(--primary); text-decoration:none;"><i class="fas fa-arrow-left"></i> BACK TO DASHBOARD</a>
            <h2 style="margin-top:25px;">Internal Material Viewer</h2>
            <p style="color:#64748b; font-size:0.85rem;">The following materials are viewed internally via Karka Cloud Secure Player.</p>
            <div class="viewer-container">
                <iframe src="https://www.tnpsc.gov.in/static_pdf/syllabus/G4_Syllabus_2022.pdf#toolbar=0"></iframe>
            </div>
            <p style="text-align:center; color:#ef4444; font-size:0.75rem; margin-top:20px; font-weight:800;">⚠️ SHARING PROHIBITED. INTERNAL USE ONLY.</p>
        </div>
    </div>
    {% endif %}

    {% if page == 'mock' %}
    <div style="position:fixed; inset:0; background:white; z-index:2000; overflow-y:auto; padding:25px;">
        <div class="container" style="max-width:650px;">
            <a href="/reset-test" style="font-weight:800; color:#ef4444; text-decoration:none;"><i class="fas fa-times-circle"></i> EXIT TEST</a>
            {% if q_idx < 5 %}
            <div style="margin-top:25px; background:#f8fafc; padding:35px; border-radius:30px; border:2px solid #eee; box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);">
                <p style="color:#64748b; font-weight:600;">Question {{ q_idx + 1 }} of 25</p>
                <p style="font-size:1.2rem; font-weight:800; margin:15px 0;">{{ question.q }}</p>
                <form method="POST" action="/submit-answer">
                    {% for opt in question.options %}
                    <button type="submit" name="answer" value="{{ opt }}" class="option">{{ opt }}</button>
                    {% endfor %}
                </form>
            </div>
            {% else %}
            <div style="text-align:center; padding:60px 20px; background:#f0fdf4; border-radius:30px; margin-top:50px;">
                <h2 style="color:#16a34a;">Quiz Analysis Completed!</h2>
                <p style="font-size:2rem; font-weight:800;">Score: {{ score }} / 5</p>
                <p style="color:#64748b; margin:20px 0;">Detailed performance report generated internally.</p>
                <a href="/reset-test" style="display:inline-block; padding:18px 45px; background:var(--dark); color:white; border-radius:15px; text-decoration:none; font-weight:800;">BACK TO DASHBOARD</a>
            </div>
            {% endif %}
        </div>
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
    q = QUIZ_DB[idx] if idx < 5 else None
    return render_template_string(HTML_LAYOUT, user_name=session.get('user_name'), page='mock', question=q, q_idx=idx, score=session['score'])

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    ans, idx = request.form.get('answer'), session.get('q_idx', 0)
    if ans == QUIZ_DB[idx]['a']: session['score'] += 1
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
