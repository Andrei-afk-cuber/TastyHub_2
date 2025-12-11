import customtkinter as ctk

from app.windows.admin.admin_frames import MainFrame
from app.classes import User
from app.windows.user.user_frames import AddRecipeFrame
from app.config import ICON_PATH, day_theme

# Main app window
class MainApp(ctk.CTk):
    def __init__(self, language: dict, user=User(4, 'admin', '0000'), theme: dict =day_theme) -> None:
        super().__init__()
        self.user = user
        self.theme = theme
        self.language = language

        self.geometry(f"1280x720+100+100")
        self.title(f"TastyHub {self.language['administrator']}")
        self.iconbitmap(ICON_PATH)
        self.resizable(False, False)
        self.configure(fg_color=theme['frame_background_color'])

        # Create main frame
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill="both", expand=True)
        self.frames = {}

    # Open main frame
    def open_main_frame(self) -> None:
        self.destroy_all_frames()
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill="both", expand=True)

    # Method for open edit recipe frame
    def open_edit_recipe_frame(self, recipe):
        # Close main frame
        self.main_frame.destroy()
        # Open add recipe frame
        self.edit_recipe_frame = AddRecipeFrame(self, recipe, admin=True)
        self.frames['edit_recipe_frame'] = self.edit_recipe_frame
        self.edit_recipe_frame.pack(fill="both", expand=True)

    # Method for delete all frames
    def destroy_all_frames(self) -> None:
        for frame_name, frame in self.frames.items():
            frame.destroy()
        self.frames = {}