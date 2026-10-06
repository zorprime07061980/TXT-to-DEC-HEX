def convert_card_code(wiegand_str):
    """Конвертирует одну строку вида '037,01594' в HEX и DEC."""
    try:
        # Очищаем строку от лишних пробелов и символов переноса строки
        clean_str = wiegand_str.strip()

        # Разделяем по запятой
        facility_code_str, card_id_str = clean_str.split(',')

        facility_code = int(facility_code_str)
        card_id = int(card_id_str)

        # Конвертация в HEX (1 байт на Facility, 2 байта на Card ID)
        hex_code = f"{facility_code:02X}{card_id:04X}"

        # Конвертация в полный DEC (10 знаков с ведущими нулями)
        dec_code = f"{int(hex_code, 16):010d}"

        return clean_str, hex_code, dec_code
    except ValueError:
        # Если строка пустая, повреждена или имеет неверный формат
        return None, None, None


def process_file_to_excel(input_filename, output_filename):
    """Читает входной файл и записывает результат через точку с запятой (CSV для Excel)."""
    with open(input_filename, 'r', encoding='utf-8') as infile, \
            open(output_filename, 'w', encoding='utf-8') as outfile:

        # Записываем строку заголовков для Excel
        outfile.write("input_code;HEX;DEC\n")

        for line in infile:
            # Пропускаем абсолютно пустые строки
            if not line.strip():
                continue

            orig_str, hex_res, dec_res = convert_card_code(line)

            if orig_str and hex_res and dec_res:
                # Записываем строку, разделяя данные точкой с запятой
                # Обратите внимание: для DEC добавлен знак ', чтобы Excel не стёр ведущие нули
                outfile.write(f"{orig_str};{hex_res};'{dec_res}\n")


# Имена файлов для работы
input_file = "input_cards.txt"
output_file = "output_cards.csv"  # Расширение .csv лучше подходит для Excel

# Запуск конвертации
process_file_to_excel(input_file, output_file)
print(f"Конвертация завершена! Файл для Excel сохранен как: {output_file}")
