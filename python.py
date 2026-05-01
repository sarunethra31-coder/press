from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS

# Initialize Flask, pointing the static folder to the current directory
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# --- EMAIL CONFIGURATION ---
def send_order_email(data):
    sender_email = "YOUR_GMAIL@gmail.com" # Replace with your gmail
    sender_password = "YOUR_APP_PASSWORD" # Replace with your 16-digit App Password
    receiver_email = "sarunethra46@gmail.com"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"New Print Order from {data.get('Name', 'Customer')}"
    
    body = f"""New Order Details:
    
name = {data.get('Name', 'N/A')}
phone number = {data.get('Phone', 'N/A')}
address = {data.get('Address', 'N/A')}
email = {data.get('Email', 'N/A')}
printing type = {data.get('Printing Type', 'N/A')}
other details = {data.get('Other Details', 'N/A')}
"""
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent to sarunethra46@gmail.com successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        print("Make sure you have added your YOUR_GMAIL@gmail.com and YOUR_APP_PASSWORD in the code.")
        return False

@app.route('/')
def index():
    """Serve the index.html page at the root URL."""
    return app.send_static_file('index.html')

@app.route('/api/submit', methods=['POST'])
def submit_order():
    """Receive order data from the frontend and save it to a JSON file."""
    data = request.json
    
    # Add a timestamp to the order
    data['timestamp'] = datetime.now().isoformat()
    
    orders_file = 'orders.json'
    
    # Read existing orders if the file exists
    orders = []
    if os.path.exists(orders_file):
        with open(orders_file, 'r', encoding='utf-8') as f:
            try:
                orders = json.load(f)
            except json.JSONDecodeError:
                orders = []
                
    # Append the new order
    orders.append(data)
    
    # Save the updated list back to the file
    with open(orders_file, 'w', encoding='utf-8') as f:
        json.dump(orders, f, indent=4)
        
    print(f"\n[NEW ORDER RECEIVED] Saved to orders.json -> {data.get('Name')}")
    
    # Attempt to send the email
    send_order_email(data)
        
    # Return success to trigger the frontend balloons animation
    return jsonify({"status": "success", "message": "Order saved successfully!"}), 200

if __name__ == '__main__':
    print("="*50)
    print("Printing Press Server is running!")
    print("Open http://127.0.0.1:5000 in your browser.")
    print("="*50)
    app.run(debug=True, port=5000)
