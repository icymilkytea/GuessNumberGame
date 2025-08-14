import random
import json
#Словарь сложностей
difficulty_levels = {
    "ЛЕГКАЯ": {"min": 0, "max": 10, "mtries": 5},
    "СРЕДНЯЯ": {"min": 0, "max": 100, "mtries": 10},
    "СЛОЖНАЯ": {"min": 0, "max": 1000, "mtries": 15}
}

#Подгрузка языков
def load_locale(lang):
    with open(f"locales/{lang}.json", "r", encoding="utf-8") as f:
        return json.load(f)

MESSAGES = load_locale("ru")

class LogicalGameError(Exception):
    pass

class DuplicateGuessError(LogicalGameError):
    pass

class OutOfRangeError(LogicalGameError):
    pass

def choose_difficulty():
    #Выбор сложности
    while True:
        difficulty = input(MESSAGES["ask_difficulty"]).upper()
        if difficulty in difficulty_levels:
            gen_n_from = difficulty_levels[difficulty]['min']
            gen_n_to = difficulty_levels[difficulty]['max']
            max_tries = difficulty_levels[difficulty]['mtries']
            return gen_n_from, gen_n_to, max_tries
        else:
            print(MESSAGES["no_difficulty"])


#Игровой цикл
def play_game():
    gen_n_from, gen_n_to, max_tries = choose_difficulty()
    #Генерация рандомного числа
    num_to_guess = random.randint(gen_n_from,gen_n_to)
    tries = 0
    previous_guesses = set()

    #Игровой цикл
    while tries < max_tries:
        try:
            if tries == 0:
                #Первая попытка
                user_guess = int(input(MESSAGES["first_try"]))
            else:
                #Остальные попытки
                user_guess = int(input(MESSAGES["next_try"].format(tries = tries+1, max_tries=max_tries)))

            #Проверки ввода на логические ошибки
            if user_guess in previous_guesses:
                raise DuplicateGuessError(MESSAGES["duplicate_guess"])
            if not gen_n_from <= user_guess <= gen_n_to:
                raise OutOfRangeError(MESSAGES["out_of_range"].format(gen_n_from = gen_n_from, gen_n_to = gen_n_to))

            tries += 1
            previous_guesses.add(user_guess)

            #Блок победы
            if user_guess == num_to_guess:
                print(MESSAGES["win"].format(tries = tries))
                break
            else: #Блок подсказок
                if user_guess > num_to_guess:
                    print(MESSAGES["greater"].format(user_guess = user_guess))
                else:
                    print(MESSAGES["less"].format(user_guess = user_guess))

        except ValueError:
            print(MESSAGES["not_integer"])
            continue
        except LogicalGameError as e:
            print(e)
            continue

    # Условия проигрыша
    else:
        print(MESSAGES["lose"].format(number_to_guess = num_to_guess))

    #Перезапуск игры
    return ask_to_play_again()

#Перезапуск игры
def ask_to_play_again():
    while True:
        again = input(MESSAGES['play_again']).lower()
        if again in ("да", "нет"):
            return again == "да"
        else:
            print(MESSAGES['invalid_yes_no'])

#Запуск игры
while play_game():
    pass