from assets.bottle import Bottle, get
from database.sqlServer import executeRequest, getConnection
from helpers.HTTPResponseHelper import getHTTPResponse

from models.answer import Response
from models.level import Level
from models.question import Question

# Get app
levelApp = Bottle()


@get('/iso21827/l/<identifier>')
def getLevel(identifier):
    """Get a level with its questions and their responses"""

    # Get the connection
    conn = getConnection()

    # Get the question
    question_cursor = executeRequest(
        """SELECT Level.Id, Level.Title, Question.Id, Question.Question, Response.Value, Response.Response, Response.Id
        FROM Level 
        INNER JOIN Question ON Level.Id = Question.IdLevel 
        INNER JOIN Response ON Question.Id = Response.IdQuestion 
        WHERE Level.Id = """ + identifier + """
        ORDER BY Question.Id, Response.Value""", conn)

    if question_cursor is not None:
        level = None
        current_question = None
        for row in question_cursor.fetchall():
            # Title
            if level is None:
                level = Level()
                level.id = row[0]
                level.title = row[1]

            # Question
            if current_question is None or current_question.id != row[1]:
                current_question = Question()
                current_question.id = row[2]
                current_question.question = row[3]
                current_question.id_level = level.id
                level.questions.append(current_question)

            # Responses
            Level.Id, Level.Title, Question.Id, Question.Question, Response.Value, Response.Response, Response.Id
            response = Response()
            response.value = row[4]
            response.response = row[5]
            response.id = row[6]
            response.id_question = current_question.id
            current_question.responses.append(response)

        # Set the result
        result = getHTTPResponse(200, level)
    else:
        # Level does not exist
        result = getHTTPResponse(500, "This level does not exist", False)

    conn.close()

    return result


@get('/iso21827/l')
def getAll():
    """Get all levels with their questions and their responses"""

    # Get the connection
    conn = getConnection()

    # Get the question
    question_cursor = executeRequest(
        """SELECT Level.Id, Level.Title, Question.Id, Question.Question, Response.Value, Response.Response, Response.Id
        FROM Level 
        INNER JOIN Question ON Level.Id = Question.IdLevel 
        INNER JOIN Response ON Question.Id = Response.IdQuestion 
        ORDER BY Level.Id, Question.Id, Response.Value""", conn)
    levels = []
    current_level = None
    current_question = None
    for row in question_cursor.fetchall():
        # New level with title
        if current_level is None or current_level.id != row[0]:
            current_level = Level()
            current_level.id = row[0]
            current_level.title = row[1]
            levels.append(current_level)

        # Question
        if current_question is None or current_question.id != row[2]:
            current_question = Question()
            current_question.id = row[2]
            current_question.id_level = current_level.id
            current_question.question = row[3]
            current_level.questions.append(current_question)

        # Responses
        response = Response()
        response.value = row[4]
        response.response = row[5]
        response.id = row[6]
        response.id_question = current_question.id
        current_question.responses.append(response)

    # Set the result
    result = getHTTPResponse(200, levels)
    conn.close()

    return result
