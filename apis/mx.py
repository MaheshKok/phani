from requests.auth import HTTPBasicAuth
from marshmallow import Schema, fields
import requests

blueprint_api = "https://int-api.mx.com"

headers = {
    "Accept": "application/vnd.mx.api.v1+json",
    "Content-Type": "application/json",
}
basic_auth = HTTPBasicAuth(
    "6111fc00-04ce-4b0c-a638-1e94d0f6ca0e",
    "0285f663616b43246a9c998211844809013aad0a",
)

user_api = f"{blueprint_api}/users"
user_guid = "USR-1cde020c-b252-4f3d-953b-a9cdbf6bb2b1"

member_api = f"{user_api}/{user_guid}/managed_members"
member_guid = "MBR-0a638081-e47e-4d0c-a4f6-643c4405da2d"

account_api = f"{member_api}/{member_guid}/accounts"
account_guid = "ACT-967f632b-9fd8-47bc-85b2-8319541c6d6d"

transaction_api = f"{account_api}/{account_guid}/transactions"
transaction_guid = "TRN-8f0ad298-80f5-45db-91d6-067c0911c8cb"

merchant_api = f"{blueprint_api}/merchants"
merchant_guid = "MCH-ad6d3405-ec03-721d-b0ca-eeceeebcb8b5"

category_api = f"{user_api}/{user_guid}/categories"


class UserSchema(Schema):
    email = fields.String()
    guid = fields.String()
    id = fields.String()
    is_disabled = fields.Boolean()
    # TODO check if fields support json
    metadata = fields.Str()


class MemberSchema(Schema):
    guid = fields.String()
    id = fields.String()
    institution_code = fields.String(required=True, allow_none=False)
    is_being_aggregated = fields.Boolean()
    is_managed_by_user = fields.Boolean()
    is_oauth = fields.Boolean()
    metadata = fields.String()
    name = fields.String()
    user_guid = fields.String()
    user_id = fields.String()

    successfully_aggregated_at = fields.String(allow_none=True)
    connection_status = fields.String(allow_none=True)
    aggregated_at = fields.String(allow_none=True)


class AccountSchema(Schema):
    account_number = fields.String()
    apr = fields.Float()
    apy = fields.Float()
    available_balance = fields.Float()
    available_credit = fields.Float()
    balance = fields.Float()
    cash_balance = fields.Float(allow_none=True)
    cash_surrender_value = fields.Float()
    created_at = fields.DateTime()
    credit_limit = fields.Float()
    currency_code = fields.String()
    day_payment_is_due = fields.Integer()
    death_benefit = fields.Integer()
    guid = fields.String()
    holdings_value = fields.Float(allow_none=True)
    id = fields.String()
    imported_at = fields.DateTime(allow_none=True)
    institution_code = fields.String()
    insured_name = fields.String(allow_none=True)
    interest_rate = fields.Float()
    is_closed = fields.Boolean()
    is_hidden = fields.Boolean()
    last_payment = fields.Float()
    last_payment_at = fields.DateTime()
    loan_amount = fields.Float()
    matures_on = fields.Date()
    member_guid = fields.String()
    member_id = fields.String()
    member_is_managed_by_user = fields.Boolean()
    metadata = fields.String()
    minimum_balance = fields.Float()
    minimum_payment = fields.Float()
    name = fields.String()
    nickname = fields.String()
    original_balance = fields.Float()
    pay_out_amount = fields.Float(allow_none=True)
    payment_due_at = fields.DateTime()
    payoff_balance = fields.Float()
    premium_amount = fields.Float(allow_none=True)
    routing_number = fields.String()
    started_on = fields.Date()
    subtype = fields.String()
    total_account_value = fields.Float(allow_none=True)
    type = fields.String()
    updated_at = fields.DateTime()
    user_guid = fields.String()
    user_id = fields.String()


