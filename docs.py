documents = [
    {'type': 'passport', 'number': '2207 876234', 'name': 'Василий Гупкин'},
    {'type': 'invoice', 'number': '11-2', 'name': 'Геннадий Покемонов'},
    {'type': 'insurance', 'number': '10006', 'name': 'Аристарх Павлов'}
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}

command = input("Введите команду: ")

if command == 'p':
    doc_num = input("Введите номер документа: ")
    for doc in documents:
        if doc.get('number') == doc_num:
            print(doc.get('name'))
            break

elif command == 's':
    doc_num = input("Введите номер документа: ")
    for shelf, docs in directories.items():
        if doc_num in docs:
            print(f"Документ хранится на полке: {shelf}")
            break
