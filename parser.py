def parse_qa(path):
    with open(path, 'r', encoding='KOI8-R') as file:
        file_contents = file.read()

    questions = []
    answers = []

    for passage in file_contents.split('\n\n'):
        if passage.startswith('Вопрос') or passage.startswith('\nВопрос'):
            questions.append(passage.replace('\n', ' '))
        elif passage.startswith('Ответ') or passage.startswith('\nОтвет'):
            answers.append(passage.replace('\n', ' '))

    qa_dict = dict(zip(questions, answers))
    return qa_dict
