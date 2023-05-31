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
    filetypes = (('All files', '*.*'),('Videofile', '*.mp4 *.avi *.mkv *.mov *.wmv *.webm *.flv'),('Audiofile', '*.mp3 *.wav *.flac *.aac *.ogg *.wma'))
    filename = filedialog.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
    url_filename_entryfield.insert(tk.END, filename)

    
def process():
    url_path = url_filename_entryfield.get()
    api_key = api_key_entryfield.get()
    size = select_model_size_combobox.get()
    translator = translator_var.get()
    whisper_translate = whisper_translate_checkbuttonvar.get()

    #Ausgabefeld leeren
    output_textbox.configure(state="normal")  # Aktiviere das Bearbeiten des Textfelds
    output_textbox.delete("1.0", tk.END)
    output_textbox.configure(state="disabled")  # Deaktiviere das Bearbeiten des Textfelds

    #Prüfen ob Text aus Eingabefeld eine gültige URL bzw. Dateipfad ist
    if re.match(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url_path):
        #Download der Datei
        download_file(url_path)

    # Überprüfe, ob der Text ein Dateipfad ist
    elif os.path.exists(url_path):
        shutil.copyfile(url_path, 'file')

    else:
        return


    if translator == "whisper":
        if url_path == "":
            messagebox.showerror("Error", "Bitte gültige(n) URL/Dateipfad eingeben")
            return

        try:
            # Erstellen des Transkribers
            model = whisper.load_model(size)

            #Prüfen ob Originalsprache beibehalten werden soll
            if whisper_translate == False:
                result = model.transcribe('file',task='translate')
            else:
                result = model.transcribe('file')

        except RuntimeError as e:
            if "CUDNN_STATUS_NOT_INITIALIZED" in str(e):
                messagebox.showinfo("Fehler", "Nicht genügend VRAM. Kleineres Modell wählen")
            else:
                messagebox.showinfo("Fehler","Ein Fehler ist aufgetreten:", str(e))


        # Ausgabe der Transkription
        for segment in result["segments"]:
            line = "[%s --> %s]%s" % (round(segment["start"],2),round(segment["end"],2), segment["text"])

            output_textbox.configure(state="normal")  # Aktiviere das Bearbeiten des Textfelds
            output_textbox.insert(tk.END, line + '\n')  # Schreibe den neuen Text in das Textfeld
            output_textbox.configure(state="disabled")  # Deaktiviere das Bearbeiten des Textfelds
        
    if translator == "deepl":

        if url_path == "" or api_key == "":
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

            output_textbox.configure(state="normal")  # Aktiviere das Bearbeiten des Textfelds
            output_textbox.insert(tk.END, line + '\n')  # Schreibe den neuen Text in das Textfeld
            output_textbox.configure(state="disabled")  # Deaktiviere das Bearbeiten des Textfelds


    #Tempfile löschen
    os.remove("./file")

    messagebox.showinfo("Success", "Data processed successfully.")

# Erstelle das Hauptfenster
window = tk.Tk()
window.title("Pr0-Videoübersetzer")
window.geometry("680x600")

# Erstelle Eingabefeld für URL
url_file_label = tk.Label(window, text="URL/File:")
url_filename_entryfield = tk.Entry(window,width=40)

# Erstelle Button um Datei auszuwählen
filepicker_button = tk.Button(window, text="Datei auswählen", command=select_file)

# Erstelle Radiobuttons für Auswahl des Übersetzers
translatorname_label = tk.Label(window, text="Übersetzer wählen:")

translator_var = tk.StringVar()
translator_var.set("whisper")  # Standardauswahl

whipser_radiobutton = tk.Radiobutton(window, text="Whisper (kein API-Key benötigt)", variable=translator_var, value="whisper")

whisper_translate_checkbuttonvar = tk.IntVar()
whisper_origin_language_checkbox = tk.Checkbutton(window, text="Whisper: Originalsprache beibehalten", variable=whisper_translate_checkbuttonvar)

deepl_radiobutton = tk.Radiobutton(window, text="Deepl (API-Key benötigt)", variable=translator_var, value="deepl")

# Erstelle Eingabefeld für API-Key
api_key_entryfield = tk.Entry(window,width=25)
api_key_entryfield.insert(-1, "API-Key")

# Erstelle Label und Combobox für Auswahl Modellgröße Whisper
model_size_label = tk.Label(window, text="Modellgröße wählen:")

select_model_size_combobox = ttk.Combobox(state="readonly", values=["tiny","base","small","medium","large"])
select_model_size_combobox.set("base")
#select_model_size_combobox = ttk.Combobox(values=["tiny (1GB VRAM)","base (1GB VRAM)","small (2GB VRAM)","medium (5GB VRAM)","large (10GB VRAM)"])

# Erstelle Textfeld für die Ausgabe
output_text_label = tk.Label(window, text="Ausgabe")

output_textbox = tk.Text(window)
output_textbox.configure(state="disabled")  # Deaktiviere das Bearbeiten des Textfelds

output_textbox_scrollbar = ttk.Scrollbar(window, orient='vertical', command=output_textbox.yview)

# Erstelle Button zum Verarbeiten der Daten
process_button = tk.Button(window, text="Process", command=process)

# Erstelle Button zum Beenden
quit_button = tk.Button(window, text="Exit", command=window.destroy)

#Anordnung der Elemente
url_file_label.grid(column=0, row=0)
url_filename_entryfield.grid(column=0, row=1)
filepicker_button.grid(column=1, row=1)
translatorname_label.grid(column=0, row=3)
whipser_radiobutton.grid(sticky="W",column=0, row=4)
deepl_radiobutton.grid(sticky="W", column=0, row=5)
whisper_origin_language_checkbox.grid(column=1, row=4)
api_key_entryfield.grid(sticky="W", column=1, row=5)
model_size_label.grid(sticky="W", column=0, row=6)
select_model_size_combobox.grid(sticky="W",column=1, row=6)
output_text_label.grid(sticky="W", column=0, row=7)
output_textbox.grid(column=0, row=8, columnspan=3, rowspan=2)
output_textbox_scrollbar.grid(column=3, row=8,rowspan=2, sticky=tk.NS)
process_button.grid(sticky="E", column=0, row=12)
quit_button.grid(sticky="W",column=1, row=12)

# Starte die Hauptereignisschleife
window.mainloop()
