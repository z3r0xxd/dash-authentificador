# gui.py

import customtkinter as ctk
import pyotp
import time
import tkinter.messagebox as messagebox
from main import load_data, save_data
from cryptography.fernet import Fernet

# Configurar o tema do CustomTkinter
ctk.set_appearance_mode("Dark")  # Tema escuro
ctk.set_default_color_theme("blue")  # Tema azul

class App(ctk.CTk):
    def __init__(self, accounts, key):
        super().__init__()
        self.title("Passa Bomb")
        self.geometry("900x600")
        self.key = key
        self.accounts = accounts  # Lista de contas carregadas

        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título da Seção "Adicionar Conta"
        self.add_account_title = ctk.CTkLabel(
            self.main_frame,
            text="Adicionar Nova Conta",
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        self.add_account_title.pack(fill="x", pady=(0, 10))

        # Frame para adicionar nova conta
        self.add_account_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.add_account_frame.pack(fill="x")

        # Campos para nome, email e senha
        self.name_entry = ctk.CTkEntry(self.add_account_frame, placeholder_text="Nome")
        self.name_entry.pack(fill="x", pady=5)

        self.email_entry = ctk.CTkEntry(self.add_account_frame, placeholder_text="Email")
        self.email_entry.pack(fill="x", pady=5)

        self.password_entry = ctk.CTkEntry(self.add_account_frame, placeholder_text="Senha", show="*")
        self.password_entry.pack(fill="x", pady=5)

        # Campo para a chave secreta do autenticador
        self.secret_key_entry = ctk.CTkEntry(self.add_account_frame, placeholder_text="Chave Secreta do Autenticador")
        self.secret_key_entry.pack(fill="x", pady=5)

        # Botão para adicionar conta
        self.add_button = ctk.CTkButton(
            self.add_account_frame,
            text="Adicionar Conta",
            command=self.add_account,
            fg_color="#2E8B57",  # Verde escuro
            hover_color="#228B22"  # Verde mais escuro ao passar o mouse
        )
        self.add_button.pack(fill="x", pady=10)

        # Título da Seção "Contas Salvas"
        self.saved_accounts_title = ctk.CTkLabel(
            self.main_frame,
            text="Contas Salvas",
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        self.saved_accounts_title.pack(fill="x", pady=(20, 10))

        # Frame para listar contas existentes
        self.accounts_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.accounts_frame.pack(fill="both", expand=True)

        # Adicionar o texto "All Rights Reserved by z3r0 2025" na posição desejada
        self.rights_label = ctk.CTkLabel(
            self.main_frame,
            text="Copyright © 2025 - All Rights Reserved - z3r0",
            font=("Arial", 12),
            anchor="center"
        )
        self.rights_label.pack(fill="x", pady=(10, 0))
        
        # Atualizar a lista de contas
        self.update_accounts_list()

        # Iniciar a atualização automática dos tokens
        self.update_tokens()

        # Configurar manipulador de eventos de fechamento
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_account(self):
        # Obter os valores dos campos
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        secret_key = self.secret_key_entry.get()

        if not name or not email or not password:
            messagebox.showwarning("Erro", "Preencha todos os campos obrigatórios!")
            return

        # Usar a chave secreta fornecida pelo usuário ou gerar uma nova
        totp_secret = secret_key if secret_key else pyotp.random_base32()

        # Adicionar a nova conta à lista
        self.accounts.append({
            "name": name,
            "email": email,
            "password": password,
            "totp_secret": totp_secret
        })

        # Limpar os campos
        self.name_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.secret_key_entry.delete(0, "end")

        # Atualizar a lista de contas
        self.update_accounts_list()

    def update_accounts_list(self):
        # Limpar o frame de contas
        for widget in self.accounts_frame.winfo_children():
            widget.destroy()

        # Exibir cada conta
        for account in self.accounts:
            account_frame = ctk.CTkFrame(self.accounts_frame, fg_color="#333333")  # Fundo escuro
            account_frame.pack(fill="x", pady=5)

            # Nome e Email
            info_label = ctk.CTkLabel(account_frame, text=f"{account['name']} ({account['email']})", font=("Arial", 14))
            info_label.pack(side="left", padx=10)

            # Token TOTP e Timer
            token_label = ctk.CTkLabel(account_frame, text="Carregando...", font=("Arial", 12))
            token_label.pack(side="left", padx=10)

            timer_label = ctk.CTkLabel(account_frame, text="Tempo restante: ", font=("Arial", 12))
            timer_label.pack(side="left", padx=10)

            # Botão para copiar os detalhes da conta
            copy_button = ctk.CTkButton(
                account_frame,
                text="Copiar",
                width=50,
                command=lambda acc=account: self.copy_account_details(acc),
                fg_color="#1E90FF",  # Azul claro
                hover_color="#104E8B"  # Azul mais escuro ao passar o mouse
            )
            copy_button.pack(side="right", padx=5)

            # Botão para deletar a conta
            delete_button = ctk.CTkButton(
                account_frame,
                text="Deletar",
                width=50,
                command=lambda acc=account: self.delete_account(acc),
                fg_color="red",  # Vermelho
                hover_color="darkred"  # Vermelho mais escuro ao passar o mouse
            )
            delete_button.pack(side="right", padx=5)

            # Armazenar referências temporárias para os labels de token e timer
            account["token_label"] = token_label
            account["timer_label"] = timer_label

    def update_tokens(self):
        # Atualizar o token e o tempo restante para cada conta
        for account in self.accounts:
            totp = pyotp.TOTP(account["totp_secret"])
            token = totp.now()
            time_remaining = 30 - (int(time.time()) % 30)

            # Atualizar os labels
            account["token_label"].configure(text=f"Token: {token}")
            account["timer_label"].configure(text=f"Tempo restante: {time_remaining} segundos")

        # Agendar a próxima atualização
        self.after(1000, self.update_tokens)

    def copy_account_details(self, account):
        # Gerar o texto com os detalhes da conta
        totp = pyotp.TOTP(account["totp_secret"])
        details = (
            f"Nome: {account['name']}\n"
            f"Email: {account['email']}\n"
            f"Senha: {account['password']}\n"
            f"Token: {totp.now()}"
        )

        # Copiar os detalhes para a área de transferência
        self.clipboard_clear()
        self.clipboard_append(details)
        self.update()
        messagebox.showinfo("Sucesso", "Detalhes da conta copiados para a área de transferência!")

    def delete_account(self, account):
        # Confirmar a exclusão com o usuário
        confirmation = messagebox.askyesno(
            title="Confirmar Exclusão",
            message=f"Tem certeza que deseja deletar a conta '{account['name']}'?"
        )

        if confirmation:
            # Remover a conta da lista
            self.accounts.remove(account)

            # Salvar os dados atualizados
            from main import save_data
            save_data("data.json", self.key, self.accounts)

            # Atualizar a lista de contas na interface
            self.update_accounts_list()

            messagebox.showinfo("Sucesso", f"Conta '{account['name']}' deletada com sucesso!")

    def on_closing(self):
        print("Salvando dados antes de fechar...")
        from main import save_data
        save_data("data.json", self.key, self.accounts)
        self.destroy()


if __name__ == "__main__":
    # Carregar chave de criptografia
    try:
        with open("key.key", "rb") as key_file:
            key = key_file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)

    # Carregar contas existentes (ou usar uma lista vazia para teste)
    accounts = load_data("data.json", key)

    # Iniciar a interface gráfica
    app = App(accounts, key)
    app.mainloop()