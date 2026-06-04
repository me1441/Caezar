#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Шифратор 3-в-1: Цезарь, Атбаш, Морзе
Графическое приложение для шифрования и дешифрования текста
Разработчик: Егоров
Год: 2026
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
import pyperclip


class CaesarCipherApp:
    """Главный класс приложения шифратора 3-в-1"""

    def __init__(self, root):
        """Инициализация приложения"""
        self.root = root
        self.y0 = 0  # Начальное состояние автомата

        # Текущие параметры
        self.current_tab = "caesar"
        self.current_language = "ru"
        self.shift_value = 3

        # Инициализация алфавитов
        self.init_alphabets()

        # Инициализация словаря Морзе
        self.init_morse_dicts()

        # Создание интерфейса
        self.create_widgets()

        # Переход в состояние "Главное окно активно"
        self.y0 = 1
        self.A0(10)

    def init_alphabets(self):
        """Инициализация алфавитов для всех поддерживаемых языков"""
        self.alphabets = {
            'ru': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
            'en': 'abcdefghijklmnopqrstuvwxyz',
            'de': 'abcdefghijklmnopqrstuvwxyzäöüß',
            'fr': 'abcdefghijklmnopqrstuvwxyzàâäèéêëîïôùûüç'
        }
        self.current_alphabet = self.alphabets['ru']

    def init_morse_dicts(self):
        """Инициализация словарей азбуки Морзе"""
        # Международная азбука Морзе (латиница)
        self.morse_dict_en = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
            'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
            'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
            'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
            'Z': '--..',
            '0': '-----', '1': '.----', '2': '..---', '3': '...--',
            '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.',
            '.': '.-.-.-', ',': '--..--', '?': '..--..', '!': '-.-.--',
            '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...',
            ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.',
            '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-',
            '@': '.--.-.', ' ': '  '
        }

        # Русская азбука Морзе
        self.morse_dict_ru = {
            'А': '.-', 'Б': '-...', 'В': '.--', 'Г': '--.', 'Д': '-..',
            'Е': '.', 'Ё': '.', 'Ж': '...-', 'З': '--..', 'И': '..',
            'Й': '.---', 'К': '-.-', 'Л': '.-..', 'М': '--', 'Н': '-.',
            'О': '---', 'П': '.--.', 'Р': '.-.', 'С': '...', 'Т': '-',
            'У': '..-', 'Ф': '..-.', 'Х': '....', 'Ц': '-.-.', 'Ч': '---.',
            'Ш': '----', 'Щ': '--.-', 'Ъ': '--.--', 'Ы': '-.--', 'Ь': '-..-',
            'Э': '..-..', 'Ю': '..--', 'Я': '.-.-',
            '0': '-----', '1': '.----', '2': '..---', '3': '...--',
            '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.',
            '.': '.-.-.-', ',': '--..--', '?': '..--..', '!': '-.-.--',
            ' ': '  '
        }

        # Создаем обратные словари для декодирования
        self.morse_reverse_en = {v: k for k, v in self.morse_dict_en.items()}
        self.morse_reverse_ru = {v: k for k, v in self.morse_dict_ru.items()}

    # ==================== АВТОМАТ УПРАВЛЕНИЯ ИНТЕРФЕЙСОМ (A0) ====================

    def A0(self, e, **kwargs):
        """Автомат управления интерфейсом"""
        y_old = self.y0

        # Проверка условий перехода
        if self.y0 == 0:  # Начальное состояние (инициализация)
            if e == 10:  # Запуск программы
                self.y0 = 1
                self.z10()  # Отобразить главное окно

        elif self.y0 == 1:  # Главное окно активно
            if e == 20:  # Выбор вкладки Цезаря
                self.y0 = 2
                self.z20()  # Переключить на вкладку Цезаря
            elif e == 30:  # Выбор вкладки Атбаш
                self.y0 = 3
                self.z30()  # Переключить на вкладку Атбаш
            elif e == 40:  # Выбор вкладки Морзе
                self.y0 = 4
                self.z40()  # Переключить на вкладку Морзе
            elif e == 100:  # Закрытие программы
                self.y0 = 0
                self.z120()  # Закрыть программу

        elif self.y0 == 2:  # Режим Цезаря
            if e == 50:  # Нажатие Зашифровать
                self.z50(kwargs.get('text'), kwargs.get('shift'))
            elif e == 60:  # Нажатие Расшифровать
                self.z60(kwargs.get('text'), kwargs.get('shift'))
            elif e == 70:  # Нажатие Информация
                self.z110()
            elif e == 80:  # Изменение языка
                self.current_language = kwargs.get('lang')
                self.current_alphabet = self.alphabets[self.current_language]
            elif e == 90:  # Изменение сдвига
                self.shift_value = kwargs.get('shift')
            elif e == 20 or e == 30 or e == 40:  # Переключение вкладки
                self.y0 = 1
                self.A0(e)
                return

        elif self.y0 == 3:  # Режим Атбаш
            if e == 50:  # Нажатие Зашифровать
                self.z70(kwargs.get('text'))
            elif e == 60:  # Нажатие Расшифровать
                self.z70(kwargs.get('text'))  # Атбаш симметричен
            elif e == 70:  # Нажатие Информация
                self.z110()
            elif e == 80:  # Изменение языка
                self.current_language = kwargs.get('lang')
                self.current_alphabet = self.alphabets[self.current_language]
            elif e == 20 or e == 30 or e == 40:  # Переключение вкладки
                self.y0 = 1
                self.A0(e)
                return

        elif self.y0 == 4:  # Режим Морзе
            if e == 50:  # Нажатие Зашифровать в Морзе
                self.z80(kwargs.get('text'))
            elif e == 60:  # Нажатие Расшифровать из Морзе
                self.z90(kwargs.get('text'))
            elif e == 70:  # Нажатие Информация
                self.z110()
            elif e == 80:  # Изменение языка
                self.current_language = kwargs.get('lang')
            elif e == 20 or e == 30 or e == 40:  # Переключение вкладки
                self.y0 = 1
                self.A0(e)
                return

        # Выполнение действий при переходе
        if y_old != self.y0 and self.y0 in [2, 3, 4]:
            self.execute_state_actions(self.y0)

    def execute_state_actions(self, state):
        """Выполнение действий в новом состоянии"""
        pass  # Действия выполняются через выходные воздействия

    # ==================== ВЫХОДНЫЕ ВОЗДЕЙСТВИЯ ====================

    def z10(self):
        """Отобразить главное окно"""
        self.root.deiconify()

    def z20(self):
        """Переключить на вкладку Цезаря"""
        self.tabview.set("Шифр Цезаря")
        self.current_tab = "caesar"

    def z30(self):
        """Переключить на вкладку Атбаш"""
        self.tabview.set("Шифр Атбаш")
        self.current_tab = "atbash"

    def z40(self):
        """Переключить на вкладку Морзе"""
        self.tabview.set("Азбука Морзе")
        self.current_tab = "morse"

    def z50(self, text, shift):
        """Выполнить шифрование Цезаря"""
        result = self.caesar_cipher(text, shift, 'encrypt')
        self.z100(result)

    def z60(self, text, shift):
        """Выполнить дешифрование Цезаря"""
        result = self.caesar_cipher(text, shift, 'decrypt')
        self.z100(result)

    def z70(self, text):
        """Выполнить шифрование/дешифрование Атбаш"""
        result = self.atbash_cipher(text)
        self.z100(result)

    def z80(self, text):
        """Выполнить кодирование Морзе"""
        result = self.morse_encode(text)
        self.z100(result)

    def z90(self, text):
        """Выполнить декодирование Морзе"""
        result = self.morse_decode(text)
        self.z100(result)

    def z100(self, result):
        """Отобразить результат"""
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", result)

    def z110(self):
        """Отобразить информацию"""
        info_text = self.get_info_text()
        messagebox.showinfo("Информация", info_text)

    def z120(self):
        """Закрыть программу"""
        self.root.destroy()

    # ==================== АЛГОРИТМЫ ШИФРОВАНИЯ ====================

    def caesar_cipher(self, text, shift, mode='encrypt'):
        """
        Шифр Цезаря - шифр сдвига с настраиваемым ключом

        Алгоритм:
        1. Получить входной текст и величину сдвига
        2. Для каждого символа определить позицию в алфавите
        3. Вычислить новую позицию: (текущая + сдвиг) mod размер_алфавита
        4. Сохранить регистр и специальные символы
        """
        result = []
        alphabet = self.current_alphabet
        shift = int(shift)

        for char in text:
            if char.lower() in alphabet:
                idx = alphabet.index(char.lower())
                if mode == 'encrypt':
                    new_idx = (idx + shift) % len(alphabet)
                else:
                    new_idx = (idx - shift) % len(alphabet)
                new_char = alphabet[new_idx]
                result.append(new_char.upper() if char.isupper() else new_char)
            else:
                result.append(char)

        return ''.join(result)

    def atbash_cipher(self, text):
        """
        Шифр Атбаш - симметричный шифр замены

        Алгоритм:
        1. Создать обратный алфавит
        2. Для каждого символа найти позицию в исходном алфавите
        3. Заменить на символ с той же позицией из обратного алфавита
        4. Шифрование и дешифрование - одна операция
        """
        result = []
        alphabet = self.current_alphabet
        reversed_alphabet = alphabet[::-1]

        for char in text:
            if char.lower() in alphabet:
                idx = alphabet.index(char.lower())
                new_char = reversed_alphabet[idx]
                result.append(new_char.upper() if char.isupper() else new_char)
            else:
                result.append(char)

        return ''.join(result)

    def morse_encode(self, text):
        """
        Кодирование в азбуку Морзе

        Алгоритм:
        1. Использовать словарь соответствия символов и кодов
        2. Для каждого символа найти соответствующий код
        3. Разделить коды букв пробелами, слова - двойными пробелами
        """
        result = []

        # Выбор словаря в зависимости от языка
        if self.current_language == 'ru':
            morse_dict = self.morse_dict_ru
        else:
            morse_dict = self.morse_dict_en

        words = text.upper().split(' ')

        for word in words:
            word_code = []
            for char in word:
                if char in morse_dict:
                    word_code.append(morse_dict[char])
                elif char in self.morse_dict_en:
                    word_code.append(self.morse_dict_en[char])
            if word_code:
                result.append(' '.join(word_code))

        return '   '.join(result)

    def morse_decode(self, text):
        """
        Декодирование из азбуки Морзе

        Алгоритм:
        1. Разделить входной текст на слова (тройные пробелы)
        2. Разделить слова на коды букв (одинарные пробелы)
        3. Найти соответствующий символ для каждого кода
        """
        result = []

        # Выбор словаря в зависимости от языка
        if self.current_language == 'ru':
            morse_reverse = self.morse_reverse_ru
        else:
            morse_reverse = self.morse_reverse_en

        words = text.strip().split('   ')

        for word in words:
            letters = word.strip().split(' ')
            word_result = []
            for letter in letters:
                if letter in morse_reverse:
                    word_result.append(morse_reverse[letter])
                elif letter in self.morse_reverse_en:
                    word_result.append(self.morse_reverse_en[letter])
                else:
                    word_result.append('?')
            result.append(''.join(word_result))

        return ' '.join(result)

    # ==================== СОЗДАНИЕ ИНТЕРФЕЙСА ====================

    def create_widgets(self):
        """Создание элементов графического интерфейса"""
        # Настройка сетки
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Создание вкладок
        self.tabview = ctk.CTkTabview(self.root, width=880, height=580)
        self.tabview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Вкладка Цезаря
        self.caesar_tab = self.tabview.add("Шифр Цезаря")
        self.create_caesar_tab()

        # Вкладка Атбаш
        self.atbash_tab = self.tabview.add("Шифр Атбаш")
        self.create_atbash_tab()

        # Вкладка Морзе
        self.morse_tab = self.tabview.add("Азбука Морзе")
        self.create_morse_tab()

        # Привязка переключения вкладок
        self.tabview.configure(command=self.on_tab_change)

    def create_caesar_tab(self):
        """Создание вкладки Шифр Цезаря"""
        frame = self.caesar_tab
        frame.grid_columnconfigure(0, weight=1)

        # Заголовок
        title = ctk.CTkLabel(frame, text="Шифр Цезаря (Caesar Cipher)", 
                            font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Описание
        desc = ctk.CTkLabel(frame, text="Шифр сдвига: каждая буква заменяется на букву, \
                                        находящуюся на фиксированное число позиций дальше в алфавите.",
                           wraplength=800, justify="left")
        desc.grid(row=1, column=0, columnspan=2, padx=20, pady=5)

        # Поле ввода
        input_label = ctk.CTkLabel(frame, text="Введите текст:", font=ctk.CTkFont(size=12, weight="bold"))
        input_label.grid(row=2, column=0, sticky="w", padx=20, pady=(10, 0))

        self.caesar_input = ctk.CTkTextbox(frame, width=800, height=120)
        self.caesar_input.grid(row=3, column=0, columnspan=2, padx=20, pady=5)

        # Панель настроек
        settings_frame = ctk.CTkFrame(frame)
        settings_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Выбор языка
        lang_label = ctk.CTkLabel(settings_frame, text="Язык алфавита:")
        lang_label.grid(row=0, column=0, padx=10, pady=10)

        self.lang_var = ctk.StringVar(value="ru")
        lang_combo = ctk.CTkComboBox(settings_frame, values=["ru", "en", "de", "fr"],
                                     variable=self.lang_var, width=100,
                                     command=self.on_language_change)
        lang_combo.grid(row=0, column=1, padx=10, pady=10)

        # Поле сдвига
        shift_label = ctk.CTkLabel(settings_frame, text="Величина сдвига (1-50):")
        shift_label.grid(row=0, column=2, padx=10, pady=10)

        self.shift_var = ctk.StringVar(value="3")
        shift_entry = ctk.CTkEntry(settings_frame, textvariable=self.shift_var, width=60)
        shift_entry.grid(row=0, column=3, padx=10, pady=10)

        # Кнопки управления
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        encrypt_btn = ctk.CTkButton(btn_frame, text="Зашифровать", 
                                    fg_color="#28A745", hover_color="#1e7e34",
                                    command=self.on_caesar_encrypt)
        encrypt_btn.grid(row=0, column=0, padx=10)

        decrypt_btn = ctk.CTkButton(btn_frame, text="Расшифровать", 
                                    fg_color="#007BFF", hover_color="#0056b3",
                                    command=self.on_caesar_decrypt)
        decrypt_btn.grid(row=0, column=1, padx=10)

        info_btn = ctk.CTkButton(btn_frame, text="Информация", 
                                 fg_color="#17A2B8", hover_color="#117a8b",
                                 command=self.on_info_click)
        info_btn.grid(row=0, column=2, padx=10)

        # Поле результата
        result_label = ctk.CTkLabel(frame, text="Результат:", font=ctk.CTkFont(size=12, weight="bold"))
        result_label.grid(row=6, column=0, sticky="w", padx=20, pady=(10, 0))

        self.result_text = ctk.CTkTextbox(frame, width=800, height=120)
        self.result_text.grid(row=7, column=0, columnspan=2, padx=20, pady=5)

        # Кнопка копирования
        copy_btn = ctk.CTkButton(frame, text="Копировать результат", 
                                 command=self.copy_result)
        copy_btn.grid(row=8, column=0, columnspan=2, pady=10)

    def create_atbash_tab(self):
        """Создание вкладки Шифр Атбаш"""
        frame = self.atbash_tab
        frame.grid_columnconfigure(0, weight=1)

        # Заголовок
        title = ctk.CTkLabel(frame, text="Шифр Атбаш (Atbash Cipher)", 
                            font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Описание
        desc = ctk.CTkLabel(frame, text="Симметричный шифр замены: первая буква алфавита \
                                        заменяется на последнюю, вторая - на предпоследнюю и т.д.",
                           wraplength=800, justify="left")
        desc.grid(row=1, column=0, columnspan=2, padx=20, pady=5)

        # Поле ввода
        input_label = ctk.CTkLabel(frame, text="Введите текст:", font=ctk.CTkFont(size=12, weight="bold"))
        input_label.grid(row=2, column=0, sticky="w", padx=20, pady=(10, 0))

        self.atbash_input = ctk.CTkTextbox(frame, width=800, height=150)
        self.atbash_input.grid(row=3, column=0, columnspan=2, padx=20, pady=5)

        # Панель настроек
        settings_frame = ctk.CTkFrame(frame)
        settings_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Выбор языка
        lang_label = ctk.CTkLabel(settings_frame, text="Язык алфавита:")
        lang_label.grid(row=0, column=0, padx=10, pady=10)

        self.atbash_lang_var = ctk.StringVar(value="ru")
        lang_combo = ctk.CTkComboBox(settings_frame, values=["ru", "en", "de", "fr"],
                                     variable=self.atbash_lang_var, width=100,
                                     command=self.on_atbash_language_change)
        lang_combo.grid(row=0, column=1, padx=10, pady=10)

        # Кнопки управления
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        encrypt_btn = ctk.CTkButton(btn_frame, text="Зашифровать", 
                                    fg_color="#28A745", hover_color="#1e7e34",
                                    command=self.on_atbash_encrypt)
        encrypt_btn.grid(row=0, column=0, padx=10)

        decrypt_btn = ctk.CTkButton(btn_frame, text="Расшифровать", 
                                    fg_color="#007BFF", hover_color="#0056b3",
                                    command=self.on_atbash_decrypt)
        decrypt_btn.grid(row=0, column=1, padx=10)

        info_btn = ctk.CTkButton(btn_frame, text="Информация", 
                                 fg_color="#17A2B8", hover_color="#117a8b",
                                 command=self.on_info_click)
        info_btn.grid(row=0, column=2, padx=10)

        # Поле результата (используем общее)
        result_label = ctk.CTkLabel(frame, text="Результат:", font=ctk.CTkFont(size=12, weight="bold"))
        result_label.grid(row=6, column=0, sticky="w", padx=20, pady=(10, 0))

        # Создаем отдельное поле результата для Атбаш
        self.atbash_result = ctk.CTkTextbox(frame, width=800, height=120)
        self.atbash_result.grid(row=7, column=0, columnspan=2, padx=20, pady=5)

        # Кнопка копирования
        copy_btn = ctk.CTkButton(frame, text="Копировать результат", 
                                 command=self.copy_atbash_result)
        copy_btn.grid(row=8, column=0, columnspan=2, pady=10)

    def create_morse_tab(self):
        """Создание вкладки Азбука Морзе"""
        frame = self.morse_tab
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Заголовок
        title = ctk.CTkLabel(frame, text="Азбука Морзе (Morse Code)", 
                            font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Описание
        desc = ctk.CTkLabel(frame, text="Кодирование текста в последовательность точек и тире. \
                                        Поддерживает русский и латинский алфавиты.",
                           wraplength=800, justify="left")
        desc.grid(row=1, column=0, columnspan=2, padx=20, pady=5)

        # Левая панель - ввод текста
        left_frame = ctk.CTkFrame(frame)
        left_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        input_label = ctk.CTkLabel(left_frame, text="Текст:", font=ctk.CTkFont(size=12, weight="bold"))
        input_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.morse_input = ctk.CTkTextbox(left_frame, width=380, height=150)
        self.morse_input.grid(row=1, column=0, padx=10, pady=5)

        encode_btn = ctk.CTkButton(left_frame, text="Зашифровать в Морзе", 
                                   fg_color="#28A745", hover_color="#1e7e34",
                                   command=self.on_morse_encode)
        encode_btn.grid(row=2, column=0, pady=10)

        # Правая панель - ввод кода Морзе
        right_frame = ctk.CTkFrame(frame)
        right_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        morse_input_label = ctk.CTkLabel(right_frame, text="Код Морзе:", 
                                         font=ctk.CTkFont(size=12, weight="bold"))
        morse_input_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.morse_code_input = ctk.CTkTextbox(right_frame, width=380, height=150)
        self.morse_code_input.grid(row=1, column=0, padx=10, pady=5)

        decode_btn = ctk.CTkButton(right_frame, text="Расшифровать из Морзе", 
                                   fg_color="#007BFF", hover_color="#0056b3",
                                   command=self.on_morse_decode)
        decode_btn.grid(row=2, column=0, pady=10)

        # Выбор языка
        settings_frame = ctk.CTkFrame(frame)
        settings_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        lang_label = ctk.CTkLabel(settings_frame, text="Язык алфавита:")
        lang_label.grid(row=0, column=0, padx=10, pady=10)

        self.morse_lang_var = ctk.StringVar(value="ru")
        lang_combo = ctk.CTkComboBox(settings_frame, values=["ru", "en"],
                                     variable=self.morse_lang_var, width=100,
                                     command=self.on_morse_language_change)
        lang_combo.grid(row=0, column=1, padx=10, pady=10)

        info_btn = ctk.CTkButton(settings_frame, text="Информация", 
                                 fg_color="#17A2B8", hover_color="#117a8b",
                                 command=self.on_info_click)
        info_btn.grid(row=0, column=2, padx=10, pady=10)

        # Поле результата
        result_label = ctk.CTkLabel(frame, text="Результат:", font=ctk.CTkFont(size=12, weight="bold"))
        result_label.grid(row=4, column=0, sticky="w", padx=20, pady=(10, 0))

        self.morse_result = ctk.CTkTextbox(frame, width=800, height=120)
        self.morse_result.grid(row=5, column=0, columnspan=2, padx=20, pady=5)

        # Кнопка копирования
        copy_btn = ctk.CTkButton(frame, text="Копировать результат", 
                                 command=self.copy_morse_result)
        copy_btn.grid(row=6, column=0, columnspan=2, pady=10)

    # ==================== ОБРАБОТЧИКИ СОБЫТИЙ ====================

    def on_tab_change(self):
        """Обработчик переключения вкладок"""
        current = self.tabview.get()
        if current == "Шифр Цезаря":
            self.A0(20)
        elif current == "Шифр Атбаш":
            self.A0(30)
        elif current == "Азбука Морзе":
            self.A0(40)

    def on_language_change(self, choice):
        """Обработчик изменения языка для Цезаря"""
        self.A0(80, lang=choice)

    def on_atbash_language_change(self, choice):
        """Обработчик изменения языка для Атбаш"""
        self.A0(80, lang=choice)

    def on_morse_language_change(self, choice):
        """Обработчик изменения языка для Морзе"""
        self.A0(80, lang=choice)

    def on_caesar_encrypt(self):
        """Обработчик шифрования Цезаря"""
        text = self.caesar_input.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning("Внимание", "Введите текст для шифрования!")
            return
        try:
            shift = int(self.shift_var.get())
            if shift < 1 or shift > 50:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Внимание", "Величина сдвига должна быть числом от 1 до 50!")
            return
        self.A0(50, text=text, shift=shift)

    def on_caesar_decrypt(self):
        """Обработчик дешифрования Цезаря"""
        text = self.caesar_input.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning("Внимание", "Введите текст для расшифровки!")
            return
        try:
            shift = int(self.shift_var.get())
            if shift < 1 or shift > 50:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Внимание", "Величина сдвига должна быть числом от 1 до 50!")
            return
        self.A0(60, text=text, shift=shift)

    def on_atbash_encrypt(self):
        """Обработчик шифрования Атбаш"""
        text = self.atbash_input.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning("Внимание", "Введите текст для шифрования!")
            return
        result = self.atbash_cipher(text)
        self.atbash_result.delete("1.0", "end")
        self.atbash_result.insert("1.0", result)

    def on_atbash_decrypt(self):
        """Обработчик дешифрования Атбаш (симметричен)"""
        text = self.atbash_input.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning("Внимание", "Введите текст для расшифровки!")
            return
        result = self.atbash_cipher(text)
        self.atbash_result.delete("1.0", "end")
        self.atbash_result.insert("1.0", result)

    def on_morse_encode(self):
        """Обработчик кодирования в Морзе"""
        text = self.morse_input.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning("Внимание", "Введите текст для кодирования!")
            return
        result = self.morse_encode(text)
        self.morse_result.delete("1.0", "end")
        self.morse_result.insert("1.0", result)

    def on_morse_decode(self):
        """Обработчик декодирования из Морзе"""
        text = self.morse_code_input.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning("Внимание", "Введите код Морзе для декодирования!")
            return
        result = self.morse_decode(text)
        self.morse_result.delete("1.0", "end")
        self.morse_result.insert("1.0", result)

    def on_info_click(self):
        """Обработчик нажатия кнопки Информация"""
        self.A0(70)

    def copy_result(self):
        """Копирование результата в буфер обмена"""
        result = self.result_text.get("1.0", "end-1c")
        if result:
            try:
                pyperclip.copy(result)
                messagebox.showinfo("Успех", "Результат скопирован в буфер обмена!")
            except:
                messagebox.showwarning("Ошибка", "Не удалось скопировать в буфер обмена")
        else:
            messagebox.showwarning("Внимание", "Нет результата для копирования")

    def copy_atbash_result(self):
        """Копирование результата Атбаш в буфер обмена"""
        result = self.atbash_result.get("1.0", "end-1c")
        if result:
            try:
                pyperclip.copy(result)
                messagebox.showinfo("Успех", "Результат скопирован в буфер обмена!")
            except:
                messagebox.showwarning("Ошибка", "Не удалось скопировать в буфер обмена")
        else:
            messagebox.showwarning("Внимание", "Нет результата для копирования")

    def copy_morse_result(self):
        """Копирование результата Морзе в буфер обмена"""
        result = self.morse_result.get("1.0", "end-1c")
        if result:
            try:
                pyperclip.copy(result)
                messagebox.showinfo("Успех", "Результат скопирован в буфер обмена!")
            except:
                messagebox.showwarning("Ошибка", "Не удалось скопировать в буфер обмена")
        else:
            messagebox.showwarning("Внимание", "Нет результата для копирования")

    def get_info_text(self):
        """Получение справочной информации"""
        current = self.tabview.get()
        if current == "Шифр Цезаря":
            return """Шифр Цезаря (Caesar Cipher)

Классический шифр сдвига, использованный Юлием Цезарем.

Алгоритм:
• Каждая буква заменяется на букву, находящуюся на фиксированное число позиций дальше в алфавите
• Величина сдвига (ключ) может быть от 1 до 50
• Сохраняется регистр букв и специальные символы

Пример (сдвиг 3):
Привет → Тулезх

Поддерживаемые языки: русский, английский, немецкий, французский"""

        elif current == "Шифр Атбаш":
            return """Шифр Атбаш (Atbash Cipher)

Древний шифр замены, изначально использованный для еврейского алфавита.

Алгоритм:
• Первая буква алфавита заменяется на последнюю
• Вторая буква заменяется на предпоследнюю
• И так далее...
• Шифрование и дешифрование выполняются одной операцией

Пример:
Атбаш → ягьяя ч

Поддерживаемые языки: русский, английский, немецкий, французский"""

        else:
            return """Азбука Морзе (Morse Code)

Международная система кодирования символов точками и тире.

Алгоритм:
• Каждая буква заменяется на уникальную комбинацию точек (.) и тире (-)
• Буквы разделяются пробелами
• Слова разделяются тройными пробелами

Пример:
SOS → ... --- ...

Поддерживаемые языки: русский, английский"""


def main():
    """Точка входа в программу"""
    # Настройка внешнего вида CustomTkinter
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Создание главного окна
    root = ctk.CTk()
    root.title("Шифратор 3-в-1: Цезарь, Атбаш, Морзе")
    root.geometry("900x650")
    root.resizable(False, False)

    # Создание приложения
    app = CaesarCipherApp(root)

    # Запуск главного цикла
    root.mainloop()


if __name__ == "__main__":
    main()
