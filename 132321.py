result = None
operand = None
operator = None
wait_for_number = True

while True:
    if wait_for_number:
        try:
            operand = float(input("Введіть число: "))
            if result is None:
                result = operand
            else:
                if operator == '+':
                    result += operand
                elif operator == '-':
                    result -= operand
                elif operator == '*':
                    result *= operand
                elif operator == '/':
                    if operand != 0:
                        result /= operand
                    else:
                        print("Помилка: ділення на нуль.")
                        continue
            wait_for_number = False
        except ValueError:
            print("Це не число. Спробуйте ще раз.")
    else:
        operator = input("Введіть оператор (+, -, *, /) або '=' для отримання результату: ")
        if operator in ['+', '-', '*', '/']:
            wait_for_number = True
        elif operator == '=':
            print(f"Результат: {result}")
            break
        else:
            print("Це не коректний оператор. Спробуйте ще раз.")