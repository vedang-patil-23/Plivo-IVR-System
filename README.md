# InspireWorks - Plivo IVR Demo

This repository contains a demo IVR (Interactive Voice Response) system built with Python and Flask to demonstrate the capabilities of Plivo's Voice API.

The application makes an outbound call and presents the recipient with a multi-level phone menu for a simulated customer support line.

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
# Clone the project
git clone <your-repo-url>
cd <your-repo-directory>

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt
```

### 3. Configuration

The application's configuration is managed in `config.py`.

> **Important:** This file contains sensitive credentials and is ignored by Git (via `.gitignore`). Never commit this file.

You will need to edit `config.py` with your own values:

| Variable           | Description                                                                                             |
| ------------------ | ------------------------------------------------------------------------------------------------------- |
| `PLIVO_AUTH_ID`    | Your Plivo Auth ID.                                                                                     |
| `PLIVO_AUTH_TOKEN` | Your Plivo Auth Token.                                                                                  |
| `PLIVO_NUMBER`     | Your Plivo phone number, in E.164 format (e.g., `+14155552671`).                                         |
| `TO_NUMBER`        | The destination phone number you want the application to call.                                          |
| `ASSOCIATE_NUMBER` | The number to forward the call to when the "connect to associate" option is selected.                   |
| `BASE_URL`         | The public URL for your local server. You will get this from `ngrok` in the next step.                    |

### 4. Expose Your Server with ngrok

Plivo's cloud platform needs a public URL to communicate with your local Flask server.

In a new terminal window, start `ngrok` to create a secure tunnel to your local port 5000.

```bash
ngrok http 5000
```

`ngrok` will provide a public "Forwarding" URL (it looks like `https://<random-string>.ngrok.io`). **Copy the HTTPS URL** and paste it as the `BASE_URL` value in your `config.py` file.

## Running the Demo

You will need two terminal windows running simultaneously, both with the virtual environment activated (`source venv/bin/activate`).

**Terminal 1: Start the Server**

Launch the Flask web server. This will listen for incoming webhooks from Plivo.

```bash
python app.py
```

**Terminal 2: Make the Call**

In your second terminal, run the `make_call.py` script to trigger the outbound call.

```bash
python make_call.py
```

The script will confirm that the call was initiated. The `TO_NUMBER` you configured will receive a call shortly. When you answer, you will be greeted by the IVR menu.