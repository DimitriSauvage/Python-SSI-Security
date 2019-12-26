from assets.bottle import run, Bottle
from level import levelApp
from maturity import maturityApp
from question import questionApp
from response import responseApp

# Get app
mainApp = Bottle()

# Include others api controllers
mainApp.merge(responseApp)
mainApp.merge(questionApp)
mainApp.merge(maturityApp)
mainApp.merge(levelApp)

# Run the app
run(host='localhost', port=8080, debug=True)
