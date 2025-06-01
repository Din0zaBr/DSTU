import pandas as pd
from deep_translator import GoogleTranslator
import json
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple
import threading
import math

# Глобальная блокировка для синхронизации вывода
print_lock = threading.Lock()


def translate_batch(texts: List[str], batch_size: int = 5) -> List[str]:
    """Переводит пакет текстов на русский язык"""
    translations = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        try:
            translator = GoogleTranslator(source='auto', target='ru')
            batch_translations = translator.translate_batch(batch)
            translations.extend(batch_translations)
        except Exception as e:
            with print_lock:
                print(f"Ошибка при переводе пакета: {e}")
            # В случае ошибки добавляем оригинальные тексты
            translations.extend(batch)
    return translations


def translate_chunk(chunk: List[Tuple[str, str]]) -> List[str]:
    """Обертка для перевода чанка сообщений"""
    texts = [msg for msg, _ in chunk]
    return translate_batch(texts)


def process_csv(input_file):
    print(f"Начинаем обработку файла: {input_file}")

    try:
        # Загрузка данных, пропускаем первую строку с заголовком
        df = pd.read_csv(input_file, skiprows=1, names=['index', 'label', 'message'])
        
        # Берем только первые 10 строк
        df = df.head(10)
        
        print(f"Будет переведено строк: {len(df)}")
        print("\nПримеры данных:")
        print(df)

        # Проверяем наличие данных
        if len(df) == 0:
            print("Ошибка: Файл пуст или не содержит данных")
            return

        # Проверяем наличие необходимых столбцов
        if 'message' not in df.columns or 'label' not in df.columns:
            print("Ошибка: В файле отсутствуют необходимые столбцы 'message' или 'label'")
            print(f"Найденные столбцы: {df.columns.tolist()}")
            return

        # Создаем список кортежей (текст, метка)
        messages_with_labels = [(row['message'], 'fraud' if row['label'] == 'spam' else 'neutral')
                                for _, row in df.iterrows()]

        print(f"\nПодготовлено сообщений для перевода: {len(messages_with_labels)}")
        print(f"Количество спам-сообщений: {sum(1 for _, label in messages_with_labels if label == 'fraud')}")
        print(f"Количество обычных сообщений: {sum(1 for _, label in messages_with_labels if label == 'neutral')}")

        # Разбиваем сообщения на части для параллельной обработки
        num_workers = 2  # Уменьшаем количество потоков для тестового перевода
        chunk_size = math.ceil(len(messages_with_labels) / num_workers)
        message_chunks = [messages_with_labels[i:i + chunk_size]
                          for i in range(0, len(messages_with_labels), chunk_size)]

        print(f"Размер чанка: {chunk_size}")
        print(f"Количество чанков: {len(message_chunks)}")

        # Открываем файлы для записи
        fraud_file = open('fraud_messages.json', 'w', encoding='utf-8')
        suspicious_file = open('neutral_messages.json', 'w', encoding='utf-8')

        # Записываем открывающую скобку массива
        fraud_file.write('[\n')
        suspicious_file.write('[\n')

        # Счетчики сообщений
        fraud_count = 0
        suspicious_count = 0

        # Флаг для запятых
        fraud_first = True
        suspicious_first = True

        print("\nНачинаем перевод...")

        # Параллельная обработка переводов
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            # Запускаем переводы для каждой части сообщений
            futures = []
            for chunk in message_chunks:
                future = executor.submit(translate_chunk, chunk)
                futures.append((future, chunk))

            # Обрабатываем результаты перевода
            for future, chunk in futures:
                translations = future.result()
                for (original, label), translated in zip(chunk, translations):
                    message_dict = {
                        "text": translated,
                        "label": label,
                        "original": original  # Добавляем оригинальный текст для проверки
                    }
                    json_str = json.dumps(message_dict, ensure_ascii=False)

                    if label == 'fraud':
                        if not fraud_first:
                            fraud_file.write(',\n')
                        fraud_file.write(json_str)
                        fraud_count += 1
                        fraud_first = False
                    else:
                        if not suspicious_first:
                            suspicious_file.write(',\n')
                        suspicious_file.write(json_str)
                        suspicious_count += 1
                        suspicious_first = False

                    if translated == original:
                        with print_lock:
                            print(f"Не удалось перевести сообщение: {original}")

        # Записываем закрывающую скобку массива
        fraud_file.write('\n]')
        suspicious_file.write('\n]')

        # Закрываем файлы
        fraud_file.close()
        suspicious_file.close()

        print(f"\nСоздано файлов:")
        print(f"- fraud_messages.json: {fraud_count} сообщений")
        print(f"- neutral_messages.json: {suspicious_count} сообщений")

    except Exception as e:
        print(f"Произошла ошибка при обработке файла: {str(e)}")


if __name__ == "__main__":
    process_csv('spam.csv')
