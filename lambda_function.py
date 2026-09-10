import json
import secrets


def generate_otp(length=6):
    return "".join(str(secrets.randbelow(10)) for _ in range(length))


def lambda_handler(event, context):
    try:
        otp_length = 6

        if "body" in event and event["body"]:
            body = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
            otp_length = int(body.get("length", 6))

        elif "queryStringParameters" in event and event.get("queryStringParameters"):
            otp_length = int(event["queryStringParameters"].get("length", 6))

        elif "length" in event:
            otp_length = int(event["length"])

        if otp_length < 4 or otp_length > 10:
            raise ValueError("OTP length must be between 4 and 10")

        otp_code = generate_otp(otp_length)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
            },
            "body": json.dumps({
                "success": True,
                "otp": otp_code,
                "message": f"Successfully generated a {otp_length}-digit OTP code."
            })
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "success": False,
                "error": f"Invalid request execution: {str(e)}"
            })
        }import json
import secrets


def generate_otp(length=6):
    return "".join(str(secrets.randbelow(10)) for _ in range(length))


def lambda_handler(event, context):
    try:
        otp_length = 6

        if "body" in event and event["body"]:
            body = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
            otp_length = int(body.get("length", 6))

        elif "queryStringParameters" in event and event.get("queryStringParameters"):
            otp_length = int(event["queryStringParameters"].get("length", 6))

        elif "length" in event:
            otp_length = int(event["length"])

        if otp_length < 4 or otp_length > 10:
            raise ValueError("OTP length must be between 4 and 10")

        otp_code = generate_otp(otp_length)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
            },
            "body": json.dumps({
                "success": True,
                "otp": otp_code,
                "message": f"Successfully generated a {otp_length}-digit OTP code."
            })
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "success": False,
                "error": f"Invalid request execution: {str(e)}"
            })
        }import json
import secrets


def generate_otp(length=6):
    return "".join(str(secrets.randbelow(10)) for _ in range(length))


def lambda_handler(event, context):
    try:
        otp_length = 6

        if "body" in event and event["body"]:
            body = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
            otp_length = int(body.get("length", 6))

        elif "queryStringParameters" in event and event.get("queryStringParameters"):
            otp_length = int(event["queryStringParameters"].get("length", 6))

        elif "length" in event:
            otp_length = int(event["length"])

        if otp_length < 4 or otp_length > 10:
            raise ValueError("OTP length must be between 4 and 10")

        otp_code = generate_otp(otp_length)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
            },
            "body": json.dumps({
                "success": True,
                "otp": otp_code,
                "message": f"Successfully generated a {otp_length}-digit OTP code."
            })
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "success": False,
                "error": f"Invalid request execution: {str(e)}"
            })
        }