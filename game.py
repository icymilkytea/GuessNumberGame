import random
#Словарь сложностей
difficulty_levels = {
    "ЛЕГКАЯ": {"min": 0, "max": 10, "mtries": 5},
    "СРЕДНЯЯ": {"min": 0, "max": 100, "mtries": 10},
    "СЛОЖНАЯ": {"min": 0, "max": 1000, "mtries": 15}
}

class LogicalGameError(Exception):
    pass

class DuplicateGuessError(LogicalGameError):
    pass

class OutOfRangeError(LogicalGameError):
    pass

#Игровой цикл
def play_game():
    #Выбор сложности
    while True:
        difficulty = input("Введите 'Легкая','Средняя' или 'Сложная' для выбора сложности игры").upper()
        if difficulty in difficulty_levels:
            gen_n_from = difficulty_levels[difficulty]['min']
            gen_n_to = difficulty_levels[difficulty]['max']
            max_tries = difficulty_levels[difficulty]['mtries']
            break
        else:
            print("Такой сложности нет")

    #Генерация рандомного числа
    num_to_guess = random.randint(gen_n_from,gen_n_to)
    tries = 0
    previous_guesses = []

    #Игровой цикл
    while tries < max_tries:
        try:
            if tries == 0:
                #Первая попытка
                user_guess = int(input("Компьютер загадал число, попробуй его отгадать:"))
            else:
                #Остальные попытки
                user_guess = int(input(f"Попытка {tries+1}/{max_tries}, попробуй его отгадать:"))

            #Проверки ввода на логические ошибки
            if user_guess in previous_guesses:
                raise DuplicateGuessError("Вы уже вводили это число!")
            if not gen_n_from <= user_guess <= gen_n_to:
                raise OutOfRangeError(f"Число должно быть между {gen_n_from} и {gen_n_to}")

            tries += 1
            previous_guesses.append(user_guess)

            #Блок победы
            if user_guess == num_to_guess:
                print(f"Число угадано! Ты выиграл. Угадал с попытки {tries}")
                break
            else: #Блок подсказок
                print(f"Число не угадано!")
                if user_guess > num_to_guess:
                    print(f"Число {user_guess} больше загаданного")
                else:
                    print(f"Число {user_guess} меньше загаданного")

        except ValueError:
            print("Нужно ввести целое число!")
            continue
        except LogicalGameError as e:
            print(e)
            continue

    # Условия проигрыша
    if tries >= max_tries:
        print(f"Попытки закончились. Было загадано число {num_to_guess}")
    if ask_to_play_again():
        return True
    else:
        return False

#Перезапуск игры
def ask_to_play_again():
    while True:
        again = input("Хотите сыграть еще раз? (да/нет)").lower()
        if again == "да":
            return True
        elif again == 'нет':
            return False
        else:
            print("Пожалуйста, введите 'да' или 'нет'.")

#Запуск игры
while play_game():
    pass