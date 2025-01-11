import tkinter as tk
from tkinter import messagebox
import time

class Dollar:
    def __init__(self, amount):
        self.amount = amount

    def __str__(self):
        return f"${self.amount:.2f}"

    def spend(self, price):
        if self.amount >= price:
            self.amount -= price
            return True
        return False

def update_balance():
    balance_label.config(text=f"Баланс: {user_money}")

def buy_hat():
    if user_money.spend(10):
        messagebox.showinfo("Покупка успешна", "Вы купили шапку за 10 долларов!")
        update_balance()
    else:
        messagebox.showerror("Ошибка", "У вас недостаточно денег для покупки.")

def buy_trip_discount():
    global trip_time
    if user_money.spend(50):
        trip_time -= 1
        messagebox.showinfo("Покупка успешна", f"Вы купили поездку на минус 1 час! Новое время поездки: {trip_time} часа.")
        update_balance()
    else:
        messagebox.showerror("Ошибка", "У вас недостаточно денег для покупки.")

def open_shop():
    shop_window = tk.Toplevel(root)
    shop_window.title("Магазин")
    
    balance_label_in_shop = tk.Label(shop_window, text=f"Ваш баланс: {user_money}", font=("Arial", 14))
    balance_label_in_shop.pack(pady=10)
    
    buy_button = tk.Button(shop_window, text="Купить шапку за 10 долларов", command=buy_hat, font=("Arial", 14))
    buy_button.pack(pady=10)
    
    buy_trip_button = tk.Button(shop_window, text="Купить поездку на минус 1 час за 50 долларов", command=buy_trip_discount, font=("Arial", 14))
    buy_trip_button.pack(pady=10)

def sit_on_train():
    if user_money.spend(50):
        messagebox.showinfo("Поезд", "Вы купили билет на поезд! Через 10 секунд поездка начнется.")
        update_balance()
        start_countdown()
    else:
        messagebox.showerror("Ошибка", "У вас недостаточно денег для покупки билета.")

def start_countdown():
    timer_label.config(text="10 секунд до начала поездки!")
    countdown(10)

def countdown(seconds):
    if seconds > 0:
        timer_label.config(text=f"{seconds} секунд до начала поездки")
        root.after(1000, countdown, seconds-1)
    else:
        timer_label.config(text=f"Поездка начинается! {trip_time} часов до прибытия!")
        start_trip()

def start_trip():
    move_train()

def move_train():
    global train
    x_position = 50  # Начальная позиция поезда
    train_width = 100  # Ширина поезда
    rail_end = 550  # Конец рельс, куда поезд должен доехать

    total_steps = trip_time * 60  # Количество шагов (поезд будет двигаться в течение времени поездки)
    step_size = 2  # Размер шага (скорость движения поезда)

    sleep_time = 0.5  # Время паузы между шагами (скорость)
    if trip_time < 2:
        sleep_time = 0.25

    # Двигаем поезд по рельсам
    for _ in range(total_steps):
        if x_position + train_width < rail_end:
            canvas.move(train, step_size, 0)  # Двигаем поезд вправо
            x_position += step_size
            root.update()  # Обновляем интерфейс
            time.sleep(sleep_time)

    show_exit_button()
    global arrival_text
    arrival_text = canvas.create_text(300, 50, text="Мы приехали!", font=("Arial", 16, "bold"), fill="black")

def show_exit_button():
    exit_button.pack(pady=20)

def exit_train():
    exit_button.pack_forget()
    hide_train()
    remove_rails()
    show_camp_scene()
    show_go_to_camp_button()

def hide_train():
    canvas.delete(train)

def remove_rails():
    canvas.delete(rails)

def show_camp_scene():
    canvas.create_oval(150, 130, 180, 160, fill="green")  # Деревья
    canvas.create_oval(200, 130, 230, 160, fill="green")
    canvas.create_oval(250, 130, 280, 160, fill="green")
    canvas.create_rectangle(100, 160, 500, 190, fill="brown")  # Земля
    canvas.create_text(300, 100, text="Вы приехали в школьный лагерь!", font=("Arial", 16, "bold"), fill="black")

def show_go_to_camp_button():
    go_to_camp_button.pack(pady=20)

def go_to_camp():
    go_to_camp_button.pack_forget()
    messagebox.showinfo("Школьный лагерь", "Вы идете к лагерю!")
    countdown_to_camp(5)

def countdown_to_camp(seconds):
    if seconds > 0:
        camp_timer_label.config(text=f"Идете к лагерю... {seconds} секунд осталось.")
        root.after(1000, countdown_to_camp, seconds-1)
    else:
        camp_timer_label.config(text="Вы пришли!")
        root.after(2000, show_second_message)

def show_second_message():
    camp_timer_label.config(text="Ждите 2-ую часть.")

root = tk.Tk()
root.title("Главное меню")

user_money = Dollar(150)
trip_time = 2

# Метка для отображения баланса
balance_label = tk.Label(root, text=f"Баланс: {user_money}", font=("Arial", 14))
balance_label.pack(pady=10)

# Кнопка для перехода в магазин
shop_button = tk.Button(root, text="Перейти в магазин", command=open_shop, font=("Arial", 14))
shop_button.pack(pady=20)

# Кнопка для посадки на поезд
sit_button_train = tk.Button(root, text="Купить билет на поезд (50 долларов)", command=sit_on_train, font=("Arial", 14))
sit_button_train.pack(pady=20)

# Canvas для рисования поезда и сцены лагеря
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack(pady=20)

# Рисуем рельсы на уровне 180 по вертикали
rails = canvas.create_line(50, 180, 550, 180, width=5)

# Рисуем поезд (поезд будет на уровне рельсов)
train = canvas.create_rectangle(50, 150, 150, 200, fill="blue")

# Кнопка для выхода с поезда
exit_button = tk.Button(root, text="Выйти с поезда", command=exit_train, font=("Arial", 14))

# Метка для таймера
timer_label = tk.Label(root, text="", font=("Arial", 14))
timer_label.pack(pady=20)

# Метка для таймера лагеря
camp_timer_label = tk.Label(root, text="", font=("Arial", 14))
camp_timer_label.pack(pady=20)

# Кнопка для идти к лагерю
go_to_camp_button = tk.Button(root, text="Идти к лагерю", command=go_to_camp, font=("Arial", 14))

root.mainloop()