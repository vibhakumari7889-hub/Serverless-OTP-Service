import json
import secrets
import time
import hashlib
import boto3

table = boto3.resource("dynamodb").Table("OTPStore")


def generate_otp(length=6):
    return "".join(str(secrets.randbelow(10)) for _ in range(length))


def hash_otp(otp):
    return hashlib.sha256(otp.encode()).hexdigest()


def response(status_code, data):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(data)
    }


def webpage():
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Serverless OTP Service</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #eef2ff, #f8fafc);
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 500px;
            background: white;
            padding: 32px;
            border-radius: 18px;
            box-shadow: 0 10px 35px rgba(0,0,0,0.12);
        }

        h1 {
            margin-top: 0;
            text-align: center;
            color: #1e293b;
        }

        .subtitle {
            text-align: center;
            color: #64748b;
            margin-bottom: 28px;
        }

        label {
            display: block;
            margin-top: 16px;
            margin-bottom: 7px;
            font-weight: bold;
            color: #334155;
        }

        input {
            width: 100%;
            padding: 13px;
            border: 1px solid #cbd5e1;
            border-radius: 9px;
            font-size: 16px;
        }

        button {
            width: 100%;
            padding: 13px;
            margin-top: 20px;
            border: none;
            border-radius: 9px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            background: #2563eb;
            color: white;
        }

        button:hover {
            background: #1d4ed8;
        }

        .verify {
            background: #16a34a;
        }

        .verify:hover {
            background: #15803d;
        }

        .result {
            margin-top: 22px;
            padding: 15px;
            border-radius: 9px;
            background: #f1f5f9;
            color: #334155;
            white-space: pre-wrap;
            word-break: break-word;
        }

        .otp {
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            letter-spacing: 6px;
            color: #2563eb;
            margin: 10px 0;
        }

        .note {
            margin-top: 20px;
            font-size: 13px;
            color: #64748b;
            text-align: center;
        }
    </style>
</head>

<body>

<div class="container">

    <h1>🔐 Serverless OTP Service</h1>

    <div class="subtitle">
        AWS Lambda + DynamoDB
    </div>

    <label>User ID</label>
    <input id="userId" type="text" placeholder="Enter user ID">

    <button onclick="generateOTP()">
        Generate OTP
    </button>

    <div id="otpResult" class="result" style="display:none;"></div>

    <label>Enter OTP</label>
    <input id="otp" type="text" maxlength="10" placeholder="Enter OTP">

    <button class="verify" onclick="verifyOTP()">
        Verify OTP
    </button>

    <div id="verifyResult" class="result" style="display:none;"></div>

    <div class="note">
        Demo project built using AWS Lambda, DynamoDB and Python.
    </div>

</div>

<script>

async function generateOTP() {

    const userId = document.getElementById("userId").value.trim();

    if (!userId) {
        alert("Please enter a User ID.");
        return;
    }

    try {

        const response = await fetch(window.location.href, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                action: "generate",
                userId: userId,
                length: 6
            })
        });

        const data = await response.json();

        const result = document.getElementById("otpResult");
        result.style.display = "block";

        if (data.success) {

            result.innerHTML =
                "<strong>OTP Generated</strong>" +
                "<div class='otp'>" +
                data.otp +
                "</div>" +
                "<div>Expires in 5 minutes.</div>";

            document.getElementById("otp").value = data.otp;

        } else {

            result.textContent = data.message || data.error || "Unable to generate OTP.";
        }

    } catch (error) {

        document.getElementById("otpResult").style.display = "block";
        document.getElementById("otpResult").textContent =
            "Error: " + error.message;
    }
}


async function verifyOTP() {

    const userId = document.getElementById("userId").value.trim();
    const otp = document.getElementById("otp").value.trim();

    if (!userId || !otp) {
        alert("Please enter User ID and OTP.");
        return;
    }

    try {

        const response = await fetch(window.location.href, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                action: "verify",
                userId: userId,
                otp: otp
            })
        });

        const data = await response.json();

        const result = document.getElementById("verifyResult");
        result.style.display = "block";

        if (data.verified) {

            result.textContent =
                "✅ " + data.message;

        } else {

            result.textContent =
                "❌ " + (data.message || data.error);
        }

    } catch (error) {

        document.getElementById("verifyResult").style.display = "block";
        document.getElementById("verifyResult").textContent =
            "Error: " + error.message;
    }
}

</script>

</body>
</html>
"""

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html; charset=UTF-8",
            "Access-Control-Allow-Origin": "*"
        },
        "body": html
    }


def lambda_handler(event, context):

    try:

        request_context = event.get("requestContext", {})
        http_info = request_context.get("http", {})
        method = http_info.get("method", "")

        # Open webpage when Function URL is visited in browser
        if method == "GET" and not event.get("queryStringParameters"):
            return webpage()

        # Handle browser CORS preflight
        if method == "OPTIONS":
            return {
                "statusCode": 204,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": ""
            }

        body = {}

        if event.get("body"):

            body = (
                json.loads(event["body"])
                if isinstance(event["body"], str)
                else event["body"]
            )

        elif event.get("queryStringParameters"):

            body = event["queryStringParameters"] or {}

        else:

            body = event or {}

        action = body.get("action", "generate")
        user_id = body.get("userId")

        if not user_id:
            raise ValueError("userId is required")

        # Generate OTP
        if action == "generate":

            otp_length = int(body.get("length", 6))

            if otp_length < 4 or otp_length > 10:
                raise ValueError(
                    "OTP length must be between 4 and 10"
                )

            otp = generate_otp(otp_length)

            ttl = int(time.time()) + 300

            table.put_item(
                Item={
                    "userId": user_id,
                    "otpHash": hash_otp(otp),
                    "ttl": ttl
                }
            )

            return response(
                200,
                {
                    "success": True,
                    "userId": user_id,
                    "otp": otp,
                    "expiresIn": 300,
                    "message": "OTP generated successfully."
                }
            )

        # Verify OTP
        if action == "verify":

            otp = str(body.get("otp", ""))

            item = table.get_item(
                Key={"userId": user_id}
            ).get("Item")

            if not item:

                return response(
                    404,
                    {
                        "success": False,
                        "verified": False,
                        "message": "OTP not found"
                    }
                )

            if int(item["ttl"]) < int(time.time()):

                table.delete_item(
                    Key={"userId": user_id}
                )

                return response(
                    400,
                    {
                        "success": False,
                        "verified": False,
                        "message": "OTP expired"
                    }
                )

            if secrets.compare_digest(
                hash_otp(otp),
                item["otpHash"]
            ):

                table.delete_item(
                    Key={"userId": user_id}
                )

                return response(
                    200,
                    {
                        "success": True,
                        "verified": True,
                        "message": "OTP verified successfully"
                    }
                )

            return response(
                401,
                {
                    "success": False,
                    "verified": False,
                    "message": "Invalid OTP"
                }
            )

        raise ValueError(
            "action must be generate or verify"
        )

    except Exception as e:

        return response(
            400,
            {
                "success": False,
                "error": str(e)
            }
        )