def remove(content, *useless: str):

    for char in useless:
        content = (str(content)).replace(char, '')

    return content

def convertList(_list, _split=False):
    string = ' '.join(_list)

    if _split:
        string = string.split(', ')

    return string




#example
#message = remove("('hello', 'bruh')", '(', ')', "'", ",")
