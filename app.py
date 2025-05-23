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


    usuario_encontrado = df[(df['login'] == login) & (df['senha'] == senha)]

    if not usuario_encontrado.empty:
        messagebox.showinfo("Sucesso", "Usuário logado com sucesso!")
        print(f"Login bem-sucedido para: {login}")
        telaPrincipal()

    else:
        messagebox.showerror("Erro", "Login ou senha incorretos.")
        print("Tentativa de login com credenciais inválidas.")

def telaPrincipal():
    root.destroy()
    janela_principal = tk.Tk()
    janela_principal.title("Minhas tarefas")
    janela_principal.geometry("600x600+700+300")
    titulo = tk.Label(janela_principal, text=("Tarefas"))
    titulo.pack(pady=5, padx=10)
    janela_principal.mainloop()

    frame = tk.Frame(janela_principal, bg="white", bd=2, relief=tk.GROOVE)
    frame.pack(pady=40, padx=40)

    txt_tarefa = tk.Label(frame, text="Adicionar Tarefa:", background="white", font=("Arial", 11))
    txt_tarefa.pack(pady=40, padx=40)


def handleCadastrar():

    root.destroy()
    janela_cadastro = tk.Tk()
    janela_cadastro.geometry("600x600+700+300")
    janela_cadastro.title("Cadastro de usuario")
    

    frame = tk.Frame(janela_cadastro, bg="white", bd=2, relief=tk.GROOVE)
    frame.pack(pady=40, padx=40)

    titulo = tk.Label(janela_cadastro, text=("Cadastre-se"))
    titulo.pack(pady=5, padx=10)

    txt_login = tk.Label(frame, text="Login", background="white", font=("Arial", 11))
    txt_login.pack(pady=(20, 5), padx=10)
    input_login = tk.Entry(frame, width=30, font=("Arial", 11))
    input_login.pack(pady=5, padx=10)

    txt_senha = tk.Label(frame, text="Senha", background="white", font=("Arial", 11))
    txt_senha.pack(pady=(15, 5), padx=10)
    input_senha = tk.Entry(frame, width=30, font=("Arial", 11))
    input_senha.pack(pady=5, padx=10)

    txt_email = tk.Label(frame, text="Email", background="white", font=("Arial", 11))
    txt_email.pack(pady=(20, 5), padx=10)
    input_email = tk.Entry(frame, width=30, font=("Arial", 11))
    input_email.pack(pady=5, padx=10)

    txt_numero = tk.Label(frame, text="Numero", background="white", font=("Arial", 11))
    txt_numero.pack(pady=(20, 5), padx=10)
    input_numero = tk.Entry(frame, width=30, font=("Arial", 11))
    input_numero.pack(pady=5, padx=10)

    
    def salvarCadastro():
        login = input_login.get()
        senha = input_senha.get()
        email = input_email.get()
        numero = input_numero.get()

        
        global df
        novo_usuario = {"login": login, "senha": senha, "email": email, "numero": numero}

        if not login or not senha or not email or not numero:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
        
        df = pd.concat([df, pd.DataFrame([novo_usuario])], ignore_index=True)

        
        df.to_json(caminho_arquivo, orient="records", indent=4, force_ascii=False)

        messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
        janela_cadastro.destroy()

    btn_cadastrar = tk.Button(frame, text="Cadastrar", command=salvarCadastro, bg="#4CAF50", fg="white", width=20, font=("Arial", 10))
    btn_cadastrar.pack(pady=(20, 10))

    janela_cadastro.pack()



frame = tk.Frame(root, bg="white", bd=2, relief=tk.GROOVE)
frame.pack(pady=50, padx=40)

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


btn_cadastrar = tk.Button(frame, text="Cadastrar-se", command=handleCadastrar, bg="#4aa4fe", fg="white", width=20, font=("Arial", 10))
btn_cadastrar.pack(pady=(20, 10))


btn_sair = tk.Button(frame, text="Sair", command=root.destroy, bg="#f44336", fg="white", width=20, font=("Arial", 10))
btn_sair.pack(pady=(0, 20))

root.mainloop()
