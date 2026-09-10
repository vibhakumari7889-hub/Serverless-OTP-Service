# Serverless OTP Generation Service

A serverless OTP generation service built using AWS Lambda and Python.

## Features

- Secure numeric OTP generation
- Configurable OTP length
- AWS Lambda serverless architecture
- Public Function URL for API access
- JSON API response
- No server management required

## Technologies Used

- Python
- AWS Lambda
- AWS Lambda Function URL
- GitHub

## How It Works

The application uses AWS Lambda to generate a secure random OTP.

A request is sent to the Lambda Function URL, and the service returns a JSON response containing the generated OTP.

## API Response

Example:

```json
{
  "success": true,
  "otp": "123456",
  "message": "Successfully generated a 6-digit OTP code."
}