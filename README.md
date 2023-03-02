# learning-python-flask

https://flask.palletsprojects.com/en/2.2.x/tutorial/layout/

## Create venv
    setup-venv.bat
## Start web service the first time
    pip install flask
    flask --app flaskr init-db
## Start web service
    flask --app flaskr run --debug
    or
    app.bat
    or
    call setup-venv.bat
    python app.py
## Test the service
    curl http://localhost:5000/hello
## Initialize database
    init-db.bat
    or
    flask --app flaskr init-db
    dir instance\flaskr.sqlite
 
## Unit tests
    pip install pytest  
    pytest

## Coverage
    pip install coverage
    coverage run -m pytest & coverage report
    or
    coverage run -m pytest & coverage html

## Build
    pip install wheel
    python setup.py bdist_wheel

## Upload
    pip install twine
    twine upload -r devpi-staging dist/flaskr-1.0.0-py3-none-any.whl

## Local installation test (on another directory)
    python -m venv venv
    venv\scripts\activate
    python -m pip install --upgrade pip
    pip install --force-reinstall ..\learning-flask\dist\flaskr-1.0.0-py3-none-any.whl

# Production setup

## Production installation (on another node)
    python -m venv venv
    venv\scripts\activate
    python -m pip install --upgrade pip --trusted-host devpi

	pip config set global.index-url "http://devpi:3141/root/pypi/+simple/"
	pip config set global.trusted-host "devpi pypi.org files.pythonhosted.org"
	pip config set search.index "http://devpi:3141/root/pypi/"
    pip config list

    pip install -i http://devpi:3141/packages/staging flaskr
    flask --app flaskr init-db
    dir venv\var\flaskr-instance\flaskr.sqlite
    gen-secret-key.bat > venv\var\flaskr-instance\config.py
    pip install waitress
    waitress-serve --port=5000 --call "flaskr:create_app"
