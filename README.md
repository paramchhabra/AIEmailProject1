Commands for initation
python -m venv venv

Commands if already initiated
.\venv\Scripts\activate
pip install -r requirements.txt
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem

After every module installation
pip freeze > requirements.txt
