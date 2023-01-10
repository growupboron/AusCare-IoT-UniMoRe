# AusCare-IoT-UniMoRe

## Install the required packages for the flask application

```bash
pip install -r webapp/requirements.txt
```

## Install [ngrok](https://ngrok.com/download) and add auth token

```bash
snap install ngrok # Linux Systems
brew install ngrok/ngrok/ngrok # Mac

ngrok config add-authtoken <token>
```

## Run the application

```bash
python webapp/run.py
```

## to test the emotion recognition script

```bash
python emotion_detect.py
```
