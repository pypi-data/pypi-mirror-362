def validate_string(question:str, error_message:str) -> str:
    '''summary_ Validate an answer to not be empty

    Args:
        question (str):
        error_message (str): Message to show when the answer is invalid

    Returns:
        str: Valid answer
    '''

    while True:
        try:
            answer = input(question).strip()
            if answer != '':
                break
            else:
                print(error_message)
        except:
            print(error_message)
    return answer

def validate_int(question:str, error_message:str) -> int:
    '''summary_ Validate an answer to be an int

    Args:
        question (str):
        error_message (str): Message to show when the answer is invalid

    Returns:
        int: Valid answer
    '''

    while True:
        answer = validate_string(question, error_message)
        try:
            return int(answer)
        except:
            print(error_message)

def validate_float(question:str, error_message:str, use_comma=True) -> float:  
    '''summary_ Validate an answer to be an float

    Args:
        question (str):
        error_message (str): Message to show when the answer is invalid
        use_comma (bool, optional): Control if the anser is 0.25 or 0,25. Defaults to True.

    Returns:
        float: Valid answer
    '''

    while True:
        answer = validate_string(question, error_message)
        try:
            if use_comma:
                answer = answer.replace(',', '.')
            return float(answer)
        except:
            print(error_message)

def validate_option(menu_title:str, options:list[str], question: str, error_message:str) -> int:
    '''summary_ Validate an answer to be an int between 1 and the size of *options*

    Examples:
        *menu_title*\n
        [ 1 ] Option A\n
        [ 2 ] Option B\n
        [ 3 ] Option C\n

    Args:
        menu_title (str): 
        options (list[str]):
        question (str):
        error_message (str): Message to show when the answer is invalid

    Returns:
        int: Valid option
    '''

    print(menu_title)
    print()
    for index, option in enumerate(options, start=1):
        print(f'[ {index} ] {option}')
    print()
    while True:
        answer = validate_int(question, error_message)
        if 1 <= answer <= len(options):
            return answer
        else:
            print(error_message)