class TransactionSchema(Schema):
    account_guid = fields.String()
    account_id = fields.String()
    amount = fields.Float()
    category = fields.String()
    category_guid = fields.String()
    check_number_string = fields.String()
    created_at = fields.DateTime()
    currency_code = fields.String()
    date = fields.Date()
    description = fields.String()
    guid = fields.String()
    id = fields.String()
    is_bill_pay = fields.Boolean()
    is_direct_deposit = fields.Boolean()
    is_expense = fields.Boolean()
    is_fee = fields.Boolean()
    is_income = fields.Boolean()
    is_international = fields.Boolean()
    is_overdraft_fee = fields.Boolean()
    is_payroll_advance = fields.Boolean()
    is_recurring = fields.Boolean(allow_none=True)
    is_subscription = fields.Boolean()
    latitude = fields.String(allow_none=True)
    localized_description = fields.String()
    localized_memo = fields.String()
    longitude = fields.String(allow_none=True)
    member_guid = fields.String()
    member_is_managed_by_user = fields.Boolean()
    memo = fields.String()
    merchant_category_code = fields.Integer()
    merchant_guid = fields.String(allow_none=True)
    merchant_location_guid = fields.String(allow_none=True)
    metadata = fields.String()
    original_description = fields.String()
    posted_at = fields.DateTime()
    status = fields.String()
    top_level_category = fields.String()
    transacted_at = fields.DateTime()
    type = fields.String()
    updated_at = fields.DateTime()
    user_guid = fields.String()
    user_id = fields.String()
    extended_transaction_type = fields.String(allow_none=True)


class MerchantSchema(Schema):
    created_at = fields.DateTime()
    guid = fields.String()
    logo_url = fields.URL()
    name = fields.String()
    updated_at = fields.DateTime()
    website_url = fields.URL()
    logo_updated_at = fields.DateTime(allow_none=True)


class CategorySchema(Schema):
    created_at = fields.DateTime(allow_none=True)
    guid = fields.String()
    is_default = fields.Boolean()
    is_income = fields.Boolean()
    metadata = fields.String(allow_none=True)
    name = fields.String()
    parent_guid = fields.String(allow_none=True)
    updated_at = fields.DateTime(allow_none=True)


def common_errors(response, payload):
    if response.status_code == 409:
        default_message = "An object with the given attributes already exists. "
        if payload.get("user"):
            message = (
                default_message
                + f"most probably user id: [{payload['user']['id']}] already exists"
            )
        elif payload.get("member"):
            message = (
                f"most probably member id: [{payload['member']['id']}] already exists"
            )
        elif payload.get("account"):
            message = (
                f"most probably account id: [{payload['account']['id']}] already exists"
            )
        elif payload.get("transaction"):
            message = f"most probably transaction id: [{payload['transaction']['id']}] already exists"
        else:
            message = default_message

        return {
            "error": {
                "message": message,
                "status": "conflict",
                "type": "record_not_unique",
            },
            "status_code": 409,
        }
    else:
        return {"error": response.json()["error"], "status_code": response.status_code}


def create_user(payload):
    response = requests.post(
        json=payload, url=user_api, headers=headers, auth=basic_auth
    )

    if response.status_code == 200:
        try:
            UserSchema().load(response.json()["user"])
        except Exception as e:
            print("error occurred validating create user response: " + str(e))

        return {"user": response.json()["user"], "status_code": response.status_code}

    return common_errors(response, payload)


def create_member(payload):
    managed_institution_api = "https://int-api.mx.com/managed_institutions"
    managed_institution_response = requests.get(
        url=managed_institution_api, headers=headers, auth=basic_auth
    )

    if managed_institution_response.status_code == 200:
        managed_institution_code_list = [
            managed_institution_dict["code"]
            for managed_institution_dict in managed_institution_response.json()[
                "institutions"
            ]
        ]
        if payload["member"]["institution_code"] not in managed_institution_code_list:
            # Below error is what we receive when we use invalid institution_code to create member
            return {
                "error": {
                    "message": f"Institution with code {payload['member']['institution_code']} not found, allowed institution_codes: {managed_institution_code_list}",
                    "status": "unprocessable_entity",
                    "type": "institution_not_allowed_error",
                },
                "status_code": 422,
            }

    response = requests.post(
        json=payload, url=member_api, headers=headers, auth=basic_auth
    )

    if response.status_code == 200:
        try:
            MemberSchema().load(response.json()["member"])
        except Exception as e:
            print(f"error occurred validating create member response: {e}")

        return {
            "member": response.json()["member"],
            "status_code": response.status_code,
        }

    return common_errors(response, payload)


