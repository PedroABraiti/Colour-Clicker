import pyautogui
import time
from pynput import keyboard
import tkinter as tk
from tkinter import simpledialog

# Variáveis globais para armazenar as cores detectadas e a cor alvo
detected_colors = set()
target_color = None
clicking = False

def on_press(key):
    global detected_colors, target_color, clicking

    try:
        if key.char == 'c':
            x, y = pyautogui.position()
            detected_colors = capture_colors_around_mouse(x, y)
            print(f"Cores detectadas: {detected_colors}")
            target_color = choose_color()
            print(f"Cor alvo escolhida: {target_color}")
            clicking = True

    except AttributeError:
        pass

def capture_colors_around_mouse(x, y, area_size=5):
    colors = set()
    region = pyautogui.screenshot(region=(x - area_size, y - area_size, 2 * area_size + 1, 2 * area_size + 1))
    for i in range(region.width):
        for j in range(region.height):
            colors.add(region.getpixel((i, j)))
    return colors

def choose_color():
    color_list = list(detected_colors)
    
    root = tk.Tk()
    root.withdraw()
    
    color_str = "\n".join([f"{index}: {color}" for index, color in enumerate(color_list)])
    choice = simpledialog.askstring("Escolha de Cor", f"Escolha a cor alvo a partir das cores detectadas (formato: (r, g, b)):\n{color_str}\nDigite o número da cor alvo:")
    
    if choice is not None and choice.isdigit():
        choice = int(choice)
        if 0 <= choice < len(color_list):
            return color_list[choice]
    return None

def is_color_similar(color1, color2, tolerance=10):
    return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color1, color2))

def is_color_in_area(target_color, x, y, area_size=5):
    region = pyautogui.screenshot(region=(x - area_size, y - area_size, 2 * area_size + 1, 2 * area_size + 1))
    for i in range(region.width):
        for j in range(region.height):
            if is_color_similar(region.getpixel((i, j)), target_color):
                return True
    return False

def click_loop():
    global clicking
    while True:
        if clicking:
            x, y = pyautogui.position()
            if is_color_in_area(target_color, x, y):
                pyautogui.mouseDown()
                time.sleep(0.05)
                pyautogui.mouseUp()
                time.sleep(1.0)
            else:
                time.sleep(0.1)

listener = keyboard.Listener(on_press=on_press)
listener.start()

click_loop()
