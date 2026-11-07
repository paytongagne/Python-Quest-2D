def validate_frame(frame):
    errors = []
    if type(frame.get('id')) is not str or not frame['id']:
        errors.append('id')
    if type(frame.get('seq')) is not int or frame['seq'] < 0:
        errors.append('seq')
    if type(frame.get('value')) not in (int,float):
        errors.append('value')
    return errors
