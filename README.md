# Plivo Project - InspireWorks IVR Demo

The application makes an outbound call and presents the recipient with a multi-level phone menu for a simulated customer support line. The project is a Demo IVR System using Plivo API.

## How It Works

The system is composed of two core components:

1.  **`make_call.py`**: A script that starts the process. It uses the Plivo API to make an outbound call to a specified phone number. In the API request, it tells Plivo where to find the first set of instructions by providing an `answer_url`.

2.  **`app.py`**: A small web server built with Flask. This server's job is to respond to HTTP requests (webhooks) from Plivo.
    - When the call is answered, Plivo requests the `answer_url`.
    - The server responds with Plivo XML (PHLO) that instructs the call to play a message and gather keypad input.
    - When the caller presses a digit, Plivo sends it back to another endpoint on the server.
    - The server then responds with new XML to advance the IVR flow, either playing a message, forwarding the call, or repeating a menu.

## Getting Started

Follow these steps to get the demo up and running on your local machine.

### 1. Prerequisites

- A Plivo account (you will need your Auth ID and Auth Token).
- A registered Plivo phone number.
- Python 3.7+
- `ngrok` to expose your local server to the internet.

### 2. Setup

First, clone the repository and set up your Python environment.

```bash
# If you haven't already, clone the project
# git clone <your-repo-url>
# cd <your-repo-directory>

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a new file named `config.txt` in the main project directory. This file will hold your credentials and settings.

> **Important:** The config file contains sensitive credentials. It is already listed in `.gitignore` to prevent you from accidentally committing it.

Your `config.txt` file should contain the following variables. Fill them in with your own values.

- `PLIVO_AUTH_ID`: Your Plivo Auth ID.
- `PLIVO_AUTH_TOKEN`: Your Plivo Auth Token.
- `PLIVO_NUMBER`: Your Plivo phone number, in E.164 format (e.g., `+14155552671`).
- `TO_NUMBER`: The destination phone number you want the application to call.
- `ASSOCIATE_NUMBER`: The number to forward the call to when the "connect to associate" option is selected.
- `BASE_URL`: The public URL for your local server. You will get this from `ngrok` in the next step.

Your `config.txt` should look like this, with your actual values:
```
PLIVO_AUTH_ID = "YOUR_PLIVO_AUTH_ID"
PLIVO_AUTH_TOKEN = "YOUR_PLIVO_AUTH_TOKEN"
PLIVO_NUMBER = "+14155552671"
TO_NUMBER = "+12025550135"
ASSOCIATE_NUMBER = "+18085550125"
BASE_URL = "https://<your-ngrok-url>.ngrok.io"
```

### 4. Expose Your Server with ngrok

Plivo's cloud platform needs a public URL to communicate with your local Flask server.

In a new terminal window, start `ngrok` to create a secure tunnel to your local port 5000.

```bash
ngrok http 5000
```

`ngrok` will provide a public "Forwarding" URL. **Copy the HTTPS URL** and paste it as the `BASE_URL` value in your `config.txt` file.

## Running the Demo

You will need two terminal windows running simultaneously, both with the virtual environment activated (`source venv/bin/activate`).

**Step 1: Prepare the Configuration**

The Python code reads its settings from a file named `config.py`. Before starting the server, rename your `config.txt` to `config.py`.

```bash
mv config.txt config.py

# On Windows
# ren config.txt config.py
```

**Step 2: Start the Server (Terminal 1)**

Launch the Flask web server. This will listen for incoming webhooks from Plivo.

```bash
python app.py
```

**Step 3: Make the Call (Terminal 2)**

In your second terminal, run the `make_call.py` script to trigger the outbound call.

```bash
python make_call.py
```

The script will confirm that the call was initiated. The `TO_NUMBER` you configured will receive a call shortly.

## License

Licensed under WTFPL Lincense.