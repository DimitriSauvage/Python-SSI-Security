import pyodbc


# Get a new connection
def getConnection(server='localhost', database='ISO_21827', username='ISO21827', password='Not24get'):
    connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server \
                        + ';DATABASE=' + database \
                        + ';UID=' + username \
                        + ';PWD=' + password
    return pyodbc.connect(connection_string)


# Execute a request
def executeRequest(request, connection):
    cursor = connection.cursor()
    return cursor.execute(request)
