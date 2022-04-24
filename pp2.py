import tkinter as tk
from tkinter import *
import time
import threading
from PIL import Image, ImageTk

run = True

class Gui:
    def __init__(self):
        self.mainWin = tk.Tk()
        self.mainWin.title('Two Player Snake')
        self.mainWin.config(bg='black')
        self.menu = tk.Frame(self.mainWin, bg="Black", borderwidth=3, relief=tk.GROOVE)
        self.menu.grid(row=2, columnspan=1)
        self.startButton = tk.Button(self.menu, bg='#5F8DE7', bd=5, relief='raised', text='Start',
                                     command=self.multiFuncs)
        self.startButton.grid(row=2, column=1)
        self.quitButton = tk.Button(self.menu, bg='#5F8DE7', bd=5, relief='raised', text='Quit', command=self.quitCall)
        self.quitButton.grid(row=3, column=1)
        self.menuImage = Image.open("Capture.gif")
        self.menuImage = ImageTk.PhotoImage(self.menuImage)
        tk.Label(self.menu, image=self.menuImage, bg='black').grid(row=1, column=1)
        tk.Label(self.menu, text="LIGHT BIKE", bg='black', fg='white', font=('Impact', 20)).grid(row=0, column=1)

        self.mainWin.bind_all('<KeyPress>',self.moving)
        self.mainWin.bind_all('<KeyPress>',self.moving2)
        self.mainWin.bind("<KeyPress-Left>", lambda e: game.L(e))
        self.mainWin.bind("<KeyPress-Right>", lambda e: game.R(e))
        self.mainWin.bind("<KeyPress-Up>", lambda e: game.D(e))
        self.mainWin.bind("<KeyPress-Down>", lambda e: game.U(e))
        self.mainWin.bind("a", lambda a: game.l(a))
        self.mainWin.bind("d", lambda a: game.r(a))
        self.mainWin.bind("s", lambda a: game.d(a))
        self.mainWin.bind("w", lambda a: game.u(a))

        self.x = -1
        self.y = 0

        self.x1 = 1
        self.y1 = 0

    def runboard(self):
        global run
        run = True
        self.w = 400
        self.h = 400
        # creates canvas
        self.canvas = Canvas(self.mainWin, width=self.w, height=self.h, bg='black')

        # creates bounds
        self.rightBound = self.canvas.create_rectangle(self.w - 2, 0, self.w + 3, self.h, fill="orange")
        self.leftBound = self.canvas.create_rectangle(0, 0, 5, self.h, fill="orange")
        self.topBound = self.canvas.create_rectangle(0, 0, self.w, 5, fill="orange")
        self.bottomBound = self.canvas.create_rectangle(0, self.h - 2, self.w, self.h + 3, fill="orange")

        self.box = self.canvas.create_rectangle(self.w-10,self.h // 2, self.w-20, self.h // 2 + 10, fill="#5f8de7",tags='box')
        self.box2 = self.canvas.create_rectangle(10, self.h // 2, 10 + 10, self.h // 2 + 10, fill="orange",tags='box2')
        self.canvas.pack()
        self.canvas.pack_propagate(False)

        self.countdown(3)

        threading.Thread(target=self.movement()).start()
        threading.Thread(target=self.movement2()).start()

    def startCall(self):
        self.menu.grid_forget()

    def quitCall(self):
        self.menu.destroy()
        self.mainWin.destroy()

    def again(self):
        self.menu2.pack_forget()

    def countdown(self,num):
        if num > 0:
            self.canvas.create_text(200,200,font=('Impact', 50),text=str(num),justify='center',tags='timer',fill='white')
            num -= 1
            time.sleep(1)
            self.canvas.delete('timer')
            self.countdown(num)
        elif num == 0:
            self.canvas.create_text(200, 200, font=('Impact', 50), text='Go!', justify='center', tags='timer',fill='white')
            time.sleep(0.5)
            self.canvas.delete('timer')

    def endgame(self):
        global run
        run = False
        self.canvas.delete('tail')
        self.canvas.delete('tail1')
        self.canvas.delete('box')
        self.canvas.delete('box2')
        self.menu2 = tk.Frame(self.canvas,bg='orange',borderwidth=10)
        self.menu2.pack(padx=125,pady=125)
        self.menu.pack_propagate(False)
        self.again = tk.Button(self.menu2,text="Play Again?",width=70,font=('Impact',15),fg='white',relief='raised',bg='orange',command=self.again)
        self.again.pack(padx=10,pady=10)
        self.quit2 = tk.Button(self.menu2,text="Quit",width=70,font=('Impact',15),fg='white',relief='raised',bg='orange',command=self.quitCall)
        self.quit2.pack(padx=10,pady=10)

    def movement(self):
        self.placesBoxHasBeenX = []
        if run:
            self.placesBoxHasBeenX.append(Lx)
            self.placesBoxHasBeenX.append(Lx - 10)
            self.canvas.move(self.box, self.x, self.y)
            self.canvas.after(100, self.movement)
            self.followBox = self.canvas.create_rectangle(Lx, Ly, Lx + 7, Ly + 7, fill="#5f8de7", tags='tail')
            if Lx >= self.w or Ly >= self.h or Lx <= 0 or Ly <= 0 or Lx in self.placesBoxHasBeenX:
                self.endgame()

    def movement2(self):

        if run:
            self.canvas.move(self.box2, self.x1, self.y1)
            self.canvas.after(100, self.movement2)
            Lx1 = self.canvas.coords('box2')[0]
            Ly1 = self.canvas.coords('box2')[1]
            self.followBox1 = self.canvas.create_rectangle(Lx1, Ly1, Lx1 + 10, Ly1 + 10, fill="orange", tags='tail1')

            if Lx1 >= self.w or Ly1 >= self.h or Lx1 <= 0 or Ly1 <= 0:
                self.endgame()

    def moving(self,event):
        if event.keysym == '<KeyPress-Left>':
            self.x = -7
            self.y = 0

        elif event.keysym == '<KeyPress-Right>':
            self.x = 7
            self.y = 0

        elif event.keysym == '<KeyPress-Down>':
            self.x = 0
            self.y = 7

        elif event.keysym == '<KeyPress-Up>':
            self.x = 0
            self.y = -7

    def moving2(self,event):
        if event.keysym == 'a':
            self.x1 = -7
            self.y1 = 0

        elif event.keysym == 'd':
            self.x1 = 7
            self.y1 = 0

        elif event.keysym == 's':
            self.x1 = 0
            self.y1 = 7

        elif event.keysym == 'w':
            self.x1 = 0
            self.y1 = -7

    def L(self, event):
        self.x = -7
        self.y = 0

    def R(self, event):
        self.x = 7
        self.y = 0

    def U(self, event):
        self.x = 0
        self.y = 7

    def D(self, event):
        self.x = 0
        self.y = -7

    def l(self, event):
        self.x1 = -7
        self.y1 = 0

    def r(self, event):
        self.x1 = 7
        self.y1 = 0

    def u(self, event):
        self.x1 = 0
        self.y1 = 7

    def d(self, event):
        self.x1 = 0
        self.y1 = -7

    def multiFuncs(self):
        t1 = threading.Thread(target=self.runboard)
        t2 = threading.Thread(target=self.startCall)
        t2.start()
        t1.start()

    def run(self):
        self.mainWin.mainloop()

if __name__ == "__main__":
    game = Gui()
    game.run()