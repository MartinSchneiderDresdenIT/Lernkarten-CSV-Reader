import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lernkarten")
        self.root.geometry("800x500")
        self.cards = []
        self.current_card = 0
        buttonheight=3

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
        self.number.pack(pady=0)
        # Frage
        self.question = tk.Label(
            kartenFrame,
            text="Bitte eine CSV-Datei öffnen.",
            wraplength=700,
            font=("Arial", 18),
            background="white"
        )
        self.question.pack(padx=20, pady=0)
        
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
            command=self.show_answer            ,
            height=buttonheight
        ).pack(pady=5,padx=5)

        # Antwort
        self.answer = tk.Label(
            root,
            text="",
            wraplength=700,
            font=("Arial", 16),
            fg="darkgreen",
            justify="left",
            anchor="w"
        )
        self.answer.pack(padx=20, pady=10)

        # Tastatursteuerung
        self.root.bind(
            "<Down>",
            lambda event: self.show_answer()
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

    def show_card(self):
        nr, question, _ = self.cards[self.current_card]
        
        self.number.config(text=f"Nr. {nr}")
        self.question.config(text=question)
        self.answer.config(text="")

    def show_answer(self):
        if self.cards:
            nr, question, answer = self.cards[self.current_card]

            self.number.config(text=f"Nr. {nr}")
            self.question.config(text=question)
            self.answer.config(text=answer)

    def hide_answer(self):
        if self.cards:
            self.answer.config(text="")

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
