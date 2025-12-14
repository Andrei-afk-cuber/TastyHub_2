# libraries
from typing import Optional

import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os

# user libraries
from app.functions import save_recipe, load_recipes, update_recipe_by_id, EditableRecipeCard
from app.classes import Recipe, RecipeCard

# Main frmae class
class MainFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master
        self.theme = master.theme
        self.language = master.language
        self.configure(fg_color=self.theme['frame_background_color'])
        # Load recipes
        self.recipes = load_recipes()

        # Variable for search type
        self.radiobutton_variable = ctk.StringVar(value="name")

        self.setup_main_frame()

    # Main frame set up method
    def setup_main_frame(self) -> None:
        self.main_frame = ctk.CTkFrame(master=self, width=1270, height=150, fg_color=self.theme['background_color'])
        self.main_frame.place(relx=0.5, rely=0.12, anchor=ctk.CENTER)

        # Close program button
        self.exit_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            text=self.language['close'],
            corner_radius=6,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.close_program
        )
        self.exit_button.place(x=1160, y=10)

        # Search entry
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

        # Button for search recipes
        self.search_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            height=40,
            text=self.language['search'],
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
            text=self.language['add_recipe'],
            corner_radius=6,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.master.open_add_recipe_frame
        )
        self.add_recipe_button.place(x=10, y=10)

        # Open user profile frame
        self.user_profile_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            text=self.language['my_posts'],
            corner_radius=6,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.master.open_user_profile_frame
        )
        self.user_profile_button.place(x=1040, y=10)

        search_by_name = ctk.CTkRadioButton(
            master=self.main_frame,
            text=self.language['by_name'],
            value="name",
            variable=self.radiobutton_variable,
            fg_color='white',
            hover_color=self.theme['hover_color'],
            text_color=self.theme['text_color'],
        )
        search_by_name.place(relx=0.3, y=110)

        search_by_ingredients = ctk.CTkRadioButton(
            master=self.main_frame,
            text=self.language['by_products'],
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

        # Display recipes
        self.display_recipes()

    # Method for close program
    def close_program(self) -> None:
        self.master.destroy()

    # Merhod for display recipes
    def display_recipes(self, by_name: Optional[str]=None, by_ingredients: Optional[str]=None) -> None:
        if by_name:
            self.recipes = load_recipes(by_name=by_name)
        elif by_ingredients:
            self.recipes = load_recipes(by_ingredients=by_ingredients)
        else:
            self.recipes = load_recipes()

        for widget in self.recipes_container.winfo_children():
            widget.destroy()
        if self.recipes:
            for i, recipe in enumerate(self.recipes):
                card = RecipeCard(
                    master=self.recipes_container,
                    recipe=recipe,
                    main_program=self.master
                )
                card.grid(row=i//5, column=i%5, padx=20, pady=10)

    # Method for search recipes
    def search_recipes(self) -> None:
        search_request = self.search_entry.get().strip().lower()

        if not search_request:
            self.display_recipes()
            return

        if self.radiobutton_variable.get() == "name":
            search_request = self.search_entry.get().strip().lower()
            self.display_recipes(by_name=search_request)
        elif self.radiobutton_variable.get() == "ingredients":
            search_request = self.search_entry.get().strip().lower()
            search_request = [product.strip().lower() for product in self.search_entry.get().split(',')]
            self.display_recipes(by_ingredients=search_request)

# Class for add recipe frame
class AddRecipeFrame(ctk.CTkFrame):
    def __init__(self, master, recipe: Optional[Recipe]=None, admin: bool=False) -> None:
        super().__init__(master)
        self.master = master
        self.theme = master.theme
        self.language = master.language
        self.recipe = recipe
        self.admin = admin
        self.selected_image_path = None

        self.configure(fg_color=self.theme['frame_background_color'])
        self.setup_add_recipe_frame()

    # load recipe image
    def load_existing_recipe_image(self) -> None:
        try:
            if not self.recipe or not self.recipe.picture_path:
                return

            image_path = os.path.join("recipe_images", self.recipe.picture_path)
            if os.path.exists(image_path):
                self.selected_image_path = image_path

                img = Image.open(image_path)
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
            else:
                self.recipe_image_label.configure(
                    text=self.language['image_is_not_found_error'],
                    text_color="red"
                )
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.recipe_image_label.configure(
                text=self.language['load_image_error'],
                text_color="red"
            )

    # method for set up add recipe frame
    def setup_add_recipe_frame(self):
        self.header_frame = ctk.CTkFrame(master=self, width=1270, height=50, fg_color=self.theme['background_color'])
        self.header_frame.place(relx=0.5, rely=0.05, anchor=ctk.CENTER)

        # top text
        self.text = ctk.CTkLabel(
            master=self.header_frame,
            text=self.language['adding_recipe'],
            font=('Century Gothic', 36),
            text_color=self.theme['text_color']
        )
        self.text.place(relx=0.35, rely=0)

        # back to main frame button
        self.back_to_main_button = ctk.CTkButton(
            master=self.header_frame,
            width=100,
            text=self.language['back'],
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

        # recipe name entry
        self.recipe_name_entry = ctk.CTkEntry(
            master=self.recipe_data_frame,
            width=200,
            placeholder_text=self.language['recipe_name'],
            font=('Century Gothic', 12),
            border_width=0,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            placeholder_text_color=self.theme['text_color']
        )
        self.recipe_name_entry.place(x=25, y=10)

        # recipe cooking time entry
        self.recipe_cocking_time_entry = ctk.CTkEntry(
            master=self.recipe_data_frame,
            width=200,
            placeholder_text=self.language['cooking_time'],
            font=('Century Gothic', 12),
            border_width=0,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            placeholder_text_color=self.theme['text_color']
        )
        self.recipe_cocking_time_entry.place(x=25, y=50)

        # products label
        ctk.CTkLabel(
            master=self.recipe_data_frame,
            text=self.language['products'],
            font=('Century Gothic', 16),
            text_color=self.theme['text_color'],
        ).place(x=30, y=90)

        # textbox for products
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

        # Frame for recipe photo
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

        # Image label
        self.recipe_image_label = ctk.CTkLabel(
            master=self.recipe_photo_frame,
            text=self.language['recipe_image'],
            width=280,
            height=180,
            fg_color="#f5f5f5",
            corner_radius=8,
            text_color="gray"
        )
        self.recipe_image_label.pack(pady=10)

        # Button for load recipe image
        self.load_image_button = ctk.CTkButton(
            master=self.recipe_data_frame,
            fg_color=self.theme['frame_background_color'],
            hover_color=self.theme['hover_color'],
            text_color=self.theme['text_color'],
            corner_radius=6,
            font=('Century Gothic', 12),
            text=self.language['load_image'],
            command=self.load_image_dialog
        )
        self.load_image_button.place(relx=0.5, y=260, anchor=ctk.CENTER)

        # Description label
        ctk.CTkLabel(
            master=self.recipe_data_frame,
            text=self.language['description'],
            font=('Century Gothic', 16),
            text_color=self.theme['text_color']
        ).place(x=30, y=260)

        # Textbox for description
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

        # Send recipe button
        self.send_recipe_button = ctk.CTkButton(
            master=self.recipe_data_frame,
            text=self.language['send'],
            corner_radius=6,
            font=('Century Gothic', 24),
            command=self.send_recipe,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color']
        )
        self.send_recipe_button.place(relx=0.87, y=570)

        if self.recipe:
            # Change buttons params
            self.send_recipe_button.configure(text=self.language['save'], command=lambda: self.send_recipe(update=True, by_admin=self.admin))
            self.text.configure(text=self.language['recipe_editing'])

            # Set values for fields
            self.recipe_name_entry.insert(0, self.recipe.name)
            self.recipe_cocking_time_entry.insert(0, str(self.recipe.cooking_time))
            self.recipe_description_textbox.insert("1.0", self.recipe.description)
            self.recipe_product_textbox.insert("1.0", ", ".join(self.recipe.products))

            # Load existing recipe image
            self.load_existing_recipe_image()

    # Method for resize image
    def resize_image(self, img, max_width: int, max_height: int) -> Image:
        img_ratio = img.width / img.height
        frame_ratio = max_width / max_height

        if img_ratio > frame_ratio:
            new_width = max_width
            new_height = int(max_width / img_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * img_ratio)

        return img.resize((new_width, new_height), Image.LANCZOS)

    # Send recipe mthod
    def send_recipe(self, update: bool =False, by_admin: bool =False) -> None:
        name = self.recipe_name_entry.get().strip().lower()
        try:
            cooking_time = int(self.recipe_cocking_time_entry.get().strip())
        except ValueError:
            messagebox.showerror(self.language['error'], self.language['incorrect_cooking_time_error'])

        products = self.recipe_product_textbox.get('1.0', 'end').strip()
        description = self.recipe_description_textbox.get('1.0', 'end').strip()
        try:
            picture_path = self.selected_image_path
        except:
            messagebox.showerror(self.language['error'], self.language['image_is_not_found_error'])


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
            messagebox.showerror(self.language['error'], self.language['not_all_fields_are_filled_in_error'])

    # dialog for load image
    def load_image_dialog(self) -> None:
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
                messagebox.showerror(self.language['error'], f"{self.language['load_image_error']}: {str(e)}")

# Class for show recipe frame
class ShowRecipeFrame(ctk.CTkFrame):
    def __init__(self, master, recipe: Recipe) -> None:
        super().__init__(master)
        self.master = master
        self.theme = master.theme
        self.language = master.language
        self.recipe = recipe

        self.configure(fg_color=self.theme['frame_background_color'])
        self.setup_show_recipe_frame()

    # set up frame
    def setup_show_recipe_frame(self) -> None:
        # Main frame
        self.show_recipe_frame = ctk.CTkFrame(
            master=self,
            width=1270,
            height=50,
            fg_color="transparent"
        )
        self.show_recipe_frame.place(relx=0.5, rely=0.05, anchor=ctk.CENTER)

        # Back button
        self.back_to_main = ctk.CTkButton(
            master=self.show_recipe_frame,
            width=100,
            text=self.language['back'],
            corner_radius=6,
            fg_color=self.theme['background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.master.open_main_frame
        )
        self.back_to_main.place(x=10, y=10)

        # Recipe name and author
        ctk.CTkLabel(
            master=self.show_recipe_frame,
            text=f"{self.recipe.name} by {self.recipe.user_name} ({self.recipe.cooking_time} мин.)",
            font=('Century Gothic', 24, 'bold'),
            text_color=self.theme['text_color'],
        ).place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Image frame
        self.image_frame = ctk.CTkFrame(
            master=self,
            fg_color=self.theme['frame_background_color'],
        )
        self.image_frame.place(relx=0.5, rely=0.25, anchor=ctk.CENTER)

        # Image label
        self.image_label = ctk.CTkLabel(
            master=self.image_frame,
            text="",
            corner_radius=8,
            fg_color="transparent",
            text_color=self.theme['text_color'],
        )
        self.image_label.pack(pady=10)

        # Products label
        ctk.CTkLabel(
            master=self,
            text=self.language['products'],
            font=('Century Gothic', 24, 'bold'),
            text_color="orange"
        ).place(relx=0.08, rely=0.15, anchor=ctk.CENTER)

        # Products list
        start_y = 130
        for ingredient in self.recipe.products:
            ctk.CTkLabel(
                master=self,
                text=f"• {ingredient}",
                font=('Century Gothic', 20),
                text_color=self.theme['text_color'],
            ).place(relx=0.015, y=start_y)
            start_y += 30

        # Recipe description frame
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

        # Load image
        self.load_recipe_image()

    # Method for load recipe image
    def load_recipe_image(self) -> None:
        try:
            image_path = os.path.join("recipe_images", self.recipe.picture_path)

            if os.path.exists(image_path):
                img = Image.open(image_path)

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
                    text=self.language['image_is_not_found_error'],
                )
        except Exception as e:
            self.image_label.configure(
                text=self.language['load_image_error'] + str(e),
                font=('Century Gothic', 14),
                text_color="red"
            )

# class for user profile frame
class UserProfileFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master
        self.theme = master.theme
        self.language = master.language
        self.recipes = load_recipes(by_username=self.master.user.username, only_confirmed=False)

        self.configure(fg_color=self.theme['frame_background_color'])
        self.setup_user_profile_frame()

    # set up user profile frame
    def setup_user_profile_frame(self) -> None:
        # Header frame
        self.header_frame = ctk.CTkFrame(master=self, width=1270, height=50, fg_color=self.theme['background_color'])
        self.header_frame.place(relx=0.5, y=30, anchor=ctk.CENTER)

        # Back button
        self.back_to_main_button = ctk.CTkButton(
            master=self.header_frame,
            width=100,
            text=self.language['back'],
            corner_radius=6,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.master.open_main_frame
        )
        self.back_to_main_button.place(x=10, y=10)

        # Header label
        ctk.CTkLabel(
            master=self.header_frame,
            text=self.language['user_profile'] + self.master.user.username,
            font=('Century Gothic', 24),
            text_color=self.theme['text_color'],
        ).place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkLabel(
            master=self,
            text=self.language['your_posts'],
            font=('Century Gothic', 24, 'bold'),
            text_color=self.theme['text_color'],
        ).place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

        # Frame for showing recipe cards
        self.recipes_container = ctk.CTkScrollableFrame(
            master=self,
            width=1200,
            height=500,
            fg_color="transparent",
        )
        self.recipes_container.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

        # Display recipes
        self.display_recipes()

    # Method for display recipes
    def display_recipes(self):
        self.recipes = load_recipes(by_username=self.master.user.username, only_confirmed=False)
        for widget in self.recipes_container.winfo_children():
            widget.destroy()

        if self.recipes:
            for i, recipe in enumerate(self.recipes):
                card = EditableRecipeCard(
                    master=self.recipes_container,
                    recipe=recipe,
                    main_program=self.master
                )
                card.grid(row=i // 5, column=i % 5, padx=5, pady=10)