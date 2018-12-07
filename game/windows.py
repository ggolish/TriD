
import tkinter as tk
import threading

# Centers a window
def center(window):
    window.root.withdraw()
    window.root.update_idletasks()
    x = (window.root.winfo_screenwidth() - window.root.winfo_reqwidth()) // 2
    y = (window.root.winfo_screenheight() - window.root.winfo_reqheight()) // 2
    window.root.geometry("+{}+{}".format(x, y))
    window.root.deiconify()

class NameEntryWindow():

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TriD Chess: Connect")

        self.row1 = tk.Frame(self.root)
        self.name_label = tk.Label(self.row1, text="Username:")
        self.name_entry = tk.Entry(self.row1, width=40)
        self.row2 = tk.Frame(self.root)
        self.connect_button = tk.Button(self.row2, text="Connect", command=self.connect_callback)
        self.cancel_button = tk.Button(self.row2, text="Cancel", command=self.root.quit)
        
        self.row1.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.name_label.pack(side=tk.LEFT)
        self.name_entry.pack(side=tk.RIGHT, fill=tk.X, expand=tk.YES)
        self.row2.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.connect_button.pack(side=tk.LEFT, padx=5)
        self.cancel_button.pack(side=tk.LEFT)
        center(self)
        
        self.name = None

    def get_name(self):
        self.root.mainloop()
        self.root.destroy()
        return self.name

    def connect_callback(self):
        s = self.name_entry.get()
        if len(s) > 0:
            self.name = s.strip()
            self.root.quit()

class OpponentChooseWindow():

    def __init__(self, update_callback):
        self.root = tk.Tk()
        self.root.title("TriD Chess: Choose Opponent")

        row1 = tk.Frame(self.root)
        self.lb = tk.Listbox(row1, width=60, height=20)
        row2 = tk.Frame(self.root)
        choose_button = tk.Button(row2, text="Choose", command=self.choose_callback)
        cancel_button = tk.Button(row2, text="Cancel", command=self.root.quit)
        self.request_frame = tk.Frame(self.root)
        self.request_var = tk.StringVar()
        request_label = tk.Label(self.request_frame, textvariable=self.request_var)
        accept_button = tk.Button(self.request_frame, text="Accept", command=self.accept_request)
        deny_button = tk.Button(self.request_frame, text="Deny", command=self.deny_request)

        row1.grid(row=0, padx=5, pady=5)
        self.lb.grid(row=0)
        row2.grid(row=2, padx=5, pady=5)
        choose_button.grid(row=0, column=0, padx=5)
        cancel_button.grid(row=0, column=1)
        self.request_frame.grid(row=1, padx=5, pady=5, sticky="W")
        request_label.grid(row=0, sticky="W")
        accept_button.grid(row=0, column=2, sticky="E", padx=5)
        deny_button.grid(row=0, column=3, sticky="E", padx=5)
        self.request_frame.grid_remove()
        center(self)

        self.opponent = None
        self.type = None
        self.update_callback = update_callback
        self.finished = False
        self.update()

    def choose_opponent(self):
        self.finished = False
        self.update()
        self.root.mainloop()
        return self.opponent, self.type

    def choose_callback(self):
        self.finished = True
        selection = self.lb.curselection()
        if selection:
            self.opponent = self.lb.get(selection[0])
            self.type = "request"
            self.root.quit()
        else:
            self.finished = False
            self.update()

    def destroy(self):
        self.finished = True
        self.root.destroy()

    def update(self):
        if self.finished: return
        response = self.update_callback()
        if response["type"] == "all":
            self.update_lb(response["users"])
        elif response["type"] == "request":
            self.opponent = response["opponent"]
            self.request_var.set("Player {} wants to play you.".format(response["opponent"]))
            self.request_frame.grid()
        self.update_timer = threading.Timer(1.0, self.update)
        self.update_timer.start()

    def update_lb(self, users):
        current = self.lb.curselection()
        self.lb.delete(0, tk.END)
        for o in users:
            self.lb.insert(tk.END, o)
        if current and current[0] < self.lb.size():
            self.lb.activate(current[0])
            self.lb.selection_set(current[0])

    def accept_request(self):
        self.type = "accept"
        self.root.quit()

    def deny_request(self):
        self.type = "deny"
        self.root.quit()

