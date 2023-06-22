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

            