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
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
        },
        "body": json.dumps(data)
    }


def lambda_handler(event, context):
    try:
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

        if action == "generate":
            otp_length = int(body.get("length", 6))

            if otp_length < 4 or otp_length > 10:
                raise ValueError("OTP length must be between 4 and 10")

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

        raise ValueError("action must be generate or verify")

    except Exception as e:
        return response(
            400,
            {
                "success": False,
                "error": str(e)
            }
        )