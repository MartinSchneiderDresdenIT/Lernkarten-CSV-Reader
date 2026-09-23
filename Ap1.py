import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re


class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lernkarten")
        self.root.geometry("800x500")
        self.cards = []
        self.current_card = 0
        buttonheight=3
        qa_field_width= 50 #Fill muss aus sein! Sonst füllt es Breite aus
        qa_field_padyx= 50 #Seitenabstand

        tk.Button(
            root,
            text="CSV-Datei öffnen",
            command=self.load_csv,
            height=buttonheight
        ).pack(pady=10)
        
		# KartenFrame
        kartenFrame=tk.Frame(root,borderwidth=1, relief="groove",background="white")
        kartenFrame.pack(pady=0)
        # Nummer der Karte
        self.number = tk.Label(
            kartenFrame,
            text="",
            font=("Arial", 14, "bold"),
            background="white"
        )
        
        
        # init Frage, update after Antwort...
        self.question = tk.Text(root, width=qa_field_width, wrap="word")
        self.question.pack(fill="x", expand=False,padx=qa_field_padyx)
        self.question.update_idletasks()
        
        
		# Auswahlbuttons
        buttonFrame= tk.Frame(root,borderwidth=1,relief="groove")
        buttonFrame.pack(pady=5)
        tk.Button(
            buttonFrame,
            text="Nächste Frage",
            command=self.next_card,
            height=buttonheight
        ).pack(pady=5,padx=5,side="right")
        
        tk.Button(
            buttonFrame,
            text="Vorherige Frage",
            command=self.prev_card,
            height=buttonheight
        ).pack(pady=5,padx=5,side="left")

        tk.Button(
            buttonFrame,
            text="Antwort anzeigen",
            command=self.show_answer,
            height=buttonheight
        ).pack(pady=5,padx=5)

        # Antwort
        self.answer = tk.Text(root, width=qa_field_width, wrap="word")
        self.answer.tag_configure("bold", font=("Arial", 10, "bold"))
        self.answer.config(state="disabled")
        self.answer.update_idletasks()
        root.after(1, self.answerFieldSizing) #AntwortFeldZeilenAnpassung
        

        # Frage
        self.question.tag_configure("bold", font=("Arial", 10, "bold"))
        self.question.insert("end", "Bitte eine ")
        self.question.insert("end", "CSV-Datei", "bold")
        self.question.insert("end", " auswählen!")
        self.question.config(state="disabled")
        self.questionFieldSizing() #FrageFeldZeilenAnpassung
        


        # Tastatursteuerung
        self.root.bind(
            "<Down>",
            lambda event: self.show_answer(qa_field_padyx)
        )
        self.root.bind(
            "<Up>",
            lambda event: self.hide_answer()
        )
        self.root.bind(
            "<Right>",
            lambda event: self.next_card()
        )
        self.root.bind(
            "<Left>",
            lambda event: self.prev_card()
        )

    def load_csv(self):
        filepath = filedialog.askopenfilename(
            title="CSV-Datei auswählen",
            filetypes=[
                ("CSV-Dateien", "*.csv"),
                ("Alle Dateien", "*.*")
            ]
        )

        if not filepath:
            return

        try:
            with open(
                filepath,
                "r",
                encoding="utf-8-sig",
                newline=""
            ) as file:
                reader = csv.DictReader(file, delimiter=";")

                self.cards = [
                    (
                        row["NR"],
                        row["Frage"],
                        row["Antwort"]
                    )
                    for row in reader
                    if (
                        row.get("NR") is not None
                        and row.get("Frage") is not None
                        and row.get("Antwort") is not None
                    )
                ]

            if not self.cards:
                raise ValueError(
                    "Die CSV-Datei enthält keine gültigen Karten."
                )

            self.current_card = 0
            self.show_card()

        except (OSError, KeyError, ValueError) as error:
            messagebox.showerror(
                "Fehler",
                f"CSV-Datei konnte nicht gelesen werden:\n{error}"
            )
    
    def formatText(self,widget,text):
        widget.config(state="normal")
        widget.delete("1.0", "end")

        BOLD_PATTERN = r"(\*\*.*?\*\*)" # Pattern für **Fett**
        parts = re.split(BOLD_PATTERN, text)
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                widget.insert("end", part[2:-2], "bold")
            else:
                widget.insert("end", part.replace("\\n","\n"))# Zeilenumbruch \n mit replace
        widget.config(state="disabled")

    def questionFieldSizing(self):
        self.question.update_idletasks()
        result = self.question.count(
            "1.0",
            "end-1c",
            "displaylines"
        )
        zeilenumbruche = result[0] if result else 0
        # print("Zeilenumbrüche: ",zeilenumbruche)
        self.question.config(height=zeilenumbruche+1)

    def answerFieldSizing(self):
        self.answer.update_idletasks()
        result = self.answer.count(
            "1.0",
            "end-1c",
            "displaylines"
        )        
        zeilenumbruche = result[0] if result else 0
        # print("Answer Zeilenumbrüche: ",zeilenumbruche)
        self.answer.config(height=zeilenumbruche+1)
        

    def show_card(self):
        self.answer.pack_forget()
        self.number.pack(pady=0)
        nr, question, _ = self.cards[self.current_card]
        
        self.number.config(text=f"Nr. {nr}")
        self.formatText(self.question,question) #insert: Frage
        self.questionFieldSizing()
        self.answer.config(state="normal")
        self.answer.delete("1.0","end")
        self.answer.config(state="disabled")
        self.answerFieldSizing()

    def show_answer(self,qa_padx):
        self.answer.pack(fill="x", expand=False, padx=qa_padx)
        if self.cards:
            NR,question, answer = self.cards[self.current_card]
            self.answer.config(state="normal")
            self.formatText(self.answer,answer)
            self.answer.config(state="disabled")
            self.answerFieldSizing()

    def hide_answer(self):
        self.answer.pack_forget()
        

    def next_card(self):
        if self.cards:
            self.current_card = (
                self.current_card + 1
            ) % len(self.cards)
            self.show_card()

    def prev_card(self):
        if self.cards:
            self.current_card = (
                self.current_card - 1
            ) % len(self.cards)
            self.show_card()
    

if __name__ == "__main__":
    app_root = tk.Tk()
    FlashcardApp(app_root)
    app_root.mainloop()
