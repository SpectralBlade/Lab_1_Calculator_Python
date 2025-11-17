from constants import BINARY_OPERATORS, UNARY_OPERATORS, OPERATORS_DICT

def tokenize_rpn(expression: str) -> list:
    """
    Токенизатор для выражений в обратной польской нотации
    Аргумент:
        expression (str): Входное выражение в RPN
    Возвращаемое значение:
        list[tuple]: Список со считанными токенами. Каждый элемент = кортеж,
        включающий в себя тип токена (оператор/число) и его значение.
    """

    if not expression or not expression.strip():
        raise SyntaxError('На вход подана пустая строка')

    # Разделяем выражение по пробелам и удаляем пустые строки
    parts = [part for part in expression.split() if part]

    tokens = []
    stack = []  # Стек для проверки скобок
    bracket_content = []  # Содержимое текущих скобок (для взаимодействия со вложенными)
    in_brackets = False

    # Чтение токенов
    i = 0
    while i < len(parts):
        part = parts[i]

        # Обработка открывающей скобки
        if part == '(':
            stack.append('(')
            in_brackets = True
            bracket_content = []
            i += 1
            continue

        # Обработка закрывающей скобки
        if part == ')':
            if not stack or stack[-1] != '(':
                raise SyntaxError("Непарная закрывающая скобка")
            stack.pop()

            # Проверяем корректность выражения внутри скобок
            if not is_valid_rpn_expression(bracket_content):
                raise SyntaxError(f"Некорректное выражение в скобках: {' '.join(bracket_content)}")

            in_brackets = False
            i += 1
            continue

        # Если мы внутри скобок, добавляем токен в список их содержимого
        if in_brackets:
            bracket_content.append(part)

        # Обработка чисел и добавление их в стек
        if is_number(part):
            tokens.append(('NUMBER', float(part)))

        # Обработка бинарных операторов
        elif part in BINARY_OPERATORS:
            tokens.append(('BINARY_OPERATOR', part))

        # Обработка унарных операторов как отдельных токенов
        elif part in UNARY_OPERATORS:
            tokens.append(('UNARY_OPERATOR', part))

        else:
            raise SyntaxError(f"Нераспознанный токен: {part}\nПоддерживаемые токены: "
                              f"числа, круглые открывающие/закрывающие скобки, "
                              f"операторы (+, -, /, *, **, %, //)")

        i += 1

    # Проверяем, что все скобки закрыты
    if stack:
        raise SyntaxError("Непарная открывающая скобка")

    # Проверяем общую корректность выражения (без учета унарных операторов)
    if not is_valid_rpn_expression_final(tokens):
        raise SyntaxError("Некорректное выражение в обратной польской нотации")

    return tokens


def is_number(s):
    """
    Проверяет, является ли строка числом (целым или дробным).
    Аргумент:
        float: число
    Возвращаемое значение:
        bool: True, если число, и False, если нет
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_valid_rpn_expression(expression_parts):
    """
    Проверяет корректность выражения в скобках
    Аргумент:
        expression_parts (list): список с числами и операторами
    Возвращаемое значение:
        bool: True, если все ок, и False, если нет
    """
    stack_size = 0

    for part in expression_parts:
        if is_number(part):
            stack_size += 1
        elif part in BINARY_OPERATORS:
            if stack_size < 2:
                return False
            stack_size -= 1
        # Унарные операторы не учитываются -
        # не должны менять баланс стека для проверки RPN
        elif part in UNARY_OPERATORS:
            if stack_size < 1:
                raise SyntaxError(f'Некорректная постановка унарного знака '
                                  f'(вы поставили его в начале выражения в скобках)')

    return stack_size == 1

def is_valid_rpn_expression_final(tokens):
    """
    Проверяет корректность финального выражения в RPN
    с учетом типов токенов
    Аргумент:
        tokens (list[tuple]) - список с токенами - кортежи со значением
        и его типом
    Возвращаемое значение:
        bool - True, если стек верен и можно переходить
        к подсчету ответа, и False, если нет. ValueError при неверной постановке
        унарного знака (для дополнительного уточнения)
    """
    number_of_tokens = 0
    stack_size = 0

    for token_type, token_value in tokens:
        if token_type == 'NUMBER':
            stack_size += 1
        elif token_type == 'BINARY_OPERATOR':
            # Бинарные операторы требуют наличие двух чисел в стеке
            # для вычисления результата
            if stack_size < 2:
                return False
            stack_size -= 1
        elif token_type == 'UNARY_OPERATOR':
            # Унарные операторы требуют хотя бы одного числа в стеке,
            # должны ставиться после числа/скобки
            if stack_size < 1:
                raise SyntaxError(f'Некорректная постановка унарного знака на позиции '
                                  f'(без учета скобок): {number_of_tokens}')

    return stack_size == 1

def calculate_expression(stack_raw: str) -> float:
    """
    Функция перехода, преобразует выражение в стек и запускает
    рекурсивную функцию return_result() для подсчета результата
    Аргумент:
        stack_raw (str): исходное выражение,
        через функцию tokenize_rpn преобразовывается
        в list[tuple]: стек с числами и операторами
    Возвращаемое значение:
        float или ValueError: Итоговый ответ или ошибка при некорректном
        результате арифметической операции
    """
    stack = return_result(tokenize_rpn(stack_raw))
    return stack

def return_result(stack: list) -> float:
    """
    Функция для подсчета результата арифметического выражения,
    принимает на вход уже преобразованное в стек выражение и поочередно
    делает операции с помощью словаря операторов. Вызывает саму себя
    до тех пор, пока в результате не получится ответ или не произойдет ошибка
    Аргумент:
        stack (list[tuple]): стек с числами и операторами
    Возвращаемое значение:
        float: или ValueError: Итоговый ответ или ошибка при некорректном
        результате арифметической операции
    """
    for i in range(0, len(stack)):
        if stack[i][1] in ['~', '$']:
            a, b, op = stack[i-2][1], stack[i-1][1], stack[i][1]
            result = OPERATORS_DICT[op](a, b)
            stack[i-1] = ('NUMBER', result)
            stack.pop(i)
            break
        elif stack[i][0] == 'BINARY_OPERATOR' and stack[i-1][0] == 'NUMBER' and stack[i-2][0] == 'NUMBER':
            a, b, op = stack[i-2][1], stack[i-1][1], stack[i][1]
            result = OPERATORS_DICT[op](a, b)
            stack[i-2] = ('NUMBER', result)
            stack.pop(i)
            stack.pop(i-1)
            break

    print(stack)
    return stack[0][1] if len(stack) == 1 else return_result(stack)