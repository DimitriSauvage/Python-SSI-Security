from database.sqlServer import executeRequest, getConnection
from helpers.HTTPResponseHelper import getHTTPResponse
from models.maturity import Maturity


def getMaturity(ip, conn=getConnection()):
    """Get the maturity of the users"""
    result = None

    # Check if all questions are responded
    responses_cursor = executeRequest("""SELECT COUNT(*)
                                            FROM User_Response 
                                            WHERE User_Response.[User] = '{}'""".format(ip), conn)

    if responses_cursor is not None and int(responses_cursor.fetchone()[0]) == 12:
        # Get the maturity for the user
        maturity_cursor = executeRequest(
            """SELECT Id, Description, GreaterThan, LessThan
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
            row = maturity_cursor.fetchone()
            maturity = Maturity()
            maturity.id = row[0]
            maturity.description = row[1]
            maturity.greater_than = row[2]
            maturity.less_than = row[3]
            result = getHTTPResponse(200, maturity)
        else:
            result = getHTTPResponse(500, "Impossible to calculate the result", False)
    else:
        # Error
        result = getHTTPResponse(500, "You do not have responded all questions", False)

    conn.close()

    return result
