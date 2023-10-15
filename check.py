def calculate_control_number(wagon_number, abbreviated_wagon_number):
    # Проверяем, что номер вагона соответствует длине длину
    if len(wagon_number) != 8:
        return None  # Если длина не соответствует ожидаемой, возвращаем None

    weight_range = [2, 1, 2, 1, 2, 1, 2]

    # Проверяем, что сокращённый номер вагона и весовой ряд имеют одинаковую длину
    if len(abbreviated_wagon_number) != len(weight_range):
        return None  # Возвращаем None в случае ошибки

    # Вычисляем поразрядные произведения и суммируем их
    multiplication = [
        int(abbreviated_wagon_number[i]) * weight_range[i]
        for i in range(len(abbreviated_wagon_number))
    ]
    total_sum = sum([mult // 10 + mult % 10 for mult in multiplication])

    # Вычисляем контрольное число
    counted_control_number = (10 - (total_sum % 10)) % 10

    return counted_control_number




def check_number(wagon_number: str):
    if len(wagon_number) != 8:
        return 0
    abbreviated_wagon_number = wagon_number[:7]  # Первые 7 чисел
    control_number = int(wagon_number[7])  # Последнее восьмое число

    counted_control_number = calculate_control_number(wagon_number, abbreviated_wagon_number)

    if counted_control_number is not None:
        if counted_control_number == control_number:
            return 1
        else:
            return 0
    else:
        return 0