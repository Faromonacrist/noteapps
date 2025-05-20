import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry
import json
import os
from datetime import datetime
from tkinter import messagebox

FILENAME = "notes.json"
PASSWORD = "123"
current_theme = "litera"

app = ttk.Window(themename=current_theme)
app.title("🗒️ Užrašų aplikacija")
app.geometry("600x800")

# Login frame
login_frame = ttk.Frame(app, padding=20)
login_frame.pack(fill=BOTH, expand=YES)

ttk.Label(login_frame, text="Įveskite slaptažodį:", font='Helvetica 12 bold').pack(pady=10)
password_entry = ttk.Entry(login_frame, show="*")
password_entry.pack(pady=5)
login_error_label = ttk.Label(login_frame, text="", bootstyle="danger")
login_error_label.pack()

# Main frame
main_frame = ttk.Frame(app, padding=10)

note_entry = None
add_date_picker = None
search_entry = None
search_date_picker = None
notes_listbox = None


def load_notes():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r", encoding="utf-8") as f:
        return json.load(f)


def save_notes(notes):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=4, ensure_ascii=False)


def refresh_notes():
    notes = load_notes()
    notes_listbox.delete(0, "end")
    for i, note in enumerate(notes, 1):
        notes_listbox.insert("end", f"{i}. [{note['date']}] {note['text']}")


def add_note():
    note = note_entry.get("1.0", "end").strip()
    date_raw = add_date_picker.entry.get()
    if not note or not date_raw:
        messagebox.showwarning("Įspėjimas", "Įveskite užrašą ir datą.")
        return

    try:
        # Normalizuojame datą
        date = datetime.strptime(date_raw, "%m/%d/%Y").strftime("%m/%d/%Y")
    except ValueError:
        messagebox.showerror("Klaida", "Netinkamas datos formatas.")
        return

    timestamp = datetime.now().strftime("%H:%M")
    new_note = {"text": note, "date": date, "time": timestamp}
    notes = load_notes()
    notes.append(new_note)
    save_notes(notes)
    refresh_notes()
    note_entry.delete("1.0", "end")


def delete_note():
    try:
        index = notes_listbox.curselection()[0]
        notes = load_notes()
        notes.pop(index)
        save_notes(notes)
        refresh_notes()
    except IndexError:
        messagebox.showwarning("Klaida", "Pasirinkite užrašą.")


def search_notes():
    query = search_entry.get().strip().lower()
    selected_date_raw = search_date_picker.entry.get().strip()

    try:
        selected_date = datetime.strptime(selected_date_raw, "%m/%d/%Y").strftime("%m/%d/%Y")
    except ValueError:
        selected_date = ""

    notes = load_notes()

    # Filtruojame pagal tekstą ir datą
    filtered = []
    for note in notes:
        text_match = query in note["text"].lower() if query else True
        date_match = note["date"] == selected_date if selected_date else True
        if text_match and date_match:
            filtered.append(note)

    # Rikiuojame pagal datą (konvertuojam į datetime objektą)
    filtered.sort(key=lambda n: datetime.strptime(n["date"], "%m/%d/%Y"))

    # Atvaizduojame
    notes_listbox.delete(0, "end")
    for i, note in enumerate(filtered, 1):
        notes_listbox.insert("end", f"{i}. [{note['date']}] {note['text']}")


def toggle_theme():
    global current_theme
    current_theme = "cyborg" if current_theme == "litera" else "litera"
    app.style.theme_use(current_theme)


def show_main_window():
    login_frame.pack_forget()
    main_frame.pack(fill=BOTH, expand=YES)
    refresh_notes()


def check_password():
    if password_entry.get() == PASSWORD:
        login_error_label.config(text="")
        show_main_window()
    else:
        login_error_label.config(text="Neteisingas slaptažodis.")


# Prisijungimo mygtukas
ttk.Button(login_frame, text="Prisijungti", command=check_password, bootstyle=PRIMARY).pack(pady=10)

# ------ MAIN FRAME TURINYS ------
ttk.Label(main_frame, text="Naujas užrašas:", font='Helvetica 12 bold').pack(anchor=W)
note_entry = ttk.Text(main_frame, height=4)
note_entry.pack(fill=X, pady=5)

ttk.Label(main_frame, text="Pasirinkite datą (pridėti):", font='Helvetica 10').pack(anchor=W)
add_date_picker = DateEntry(main_frame, width=12, dateformat="%m/%d/%Y")
add_date_picker.pack(pady=5)

ttk.Button(main_frame, text="Pridėti", command=add_note, bootstyle=SUCCESS).pack(fill=X, pady=5)

ttk.Label(main_frame, text="Paieška pagal tekstą:", font='Helvetica 10').pack(anchor=W, pady=(10, 0))
search_entry = ttk.Entry(main_frame)
search_entry.pack(fill=X, pady=5)

ttk.Label(main_frame, text="Pasirinkite datą (paieškai):", font='Helvetica 10').pack(anchor=W)
search_date_picker = DateEntry(main_frame, width=12, dateformat="%m/%d/%Y")
search_date_picker.pack(pady=5)

ttk.Button(main_frame, text="Ieškoti", command=search_notes, bootstyle=INFO).pack(fill=X)

notes_listbox = tk.Listbox(main_frame, height=10, font=("Arial", 10))
notes_listbox.pack(fill=BOTH, expand=YES, pady=10)

ttk.Button(main_frame, text="Ištrinti pažymėtą", command=delete_note, bootstyle=DANGER).pack(fill=X, pady=5)
ttk.Button(main_frame, text="Keisti temą", command=toggle_theme, bootstyle=SECONDARY).pack(fill=X)

app.bind("<Escape>", lambda event: app.destroy())
# Paleidžiam programą
app.mainloop()
"# test" 
