# Serverless Email API

A REST API built with Serverless Framework and AWS Lambda to send emails via AWS SES.

## Features

- REST API endpoint for sending emails
- Input validation and error handling
- AWS SES integration
- Serverless offline support for local development
- CORS enabled

## Prerequisites

- Node.js (v14 or higher)
- Python 3.11
- AWS Account with SES configured
- Serverless Framework

## Installation

1. Clone the repository:
```bash
   git clone https://github.com/maitysneha5101-cloud/serverless-email-api.git
   cd serverless-email-api
```

2. Install dependencies:
```bash
   npm install
   pip install -r requirements.txt
```

3. Configure AWS credentials:
```bash
   serverless config credentials --provider aws --key YOUR_ACCESS_KEY --secret YOUR_SECRET_KEY
```

4. Update sender email in `handler.py` or set environment variable

## Local Development
```bash
serverless offline start
```

## Deployment
```bash
serverless deploy
```

## API Usage

**Endpoint:** `POST /send-email`

**Request:**
```json
{
  "receiver_email": "recipient@example.com",
  "subject": "Test Email",
  "body_text": "This is a test email!"
}
```

**Response:**
```json
{
  "message": "Email sent successfully",
  "messageId": "...",
  "receiver": "recipient@example.com"
}
```

## License

MIT