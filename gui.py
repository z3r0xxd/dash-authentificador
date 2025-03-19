import customtkinter as ctk
import pyotp
import time
import tkinter.messagebox as messagebox
from utils import load_data, save_data
from cryptography.fernet import Fernet
import pygetwindow as gw
import pyautogui


class App(ctk.CTk):
    def __init__(self, accounts, key):
        super().__init__()
        self.title("Passa Bomb")
        self.geometry("900x600")

        # Configurar o tema escuro personalizado
        ctk.set_appearance_mode("Dark")  # Modo escuro
        ctk.set_default_color_theme("green")  # Tema verde
        
        self.key = key
        self.accounts = accounts  # Lista de contas carregadas

        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="#000000")  # Fundo preto
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título da Seção "Adicionar Conta"
        self.add_account_title = ctk.CTkLabel(
            self.main_frame,
            text="Adicionar Nova Conta",
            font=("Arial", 18, "bold"),
            text_color="#00FF00"  # Verde neon
        )
        self.add_account_title.pack(fill="x", pady=(0, 10))

        # Frame para adicionar nova conta
        self.add_account_frame = ctk.CTkFrame(self.main_frame, fg_color="#1E1E1E")  # Cinza escuro
        self.add_account_frame.pack(fill="x")

        # Campos para nome, email e senha
        self.name_entry = ctk.CTkEntry(self.add_account_frame, placeholder_text="Nome", fg_color="#333333", border_color="#00FF00")
        self.name_entry.pack(fill="x", pady=5)

        self.email_entry = ctk.CTkEntry(self.add_account_frame, placeholder_text="Email", fg_color="#333333", border_color="#00FF00")
        self.email_entry.pack(fill="x", pady=5)

        self.password_entry = ctk.CTkEntry(self.add_account_frame, placeholder_text="Senha", show="*", fg_color="#333333", border_color="#00FF00")
        self.password_entry.pack(fill="x", pady=5)

        self.secret_key_entry = ctk.CTkEntry(self.add_account_frame, placeholder_text="Chave Secreta do Autenticador", fg_color="#333333", border_color="#00FF00")
        self.secret_key_entry.pack(fill="x", pady=5)

        # Botão para adicionar conta
        self.add_button = ctk.CTkButton(
            self.add_account_frame,
            text="Adicionar Conta",
            command=self.add_account,  # Referência ao método add_account
            fg_color="#00FF00",  # Verde neon
            hover_color="#32CD32",  # Verde mais claro ao passar o mouse
            text_color="black"
        )
        self.add_button.pack(fill="x", pady=10)

        # Título da Seção "Contas Salvas"
        self.saved_accounts_title = ctk.CTkLabel(
            self.main_frame,
            text="Contas Salvas",
            font=("Arial", 18, "bold"),
            text_color="#00FF00"  # Verde neon
        )
        self.saved_accounts_title.pack(fill="x", pady=(20, 10))

        # Frame para listar contas existentes
        self.accounts_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="#1E1E1E")  # Cinza escuro
        self.accounts_frame.pack(fill="both", expand=True)

        # Atualizar a lista de contas
        self.update_accounts_list()

        # Iniciar a atualização automática dos tokens
        self.update_tokens()

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
            info_label = ctk.CTkLabel(account_frame, text=f"{account['name']} ({account['email']})", font=("Arial", 14), text_color="#00FFFF")  # Azul ciano
            info_label.pack(side="left", padx=10)

            # Token TOTP e Timer
            token_label = ctk.CTkLabel(account_frame, text="Carregando...", font=("Arial", 12), text_color="#00FF00")  # Verde neon
            token_label.pack(side="left", padx=10)

            timer_label = ctk.CTkLabel(account_frame, text="Tempo restante: ", font=("Arial", 12), text_color="#00FF00")  # Verde neon
            timer_label.pack(side="left", padx=10)

            # Botão para copiar os detalhes da conta
            copy_button = ctk.CTkButton(
                account_frame,
                text="Copiar",
                width=50,
                command=lambda acc=account: self.copy_account_details(acc),
                fg_color="#00FF00",  # Verde neon
                hover_color="#32CD32",  # Verde mais claro ao passar o mouse
                text_color="black"
            )
            copy_button.pack(side="right", padx=5)

            # Botão para deletar a conta
            delete_button = ctk.CTkButton(
                account_frame,
                text="Deletar",
                width=50,
                command=lambda acc=account: self.delete_account(acc),
                fg_color="#FF4500",  # Laranja neon
                hover_color="#FF8C00",  # Laranja mais claro ao passar o mouse
                text_color="white"
            )
            delete_button.pack(side="right", padx=5)

            # Botão para logar no Tibia
            login_button = ctk.CTkButton(
                account_frame,
                text="Logar",
                width=50,
                command=lambda acc=account: self.login_to_tibia(acc),
                fg_color="#FFD700",  # Amarelo neon
                hover_color="#FFA500",  # Laranja ao passar o mouse
                text_color="black"
            )
            login_button.pack(side="right", padx=5)

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
            if "token_label" in account and "timer_label" in account:
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

            # Atualizar a lista de contas na interface
            self.update_accounts_list()

            messagebox.showinfo("Sucesso", f"Conta '{account['name']}' deletada com sucesso!")

    def login_to_tibia(self, account):
        # Gerar o token TOTP
        totp = pyotp.TOTP(account["totp_secret"])
        token = totp.now()

        # Copiar o token para o clipboard
        self.clipboard_clear()
        self.clipboard_append(token)
        self.update()

        # Localizar a janela do Tibia
        try:
            tibia_windows = gw.getWindowsWithTitle("Tibia")  # Altere "Tibia" para o título correto
            if not tibia_windows:
                messagebox.showerror("Erro", "Janela do Tibia não encontrada!")
                return

            tibia_window = tibia_windows[0]  # Pega a primeira janela encontrada
            if tibia_window.isMinimized:
                tibia_window.restore()  # Restaura a janela se estiver minimizada
            tibia_window.activate()  # Ativa a janela
            time.sleep(1)  # Aguarda um momento para garantir que a janela esteja ativa
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ativar a janela do Tibia: {e}")
            return

        # Preencher os campos automaticamente
        try:
            # Digitar o email
            email = account["email"]
            pyautogui.write(email, interval=0.02)  # Digita o email rapidamente

            pyautogui.press("tab")  # Avança para o próximo campo (senha)

            # Digitar a senha
            pyautogui.write(account["password"], interval=0.02)  # Digita a senha rapidamente
            pyautogui.press("enter")  # Pressiona Enter para enviar o formulário

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao tentar logar: {e}")