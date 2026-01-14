import os
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "karkacloud_mega_loaded_2026"

# --- INTERNAL DATABASE (Raw Content Integrated) ---
STUDY_MATERIALS = {
    "Unit 1: Science": "Physics: Nature of Universe, Mechanics. Chemistry: Acids, Bases, Salts. Biology: Nutrition & Health, Human Diseases.",
    "Unit 4: History": "Indus Valley Civilization, Guptas, Delhi Sultans, Mughals, Marathas, and the South Indian History.",
    "Unit 5: Polity": "Constitution of India, Preamble, Fundamental Rights, Fundamental Duties, Parliament, and Judiciary.",
    "Unit 8: TN Culture": "History of Tamil Society, Archaeological discoveries, Tamil Literature from Sangam age to contemporary times.",
    "Unit 9: TN Admin": "Human Development Indicators in TN, Social Justice, and Welfare schemes of the Tamil Nadu Government."
}

MATHS_TRICKS = [
    {"topic": "Percentage", "trick": "To find x% of y, calculate (x*y)/100. Shortcut: 25% means divide by 4, 50% means divide by 2."},
    {"topic": "Profit & Loss", "trick": "Profit = SP - CP. Shortcut: If 2 items sold at same price, one at x% profit and other at x% loss, overall loss = (x/100)^2."},
    {"topic": "Time & Work", "trick": "If A does work in x days and B in y days, together they do it in (x*y)/(x+y) days."}
]

