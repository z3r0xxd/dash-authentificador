# main.py

import json
import base64
from cryptography.fernet import Fernet

# Gerar uma chave de criptografia (ou carregar uma chave existente)
try:
    with open("key.key", "rb") as key_file:
        key = key_file.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Funções de criptografia
def encrypt_data(key, data):
    fernet = Fernet(key)
    encrypted_bytes = fernet.encrypt(data.encode())
    return base64.b64encode(encrypted_bytes).decode()

def decrypt_data(key, encrypted_data):
    fernet = Fernet(key)
    encrypted_bytes = base64.b64decode(encrypted_data)
    return fernet.decrypt(encrypted_bytes).decode()

# Salvar dados no arquivo JSON
def save_data(filename, key, accounts):
    encrypted_accounts = []
    for account in accounts:
        encrypted_account = {}
        for k, v in account.items():
            encrypted_account[k] = encrypt_data(key, v)  # Criptografa apenas os valores
        encrypted_accounts.append(encrypted_account)
    with open(filename, "w") as file:
        json.dump(encrypted_accounts, file, indent=4)  # Use indent=4 para facilitar a leitura

# Carregar dados do arquivo JSON
def save_data(filename, key, accounts):
    try:
        encrypted_accounts = []
        for account in accounts:
            encrypted_account = {}
            for k, v in account.items():
                encrypted_account[k] = encrypt_data(key, v)  # Criptografa apenas os valores
            encrypted_accounts.append(encrypted_account)
        
        with open(filename, "w") as file:
            json.dump(encrypted_accounts, file, indent=4)  # Use indent=4 para facilitar a leitura
        print(f"Dados salvos em {filename}")
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")

def load_data(filename, key):
    try:
        with open(filename, "r") as file:
            encrypted_accounts = json.load(file)
        accounts = []
        for encrypted_account in encrypted_accounts:
            decrypted_account = {}
            for k, v in encrypted_account.items():
                decrypted_account[k] = decrypt_data(key, v)  # Descriptografa apenas os valores
            accounts.append(decrypted_account)
        print(f"Dados carregados de {filename}")
        return accounts
    except FileNotFoundError:
        print(f"Arquivo {filename} não encontrado. Usando lista vazia.")
        return []
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return []

if __name__ == "__main__":
    # Carregar contas existentes
    accounts = load_data("data.json", key)

    # Iniciar a interface gráfica
    app = App(accounts, key)
    app.mainloop()

    # Salvar contas ao fechar o aplicativo
    save_data("data.json", key, app.accounts)