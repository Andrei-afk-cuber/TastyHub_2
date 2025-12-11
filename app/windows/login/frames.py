# libraries
import customtkinter as ctk
from customtkinter import CTkLabel
from tkinter import messagebox

# user libraries
from .functions import toggle_password, check_login, register_user
from app.config import night_theme, day_theme
from app.functions import json_to_dict

# Main frame class
class MainFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master
        self.language = master.language
        self.theme = master.theme
        self.configure(fg_color=self.theme['background_color'])
        self.setup_login_frame()

    # Main frame set up method
    def setup_login_frame(self) -> None:
        self.login_frame = ctk.CTkFrame(master=self, width=320, height=380, fg_color=self.theme['frame_background_color'])
        self.login_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Верхний текст
        self.text = CTkLabel(
            master=self.login_frame,
            text="TastyHub",
            font=('Century Gothic', 32),
            text_color=self.theme['text_color'],
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
            placeholder_text=self.language['user_login'],
            border_width=0,
            fg_color=self.theme['textbox_bg_color'],
            placeholder_text_color=self.theme['textbox_text_color'],
            text_color=self.theme['textbox_text_color']
        )
        self.u_block.place(x=50, y=110)

        # Поле ввода пароля
        self.show_password_var = ctk.BooleanVar()
        self.p_block = ctk.CTkEntry(
            master=self.login_frame,
            width=220,
            placeholder_text=self.language['password'],
            border_width=0,
            fg_color=self.theme['textbox_bg_color'],
            placeholder_text_color=self.theme['textbox_text_color'],
            text_color=self.theme['textbox_text_color'],
            show="*"
        )
        self.p_block.place(x=50, y=150)

        # галочка для показа пароля
        self.show_password = ctk.CTkCheckBox(
            master=self.login_frame,
            text=self.language['show_password'],
            font=('Century Gothic', 12),
            border_width=2,
            command=lambda: toggle_password(self.p_block, self.show_password_var),
            variable=self.show_password_var,
            fg_color=self.theme['button_color'],
            hover_color=self.theme['hover_color'],
            text_color=self.theme['text_color']
        )
        self.show_password.place(x=50, y=190)

        # Кнопка входа в аккаунт
        self.login_button = ctk.CTkButton(
            master=self.login_frame,
            width=120,
            text=self.language['sign_in'],
            corner_radius=6,
            fg_color=self.theme['button_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.check_login_credentials,
        )
        self.login_button.place(relx=0.5, y=260, anchor=ctk.CENTER)

        # Кнопка регистрации
        self.register_button = ctk.CTkButton(
            master=self.login_frame,
            width=120,
            text=self.language['sign_up'],
            corner_radius=6,
            fg_color=self.theme['button_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.master.open_register_frame
        )
        self.register_button.place(relx=0.5, y=300, anchor=ctk.CENTER)

        # button for change color theme
        self.change_theme_button = ctk.CTkButton(
            self.login_frame,
            width=0,
            corner_radius=6,
            fg_color=self.theme['background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            text=self.language['theme'],
            command=self.change_theme_color
        )
        self.change_theme_button.place(relx=0.90, rely=0.06, anchor=ctk.CENTER)

        # button for change language
        self.change_language_button = ctk.CTkButton(
            self.login_frame,
            width=65,
            text=self.language['language'],
            fg_color=self.theme['background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=lambda: self.change_language(self.language['language'])
        )
        self.change_language_button.place(relx=0.12, rely=0.06, anchor=ctk.CENTER)

        # button for get information about authors
        self.about_button = ctk.CTkButton(
            self.login_frame,
            width=120,
            text=self.language['about'],
            fg_color=self.theme['background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.master.open_about_frame
        )
        self.about_button.place(relx=0.5, y=340, anchor=ctk.CENTER)

    # Function for login check
    def check_login_credentials(self) -> None:
        username = self.u_block.get()
        password = self.p_block.get()

        user = check_login(username, password)

        if user and user.isAuthorized():
            self.master.open_main_program(user)
        elif user and not user.isAuthorized():
            messagebox.showinfo(self.language['wait'], self.language['user_is_not_confirmed_message'])
        else:
            self.error_label.configure(text=self.language['incorrect_password_error'])

    # method for change theme color
    def change_theme_color(self) -> None:
        if self.master.theme == day_theme:
            self.master.theme = night_theme
        else:
            self.master.theme = day_theme

        self.master.configure(fg_color=self.master.theme['background_color'])
        self.destroy()
        self.master.open_main_frame()

    # method for change language
    def change_language(self, language: str) -> None:
        if language == 'Русский':
            new_language = json_to_dict("app/locales/english.json")
            self.master.language = new_language
        else:
            new_language = json_to_dict("app/locales/russian.json")
            self.master.language = new_language

        self.destroy()
        self.master.open_main_frame()

class AboutFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master
        self.language = master.language
        self.theme = master.theme

        self.configure(fg_color=self.theme['background_color'])
        self.setup_register_frame()

    # Method for set up main registration frame
    def setup_register_frame(self) -> None:
        self.master.change_title(self.master.language['registration'])
        # Create the registration frame
        self.about_frame = ctk.CTkFrame(
            master=self,
            width=320,
            height=380,
            fg_color=self.theme['frame_background_color'],
        )
        self.about_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.back_button = ctk.CTkButton(
            master=self,
            width=30,
            height=30,
            text=self.language['back'],
            corner_radius=6,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.master.open_main_frame
        )
        self.back_button.place(x=10, y=10)

        self.about_label = ctk.CTkLabel(
            master=self,
            text_color=self.theme['text_color'],
            font=('Century Gothic', 13, 'bold'),
            bg_color=self.theme['frame_background_color'],
            text="TastyHub - платформа обмена рецепта-\nми. "
                 "Это клиент-серверное приложение,\n разработаное "
                 "для обмена рецептами меж-\nду пользователями."
                 " Программа разработана \nстудентами БНТУ:\n"
                 "Лях Андрей Игоревич гр. 10701323\n"
                 "Куцко Владислав Витальевич гр. 10701123",
        )
        self.about_label.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

# Registration frame
class RegistrationFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master
        self.language = master.language
        self.theme = master.theme

        self.configure(fg_color=self.theme['background_color'])
        self.setup_register_frame()

    # Method for set up main registration frame
    def setup_register_frame(self) -> None:
        self.master.change_title(self.master.language['registration'])
        # Create the registration frame
        self.registration_frame = ctk.CTkFrame(
            master=self,
            width=320,
            height=380,
            fg_color=self.theme['frame_background_color'],
        )
        self.registration_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Верхний текст
        self.text = CTkLabel(
            master=self.registration_frame,
            text=self.language['welcome'],
            font=('Century Gothic', 25),
            text_color=self.theme['text_color'],
        )
        self.text.place(relx=0.5, y=50, anchor=ctk.CENTER)

        self.back_button = ctk.CTkButton(
            master=self,
            width=30,
            height=30,
            text=self.language['back'],
            corner_radius=6,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.master.open_main_frame
        )
        self.back_button.place(x=10, y=10)

        # Поле ввода логина
        self.username_entry = ctk.CTkEntry(
            master=self.registration_frame,
            width=220,
            border_width=0,
            placeholder_text=self.language['username'],
            placeholder_text_color=self.theme['textbox_text_color'],
            text_color=self.theme['textbox_text_color'],
            fg_color=self.theme['background_color'],
        )
        self.username_entry.place(x=50, y=100)

        # Поле ввода пароля
        self.show_password_var = ctk.BooleanVar()
        self.p_block = ctk.CTkEntry(
            master=self.registration_frame,
            width=220,
            placeholder_text=self.language['password'],
            show="*",
            border_width=0,
            placeholder_text_color=self.theme['textbox_text_color'],
            text_color=self.theme['textbox_text_color'],
            fg_color=self.theme['background_color'],
        )
        self.p_block.place(x=50, y=140)

        # Галочка показа пароля
        self.show_password = ctk.CTkCheckBox(
            master=self.registration_frame,
            text=self.language['show_password'],
            font=('Century Gothic', 12),
            border_width=2,
            command=lambda: toggle_password(self.p_block, self.show_password_var),
            variable=self.show_password_var,
            text_color=self.theme['text_color'],
            fg_color=self.theme['button_color'],
            hover_color=self.theme['hover_color'],
        )
        self.show_password.place(x=50, y=190)

        self.register_button = ctk.CTkButton(
            master=self.registration_frame,
            width=120,
            text=self.language['sign_up'],
            corner_radius=6,
            fg_color=self.theme['button_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.new_user_data
        )
        self.register_button.place(relx=0.5, y=300, anchor=ctk.CENTER)

    # New user registration method
    def new_user_data(self) -> None:
        username = self.username_entry.get()
        password = self.p_block.get()

        if not username or not password:
            messagebox.showerror(self.language['error'], self.language['not_all_fields_are_filled_in_error'])
            return

        if register_user(username, password):
            messagebox.showinfo(self.language['success'], self.language['successful_registration_message'])
            self.registration_frame.place_forget()
            self.master.open_main_frame()
            return
        else:
            messagebox.showerror(self.language['error'], self.language['login_is_taken_error'])
            return