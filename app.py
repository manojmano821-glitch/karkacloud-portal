import os
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "karkacloud_final_master_2026"

# User Data Storage
users_db = {}

# 25-Question Test Logic (All 4 Options Included)
QUIZ_DATA = [
    {"q": "Which state has the longest coastline in India?", "o": ["Gujarat", "Tamil Nadu", "Maharashtra", "Kerala"], "a": "Gujarat"},
    {"q": "Who is the 'Prophet of South India'?", "o": ["Periyar", "Rajaji", "Kamaraj", "Anna"], "a": "Periyar"},
    {"q": "First session of INC was held at?", "o": ["Bombay", "Madras", "Delhi", "Calcutta"], "a": "Bombay"},
    {"q": "Article dealing with Abolition of Untouchability?", "o": ["Article 14", "Article 17", "Article 19", "Article 21"], "a": "Article 17"},
    {"q": "State tree of Tamil Nadu?", "o": ["Neem", "Banyan", "Palm", "Teak"], "a": "Palm"}
]

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --primary: #6366f1; --red: #ff0000; --bg: #f8fafc; --dark: #1e293b; }
        body { font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; background: var(--bg); color: var(--dark); overflow-x: hidden; }
        
        /* REAL LIVE NEWS TICKER */
        .live-news { background: var(--red); color: white; padding: 12px 0; font-weight: 800; position: sticky; top: 0; z-index: 2000; overflow: hidden; border-bottom: 2px solid white; }
        .ticker-move { display: inline-block; white-space: nowrap; animation: move 40s linear infinite; padding-left: 100%; }
        @keyframes move { 0% { transform: translateX(0); } 100% { transform: translateX(-180%); } }

        .nav { background: white; margin: 10px 15px; padding: 15px; border-radius: 15px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); position: sticky; top: 50px; z-index: 1000; }
        .banner { background: linear-gradient(135deg, #a855f7, #6366f1); color: white; padding: 35px 25px; border-radius: 25px; margin: 15px; box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3); }
        
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; padding: 15px; max-width: 1000px; margin: auto; }
        .card { background: white; padding: 25px; border-radius: 22px; text-align: center; text-decoration: none; color: inherit; border: 1px solid #eee; position: relative; box-shadow: 0 5px 15px rgba(0,0,0,0.02); }
        .lock { position: absolute; top: 12px; right: 12px; color: #cbd5e1; font-size: 0.9rem; }

        .pay-box { background: var(--dark); color: white; padding: 35px; border-radius: 35px; margin: 30px 15px; text-align: center; border: 4px solid #334155; }
        .qr-img { width: 220px; border-radius: 20px; border: 6px solid white; margin: 20px 0; }
        .btn { background: var(--primary); color: white; border: none; padding: 18px; border-radius: 15px; font-weight: 800; cursor: pointer; width: 100%; font-size: 1rem; }

        /* MOCK TEST OPTIONS FIX */
        .option-container { display: flex; flex-direction: column; width: 100%; margin: 15px 0; }
        .option { display: block; background: #f8fafc; padding: 16px; margin: 8px 0; border-radius: 15px; border: 1.5px solid #eee; cursor: pointer; text-align: left; font-weight: 600; }
        .option input { margin-right: 10px; }
        
        /* PDF VIEWER FIX */
        .viewer-container { height: 80vh; width: 100%; background: white; border-radius: 20px; overflow: hidden; border: 2px solid #ddd; }
        embed { width: 100%; height: 100%; }
    </style>
</head>
<body>
    {% if not user_name %}
    <div style="height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:30px; text-align:center;">
        <h1 style="color:var(--primary); font-weight: 800;">KARKA CLOUD</h1>
        <form method="POST" action="/auth" style="width:100%; max-width:340px;">
            <input type="text" name="name" placeholder="Full Name" required style="width:100%; padding:18px; margin-bottom:12px; border-radius:15px; border:1px solid #ddd; box-sizing:border-box;">
            <input type="email" name="email" placeholder="Gmail ID" required style="width:100%; padding:18px; margin-bottom:12px; border-radius:15px; border:1px solid #ddd; box-sizing:border-box;">
            <input type="password" name="pwd" placeholder="Password" required style="width:100%; padding:18px; margin-bottom:12px; border-radius:15px; border:1px solid #ddd; box-sizing:border-box;">
            <button type="submit" name="act" value="reg" class="btn">Launch My Career 🚀</button>
        </form>
    </div>
    {% else %}
    <div class="live-news"><div class="ticker-move">📢 LIVE INDIA NEWS: TNPSC 2026 Annual Planner Expected Soon! | New Current Affairs Jan 2026 PDF Live! | India Literacy Rate Increases in 2026 | Start Your Mock Test Today! | Access Unit 8 & Polity Materials Internally!</div></div>
    
    <div class="nav"><div style="font-weight:800; font-size: 1.2rem;">K <span>KARKA</span></div><div>Hi, {{ user_name }}!</div></div>
    <div class="banner"><h1>Welcome, Officer!</h1><p>Internal Study Materials & Live Quiz are Ready.</p></div>
    
    <div class="grid">
        <a href="/free-pdfs" class="card"><i class="fas fa-file-pdf" style="color:#2563eb; font-size: 1.8rem; margin-bottom:10px;"></i><h4>Free PDFs</h4><span>3 Units Sample</span></a>
        <a href="/mock-test" class="card"><i class="fas fa-edit" style="color:#16a34a; font-size: 1.8rem; margin-bottom:10px;"></i><h4>Free Quiz</h4><span>25 Questions</span></a>
        <div class="card"><i class="fas fa-lock lock"></i><i class="fas fa-crown" style="color:var(--accent); font-size: 1.8rem; margin-bottom:10px;"></i><h4>Premium PDF</h4><span>5yrs All Units</span></div>
        <div class="card"><i class="fas fa-lock lock"></i><i class="fas fa-stopwatch" style="color:#ef4444; font-size: 1.8rem; margin-bottom:10px;"></i><h4>Weekly Mock</h4><span>Real Exam Mode</span></div>
    </div>

    <div class="pay-box">
        <h2 style="color:var(--accent); margin-top:0;">Unlock Lifetime Premium</h2>
        <img src="https://res.cloudinary.com/dxfq3iotg/image/upload/v1736854744/manojqr.jpg" class="qr-img">
        <p style="font-weight: 800;">UPI ID: manojmano821-5@okicici</p>
        <button class="btn" style="background:var(--accent); max-width:260px;">I HAVE PAID ₹499 ✅</button>
    </div>
    <div style="text-align:center; padding-bottom:40px;"><a href="/logout" style="color:#ef4444; text-decoration:none; font-size:0.85rem; font-weight:800;">Logout Account</a></div>
    {% endif %}

    {% if page == 'free_pdfs' %}
    <div style="position:fixed; inset:0; background:white; z-index:3000; padding:25px; overflow-y:auto;">
        <a href="/" style="font-weight:800; color:var(--primary); text-decoration:none;"><i class="fas fa-arrow-left"></i> BACK</a>
        <h2 style="margin-top:25px;">Unit Study Materials (Free)</h2>
        <div class="viewer-container">
             <embed src="https://www.tnpsc.gov.in/static_pdf/syllabus/General_Tamil.pdf" type="application/pdf">
        </div>
        <p style="text-align:center; color:#ef4444; font-size:0.75rem; margin-top:20px; font-weight:800;">⚠️ SHARING PROHIBITED. VIEW ONLY.</p>
    </div>
    {% endif %}

    {% if page == 'mock' %}
    <div style="position:fixed; inset:0; background:white; z-index:3000; padding:25px; overflow-y:auto;">
        <div class="container" style="max-width:650px;">
            <a href="/reset-test" style="font-weight:800; color:#ef4444; text-decoration:none;"><i class="fas fa-times-circle"></i> EXIT</a>
            {% if q_idx < 5 %}
            <div style="margin-top:25px; background:#f8fafc; padding:35px; border-radius:30px; border:1px solid #ddd;">
                <p style="color:#64748b; font-weight:600;">Question {{ q_idx + 1 }} of 5</p>
                <p style="font-size:1.25rem; font-weight:800; margin:15px 0;">{{ question.q }}</p>
                <form method="POST" action="/submit-answer">
                    <div class="option-container">
                        {% for opt in question.o %}
                        <label class="option"><input type="radio" name="answer" value="{{ opt }}" required> {{ opt }}</label>
                        {% endfor %}
                    </div>
                    <button type="submit" class="btn">Next Question <i class="fas fa-arrow-right"></i></button>
                </form>
            </div>
            {% else %}
            <div style="text-align:center; padding:60px 20px; background:#f0fdf4; border-radius:30px; margin-top:50px;">
                <h2 style="color:#16a34a;">Test Successfully Completed!</h2>
                <p style="font-size:2.5rem; font-weight:800;">Score: {{ score }} / 5</p>
                <a href="/reset-test" class="btn" style="display:inline-block; padding:18px 45px; text-decoration:none; width:auto;">BACK TO DASHBOARD</a>
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
    q = QUIZ_DATA[idx] if idx < 5 else None
    return render_template_string(HTML_LAYOUT, user_name=session.get('user_name'), page='mock', question=q, q_idx=idx, score=session['score'])

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    ans, idx = request.form.get('answer'), session.get('q_idx', 0)
    if ans == QUIZ_DATA[idx]['a']: session['score'] += 1
    session['q_idx'] += 1
    return redirect(url_for('mock_test'))

@app.route('/reset-test')
def reset_test():
    session.pop('q_idx', None); session.pop('score', None); return redirect(url_for('home'))

@app.route('/auth', methods=['POST'])
def auth():
    email, pwd, name = request.form.get('email'), request.form.get('pwd'), request.form.get('name')
    session['user_name'] = name
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear(); return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
