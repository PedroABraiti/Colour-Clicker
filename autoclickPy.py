from pynput.mouse import Button, Controller, Listener
import time
import threading

# Controlador do mouse
mouse = Controller()

# Variável para controlar o autoclick
autoclick_active = False

# Função para realizar o autoclick
def autoclick():
    while autoclick_active:
        mouse.click(Button.right)
        time.sleep(0.4)  # Intervalo entre os cliques, em segundos

# Função que será chamada ao pressionar um botão do mouse
def on_click(x, y, button, pressed):
    global autoclick_active
    if button == Button.right:
        if pressed:
            autoclick_active = True
            # Inicia a thread do autoclick
            threading.Thread(target=autoclick).start()
        elif not pressed:
            autoclick_active = False

# Configura o Listener para monitorar os eventos do mouse
with Listener(on_click=on_click) as listener:
    listener.join()
