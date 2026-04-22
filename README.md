# 🔐 Secure Password Vault

A fully local, AES-256 encrypted password manager built with Python and Streamlit. No cloud, no subscriptions — your passwords stay on your machine.

---

## 📸 Screenshots

| Master Password Setup | Add Password |
|---|---|
| ![Master Password](screenshots/master_pwd.png) | ![Add Password](screenshots/add.png) |

| View Passwords | Search |
|---|---|
| ![View](screenshots/view.png) | ![Search](screenshots/search.png) |

| Delete |
|---|
| ![Delete](screenshots/delete.png) |

---

## ✨ Features

- 🔑 **Master Password** — single password to unlock your entire vault
- 🛡️ **AES-256 CBC Encryption** — every entry encrypted with a unique IV
- 🔒 **PBKDF2 Key Derivation** — master password hashed with 100,000 iterations, never stored directly
- 💪 **Live Password Strength Meter** — real-time feedback as you type (Weak / Medium / Strong)
- 👁️ **Show / Hide Passwords** — reveal only when needed
- 📋 **One-Click Copy** — copy to clipboard without exposing on screen
- 🔍 **Search** — instantly find entries by site name
- ❌ **Delete** — remove entries by index

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Streamlit** — UI framework
- **PyCryptodome** — AES encryption & PBKDF2
- **Pyperclip** — clipboard support
- **JSON** — local encrypted storage

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/secure-password-vault.git
cd secure-password-vault
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run secure_vault.py
```

### 4. First Launch
- You'll be prompted to create a **Master Password** (min. 8 characters)
- After setup, log in with your master password every time you open the app

---

## 📁 Project Structure

```
secure-password-vault/
│
├── secure_vault.py       # Main application
├── secure_db.json        # Encrypted database (auto-created on first run)
├── requirements.txt      # Dependencies
├── .gitignore            # Files to exclude from git
├── README.md             # You're here
└── screenshots/          # App screenshots
    ├── master_pwd.png
    ├── add.png
    ├── view.png
    ├── search.png
    └── delete.png
```

---

## 🔐 Security Details

| Feature | Implementation |
|---|---|
| Encryption | AES-256 CBC |
| Key Derivation | PBKDF2-SHA256, 100,000 iterations |
| IV | Random 16-byte IV per entry |
| Salt | Random 16-byte salt |
| Storage | Local JSON file only |

> ⚠️ **Note:** `secure_db.json` is excluded from git via `.gitignore` to protect your data. Never commit this file.

---

## ⚙️ Requirements

- Python 3.7+
- Works on Windows, macOS, Linux

> **Note:** The copy-to-clipboard feature (`pyperclip`) requires a display environment. It works locally but may not work on cloud-hosted Streamlit.

---

## 📄 License

MIT License — free to use, modify, and distribute.
