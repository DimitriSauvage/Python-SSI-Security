from assets.bottle import run, Bottle, get, HTTPResponse, put, request
from database.sqlServer import executeRequest, getConnection

# Get app
maturityApp = Bottle()


@get('/iso21827/m/<identifier>')
def getMaturity(identifier):
    """Get a maturity"""
    result = None

    # Get the connection
    conn = getConnection()

    # Get the maturity
    maturity_cursor = executeRequest(
        "SELECT LessThan, GreaterThan, Description FROM Maturity WHERE Maturity.Id = " + identifier, conn)
    maturity_response = maturity_cursor.fetchone()
    if maturity_response is not None:
        content = "<= " + str(maturity_response[0]) \
                  + " <= " \
                  + str(maturity_response[1]) \
                  + " - " + maturity_response[2]

        result = HTTPResponse(status=200, body=content)
    else:
        # Question does not exist
        result = HTTPResponse(status=500, body="This maturity does not exist")
    conn.close()
    return result


@get('/iso21827/m')
def getAll():
    """Get all maturities"""
    result = None
    content = 'Maturities<br/>'

    # Get the connection
    conn = getConnection()

    # Get the maturity
    maturity_cursor = executeRequest("SELECT LessThan, GreaterThan, Description FROM Maturity ", conn)

    for maturity_response in maturity_cursor.fetchall():
        content += str(maturity_response[1]) + " => " + str(maturity_response[0]) + " : " + \
                  maturity_response[2] + "<br>"

    conn.close()
    result = HTTPResponse(status=200, body=content)
    return result
