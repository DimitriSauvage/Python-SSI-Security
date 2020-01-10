def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""
    return obj.__dict__
