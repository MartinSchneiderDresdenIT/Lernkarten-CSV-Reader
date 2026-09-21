import csv
from logging import root
import tkinter as tk
from tkinter import filedialog, messagebox


class FlashcardApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Lernkarten")
		self.root.geometry("800x500")
		self.cards = []
		self.current_card = 0

		tk.Button(root, text="CSV-Datei öffnen", command=self.load_csv).pack(pady=10)

		self.question = tk.Label(
			root, text="Bitte eine CSV-Datei öffnen.",
			wraplength=500, font=("Arial", 18), height=4
		)
		self.question.pack(padx=20, pady=10)

		tk.Button(root, text="Nächste Frage ", command=self.next_card).pack(pady=5)
		tk.Button(root, text="Antwort anzeigen ", command=self.show_answer).pack(pady=5)
		
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
		self.root.bind("<Down>", lambda event: self.show_answer())
		self.root.bind("<Up>", lambda event: self.hide_answer())
		self.root.bind("<Right>", lambda event: self.next_card())
		self.root.bind("<Left>", lambda event: self.prev_card())

		

	def load_csv(self):
		filepath = filedialog.askopenfilename(
			title="CSV-Datei auswählen",
			filetypes=[("CSV-Dateien", "*.csv"), ("Alle Dateien", "*.*")]
		)
		if not filepath:
			return

		try:
			with open(filepath, "r", encoding="utf-8-sig", newline="") as file:
				reader = csv.DictReader(file, delimiter=";")
				self.cards = [
					(row["Frage"], row["Antwort"])
					for row in reader
					if row.get("Frage") is not None and row.get("Antwort") is not None
				]
			if not self.cards:
				raise ValueError("Die CSV-Datei enthält keine gültigen Karten.")
			self.current_card = 0
			self.show_card()
		except (OSError, KeyError, ValueError) as error:
			messagebox.showerror("Fehler", f"CSV-Datei konnte nicht gelesen werden:\n{error}")

	def show_card(self):
		question, _ = self.cards[self.current_card]
		self.question.config(text=question)
		self.answer.config(text="")

	def show_answer(self):
		if self.cards:
			self.answer.config(text=self.cards[self.current_card][1])
			
	def hide_answer(self):
		if self.cards:
			self.answer.config(text="")

	def next_card(self):
		if self.cards:
			self.current_card = (self.current_card + 1) % len(self.cards)
			self.show_card()

	def prev_card(self):
		if self.cards:
			self.current_card = (self.current_card - 1) % len(self.cards)
			self.show_card()


if __name__ == "__main__":
	app_root = tk.Tk()
	FlashcardApp(app_root)
	app_root.mainloop()
