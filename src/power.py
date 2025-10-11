from src.constants import BINARY_OPERATORS, UNARY_OPERATORS

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
        elif part in UNARY_OPERATORS:
            if stack_size < 1:
                raise SyntaxError(f'Некорректная постановка унарного знака '
                                  f'(вы поставили его в начале выражения в скобках)')
        # Унарные операторы не учитываются, т.к. не должны менять баланс стека для проверки RPN

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
    current_token_type = ''
    number_of_tokens = 0
    stack_size = 0

    for token_type, token_value in tokens:
        if token_type == 'NUMBER':
            stack_size += 1
            current_token_type = 'NUMBER'; number_of_tokens += 1
        elif token_type == 'BINARY_OPERATOR':
            # Бинарные операторы требуют наличие двух чисел в стеке
            # для вычисления результата
            if stack_size < 2:
                return False
            stack_size -= 1
            current_token_type = 'BINARY_OPERATOR'; number_of_tokens += 1
        elif token_type == 'UNARY_OPERATOR':
            # Унарные операторы требуют хотя бы одного числа в стеке,
            # должны ставиться после числа/скобки
            if stack_size < 1:
                raise SyntaxError(f'Некорректная постановка унарного знака на позиции '
                                  f'(без учета скобок): {number_of_tokens}')
            current_token_type = 'UNARY_OPERATOR'; number_of_tokens += 1

    return stack_size == 1

def calculate_expression(stack_raw: str) -> float:
    """
    Функция для подсчета результата арифметического выражения.
    Аргумент:
        stack_raw (str): исходное выражение,
        через функцию tokenize_rpn преобразовывается
        в list[tuple]: стек с числами и операторами
    Возвращаемое значение:
        float: Итоговый ответ, или ValueError, если ошибка при
        какой-либо операции деления на ноль
    """
    stack = tokenize_rpn(stack_raw)

    # Обработка унарных операторов ($ никак не изменяет число, ~ умножает его на -1)
    while len(stack) > 1:
        for i in range(0, len(stack)):
            operation_ok = 0
            if stack[i][1] == '~':
                stack[i-1] = ('NUMBER', stack[i-1][1]*-1)
                stack.pop(i)
                break
            elif stack[i][1] == '$':
                stack.pop(i)
                break

            # Вычисления внутри списка
            if stack[i][0] == 'BINARY_OPERATOR' and stack[i-1][0] == 'NUMBER' and stack[i-2][0] == 'NUMBER':
                if stack[i][1] == '+':
                    stack[i-2] = ('NUMBER', stack[i-2][1] + stack[i-1][1])
                    operation_ok = 1
                elif stack[i][1] == '-':
                    stack[i-2] = ('NUMBER', stack[i-2][1] - stack[i-1][1])
                    operation_ok = 1
                elif stack[i][1] == '*':
                    stack[i-2] = ('NUMBER', stack[i-2][1] * stack[i-1][1])
                    operation_ok = 1
                elif stack[i][1] == '/':
                    if stack[i-1][1] == 0:
                        raise ValueError(f'Деление на ноль невозможно: '
                                         f'{stack[i-2][1], stack[i-1][1], stack[i][1]}')
                    else:
                        stack[i-2] = ('NUMBER', stack[i-2][1] / stack[i-1][1])
                        operation_ok = 1
                elif stack[i][1] == '%':
                    if stack[i-1][1] == 0:
                        raise ValueError(f'Вычисление остатка от деления на ноль невозможно: '
                                         f'{stack[i-2][1], stack[i-1][1], stack[i][1]}')
                    elif int(stack[i-1][1]) != stack[i-1][1]:
                        raise ValueError(f'Операция вычисления остатка от деления на нецелое число'
                                         f' не поддерживается: {stack[i-1][1]}')
                    else:
                        stack[i-2] = ('NUMBER', stack[i-2][1] % stack[i-1][1])
                        operation_ok = 1
                elif stack[i][1] == '//':
                    if stack[i-1][1] == 0:
                        raise ValueError(f'Целочисленное деление на ноль невозможно: '
                                         f'{stack[i-2][1], stack[i-1][1], stack[i][1]}')
                    elif int(stack[i-1][1]) != stack[i-1][1]:
                        raise ValueError(f'Операция целочисленного деления на нецелое число'
                                         f' не поддерживается: {stack[i-1][1]}')
                    else:
                        stack[i-2] = ('NUMBER', stack[i-2][1] // stack[i-1][1])
                        operation_ok = 1
                elif stack[i][1] == '**':
                    if isinstance(stack[i-2][1] ** stack[i-1][1], complex):
                        raise ValueError(f'Отсутствует решение в действительных числах: '
                                         f'{stack[i-2][1], stack[i-1][1], stack[i][1]}')
                    else:
                        stack[i-2] = ('NUMBER', stack[i-2][1] ** stack[i-1][1])
                        operation_ok = 1

                # Если выполнилась операция, удаляем лишние ее элементы из списка
                if operation_ok:
                    stack.pop(i)
                    stack.pop(i-1)
                    break

    return stack[0][1]
