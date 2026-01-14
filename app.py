import sqlite3
import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# News API key from environment variable
API_KEY = os.environ.get('MY_API_KEY')

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="ta">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --blue: #007aff; --gold: #f39c12; --white: #ffffff; }
        body { font-family: 'Poppins', sans-serif; margin: 0; background: #f8f9fa; color: #333; }
        
        /* Login Overlay */
        #login-overlay { position: fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:1000; display: flex; align-items: center; justify-content: center; text-align: center; }
        .login-card { width: 85%; max-width: 400px; padding: 20px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        
        .header { background: var(--white); padding: 15px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .logo { font-size: 1.5rem; font-weight: 800; color: var(--blue); }
        .logo span { color: var(--gold); }
        
        .container { padding: 20px; max-width: 500px; margin: auto; }
        .dashboard { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .card { background: var(--white); padding: 20px; border-radius: 20px; text-align: center; border: 1px solid #eee; position: relative; }
        .badge { position: absolute; top: 10px; right: 10px; font-size: 0.6rem; padding: 4px 8px; border-radius: 6px; font-weight: bold; }
        .free { background: #e3fcef; color: #00a854; }
        .premium { background: #fff1e6; color: #ff8800; }
        
        input { width: 90%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 10px; }
        .btn { background: var(--blue); color: white; border: none; padding: 15px; width: 100%; border-radius: 12px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>

    <div id="login-overlay">
        <div class="login-card" id="auth-box">
            <div class="logo">KARKA <span>CLOUD</span></div>
            <h3>Student Register</h3>
            <p>Enter Email to get OTP</p>
            <input type="email" id="email" placeholder="Gmail ID">
            <input type="password" id="pass" placeholder="Password">
            <button class="btn" onclick="sendOTP()">Send OTP</button>
        </div>
    </div>

    <div id="main-content" style="display:none;">
        <div class="header"><div class="logo">KARKA <span>CLOUD</span></div></div>
        <div class="container">
            <h3>Welcome, Aspirant!</h3>
            <div class="dashboard">
                <div class="card"><span class="badge free">Free</span><i class="fas fa-book"></i><br>Tamil Notes</div>
                <div class="card"><span class="badge premium">Paid</span><i class="fas fa-crown"></i><br>Maths Tricks</div>
            </div>
            <div style="margin-top:20px; text-align:center; padding:20px; border:2px dashed var(--blue); border-radius:20px;">
                <h4>💎 Unlock Everything</h4>
                <p>Pay ₹99 to <b>yourname@upi</b></p>
                <button class="btn">Pay via QR</button>
            </div>
        </div>
    </div>

    <script>
        function sendOTP() {
            let email = document.getElementById('email').value;
            if(email.includes("@gmail.com")) {
                let otp = prompt("OTP sent to " + email + ". Enter 4-digit OTP (Try 1234 for testing):");
                if(otp == "1234") {
                    document.getElementById('login-overlay').style.display = 'none';
                    document.getElementById('main-content').style.display = 'block';
                } else {
                    alert("Invalid OTP!");
                }
            } else {
                alert("Please enter a valid Gmail ID");
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
            
