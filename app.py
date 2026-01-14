import os, random, smtplib
from flask import Flask, render_template_string, request, session
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "karkacloud_final_2026"

# Cloud Settings
S_EMAIL = os.environ.get('SENDER_EMAIL')
S_PASS = os.environ.get('SENDER_PASSWORD')

# Minimal Design to prevent 502 Errors
HTML = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body { font-family: sans-serif; text-align: center; padding: 50px; background: #f4f7f6; }
    .box { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); max-width: 350px; margin: auto; }
    input { width: 90%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; }
    button { background: #007aff; color: white; border: none; padding: 12px; width: 95%; border-radius: 8px; cursor: pointer; font-weight: bold; }
</style>
</head>
<body>
    <div class="box">
        <h2 style="color:#007aff">KARKA CLOUD</h2>
        {% if not logged_in %}
            {% if not s %}
            <form method="POST" action="/send">
                <input type="email" name="e" placeholder="Enter Gmail ID" required>
                <button type="submit">Get OTP</button>
            </form>
            {% else %}
            <p>OTP sent to {{ email }}</p>
            <form method="POST" action="/verify">
                <input type="text" name="u" placeholder="Enter 4-Digit OTP" required>
                <button type="submit">Login</button>
            </form>
            {% endif %}
        {% else %}
            <h3>Welcome to Dashboard!</h3>
            <p>Success! You are logged in.</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML, logged_in=session.get('u'))

@app.route('/send', methods=['POST'])
def send():
    email = request.form.get('e')
    otp = str(random.randint(1000, 9999))
    session['o'], session['te'] = otp, email
    
    msg = EmailMessage()
    msg.set_content(f"Your Karka Cloud OTP is: {otp}")
    msg['Subject'] = 'Login Verification'
    msg['From'], msg['To'] = S_EMAIL, email

    try:
        # Fast Connection
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=10) as s:
            s.starttls()
            s.login(S_EMAIL, S_PASS)
            s.send_message(msg)
        return render_template_string(HTML, s=True, email=email)
    except Exception as e:
        return f"Error: {str(e)}. Please check Render Password."

@app.route('/verify', methods=['POST'])
def verify():
    if request.form.get('u') == session.get('o'):
        session['u'] = session['te']
        return render_template_string(HTML, logged_in=True)
    return "Wrong OTP! <a href='/'>Back</a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
