import flask
from flask import Flask, request, Response
import plivo
from config import PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN, ASSOCIATE_NUMBER, BASE_URL

app = Flask(__name__)

@app.route('/')
def health_check():
    return "IVR app is running."

@app.route('/ivr/', methods=['GET', 'POST'])
def main_menu():
    """Serves the initial language selection menu."""
    response = plivo.Response()
    
    get_input = plivo.GetInput(
        action=f'{BASE_URL}/ivr/menu1',
        method='POST',
        input_type='dtmf',
        num_digits=1,
        retries=3,
        timeout=5
    )
    
    speak_body_en = "Hello, and thank you for calling. Press 1 for English."
    speak_body_es = "Presione dos para español."
    
    response.add(plivo.Speak(speak_body_en))
    response.add(plivo.Speak(speak_body_es, language="es-ES"))
    
    get_input.add(response)

    fallback_response = plivo.Response()
    fallback_response.add(plivo.Speak("We did not receive an input. Goodbye."))
    
    return Response(str(fallback_response), mimetype='text/xml')

@app.route('/ivr/menu1', methods=['GET', 'POST'])
def handle_language_selection():
    """Handles language selection and serves the action menu."""
    digit = request.form.get('Digits')
    response = plivo.Response()

    if digit == '1':  # Eng
        get_input = plivo.GetInput(
            action=f'{BASE_URL}/ivr/menu2?language=en',
            method='POST',
            input_type='dtmf',
            num_digits=1,
            retries=3,
            timeout=5
        )
        get_input.add(plivo.Speak("Press 1 to play a short audio message. Press 2 to connect to a live associate."))
        response.add(get_input)
        response.add(plivo.Speak("We did not receive an input. Redirecting to the main menu."))
        response.add(plivo.Redirect(f'{BASE_URL}/ivr/'))

    elif digit == '2':  # Esp
        get_input = plivo.GetInput(
            action=f'{BASE_URL}/ivr/menu2?language=es',
            method='POST',
            input_type='dtmf',
            num_digits=1,
            retries=3,
            timeout=5
        )
        speak_body = "Presione 1 para reproducir un mensaje de audio corto. Presione 2 para conectarse con un asociado en vivo."
        get_input.add(plivo.Speak(speak_body, language="es-ES"))
        response.add(get_input)
        response.add(plivo.Speak("No recibimos una entrada. Redirigiendo al menú principal.", language="es-ES"))
        response.add(plivo.Redirect(f'{BASE_URL}/ivr/'))
        
    else:
        response.add(plivo.Speak("Invalid input. Please try again."))
        response.add(plivo.Redirect(f'{BASE_URL}/ivr/'))

    return Response(str(response), mimetype='text/xml')


@app.route('/ivr/menu2', methods=['GET', 'POST'])
def handle_action_selection():
    """Handles the final action: play audio or dial."""
    digit = request.form.get('Digits')
    language = request.args.get('language', 'en')
    response = plivo.Response()

    if digit == '1':
        if language == 'es':
            response.add(plivo.Speak("Reproduciendo el mensaje.", language="es-ES"))
        else:
            response.add(plivo.Speak("Playing the message."))
        
        response.add(plivo.Play("https://s3.amazonaws.com/plivocloud/Trumpet.mp3"))
        response.add(plivo.Hangup())

    elif digit == '2':
        if language == 'es':
            response.add(plivo.Speak("Conectándote con un asesor. Por favor, espera.", language="es-ES"))
        else:
            response.add(plivo.Speak("Connecting you to an associate. Please wait."))
        
        response.add(plivo.Dial(ASSOCIATE_NUMBER))

    else:
        if language == 'es':
            response.add(plivo.Speak("Entrada no válida. Inténtelo de nuevo.", language="es-ES"))
        else:
            response.add(plivo.Speak("Invalid input. Please try again."))
        
        if language == 'es':
             response.add(plivo.Redirect(f'{BASE_URL}/ivr/menu1?Digits=2'))
        else:
             response.add(plivo.Redirect(f'{BASE_URL}/ivr/menu1?Digits=1'))


    return Response(str(response), mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)

