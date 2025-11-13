import plivo
from config import PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN, PLIVO_NUMBER, TO_NUMBER, BASE_URL

def make_outbound_call():
    if not all([PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN, PLIVO_NUMBER, TO_NUMBER, BASE_URL]):
        print("Error: Configuration variables are not set. Please edit config.py")
        return

    try:
        client = plivo.RestClient(PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN)
        response = client.calls.create(
            from_=PLIVO_NUMBER,
            to_=TO_NUMBER,
            answer_url=f'{BASE_URL}/ivr/',
            answer_method='POST',
        )
        print(f"Call initiated successfully!")
        print(f"Call UUID: {response.request_uuid}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    make_outbound_call()
