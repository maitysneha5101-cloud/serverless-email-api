from flask import Flask, request, jsonify
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        
        # Validate input
        receiver_email = data.get('receiver_email')
        subject = data.get('subject')
        body_text = data.get('body_text')
        
        errors = []
        
        if not receiver_email:
            errors.append('receiver_email is required')
        elif not validate_email(receiver_email):
            errors.append('receiver_email must be a valid email address')
        
        if not subject:
            errors.append('subject is required')
        
        if not body_text:
            errors.append('body_text is required')
        
        if errors:
            return jsonify({
                'error': 'Validation failed',
                'details': errors
            }), 400
        
        # Email configuration
        sender_email = os.environ.get('SENDER_EMAIL')
        sender_password = os.environ.get('SENDER_PASSWORD')
        
        if not sender_email or not sender_password:
            return jsonify({
                'error': 'Server configuration error',
                'message': 'Email credentials not configured'
            }), 500
        
        # Create message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body_text, 'plain'))
        
        # Send email via Gmail SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        return jsonify({
            'message': 'Email sent successfully',
            'receiver': receiver_email
        }), 200
        
    except smtplib.SMTPAuthenticationError:
        return jsonify({
            'error': 'Authentication failed',
            'message': 'Invalid email credentials'
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Email API is running',
        'endpoints': {
            '/send-email': 'POST - Send an email',
            '/health': 'GET - Health check'
        }
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
