import tkinter as tk
from tkinter import filedialog, messagebox
import piexif
import os
from tkcalendar import DateEntry
import time

# Funzione per ottenere la data di scatto originale dai dati EXIF
def get_data_exif(file_path):
    try:
        img = Image.open(file_path)
        exif_data = img._getexif()
        
        # Trova il tag corrispondente a "DateTimeOriginal"
        date_time_original_tag = None
        for tag, value in TAGS.items():
            if value == 'DateTimeOriginal':
                date_time_original_tag = tag
                break
        
        if exif_data and date_time_original_tag:
            return exif_data.get(date_time_original_tag)
        else:
            return "N/A"
    
    except Exception as e:
        return f"Errore: {str(e)}"

# Funzione per modificare la data di scatto EXIF
def cambia_data_exif(file_path, nuova_data):
    try:
        img = Image.open(file_path)
        
        # Carica i dati EXIF esistenti o crea un nuovo dizionario se non esistono
        if 'exif' in img.info:
            exif_dict = piexif.load(img.info['exif'])
        else:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}

        # Aggiungi o modifica la data di scatto nel tag 36867 (DateTimeOriginal)
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = nuova_data.encode('utf-8')
        
        # Anche per il tag 36868 (DateTimeDigitized) e 306 (DateTime) per coerenza
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = nuova_data.encode('utf-8')
        exif_dict['0th'][piexif.ImageIFD.DateTime] = nuova_data.encode('utf-8')

        exif_bytes = piexif.dump(exif_dict)
        img.save(file_path, exif=exif_bytes)
        
        return True  # Indica che l'operazione è stata eseguita correttamente
    
    except Exception as e:
        return False  # Indica che c'è stato un errore

# Funzione per selezionare i file
def seleziona_file():
    file_paths = filedialog.askopenfilenames(filetypes=[("Immagini", "*.jpg *.jpeg *.png")])
    if file_paths:
        listbox_files.delete(0, tk.END)  # Svuota la lista precedente
        for file_path in file_paths:
            data_exif = get_data_exif(file_path)
            listbox_files.insert(tk.END, f"{os.path.basename(file_path)} - Data di scatto: {data_exif}")
        root.file_paths = file_paths

# Funzione per modificare la data di scatto per tutti i file selezionati
def modifica_data():
    if hasattr(root, 'file_paths') and root.file_paths:
        # Costruisce la data completa
        nuova_data = f"{calendario.get_date().strftime('%Y:%m:%d')} {entry_ora.get()}"
        if nuova_data:
            success = True
            for file_path in root.file_paths:
                if not cambia_data_exif(file_path, nuova_data):
                    success = False
                    break  # Se un file fallisce, interrompiamo il ciclo
            
            # Mostra un unico messaggio alla fine
            if success:
                messagebox.showinfo("Successo", "La data di scatto è stata modificata con successo per tutti i file selezionati!")
            else:
                messagebox.showerror("Errore", "Si è verificato un errore durante la modifica di uno o più file.")
        else:
            messagebox.showwarning("Avviso", "Inserisci una nuova data prima di continuare.")
    else:
        messagebox.showwarning("Avviso", "Seleziona prima uno o più file.")

# Creazione della GUI
root = tk.Tk()
root.title("Modifica EXIF - Data di Scatto")

# Bottone per selezionare file
button_seleziona = tk.Button(root, text="Seleziona File", command=seleziona_file)
button_seleziona.pack(padx=10, pady=10)

# Lista per mostrare i file selezionati e le loro date
listbox_files = tk.Listbox(root, width=80, height=10)
listbox_files.pack(padx=10, pady=10)

# Label e DateEntry per selezionare la nuova data
label_data = tk.Label(root, text="Seleziona la nuova data:")
label_data.pack(padx=10, pady=5)

calendario = DateEntry(root, date_pattern='yyyy/mm/dd')
calendario.pack(padx=10, pady=5)

# Label e Entry per inserire la nuova ora
label_ora = tk.Label(root, text="Inserisci la nuova ora (HH:MM:SS):")
label_ora.pack(padx=10, pady=5)

entry_ora = tk.Entry(root, width=10)
entry_ora.insert(0, time.strftime('%H:%M:%S'))  # Inserisce l'ora corrente come valore predefinito
entry_ora.pack(padx=10, pady=5)

# Bottone per modificare la data
button_modifica = tk.Button(root, text="Modifica Data di Scatto", command=modifica_data)
button_modifica.pack(padx=10, pady=10)

# Avvio del loop della GUI
root.mainloop()
