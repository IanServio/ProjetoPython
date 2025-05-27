import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

caminho_arquivo = os.path.join(os.path.dirname(__file__), "data.json")

def garantir_tarefa(df):
    if 'tarefa' not in df.columns:
        df['tarefa'] = [[] for _ in range(len(df))]
    else:
        for i in range(len(df)):
            if isinstance(df.at[i, 'tarefa'], float) or df.at[i, 'tarefa'] is None:
                df.at[i, 'tarefa'] = []
    return df

def carregar_df():
    try:
        if os.path.exists(caminho_arquivo) and os.path.getsize(caminho_arquivo) > 0:
            df = pd.read_json(caminho_arquivo)
            df = garantir_tarefa(df)
        else:
            df = pd.DataFrame(columns=["login", "senha", "email", "numero", "tarefa"])
    except Exception as e:
        print("Erro ao carregar data.json:", e)
        df = pd.DataFrame(columns=["login", "senha", "email", "numero", "tarefa"])
    return df

df = carregar_df()

root = tk.Tk()
root.title("Sistema de Tarefas")
root.configure(background="#181818")
root.minsize(400, 400)
root.maxsize(800, 800)
root.geometry("600x600+700+300")

def handleLogin():
    global df
    df = carregar_df()
    login = input_login.get()
    senha = input_senha.get()
    usuario_encontrado = df[(df['login'] == login) & (df['senha'] == senha)]
    if not usuario_encontrado.empty:
        messagebox.showinfo("Sucesso", "Usuário logado com sucesso!")
        telaPrincipal(login)
    else:
        messagebox.showerror("Erro", "Login ou senha incorretos.")
        print("Tentativa de login com credenciais inválidas.")

def telaPrincipal(usuario_login):
    global df
    root.destroy()
    janela_principal = tk.Tk()
    janela_principal.title("Minhas tarefas")
    janela_principal.geometry("600x600+700+300")
    janela_principal.configure(background="#181818")

    label_usuario = tk.Label(janela_principal, text=f"Usuário: {usuario_login}", font=("Arial", 12), bg="#181818", fg="white")
    label_usuario.pack(pady=10)

    titulo = tk.Label(janela_principal, text="Tarefas", bg="#181818", fg="white", font=("Arial", 14, "bold"))
    titulo.pack(pady=5, padx=10)

    frame = tk.Frame(janela_principal, bg="#222222", bd=2, relief=tk.GROOVE)
    frame.pack(pady=40, padx=40)

    label_nova_tarefa = tk.Label(frame, text="Nova tarefa:", background="#222222", font=("Arial", 11), fg="white")
    label_nova_tarefa.pack(pady=(10, 5), padx=10)

    entry_tarefa = tk.Entry(frame, width=40, font=("Arial", 11), bg="#333333", fg="white", insertbackground="white")
    entry_tarefa.pack(pady=5, padx=10)

    frame_tarefas = tk.Frame(janela_principal, bg="#181818")
    frame_tarefas.pack(pady=10)

    def atualizar_lista():
        for widget in frame_tarefas.winfo_children():
            widget.destroy()
        df_local = carregar_df()
        idxs = df_local[df_local['login'] == usuario_login].index
        if len(idxs) > 0:
            idx = idxs[0]
            tarefas = df_local.at[idx, 'tarefa']
            if isinstance(tarefas, list):
                for i, t in enumerate(tarefas):
                    tarefa_frame = tk.Frame(frame_tarefas, bg="#181818")
                    tarefa_frame.pack(fill="x", pady=2)
                    lbl = tk.Label(tarefa_frame, text=t, bg="#181818", fg="white", anchor="w", width=40, font=("Arial", 11))
                    lbl.pack(side="left", padx=5)
                    btn_excluir = tk.Button(
                        tarefa_frame,
                        text="Excluir",
                        bg="#f44336",
                        fg="white",
                        font=("Arial", 9),
                        relief="flat",
                        borderwidth=0,
                        highlightthickness=0,
                        activebackground="#d32f2f",
                        activeforeground="white",
                        command=lambda idx_tarefa=i: excluir_tarefa(idx_tarefa)
                    )
                    btn_excluir.pack(side="right", padx=5, ipadx=10, ipady=2)

    def adicionar_tarefa():
        global df
        tarefa = entry_tarefa.get()
        if tarefa:
            df = carregar_df()
            idxs = df[df['login'] == usuario_login].index
            if len(idxs) > 0:
                idx = idxs[0]
                if 'tarefa' not in df.columns or df.at[idx, 'tarefa'] is None:
                    df.at[idx, 'tarefa'] = []
                tarefas = df.at[idx, 'tarefa']
                if not isinstance(tarefas, list):
                    tarefas = []
                tarefas.append(tarefa)
                df.at[idx, 'tarefa'] = tarefas
                df.to_json(caminho_arquivo, orient="records", indent=4, force_ascii=False)
                entry_tarefa.delete(0, tk.END)
                atualizar_lista()
                messagebox.showinfo("Adicionar Tarefa", f"Tarefa adicionada: {tarefa}")
            else:
                messagebox.showerror("Erro", "Usuário não encontrado.")
        else:
            messagebox.showwarning("Aviso", "Digite uma tarefa antes de adicionar.")

    def excluir_tarefa(idx_tarefa):
        global df
        df = carregar_df()
        idxs = df[df['login'] == usuario_login].index
        if len(idxs) > 0:
            idx = idxs[0]
            tarefas = df.at[idx, 'tarefa']
            if isinstance(tarefas, list) and 0 <= idx_tarefa < len(tarefas):
                del tarefas[idx_tarefa]
                df.at[idx, 'tarefa'] = tarefas
                df.to_json(caminho_arquivo, orient="records", indent=4, force_ascii=False)
                atualizar_lista()
                messagebox.showinfo("Excluir Tarefa", "Tarefa excluída com sucesso.")

    btn_adicionar = tk.Button(
        frame, text="Adicionar Tarefa", command=adicionar_tarefa,
        bg="#4CAF50", fg="white", width=20, font=("Arial", 10, "bold"),
        relief="flat", borderwidth=0, highlightthickness=0, activebackground="#388e3c", activeforeground="white"
    )
    btn_adicionar.pack(pady=(10, 5), ipadx=10, ipady=4)

    atualizar_lista()
    janela_principal.mainloop()

