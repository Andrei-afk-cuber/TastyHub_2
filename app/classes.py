import customtkinter as ctk
import os
from PIL import ImageTk, Image

from app.config import night_theme as theme

# user data-class
class User:
    def __init__(self, id: int, username: str, password: str, admin: int=0, authorized: int=0, recipes: list=[]) -> None:
        self._id = id
        self._username = username
        self._password = password
        self._admin = admin
        self._authorized = authorized
        self._recipes = recipes

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def admin(self) -> int:
        return self._admin

    @property
    def authorized(self) -> int:
        return self._authorized

    @property
    def recipes(self) -> list:
        return self._recipes

    def __repr__(self):
        return (f"User(id={self._id}, name={self._username}, password={self._password}, admin={bool(self._admin)}, "
                f"authorized={bool(self._authorized)}, recipes={self._recipes})")


# recipe data-class
class Recipe:
    def __init__(self, id, name, description, cooking_time, picture_path, confirmed, user_name, products):
        self._id = id
        self._name = name
        self._description = description
        self._cooking_time = cooking_time
        self._picture_path = picture_path
        self._confirmed = confirmed
        self._user_name = user_name
        self._products = products

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def cooking_time(self):
        return self._cooking_time

    @property
    def picture_path(self):
        return self._picture_path

    @property
    def confirmed(self):
        return self._confirmed

    @confirmed.setter
    def confirmed(self, value):
        self._confirmed = value

    @property
    def user_name(self):
        return self._user_name

    @property
    def products(self):
        return self._products

    def to_dict(self):
        return {
            'id': self._id,
            'name': self._name,
            'description': self.description,
            'cooking_time': self.cooking_time,
            'picture_path': self.picture_path,
            'confirmed': self.confirmed,
            'user_name': self.user_name,
            'products': self.products
        }

    def __repr__(self):
        return f"Recipe(id={self._id}, name={self._name}, user_name={self._user_name}...)"

class RecipeCard(ctk.CTkFrame):
    def __init__(self, master, recipe, main_program):
        self.theme = main_program.theme
        self.language = main_program.language
        super().__init__(
            master,
            fg_color=self.theme['background_color'],
            corner_radius=10,
            border_width=0,
            border_color="#e0e0e0",
            width=220,
            height=320
        )
        self.main_program = main_program
        self.recipe = recipe

        # Настройка сетки
        self.grid_columnconfigure(0, weight=1)

        # Название рецепта
        self.name_label = ctk.CTkLabel(
            self,
            text=recipe.name.capitalize(),
            font=("Arial", 14, "bold"),
            wraplength=180,
            text_color=self.theme['text_color'],
            height=40
        )
        self.name_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="n")

        # Изображение для рецепта
        self.image_label = ctk.CTkLabel(
            self,
            text="",
            width=180,
            height=120,
            fg_color="transparent",
            corner_radius=8,
            text_color=self.theme['text_color'],
        )
        self.image_label.grid(row=1, column=0, padx=10, pady=5)

        # Краткое описание
        short_desc = (recipe.description[:100] + "...") if len(
            recipe.description) > 100 else recipe.description
        self.desc_label = ctk.CTkLabel(
            self,
            text=short_desc,
            font=("Arial", 11),
            wraplength=180,
            justify="left",
            height=60,
            text_color=self.theme['text_color'],
        )
        self.desc_label.grid(row=2, column=0, padx=10, pady=5)

        # Кнопка "Подробнее"
        self.detail_btn = ctk.CTkButton(
            self,
            text=self.language['look'],
            width=120,
            height=30,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=lambda:self.main_program.open_show_recipe_frame(recipe)
        )
        self.detail_btn.grid(row=3, column=0, pady=(5, 10))

        self.load_recipe_image()

    def load_recipe_image(self):
        try:
            image_path = os.path.join("recipe_images", self.recipe.picture_path)

            # create folder if not exists
            if not os.path.exists(image_path):
                os.mkdir(image_path)

            if os.path.exists(image_path):
                img = Image.open(image_path)

                width, height = 200, 140
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
                    text=self.language['image_is_not_found_error'],
                )
        except Exception as e:
            self.image_label.configure(
                text=self.language['load_image_error'],
                font=('Century Gothic', 14),
                text_color="red"
            )