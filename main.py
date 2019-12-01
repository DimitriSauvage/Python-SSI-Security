from assets.bottle import run, Bottle, get, HTTPResponse, put, request
from database.sqlServer import executeRequest, getConnection
from response import responseApp
import pyodbc

# Get app
mainApp = Bottle()

# Include others api controllers
mainApp.merge(responseApp);


@get('/iso21827/q/<id>')
def getQuestion(id):
    # Get the connection
    conn = getConnection()

    # Get the question
    result = None
    question_cursor = executeRequest("SELECT Question FROM Question WHERE Question.Id = " + id)
    question_response = question_cursor.fetchone()
    if question_response is not None:
        result = question_response[0]
        # Get the responses
        responses_cursor = executeRequest("SELECT Reponse FROM Reponse WHERE IdQuestion = " + id + " ORDER BY Valeur")
        for response in responses_cursor:
            result += '<br/>' + response[0]

    conn.close()
    return HTTPResponse(status=200, body=result)


@put('/iso21827/q/<question_id>/r/<response>')
def setResult(question_id, response):
    # SQL Server DB connection
    conn = getConnection()

    # Get the user IP address
    ip = request.environ.get('REMOTE_ADDR')

    # Check if the user has already answered to the question
    response_id = None
    has_answered_cursor = executeRequest(
        "SELECT Id FROM Utilisateur_reponse WHERE IdQuestion = {} AND Utilisateur = '{}'".format(question_id, ip))
    response_id = has_answered_cursor.fetchone()

    if response_id is not None:
        executeRequest("UPDATE Utilisateur_reponse SET IdReponse = {} WHERE Id = {}".format(response, response_id))
    else:
        executeRequest("INSERT INTO Utilisateur_reponse(IdQuestion, IdReponse, Utilisateur) VALUES ({}, {}, '{}')".format(question_id, response, ip))

    return HTTPResponse(status=204, body="Response saved successfully")


run(host='localhost', port=8080, debug=True)
