from assets.bottle import run, Bottle, get, HTTPResponse, put, request
from database.sqlServer import executeRequest, getConnection

# Get app
resultApp = Bottle()


@get('/iso21827/result')
def getResult():
    """Get the maturity of the user"""
    result = None

    # Get the user
    ip = request.environ.get('REMOTE_ADDR')

    # Get the connection
    conn = getConnection()

    # Check if all questions are answered
    answers_cursor = executeRequest("""SELECT COUNT(*)
                                        FROM User_Response 
                                        WHERE User_Response.[User] = '{}'""".format(ip), conn)

    if answers_cursor is not None and int(answers_cursor.fetchone()[0]) == 12:
        # Get the maturity for the user
        maturity_cursor = executeRequest(
            """SELECT Description
                FROM Maturity
                WHERE (SELECT SUM(T.[Value]) AS [Value]
                FROM ( SELECT MAX(Response.Value) AS [Value], Level.Id
                FROM User_Response
                INNER JOIN Response ON User_Response.IdResponse = Response.Id
                INNER JOIN Question on User_Response.IdQuestion = Question.Id
                INNER JOIN Level on Question.IdLevel = Level.Id
                WHERE [User] = '{}'
                GROUP BY Level.Id) AS T
                ) BETWEEN Maturity.GreaterThan AND Maturity.LessThan""".format(ip), conn)
        if maturity_cursor is not None:
            result = HTTPResponse(status=200, body="Maturity result : " + maturity_cursor.fetchone()[0])
        else:
            result = HTTPResponse(status=500, body="Impossible to calculate the result")
    else:
        # Error
        result = HTTPResponse(status=500, body="You do not have answered all questions")

    conn.close()
    return result

