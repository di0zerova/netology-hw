import csv

clients = []
with open('web_clients_correct.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        clients.append(row)

descriptions = []
for client in clients:

    name = client['name']
    gender = client['sex']
    age = client['age']
    device = client['device_type']
    browser = client['browser']
    bill = client['bill']


    region = client['region']
    if region == '-':
        region = 'неизвестный регион'
    else:
        region = region.split('/')[0].strip()


    if gender == 'female':
        gender1 = 'женского'
        action = 'совершила'
    else:
        gender1 = 'мужского'
        action = 'совершил'


    if device == 'mobile':
        devicedesu = 'мобильного устройства'
    elif device == 'tablet':
        devicedesu = 'планшета'
    elif device == 'laptop':
        devicedesu = 'ноутбука'
    elif device == 'desktop':
        devicedesu = 'компьютера'
    else:
        devicedesu = device


    text = (f"Пользователь {name} {gender1} пола, {age} лет {action} покупку на "
            f"{bill} у.е. с {devicedesu} через браузер {browser}. "
            f"Регион, из которого совершалась покупка: {region}.")

    descriptions.append(text)


with open('descriptoins.txt', 'w') as file:
    for desc in descriptions:
        file.write(f"{desc}\n\n")