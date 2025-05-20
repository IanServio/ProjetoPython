import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

caminho_arquivo = os.path.join(os.path.dirname(__file__), "data.json")

try:
    df = pd.read_json(caminho_arquivo)
except Exception as e:
    df = pd.DataFrame()
    print("Erro ao carregar data.json:", e)

root = tk.Tk()
root.title("Sistema de Tarefas")
root.configure(background="#f4f4f4")
root.minsize(400, 400)
root.maxsize(800, 800)
root.geometry("600x600+700+300")

def handleLogin():
    login = input_login.get()
    senha = input_senha.get()

    # Verifica se há correspondência no DataFrame
    usuario_encontrado = df[(df['login'] == login) & (df['senha'] == senha)]

    if not usuario_encontrado.empty:
        messagebox.showinfo("Sucesso", "Usuário logado com sucesso!")
        print(f"✅ Login bem-sucedido para: {login}")
    else:
        messagebox.showerror("Erro", "Login ou senha incorretos.")
        print("❌ Tentativa de login com credenciais inválidas.")

frame = tk.Frame(root, bg="white", bd=2, relief=tk.GROOVE)
frame.pack(pady=20, padx=40)

txt_login = tk.Label(frame, text="Login", background="white", font=("Arial", 11))
txt_login.pack(pady=(20, 5), padx=10)
input_login = tk.Entry(frame, width=30, font=("Arial", 11))
input_login.pack(pady=5, padx=10)

txt_senha = tk.Label(frame, text="Senha", background="white", font=("Arial", 11))
txt_senha.pack(pady=(15, 5), padx=10)
input_senha = tk.Entry(frame, show="*", width=30, font=("Arial", 11))
input_senha.pack(pady=5, padx=10)

btn_acessar = tk.Button(frame, text="Acessar", command=handleLogin, bg="#4CAF50", fg="white", width=20, font=("Arial", 10))
btn_acessar.pack(pady=(20, 10))

btn_sair = tk.Button(frame, text="Sair", command=root.destroy, bg="#f44336", fg="white", width=20, font=("Arial", 10))
btn_sair.pack(pady=(0, 20))

root.mainloop()
