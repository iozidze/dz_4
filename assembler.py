import sys
import json


def parse_instruction(line):
    """Парсинг строки ассемблерного кода."""
    line = line.strip()
    if not line or line.startswith('#'):
        return None, None

    parts = line.split(None, 1)
    mnemonic = parts[0].upper()
    operands = parts[1].split(',') if len(parts) > 1 else []
    return mnemonic, [op.strip() for op in operands]


def validate_operands_count(mnemonic, operands, expected_count):
    """Проверка количества операндов."""
    if len(operands) != expected_count:
        raise ValueError(f"{mnemonic} требует {expected_count} операнд(а/ов), получено: {len(operands)}.")


def assemble_instruction(mnemonic, operands):
    """Генерация машинного кода для инструкции."""
    if mnemonic == 'LOAD_CONST':
        validate_operands_count(mnemonic, operands, 2)
        A = 87
        B = int(operands[0])
        C = int(operands[1])
        instr = (A & 0x7F) | ((B & 0x1F) << 7) | ((C & 0xFF) << 12)
        return instr.to_bytes(3, byteorder='little'), {"opcode": A, "B": B, "C": C}

    elif mnemonic == 'LOAD_MEM':
        validate_operands_count(mnemonic, operands, 3)
        A = 111
        B = int(operands[0])
        C = int(operands[1])
        D = int(operands[2])
        instr = (A & 0x7F) | ((B & 0xFFF) << 7) | ((C & 0x1F) << 19) | ((D & 0x1F) << 24)
        return instr.to_bytes(4, byteorder='little'), {"opcode": A, "B": B, "C": C, "D": D}

    elif mnemonic == 'STORE_MEM':
        validate_operands_count(mnemonic, operands, 3)
        A = 95
        B = int(operands[0])
        C = int(operands[1])
        D = int(operands[2])
        instr = (A & 0x7F) | ((B & 0x1F) << 7) | ((C & 0xFFF) << 12) | ((D & 0x1F) << 24)
        return instr.to_bytes(4, byteorder='little'), {"opcode": A, "B": B, "C": C, "D": D}

    elif mnemonic == 'ABS':
        validate_operands_count(mnemonic, operands, 2)
        A = 64
        B = int(operands[0])
        C = int(operands[1])
        instr = (A & 0x7F) | ((B & 0x1F) << 7) | ((C & 0x1F) << 12)
        return instr.to_bytes(3, byteorder='little'), {"opcode": A, "B": B, "C": C}

    else:
        raise ValueError(f"Неизвестная инструкция: {mnemonic}")


def main():
    if len(sys.argv) < 4:
        print("Usage: python assembler.py <input_file> <output_file> <log_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]

    instructions_log = []

    try:
        with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'wb') as f_out:
            for line in f_in:
                mnemonic, operands = parse_instruction(line)
                if mnemonic is None:
                    continue
                try:
                    instr_bytes, log_entry = assemble_instruction(mnemonic, operands)
                    f_out.write(instr_bytes)
                    instructions_log.append(log_entry)
                except ValueError as e:
                    print(f"Ошибка обработки строки: {line.strip()} - {e}")
                    sys.exit(1)

        with open(log_file, 'w', encoding='utf-8') as f_log:
            json.dump(instructions_log, f_log, ensure_ascii=False, indent=2)

        print(f"Сборка завершена. Бинарный файл: {output_file}, лог: {log_file}")

    except FileNotFoundError as e:
        print(f"Ошибка: файл не найден - {e.filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Неизвестная ошибка: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()