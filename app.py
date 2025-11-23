from app.windows.user import user_main_program as ump
from app.windows.admin import admin_main_program as amp
from app.windows.login.app import LoginMainApp
# Create main program instance
user_main_program = ump.MainApp
admin_main_program = amp.MainApp

if __name__ == '__main__':
    LoginMainApp(user_main_program, admin_main_program).mainloop()