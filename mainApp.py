from assets.bottle import run, Bottle
from levelApp import levelApp
from maturityApp import maturityApp
from questionApp import questionApp
from responseApp import responseApp
# Get app
from resultApp import resultApp

mainApp = Bottle()

# Include others api controllers
mainApp.merge(responseApp)
mainApp.merge(questionApp)
mainApp.merge(maturityApp)
mainApp.merge(resultApp)
mainApp.merge(levelApp)

# Run the app
run(host='localhost', port=8080, debug=True)
