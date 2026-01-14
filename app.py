import sqlite3
from flask import Flask, render_template_string

app = Flask(__name__)

# Light Mode & Creative Dashboard UI
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="ta">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --blue: #007aff; --gold: #f39c12; --white: #ffffff; }
        body { font-family: 'Poppins', sans-serif; margin: 0; background: #f8f9fa; color: #333; }
        .header { background: var(--white); padding: 20px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); sticky; top: 0; z-index: 100; }
        .logo { font-size: 1.5rem; font-weight: 800; color: var(--blue); }
        .logo span { color: var(--gold); }
        .ticker { background: #ff4757; color: white; padding: 12px; overflow: hidden; white-space: nowrap; font-weight: bold; }
        .ticker p { display: inline-block; animation: move 20s linear infinite; margin: 0; }
        @keyframes move { from { transform: translateX(100%); } to { transform: translateX(-100%); } }
        .container { padding: 20px; max-width: 500px; margin: auto; }
        .dashboard { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; }
        .card { background: var(--white); padding: 25px 15px; border-radius: 20px; text-align: center; border: 1px solid #eee; transition: 0.3s; position: relative; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
        .card i { font-size: 2rem; color: var(--blue); margin-bottom: 10px; }
        .badge { position: absolute; top: 10px; right: 10px; font-size: 0.6rem; padding: 4px 8px; border-radius: 6px; font-weight: bold; text-transform: uppercase; }
        .free { background: #e3fcef; color: #00a854; }
        .premium { background: #fff1e6; color: #ff8800; }
        .pay-box { background: #eef6ff; border: 2px dashed var(--blue); padding: 20px; border-radius: 20px; text-align: center; margin-top: 25px; }
        .btn { background: var(--blue); color: white; border: none; padding: 15px; width: 100%; border-radius: 12px; font-weight: bold; cursor: pointer; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="header"><div class="logo">KARKA <span>CLOUD</span></div></div>
    <div class="ticker"><p>🚀 2026 Annual Planner Released! | Group 4 Hall Ticket starts today! | Daily Test Updated 🚀</p></div>
    <div class="container">
        <h3>Success Dashboard</h3>
        <div class="dashboard">
            <div class="card"><span class="badge free">Free</span><i class="fas fa-book"></i><br>Tamil Notes</div>
            <div class="card"><span class="badge premium">Paid</span><i class="fas fa-crown"></i><br>Maths Tricks</div>
            <div class="card"><span class="badge premium">Paid</span><i class="fas fa-file-pdf"></i><br>Unit 8 & 9</div>
            <div class="card"><span class="badge free">Free</span><i class="fas fa-pen-nib"></i><br>Daily Test</div>
        </div>
        <div class="pay-box">
            <h4>💎 Unlock Premium Access</h4>
            <p>Pay <b>₹99</b> and get all PDF shortcuts instantly.</p>
            <p style="font-size: 0.9rem;"><b>UPI ID: yourname@upi</b></p>
            <button class="btn" onclick="alert('Unga UPI app-ku redirect aagudhu...')">Pay via QR/UPI</button>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
