from queue import Queue
from threading import Thread
from PIL import Image, ImageTk
from pronouncer import *
from addword import * 

"""
TODO:
# 1. Add the reveal command and button
# 2. Add the option of adding words
# 3. Clean the word_list.txt 
# 4. Browsing through the words using numbers (spinbox)
# 5. Reading the definition 
# 6. Alter the IntVar with a spinbox
# 7. Use queue ds for speaking
# 8. a chechbutton for allowing the option
"""

def apply_func_to_q(func, q):
    while not q.empty():
        func(q.get())


class MainApp(tk.Frame):

    def __init__(self, master):
        self.master = master
        self.master.geometry('300x100')
        self.master.resizable(0, 0)
        self.master.title('Word Speller')
        self.master.protocol('WM_DELETE_WINDOW', self._close_app)
        self._load_words()
        self.index_spinbox = ttk.Spinbox(self.master, from_=1, to=len(self.words), width=10)
        self.index_spinbox.set(1)
        self.index_spinbox.bind("<Return>", func=self._update_word)
        self.h = 13
        self.word_revealed = False

        # a chechbutton for the user to choose to read the definiton or not
        self.want_def = tk.IntVar()
        self.def_check = ttk.Checkbutton(self.master, text='Read Definition', variable=self.want_def)

        # loading the image for the play button
        self.play_image = Image.open('images/play.png').resize((self.h, self.h))
        self.play_image = ImageTk.PhotoImage(self.play_image)

        # making the buttons and the enteries
        self.play_btn = ttk.Button(self.master, image=self.play_image, command=self._play_word)
        self.next_btn = ttk.Button(self.master, text='Next Word', command=self.next_word)
        self.prev_btn = ttk.Button(self.master, text='Previous Word', command=self.prev_word)
        self.add_word_btn = ttk.Button(self.master, text='Add a Word', command=self._add_word)
        self.reveal_btn = ttk.Button(self.master, text='Reveal', command=self.reveal_word)
        self._make_answer_entry()
        # word label
        self.word_label = ttk.Label(self.master, text='*' * len(self.word))

        # handling the speaking in a queue
        self.speaking_queue = Queue() # the queue
        self.speaking_options = ('en', False) # the options for speaking
        self.thread_running = True # a variable for keeping the loop running as long as the program is running (will be terminated when the window is closed)
        self.sound_thread = Thread(target=self._speaking_loop) # the thread that is going to handle the speaking
        self.sound_thread.start() 
        self._place_widgets() # placing the widgets
        self._check_buttons() # checking the buttons to ensure that the prev_btn is disabled for the first item by defualt

    @property 
    def word(self):
        return self.words[int(self.index_spinbox.get())-1].name

    @property
    def full_word(self):
        return self.words[int(self.index_spinbox.get())-1]

    def _update_word(self, *args):
        self._check_buttons()
        self._update_labels()
        self._play_word()

    def _speaking_loop(self, *args):
        while self.thread_running:
            apply_func_to_q(say, self.speaking_queue)

            continue

    def _close_app(self):
        self.thread_running = False
        self.__clear_sound_files()
        self.master.destroy()

    def __clear_sound_files(self):
        for f in os.listdir('.'):
            if f.endswith('current_word.mp3'):
                try:
                    os.remove(f'./{f}')
                except PermissionError:
                    pass

    def _add_word(self):
        miniMaster = tk.Toplevel()
        add_window = AddWordWindow(miniMaster)
        while not add_window.word_taken:
            if self.thread_running:
                continue
            else:
                break

        obj = add_window.word_obj
        if obj:
            self.words.append(obj)

    def _check_buttons(self):
        self.answer_entry['state'] = 'enabled'
        self.next_btn['state'] = 'enabled'
        self.prev_btn['state'] = 'enabled'
        try:
            index = int(self.index_spinbox.get())
        except ValueError:
            self.index_spinbox.delete(0, tk.END)
            self.index_spinbox.insert(0, 1)
            index = int(self.index_spinbox.get())

        if index == len(self.words):
            self.next_btn['state'] = 'disabled'
        
        elif index == 1:
            self.prev_btn['state'] = 'disabled'

    def _update_labels(self):
        self.word_label['text'] = self.word if self.word_revealed else '*' * len(self.word)
        self.answer_entry.delete(0, tk.END)

    def say(self, text, lang='en', slow=False):
        self.speaking_queue.put(text)
        self.speaking_options = (lang, slow)

    def reveal_word(self, *args):
        self.answer_entry['state'] = 'disabled'
        self.word_revealed = True
        self._update_labels()
        word_speparated = " ".join(list(self.word.upper()))
        self.say(f"The word is {self.word} and spelled as {word_speparated}.")

    def next_word(self, *args):
        self._check_buttons()
        old = int(self.index_spinbox.get())
        self.index_spinbox.delete(0, tk.END)
        self.index_spinbox.insert(0, str(old + 1)) 
        self._check_buttons()
        self.word_revealed = False
        self._update_labels()
        apply_func_to_q(lambda x: 0, self.speaking_queue)
        self._play_word()

    def prev_word(self, *args): 
        self._check_buttons()
        old = int(self.index_spinbox.get())
        self.index_spinbox.delete(0, tk.END)
        self.index_spinbox.insert(0, str(old - 1)) 
        self._check_buttons()
        self.word_revealed = False
        self._update_labels()
        apply_func_to_q(lambda x: 0, self.speaking_queue)
        self._play_word()

    def _load_words(self, filename='word_list.txt'):
        self.words = []
        with open('word_list.txt', 'r') as f:
            for line in f.readlines():
                if ':' in line:
                    colon_index = line.index(':') 
                    w = line[:colon_index].strip()
                    d = line[colon_index+1:].strip()
                else:
                    w = line.strip()
                    d = ''

                self.words.append(Word(w, d))

    def _make_answer_entry(self):
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
            self.say("You're correct!")
            self.word_revealed = True
            self._update_labels()
            self.next_word()
            return True

        else:
            self.say('Incorrect.')
            return False

    def _place_widgets(self):
        self.word_label.place(relx=.5, rely=.1, anchor=tk.CENTER)
        self.prev_btn.place(relx=0, rely=.3)
        self.next_btn.place(relx=.75, rely=.3)
        self.play_btn.place(relx=0, rely=.78)
        self.add_word_btn.place(rely=0)
        self.answer_entry.place(relx=.3, rely=.78)
        self.reveal_btn.place(relx=.75, rely=.77)
        self.index_spinbox.place(relx=.4, rely=.31)
        self.def_check.place(relx=.65, rely=0)

    def _play_word(self, *args):
        word = self.full_word
        self.say(word.name, 'en', False)
        if self.want_def.get():
            self.say(word.definition)
    

def test():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == '__main__':
    test()