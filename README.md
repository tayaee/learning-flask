# learning-python-flask

https://flask.palletsprojects.com/en/2.2.x/tutorial/layout/

  # Create venv
    setup-venv.bat
# Start web service
    flask --app flaskr run --debug
or

    app.bat
or

    call setup-venv.bat
    python app.py
# Test the service
    curl http://localhost:5000/hello
# Initialize database
    init-db.bat
or

    flask --app flaskr init-db
    dir instance\flaskr.sqlite
 
# Unit tests
    pytest

# Coverage
    coverage run -m pytest
    coverage report
    coverage html