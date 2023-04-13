import tkinter as tk
import tkinter.messagebox as msgBox
import tkinter.font as tkFont
from tkinter.scrolledtext import ScrolledText

class ShowdownConvUI:
    def __init__(self, root):
        #setting title
        root.title("Showdown Convertor UI")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.ShowdownText= ScrolledText(root, wrap=tk.WORD)
        self.ShowdownText["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=10)
        self.ShowdownText["font"] = ft
        self.ShowdownText["fg"] = "#333333"
        self.ShowdownText.place(x=20,y=25,width=220,height=450)

        self.HGEngineText=ScrolledText(root, wrap=tk.WORD)
        self.HGEngineText["bg"] = "#fcfcfc"
        ft = tkFont.Font(family='Times',size=10)
        self.HGEngineText["font"] = ft
        self.HGEngineText["fg"] = "#333333"
        self.HGEngineText["relief"] = "sunken"
        self.HGEngineText.place(x=360,y=25,width=214,height=450)

        self.WholeTrainer = tk.IntVar()
        TrainerCheck=tk.Checkbutton(root)
        ft = tkFont.Font(family='Times',size=10)
        TrainerCheck["font"] = ft
        TrainerCheck["fg"] = "#333333"
        TrainerCheck["justify"] = "center"
        TrainerCheck["text"] = "Whole Trainer?"
        TrainerCheck.place(x=260,y=150,width=70,height=25)
        TrainerCheck["offvalue"] = "0"
        TrainerCheck["onvalue"] = "1"
        TrainerCheck["variable"] = self.WholeTrainer


        ToHGEngine=tk.Button(root)
        ToHGEngine["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        ToHGEngine["font"] = ft
        ToHGEngine["fg"] = "#000000"
        ToHGEngine["justify"] = "center"
        ToHGEngine["text"] = "To hg-engine >"
        ToHGEngine.place(x=250,y=100,width=100,height=30)
        ToHGEngine["command"] = self.ToHGEngine_command

        ToShowdown=tk.Button(root)
        ToShowdown["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        ToShowdown["font"] = ft
        ToShowdown["fg"] = "#000000"
        ToShowdown["justify"] = "center"
        ToShowdown["text"] = "< To showdown"
        #ToShowdown.place(x=250,y=400,width=100,height=30)
        ToShowdown["command"] = self.ToShowdown_command

    def ToHGEngine_command(self):
        data = self.ShowdownText.get('1.0', tk.END)

        teams = parse(data)
        process(teams)
        output = convert(teams, self.WholeTrainer.get())

        if output == 'No valid Smogon-format mons detected':
            msgBox.showerror("Error", output)        
        else:
            self.HGEngineText.delete('1.0', tk.END)
            self.HGEngineText.insert(tk.INSERT, output)
        

    def ToShowdown_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShowdownConvUI(root)
    root.mainloop()
