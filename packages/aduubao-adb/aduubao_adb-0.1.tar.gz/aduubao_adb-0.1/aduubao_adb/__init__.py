import os
import subprocess
import tkinter as tk
import sys

def audio_play(caminho_audio):
    if os.name == 'nt':
        os.startfile(caminho_audio)
    elif os.name == 'posix':
        try:
            subprocess.run(['xdg-open', caminho_audio])
        except Exception:
            subprocess.run(['open', caminho_audio])
    else:
        raise OSError("Sistema operacional não suportado para reprodução de áudio")

def text(texto):
    print(texto)

def window(titulo, texto):
    root = tk.Tk()
    root.title(titulo)
    label = tk.Label(root, text=texto, padx=20, pady=20)
    label.pack()
    root.mainloop()

def arquivo(nome_arquivo, conteudo):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)

def pause():
    print("Pressione qualquer tecla para continuar...")
    try:
        import msvcrt
        msvcrt.getch()
    except ImportError:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
