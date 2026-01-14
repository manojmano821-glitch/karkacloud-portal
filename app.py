import os
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "karkacloud_final_master_2026"

# Database: {email: {"pwd": pwd, "name": name}}
users_db = {}

# Detailed English Maths Tricks
TRICKS_DATA = [
    {"title": "Square Numbers Ending in 5", "desc": "Take the first digit, multiply by the next number, and append 25. Example: 35x35 = (3x4) and 25 = 1225."},
    {"title": "11x Multiplication Hack", "desc": "Add the two digits and place the sum in the middle. Example: 52x11 = 5 (5+2) 2 = 572."}
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
        :root { --primary: #6366f1; --accent: #f59e0b; --bg: #f8fafc; --dark: #1e293b; }
        body { font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; background: var(--bg); color: var(--dark); overflow-x: hidden; }
        
        .ticker { background: var(--dark); color: var(--accent); padding: 10px; font-weight: 800; font-size: 0.85rem; position: sticky; top: 0; z-index: 1100; border-bottom: 2px solid var(--accent); }
        .ticker-move { white-space: nowrap; animation: marquee 25s linear infinite; display: inline-block; padding-left: 100%; }
        @keyframes marquee { 0% { transform: translateX(0); } 100% { transform: translateX(-100%); } }

        .nav { background: rgba(255,255,255,0.85); backdrop-filter: blur(10px); margin: 10px 15px; padding: 12px 20px; border-radius: 20px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 45px; z-index: 1000; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
        .logo { font-size: 1.4rem; font-weight: 800; color: #334155; text-decoration: none; }
        .logo span { color: var(--accent); }

        .banner { background: linear-gradient(135deg, #a855f7, #6366f1); color: white; padding: 35px 25px; border-radius: 30px; margin: 15px; box-shadow: 0 15px 35px rgba(99, 102, 241, 0.25); }
        .banner h1 { margin: 0; font-size: 1.8rem; }

        .container { padding: 0 15px 40px; }
        .section-header { margin: 30px 10px 10px; font-size: 0.85rem; font-weight: 800; text-transform: uppercase; color: #64748b; letter-spacing: 1px; }
        
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }
        .card { background: white; padding: 22px; border-radius: 24px; text-decoration: none; color: inherit; box-shadow: 0 10px 20px rgba(0,0,0,0.02); display: flex; flex-direction: column; align-items: center; text-align: center; border: 1px solid rgba(255,255,255,0.7); transition: 0.3s; position: relative; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0,0,0,0.06); }
        
        .lock-icon { position: absolute; top: 12px; right: 12px; color: #94a3b8; font-size: 0.8rem; }
        .icon-box { width: 50px; height: 50px; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; margin-bottom: 12px; }
        .icon-gold { background: #fffbeb; color: #d97706; }
        .icon-blue { background: #eff6ff; color: #2563eb; }
        .icon-green { background: #f0fdf4; color: #16a34a; }

        .pay-box { background: var(--dark); color: white; padding: 35px 25px; border-radius: 30px; margin: 30px 15px; text-align: center; border: 4px solid #334155; }
        .qr-img { width: 220px; border-radius: 15px; margin: 20px 0; border: 5px solid white; }
        .btn-pay { background: var(--accent); color: white; border: none; padding: 16px; border-radius: 15px; font-weight: 800; cursor: pointer; width: 100%; max-width: 250px; margin-top: 10px; }

        footer { background: white; padding: 40px 25px; margin-top: 50px; border-top: 1px solid #e2e8f0; text-align: left; }
        footer h4 { margin-bottom: 10px; color: var(--primary); }
        footer p { font-size: 0.85rem; color: #64748b; line-height: 1.6; }
        .footer-links a { display: block; color: #1e293b; text-decoration: none; font-size: 0.85rem; margin-bottom: 8px; font-weight: 600; }
    </style>
</head>
<body>

    {% if not user_name %}
    <div style="height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; background:#fff; padding:30px;">
        <div style="font-size: 2.5rem; font-weight: 800; color: var(--primary); margin-bottom: 10px;">KARKA</div>
        <p style="color:#64748b; margin-bottom: 30px;">Digital Portal for TNPSC Success</p>
        <form method="POST" action="/auth" style="display:flex; flex-direction:column; width:100%; max-width:340px;">
            <input type="text" name="name" placeholder="Full Name" required style="padding:16px; margin-bottom:12px; border-radius:16px; border:1.5px solid #e2e8f0; background:#f8fafc; font-size:1rem;">
            <input type="email" name="email" placeholder="Gmail ID" required style="padding:16px; margin-bottom:12px; border-radius:16px; border:1.5px solid #e2e8f0; background:#f8fafc; font-size:1rem;">
            <input type="password" name="pwd" placeholder="Password" required style="padding:16px; margin-bottom:12px; border-radius:16px; border:1.5px solid #e2e8f0; background:#f8fafc; font-size:1rem;">
            <button type="submit" name="act" value="reg" style="padding:18px; background:var(--primary); color:white; border:none; border-radius:16px; font-weight:800; cursor:pointer; font-size:1rem; box-shadow:0 10px 20px rgba(99,102,241,0.2);">🚀 Launch My Career</button>
        </form>
    </div>
    {% else %}

    <div class="ticker">
        <div class="ticker-move">
            📢 LIVE UPDATES: TNPSC Group 4 Results 2026 Announcement Soon! | Current Affairs January 2026 PDF Released! | New Maths Tricks Added! | Start your Mock Test now!
        </div>
    </div>

    <div class="nav">
        <a href="/" class="logo">K <span>KARKA</span></a>
        <div style="font-weight:800; font-size:0.85rem; color:#64748b;"><i class="fas fa-user-circle"></i> {{ user_name }}</div>
    </div>

    <div class="banner">
        <h1>Vanakkam, {{ user_name }}!</h1>
        <p>Goal: TNPSC 2026. <br><b>3 New Free Materials Available!</b></p>
    </div>

    <div class="container">
        <div class="section-header">Free Resources</div>
        <div class="grid">
            <a href="/free-pdfs" class="card">
                <div class="icon-box icon-blue"><i class="fas fa-file-pdf"></i></div>
                <h4>Free PDFs</h4><span style="font-size:0.6rem;">3 Downloads Ready</span>
            </a>
            <a href="/mock-test" class="card">
                <div class="icon-box icon-green"><i class="fas fa-pen-nib"></i></div>
                <h4>Sample Test</h4><span style="font-size:0.6rem;">Check Progress</span>
            </a>
        </div>

        <div class="section-header">Premium Materials (Locked)</div>
        <div class="grid">
            <div class="card"><i class="fas fa-lock lock-icon"></i><div class="icon-box icon-gold"><i class="fas fa-calculator"></i></div><h4>Maths Tricks</h4><span style="font-size:0.6rem;">1000+ Premium Hacks</span></div>
            <div class="card"><i class="fas fa-lock lock-icon"></i><div class="icon-box icon-gold"><i class="fas fa-book-atlas"></i></div><h4>Q-Bank 5yrs</h4><span style="font-size:0.6rem;">Solved Papers</span></div>
        </div>

        <div class="pay-box">
            <h2 style="color:var(--accent); margin:0;">Unlock Lifetime Premium</h2>
            <p style="color:#94a3b8; font-size:0.9rem;">Scan the QR below to pay ₹499 via GPay/PhonePe</p>
            <img src="https://i.ibb.co/L6V2MhW/1000385502.jpg" alt="UPI QR" class="qr-img">
            <p style="font-weight:800;">UPI ID: manojmano821-5@okicici</p>
            <button class="btn-pay" onclick="alert('Once paid, send screenshot to admin for activation!')">I HAVE PAID ✅</button>
        </div>

        <footer>
            <h4>About Karka Cloud</h4>
            <p>Karka Cloud is a premium digital learning platform dedicated to TNPSC aspirants. We provide high-quality materials, shortcuts, and mock tests to help you clear exams in your first attempt.</p>
            
            <h4 style="margin-top:25px;">Quick Links</h4>
            <div class="footer-links">
                <a href="#">Career at Karka</a>
                <a href="#">Contact Us: admin@karkacloud.com</a>
                <a href="#">Terms & Conditions</a>
            </div>
            <p style="text-align:center; margin-top:30px; font-size:0.7rem;">© 2026 Karka Cloud | Designed for Excellence</p>
            <div style="text-align:center;"><a href="/logout" style="color:#94a3b8; font-size:0.8rem; text-decoration:none;">Logout Account</a></div>
        </footer>
    </div>
    {% endif %}

    {% if page == 'free_pdfs' %}
    <div style="position:fixed; inset:0; background:#fff; z-index:2000; overflow-y:auto; padding:25px;">
        <a href="/" style="font-weight:800; color:var(--primary); text-decoration:none;"><i class="fas fa-arrow-left"></i> BACK</a>
        <h2 style="margin-top:25px;">Free Study Materials</h2>
        <div class="grid">
            <div class="card"><i class="fas fa-file-pdf"></i><p>TNPSC Unit 8 Notes</p><a href="#" download style="color:var(--primary); font-size:0.8rem; font-weight:800;">Download Now</a></div>
            <div class="card"><i class="fas fa-file-pdf"></i><p>Indian Polity (Intro)</p><a href="#" download style="color:var(--primary); font-size:0.8rem; font-weight:800;">Download Now</a></div>
        </div>
        <p style="text-align:center; margin-top:40px; color:#ef4444; font-size:0.75rem; font-weight:800;">⚠️ Do not share these materials. Personal use only.</p>
    </div>
    {% endif %}

    {% if page == 'mock' %}
    <div style="position:fixed; inset:0; background:#fff; z-index:2000; overflow-y:auto; padding:25px;">
        <a href="/" style="font-weight:800; color:var(--primary); text-decoration:none;"><i class="fas fa-times-circle"></i> EXIT</a>
        <h2 style="margin-top:25px;">Sample Mock Test</h2>
        <div style="background:#f8fafc; padding:25px; border-radius:24px; box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);">
            <p><b>Q1. Which state in India has the longest coastline?</b></p>
            <label style="display:block; margin:10px;"><input type="radio" name="q1"> Gujarat</label>
            <label style="display:block; margin:10px;"><input type="radio" name="q1"> Tamil Nadu</label>
            <hr style="border:0.5px solid #e2e8f0; margin:20px 0;">
            <p style="color:#64748b;">More questions are available in the Premium Question Bank...</p>
            <button class="btn-pay" style="width:100%; max-width:none;">Submit Answers</button>
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
    return render_template_string(HTML_LAYOUT, user_name=session.get('user_name'), page='mock')

@app.route('/auth', methods=['POST'])
def auth():
    email, pwd, name, act = request.form.get('email'), request.form.get('pwd'), request.form.get('name'), request.form.get('act')
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
    
