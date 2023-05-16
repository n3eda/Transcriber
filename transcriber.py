import tkinter as tk
from tkinter import messagebox

import requests
import whisper
import os
import deepl

def download_file(url):
    #Herunterladen des Videos
    response = requests.get(url)
    with open("file.mp4", "wb") as f:
        f.write(response.content)
    

def process():
    url = url_entry.get()
    api_key = api_key_entry.get()
    size = size_var.get()
    translator = translator_var.get()

    #Ausgabefeld leeren
    output_text.configure(state="normal")  # Aktiviere das Bearbeiten des Textfelds
    output_text.delete("1.0", tk.END)
    output_text.configure(state="disabled")  # Deaktiviere das Bearbeiten des Textfelds

    #Download der Datei
    download_file(url)


    if translator == "whisper":
        if url == "":
            messagebox.showerror("Error", "Please enter a valid URL")
            return

        # Erstellen des Transkribers
        model = whisper.load_model(size)
        result = model.transcribe('file.mp4',task='translate')

        # Ausgabe der Transkription
        for segment in result["segments"]:
            line = "[%s --> %s]%s" % (round(segment["start"],2),round(segment["end"],2), segment["text"])

            output_text.configure(state="normal")  # Aktiviere das Bearbeiten des Textfelds
            output_text.insert(tk.END, line + '\n')  # Schreibe den neuen Text in das Textfeld
            output_text.configure(state="disabled")  # Deaktiviere das Bearbeiten des Textfelds
        
    if translator == "deepl":

        if url == "" or api_key == "":
            messagebox.showerror("Error", "Please enter a URL and API key.")
            return

        # Erstellen des Transkribers
        model = whisper.load_model(size)
        result = model.transcribe('file.mp4')

        translator = deepl.Translator(api_key)

        # Ausgabe der Transkription
        for segment in result["segments"]:
            translated = translator.translate_text(segment["text"], target_lang="DE")
            line = "[%s --> %s]%s" % (segment["start"],segment["end"], translated)

            output_text.configure(state="normal")  # Aktiviere das Bearbeiten des Textfelds
            output_text.insert(tk.END, line + '\n')  # Schreibe den neuen Text in das Textfeld
            output_text.configure(state="disabled")  # Deaktiviere das Bearbeiten des Textfelds


    #Tempfile löschen
    os.remove("./file.mp4")

    messagebox.showinfo("Success", "Data processed successfully.")

# Erstelle das Hauptfenster
window = tk.Tk()
window.title("Pr0-Videoübersetzer")
window.geometry("400x600")

# Erstelle Eingabefeld für URL
url_label = tk.Label(window, text="URL:")
url_label.pack()
url_entry = tk.Entry(window,width=40)
url_entry.pack()


# Erstelle Radiobuttons für Auswahl des Übersetzers
translator = tk.Label(window, text="Übersetzer wählen:")
translator.pack()

translator_var = tk.StringVar()
translator_var.set("whisper")  # Standardauswahl

pick_deepl = tk.Radiobutton(window, text="Deepl(API-Key benötigt)", variable=translator_var, value="deepl")
pick_deepl.pack()

pick_whisper = tk.Radiobutton(window, text="Whisper (kein API-Key benötigt)", variable=translator_var, value="whisper")
pick_whisper.pack()

# Erstelle Eingabefeld für API-Key
api_key_label = tk.Label(window, text="API Key:")
api_key_label.pack()
api_key_entry = tk.Entry(window,width=25)
api_key_entry.pack()

# Erstelle Radiobuttons für Größenauswahl
size_label = tk.Label(window, text="Modellgröße wählen:")
size_label.pack()

size_var = tk.StringVar()
size_var.set("base")  # Standardauswahl

size_tiny = tk.Radiobutton(window, text="tiny (1GB VRAM)", variable=size_var, value="tiny")
size_tiny.pack()

size_base = tk.Radiobutton(window, text="base (1GB VRAM)", variable=size_var, value="base")
size_base.pack()

size_small = tk.Radiobutton(window, text="small (2GB VRAM)", variable=size_var, value="small")
size_small.pack()

size_medium = tk.Radiobutton(window, text="medium (5GB VRAM)", variable=size_var, value="medium")
size_medium.pack()

# Erstelle Textfeld für die Ausgabe
output_text = tk.Text(window, height=20)
output_text.pack()
output_text.configure(state="disabled")  # Deaktiviere das Bearbeiten des Textfelds

# Erstelle Button zum Verarbeiten der Daten
process_button = tk.Button(window, text="Process", command=process)
process_button.pack()

# Erstelle Button zum Beenden
quit_button = tk.Button(window, text="Exit", command=window.destroy)
quit_button.pack()

# Starte die Hauptereignisschleife
window.mainloop()
