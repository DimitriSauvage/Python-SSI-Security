from assets.bottle import route, run, Bottle
from response import responseApp

# Get app
mainApp = Bottle()

# Include others api controllers
mainApp.merge(responseApp);

@route('/hello')
def hello():
    return "Hello World!"


run(host='localhost', port=8080, debug=True)
