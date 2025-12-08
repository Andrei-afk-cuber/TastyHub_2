import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os

from app.config import day_theme as theme
from app.functions import save_recipe, load_recipes, load_products, update_recipe_by_id, EditableRecipeCard
from app.classes import Recipe, RecipeCard

# Класс основного фрейма приложения
class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.theme = master.theme
        self.configure(fg_color=self.theme['frame_background_color'])
        # Загружаем рецепты
        self.recipes = load_recipes()

        # Переменная для поиска
        self.radiobutton_variable = ctk.StringVar(value="name")

        self.setup_main_frame()

    # Функция для отрисовки основного фрейма
    def setup_main_frame(self):
        # Создаем фрейм сверху страницы
        self.main_frame = ctk.CTkFrame(master=self, width=1270, height=150, fg_color=self.theme['background_color'])
        self.main_frame.place(relx=0.5, rely=0.12, anchor=ctk.CENTER)

        # Кнопка закрытия программы
        self.exit_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            text="Закрыть",
            corner_radius=6,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.close_program
        )
        self.exit_button.place(x=1160, y=10)

        # Поле ввода для поиска
        self.search_entry = ctk.CTkEntry(
            master=self.main_frame,
            fg_color=self.theme['frame_background_color'],
            corner_radius=6,
            border_width=0,
            text_color=self.theme['text_color'],
            placeholder_text_color=self.theme['text_color'],
            bg_color=self.theme['background_color'],
            width=800,
            height=40,
            font=('Century Gothic', 16)
        )
        self.search_entry.place(relx=0.12, y=60)

        # Кнопка поиска
        self.search_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            height=40,
            text="Поиск",
            corner_radius=6,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command = self.search_recipes
        )
        self.search_button.place(x=980, y=60)

        # Add recipe button
        self.add_recipe_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            text="Добавить рецепт",
            corner_radius=6,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.master.open_add_recipe_frame
        )
        self.add_recipe_button.place(x=10, y=10)

        # Кнопка открытия профиля пользователя
        self.user_profile_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            text="Мои публикации",
            corner_radius=6,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.master.open_user_profile_frame
        )
        self.user_profile_button.place(x=1040, y=10)

        search_by_name = ctk.CTkRadioButton(
            master=self.main_frame,
            text="По имени",
            value="name",
            variable=self.radiobutton_variable,
            fg_color='white',
            hover_color=self.theme['hover_color'],
            text_color=self.theme['text_color'],
        )
        search_by_name.place(relx=0.3, y=110)

        search_by_ingredients = ctk.CTkRadioButton(
            master=self.main_frame,
            text="По ингредиентам",
            value="ingredients",
            variable=self.radiobutton_variable,
            fg_color='white',
            hover_color=self.theme['hover_color'],
            text_color=self.theme['text_color']
        )
        search_by_ingredients.place(relx=0.5, y=110)

        # Создаем фрейм для отображения карточек рецептов
        self.recipes_container = ctk.CTkScrollableFrame(
            master=self,
            width=1200,
            height=500,
            fg_color="transparent",
        )
        self.recipes_container.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

        # Отображаем рецепты
        self.display_recipes()

    # Функция для закрытия программы
    def close_program(self):
        self.master.destroy()

    # Метод отображения рецептов
    def display_recipes(self, by_name=None, by_ingredients=None):
        if by_name:
            self.recipes = load_recipes(by_name=by_name)
        elif by_ingredients:
            self.recipes = load_recipes(by_ingredients=by_ingredients)
        else:
            self.recipes = load_recipes()

        # Очищаем контейнер перед добавлением новых карточек
        for widget in self.recipes_container.winfo_children():
            widget.destroy()
        if self.recipes:
            # Создаем карточки для каждого рецепта
            for i, recipe in enumerate(self.recipes):
                card = RecipeCard(
                    master=self.recipes_container,
                    recipe=recipe,
                    main_program=self.master
                )
                card.grid(row=i//5, column=i%5, padx=20, pady=10)

    # Метод для поиска рецептов по параметрам
    def search_recipes(self):
        search_request = self.search_entry.get().strip().lower()

        if not search_request:
            self.display_recipes()
            return

        if self.radiobutton_variable.get() == "name":
            print("Поиск по названию рецепта")
            search_request = self.search_entry.get().strip().lower()
            self.display_recipes(by_name=search_request)
        elif self.radiobutton_variable.get() == "ingredients":
            print("Поиск по ингредиентам")
            search_request = self.search_entry.get().strip().lower()
            search_request = [product.strip().lower() for product in self.search_entry.get().split(',')]
            self.display_recipes(by_ingredients=search_request)

class AddRecipeFrame(ctk.CTkFrame):
    def __init__(self, master, recipe=None, admin=False):
        super().__init__(master)
        
        self.master = master
        self.theme = master.theme
        self.recipe = recipe
        self.admin = admin
        self.selected_image_path = None
        self.products = load_products()

        self.configure(fg_color=self.theme['frame_background_color'])
        self.setup_add_recipe_frame()

    def load_existing_recipe_image(self):
        try:
            if not self.recipe or not self.recipe.picture_path:
                return

            image_path = os.path.join("recipe_images", self.recipe.picture_path)
            if os.path.exists(image_path):
                # Сохраняем путь к текущему изображению
                self.selected_image_path = image_path

                # Создаем CTkImage
                img = Image.open(image_path)
                img = self.resize_image(img, 280, 180)
                self.recipe_image = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(280, 180)
                )

                # Устанавливаем изображение
                self.recipe_image_label.configure(
                    image=self.recipe_image,
                    text=""
                )
            else:
                self.recipe_image_label.configure(
                    text="Изображение не найдено",
                    text_color="red"
                )
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.recipe_image_label.configure(
                text="Ошибка загрузки",
                text_color="red"
            )

    def setup_add_recipe_frame(self):
        # Create recipe frame
        self.header_frame = ctk.CTkFrame(master=self, width=1270, height=50, fg_color=self.theme['background_color'])
        self.header_frame.place(relx=0.5, rely=0.05, anchor=ctk.CENTER)

        # top text
        self.text = ctk.CTkLabel(
            master=self.header_frame,
            text="Добавление рецепта",
            font=('Century Gothic', 36),
            text_color=self.theme['text_color']
        )
        self.text.place(relx=0.35, rely=0)

        # Кнопка возврата к основному фрейму
        self.back_to_main_button = ctk.CTkButton(
            master=self.header_frame,
            width=100,
            text="Назад",
            corner_radius=6,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.master.open_main_frame
        )
        self.back_to_main_button.place(x=10, y=10)

        self.recipe_data_frame = ctk.CTkFrame(
            master=self,
            width=1270,
            height=620,
            fg_color=self.theme['background_color'],
        )
        self.recipe_data_frame.place(relx=0.005, y=70)

        # Поле ввода названия рецепта
        self.recipe_name_entry = ctk.CTkEntry(
            master=self.recipe_data_frame,
            width=200,
            placeholder_text="Название рецепта",
            font=('Century Gothic', 12),
            border_width=0,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            placeholder_text_color=self.theme['text_color']
        )
        self.recipe_name_entry.place(x=25, y=10)

        # Поле ввода времени приготовления
        self.recipe_cocking_time_entry = ctk.CTkEntry(
            master=self.recipe_data_frame,
            width=200,
            placeholder_text="Время приготовления (мин)",
            font=('Century Gothic', 12),
            border_width=0,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            placeholder_text_color=self.theme['text_color']
        )
        self.recipe_cocking_time_entry.place(x=25, y=50)

        # метка продуктов
        ctk.CTkLabel(
            master=self.recipe_data_frame,
            text="Продукты: ",
            font=('Century Gothic', 16),
            text_color=self.theme['text_color'],
        ).place(x=30, y=90)

        # поле для ввода продуктов для рецепта
        self.recipe_product_textbox = ctk.CTkTextbox(
            master=self.recipe_data_frame,
            font=('Century Gothic', 12),
            corner_radius=12,
            width=200,
            height=100,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color']
        )
        self.recipe_product_textbox.place(x=25, y=130)

        # Фрейм для изображения блюда
        self.recipe_photo_frame = ctk.CTkFrame(
            master=self.recipe_data_frame,
            width=300,
            height=200,
            fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color="#e0e0e0"
        )
        self.recipe_photo_frame.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

        # Метка для изображения
        self.recipe_image_label = ctk.CTkLabel(
            master=self.recipe_photo_frame,
            text="Изображение рецепта",
            width=280,
            height=180,
            fg_color="#f5f5f5",
            corner_radius=8,
            text_color="gray"
        )
        self.recipe_image_label.pack(pady=10)

        self.load_image_button = ctk.CTkButton(
            master=self.recipe_data_frame,
            fg_color=self.theme['frame_background_color'],
            hover_color=self.theme['hover_color'],
            text_color=self.theme['text_color'],
            corner_radius=6,
            font=('Century Gothic', 12),
            text="Загрузить изображение",
            command=self.load_image_dialog
        )
        self.load_image_button.place(relx=0.5, y=260, anchor=ctk.CENTER)

        # метка описания
        ctk.CTkLabel(
            master=self.recipe_data_frame,
            text="Описание: ",
            font=('Century Gothic', 16),
            text_color=self.theme['text_color']
        ).place(x=30, y=260)

        # поле для ввода описания рецепта
        self.recipe_description_textbox = ctk.CTkTextbox(
            master=self.recipe_data_frame,
            font=('Century Gothic', 12),
            corner_radius=12,
            width=1220,
            height=240,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color']
        )
        self.recipe_description_textbox.place(relx=0.5, y=430, anchor=ctk.CENTER)

        # кнопка подтверждения добавления рецепта
        self.send_recipe_button = ctk.CTkButton(
            master=self.recipe_data_frame,
            text="Отправить",
            corner_radius=6,
            font=('Century Gothic', 24),
            command=self.send_recipe,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color']
        )
        self.send_recipe_button.place(relx=0.87, y=570)

        if self.recipe:
            # Изменяем параметры кнопок
            self.send_recipe_button.configure(text="Сохранить", command=lambda: self.send_recipe(update=True, by_admin=self.admin))
            self.text.configure(text="Редактирование рецепта")

            # Устанавливаем значения для полей рецепта
            self.recipe_name_entry.insert(0, self.recipe.name)
            self.recipe_cocking_time_entry.insert(0, str(self.recipe.cooking_time))
            self.recipe_description_textbox.insert("1.0", self.recipe.description)
            self.recipe_product_textbox.insert("1.0", ", ".join(self.recipe.products))

            # Загружаем существующее изображение рецепта
            self.load_existing_recipe_image()
    # Метод для загрузки изображения уже существующего рецепта

    # Метод изменения изображения рецепта с сохранением пропорций
    def resize_image(self, img, max_width, max_height):
        img_ratio = img.width / img.height
        frame_ratio = max_width / max_height

        if img_ratio > frame_ratio:
            new_width = max_width
            new_height = int(max_width / img_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * img_ratio)

        return img.resize((new_width, new_height), Image.LANCZOS)

    # method for get all products from server
    def load_products(self):
        pass

    # Метод отправки рецепта
    def send_recipe(self, update=False, by_admin=False):
        name = self.recipe_name_entry.get().strip().lower()
        try:
            cooking_time = int(self.recipe_cocking_time_entry.get().strip())
        except ValueError:
            messagebox.showerror("Ошибка", "Время приготовления должно быть целым числом")

        products = self.recipe_product_textbox.get('1.0', 'end').strip()
        description = self.recipe_description_textbox.get('1.0', 'end').strip()
        try:
            picture_path = self.selected_image_path
        except:
            messagebox.showerror("Ошибка", "Выберите картинку для рецепта")


        if name and cooking_time and products and description and picture_path:
            if self.recipe:
                author_name = self.recipe.user_name
            else:
                author_name = self.master.user.username

            products = [i.strip().lower() for i in products.split(',')]
            recipe = Recipe(
                None,
                name=name,
                description=description,
                cooking_time=cooking_time,
                picture_path=picture_path,
                confirmed=1 if by_admin else 0,
                user_name=author_name,
                products=products
            )

            # Сохраняем или заменяем существующий рецепт
            if update:
                update_recipe_by_id(self.recipe, recipe, by_admin=by_admin)
            else:
                save_recipe(recipe)

            self.master.open_main_frame()

            return
        else:
            messagebox.showerror("Ошибка", "Вы не заполнили все поля")

        print("Вы отправили рецепт")

    def load_image_dialog(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            self.selected_image_path = file_path
            try:
                img = Image.open(file_path)
                img = self.resize_image(img, 280, 180)
                self.recipe_image = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(280, 180)
                )
                self.recipe_image_label.configure(
                    image=self.recipe_image,
                    text=""
                )
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {str(e)}")

