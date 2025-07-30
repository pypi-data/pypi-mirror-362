import os
from colorama import init, Fore
init()

text = []

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def write():
    global text
    clear_terminal()
    print('Вы находитесь в режиме записи')
    while True:
        line = input()
        if line == '/save':
            while True:
                file_path = input('Введите путь для сохранения: ').strip()
                if not file_path:
                    print(f'{Fore.RED}Ошибка: путь не может быть пустым!{Fore.RESET}')
                    continue
                try:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write('\n'.join(text))
                    print(f'{Fore.GREEN}Файл сохранён!{Fore.RESET}')
                    text = []
                    break
                except Exception as e:
                    print(f'{Fore.RED}Возникла ошибка! {e}{Fore.RESET}')
        elif line == '/commands':
            text = []
            return
        elif line == '/exit':
            quit()
        else:
            text.append(line)

def num_write():
    global text
    clear_terminal()
    print('Вы находитесь в режиме нумерованной записи')
    i = 1
    while True:
        line = input(f'{i}. ')
        i+=1
        if line == '/save':
            while True:
                file_path = input('Введите путь для сохранения: ').strip()
                if not file_path:
                    print(f'{Fore.RED}Ошибка: путь не может быть пустым!{Fore.RESET}')
                    continue
                try:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write('\n'.join(text))
                    print(f'{Fore.GREEN}Файл сохранён!{Fore.RESET}')
                    text = []
                    i = 1
                    break
                except Exception as e:
                    print(f'{Fore.RED}Возникла ошибка! {e}{Fore.RESET}')
        elif line == '/commands':
            text = []
            return
        elif line == '/exit':
            quit()
        else:
            text.append(line)

def help():
    clear_terminal()
    print('''
    Редактор имеет три режима:
    1. Режим команд (по умолчанию при запуске):
    /commands - перейти в режим команд (доступно во всех режимах)

    2. Режим записи:
    /write - перейти в режим записи (доступно только из режима команд)
    /save - сохранить файл (доступно только в режиме записи)

    Инструкция по сохранению:
    1. Введите /save
    2. Укажите путь, например:
        Примеры путей:
        • Абсолютный: C:/папка/файл.txt
        • Относительный: docs/notes.txt (сохранится в подпапке)
        • Только имя: file.txt (сохранится в текущей папке)

    3. Режим нумерованной записи:
    /numwrite - перейти в режим с автонумерацией строк
    (команды /save и другие работают аналогично)

    4. Режим помощи (вы сейчас здесь):
    /help - открыть справку (доступно только в режиме команд)

    Общие команды:
    /exit - выйти из редактора (доступно в любом режиме)
    ''')
    while True:
        user_input = input('> ')
        if user_input == '/exit':
            quit()
        elif user_input == '/commands':
            return
        else:
            print(f'Команда {user_input} не является внутренней командой режима help')

def commands():
    while True:
        clear_terminal()
        print('''
        Вы находитесь в режиме commands
        /write - режим записи
        /numwrite - режим нумерованной
        /help - режим помощи
        /exit - выход из редактора
        ''')
        user_input = input('> ')
        if user_input == '/write':
            write()
        elif user_input == '/numwrite':
            num_write()
        elif user_input == '/help':
            help()
        elif user_input == '/exit':
            quit()

commands()