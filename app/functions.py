# importing necessary libraries
import sqlite3
import os
import shutil
from tkinter import messagebox
from PIL import Image
import customtkinter as ctk
import socket
import json
import datetime
import base64
import io
from typing import List, Optional

# importing my addictions
from app.classes import Recipe
from app.models.main import User
from app.config import SERVER_HOST, SERVER_PORT

# function for create requests to server
def send_request(request: dict) -> dict:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            s.connect((SERVER_HOST, SERVER_PORT))
            request_data = json.dumps(request).encode('utf-8')
            s.sendall(request_data)
            response = ""
            while True:
                chunk = s.recv(4096).decode('utf-8')
                if not chunk:
                    break
                response += chunk
                if response.endswith('}'):
                    break
            return json.loads(response)
    except (ConnectionError, json.JSONDecodeError) as e:
        print(f"Network error: {e}")
        return {"status": "error", "message": "Network error"}

# function for get database connection
def get_database_connection():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    return db, cursor

# close database connection
def close_database_connection(db):
    if db:
        db.close()

# function for load recipes from server
def load_recipes(only_confirmed: bool=True, by_name: str=None, by_ingredients: list=None, by_username: str=None):                             # temp method for check bug place
    response = send_request({
        "action": "load_recipes",
        "only_confirmed": only_confirmed,
        "by_name": by_name,
        "by_ingredients": by_ingredients,
        "by_username": by_username
    })
    if response.get("status") == "success":
        recipes = []
        os.makedirs("recipe_images", exist_ok=True)

        for recipe_data in response.get("recipes", []):
            picture_path = recipe_data['picture_path']
            if recipe_data.get('image_data'):
                try:
                    image_path = os.path.join("recipe_images", picture_path)

                    if not os.path.exists(image_path):
                        image_bytes = base64.b64decode(recipe_data['image_data'])
                        with open(image_path, 'wb') as img_file:
                            img_file.write(image_bytes)
                except Exception as e:
                    print(f"Image decode error: {e}")

            recipes.append(Recipe(
                recipe_data["id"],
                recipe_data['name'],
                recipe_data['description'],
                recipe_data['cooking_time'],
                picture_path,
                recipe_data['confirmed'],
                recipe_data['user_name'],
                recipe_data['products']
            ))

        return recipes

# load users data from server
def load_users() -> List[User]:
    response = send_request({"action": "load_users"})
    if response.get("status") == "success":
        users = []
        for user_data in response.get("users", []):
            try:
                users.append(User(
                    id=user_data["id"],
                    username=user_data['username'],
                    password=user_data['password'],
                    admin=user_data['admin'],
                    authorized=user_data['authorized']
                ))
            except Exception as e:
                print(f"Error creating User object: {e}")
                continue
        return users
    return []

# function for copy image
def copy_image(source_path: str, destination_folder: str="recipe_images") -> Optional[str]:
    try:
        if not os.path.exists(source_path):
            print(f"Ошибка: файла {source_path} не существует")
            return None
        os.makedirs(destination_folder, exist_ok=True)
        filename = os.path.basename(source_path)
        base, ext = os.path.splitext(filename)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"{base}_{timestamp}{ext}"
        unique_destination = os.path.join(destination_folder, unique_filename)
        shutil.copy2(source_path, unique_destination)
        return unique_destination
    except Exception as e:
        print(f"Ошибка при копировании: {e}")
        return None

# function for save recipe
def save_recipe(recipe: Recipe) -> Optional[int]:
    try:
        image_path = recipe.picture_path
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Файл изображения не найден: {image_path}")
        img = Image.open(image_path)
        max_size = (800, 800)
        img.thumbnail(max_size, Image.LANCZOS)
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        recipe_data = {
            "name": recipe.name,
            "description": recipe.description,
            "cooking_time": recipe.cooking_time,
            "picture_path": os.path.basename(recipe.picture_path),
            "confirmed": recipe.confirmed,
            "user_name": recipe.user_name,
            "image_data": image_data,
            "products": recipe.products
        }
        response = send_request({
            "action": "save_recipe",
            "recipe_data": recipe_data
        })
        if response.get("status") == "success":
            return response.get("recipe_id")
        else:
            messagebox.showerror("Ошибка", response.get("message", "Неизвестная ошибка сервера"))
            return None
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при сохранении рецепта: {str(e)}")
        return None

