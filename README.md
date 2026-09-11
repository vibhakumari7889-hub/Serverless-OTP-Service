# Serverless OTP Service 🔐

A serverless OTP generation and verification web application built using AWS Lambda and Python.

## Features

- Secure numeric OTP generation
- OTP length between 4–10 digits
- SHA-256 hashing before storing OTP
- 5-minute OTP expiration
- One-time OTP verification
- OTP removed after successful verification
- Browser-based web interface
- AWS Lambda Function URL
- CORS support
- No traditional server required

## Architecture

User Browser
     ↓
AWS Lambda Function URL
     ↓
AWS Lambda + Python
     ↓
Temporary OTP Storage in Lambda Memory

## Technologies Used

- Python 3.14
- AWS Lambda
- AWS Lambda Function URL
- Python `secrets`
- SHA-256 hashing
- HTML
- CSS
- JavaScript

## How It Works

### 1. Generate OTP

The user enters a User ID and clicks **Generate OTP**.

AWS Lambda generates a secure numeric OTP and temporarily stores its hash in Lambda memory.

### 2. Verify OTP

The user enters the OTP and clicks **Verify OTP**.

The entered OTP is hashed and compared with the stored hash.

If the OTP is correct and has not expired, verification is successful.

### 3. Expiration

Each OTP is valid for approximately 5 minutes.

Expired OTPs are removed from temporary storage.

## Live Demo

https://fiuerhtw6wrgdsm2itc3e6mj7a0hlucj.lambda-url.ap-south-1.on.aws/

## Project Repository

https://github.com/vibhakumari7889-hub/Serverless-OTP-Service

## Security

The project uses Python's `secrets` module for secure OTP generation and SHA-256 hashing for temporary OTP storage.

### Demo Limitation

This project is designed as a learning and portfolio demonstration.

OTP values are displayed in the demo interface and returned by the API. In a production authentication system, OTPs should be delivered through a trusted channel such as SMS or email and should use persistent secure storage, authentication, rate limiting, monitoring, and other security controls.

## AWS Deployment

The application was deployed using AWS Lambda in the Mumbai (`ap-south-1`) region.

## Future Improvements

- SMS OTP delivery using Amazon SNS
- Email OTP delivery using Amazon SES
- Persistent OTP storage
- API Gateway
- Rate limiting
- AWS WAF
- Authentication
- Monitoring and logging improvements

## Author

Vibha Kumari

B.Tech – Information Technology