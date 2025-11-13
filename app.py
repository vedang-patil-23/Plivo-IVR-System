import flask
from flask import Flask, request
from flask import make_response as FlaskResponse
from config import PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN, ASSOCIATE_NUMBER, BASE_URL

app = Flask(__name__)

@app.route('/')
def health_check():
    return "IVR app is running."

@app.route('/ivr/', methods=['GET', 'POST'])
def main_menu():
    speak_body_en = "Hello, and thank you for calling. Press 1 for English."
    speak_body_es = "Presione dos para español."
    
    xml_response = f"""
    <Response>
        <GetInput action="{BASE_URL}/ivr/menu1" method="POST" input_type="dtmf" num_digits="1" retries="3" timeout="5">
            <Speak>{speak_body_en}</Speak>
            <Speak language="es-ES">{speak_body_es}</Speak>
        </GetInput>
        <Speak>We did not receive an input. Goodbye.</Speak>
        <Hangup/>
    </Response>
    """
    
    response = FlaskResponse(xml_response)
    response.headers['Content-Type'] = 'text/xml'
    return response

@app.route('/ivr/menu1', methods=['GET', 'POST'])
def handle_language_selection():
    digit = request.form.get('Digits')
    
    if digit == '1':  # Eng
        xml_response = f"""
        <Response>
            <GetInput action="{BASE_URL}/ivr/menu2?language=en" method="POST" input_type="dtmf" num_digits="1" retries="3" timeout="5">
                <Speak>Press 1 to play a short audio message. Press 2 to connect to a live associate.</Speak>
            </GetInput>
            <Speak>We did not receive an input. Redirecting to the main menu.</Speak>
            <Redirect>{BASE_URL}/ivr/</Redirect>
        </Response>
        """

    elif digit == '2':  # Esp
        speak_body = "Presione 1 para reproducir un mensaje de audio corto. Presione 2 para conectarse con un asociado en vivo."
        xml_response = f"""
        <Response>
            <GetInput action="{BASE_URL}/ivr/menu2?language=es" method="POST" input_type="dtmf" num_digits="1" retries="3" timeout="5">
                <Speak language="es-ES">{speak_body}</Speak>
            </GetInput>
            <Speak language="es-ES">No recibimos una entrada. Redirigiendo al menú principal.</Speak>
            <Redirect>{BASE_URL}/ivr/</Redirect>
        </Response>
        """
        
    else:
        xml_response = f"""
        <Response>
            <Speak>Invalid input. Please try again.</Speak>
            <Redirect>{BASE_URL}/ivr/</Redirect>
        </Response>
        """

    response = FlaskResponse(xml_response)
    response.headers['Content-Type'] = 'text/xml'
    return response


@app.route('/ivr/menu2', methods=['GET', 'POST'])
def handle_action_selection():
    digit = request.form.get('Digits')
    language = request.args.get('language', 'en')
    
    if digit == '1':
        speak_text = "Reproduciendo el mensaje." if language == 'es' else "Playing the message."
        xml_response = f"""
        <Response>
            <Speak language="{language}-{'ES' if language == 'es' else 'EN'}">{speak_text}</Speak>
            <Play>https://s3.amazonaws.com/plivocloud/Trumpet.mp3</Play>
            <Hangup/>
        </Response>
        """

    elif digit == '2':
        speak_text = "Conectándote con un asesor. Por favor, espera." if language == 'es' else "Connecting you to an associate. Please wait."
        xml_response = f"""
        <Response>
            <Speak language="{language}-{'ES' if language == 'es' else 'EN'}">{speak_text}</Speak>
            <Dial>{ASSOCIATE_NUMBER}</Dial>
        </Response>
        """

    else:
        speak_text = "Entrada no válida. Inténtelo de nuevo." if language == 'es' else "Invalid input. Please try again."
        redirect_url_param = 2 if language == 'es' else 1
        xml_response = f"""
        <Response>
            <Speak language="{language}-{'ES' if language == 'es' else 'EN'}">{speak_text}</Speak>
            <Redirect>{BASE_URL}/ivr/menu1?Digits={redirect_url_param}</Redirect>
        </Response>
        """

    response = FlaskResponse(xml_response)
    response.headers['Content-Type'] = 'text/xml'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
