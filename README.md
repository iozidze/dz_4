Разработать ассемблер и интерпретатор для учебной виртуальной машины
(УВМ). Система команд УВМ представлена далее.

Для ассемблера необходимо разработать читаемое представление команд
УВМ. Ассемблер принимает на вход файл с текстом исходной программы, путь к
которой задается из командной строки. Результатом работы ассемблера является
бинарный файл в виде последовательности байт, путь к которому задается из
командной строки. Дополнительный ключ командной строки задает путь к файлулогу, в котором хранятся ассемблированные инструкции в духе списков
“ключ=значение”, как в приведенных далее тестах.

Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ
и сохраняет в файле-результате значения из диапазона памяти УВМ. Диапазон
также указывается из командной строки.

Форматом для файла-лога и файла-результата является json.

Необходимо реализовать приведенные тесты для всех команд, а также
написать и отладить тестовую программу.

Загрузка константы

A B C

Биты 0—6 Биты 7—11 Биты 12—19
87 Адрес Константа
Размер команды: 3 байт. Операнд: поле C. Результат: регистр по адресу,
которым является поле B.
Тест (A=87, B=4, C=40):
0x57, 0x82, 0x02
Чтение значения из памяти
A B C D
Биты 0—6 Биты 7—18 Биты 19—23 Биты 24—28
111 Смещение Адрес Адрес

Размер команды: 4 байт. Операнд: значение в памяти по адресу, которым
является сумма адреса (регистр по адресу, которым является поле D) и смещения
(поле B). Результат: регистр по адресу, которым является поле C.

Тест (A=111, B=997, C=1, D=31):

0xEF, 0xF2, 0x09, 0x1F

Запись значения в память

A B C D

Биты 0—6 Биты 7—11 Биты 12—23 Биты 24—28

95 Адрес Смещение Адрес

Размер команды: 4 байт. Операнд: регистр по адресу, которым является поле

B. Результат: значение в памяти по адресу, которым является сумма адреса
(регистр по адресу, которым является поле D) и смещения (поле C).

Тест (A=95, B=26, C=98, D=1):

0x5F, 0x2D, 0x06, 0x01

Унарная операция: abs()

A B C

Биты 0—6 Биты 7—11 Биты 12—16

64 Адрес Адрес

Размер команды: 3 байт. Операнд: значение в памяти по адресу, которым
является регистр по адресу, которым является поле C. Результат: регистр по
адресу, которым является поле B.

Тест (A=64, B=12, C=18):

0x40, 0x26, 0x01

Тестовая программа

Выполнить поэлементно операцию abs() над вектором длины 7. Результат
записать в новый вектор.