from marshmallow import Schema, fields
import requests


env = "production"
version = "v1.0"

if env == "production":
    blueprint_api = "https://api.instnt.org/secure"
elif env == "sandbox":
    blueprint_api = "https://sandbox-api.instnt.org/secure"
else:
    raise Exception("environment variable can be either 'production' or 'sandbox' ")


headers = {
    "Content-Type": "application/json",
}

get_assertion_api = f"{blueprint_api}/getassertion/{version}"
submit_form_api = f"{blueprint_api}/submitformdata/{version}"
docverify_authenticate_api = f"{blueprint_api}/docverify/authenticate/{version}"


class AssertionSchema(Schema):
    instnttxnid = fields.String(required=True)


class FormSchema(Schema):
    email = fields.String()
    firstName = fields.String()
    surName = fields.String()
    mobileNumber = fields.Integer()
    email = fields.Email()
    client_referer_url = fields.URL()
    client_referer_host = fields.String()
    fingerprint = fields.String(required=False)
    form_key = fields.String()


class DocumentSchema(Schema):
    formKey = fields.String()
    documentType = fields.String()
    documentFrontImage = fields.String(required=False)
    documentBackImage = fields.String(required=False)
    selfieImage = fields.String(required=False)


def common_errors(response, payload):

    if response.status_code == 202:
        message = "Document images submitted but verification in-flight"

    elif response.status_code == 400:
        message = "Bad request"

    elif response.status_code == 403:
        message = "Unauthorized access to formKey"

    elif response.status_code == 404:
        message = "Unauthorized access to formKey"

    elif response.status_code == 405:
        message = "Method not allowed"

    elif response.status_code == 408:
        message = "Request timeout"
    else:
        message = "unknown error"

    return {
        "message": message,
        "error": response.json()["error"],
        "status_code": response.status_code,
    }


def get_assertion(payload):
    response = requests.post(json=payload, url=get_assertion_api, headers=headers)

    if response.status_code == 200:
        try:
            # TODO decode response and then validate
            pass
        except Exception as e:
            print("error occurred in get_assertion: " + str(e))

        return {"body": response.json(), "status_code": response.status_code}

    return common_errors(response, payload)


def submit_form(payload):
    response = requests.post(json=payload, url=submit_form_api, headers=headers)

    if response.status_code == 200:
        try:
            # TODO decode response and then validate
            FormSchema().load(response.json())
        except Exception as e:
            print("error occurred submitting form: " + str(e))

        return {"body": response.json(), "status_code": response.status_code}

    return common_errors(response, payload)


def verify_document(payload):
    response = requests.post(
        json=payload, url=docverify_authenticate_api, headers=headers
    )

    if response.status_code == 200:
        try:
            # TODO decode response and then validate
            DocumentSchema().load(response.json())
        except Exception as e:
            print("error occurred verifying document: " + str(e))

        return {"body": response.json(), "status_code": response.status_code}

    return common_errors(response, payload)


def lambda_handler(event, context):
    try:
        event_body = event.get("body")
    except:
        event_body = event

    action = event.get("action", None)

    if action == "get_assertion":
        return submit_form(event_body)

    elif action == "submit_form":
        return submit_form(event_body)

    elif action == "verify_document":
        return verify_document(event_body)

    else:
        return "unknown action"


# For Testing use below payload

get_assertion_payload = {
    "instnttxnid": "xxx",
}

submit_form_payload = {
    "firstName": "xxx",
    "surName": "xxx",
    "mobileNumber": "4152031349",
    "email": "xx@xx.com",
    "client_referer_url": "https://sandbox.acmebank.org/signup.html",
    "client_referer_host": "sandbox.acmebank.org",
    "fingerprint": "",
    "form_key": "v879876100000",
}


verify_document_payload = {
    "formKey": "v879876100000",
    "documentType": "License",
    "documentFrontImage": 0,
    "documentBackImage": 0,
    "selfieImage": "....",
}

post_action_list = [
    "get_assertion" "submit_form",
    "verify_document",
]

payload_list = [
    get_assertion_payload,
    submit_form_payload,
    verify_document_payload,
]

post_event = {
    "action": post_action_list[0],
    "body": payload_list[0],
}

# this is for local testing only
print(lambda_handler(post_event, ""))
