from flask import Flask
from views import test, data

#from views import test #imports test variable from the views.py file

#Initializes the website application
#Also registers all the possible links from the home page based on the URL
app = Flask(__name__)
app.register_blueprint(test, url_prefix="/")
app.register_blueprint(data, name='data', url_prefix="/")
#app.register_blueprint(test, url_prefix="/test")


if __name__ == '__main__':
    app.run(debug=True, port=8000)