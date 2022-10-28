def name_correct(name):
    name = name.replace(' ', '_')
    name = name.replace('&', 'and')
    name = name.replace('<', '-')
    name = name.replace('>', '-')
    name = name.replace(':', '-')
    name = name.replace('"', "'")
    name = name.replace('/', '_')
    name = name.replace('\\', '_')
    name = name.replace('*', '_')
    name = name.replace('|', '_')
    name = name.replace('?', '_')
    return name