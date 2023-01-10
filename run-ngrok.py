from website import create_app
from flask_ngrok2 import run_with_ngrok

app = create_app()
run_with_ngrok(app)

print(__name__)

if __name__ == '__main__':
    app.run(debug=True,port=5000)