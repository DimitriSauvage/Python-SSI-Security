from assets.bottle import Bottle, put, request
from database.sqlServer import executeRequest, getConnection

# Get app
from helpers.HTTPResponseHelper import getHTTPResponse

responseApp = Bottle()


@put('/iso21827/q/<question_id>/r/<response>')
def setResponse(question_id, response):
    """Set the response of the user for a defined question"""

    result = ''

    # SQL Server DB connection
    conn = getConnection()

    # Get the user IP address
    ip = request.environ.get('REMOTE_ADDR')

    # Get the Id of the response
    response_cursor = executeRequest("""SELECT Id
                                        FROM Response
                                        WHERE Response.Value = """ + str(response) + """
                                        AND Response.IdQuestion = """ + str(question_id), conn)
    if response_cursor is None:
        result = getHTTPResponse(500, "This response does not exist for this question", False)
    else:
        response_id = response_cursor.fetchone()[0]

        # Check if the user has already responded to the question
        has_responded_cursor = executeRequest(
            "SELECT Id FROM User_Response WHERE IdQuestion = {} AND [User] = '{}'".format(int(question_id), ip), conn)
        user_response_id = has_responded_cursor.fetchone()[0]

        if user_response_id is not None:
            executeRequest(
                "UPDATE User_Response SET IdResponse = {} WHERE Id = {}".format(response_id, user_response_id), conn)

            result = getHTTPResponse(204, "", False)
        else:
            executeRequest(
                "INSERT INTO User_Response(IdQuestion, IdResponse, [User]) VALUES ({}, {}, '{}')".format(
                    question_id, response_id, ip), conn)
            result = getHTTPResponse(201, "Response created successfully", False)

        # Commit entries
        conn.commit()
    conn.close()
    return result
