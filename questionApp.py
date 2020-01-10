from assets.bottle import Bottle, get
from database.sqlServer import executeRequest, getConnection

# Get app
from helpers.HTTPResponseHelper import getHTTPResponse
from models.answer import Response
from models.question import Question

questionApp = Bottle()


@get('/iso21827/q/<identifier>')
def getQuestion(identifier):
    """Get a question with is responses"""
    result = None

    # Get the connection
    conn = getConnection()

    # Get the question
    question_cursor = executeRequest("""SELECT Question.Id, Question.IdLevel, Question.Question,
                                                Response.Response, Response.Value, Response.Id
                                        FROM Question 
                                        INNER JOIN Response ON Question.Id = Response.IdQuestion
                                        WHERE Question.Id = """ + identifier + """ 
                                        ORDER BY Response.Value""", conn)
    if question_cursor is not None:
        question = None
        for row in question_cursor.fetchall():
            # Question
            if question is None:
                question = Question()
                question.id = row[0]
                question.id_level = row[1]
                question.question = row[2]

            # Responses
            response = Response()
            response.response = row[3]
            response.value = row[4]
            response.id = row[5]

            question.responses.append(response)

            result = getHTTPResponse(200, question)
    else:
        # Question does not exist
        result = getHTTPResponse(500, "This question does not exist", False)
    conn.close()
    return result


@get('/iso21827/q')
def getAll():
    """Get all questions with their responses"""

    # Get the connection
    conn = getConnection()

    # Get the questions
    questions_cursor = executeRequest("""SELECT Question.Id, Question.Question, Question.IdLevel,
                                                Response.Id, Response.Value, Response.Response 
                                         FROM Question 
                                         INNER JOIN Response ON Question.Id = Response.IdQuestion
                                         ORDER BY Question.Id, Response.Value""", conn)

    questions = []
    current_question = None
    for row in questions_cursor.fetchall():
        # Question
        if current_question is None or current_question.id != row[0]:
            current_question = Question()
            current_question.id = row[0]
            current_question.question = row[1]
            current_question.id_level = row[2]
            questions.append(current_question)

        # Responses
        response = Response()
        response.id = row[3]
        response.value = row[4]
        response.response = row[5]
        response.id_question = current_question.id
        current_question.responses.append(response)

    conn.close()

    result = getHTTPResponse(200, questions)
    return result
