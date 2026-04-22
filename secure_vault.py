import streamlit as st
import json, os, base64
import pyperclip
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from hashlib import pbkdf2_hmac

DB_FILE = "secure_db.json"

# =========================
# 💪 PASSWORD STRENGTH
# =========================

def check_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    return score

# =========================
# 🔐 CRYPTO (SECURE)
# =========================

def derive_key(password, salt):
    return pbkdf2_hmac("sha256", password.encode(), salt, 100000, dklen=32)

def encrypt(data, key):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(iv + ct).decode()

def decrypt(data, key):
    raw = base64.b64decode(data)
    iv = raw[:16]
    ct = raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size).decode()

# =========================
# 📂 DATABASE
# =========================

def load_db():
    if not os.path.exists(DB_FILE):
        return {"salt": "", "master_hash": "", "data": []}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

db = load_db()

# =========================
# 🖥️ UI
# =========================

st.set_page_config(page_title="Secure Vault", page_icon="🔐")
st.title("🔐 Secure Password Vault")

# =========================
# 🆕 FIRST SETUP
# =========================

if db["master_hash"] == "":
    st.subheader("Create Master Password")
    pwd = st.text_input("New Master Password", type="password")

    if st.button("Set Password"):
        if len(pwd) < 8:
            st.error("Use at least 8 characters")
        else:
            salt = get_random_bytes(16)
            key = derive_key(pwd, salt)
            db["salt"] = base64.b64encode(salt).decode()
            db["master_hash"] = base64.b64encode(key).decode()
            save_db(db)
            st.success("Setup complete ✅")
            st.rerun()

# =========================
# 🔐 LOGIN
# =========================

else:
    if "auth" not in st.session_state:
        st.session_state.auth = False

    pwd = st.text_input("Enter Master Password", type="password")

    if st.button("Login"):
        salt = base64.b64decode(db["salt"])
        key = derive_key(pwd, salt)

        if base64.b64encode(key).decode() == db["master_hash"]:
            st.session_state.auth = True
            st.session_state.key = key
            st.success("Login successful ✅")
        else:
            st.error("Wrong password ❌")

# =========================
# 🔓 MAIN APP
# =========================

if st.session_state.get("auth"):
    key = st.session_state.key

    menu = st.sidebar.radio("Menu", ["Add", "View", "Search", "Delete"])

    # ➕ ADD
    if menu == "Add":
        st.subheader("Add Password")

        col1, col2 = st.columns(2)
        site = col1.text_input("Website")
        user = col2.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if pwd:
            strength = check_strength(pwd)
            if strength <= 2:
                st.error("Weak Password ❌")
            elif strength == 3:
                st.warning("Medium Password ⚠️")
            else:
                st.success("Strong Password 💪")

        if st.button("Save"):
            data = json.dumps({"site": site, "user": user, "pwd": pwd})
            db["data"].append(encrypt(data, key))
            save_db(db)
            st.success("Saved securely 🔐")

    # 👀 VIEW
    elif menu == "View":
        st.subheader("Stored Passwords")

        if not db["data"]:
            st.warning("No entries")
        else:
            for i, item in enumerate(db["data"]):
                try:
                    d = json.loads(decrypt(item, key))

                    with st.expander(f"{i}: {d['site']}"):
                        st.write(f"👤 {d['user']}")

                        col1, col2 = st.columns([3, 1])

                        with col1:
                            show = st.checkbox(f"Show password {i}")
                            if show:
                                st.code(d["pwd"])
                            else:
                                st.write("🔑 ********")

                        with col2:
                            if st.button(f"Copy {i}"):
                                pyperclip.copy(d["pwd"])
                                st.success("Copied!")

                except:
                    st.error("Decryption error")

    # 🔍 SEARCH
    elif menu == "Search":
        st.subheader("Search")
        query = st.text_input("Enter site name")

        for item in db["data"]:
            try:
                d = json.loads(decrypt(item, key))
                if query.lower() in d["site"].lower():
                    st.write(f"🌐 {d['site']} | 👤 {d['user']} | 🔑 {d['pwd']}")
            except:
                pass

    # ❌ DELETE
    elif menu == "Delete":
        st.subheader("Delete Entry")
        index = st.number_input("Index", step=1)

        if st.button("Delete"):
            try:
                db["data"].pop(index)
                save_db(db)
                st.success("Deleted ✅")
            except:
                st.error("Invalid index ❌")