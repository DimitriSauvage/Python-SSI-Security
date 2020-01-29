from assets.bottle import Bottle, get, post, request
from database.sqlServer import executeRequest, getConnection

# Get app
from helpers.HTTPResponseHelper import getHTTPResponse
from helpers.ResultHelper import getMaturity
from models.maturity import Maturity

maturityApp = Bottle()


@get('/iso21827/m/<identifier>')
def getMat(identifier):
    """Get a maturity"""
    result = None

    # Get the connection
    conn = getConnection()

    # Get the maturity
    maturity_cursor = executeRequest(
        "SELECT Id, LessThan, GreaterThan, Description FROM Maturity WHERE Maturity.Id = " + identifier, conn)
    row = maturity_cursor.fetchone()
    if row is not None:
        maturity = Maturity()
        maturity.id = row[0]
        maturity.less_than = row[1]
        maturity.greater_than = row[2]
        maturity.description = row[3]

        result = getHTTPResponse(200, maturity)
    else:
        # Question does not exist
        result = getHTTPResponse(500, "This maturity does not exist", False)
    conn.close()
    return result


@get('/iso21827/m')
def getAll():
    """Get all maturities"""

    # Get the connection
    conn = getConnection()

    # Get the maturity
    maturity_cursor = executeRequest("SELECT Id, LessThan, GreaterThan, Description FROM Maturity", conn)

    maturities = []
    for row in maturity_cursor.fetchall():
        maturity = Maturity()
        maturity.id = row[0]
        maturity.less_than = row[1]
        maturity.greater_than = row[2]
        maturity.description = row[3]
        maturities.append(maturity)

    conn.close()
    return getHTTPResponse(200, maturities)


@post('/iso21827/m/<params>')
def setResponses(**params):
    """Set the response of the user for a defined question"""

    result = None

    if len(params) != 12:
        result = getHTTPResponse(500, 'You must set responses for all questions', False)
    else:
        # SQL Server DB connection
        conn = getConnection()

        # Get the user IP address
        ip = request.environ.get('REMOTE_ADDR')

        # Delete all responses of the users
        executeRequest("DELETE FROM User_Response WHERE User_Response.User = '{}'".format(ip), conn)

        count = 1
        for response_value in params:
            # Get the response id
            response_cursor = executeRequest("SELECT Id FROM Response WHERE Response.Value = {}".format(int(response_value)),
                                             conn)
            response_id_value = response_cursor.fetchone()
            if response_id_value is None:
                result = getHTTPResponse(500,
                                         'The response value {} for the question {} does not exist'.format(
                                             str(response_value), count),
                                         False)
                break
            else:
                executeRequest(
                    "INSERT INTO User_Response(IdQuestion, IdResponse, User) VALUES ({}, {}, '{}')".format(
                        count, int(response_id_value[0]), ip), conn)

                count += 1
        # Calculate the maturity
        result = getMaturity(request.environ.get('REMOTE_ADDR'), conn)
        conn.commit()
        conn.close()

    return result
