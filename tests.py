import sys
import unittest
import subprocess
import os

class TestAssembler(unittest.TestCase):
    def setUp(self):
        self.assembler = 'python assembler.py'  # Команда для запуска ассемблера
        self.temp_asm = 'temp_test.asm'
        self.temp_bin = 'temp_test.bin'
        self.temp_log = 'temp_test_log.json'

    def tearDown(self):
        for file in [self.temp_asm, self.temp_bin, self.temp_log]:
            if os.path.exists(file):
                os.remove(file)

    def run_assembler(self, asm_code):
        """Запуск ассемблера с заданным кодом."""
        with open(self.temp_asm, 'w', encoding='utf-8') as f:
            f.write(asm_code)
        cmd = [sys.executable, '/Users/user/PycharmProjects/anya/assembler.py',
               self.temp_asm, self.temp_bin, self.temp_log]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            print(f"Ошибка: {result.stderr.decode('utf-8')}")
        self.assertEqual(result.returncode, 0, "Ассемблер завершился с ошибкой.")

        # Возвращаем бинарный файл как байты
        with open(self.temp_bin, 'rb') as f:
            return f.read()

    def test_load_const(self):
        """Тест команды LOAD_CONST (A=87, B=4, C=40)."""
        asm_code = "LOAD_CONST 4, 40\n"
        expected_bytes = bytes([0x57, 0x82, 0x02])  # Ожидаемые байты
        actual_bytes = self.run_assembler(asm_code)
        self.assertEqual(actual_bytes, expected_bytes, "LOAD_CONST сгенерировала неверные байты.")

    def test_load_mem(self):
        """Тест команды LOAD_MEM (A=111, B=997, C=1, D=31)."""
        asm_code = "LOAD_MEM 997, 1, 31\n"  # Добавлены все 4 операнда
        expected_bytes = bytes([0xEF, 0xF2, 0x09, 0x1F])  # Ожидаемые байты
        actual_bytes = self.run_assembler(asm_code)
        self.assertEqual(actual_bytes, expected_bytes, "LOAD_MEM сгенерировала неверные байты.")

    def test_store_mem(self):
        """Тест команды STORE_MEM (A=95, B=26, C=98, D=1)."""
        asm_code = "STORE_MEM 26, 98, 1\n"
        expected_bytes = bytes([0x5F, 0x2D, 0x06, 0x01])  # Ожидаемые байты
        actual_bytes = self.run_assembler(asm_code)
        self.assertEqual(actual_bytes, expected_bytes, "STORE_MEM сгенерировала неверные байты.")

    def test_abs(self):
        """Тест команды ABS (A=64, B=12, C=18)."""
        asm_code = "ABS 12, 18\n"
        expected_bytes = bytes([0x40, 0x26, 0x01])  # Ожидаемые байты
        actual_bytes = self.run_assembler(asm_code)
        self.assertEqual(actual_bytes, expected_bytes, "ABS сгенерировала неверные байты.")


if __name__ == '__main__':
    unittest.main()