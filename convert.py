import os
import re
from bs4 import BeautifulSoup

def extract_messages():
    # Ищем все файлы формата messages.html, messages2.html и т.д.
    all_files = os.listdir('.')
    msg_files = [f for f in all_files if re.match(r'messages\d*\.html', f)]
    
    # Сортируем файлы правильно: messages.html (первый), затем messages2.html и т.д.
    def get_file_number(name):
        match = re.search(r'messages(\d+)\.html', name)
        return int(match.group(1)) if match else 1

    msg_files.sort(key=get_file_number)
    
    last_sender = "Неизвестен"
    output_filename = 'all_messages_combined.txt'
    
    print(f"Найдено файлов для обработки: {len(msg_files)}")
    
    with open(output_filename, 'w', encoding='utf-8') as out_file:
        for file_path in msg_files:
            print(f"Обработка {file_path}...")
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                
                # Находим все блоки сообщений
                messages = soup.find_all('div', class_='message')
                
                for msg in messages:
                    # Пропускаем служебные сообщения (о смене даты, закрепленные и т.д.)
                    if 'service' in msg.get('class', []):
                        continue
                        
                    body = msg.find('div', class_='body')
                    if not body:
                        continue
                    
                    # Определяем отправителя (ник). В "склеенных" сообщениях ника нет, берем последний
                    sender_div = body.find('div', class_='from_name', recursive=False)
                    if sender_div:
                        last_sender = sender_div.get_text(strip=True)
                    
                    # Извлекаем дату и время из атрибута title блока с временем
                    date_div = body.find('div', class_='date', recursive=False)
                    date_str, time_str = "??.??.????", "??:??"
                    if date_div and 'title' in date_div.attrs:
                        # Пример title: "09.03.2023 21:37:49 UTC+05:00"
                        full_date_info = date_div['title']
                        match = re.search(r'(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2})', full_date_info)
                        if match:
                            date_str, time_str = match.groups()
                    
                    # Извлекаем текст сообщения
                    text_div = msg.find('div', class_='text')
                    if text_div:
                        # separator=' ' заменяет <br> на пробелы, strip убирает пустоты
                        message_text = text_div.get_text(separator=' ', strip=True)
                        # Очищаем от переносов строк внутри сообщения, чтобы была одна строка
                        clean_text = message_text.replace('\n', ' ').replace('\r', '')
                        
                        # Формируем строку: "ник", "дата", "время": "сообщение"
                        line = f'"{last_sender}", "{date_str}", "{time_str}": "{clean_text}"\n'
                        out_file.write(line)

    print(f"\nГотово! Все сообщения объединены в файл: {output_filename}")

if __name__ == "__main__":
    try:
        extract_messages()
    except Exception as e:
        print(f"Произошла ошибка: {e}")