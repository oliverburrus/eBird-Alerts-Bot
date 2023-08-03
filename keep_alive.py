# Import required modules
from flask import Flask
from threading import Thread

# Create a Flask app with an empty name
app = Flask('')

# Define the route for the home page '/'
@app.route('/')
def home():
    return "I'm alive"  # When someone accesses the home page, this message will be returned

# Define a function 'run' to start the Flask app
def run():
    app.run(host='0.0.0.0', port=8080)  # Start the Flask app on 0.0.0.0 (all available network interfaces) on port 8080

# Define a function 'keep_alive' to keep the Flask app running in the background
def keep_alive():
    t = Thread(target=run)  # Create a new thread that will execute the 'run' function
    t.start()  # Start the new thread, which will start the Flask app in the background
