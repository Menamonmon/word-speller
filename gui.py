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
        self.load_words()
        self.current_word_index = 0
        self.h = 13
        self.word_revealed = False

        # styling
        self.style = ttk.Style()
        self.style.configure('TButton', height=self.h, bg='red', font='impact 8')
        self.style.configure('TEntry', height=self.h, bg='red', font='impact')

        # loading the image for the play button
        self.play_image = Image.open('images/play.png').resize((self.h, self.h))
        self.play_image = ImageTk.PhotoImage(self.play_image)

        # making the button and the enteries
        self.play_btn = ttk.Button(self.master, image=self.play_image, command=self._play_word)
        self.next_btn = ttk.Button(self.master, text='Next Word', command=self.next_word)
        self.prev_btn = ttk.Button(self.master, text='Previous Word', command=self.prev_word)
        self.add_word_btn = ttk.Button(self.master, text='Add a Word')
        self.reveal_btn = ttk.Button(self.master, text='Reveal')
        self.make_answer_entry()
        # word label
        self.word_label = ttk.Label(self.master, text='*' * len(self.word))
        self.place_widgets()
        self.check_buttons()

    @property 
    def word(self):
        return self.words[self.current_word_index]

    def check_buttons(self):
        self.next_btn['state'] = 'enabled'
        self.prev_btn['state'] = 'enabled'
        if self.current_word_index > len(self.words) - 1:
            self.next_btn['state'] = 'disabled'
        
        elif self.current_word_index == 0:
            self.prev_btn['state'] = 'disabled'

    def update_labels(self):
        self.word_label['text'] = self.word if self.word_revealed else '*' * len(self.word)

    def reveal_word(self, *args):
        self.word_revealed = True
        self.update_labels()
        self._play_word()
        self.answer_entry['state'] = 'disabled'

    def next_word(self, *args):
        self.check_buttons()
        if self.current_word_index + 1 >= len(self.words):
            raise Exception(f'The checkbutton method did not work properly, becuase at this point the current index would be {self.current_word_index+1} while the number of words is {len(self.words)}')

        self.current_word_index += 1 
        self.check_buttons()
        self.word_revealed = False
        self.update_labels()

    def prev_word(self, *args): 
        self.check_buttons()
        if self.current_word_index < 0:
            raise Exception(f'The checkbutton method did not work properly, becuase at this point the current index is less that zero ({self.current_word_index})')

        self.current_word_index -= 1
        self.check_buttons()
        self.word_revealed = False
        self.update_labels()

    def load_words(self, filename='word_list.txt'):
        with open(filename, 'r') as f:
            self.words = [word.strip() for word in f.readlines()]

    def make_answer_entry(self):
        self.answer = tk.StringVar()
        ttk.Label(self.master, text='Type the word here: ').place(relx=.29, rely=.55)
        self.answer_entry = ttk.Entry(self.master, textvariable=self.answer)
        self.answer_entry.bind('<Return>', func=self.check_answer)

        def check_length(var, limit):
            text = var.get()
            if len(text) > limit:
                var.set(text[:limit])
        self.answer.trace('w', lambda *a: check_length(self.answer, len(self.word)))

    def check_answer(self, *args):
        if self.answer.get().lower() == self.word.lower():
            say("You're correct.")
            self.word_revealed = True
            self.update_labels()
        else:
            say('Give it another try')

    def place_widgets(self):
        self.word_label.place(relx=.5, rely=.1, anchor=tk.CENTER)
        self.prev_btn.place(relx=0, rely=.3)
        self.next_btn.place(relx=.75, rely=.3)
        self.play_btn.place(relx=0, rely=.78)
        self.answer_entry.place(relx=.3, rely=.78)
        self.reveal_btn.place(relx=.4, rely=.78)

    def _play_word(self, *args):
        say(self.word, 'en', False)

def test():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == '__main__':
    test()