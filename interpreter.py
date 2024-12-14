import sys
import json

def abs_val(value):
    return abs(value)

class Interpreter:
    def __init__(self, binary_file, result_file, mem_start, mem_end):
        self.binary_file = binary_file
        self.result_file = result_file
        self.mem_start = mem_start
        self.mem_end = mem_end
        self.memory = [0] * 256
        self.registers = [0] * 32
        self.pc = 0  # Program counter
        self.code = b""

    def load_code(self):
        """Загружает бинарный код в память."""
        with open(self.binary_file, 'rb') as f:
            self.code = f.read()

    def fetch_instruction(self):
        """Извлекает текущую инструкцию."""
        if self.pc >= len(self.code):
            return None
        return int.from_bytes(self.code[self.pc:self.pc + 4], byteorder='little', signed=False)

    def execute_instruction(self, instr):
        """Обрабатывает инструкцию."""
        opcode = instr & 0x7F
        if opcode == 87:  # LOAD_CONST
            B = (instr >> 7) & 0x1F
            C = (instr >> 12) & 0xFF
            if C<246/2:
                self.registers[B] = C
            else:
                self.registers[B] = C-247
            self.pc += 3
            print(f"LOAD_CONST: B={B}, C={C} -> reg[{B}]={self.registers[B]}")

        elif opcode == 111:  # LOAD_MEM
            B = (instr >> 7) & 0xFFF
            C = (instr >> 19) & 0x1F
            D = (instr >> 24) & 0x1F
            addr = self.registers[D] + B
            if addr < len(self.memory):
                self.registers[C] = self.memory[addr]
            else:
                print(f"Ошибка: попытка доступа к недопустимому адресу памяти {addr}")
            self.pc += 4
            print(f"LOAD_MEM: B={B}, C={C}, D={D} -> mem[{addr}] -> reg[{C}]={self.registers[C]}")

        elif opcode == 95:  # STORE_MEM
            B = (instr >> 7) & 0x1F
            C = (instr >> 12) & 0xFFF
            D = (instr >> 24) & 0x1F
            addr = self.registers[D] + C
            if addr < len(self.memory):
                self.memory[addr] = self.registers[B]
            else:
                print(f"Ошибка: попытка записи в недопустимый адрес памяти {addr}")
            self.pc += 4
            print(f"STORE_MEM: B={B}, C={C}, D={D} -> reg[{B}]={self.registers[B]} -> mem[{addr}]={self.memory[addr]}")

        elif opcode == 64:  # ABS
            B = (instr >> 7) & 0x1F
            C = (instr >> 12) & 0x1F
            self.registers[B] = abs_val(self.registers[C])
            self.pc += 3
            print(f"ABS: B={B}, C={C} -> reg[{B}]={self.registers[B]} (abs of reg[{C}]={self.registers[C]})")

        else:
            raise ValueError(f"Неизвестная команда: {opcode}")

    def run(self):
        """Запускает интерпретатор."""
        try:
            self.load_code()
            while self.pc < len(self.code):
                instr = self.fetch_instruction()
                if instr is None:
                    break
                self.execute_instruction(instr)

            # Сохраняем результаты в файл
            result = {i: self.memory[i] for i in range(self.mem_start, self.mem_end + 1)}
            with open(self.result_file, 'w', encoding='utf-8') as f_out:
                json.dump(result, f_out, ensure_ascii=False, indent=2)

            print(f"Интерпретация завершена. Результат сохранён в {self.result_file}")

        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")


def main():
    if len(sys.argv) < 5:
        print("Usage: python interpreter.py <binary_file> <result_file> <mem_start> <mem_end>")
        sys.exit(1)

    binary_file = sys.argv[1]
    result_file = sys.argv[2]
    mem_start = int(sys.argv[3])
    mem_end = int(sys.argv[4])

    interpreter = Interpreter(binary_file, result_file, mem_start, mem_end)
    interpreter.run()


if __name__ == "__main__":
    main()