from assets.bottle import run, Bottle, get, HTTPResponse, put, request
from database.sqlServer import executeRequest, getConnection

# Get app
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
    answer_cursor = executeRequest("""SELECT Id
                                        FROM Response
                                        WHERE Response.Value = """ + str(response) + """
                                        AND Response.IdQuestion = """ + str(question_id), conn)
    if answer_cursor is None:
        result = HTTPResponse(status=500, body="This answer does not exist for this question")
    else:
        response_id = answer_cursor.fetchone()[0]

        # Check if the user has already answered to the question
        has_answered_cursor = executeRequest(
            "SELECT Id FROM User_Response WHERE IdQuestion = {} AND [User] = '{}'".format(int(question_id), ip), conn)
        user_response_id = has_answered_cursor.fetchone()[0]

        if user_response_id is not None:
            executeRequest(
                "UPDATE User_Response SET IdResponse = {} WHERE Id = {}".format(response_id, user_response_id), conn)
            result = HTTPResponse(status=204)
        else:
            executeRequest(
                "INSERT INTO User_Response(IdQuestion, IdResponse, [User]) VALUES ({}, {}, '{}')".format(
                    question_id, response_id, ip), conn)
            result = HTTPResponse(status=201, body="Response created successfully")

        # Commit entries
        conn.commit()
    conn.close()
    return result
