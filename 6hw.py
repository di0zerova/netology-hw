import json


def create_funnel_streaming(visit_log_path, purchase_log_path, output_path):
    purchases = {}

    print("Чтение purchase_log.txt...")
    with open(purchase_log_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            try:
                data = json.loads(line.strip())
                user_id = data.get('user_id')
                category = data.get('category')
                if user_id and category:
                    purchases[user_id] = category
            except json.JSONDecodeError:
                continue

            if i % 100000 == 0:
                print(f"Обработано {i} строк из purchase_log.txt")

    print(f"Найдено {len(purchases)} покупок")

    print("Обработка visit_log.csv...")
    with open(visit_log_path, 'r', encoding='utf-8') as visit_file, \
            open(output_path, 'w', encoding='utf-8') as output_file:

        output_file.write('user_id,source,category\n')

        next(visit_file)

        processed_count = 0
        written_count = 0

        for line in visit_file:
            line = line.strip()
            if not line:
                continue

            parts = line.split(',')
            if len(parts) >= 2:
                user_id = parts[0]
                source = parts[1]

                if user_id in purchases:
                    category = purchases[user_id]
                    output_file.write(f'{user_id},{source},{category}\n')
                    written_count += 1

            processed_count += 1
            if processed_count % 100000 == 0:
                print(f"Обработано {processed_count} строк из visit_log.csv")

    print(f"Записано {written_count} строк в funnel.csv")


create_funnel_streaming('visit_log.csv', 'purchase_log.txt', 'funnel.csv')

print("\nПервые 3 строки файла funnel.csv:")
with open('funnel.csv', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i < 3:
            print(line.strip())
        else:
            break