from assets.bottle import Bottle, get, HTTPResponse
from database.sqlServer import executeRequest, getConnection

# Get app
questionApp = Bottle()


@get('/iso21827/q/<identifier>')
def getQuestion(identifier):
    """Get a question with is answers"""
    result = None
    content = ""

    # Get the connection
    conn = getConnection()

    # Get the question
    question_cursor = executeRequest("""SELECT Question.Question, Response.Response, Response.Value
                                        FROM Question 
                                        INNER JOIN Response ON Question.Id = Response.IdQuestion
                                        WHERE Question.Id = """ + identifier + """ 
                                        ORDER BY Response.Value""", conn)
    if question_cursor is not None:
        has_question = False
        for row in question_cursor.fetchall():
            # Question
            if has_question is False:
                has_question = True
                content = row[0] + "<br/>"

            # Answers
            content += str(row[2]) + " - " + row[1]

            result = HTTPResponse(status=200, body=content)
    else:
        # Question does not exist
        result = HTTPResponse(status=500, body="This question does not exist")
    conn.close()
    return result


@get('/iso21827/q')
def getAll():
    """Get all questions with their answers"""
    result = None
    content = ""

    # Get the connection
    conn = getConnection()

    # Get the questions
    questions_cursor = executeRequest("""SELECT Question.Id, Question.Question, Response.Value, Response.Response 
                                         FROM Question 
                                         INNER JOIN Response ON Question.Id = Response.IdQuestion
                                         ORDER BY Question.Id, Response.Value""", conn)

    question_id = None
    for row in questions_cursor.fetchall():
        # Question
        if question_id is None or question_id != row[0]:
            content += row[1] + '</br>'
            question_id = row[0]

        # Answers
        content += str(row[2]) + ' - ' + row[3] + '<br/>'

    conn.close()

    result = HTTPResponse(status=200, body=content)
    return result
