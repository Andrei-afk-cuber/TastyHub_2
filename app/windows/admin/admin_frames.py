import customtkinter as ctk
from customtkinter import CTkLabel
from app.windows.login.config import theme
from app.functions import load_users, load_recipes, AdminRecipeCard, UserCard

# Класс основного фрейма приложения
class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Загружаем пользователей и рецепты из БД
        self.users = None
        self.recipes = None

        self.setup_main_frame()

    # Функция для отрисовки основного фрейма
    def setup_main_frame(self):
        self.main_frame = ctk.CTkFrame(master=self, width=1270, height=50)
        self.main_frame.place(relx=0.5, rely=0.05, anchor=ctk.CENTER)

        # top text
        self.text = CTkLabel(
            master=self.main_frame,
            text=self.master.user.getUsername(),
            font=('Times New Roman', 12)
        )
        self.text.place(x=90, y=45)

        # Кнопка выхода
        self.exit_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            text="Закрыть",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.close_program
        )
        self.exit_button.place(x=1160, y=10)

        # Кнопка для просмотра пользователей
        self.users_check_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            text="Пользователи",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.display_users
        )
        self.users_check_button.place(relx=0.4, y=10)

        # Кнопка для просмотра рецептов
        self.recipes_check_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            text="Публикации",
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.display_recipes
        )
        self.recipes_check_button.place(relx=0.5, y=10)

        # Контейнер для размещения на нем информации
        self.data_container = ctk.CTkScrollableFrame(
            master=self,
            width=1250,
            height=600,
            fg_color="transparent",
        )
        self.data_container.place(relx=0.5, rely=0.55, anchor=ctk.CENTER)

    # Функция для закрытия программы
    def close_program(self):
        self.master.destroy()


    def display_users(self):
        # Загружаем пользователей из БД
        self.users = load_users()

        # Очищаем контейнер, перед добавлением новых карточек
        for widget in self.data_container.winfo_children():
            widget.destroy()

        # Создаем карточки для каждого пользователя
        for i, user in enumerate(self.users):
            card = UserCard(
                master=self.data_container,
                user=user,
                main_program=self.master
            )
            card.grid(row=i, column=0, padx=10, pady=5, sticky="ew")

    # Метод для отображения рецептов
    def display_recipes(self):
        # Загружаем рецепты из БД
        self.recipes = load_recipes(only_confirmed=False)

        # Очищаем контейнер, перед добавлением новых карточек
        for widget in self.data_container.winfo_children():
            widget.destroy()

        # Создаем карточки для каждого рецепта
        for i, recipe in enumerate(self.recipes):
            card = AdminRecipeCard(
                master=self.data_container,
                recipe=recipe,
                main_program=self.master
            )
            card.grid(pady=5, padx=5, sticky="ew")