BINARY_OPERATORS = {'+', '-', '*', '/', '%', '//', '**'}
UNARY_OPERATORS = {'~', '$'}
ASCII_CAT = """
   ./\_____/\.
  ./  o   o  \.
  ( ==  ^  == )
   )         (
  (           )
 ( (  )   (  ) )
(__(__)___(__)__)
"""
OPERATORS_DICT = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b if b != 0 else handle_error(a, b, '/'),
    '%': lambda a, b: a % b if check_integers(a, b, '%') else None,
    '//': lambda a, b: a // b if check_integers(a, b, '//') else None,
    '**': lambda a, b: a ** b if not isinstance(a ** b, complex) else handle_error(a, b, '**'),
    '~': lambda a, b: -b,
    '$': lambda a, b: b
}

def handle_error(a, b, op):
    if op == '**':
        raise ValueError(f'Отсутствует решение в действительных числах: {a, b, op}')
    else:
        raise ValueError(f'Операция "{op}" на ноль невозможна: {a, b, op}')

def check_integers(a, b, op):
    if b == 0:
        handle_error(a, b, op)
    if int(a) != a or int(b) != b:
        raise ValueError(f'Операция "{op}" с нецелыми числами не поддерживается: {a, b, op}')
    return True