def create_account(payload):

    response = requests.post(
        json=payload,
        url=account_api,
        headers=headers,
        auth=basic_auth,
    )

    if response.status_code == 200:
        try:
            AccountSchema().load(response.json()["account"])
        except Exception as e:
            print(f"error occurred validating create account response: {e}")

        return {
            "account": response.json()["account"],
            "status_code": response.status_code,
        }

    return common_errors(response, payload)


def create_transaction(payload):
    response = requests.post(
        json=payload,
        url=transaction_api,
        headers=headers,
        auth=basic_auth,
    )

    if response.status_code == 200:
        try:
            TransactionSchema().load(response.json()["transaction"])
        except Exception as e:
            print(f"error occurred validating create transaction response: {e}")

        return {
            "transaction": response.json()["transaction"],
            "status_code": response.status_code,
        }

    if response.status_code == 409:
        return {
            "error": {
                "message": f"An object with the given attributes already exists. most probably transaction id: {payload['transaction']['id']}, already exists",
                "status": "conflict",
                "type": "record_not_unique",
            },
            "status_code": 409,
        }

    return common_errors(response, payload)


def read_transaction():
    response = requests.get(
        url=f"{transaction_api}/{transaction_guid}",
        headers=headers,
        auth=basic_auth,
    )

    if response.status_code == 200:
        try:
            TransactionSchema().load(response.json()["transaction"])
        except Exception as e:
            print(f"error occurred validating read transaction response: {e}")

        return {
            "transaction": response.json()["transaction"],
            "status_code": response.status_code,
        }

    return {"error": response.json()["error"], "status_code": response.status_code}


def list_transactions():
    response = requests.get(
        url=transaction_api,
        headers=headers,
        auth=basic_auth,
    )

    if response.status_code == 200:
        try:
            TransactionSchema(many=True).load(response.json()["transactions"])
        except Exception as e:
            print(f"error occurred validating list transactions response: {e}")

        return {
            "transactions": response.json()["transactions"],
            "status_code": response.status_code,
        }

    return {"error": response.json()["error"], "status_code": response.status_code}


def read_merchant():
    response = requests.get(
        url=f"{merchant_api}/{merchant_guid}",
        headers=headers,
        auth=basic_auth,
    )

    if response.status_code == 200:
        try:
            MerchantSchema().load(response.json()["merchant"])
        except Exception as e:
            print(f"error occurred validating read merchant response: {e}")

        return {
            "merchant": response.json()["merchant"],
            "status_code": response.status_code,
        }

    return {"error": response.json()["error"], "status_code": response.status_code}


def list_merchants():
    response = requests.get(
        url=merchant_api,
        headers=headers,
        auth=basic_auth,
    )

    if response.status_code == 200:
        try:
            MerchantSchema(many=True).load(response.json()["merchants"])
        except Exception as e:
            print(f"error occurred validating list transactions response: {e}")

        return {
            "merchants": response.json()["merchants"],
            "status_code": response.status_code,
        }

    return {"error": response.json()["error"], "status_code": response.status_code}


def list_categories():
    response = requests.get(
        url=category_api,
        headers=headers,
        auth=basic_auth,
    )

    if response.status_code == 200:
        try:
            CategorySchema(many=True).load(response.json()["categories"])
        except Exception as e:
            print(f"error occurred validating list categories response: {e}")

        return {
            "categories": response.json()["categories"],
            "status_code": response.status_code,
        }

    return {"error": response.json()["error"], "status_code": response.status_code}


