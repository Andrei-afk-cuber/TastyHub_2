import customtkinter as ctk
import os
from PIL import ImageTk, Image

class User(object):
    def __init__(self, username, password, admin=False, authorized=False, id=0):
        self.__id = id
        self.__username = username
        self.__password = password
        self.__admin = admin
        self.__authorized = authorized

    def getId(self):
        return self.__id

    def getUsername(self):
        return self.__username

    def getPassword(self):
        return self.__password

    def isAdmin(self):
        return self.__admin

    def isAuthorized(self):
        return self.__authorized

    def setUsername(self, login):
        self.__username = login

    def setPassword(self, password):
        self.__password = password

    def setAdmin(self, admin):
        self.__admin = admin

    def activateAccount(self):
        self.__authorized = True

    def deactivateAccount(self):
        self.__authorized = False

class Recipe(object):
    def __init__(self, author, name, description, picture_path, cooking_time = 0, product_list=[], confirmed=False, id=0):
        self.__id = id
        self.__name = name
        self.__description = description
        self.__cooking_time = cooking_time
        self.__product_list = product_list
        self.__confirmed = confirmed
        self.__picture_path = picture_path
        self.__author = author

    def getId(self):
        return self.__id

    def getAuthor(self):
        return self.__author

    def getName(self):
        return self.__name

    def getDescription(self):
        return self.__description

    def getCookingTime(self):
        return self.__cooking_time

    def getProductList(self):
        return self.__product_list

    def getPicturePath(self):
        return self.__picture_path

    def getConfirmed(self):
        return self.__confirmed

    def setName(self, name):
        self.__name = name

    def setAuthor(self, author):
        self.__author = author

    def setDescription(self, description):
        self.__description = description

    def setCookingTime(self, cooking_time):
        self.__cooking_time = cooking_time

    def setProductList(self, product_list):
        self.__product_list = product_list

    def setConfirmed(self, confirmed=True):
        self.__confirmed = confirmed

    def setPiсturePath(self, picture_path):
        self.__picture_path = picture_path

    def to_dict(self):
        return {
            "id": self.__id,
            "author": self.__author,
            "name": self.__name,
            "description": self.__description,
            "cooking_time": self.__cooking_time,
            "product_list": self.__product_list,
            "confirmed": self.__confirmed,
            "picture_path": self.__picture_path,
        }

class RecipeCard(ctk.CTkFrame):
    def __init__(self, master, recipe, main_program):
        super().__init__(
            master,
            fg_color=theme['recipe_card_fg_color'],
            corner_radius=10,
            border_width=1,
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
            text=recipe.getName().capitalize(),
            font=("Arial", 14, "bold"),
            wraplength=180,
            text_color=theme['text_color'],
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
            corner_radius=8
        )
        self.image_label.grid(row=1, column=0, padx=10, pady=5)

        # Краткое описание
        short_desc = (recipe.getDescription()[:100] + "...") if len(
            recipe.getDescription()) > 100 else recipe.getDescription()
        self.desc_label = ctk.CTkLabel(
            self,
            text=short_desc,
            font=("Arial", 11),
            wraplength=180,
            justify="left",
            height=60
        )
        self.desc_label.grid(row=2, column=0, padx=10, pady=5)

        # Кнопка "Подробнее"
        self.detail_btn = ctk.CTkButton(
            self,
            text="Подробнее",
            width=120,
            height=30,
            fg_color=theme['fg_color'],
            hover_color=theme['hover_color'],
            command=lambda:self.main_program.open_show_recipe_frame(recipe)
        )
        self.detail_btn.grid(row=3, column=0, pady=(5, 10))

        self.load_recipe_image()

    def load_recipe_image(self):
        try:
            image_path = os.path.join("recipe_images", self.recipe.getPicturePath())

            if os.path.exists(image_path):
                img = Image.open(image_path)

                # Ресайз с сохранением пропорций
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
                    text="Изображение не найдено"
                )
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.image_label.configure(
                text="Ошибка загрузки",
                font=('Century Gothic', 14),
                text_color="red"
            )