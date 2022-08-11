from flask import Flask

# create a new Flask app instance
app = Flask(__name__)

# define the starting point, also known as the root
@app.route('/') # the forward slash denotes that we want to put our data at the root of our routes. The forward slash is commonly known as the highest level of hierarchy in any computer system.
# put the code you want in that specific route below @app.route()

def hello_world():
    return 'Hello world'
