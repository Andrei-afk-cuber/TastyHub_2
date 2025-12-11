import customtkinter as ctk
from customtkinter import CTkLabel
from app.functions import load_users, load_recipes, AdminRecipeCard, UserCard

# Main frame
class MainFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master
        self.theme = master.theme
        self.language = master.language
        self.configure(fg_color=self.theme['frame_background_color'])

        # Load users and recipe from database
        self.users = None
        self.recipes = None

        self.setup_main_frame()

    # Method for set up main frame
    def setup_main_frame(self) -> None:
        self.main_frame = ctk.CTkFrame(master=self, width=1270, height=50, fg_color=self.theme['background_color'])
        self.main_frame.place(relx=0.5, rely=0.05, anchor=ctk.CENTER)

        # top text
        self.text = CTkLabel(
            master=self.main_frame,
            text=self.master.user.username,
            font=('Times New Roman', 12)
        )
        self.text.place(x=90, y=45)

        # exit button
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

        # User check button
        self.users_check_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            text=self.language['users'],
            corner_radius=6,
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.display_users
        )
        self.users_check_button.place(relx=0.4, y=10)

        # Recipes check button
        self.recipes_check_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            text=self.language['posts'],
            fg_color=self.theme['frame_background_color'],
            text_color=self.theme['text_color'],
            hover_color=self.theme['hover_color'],
            command=self.display_recipes
        )
        self.recipes_check_button.place(relx=0.5, y=10)

        # Data container for recipes view
        self.data_container = ctk.CTkScrollableFrame(
            master=self,
            width=1250,
            height=600,
            fg_color="transparent",
        )
        self.data_container.place(relx=0.5, rely=0.55, anchor=ctk.CENTER)

    # Method for close program
    def close_program(self) -> None:
        self.master.destroy()

    # Method for display users
    def display_users(self) -> None:
        self.users = load_users()

        for widget in self.data_container.winfo_children():
            widget.destroy()

        for i, user in enumerate(self.users):
            card = UserCard(
                master=self.data_container,
                user=user,
                main_program=self.master
            )
            card.grid(row=i, column=0, padx=10, pady=5, sticky="ew")

    # Method for show recipes
    def display_recipes(self) -> None:
        self.recipes = load_recipes(only_confirmed=False)

        for widget in self.data_container.winfo_children():
            widget.destroy()

        if self.recipes:
            for i, recipe in enumerate(self.recipes):
                card = AdminRecipeCard(
                    master=self.data_container,
                    recipe=recipe,
                    main_program=self.master
                )
                card.grid(pady=5, padx=5, sticky="ew")