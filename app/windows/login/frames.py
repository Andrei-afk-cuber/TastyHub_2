import customtkinter as ctk
from customtkinter import CTkLabel
from .functions import toggle_password, check_login, register_user
from .config import theme
from tkinter import messagebox

# Класс основного фрейма приложения
class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.setup_login_frame()

    # Функция для отрисовки основного фрейма
    def setup_login_frame(self):
        # Создание фрейма входа в аккаунт
        self.login_frame = ctk.CTkFrame(master=self, width=320, height=380)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Верхний текст
        self.text = CTkLabel(
            master=self.login_frame,
            text="TastyHub",
            font=('Century Gothic', 32)
        )
        self.text.place(x=90, y=45)

        self.error_label = ctk.CTkLabel(
            master=self.login_frame,
            text="",
            font=('Century Gothic', 12),
            text_color="red",
        )
        self.error_label.place(x=70, y=80)

        # Поле ввода логина
        self.u_block = ctk.CTkEntry(
            master=self.login_frame,
            width=220,
            placeholder_text="Логин пользователя",
        )
        self.u_block.place(x=50, y=110)

        # Поле ввода пароля
        self.show_password_var = ctk.BooleanVar()
        self.p_block = ctk.CTkEntry(
            master=self.login_frame,
            width=220,
            placeholder_text="Пароль",
            show="*"
        )
        self.p_block.place(x=50, y=150)

        # галочка для показа пароля
        self.show_password = ctk.CTkCheckBox(
            master=self.login_frame,
            text="Показать пароль",
            font=('Century Gothic', 12),
            command=lambda: toggle_password(self.p_block, self.show_password_var),
            variable=self.show_password_var,
            fg_color=theme['fg_color'],
            hover_color=theme['hover_color'],
        )
        self.show_password.place(x=50, y=190)

        # Кнопка входа в аккаунт
        self.login_button = ctk.CTkButton(
            master=self.login_frame,
            width=120,
            text="Войти",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.check_login_credentials,
        )
        self.login_button.place(relx=0.5, y=260, anchor=ctk.CENTER)

        # Кнопка регистрации
        self.register_button = ctk.CTkButton(
            master=self.login_frame,
            width=120,
            text="Создать аккаунт",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.master.open_register_frame
        )
        self.register_button.place(relx=0.5, y=300, anchor=ctk.CENTER)

    # Функция для проверки пароля и логина
    def check_login_credentials(self):
        # Получаем из полей ввода логин и пароль
        username = self.u_block.get()
        password = self.p_block.get()

        # Вызов функции check_login
        user = check_login(username, password)

        # Если пользователь был успешно создан
        if user and user.isAuthorized():
            # Успешный логин
            print("Успешная авторизация")
            self.master.open_main_program(user)
        # Если пользователь существует, но его аккаунт не подтвержден
        elif user and not user.isAuthorized():
            messagebox.showinfo("Подождите", "Вы зарегистрировались, но ваш аккаунт ожидает подтверждения"
                                             " со стороны администрации. Подождите пожалуйста:).")
        # Пользователь не существует
        else:
            # Неуспешный логин
            self.error_label.configure(text="Неверный логин или пароль")

# Класс фрейма регистрации
class RegistrationFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.setup_register_frame()

    # Метод отрисовки фрейма регистрации
    def setup_register_frame(self):
        self.master.change_title("Регистрация")
        # Create the registration frame
        self.registration_frame = ctk.CTkFrame(
            master=self,
            width=320,
            height=380
        )
        self.registration_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Верхний текст
        self.text = CTkLabel(
            master=self.registration_frame,
            text="Добро пожаловать в\n TestyHub",
            font=('Century Gothic', 25)
        )
        self.text.place(relx=0.5, y=50, anchor=ctk.CENTER)

        self.back_button = ctk.CTkButton(
            master=self,
            width=30,
            height=30,
            text="Назад",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.master.open_main_frame
        )
        self.back_button.place(x=10, y=10)

        # Поле ввода логина
        self.username_entry = ctk.CTkEntry(
            master=self.registration_frame,
            width=220,
            placeholder_text="Логин",
        )
        self.username_entry.place(x=50, y=100)

        # Поле ввода пароля
        self.show_password_var = ctk.BooleanVar()
        self.p_block = ctk.CTkEntry(
            master=self.registration_frame,
            width=220,
            placeholder_text="Пароль",
            show="*"
        )
        self.p_block.place(x=50, y=140)

        # Галочка показа пароля
        self.show_password = ctk.CTkCheckBox(
            master=self.registration_frame,
            text="Показать пароль",
            font=('Century Gothic', 12),
            command=lambda: toggle_password(self.p_block, self.show_password_var),
            variable=self.show_password_var,
            fg_color=theme['fg_color'],
            hover_color=theme['hover_color'],
        )
        self.show_password.place(x=50, y=190)

        self.register_button = ctk.CTkButton(
            master=self.registration_frame,
            width=120,
            text="Зарегистрироваться",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.new_user_data
        )
        self.register_button.place(relx=0.5, y=300, anchor=ctk.CENTER)

    # Метод для регистрации нового пользователя
    def new_user_data(self):
        username = self.username_entry.get()
        password = self.p_block.get()

        if not username or not password:
            print("Пожалуйста, заполните поля ввода логина и пароля")
            messagebox.showerror("Ошибка", "Заполните поля логина и пароля")
            return

        if register_user(username, password):
            # Успешная регистрация
            print("Пользователь успешно зарегистрировался")
            messagebox.showinfo("Поздравляем", "Регистрация прошла успешно")
            self.registration_frame.place_forget()
            self.master.open_main_frame()
            return
        else:
            # В случае, если пользователь с таким логином уже зарегистрирован
            print("Логин уже используется")
            messagebox.showerror("Ошибка", "Этот логин уже занят, используйте другой")
            return