def handleCadastrar():
    def salvarCadastro():
        global df
        df = carregar_df()
        login = input_login_cad.get()
        senha = input_senha_cad.get()
        email = input_email.get()
        numero = input_numero.get()
        if not login or not senha or not email or not numero:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
        if not df[df['login'] == login].empty:
            messagebox.showerror("Erro", "Login já existe.")
            return
        novo_usuario = {
            "login": login,
            "senha": senha,
            "email": email,
            "numero": numero,
            "tarefa": []
        }
        df = pd.concat([df, pd.DataFrame([novo_usuario])], ignore_index=True)
        df = garantir_tarefa(df)
        df.to_json(caminho_arquivo, orient="records", indent=4, force_ascii=False)
        messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
        janela_cadastro.destroy()
        root.deiconify()

    janela_cadastro = tk.Toplevel(root)
    janela_cadastro.geometry("600x600+700+300")
    janela_cadastro.title("Cadastro de usuario")
    janela_cadastro.configure(background="#181818")

    titulo = tk.Label(janela_cadastro, text="Cadastre-se", bg="#181818", fg="white", font=("Arial", 14, "bold"))
    titulo.pack(pady=5, padx=10)

    frame = tk.Frame(janela_cadastro, bg="#222222", bd=2, relief=tk.GROOVE)
    frame.pack(pady=40, padx=40)

    txt_login = tk.Label(frame, text="Login", background="#222222", font=("Arial", 11), fg="white")
    txt_login.pack(pady=(20, 5), padx=10)
    input_login_cad = tk.Entry(frame, width=30, font=("Arial", 11), bg="#333333", fg="white", insertbackground="white")
    input_login_cad.pack(pady=5, padx=10)

    txt_senha = tk.Label(frame, text="Senha", background="#222222", font=("Arial", 11), fg="white")
    txt_senha.pack(pady=(15, 5), padx=10)
    input_senha_cad = tk.Entry(frame, width=30, font=("Arial", 11), bg="#333333", fg="white", insertbackground="white")
    input_senha_cad.pack(pady=5, padx=10)

    txt_email = tk.Label(frame, text="Email", background="#222222", font=("Arial", 11), fg="white")
    txt_email.pack(pady=(20, 5), padx=10)
    input_email = tk.Entry(frame, width=30, font=("Arial", 11), bg="#333333", fg="white", insertbackground="white")
    input_email.pack(pady=5, padx=10)

    txt_numero = tk.Label(frame, text="Numero", background="#222222", font=("Arial", 11), fg="white")
    txt_numero.pack(pady=(20, 5), padx=10)
    input_numero = tk.Entry(frame, width=30, font=("Arial", 11), bg="#333333", fg="white", insertbackground="white")
    input_numero.pack(pady=5, padx=10)

    btn_cadastrar = tk.Button(
        frame, text="Cadastrar", command=salvarCadastro,
        bg="#4CAF50", fg="white", width=20, font=("Arial", 10, "bold"),
        relief="flat", borderwidth=0, highlightthickness=0, activebackground="#388e3c", activeforeground="white"
    )
    btn_cadastrar.pack(pady=(20, 10), ipadx=10, ipady=4)

    def voltar_para_login():
        janela_cadastro.destroy()
        root.deiconify()

    btn_voltar = tk.Button(
        frame, text="Voltar", command=voltar_para_login,
        bg="#4aa4fe", fg="white", width=20, font=("Arial", 10, "bold"),
        relief="flat", borderwidth=0, highlightthickness=0, activebackground="#1976d2", activeforeground="white"
    )
    btn_voltar.pack(pady=(0, 10), ipadx=10, ipady=4)

