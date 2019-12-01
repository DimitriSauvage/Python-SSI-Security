from assets.bottle import route, Bottle

responseApp = Bottle()

@route('/responses')
def get_all():
    """

    :return:
    """
    return "TEST!!!"