# method for update recipe
def update_recipe_by_id(old_recipe, new_recipe, by_admin: bool=False):
    delete_recipe(old_recipe)
    new_recipe.confirmed = int(by_admin)
    save_recipe(new_recipe)

# delete recipe function
def delete_recipe(recipe: Recipe) -> bool:
    response = send_request({
        "action": "delete_recipe",
        "recipe_id": recipe.id
    })
    return response.get("status") == "success"

# accept user function
def accept_user(user: User) -> bool:
    response = send_request({
        "action": "activate_user",
        "user_id": user.id
    })
    return response.get("status") == "success"

# function for grant admin privileges to user by id
def grant_admin_privileges(user: User) -> bool:
    accept_user(user)
    response = send_request({
        "action": "grant_admin_privileges",
        "user_id": user.id
    })
    return response.get("status") == "success"

# function for deleting user
def delete_user(user: User) -> bool:
    response = send_request({
        "action": "delete_user",
        "user_id": user.id
    })
    return response.get("status") == "success"

# transform json to dict function
def json_to_dict(filename: str) -> dict:
    with open(filename, encoding="utf-8") as json_file:
        data = json.load(json_file)

    return data

class EditableRecipeCard(ctk.CTkFrame):
    def __init__(self, master, recipe, main_program) -> None:
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
        self.ctk_image = None

        self.grid_columnconfigure(0, weight=1)

        self.name_label = ctk.CTkLabel(
            master=self,
            text=recipe.name.capitalize(),
            font=("Arial", 14, "bold"),
            wraplength=180,
            text_color=self.theme['text_color'],
            height=40
        )
        self.name_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="n")

        if not recipe.name:
            self.name_label.configure(text_color="red")

        self.image_label = ctk.CTkLabel(
            self,
            text="",
            width=180,
            height=120,
            fg_color="transparent",
            text_color=self.theme['text_color'],
            corner_radius=8
        )
        self.image_label.grid(row=1, column=0, padx=10, pady=5)

        short_desc = (recipe.getDescription()[:100] + "...") if len(
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

        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=3, column=0, pady=(5, 10))

        self.delete_btn = ctk.CTkButton(
            self.buttons_frame,
            text=self.language['delete'],
            width=10,
            height=30,
            fg_color="#db0404",
            hover_color="#910000",
            # text_color="white",
            text_color=self.theme['text_color'],
            command=self.confirm_delete
        )
        self.delete_btn.pack(side="left", padx=5)

        self.edit_btn = ctk.CTkButton(
            self.buttons_frame,
            text=self.language['edit'],
            width=100,
            height=30,
            fg_color=self.theme['frame_background_color'],
            hover_color=self.theme['hover_color'],
            text_color=self.theme['text_color'],
            command=lambda: self.main_program.open_edit_recipe_frame(recipe)
        )
        self.edit_btn.pack(side="left", padx=5)

        self.load_recipe_image()

    # method for load recipe image
    def load_recipe_image(self) -> None:
        try:
            image_path = os.path.join("recipe_images", self.recipe.picture_path)
            if os.path.exists(image_path):
                self.ctk_image = ctk.CTkImage(
                    light_image=Image.open(image_path),
                    dark_image=Image.open(image_path),
                    size=(180, 120)
                )
                self.image_label.configure(image=self.ctk_image, text="")
            else:
                self.image_label.configure(
                    text=self.language['image_is_not_found_error'],
                    font=('Century Gothic', 12),
                    text_color="gray"
                )
        except Exception as e:
            print(self.language['load_image_error'] + ': ' + str(e))
            self.image_label.configure(
                text=self.language['load_image_error'],
                font=('Century Gothic', 12),
                text_color="red"
            )

    # function for create window for confirmation recipe deleting
    def confirm_delete(self) -> None:
        answer = messagebox.askyesno(
            self.language['accepting'],
            self.language['delete_recipe_accept'] + self.recipe.name,
            parent=self
        )
        if answer:
            if self.delete_recipe():
                self.destroy()
                if hasattr(self.main_program, 'user_profile_frame'):
                    self.main_program.user_profile_frame.display_recipes()
                elif hasattr(self.main_program, 'main_frame'):
                    self.main_program.main_frame.display_recipes()
            else:
                messagebox.showerror(self.language['error'], self.language['delete_recipe_error'], parent=self)

    # create request for delete recipe
    def delete_recipe(self) -> bool:
        response = send_request({
            'action': 'delete_recipe',
            'recipe_id': self.recipe.id
        })
        return response.get('status') == 'success'

