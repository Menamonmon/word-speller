from gui import MainApp, tk

def main():
    masterWindow = tk.Tk()
    app = MainApp(masterWindow)
    masterWindow.mainloop()

if __name__ == '__main__':
    main()