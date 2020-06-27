import tkinter as tk
from tkinter import ttk
from word import Word

class AddWordWindow:

    def __init__(self, master, filename='word_list.txt'):
        self.master = master
        self.master.protocol('WM_DELETE_WINDOW', self._destroy)
        self.filename = filename
        self.word_taken = False
        self.word_obj = None

        def fout(var, val):
            var.set(val)

        def fin(var):
            var.set('')

        # word entry
        self.word = tk.StringVar()
        self.word_entry = ttk.Entry(self.master, textvariable=self.word)

        # definition entry
        self.definition = tk.StringVar()
        self.def_entry = ttk.Entry(self.master, textvariable=self.definition)
        self.add_btn = ttk.Button(self.master, text="Add", command=self.add_word)
        self.place_widgets()

        self.master.mainloop()

    def add_word(self):
        w = self.word.get().capitalize()
        d = self.definition.get().capitalize()
        if not d.strip():
            newline = f'\n{w}'
        else:
            newline = f'\n{w}: {d.strip()}'
        with open(self.filename, 'a') as file:
            file.write(newline)

        self.word_obj = Word(w, d.strip())
        self.word_taken = True
        self.master.destroy()

    def place_widgets(self):
        ttk.Label(self.master, text="Word: ").grid(row=0, column=0, sticky=tk.W)
        self.word_entry.grid(row=1, sticky=tk.W)
        ttk.Label(self.master, text="Definition: \n(If left empty, a definition \nform Merriam Webster would be used)").grid(row=2, sticky=tk.W)
        self.def_entry.grid(row=3, sticky=tk.W)
        self.add_btn.grid(row=4, column=1, sticky=tk.E)

    def _destroy(self, *a):
        self.word_taken = True
        self.master.destroy()