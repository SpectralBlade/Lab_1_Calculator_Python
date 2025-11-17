from power import calculate_expression
from constants import ASCII_CAT

def main() -> None:
    accept_point = input("Вы любите котов? Введите число \"1\", если да, \"0\", если нет\n")
    if accept_point == '1':
        pass
    elif accept_point == '0':
        raise ConnectionRefusedError('Ошибка: Вы не имеете права пользоваться данным калькулятором')
    else:
        raise SyntaxError('Вы ввели что-то, не являющееся цифрой 0 или 1')
    expression = input('Отлично! \nВведите выражение в обратной польской нотации: ')
    answer = calculate_expression(expression)
    print(f'Ваш ответ: {answer}')
    print(ASCII_CAT)

if __name__ == "__main__":
    main()
