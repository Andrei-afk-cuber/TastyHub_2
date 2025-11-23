import customtkinter as ctk
from app.windows.admin.admin_frames import MainFrame
from app.classes import User
from app.windows.user.user_frames import AddRecipeFrame

# Основное окно приложения
class MainApp(ctk.CTk):
    def __init__(self, user=User("test_admin", 0000, True)):
        super().__init__()

        self.user = user

        self.geometry(f"1280x720+100+100")   # Standard size 600x400
        self.title("TastyHub (Администратор)")
        self.iconbitmap("images/icon.ico")
        self.resizable(False, False)

        # Создаем основное окно
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill="both", expand=True)
        self.frames = {}

    # Открываем основной фрейм
    def open_main_frame(self):
        self.destroy_all_frames()
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill="both", expand=True)

    # Метод открытия фрейма для редактирования рецепта
    def open_edit_recipe_frame(self, recipe):
        # Закрываем фрейм профиля пользователя
        self.main_frame.destroy()
        # Открываем фрейм редактирования рецепта
        self.edit_recipe_frame = AddRecipeFrame(self, recipe, admin=True)
        self.frames['edit_recipe_frame'] = self.edit_recipe_frame
        self.edit_recipe_frame.pack(fill="both", expand=True)

    # Функция удаления всех фреймов
    def destroy_all_frames(self):
        # Удаляем все фреймы, которые есть в словаре
        for frame_name, frame in self.frames.items():
            frame.destroy()
        self.frames = {}

# Раскомментировать при запуске AdminMainProgram
# MainApp().mainloop()