# Serverless OTP Service 🔐

A serverless OTP generation and verification service built using **AWS Lambda** and **Amazon DynamoDB**.

The project demonstrates how to generate secure one-time passwords, store only their hashed values, apply automatic expiration using DynamoDB TTL, and verify OTPs through a public Lambda Function URL.

## 🚀 Features

* Secure numeric OTP generation using Python `secrets`
* Configurable OTP length from 4 to 10 digits
* SHA-256 hashing before storing OTPs
* OTP expiration after 5 minutes
* DynamoDB-based OTP storage
* DynamoDB TTL for automatic cleanup
* One-time verification
* OTP deleted after successful verification
* AWS Lambda serverless architecture
* Public Lambda Function URL API
* CORS-enabled responses
* No traditional server required

## 🏗️ Architecture

```text
Client
  |
  | HTTP POST
  v
AWS Lambda Function URL
  |
  v
AWS Lambda
  |
  +---- Generate OTP
  |       |
  |       v
  |   SHA-256 Hash
  |       |
  |       v
  |   DynamoDB OTPStore
  |       |
  |       +---- TTL: 5 minutes
  |
  +---- Verify OTP
          |
          v
      Compare Hash
          |
      +---+---+
      |       |
    Valid   Invalid
      |       |
      v       v
   Delete   Reject
    OTP
```

## 🛠️ Technologies Used

* **Python**
* **AWS Lambda**
* **Amazon DynamoDB**
* **AWS IAM**
* **AWS Lambda Function URL**
* **Boto3**
* **Git & GitHub**

## 📂 Project Structure

```text
Serverless-OTP-Service/
│
├── lambda_function.py
├── README.md
└── .gitignore
```

## 🔄 API Flow

### 1. Generate OTP

Send a POST request with:

```json
{
  "action": "generate",
  "userId": "test-user"
}
```

The service:

1. Generates a secure OTP.
2. Creates a SHA-256 hash of the OTP.
3. Stores the hash and expiration timestamp in DynamoDB.
4. Returns the OTP for demonstration/testing purposes.

Example response:

```json
{
  "success": true,
  "userId": "test-user",
  "otp": "******",
  "expiresIn": 300,
  "message": "OTP generated successfully."
}
```

### 2. Verify OTP

Send:

```json
{
  "action": "verify",
  "userId": "test-user",
  "otp": "YOUR_OTP"
}
```

If the OTP is correct and has not expired:

```json
{
  "success": true,
  "verified": true,
  "message": "OTP verified successfully"
}
```

After successful verification, the OTP record is deleted from DynamoDB.

## ⏱️ OTP Expiration

Each OTP is valid for **5 minutes (300 seconds)**.

The project uses a DynamoDB TTL attribute named:

```text
ttl
```

Expired records can be automatically removed by DynamoDB.

The Lambda function also checks the expiration timestamp during verification.

## 🔐 Security

The project follows several security practices:

* OTPs are generated using Python's cryptographically secure `secrets` module.
* Plaintext OTPs are not stored in DynamoDB.
* SHA-256 hashes are stored instead.
* `secrets.compare_digest()` is used for hash comparison.
* OTP records are deleted after successful verification.
* DynamoDB access is restricted through IAM permissions.

## ⚠️ Demo Limitation

For demonstration purposes, the generated OTP is returned in the API response.

A production authentication system should **not return the OTP directly to the client**.

Instead, the OTP should be delivered through a trusted channel such as:

* SMS
* Email
* Another verified communication channel

Additional production protections should include:

* API Gateway
* Authentication/authorization
* Rate limiting
* AWS WAF
* Monitoring and logging
* Protection against brute-force attempts

## 🌐 AWS Deployment

The service is deployed using:

**AWS Region:** Asia Pacific (Mumbai)

**Main AWS Services:**

* AWS Lambda
* Amazon DynamoDB
* AWS IAM
* Lambda Function URL

### Live API

The project includes a publicly accessible AWS Lambda Function URL for testing.

> The live endpoint is intended for demonstration and learning purposes.

## 🧪 Testing

The API was tested successfully through:

* AWS Lambda Test Events
* DynamoDB item verification
* Public Lambda Function URL
* PowerShell HTTP requests

Verified flow:

```text
Generate OTP
      ↓
Store OTP Hash + TTL
      ↓
Verify OTP
      ↓
verified: true
      ↓
Delete OTP
```

## 📌 Future Improvements

Possible improvements for a production-ready version:

* SMS OTP delivery using Amazon SNS
* Email OTP delivery using Amazon SES
* API Gateway integration
* AWS WAF protection
* Rate limiting
* Attempt limits
* Authentication and authorization
* CloudWatch monitoring and alerts
* Infrastructure as Code using AWS SAM or Terraform

## 👩‍💻 Author

**Vibha Kumari**

B.Tech — Information Technology

GitHub:
https://github.com/vibhakumari7889-hub

## 📄 License

This project is created for educational, portfolio, and demonstration purposes.
