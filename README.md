Passa Bomb 
Overview 

Passa Bomb is a tool designed to simplify the process of sharing online game accounts with friends or team members. It allows you to store and manage multiple accounts along with their authentication details securely. With just one click, you can easily share account information while ensuring that sensitive data remains protected. 
Features 

    Account Management:  Easily add, store, and delete game accounts.
    Authentication Support:  Supports TOTP (Time-based One-Time Password) for secure authentication.
    User-Friendly Interface:  Intuitive and modern GUI built with CustomTkinter.
    Data Encryption:  All stored data is encrypted using strong cryptographic methods to ensure security.
    Token Generation:  Automatically generates and updates TOTP tokens for each account.
     

How It Works 

    Add an Account:  
        Enter the account details such as name, email, password, and the secret key from the authenticator.
        Click "Add Account" to save the new account in the system.
         

    View Accounts:  
        The list of saved accounts will be displayed under the "Contas Salvas" section.
        Each account entry shows the name, email, current token, and time remaining until the next token update.
         

    Copy Account Details:  
        Click the "Copiar" button next to an account to copy all its details, including the current token, to the clipboard.
        This makes it easy to share the account information with others.
         

    Delete an Account:  
        To remove an account, click the "Deletar" button next to it.
        A confirmation dialog will appear; confirm the deletion if you're sure.
         

    Automatic Token Updates:  
        The application automatically updates the TOTP tokens every 30 seconds.
        The "Tempo restante" field shows how much time is left before the next token update.
         
     

Getting Started 
Prerequisites 

    Python 3.6 or higher
    Required libraries: customtkinter, pyotp, cryptography
     

Installation 

1 Clone the repository: 
git clone https://github.com/yourusername/passa-bomb.git
cd passa-bomb
2 Install the required packages:
pip install customtkinter pyotp cryptography
 
3 Install the required packages: 
python gui.py
 
    Use the interface to add new accounts, view existing ones, and manage them as needed.
    Ensure that you keep your encryption key (key.key) safe, as it is used to encrypt and decrypt your account data.
     

Contributing 

Contributions are welcome! If you find any bugs or have suggestions for new features, please open an issue or submit a pull request. 
License 

For any questions or feedback, feel free to contact me at your-email@example.com . 
