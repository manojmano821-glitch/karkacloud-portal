import os
import random
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template_string, request, session

app = Flask(__name__)
app.secret_key = "karkacloud_secure_key_2026"

# Cloud Environment Variables
API_KEY = os.environ.get('MY_API_KEY')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="ta">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --blue: #007aff; --gold: #f39c12; --white: #ffffff; }
        body { font-family: 'Poppins', sans-serif; margin: 0; background: #f8f9fa; color: #333; }
        
        /* Login Screen */
        .login-screen { max-width: 400px; margin: 60px auto; padding: 30px; background: white; border-radius: 25px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); text-align: center; }
        input { width: 90%; padding: 15px; margin: 10px 0; border: 1px solid #eee; border-radius: 12px; background: #f9f9f9; font-size: 1rem; }
        
        /* Dashboard Design */
        .header { background: var(--white); padding: 15px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .logo { font-size: 1.6rem; font-weight: 800; color: var(--blue); }
        .logo span { color: var(--gold); }
        .ticker { background: #ff4757; color: white; padding: 10px; overflow: hidden; white-space: nowrap; font-weight: bold; }
        .ticker-text { display: inline-block; animation: scroll 25s linear infinite; }
        @keyframes scroll { from { transform: translateX(100%); } to { transform: translateX(-100%); } }
        
        .container { padding: 20px; max-width: 500px; margin: auto; }
        .dashboard { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; }
        .card { background: white; padding: 25px 15px; border-radius: 20px; text-align: center; border: 1px solid #eee; position: relative; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
        .card i { font-size: 2rem; color: var(--blue); margin-bottom: 10px; }
        .badge { position: absolute; top: 10px; right: 10px; font-size: 0.6rem; padding: 4px 8px; border-radius: 6px; font-weight: bold; }
        .free { background: #e3fcef; color: #00a854; }
        .premium { background: #fff1e6; color: #ff8800; }
        
        .btn { background: var(--blue); color: white; border: none; padding: 15px; width: 100%; border-radius: 12px; font-weight: bold; cursor: pointer; margin-top: 10px; font-size: 1rem; }
        .loading { color: var(--blue); font-weight: bold; margin-top: 10px; display: none; }
    </style>
</head>
<body>

    {% if not logged_in %}
    <div class="login-screen">
        <div class="logo">KARKA <span>CLOUD</span></div>
        {% if not otp_sent %}
        <h3>Student Portal</h3>
        <p style="color:#666;">Login via Gmail OTP</p>
        <form method="POST" action="/send-otp" onsubmit="showLoading()">
            <input type="email" name="email" placeholder="Enter Gmail ID" required>
            <button class="btn" type="submit">Get OTP</button>
            <div id="loader" class="loading">Sending OTP... Please wait</div>
        </form>
        {% else %}
        <h3>Verify OTP</h3>
        <p style="color:#666;">Sent to: {{ email }}</p>
        <form method="POST" action="/verify-otp">
            <input type="text" name="user_otp" placeholder="Enter 4-Digit OTP" required maxlength="4">
            <button class="btn" type="submit">Verify & Enter</button>
        </form>
        {% endif %}
    </div>
    <script>function showLoading(){ document.getElementById('loader').style.display='block'; }</script>

    {% else %}
    <div class="header"><div class="logo">KARKA <span>CLOUD</span></div></div>
    <div class="ticker"><div class="ticker-text">🚀 TNPSC Group 4 Result Update | Daily Current Affairs Added | Premium Notes Available 🚀</div></div>
    
    <div class="container">
        <h3>Welcome, Aspirant!</h3>
        <div class="dashboard">
            <div class="card"><span class="badge free">Free</span><i class="fas fa-book"></i><br>Tamil Notes</div>
            <div class="card"><span class="badge premium">Paid</span><i class="fas fa-crown"></i><br>Maths Tricks</div>
            <div class="card"><span class="badge premium">Paid</span><i class="fas fa-file-pdf"></i><br>Unit 8 & 9</div>
            <div class="card"><span class="badge free">Free</span><i class="fas fa-pen-nib"></i><br>Daily Test</div>
        </div>
        
        <div style="margin-top:25px; background:#eef6ff; border:2px dashed var(--blue); padding:20px; border-radius:20px; text-align:center;">
            <h4>💎 Premium Unlock</h4>
            <p>Pay <b>₹99</b> for Lifetime Access</p>
            <p><b>UPI: yourid@upi</b></p>
            <button class="btn" onclick="alert('Contact Admin for Payment')">Pay via QR/UPI</button>
        </div>
    </div>
    {% endif %}
</body>
</html>
"""

def send_mail(receiver, otp):
    msg = EmailMessage()
    msg.set_content(f"Unga Karka Cloud Login OTP: {otp}. Success Portal-ai thirakka idhai payanpaduthunga.")
    msg['Subject'] = 'Karka Cloud OTP Verification'
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver
    
    # Stable Connection using Port 587 (TLS)
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.send_message(msg)

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT, logged_in=session.get('user'))

@app.route('/send-otp', methods=['POST'])
def handle_send_otp():
    email = request.form.get('email')
    otp = str(random.randint(1000, 9999))
    session['otp'] = otp
    session['temp_email'] = email
    try:
        send_mail(email, otp)
        return render_template_string(HTML_LAYOUT, otp_sent=True, email=email)
    except Exception as e:
        return f"Error: {e}. Check Render Variables 'SENDER_EMAIL' and 'SENDER_PASSWORD'."

@app.route('/verify-otp', methods=['POST'])
def verify():
    user_otp = request.form.get('user_otp')
    if user_otp == session.get('otp'):
        session['user'] = session['temp_email']
        return render_template_string(HTML_LAYOUT, logged_in=True)
    return "Invalid OTP! <a href='/'>Try again</a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    
