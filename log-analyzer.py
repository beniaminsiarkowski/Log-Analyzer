import re
import tkinter as tk
from tkinter import filedialog, scrolledtext

# --- FUNKCJE POMOCNICZE ---

def wyciagnij_emaile(tekst):
    # Szuka wzorca: cos@cos.cos
    wzorzec = r'[a-zA-Z._%+-0-9]+@[a-zA-Z0-9-]+\.[a-zA-Z]+'
    return re.findall(wzorzec, tekst)

def wyciagnij_ip(tekst):
    # Szuka wzorca: 000.000.000.000
    wzorzec_ip = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    return re.findall(wzorzec_ip, tekst)

def analizuj_plik(sciezka_do_pliku):
    # Otwiera plik, czyta treść i ją zwraca
    # 'encoding="utf-8"' zapobiega błędom z polskimi znakami
    with open(sciezka_do_pliku, 'r', encoding='utf-8') as plik:
        tresc = plik.read()
        return tresc

# --- GŁÓWNY PROGRAM ---
def uruchom_skaner():
    pole_wynikow.delete('1.0', tk.END)
    sciezka = filedialog.askopenfilename()
    if not sciezka:
        return
    try:
        pole_wynikow.insert(tk.END, f"--- ANALIZA PLIKU: {sciezka} ---\n\n")
        # Wczytujemy plik (musi być w tym samym folderze!)
        logi_z_pliku = analizuj_plik(sciezka)

        pole_wynikow.insert(tk.END, "--- 1. ZNALEZIONE MAILE ---\n")
        maile = wyciagnij_emaile(logi_z_pliku)
        for m in maile:
           pole_wynikow.insert(tk.END, "Znaleziony email: " + m + "\n")

        pole_wynikow.insert(tk.END, "--- 2. ZNALEZIONE ADRESY IP ---\n")
        adresy = wyciagnij_ip(logi_z_pliku)
        for ip in adresy:
            pole_wynikow.insert(tk.END, "Znalezione ip: " + ip + "\n")
        
        

    except (FileNotFoundError, UnicodeDecodeError):
        pole_wynikow.insert(tk.END, "BŁĄD: Nie udało się otworzyć pliku!")


def zapisz_plik():
     wybor_miejsca_zapisu = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt")])
     caly_wynik = pole_wynikow.get("1.0", tk.END)
     with open(wybor_miejsca_zapisu, "a") as f:
         f.write(caly_wynik)























# --- GŁÓWNE OKNO ---
root = tk.Tk()
root.title("Log Analyzer v1.0")
root.geometry("600x500")
root.configure(background='#7E7E7E')

# 1. NAPIS (LABEL)

napis = tk.Label(root, text="Log Analyzer", font=("Arial", 14))
napis.pack(pady=10)

# 2. PRZYCISK (BUTTON)

przycisk = tk.Button(root, text="📂 Wybierz plik...", command=uruchom_skaner, font=("Arial", 12))
przycisk.pack(pady=10)
przycisk.configure(background='white')



# 3. POLE WYNIKÓW (SCROLLEDTEXT)

pole_wynikow = scrolledtext.ScrolledText(root, width=70, height=20)
pole_wynikow.pack(padx=10, pady=10)

przycisk_save = tk.Button(root, text="Zapisz w pliku...", command=zapisz_plik, font=("Arial", 12))
przycisk_save.pack(pady=10)

# 4. START
root.mainloop()
