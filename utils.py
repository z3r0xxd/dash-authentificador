import json
import base64
from cryptography.fernet import Fernet


def load_data(filename, key):
    try:
        with open(filename, "r") as file:
            content = file.read()
            if not content.strip():  # Verifica se o arquivo está vazio
                print(f"Arquivo {filename} está vazio. Usando lista vazia.")
                return []
            encrypted_accounts = json.loads(content)  # Usa json.loads para carregar o conteúdo
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
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON no arquivo {filename}. Usando lista vazia.")
        return []
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return []


def save_data(filename, key, accounts):
    try:
        encrypted_accounts = []
        for account in accounts:
            encrypted_account = {}
            for k, v in account.items():
                if k not in ["token_label", "timer_label"]:  # Ignora widgets
                    encrypted_account[k] = encrypt_data(key, v)  # Criptografa apenas os valores serializáveis
            encrypted_accounts.append(encrypted_account)

        with open(filename, "w") as file:
            json.dump(encrypted_accounts, file, indent=4)  # Usa o módulo json aqui
        print(f"Dados salvos em {filename}")
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")


def encrypt_data(key, data):
    fernet = Fernet(key)
    encrypted_bytes = fernet.encrypt(data.encode())
    return base64.b64encode(encrypted_bytes).decode()  # Usa o módulo base64 aqui


def decrypt_data(key, encrypted_data):
    fernet = Fernet(key)
    encrypted_bytes = base64.b64decode(encrypted_data)  # Usa o módulo base64 aqui
    return fernet.decrypt(encrypted_bytes).decode()