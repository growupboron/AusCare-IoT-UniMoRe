# AusCare-IoT-UniMoRe

## Install the required packages for the flask application

```bash
pip install -r requirements.txt
```

## Run the application on localhost

```bash
python run.py
```

## Install [ngrok](https://ngrok.com/download) and add auth token

```bash
snap install ngrok # Linux Systems
brew install ngrok/ngrok/ngrok # Mac

ngrok config add-authtoken <token>
```

## Run the application using ngrok

```bash
python run-ngrok.py
```

## to test the emotion recognition script

```bash
python experiments/emotion-detector-deployed/emotion_detect.py
```
