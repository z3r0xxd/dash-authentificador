# main.py

import json
import base64
from cryptography.fernet import Fernet
from utils import load_data, save_data
from gui import App

# Gerar ou carregar chave de criptografia
try:
    with open("key.key", "rb") as key_file:
        key = key_file.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

if __name__ == "__main__":
    # Carregar contas existentes
    accounts = load_data("data.json", key)

    # Iniciar a interface gráfica
    app = App(accounts, key)
    app.mainloop()

    # Limpar widgets antes de salvar
    accounts_to_save = []
    for account in app.accounts:
        # Cria uma cópia limpa dos dados, sem os widgets
        clean_account = {
            "name": account["name"],
            "email": account["email"],
            "password": account["password"],
            "totp_secret": account["totp_secret"]
        }
        accounts_to_save.append(clean_account)

    # Depurar os dados antes de salvar
    print("Dados a serem salvos:", accounts_to_save)

    # Salvar contas ao fechar o aplicativo
    save_data("data.json", key, accounts_to_save)