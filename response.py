from assets.bottle import route, Bottle

responseApp = Bottle()

@route('/responses')
def getAll():
    return "TEST!!!"