titulo_signin = tk.Label(root, text="Sign In", bg="#181818", fg="white", font=("Arial", 20, "bold"))
titulo_signin.pack(pady=(30, 0))

frame = tk.Frame(root, bg="#222222", bd=2, relief=tk.GROOVE)
frame.pack(pady=50, padx=40)

txt_login = tk.Label(frame, text="Login", background="#222222", font=("Arial", 11), fg="white")
txt_login.pack(pady=(20, 5), padx=10)
input_login = tk.Entry(frame, width=30, font=("Arial", 11), bg="#333333", fg="white", insertbackground="white")
input_login.pack(pady=5, padx=10)

txt_senha = tk.Label(frame, text="Senha", background="#222222", font=("Arial", 11), fg="white")
txt_senha.pack(pady=(15, 5), padx=10)
input_senha = tk.Entry(frame, show="*", width=30, font=("Arial", 11), bg="#333333", fg="white", insertbackground="white")
input_senha.pack(pady=5, padx=10)

btn_acessar = tk.Button(
    frame, text="Acessar", command=handleLogin,
    bg="#4CAF50", fg="white", width=20, font=("Arial", 10, "bold"),
    relief="flat", borderwidth=0, highlightthickness=0, activebackground="#388e3c", activeforeground="white"
)
btn_acessar.pack(pady=(20, 10), ipadx=10, ipady=4)

btn_cadastrar = tk.Button(
    frame, text="Cadastrar-se", command=handleCadastrar,
    bg="#4aa4fe", fg="white", width=20, font=("Arial", 10, "bold"),
    relief="flat", borderwidth=0, highlightthickness=0, activebackground="#1976d2", activeforeground="white"
)
btn_cadastrar.pack(pady=(20, 10), ipadx=10, ipady=4)

btn_sair = tk.Button(
    frame, text="Sair", command=root.destroy,
    bg="#f44336", fg="white", width=20, font=("Arial", 10, "bold"),
    relief="flat", borderwidth=0, highlightthickness=0, activebackground="#d32f2f", activeforeground="white"
)
btn_sair.pack(pady=(0, 20), ipadx=10, ipady=4)

root.mainloop()