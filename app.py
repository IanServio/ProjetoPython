import tkinter as tk
from tkinter import messagebox

root = tk.Tk()

root.title("Sistema de Tarefas")
root.configure(background="#f4f4f4")
root.minsize(400, 400)
root.maxsize(800, 800)
root.geometry("600x600+700+300")

def handleLogin():
    messagebox.showinfo("Info", "Usuário Logado")



image = tk.PhotoImage(file="book.gif").subsample(5, 5)
img_label = tk.Label(root, image=image, bg="#f4f4f4")
img_label.pack(pady=10)



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
