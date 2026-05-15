import tkinter as tk
from tkinter import messagebox
from github import Github, Auth
import qrcode
from PIL import Image, ImageTk
import io
import json
import os

# -----------------------------
# PARAMÈTRES GITHUB
# -----------------------------
GITHUB_TOKEN = ""          # ⚠ à remplacer
REPO_NAME = "fdu-edo/QRCodeMSG"
FILE_PATH = "message.txt"
BRANCH = "main"

# URL GitHub Pages (affichage lisible)
QR_URL = "https://fdu-edo.github.io/QRCodeMSG/"

# FICHIER LOCAL POUR SAUVEGARDE
LOCAL_FILE = "messages.json"

# -----------------------------
# LISTE DES MESSAGES LOCAUX
# -----------------------------
messages = []


# -----------------------------
# SAUVEGARDE LOCALE
# -----------------------------
def load_local_messages():
    global messages
    if os.path.exists(LOCAL_FILE):
        try:
            with open(LOCAL_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)
        except:
            messages = []
    else:
        messages = []


def save_local_messages():
    with open(LOCAL_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


# -----------------------------
# FONCTIONS GITHUB
# -----------------------------
def get_github_file():
    auth = Auth.Token(GITHUB_TOKEN)
    g = Github(auth=auth)

    repo = g.get_repo(REPO_NAME)
    contents = repo.get_contents(FILE_PATH, ref=BRANCH)
    return contents.decoded_content.decode("utf-8")


def update_github_file(new_content):
    auth = Auth.Token(GITHUB_TOKEN)
    g = Github(auth=auth)

    repo = g.get_repo(REPO_NAME)
    contents = repo.get_contents(FILE_PATH, ref=BRANCH)

    repo.update_file(
        path=FILE_PATH,
        message="Publication via l'application Tkinter",
        content=new_content,
        sha=contents.sha,
        branch=BRANCH
    )


# -----------------------------
# GÉNÉRATION DU QR CODE
# -----------------------------
def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill="black", back_color="white")


# -----------------------------
# INTERFACE TKINTER
# -----------------------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Gestion du Message QRCode")

        # LISTBOX
        self.listbox = tk.Listbox(root, height=5, width=80)
        self.listbox.pack(fill="x", padx=10, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # BOUTONS
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=5)

        self.btn_edit = tk.Button(frame_buttons, text="Modifier", command=self.edit_message)
        self.btn_edit.grid(row=0, column=0, padx=5)

        self.btn_save = tk.Button(frame_buttons, text="Sauvegarder", command=self.save_message)
        self.btn_save.grid(row=0, column=1, padx=5)

        self.btn_delete = tk.Button(frame_buttons, text="Supprimer", command=self.delete_message)
        self.btn_delete.grid(row=0, column=2, padx=5)

        # ZONE DE TEXTE
        self.text = tk.Text(root, width=60, height=10, font=("Arial", 14))
        self.text.pack(pady=10)

        # BOUTON PUBLIER
        self.btn_publish = tk.Button(root, text="Publier le message", command=self.publish_message)
        self.btn_publish.pack(pady=5)

        # QR CODE
        self.qr_label = tk.Label(root)
        self.qr_label.pack(pady=10)

        # Charger messages locaux
        load_local_messages()
        self.refresh_listbox()

        # Charger message GitHub
        self.load_initial_message()

        # QR code dès le lancement
        self.update_qr()

    # -----------------------------
    # LISTBOX
    # -----------------------------
    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for msg in messages:
            first_line = msg.split("\n")[0]
            self.listbox.insert(tk.END, first_line)

    def on_select(self, event):
        if not self.listbox.curselection():
            return
        index = self.listbox.curselection()[0]
        msg = messages[index]
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, msg)

    # -----------------------------
    # GESTION DES MESSAGES
    # -----------------------------
    def save_message(self):
        new_msg = self.text.get("1.0", tk.END).strip()
        if new_msg and new_msg not in messages:
            messages.append(new_msg)
            save_local_messages()
            self.refresh_listbox()
            messagebox.showinfo("OK", "Message ajouté.")

    def edit_message(self):
        if not self.listbox.curselection():
            return
        index = self.listbox.curselection()[0]
        new_msg = self.text.get("1.0", tk.END).strip()
        messages[index] = new_msg
        save_local_messages()
        self.refresh_listbox()
        messagebox.showinfo("OK", "Message modifié.")

    def delete_message(self):
        if not self.listbox.curselection():
            return
        index = self.listbox.curselection()[0]
        messages.pop(index)
        save_local_messages()
        self.refresh_listbox()
        self.text.delete("1.0", tk.END)
        messagebox.showinfo("OK", "Message supprimé.")

    # -----------------------------
    # CHARGEMENT INITIAL
    # -----------------------------
    def load_initial_message(self):
        try:
            content = get_github_file()
            self.text.insert(tk.END, content)

            if content not in messages:
                messages.append(content)
                save_local_messages()
                self.refresh_listbox()

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger : {e}")

    # -----------------------------
    # PUBLICATION + QR CODE
    # -----------------------------
    def publish_message(self):
        try:
            new_content = self.text.get("1.0", tk.END).strip()
            update_github_file(new_content)
            messagebox.showinfo("Succès", "Message publié sur GitHub")
            self.update_qr()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de publier : {e}")

    # -----------------------------
    # QR CODE PERMANENT
    # -----------------------------
    def update_qr(self):
        img = generate_qr_code(QR_URL)
    
        # Sauvegarde en JPG dans le répertoire local
        img.save("qrcode.jpg", format="JPEG")
    
        # Affichage dans l'application
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        bio.seek(0)
    
        qr_img = Image.open(bio)
        qr_img = qr_img.resize((250, 250))
        qr_photo = ImageTk.PhotoImage(qr_img)
    
        self.qr_label.config(image=qr_photo)
        self.qr_label.image = qr_photo

# -----------------------------
# LANCEMENT
# -----------------------------
root = tk.Tk()
app = App(root)
root.mainloop()
