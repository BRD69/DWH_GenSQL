def get_text_null(text: str) -> str:
    if text == "" or text == 'null':
        return 'null'
    else:
        return f"N'{text}'"


def get_length(text):
    try:
        return int(text)
    except:
        return 'null'


def get_state(state):
    if state == 2:
        return 1
    else:
        return state


def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return s[0] + ''.join(i.capitalize() for i in s[1:])