# recipe card class for admin program
class AdminRecipeCard(ctk.CTkFrame):
    def __init__(self, master, recipe, main_program) -> None:
        self.theme = main_program.theme
        self.language = main_program.language
        super().__init__(
            master,
            fg_color=self.theme['background_color'],
            corner_radius=10,
            border_width=2,
            border_color=self.theme['hover_color'],
            width=1230,
            height=150
        )
        self.main_program = main_program
        self.recipe = recipe
        self.ctk_image = None

        self.name_label = ctk.CTkLabel(
            master=self,
            text=recipe.name,
            font=("Arial", 14, "bold"),
            wraplength=180,
            text_color=self.theme['text_color'],
            height=40
        )
        self.name_label.place(relx=0.5, rely=0.15, anchor=ctk.CENTER)

        if not recipe.confirmed:
            self.name_label.configure(text_color="red")

        self.image_label = ctk.CTkLabel(
            self,
            text="",
            width=180,
            height=120,
            fg_color="transparent",
            corner_radius=8
        )
        self.image_label.place(relx=0.01, rely=0.5, anchor='w')

        short_desc = (recipe.description[:100] + "...") if len(
            recipe.description) > 100 else recipe.description
        self.desc_label = ctk.CTkLabel(
            self,
            text=short_desc,
            font=("Arial", 11),
            wraplength=180,
            justify="left",
            height=60,
            text_color=self.theme['text_color']
        )
        self.desc_label.place(rely=0.4, relx=0.2, anchor='w')

        self.delete_btn = ctk.CTkButton(
            master=self,
            text=self.language['delete'],
            width=120,
            height=30,
            fg_color="#db0404",
            hover_color="#910000",
            command=self.confirm_delete
        )
        self.delete_btn.place(x=1100, y=40, anchor='w')

        self.edit_btn = ctk.CTkButton(
            master=self,
            text=self.language['edit'],
            width=120,
            height=30,
            fg_color=self.theme['frame_background_color'],
            hover_color=self.theme['hover_color'],
            text_color=self.theme['text_color'],
            command=lambda: self.main_program.open_edit_recipe_frame(recipe)
        )
        self.edit_btn.place(x=1100, y=80, anchor='w')

        if not self.recipe.confirmed:
            self.edit_btn.configure(
                text=self.language['confirm'],
                fg_color="#17ad03",
                hover_color="#0c5c02",
            )

        self.load_recipe_image()

    # method for load recipe image
    def load_recipe_image(self) -> None:
        try:
            image_path = os.path.join("recipe_images", self.recipe.picture_path)
            if os.path.exists(image_path):
                self.ctk_image = ctk.CTkImage(
                    light_image=Image.open(image_path),
                    dark_image=Image.open(image_path),
                    size=(180, 120)
                )
                self.image_label.configure(image=self.ctk_image, text="")
            else:
                self.image_label.configure(
                    text=self.language['image_is_not_found_error'],
                    font=('Century Gothic', 12),
                    text_color="gray"
                )
        except Exception as e:
            self.image_label.configure(
                text=self.language['load_image_error'] + str(e),
                font=('Century Gothic', 12),
                text_color="red"
            )

    # method for confirm recipe delete
    def confirm_delete(self) -> None:
        answer = messagebox.askyesno(
            self.language['accepting'],
            self.language['delete_recipe_accept'] + self.recipe.name,
            parent=self
        )
        if answer:
            if delete_recipe(self.recipe):
                self.destroy()
                if hasattr(self.main_program, 'user_profile_frame'):
                    self.main_program.user_profile_frame.display_recipes()
                elif hasattr(self.main_program, 'main_frame'):
                    self.main_program.main_frame.display_recipes()
            else:
                messagebox.showerror(self.lanugage['error'], self.language['delete_recipe_error'], parent=self)

    def delete_recipe(self) -> None:
        try:
            db, cursor = get_database_connection()
            recipe_id = self.recipe.id
            cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
            db.commit()
            if hasattr(self, 'ctk_image'):
                self.image_label.configure(image=None)
                del self.ctk_image
            image_path = os.path.join("recipe_images", self.recipe.picture_path)
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except PermissionError:
                    import time
                    time.sleep(0.5)
                    try:
                        os.remove(image_path)
                    except Exception as e:
                        print(str(e))
            messagebox.showinfo(self.language['success'], self.language['recipe_delete_successful'], parent=self)
        except Exception as e:
            messagebox.showerror(self.language['error'], self.language['delete_recipe_error'] + ' : ' + str(e), parent=self)
        finally:
            close_database_connection(db)
            self.main_program.main_frame.display_recipes()

