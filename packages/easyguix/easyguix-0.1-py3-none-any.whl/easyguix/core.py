import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, colorchooser
from tkinter import ttk
from PIL import Image, ImageTk
import threading
from tkcalendar import Calendar

try:
    from plyer import notification
except:
    notification = None

try:
    import webview  # for web embedding
except:
    webview = None

class EasyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def text(self, message):
        messagebox.showinfo("Mesaj", message)

    def label(self, message):
        win = tk.Toplevel()
        win.title("Label")
        tk.Label(win, text=message, font=("Arial", 14)).pack(padx=20, pady=20)
        tk.Button(win, text="Kapat", command=win.destroy).pack(pady=10)
        win.mainloop()

    def button(self, message):
        win = tk.Toplevel()
        win.title("Buton")
        def clicked():
            print("Tıklandı!")
            win.destroy()
        tk.Button(win, text=message, font=("Arial", 14), command=clicked).pack(padx=30, pady=30)
        win.mainloop()

    def input(self, prompt):
        return simpledialog.askstring("Girdi", prompt)

    def checkbox(self, message):
        win = tk.Toplevel()
        win.title("Checkbox")
        var = tk.BooleanVar()
        tk.Label(win, text=message, font=("Arial", 12)).pack(pady=10)
        tk.Checkbutton(win, text="Seç", variable=var).pack()
        result = {"secili": None}
        def done():
            result["secili"] = var.get()
            win.destroy()
        tk.Button(win, text="Tamam", command=done).pack(pady=10)
        win.mainloop()
        return result["secili"]

    def slider(self, message, min=0, max=100):
        win = tk.Toplevel()
        win.title("Slider")
        tk.Label(win, text=message, font=("Arial", 12)).pack(pady=10)
        val = tk.IntVar(value=min)
        scale = tk.Scale(win, from_=min, to=max, orient="horizontal", variable=val)
        scale.pack()
        result = {"value": None}
        def done():
            result["value"] = val.get()
            win.destroy()
        tk.Button(win, text="Tamam", command=done).pack(pady=10)
        win.mainloop()
        return result["value"]

    def image(self, filepath):
        win = tk.Toplevel()
        win.title("Resim")
        try:
            image = Image.open(filepath)
            image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(image)
            tk.Label(win, image=photo).pack()
            win.image = photo
        except:
            tk.Label(win, text="Resim yüklenemedi!").pack()
        tk.Button(win, text="Kapat", command=win.destroy).pack(pady=10)
        win.mainloop()

    def notify(self, message, title="EasyGUI"):
        if notification:
            threading.Thread(target=lambda: notification.notify(title=title, message=message, timeout=5)).start()
        else:
            print("[Uyarı] 'plyer' yüklü değil, masaüstü bildirimi gösterilemiyor.")

    def dropdown(self, title, options):
        win = tk.Toplevel()
        win.title(title)
        var = tk.StringVar(value=options[0])
        ttk.Label(win, text=title).pack(pady=5)
        dropdown = ttk.Combobox(win, values=options, textvariable=var, state="readonly")
        dropdown.pack(padx=10, pady=5)
        result = {"secilen": None}
        def done():
            result["secilen"] = var.get()
            win.destroy()
        tk.Button(win, text="Tamam", command=done).pack(pady=10)
        win.mainloop()
        return result["secilen"]

    def multichoice(self, title, options):
        win = tk.Toplevel()
        win.title(title)
        vars = [tk.BooleanVar() for _ in options]
        tk.Label(win, text=title).pack()
        for i, opt in enumerate(options):
            tk.Checkbutton(win, text=opt, variable=vars[i]).pack(anchor='w')
        result = {"secimler": None}
        def done():
            result["secimler"] = [opt for i, opt in enumerate(options) if vars[i].get()]
            win.destroy()
        tk.Button(win, text="Seç", command=done).pack(pady=10)
        win.mainloop()
        return result["secimler"]

    def fileopen(self):
        return filedialog.askopenfilename()

    def filesave(self):
        return filedialog.asksaveasfilename()

    def colorpicker(self):
        color = colorchooser.askcolor()[1]
        return color

    def datepicker(self):
        result = {"tarih": None}
        def get_date():
            result["tarih"] = cal.get_date()
            win.destroy()
        win = tk.Toplevel()
        win.title("Tarih Seç")
        cal = Calendar(win, selectmode='day')
        cal.pack(pady=10)
        tk.Button(win, text="Seç", command=get_date).pack(pady=10)
        win.mainloop()
        return result["tarih"]

    def theme(self, mode):
        if mode == "dark":
            self.root.tk_setPalette(background='#2e2e2e', foreground='white')
        else:
            self.root.tk_setPalette(background='white', foreground='black')

    def web(self, url, title="Web Görüntüleyici"):
        if not webview:
            print("[Uyarı] 'tkwebview2' kurulu değil.")
            return
        webview.create_window(title, url)
        webview.start()
