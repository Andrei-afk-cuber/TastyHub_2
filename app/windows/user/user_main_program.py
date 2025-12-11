# libraries
import customtkinter as ctk

# user libraries
from app.windows.user.user_frames import MainFrame, AddRecipeFrame, ShowRecipeFrame, UserProfileFrame
from app.classes import User
from app.config import ICON_PATH, day_theme

# Main app window
class MainApp(ctk.CTk):
    def __init__(self, language: dict, user=User(0, 'developer', 0000), theme: dict =day_theme) -> None:
        super().__init__()
        self.user = user
        self.theme = theme
        self.language = language

        self.configure(fg_color=self.theme['frame_background_color'])

        self.geometry(f"1280x720+100+100")   # Standard size 600x400
        self.title("TastyHub")
        self.iconbitmap(ICON_PATH)
        self.resizable(width=False, height=False)
        # Create the main frame
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill="both", expand=True)
        self.frames = {}

    # Open main frame
    def open_main_frame(self) -> None:
        self.destroy_all_frames()
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill="both", expand=True)

    # Method for open add recipe frame
    def open_add_recipe_frame(self) -> None:
        self.main_frame.destroy()
        self.add_recipe_frame = AddRecipeFrame(self)
        self.frames['add_recipe_frame'] = self.add_recipe_frame
        self.add_recipe_frame.pack(fill="both", expand=True)

    # Method for open show recipe frame
    def open_show_recipe_frame(self, recipe) -> None:
        self.main_frame.destroy()
        # Открываем фрейм просмотра рецепта
        self.show_recipe_frame = ShowRecipeFrame(self, recipe)
        self.frames['show_recipe_frame'] = self.show_recipe_frame
        self.show_recipe_frame.pack(fill="both", expand=True)

    # Method for open uper profile frame
    def open_user_profile_frame(self) -> None:
        self.main_frame.destroy()
        self.user_profile_frame = UserProfileFrame(self)
        self.frames['user_profile_frame'] = self.user_profile_frame
        self.user_profile_frame.pack(fill="both", expand=True)

    # Method for open edit recipe frame
    def open_edit_recipe_frame(self, recipe) -> None:
        self.user_profile_frame.destroy()
        self.edit_recipe_frame = AddRecipeFrame(self, recipe)
        self.frames['edit_recipe_frame'] = self.edit_recipe_frame
        self.edit_recipe_frame.pack(fill="both", expand=True)

    # Method for destroy all frames
    def destroy_all_frames(self) -> None:
        for frame_name, frame in self.frames.items():
            frame.destroy()
        self.frames = {}