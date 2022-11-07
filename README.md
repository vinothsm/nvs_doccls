# nvs_doccls

### setup
    python -m venv env
    env/Scripts/activate
    python -m pip install --upgrade pip
    pip install -r requiremnts.txt

### run
start the worker:
    - dramatiq ics_innovation.worker

start the app:
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

