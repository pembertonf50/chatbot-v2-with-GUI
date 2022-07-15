venv:
python -m venv venv # command to create virtual environment dir
.\scipts\activate.bat # activates environment
deactivate # deactivates venv
rmdir venv /s # deletes venv

pip:
pip install -r requirements.txt
pip freeze > requirements.txt

dont add the virtual env, .idea, _pycache_, readme.txt to heroku
heroku create <app name>