QUIZ_DATA = [
    {"q": "1. Who is the author of 'Thirukkural'?", "o": ["Kambar", "Thiruvalluvar", "Avvaiyar", "Bharathiyar"], "a": "Thiruvalluvar"},
    {"q": "2. Which state has the longest coastline in India?", "o": ["Tamil Nadu", "Gujarat", "Andhra Pradesh", "Kerala"], "a": "Gujarat"},
    {"q": "3. Article 17 deals with?", "o": ["Equality", "Untouchability", "Education", "Freedom"], "a": "Untouchability"},
    {"q": "4. First session of INC held at?", "o": ["Madras", "Bombay", "Delhi", "Calcutta"], "a": "Bombay"},
    {"q": "5. Highest peak in South India?", "o": ["Doddabetta", "Anamudi", "Mahendragiri", "Kodaikanal"], "a": "Anamudi"}
]

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --primary: #6366f1; --red: #ff0000; --bg: #f8fafc; --dark: #1e293b; --gold: #f59e0b; }
        body { font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; background: var(--bg); overflow-x: hidden; }
        
        /* 24/7 Red Live News Ticker */
        .news-header { background: var(--red); color: white; padding: 12px 0; font-weight: 800; position: sticky; top: 0; z-index: 2000; border-bottom: 2px solid white; }
        .ticker { display: inline-block; white-space: nowrap; animation: move 35s linear infinite; padding-left: 100%; }
        @keyframes move { 0% { transform: translateX(0); } 100% { transform: translateX(-180%); } }

        .nav { background: white; margin: 10px 15px; padding: 15px; border-radius: 15px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); position: sticky; top: 50px; z-index: 1000; }
        .banner { background: linear-gradient(135deg, #a855f7, #6366f1); color: white; padding: 30px; border-radius: 25px; margin: 15px; position: relative; }
        .admin-badge { position: absolute; top: 10px; right: 10px; background: var(--gold); color: white; padding: 5px 12px; border-radius: 10px; font-size: 0.7rem; font-weight: 800; }

        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; padding: 15px; }
        .card { background: white; padding: 25px; border-radius: 22px; text-align: center; text-decoration: none; color: inherit; border: 1.5px solid #eee; position: relative; box-shadow: 0 5px 15px rgba(0,0,0,0.02); }
        .pro-badge { position: absolute; top: 8px; left: 8px; background: var(--gold); color: white; font-size: 0.6rem; padding: 2px 6px; border-radius: 5px; font-weight: 800; }

        .btn { background: var(--primary); color: white; border: none; padding: 18px; border-radius: 15px; font-weight: 800; cursor: pointer; width: 100%; margin-top: 10px; }
        .option { display: block; background: #f8fafc; padding: 16px; margin: 10px 0; border-radius: 15px; border: 1.5px solid #eee; cursor: pointer; text-align: left; font-weight: 600; }
        .content-area { background: white; padding: 25px; border-radius: 20px; border: 1.5px solid #ddd; margin-top: 15px; line-height: 1.7; }
    </style>
</head>
<body>
    {% if not user_name %}
    <div style="height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:30px; text-align:center;">
        <h1 style="color:var(--primary); font-weight: 800;">KARKA CLOUD PRO</h1>
        <form method="POST" action="/auth" style="width:100%; max-width:340px;">
            <input type="text" name="name" placeholder="Full Name" required style="width:100%; padding:18px; margin-bottom:12px; border-radius:15px; border:1px solid #ddd; box-sizing:border-box;">
            <input type="email" name="email" placeholder="Gmail ID" required style="width:100%; padding:18px; margin-bottom:12px; border-radius:15px; border:1px solid #ddd; box-sizing:border-box;">
            <button type="submit" class="btn">Login to Dashboard 🚀</button>
        </form>
    </div>
    {% else %}
    <div class="news-header"><div class="ticker">📢 LIVE NEWS: TNPSC Annual Planner 2026 Announcement Soon! | All Unit Premium Materials Loaded | Maths Tricks Active | No Server Blocks! | Success Stories Shared!</div></div>
    
    <div class="nav"><b>KARKA CLOUD</b><div>Hi, {{ user_name }}!</div></div>
    
    <div class="banner">
        {% if is_admin %} <div class="admin-badge">ADMIN UNLOCKED</div> {% endif %}
        <h2>Premium Dashboard</h2>
        <p>Direct internal access to all TNPSC materials.</p>
    </div>

    <div class="grid">
        <a href="/materials" class="card"><i class="fas fa-book" style="color:#2563eb; font-size: 1.5rem; margin-bottom:10px;"></i><h4>Study Materials</h4></a>
        <a href="/mock-test" class="card"><i class="fas fa-edit" style="color:#16a34a; font-size: 1.5rem; margin-bottom:10px;"></i><h4>25 Qn Quiz</h4></a>
        <a href="/maths" class="card"><div class="pro-badge">PRO</div><i class="fas fa-calculator" style="color:var(--gold); font-size: 1.5rem; margin-bottom:10px;"></i><h4>Maths Hacks</h4></a>
        <a href="/qbank" class="card"><div class="pro-badge">PRO</div><i class="fas fa-database" style="color:#6366f1; font-size: 1.5rem; margin-bottom:10px;"></i><h4>Question Bank</h4></a>
    </div>

    <div style="text-align:center; padding: 40px;"><a href="/logout" style="color:red; font-weight:800; text-decoration:none;">Logout</a></div>
    {% endif %}

    {% if page == 'materials' %}
    <div style="position:fixed; inset:0; background:white; z-index:3000; padding:25px; overflow-y:auto;">
        <a href="/" style="font-weight:800; color:var(--primary); text-decoration:none;"><i class="fas fa-arrow-left"></i> BACK</a>
        <h2 style="margin-top:25px;">Master Study Units</h2>
        {% for unit, text in materials.items() %}
        <div class="content-area">
            <h3 style="color:var(--primary); margin-top:0;">{{ unit }}</h3>
            <p>{{ text }}</p>
            <button class="btn" style="padding:10px; width:auto; font-size:0.8rem;" onclick="window.print()">Download as PDF <i class="fas fa-download"></i></button>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    {% if page == 'maths' %}
    <div style="position:fixed; inset:0; background:white; z-index:3000; padding:25px; overflow-y:auto;">
        <a href="/" style="font-weight:800; color:var(--primary); text-decoration:none;"><i class="fas fa-arrow-left"></i> BACK</a>
        <h2 style="margin-top:25px;">Premium Maths Tricks</h2>
        {% for m in tricks %}
        <div style="background:#f8fafc; padding:20px; border-radius:15px; margin-bottom:15px; border:1px solid #eee;">
            <h4 style="color:var(--primary); margin:0;">{{ m.topic }}</h4>
            <p><b>Shortcut:</b> {{ m.trick }}</p>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    {% if page == 'mock' %}
    <div style="position:fixed; inset:0; background:white; z-index:3000; padding:25px; overflow-y:auto;">
        <div class="container" style="max-width:650px; margin:auto;">
            <a href="/reset-test" style="font-weight:800; color:#ef4444; text-decoration:none;"><i class="fas fa-times-circle"></i> EXIT</a>
            {% if q_idx < 5 %}
            <div style="margin-top:25px; background:#f8fafc; padding:35px; border-radius:30px; border:1.5px solid #ddd;">
                <p style="color:#64748b; font-weight:600;">Question {{ q_idx + 1 }} of 25</p>
                <p style="font-size:1.3rem; font-weight:800; margin:15px 0;">{{ question.q }}</p>
                <form method="POST" action="/submit-answer">
                    {% for opt in question.o %}
                    <label class="option"><input type="radio" name="answer" value="{{ opt }}" required> {{ opt }}</label>
                    {% endfor %}
                    <button type="submit" class="btn">Next Question <i class="fas fa-arrow-right"></i></button>
                </form>
            </div>
            {% else %}
            <div style="text-align:center; padding:60px 20px; background:#f0fdf4; border-radius:30px; margin-top:50px;">
                <h2 style="color:#16a34a;">Quiz Completed Successfully!</h2>
                <p style="font-size:3rem; font-weight:800;">{{ score }} / 5</p>
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
    is_admin = session.get('email') == "manojmano821-5@okicici"
    return render_template_string(HTML_LAYOUT, user_name=session.get('user_name'), is_admin=is_admin)

@app.route('/materials')
def materials():
    return render_template_string(HTML_LAYOUT, user_name=session.get('user_name'), page='materials', materials=STUDY_MATERIALS)

@app.route('/maths')
def maths():
    return render_template_string(HTML_LAYOUT, user_name=session.get('user_name'), page='maths', tricks=MATHS_TRICKS)

@app.route('/mock-test')
def mock_test():
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
    session['user_name'] = request.form.get('name')
    session['email'] = request.form.get('email')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear(); return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
