import re
import customtkinter as ctk
from tkinter import messagebox
from app.windows.login.config import theme


class SetIpWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("300x300")
        self.title("Настройки подключения")
        self.setup_window()

    def setup_window(self):
        # Заголовок
        ctk.CTkLabel(
            master=self,
            text="Введите хост и порт для подключения",
            font=('Century Gothic', 16),
            justify="center"
        ).place(relx=0.5, rely=0.1, anchor="center")

        # Поле для хоста
        self.host_entry = ctk.CTkEntry(
            master=self,
            placeholder_text="192.168.0.1",
            width=180,
        )
        self.host_entry.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

        # Поле для порта
        self.port_entry = ctk.CTkEntry(
            master=self,
            placeholder_text="65432",
            width=180
        )
        self.port_entry.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)

        # Кнопка
        self.send_button = ctk.CTkButton(
            master=self,
            text="Подключиться",
            fg_color=theme['fg_color'],
            hover_color=theme['hover_color'],
            corner_radius=6,
            font=('Century Gothic', 14),
            command=self.on_send_click
        )
        self.send_button.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

        # Кнопка отмены
        self.cancel_button = ctk.CTkButton(
            master=self,
            text="Отмена",
            fg_color="#db0404",
            hover_color="#910000",
            corner_radius=6,
            font=('Century Gothic', 12),
            command=self.destroy
        )
        self.cancel_button.place(relx=0.5, rely=0.85, anchor=ctk.CENTER)

    def on_send_click(self):
        """Обработчик нажатия кнопки подключения"""
        result = self.send_ip()
        if result:
            print(f"Установлены параметры: {result[0]}:{result[1]}")

    def send_ip(self):
        """Получает и проверяет введенные данные"""
        try:
            host = str(self.host_entry.get()).strip()
            port = int(self.port_entry.get())

            # Проверка порта
            if not (0 < port <= 65535):
                raise ValueError("Порт должен быть от 1 до 65535")

            # Базовая проверка IP
            if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', host):
                raise ValueError("Неверный формат IP-адреса")

            parts = host.split('.')
            if not all(0 <= int(part) <= 255 for part in parts):
                raise ValueError("Каждая часть IP должна быть от 0 до 255")

            self.destroy()
            return (host, port)

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
            return None
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неизвестная ошибка: {str(e)}")
            return None