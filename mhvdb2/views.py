from mhvdb2 import app

@app.route('/')
def index():
    return 'Hello World!'
