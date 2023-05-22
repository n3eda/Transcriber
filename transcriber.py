import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

import re
import shutil
import requests
import whisper
import os
import deepl

def download_file(url):
    #Herunterladen des Videos
    response = requests.get(url)
    with open("file", "wb") as f:
        f.write(response.content)

def select_file():
    #Öffnen des Filepickers
    filetypes = (('All files', '*.*'),('Videofile', '*.mp4'))
    filename = filedialog.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
    url_filename_entry.insert(tk.END, filename)

    
def process():
    url = url_filename_entry.get()
    api_key = api_key_entry.get()
    size = select_model_size_combobox.get()
    translator = translator_var.get()
    whisper_translate = whisper_translate_checkbuttonvar.get()

    #Ausgabefeld leeren
    output_text.configure(state="normal")  # Aktiviere das Bearbeiten des Textfelds
    output_text.delete("1.0", tk.END)
    output_text.configure(state="disabled")  # Deaktiviere das Bearbeiten des Textfelds

    #Prüfen ob Text aus Eingabefeld eine gültige URL bzw. Dateipfad ist
    if re.match(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url):
        #Download der Datei
        download_file(url)

    # Überprüfe, ob der Text ein Dateipfad ist
    elif os.path.exists(url):
        shutil.copyfile(url, 'file')

    else:
        return


    if translator == "whisper":
        if url == "":
            messagebox.showerror("Error", "Please enter a valid URL/Filename")
            return

        # Erstellen des Transkribers
        model = whisper.load_model(size)

        #Prüfen ob Originalsprache beibehalten werden soll
        if whisper_translate == False:
            result = model.transcribe('file',task='translate')
        else:
            result = model.transcribe('file')


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
        result = model.transcribe('file')

        translator = deepl.Translator(api_key)

        # Ausgabe der Transkription
        for segment in result["segments"]:
            translated = translator.translate_text(segment["text"], target_lang="DE")
            line = "[%s --> %s]%s" % (segment["start"],segment["end"], translated)

            output_text.configure(state="normal")  # Aktiviere das Bearbeiten des Textfelds
            output_text.insert(tk.END, line + '\n')  # Schreibe den neuen Text in das Textfeld
            output_text.configure(state="disabled")  # Deaktiviere das Bearbeiten des Textfelds


    #Tempfile löschen
    os.remove("./file")

    messagebox.showinfo("Success", "Data processed successfully.")

# Erstelle das Hauptfenster
window = tk.Tk()
window.title("Pr0-Videoübersetzer")
window.geometry("650x450")

# Erstelle Eingabefeld für URL
url_file_label = tk.Label(window, text="URL/File:")
url_file_label.grid(column=0, row=0)
url_filename_entry = tk.Entry(window,width=40)
url_filename_entry.grid(column=0, row=1)

# Erstelle Button um Datei auszuwählen
filename = tk.Button(window, text="Datei auswählen", command=select_file)
filename.grid(column=1, row=1)


# Erstelle Radiobuttons für Auswahl des Übersetzers
translator = tk.Label(window, text="Übersetzer wählen:")
translator.grid(column=0, row=3)

translator_var = tk.StringVar()
translator_var.set("whisper")  # Standardauswahl

pick_whisper = tk.Radiobutton(window, text="Whisper (kein API-Key benötigt)", variable=translator_var, value="whisper")
pick_whisper.grid(sticky="W",column=0, row=4)

whisper_translate_checkbuttonvar = tk.IntVar()
whisper_translate_checkbutton = tk.Checkbutton(window, text="Whisper: Originalsprache beibehalten", variable=whisper_translate_checkbuttonvar)
whisper_translate_checkbutton.grid(column=1, row=4)

pick_deepl = tk.Radiobutton(window, text="Deepl(API-Key benötigt)", variable=translator_var, value="deepl")
pick_deepl.grid(sticky="W", column=0, row=5)

# Erstelle Eingabefeld für API-Key
api_key_entry = tk.Entry(window,width=25)
api_key_entry.insert(-1, "API-Key")
api_key_entry.grid(sticky="W", column=1, row=5)

# Erstelle Label und Combobox für Auswahl Modellgröße Whisper
size_label = tk.Label(window, text="Modellgröße wählen:")
size_label.grid(sticky="W", column=0, row=6)

select_model_size_combobox = ttk.Combobox(values=["tiny","base","small","medium","large"])
#select_model_size_combobox = ttk.Combobox(values=["tiny (1GB VRAM)","base (1GB VRAM)","small (2GB VRAM)","medium (5GB VRAM)","large (10GB VRAM)"])
select_model_size_combobox.grid(sticky="W",column=1, row=6)

# Erstelle Textfeld für die Ausgabe
output_text_label = tk.Label(window, text="Ausgabe")
output_text_label.grid(sticky="W", column=0, row=7)

output_text = tk.Text(window)
output_text.grid(column=0, row=8, columnspan=3, rowspan=2)
output_text.configure(state="disabled")  # Deaktiviere das Bearbeiten des Textfelds

scrollbar_output_text = ttk.Scrollbar(window, orient='vertical', command=output_text.yview)
scrollbar_output_text.grid(column=3, row=8,rowspan=2, sticky=tk.NS)

# Erstelle Button zum Verarbeiten der Daten
process_button = tk.Button(window, text="Process", command=process)
process_button.grid(sticky="E", column=0, row=12)

# Erstelle Button zum Beenden
quit_button = tk.Button(window, text="Exit", command=window.destroy)
quit_button.grid(sticky="W",column=1, row=12)

# Starte die Hauptereignisschleife
window.mainloop()
