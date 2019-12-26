from assets.bottle import Bottle, get, HTTPResponse
from database.sqlServer import executeRequest, getConnection

# Get app
levelApp = Bottle()


@get('/iso21827/l/<identifier>')
def getLevel(identifier):
    """Get a level with its questions and their answers"""
    result = None
    content = ""

    # Get the connection
    conn = getConnection()

    # Get the question
    question_cursor = executeRequest(
        """SELECT Level.Title, Question.Id, Question.Question, Response.Value, Response.Response
        FROM Level 
        INNER JOIN Question ON Level.Id = Question.IdLevel 
        INNER JOIN Response ON Question.Id = Response.IdQuestion 
        WHERE Level.Id = """ + identifier + """
        ORDER BY Question.Id, Response.Value""", conn)

    if question_cursor is not None:
        has_title = False
        current_question_id = None
        for row in question_cursor.fetchAll():
            # Title
            if not has_title:
                content = row[0] + '<br/>'
                has_title = True

            # Question
            if current_question_id is None or current_question_id != row[1]:
                content += row[3] + '<br/>'
                current_question_id = row[1]

            # Answers
            content += row[4] + "<br/>"

        # Set the result
        result = HTTPResponse(status=200, body=content)
    else:
        # Level does not exist
        result = HTTPResponse(status=500, body="This level does not exist")

    conn.close()

    return result


@get('/iso21827/l')
def getAll():
    """Get all levels with their questions and their answers"""
    result = None
    content = ""

    # Get the connection
    conn = getConnection()

    # Get the question
    question_cursor = executeRequest(
        """SELECT Level.Id, Level.Title, Question.Id, Question.Question, Response.Value, Response.Response
        FROM Level 
        INNER JOIN Question ON Level.Id = Question.IdLevel 
        INNER JOIN Response ON Question.Id = Response.IdQuestion 
        ORDER BY Level.Id, Question.Id, Response.Value""", conn)

    current_level_id = None
    current_question_id = None
    for row in question_cursor.fetchAll():
        # Title
        if current_level_id is None or current_level_id != row[0]:
            content = row[1] + '<br/>'
            current_level_id = row[0]

        # Question
        if current_question_id is None or current_question_id != row[2]:
            content += row[3] + '<br/>'
            current_question_id = row[2]

        # Answers
        content += row[5] + "<br/>"

    # Set the result
    result = HTTPResponse(status=200, body=content)
    conn.close()

    return result
