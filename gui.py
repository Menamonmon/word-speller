import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from pronouncer import say
class MainApp(tk.Frame):

    def __init__(self, master):
        self.master = master
        self.master.geometry('300x100')
        self.master.resizable(0, 0)
        self.master.title('Word Speller')
        self.word = 'Google'
        self.h = 13
        # styling
        self.style = ttk.Style()
        self.style.configure('TButton', height=self.h, bg='red', font='impact 8')
        self.style.configure('TEntry', height=self.h, bg='red', font='impact')

        # loading the image for the play button
        self.play_image = Image.open('images/play.png').resize((self.h, self.h))
        self.play_image = ImageTk.PhotoImage(self.play_image)

        # making the button and the enteries
        self.play_btn = ttk.Button(self.master, image=self.play_image, command=self._play_word)
        self.next_btn = ttk.Button(self.master, text='Next Word')
        self.prev_btn = ttk.Button(self.master, text='Previous Word')
        self.add_word_btn = ttk.Button(self.master, text='Add a Word')
        self.reveal_btn = ttk.Button(self.master, text='Reveal')
        self.make_answer_entry()
        # word label
        self.word_label = ttk.Label(self.master, text='*' * self.word_len)
        self.place_widgets()
    
    @property
    def word_len(self):
        if hasattr(self, "word"):
            return len(self.word.get())

        return 0

    def make_answer_entry(self):
        self.word = tk.StringVar()
        self.answer_entry = ttk.Entry(self.master, textvariable=self.word)
        self.answer_entry.insert(0, 'Type the word here')
        self.answer_entry.bind('<FocusIn>', func=lambda x: focus_on(self.answer_entry))
        self.answer_entry.bind('<FocusOut>', func=lambda x: focus_off(self.answer_entry))

        def focus_on(entry, *args):
            entry.delete(0, tk.END)
        
        def focus_off(entry, *args):
            entry.insert(0, 'Type the word here')

        def check_length(var, limit):
            text = var.get()
            if len(text) > limit:
                var.set(text[:limit])
        self.word.trace('w', lambda *a: check_length(self.word, self.word_len))

    def place_widgets(self):
        self.word_label.place(relx=.5, rely=.1, anchor=tk.CENTER)
        self.prev_btn.place(relx=0, rely=.3)
        self.next_btn.place(relx=.75, rely=.3)
        self.play_btn.place(relx=0, rely=.78)
        self.answer_entry.place(relx=.3, rely=.78)
        self.reveal_btn.place(relx=.4, rely=.78)

    def _play_word(self, *args):
        word = self.word.get() if self.word.get() != 'Type the word here' else 'There is no current word'
        say(word, 'en', False)

def test():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == '__main__':
    test()