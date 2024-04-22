import os
import tkinter as tk
from tkinter import filedialog, messagebox, GROOVE, END
from tkinter.ttk import Combobox, Button

import pyttsx3

from tts import text_to_speech
from stt import speech_to_text
from pdf_reader import read_pdf_text


class Application:
    engine = pyttsx3.init()

    def __init__(self):
        self.speed_combobox = None
        self.gender_combobox = None
        self.text_area = None
        self.root = tk.Tk()
        self.root.title("Text and Speech Converter")
        self.root.geometry("900x450")
        self.root.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        self.root.configure(bg="#025")
        header_fr = tk.Frame(self.root, bg="white", width=900, height=100)
        header_fr.place(x=0, y=0)
        tk.Label(header_fr, text="TEXT TO SPEECH", font="arial 20 bold", bg="white", fg="black").place(x=350, y=10)

        self.text_area = tk.Text(self.root, font="Roboto", bg="white", wrap="word")
        self.text_area.place(x=10, y=150, width=500, height=250)

        gender_lbl = tk.Label(self.root, text="VOICE", font="arial 15 bold", bg="#025", fg="white")
        gender_lbl.place(x=550, y=160)
        self.gender_combobox = Combobox(self.root, values=["Male", "Female"], state="readonly", width=10)
        self.gender_combobox.place(x=550, y=200)
        self.gender_combobox.set("Male")

        speed_lbl = tk.Label(self.root, text="SPEED", font="arial 15 bold", bg="#025", fg="white")
        speed_lbl.place(x=750, y=160)
        self.speed_combobox = Combobox(self.root, values=["Fast", "Normal", "Slow"], state="readonly", width=10)
        self.speed_combobox.place(x=750, y=200)
        self.speed_combobox.set("Normal")

        play_btn_img = tk.PhotoImage(file="assets/play_btn1.png")
        play_btn = Button(self.root, text="Play", image=play_btn_img, command=self.speak_now)
        play_btn.image = play_btn_img
        play_btn.place(x=550, y=280)

        dw_btn_img = tk.PhotoImage(file="assets/dw_btn1.png")
        dw_btn = Button(self.root, text="Download", image=dw_btn_img, command=self.download)
        dw_btn.image = dw_btn_img
        dw_btn.place(x=750, y=280)

        # TODO
        # self.select_pdf_button = Button(self.root, text="Select PDF and Convert to Speech",
        #                                command=self.select_pdf_file)
        #self.select_pdf_button.pack(padx=60, pady=120)
        #
        #self.select_audio_button = Button(self.root, text="Select Audio and Convert to Text",
        #                                  command=self.select_audio_file)
        #self.select_audio_button.pack(padx=60, pady=120)

    def speak_now(self):
        text = self.text_area.get("1.0", "end-1c")
        gender = self.gender_combobox.get()
        speed = self.speed_combobox.get()
        voices = self.engine.getProperty("voices")
        voice = voices[0] if gender == "Male" else voices[1]
        self.engine.setProperty("voice", voice.id)
        rate = 250 if speed == "Fast" else 150 if speed == "Normal" else 60
        self.engine.setProperty("rate", rate)
        self.engine.say(text)
        self.engine.runAndWait()

    def download(self):
        text = self.text_area.get("1.0", "end-1c")
        gender = self.gender_combobox.get()
        speed = self.speed_combobox.get()
        voices = self.engine.getProperty("voices")
        voice = voices[0] if gender == "Male" else voices[1]
        self.engine.setProperty("voice", voice.id)
        rate = 250 if speed == "Fast" else 150 if speed == "Normal" else 60
        self.engine.setProperty("rate", rate)
        file_path = filedialog.askdirectory()
        if file_path:  # Check if a directory was selected
            full_path = os.path.join(file_path, "text.mp3")
            try:
                self.engine.save_to_file(text, full_path)
                self.engine.runAndWait()
                messagebox.showinfo("Success", f"File has been saved successfully at {full_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
        else:
            messagebox.showinfo("Cancelled", "No directory was selected.")

    def run(self):
        self.root.mainloop()

    def select_pdf_file(self):
        file_path = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            text = read_pdf_text(file_path)
            if text:
                self.convert_text_to_speech(text)
            else:
                messagebox.showinfo("Info", "No text found in PDF.")

    def convert_text_to_speech(self, text, lang='en'):
        try:
            text_to_speech(text, lang)
            messagebox.showinfo("Success", "Speech has been generated from text.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def select_audio_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio Files", "*.wav;*.mp3")]
        )
        if file_path:
            try:
                text = speech_to_text(file_path)
                messagebox.showinfo("Recognized Speech", text)
            except Exception as e:
                messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = Application()
    app.run()
