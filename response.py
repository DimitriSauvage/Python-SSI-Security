from assets.bottle import run, Bottle, get, HTTPResponse, put, request
from database.sqlServer import executeRequest, getConnection

# Get app
responseApp = Bottle()


@put('/iso21827/q/<question_id>/r/<response>')
def setResponse(question_id, response):
    """Set the response of the user for a defined question"""
    # SQL Server DB connection
    conn = getConnection()

    # Get the user IP address
    ip = request.environ.get('REMOTE_ADDR')

    # Check if the user has already answered to the question
    response_id = None
    has_answered_cursor = executeRequest(
        "SELECT Id FROM User_Response WHERE IdQuestion = {} AND User = '{}'".format(question_id, ip))
    response_id = has_answered_cursor.fetchone()

    if response_id is not None:
        executeRequest("UPDATE User_Response SET IdResponse = {} WHERE Id = {}".format(response, response_id))
    else:
        executeRequest(
            "INSERT INTO User_Response(IdQuestion, IdResponse, User) VALUES ({}, {}, '{}')".format(
                question_id, response, ip))

    return HTTPResponse(status=204, body="Response saved successfully")
