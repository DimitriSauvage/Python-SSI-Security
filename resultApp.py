from assets.bottle import Bottle, get, request
from database.sqlServer import getConnection

# Get app
from helpers.HTTPResponseHelper import getHTTPResponse
from helpers.ResultHelper import getMaturity
from models.maturity import Maturity

resultApp = Bottle()


@get('/iso21827/result')
def getResult():
    """Get the maturity of the user"""

    return getMaturity(request.environ.get('REMOTE_ADDR'))