def lambda_handler(event, context):
    try:
        event_body = event.get("body")
    except:
        event_body = event

    action = event.get("action", None)

    if action == "create_user":
        return create_user(event_body)

    if action == "create_member":
        return create_member(event_body)

    if action == "create_account":
        return create_account(event_body)

    if action == "create_transaction":
        return create_transaction(event_body)

    if action == "read_transaction":
        return read_transaction()

    if action == "list_transactions":
        return list_transactions()

    if action == "read_merchant":
        return read_merchant()

    if action == "list_merchants":
        return list_merchants()

    if action == "list_categories":
        return list_categories()


# For Testing use below payload


create_user_payload = {
    "user": {
        "email": "email-test@provider.com",
        "id": "My-Unique-ID-test_again",
        "is_disabled": False,
        "metadata": "some metadata",
    }
}


create_member_payload = {
    "member": {
        "id": "mx bank",
        "institution_code": "d858b7e5-ede7-495e-a43b-c191d68a2ea6",
        "metadata": "some metadata",
        "name": "mx Bank",
    }
}


create_account_payload = {
    "account": {
        "account_number": "5366",
        "apr": 1.0,
        "apy": 1.0,
        "available_balance": 1000.0,
        "available_credit": 1000.0,
        "balance": 1000.0,
        "cash_surrender_value": 1000.0,
        "credit_limit": 100.0,
        "currency_code": "USD",
        "day_payment_is_due": 20,
        "death_benefit": 1000,
        "id": "1040434698121",
        "interest_rate": 1.0,
        "is_closed": False,
        "is_hidden": False,
        "last_payment": 100.0,
        "last_payment_at": "2015-10-13T17:57:37.000Z",
        "loan_amount": 1000.0,
        "matures_on": "2015-10-13T17:57:37.000Z",
        "metadata": "some metadata",
        "minimum_balance": 100.0,
        "minimum_payment": 10.0,
        "name": "Test account 2",
        "nickname": "Swiss Account",
        "original_balance": 10.0,
        "payment_due_at": "2015-10-13T17:57:37.000Z",
        "payoff_balance": 10.0,
        "routing_number": "68899990000000",
        "started_on": "2015-10-13T17:57:37.000Z",
        "subtype": "NONE",
        "type": "SAVINGS",
    }
}

create_transaction_payload = {
    "transaction": {
        "amount": "61.11",
        "category": "Groceries",
        "check_number_string": "6812",
        "currency_code": "USD",
        "description": "Whole foods",
        "id": "transaction-265abee9-889b-af6a-c69b-25157db2bdd9-2",
        "is_international": False,
        "latitude": -43.2075,
        "localized_description": "This is a localized_description",
        "localized_memo": "This is a localized_memo",
        "longitude": 139.691706,
        "memo": "This is a memo",
        "merchant_category_code": 5411,
        "merchant_guid": "MCH-7ed79542-884d-2b1b-dd74-501c5cc9d25b",
        "merchant_location_guid": "MCL-00024e59-18b5-4d79-b879-2a7896726fea",
        "metadata": "some metadata",
        "posted_at": "2016-10-07T06:00:00.000Z",
        "status": "POSTED",
        "transacted_at": "2016-10-06T13:00:00.000Z",
        "type": "DEBIT",
    }
}

post_action_list = [
    "create_user",
    "create_member",
    "create_account",
    "create_transaction",
]



read_action_list = [
    "read_transaction",
    "list_transactions",
    "read_merchant",
    "list_merchants",
    "list_categories",
]
read_event = {"action": read_action_list[4]}


payload_list = [
    create_user_payload,
    create_member_payload,
    create_account_payload,
    create_transaction_payload,
]
post_event = {
    "action": post_action_list[0],
    "body": payload_list[0],
}

print(lambda_handler(read_event, ""))
