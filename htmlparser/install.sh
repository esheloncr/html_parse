source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations htmlparser
python manage.py migrate htmlparser