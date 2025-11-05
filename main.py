import os
from tkinter import *
from PIL import Image, ImageTk 

# --- KONFIGURACIJA ---
IMAGE_PATH = "images"

root = Tk()
root.title("Bookstore")
root.geometry("1100x650")
root.config(bg="white")

cart = {}  # {naslov: {"cena": cena(float), "kolicina": broj, "ukupno": cena*kolicina}}

# --- FUNKCIJE ---
def dodaj_u_korpu(naslov, cena_str):
    cena = float(cena_str.replace("€","").strip())
    if naslov in cart:
        cart[naslov]["kolicina"] += 1
    else:
        cart[naslov] = {"cena": cena, "kolicina": 1}
    cart[naslov]["ukupno"] = cart[naslov]["kolicina"] * cart[naslov]["cena"]
    osvezi_korpu()

def obrisi_iz_korpe(naslov):
    if naslov in cart:
        cart.pop(naslov)
    osvezi_korpu()

def obrisi_sve_iz_korpe():
    cart.clear()
    osvezi_korpu()

def osvezi_korpu():
    for widget in cart_frame_inner.winfo_children():
        widget.destroy()

    ukupno = 0
    for naslov, podaci in cart.items():
        ukupno += podaci["ukupno"]
        row_frame = Frame(cart_frame_inner, bg="white")
        row_frame.pack(fill=X, pady=2)

        Label(row_frame, text=f"{naslov} x{podaci['kolicina']} - {podaci['ukupno']:.2f} €",
              anchor="w", bg="white").pack(side=LEFT, padx=5)

        btn_delete = Button(row_frame, text="🗑", command=lambda n=naslov: obrisi_iz_korpe(n),
                            bg="#ffdddd", relief=FLAT)
        btn_delete.pack(side=RIGHT, padx=5)

    # Ажурирање броја књига и укупне цене
    broj_knjiga = sum([p['kolicina'] for p in cart.values()])
    cart_label.config(text=f"🛒 {broj_knjiga}")
    total_label.config(text=f"UKUPNO: {ukupno:.2f} €")

    # Прикажи или сакриј дугме "Обриши све"
    if broj_knjiga > 0:
        clear_all_button.pack(pady=5)
    else:
        clear_all_button.pack_forget()

def filtriraj_knjige(*args):
    query = search_entry.get().lower()
    selektovani_zanr = zanr_var.get()

    for frame, (naslov, _, _, zanr) in knjige_frames:
        vidljiv = True
        if query not in naslov.lower():
            vidljiv = False
        if selektovani_zanr != "Svi" and selektovani_zanr != zanr:
            vidljiv = False
        if vidljiv:
            frame.grid()
        else:
            frame.grid_remove()

def promeni_zanr(*args):
    filtriraj_knjige()

# --- HEADER ---
header_frame = Frame(root, bg="#f5f5f5", height=60)
header_frame.pack(fill=X, side=TOP)

# PADAJUĆI MENI - ŽANROVI
zanrovi = ["Svi", "Self-Help", "Productivity", "Programming", "Software Design", "Python"]
zanr_var = StringVar(value="Svi")
zanr_menu = OptionMenu(header_frame, zanr_var, *zanrovi)
zanr_menu.config(font=("Arial", 12), bg="white")
zanr_menu.pack(side=LEFT, padx=10, pady=10)
zanr_var.trace("w", promeni_zanr)

title_label = Label(header_frame, text="📚 My Bookstore", font=("Arial", 20, "bold"), bg="#f5f5f5")
title_label.pack(side=LEFT, padx=20)

search_entry = Entry(header_frame, width=30, font=("Arial", 12))
search_entry.pack(side=LEFT, padx=10, pady=10)
search_entry.bind("<KeyRelease>", filtriraj_knjige)

cart_label = Label(header_frame, text="🛒 0", font=("Arial", 16), bg="#f5f5f5")
cart_label.pack(side=RIGHT, padx=20)

# --- GLAVNI SADRZAJ ---
main_frame = Frame(root, bg="white")
main_frame.pack(fill=BOTH, expand=True)

books_frame = Frame(main_frame, bg="white")
books_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

canvas = Canvas(books_frame, bg="white", highlightthickness=0)
scrollbar = Scrollbar(books_frame, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas, bg="white")
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

# Korpa
cart_frame = Frame(main_frame, bg="#fafafa", width=250, relief=SOLID, bd=1)
cart_frame.pack(side=RIGHT, fill=Y)

Label(cart_frame, text="🛒 Korpa", font=("Arial", 14, "bold"), bg="#fafafa").pack(pady=10)
cart_frame_inner = Frame(cart_frame, bg="white")
cart_frame_inner.pack(fill=BOTH, expand=True, padx=5, pady=5)

# Дугме за брисање свих ставки (појављује се динамички)
clear_all_button = Button(cart_frame, text="🗑 Obriši sve", bg="#ff8888", fg="white",
                          font=("Arial", 11, "bold"), command=obrisi_sve_iz_korpe)

total_label = Label(cart_frame, text="UKUPNO: 0.00 €", font=("Arial", 12, "bold"), bg="#fafafa")
total_label.pack(pady=10)

# --- PRIKAZ KNJIGA ---
books = [
    ("Atomic Habits", "book1.jpg", "15 €", "Self-Help"),
    ("Deep Work", "book2.jpg", "20 €", "Productivity"),
    ("Clean Code", "book3.jpg", "25 €", "Programming"),
    ("The Pragmatic Programmer", "book4.jpg", "22 €", "Programming"),
    ("Design Patterns", "book5.png", "30 €", "Software Design"),
    ("Python Crash Course", "book6.png", "18 €", "Python"),
]

knjige_frames = []
row = 0
col = 0
for naslov, img_file, cena, zanr in books:
    frame = Frame(scrollable_frame, bg="white", bd=2, relief=GROOVE)
    frame.grid(row=row, column=col, padx=15, pady=15)

    try:
        img_path = os.path.join(IMAGE_PATH, img_file)
        img = Image.open(img_path).resize((120, 160))
        img_tk = ImageTk.PhotoImage(img)
        img_label = Label(frame, image=img_tk, bg="white")
        img_label.image = img_tk
        img_label.pack()
    except:
        Label(frame, text="[No Image]", bg="white").pack()

    Label(frame, text=naslov, font=("Arial", 12, "bold"), bg="white").pack(pady=5)
    Label(frame, text=cena, font=("Arial", 11), fg="green", bg="white").pack()

    btn = Button(frame, text="Dodaj u korpu",
                 command=lambda n=naslov, c=cena: dodaj_u_korpu(n, c),
                 bg="#ffcc66")
    btn.pack(pady=5)

    knjige_frames.append((frame, (naslov, img_file, cena, zanr)))

    col += 1
    if col > 2:
        col = 0
        row += 1

root.mainloop()