class ShowRecipeFrame(ctk.CTkFrame):
    def __init__(self, master, recipe):
        super().__init__(master)
        self.master = master
        self.theme = master.theme
        self.recipe = recipe

        self.configure(fg_color=self.theme['frame_background_color'])
        self.setup_show_recipe_frame()

    def setup_show_recipe_frame(self):
        # Основной фрейм заголовка
        self.show_recipe_frame = ctk.CTkFrame(
            master=self,
            width=1270,
            height=50,
            fg_color="transparent"
        )
        self.show_recipe_frame.place(relx=0.5, rely=0.05, anchor=ctk.CENTER)

        # Кнопка возврата
        self.back_to_main = ctk.CTkButton(
            master=self.show_recipe_frame,
            width=100,
            text="Назад",
            corner_radius=6,
            fg_color=self.theme['background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.master.open_main_frame
        )
        self.back_to_main.place(x=10, y=10)

        # Название рецепта и автор
        ctk.CTkLabel(
            master=self.show_recipe_frame,
            text=f"{self.recipe.name} by {self.recipe.user_name} ({self.recipe.cooking_time} мин.)",
            font=('Century Gothic', 24, 'bold'),
            text_color=self.theme['text_color'],
        ).place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Контейнер для изображения
        self.image_frame = ctk.CTkFrame(
            master=self,
            fg_color=self.theme['frame_background_color'],
        )
        self.image_frame.place(relx=0.5, rely=0.25, anchor=ctk.CENTER)

        # Метка для изображения
        self.image_label = ctk.CTkLabel(
            master=self.image_frame,
            text="",
            corner_radius=8,
            fg_color="transparent",
            text_color=self.theme['text_color'],
        )
        self.image_label.pack(pady=10)

        # Заголовок ингредиентов
        ctk.CTkLabel(
            master=self,
            text="Ингредиенты:",
            font=('Century Gothic', 24, 'bold'),
            text_color="orange"
        ).place(relx=0.08, rely=0.15, anchor=ctk.CENTER)

        # Список ингредиентов
        start_y = 130
        for ingredient in self.recipe.products:
            ctk.CTkLabel(
                master=self,
                text=f"• {ingredient}",
                font=('Century Gothic', 20),
                text_color=self.theme['text_color'],
            ).place(relx=0.015, y=start_y)
            start_y += 30

        # Фрейм с описанием рецепта
        self.recipe_description_frame = ctk.CTkScrollableFrame(
            master=self,
            width=1200,
            height=380,
            corner_radius=10,
            fg_color="transparent"
        )
        self.recipe_description_frame.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

        self.description_text = ctk.CTkTextbox(
            master=self.recipe_description_frame,
            width=1150,
            height=300,
            font=('Century Gothic', 14),
            wrap="word",  # Перенос по словам
            fg_color=self.theme['background_color'],
            text_color=self.theme['text_color'],
            border_width=0,
            border_color="#e0e0e0",
            corner_radius=8,
            padx=10,
            pady=10
        )
        self.description_text.insert("1.0", self.recipe.description)
        self.description_text.configure(state="disabled")  # Запрещаем редактирование
        self.description_text.pack(pady=(0, 10), padx=20, fill="both", expand=True)

        # Загружаем изображение
        self.load_recipe_image()

    def load_recipe_image(self):
        try:
            image_path = os.path.join("recipe_images", self.recipe.picture_path)

            if os.path.exists(image_path):
                img = Image.open(image_path)

                # Ресайз с сохранением пропорций
                width, height = 380, 280
                img_ratio = img.width / img.height
                frame_ratio = width / height

                if img_ratio > frame_ratio:
                    new_width = width
                    new_height = int(width / img_ratio)
                else:
                    new_height = height
                    new_width = int(height * img_ratio)

                img = img.resize((new_width, new_height), Image.LANCZOS)
                self.recipe_image = ImageTk.PhotoImage(img)

                self.image_label.configure(
                    image=self.recipe_image,
                    text=""
                )
            else:
                self.image_label.configure(
                    text="Изображение не найдено",
                )
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.image_label.configure(
                text="Ошибка загрузки",
                font=('Century Gothic', 14),
                text_color="red"
            )

class UserProfileFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.theme = master.theme
        self.recipes = load_recipes(by_name=self.master.user.username, only_confirmed=False)

        self.configure(fg_color=self.theme['frame_background_color'])
        self.setup_user_profile_frame()

    def setup_user_profile_frame(self):
        # Создаем фрейм сверху страницы
        self.header_frame = ctk.CTkFrame(master=self, width=1270, height=50, fg_color=self.theme['background_color'])
        self.header_frame.place(relx=0.5, y=30, anchor=ctk.CENTER)

        # Кнопка возврата к основному фрейму
        self.back_to_main_button = ctk.CTkButton(
            master=self.header_frame,
            width=100,
            text="Назад",
            corner_radius=6,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.master.open_main_frame
        )
        self.back_to_main_button.place(x=10, y=10)

        ctk.CTkLabel(
            master=self.header_frame,
            text=f"Профиль пользователя {self.master.user.username}",
            font=('Century Gothic', 24),
            text_color=self.theme['text_color'],
        ).place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkLabel(
            master=self,
            text="Ваши посты",
            font=('Century Gothic', 24, 'bold'),
            text_color=self.theme['text_color'],
        ).place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

        # Создаем фрейм для отображения карточек рецептов
        self.recipes_container = ctk.CTkScrollableFrame(
            master=self,
            width=1200,
            height=500,
            fg_color="transparent",
        )
        self.recipes_container.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

        # Отображаем рецепты
        self.display_recipes()

    # Метод отображения рецептов
    def display_recipes(self):
        self.recipes = load_recipes(by_username=self.master.user.username, only_confirmed=False)
        # Очищаем контейнер перед добавлением новых карточек
        for widget in self.recipes_container.winfo_children():
            widget.destroy()

        # Создаем карточки для каждого рецепта
        for i, recipe in enumerate(self.recipes):
            card = EditableRecipeCard(
                master=self.recipes_container,
                recipe=recipe,
                main_program=self.master
            )
            card.grid(row=i // 5, column=i % 5, padx=5, pady=10)