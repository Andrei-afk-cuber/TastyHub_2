# importing libraries
import customtkinter as tk

# importing user modules
from app.windows.login.frames import MainFrame, RegistrationFrame, AboutFrame
from app.config import ICON_PATH, day_theme
from app.functions import json_to_dict

# Main app window
class LoginMainApp(tk.CTk):
    def __init__(self, user_program_class, admin_program_class) -> None:
        super().__init__()
        self.theme = day_theme
        self.language = json_to_dict("app/locales/russian.json")

        self.user_program_class = user_program_class
        self.admin_program_class = admin_program_class

        self.configure(fg_color=self.theme['background_color'])

        self.geometry(f"600x400+550+250")
        self.title(self.language['authorization'])
        self.iconbitmap(ICON_PATH)
        # Create the main frame
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill="both", expand=True)
        self.frames = {}

    # Change title method
    def change_title(self, new_title: str) -> None:
        self.title(new_title)

    # Open register frame method
    def open_register_frame(self) -> None:
        self.main_frame.destroy()
        self.register_frame = RegistrationFrame(self)
        self.frames['register_frame'] = self.register_frame
        self.register_frame.pack(expand=True, fill="both")

    # Open main frame
    def open_main_frame(self) -> None:
        self.destroy_all_frames()
        self.change_title(self.language['authorization'])
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill="both", expand=True)

    # Open about frame
    def open_about_frame(self) -> None:
        self.main_frame.destroy()
        self.about_frame = AboutFrame(self)
        self.frames['about_frame'] = self.about_frame
        self.about_frame.pack(expand=True, fill="both")

    def open_main_program(self, user) -> None:
        self.destroy()
        if user.admin():
            self.main_program = self.admin_program_class(self.language ,user, self.theme)
        else:
            self.main_program = self.user_program_class(self.language, user, self.theme)

        self.main_program.mainloop()

    # function for delete all frames
    def destroy_all_frames(self) -> None:
        for frame_name, frame in self.frames.items():
            frame.destroy()
        self.frames = {}