# class for user card
class UserCard(ctk.CTkFrame):
    def __init__(self, master, user: User, main_program) -> None:
        self.theme = main_program.theme
        self.language = main_program.language
        super().__init__(
            master,
            fg_color=self.theme['background_color'],
            corner_radius=10,
            border_width=2,
            border_color=self.theme['hover_color'],
            width=1230,
            height=60
        )
        self.user = user
        self.main_program = main_program

        self.username_label = ctk.CTkLabel(
            master=self,
            text=user.username,
            text_color="green",
            font=("Century Gothic", 14, "bold"),
        )
        self.username_label.place(rely=0.5, relx=0.02, anchor="w")

        if not user.authorized:
            self.username_label.configure(text_color="red")
        if user.admin:
            self.username_label.configure(text_color="blue")
        if self.main_program.user.username == user.username:
            self.username_label.configure(text_color="#03fccf")

        self.delete_user_button = ctk.CTkButton(
            master=self,
            text=self.language['delete'],
            corner_radius=6,
            width=100,
            fg_color="#db0404",
            hover_color="#910000",
            command=self.confirm_user_delete
        )
        self.delete_user_button.place(rely=0.5, relx=0.9, anchor="w")

        if not user.authorized:
            self.accept_user_button = ctk.CTkButton(
                master=self,
                text=self.language['accept'],
                corner_radius=6,
                width=100,
                fg_color="#17ad03",
                hover_color="#0c5c02",
                command=self.confirm_user_confirm
            )
            self.accept_user_button.place(rely=0.5, relx=0.8, anchor="w")

        if not user.admin:
            self.set_admin_button = ctk.CTkButton(
                master=self,
                text=self.language['grant_admin_privileges'],
                corner_radius=6,
                width=200,
                command=self.confirm_user_admin
            )
            self.set_admin_button.place(rely=0.5, relx=0.6, anchor="w")

    # method for confirm user status
    def confirm_user_confirm(self) -> None:
        answer = messagebox.askyesno(
            self.language['verification_confirmation'],
            self.language['accept_verification'],
            parent=self
        )
        if answer:
            accept_user(self.user)
            self.main_program.main_frame.display_users()

    # method for grant admin privileges
    def confirm_user_admin(self) -> None:
        answer = messagebox.askyesno(
            self.language['accepting'],
            self.language['admin_confirmation'],
        )
        if answer:
            grant_admin_privileges(self.user)
            self.main_program.main_frame.display_users()

    # method for create confirm user window
    def confirm_user_delete(self) -> None:
        answer = messagebox.askyesno(
            self.language['accepting'],
            self.language['user_deleting_confirmation'],
            parent=self
        )
        if answer:
            delete_user(self.user)
            self.main_program.main_frame.display_users()