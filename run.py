from app import create_app
from app.modules.ssl.https_setup import ssl_bp
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == '__main__':
   ssl_bp(app)
   #app.run(debug=True)