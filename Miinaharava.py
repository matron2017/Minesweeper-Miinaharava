#Simon Savukoski

#Miinaharava, jossa voi merkata miinoja oikealla klikkauksella

# ja avata miinoja vasemmalla hiiren painalluksella.

#Pelin voi voittaa avaamalla kaikki ei miinotetut napit.

#Kätetään hyväksi tkinter kirjastoa graafisen esittämisen helpottamiseksi.

#Random-kirjastoa käytetään miinojen määrän satunnaisessa luomisessa.

import random

from tkinter import *

#Funktio, jota käytetään pelin uudellen aloittamisessa


def restart():
    #Otetaan pelin koko ja miinojen määrä Gamesize luokasta
    questions_ui = Gamesize()
    try:
        width, length, maxmines = questions_ui.start()
    except TclError:
        return
    board, width, length = minesweeper(int(width), int(length), int(maxmines))


    questions_ui.destroy()
    ui = Userinterface(board, width, length)
    ui.start()

#Pelinkoko-luokka, jossa määritellään pelin koko ja miinojen määrä

class Gamesize:
    def __init__(self):
        #Tehdään syöttöikkunat, johon annetaan pelikentän koko ja miinojen
        #maksimimäärä.
        self.__mainwindow = Tk()
        self.__mainwindow.title("Minesweeper")
        self.__width = Entry(self.__mainwindow)
        self.__widthlabel = Label(text="Width of board")
        self.__width.grid(row=0, column=2)
        self.__widthlabel.grid(row=0, column=0)
        self.__length = Entry(self.__mainwindow)
        self.__lenghtlabel = Label(text="Lenght of board")
        self.__lenghtlabel.grid(row=2, column=0)
        self.__length.grid(row=2, column=2)
        self.__maxmines = Entry(self.__mainwindow)
        self.__maxmineslabel = Label(text="Maximum amount of mines per line")
        self.__maxmines.grid(row=4, column=2)
        self.__maxmineslabel.grid(row=4, column=0)

        self.__startbutton = Button(text="Start the game by pressing this button", command= self.checkvalues)
        self.__startbutton.grid(row=7, column=2)
        self.__integerlabel = Label(text="Give the numbers as integers, the game won't work otherwise")
        self.__integerlabel.grid(row=7, column=0)

    def start(self):
        self.__mainwindow.mainloop()
        return self.__width.get(), self.__length.get(), self.__maxmines.get()

    def stop(self):
        self.__mainwindow.quit()

    def destroy(self):
        self.__mainwindow.destroy()

    #Tarkistetaan arvot jotka käyttäjä antaa,
    # ja tulostetaan ilmoitus jos arvot eivät sovi pelin toiminnallisuuteen
    def checkvalues(self):
        try:
            if 30 >= int(self.__width.get()) > 0 and 30 >= int(self.__length.get()) > 0 and int(self.__width.get()) * int(self.__length.get()) > int(self.__maxmines.get()) > 1:
                self.stop()
            else:
                self.__warninglabel = Label(
                    text="Values must be given as integers over 0.")
                self.__warninglabel.grid(row=9, column=0)
                self.__otherwarninglabel = Label(text="The maximum size board can be is 30x30. Mines can't fill the whole board and the maximum amount of mines must bet at least 2.")
                self.__otherwarninglabel.grid(row=10, column=0)
        except:
            self.__warninglabel = Label(text="Values must be given as integers over 0.")
            self.__warninglabel.grid(row=9, column=0)
            self.__otherwarninglabel = Label(text="The maximum size board can be is 30x30. Mines can't fill the whole board and the maximum amount of mines must bet at least 2.")
            self.__otherwarninglabel.grid(row=10, column=0)


#Pelipöytä ikkuna, jossa esitetään pelikenttä

class Userinterface:

    def __init__(self, board, width, length, ):

        #Perusmuuttujat, joita käytetään myöhemmin.

        self.__marked = 0

        self.__revealed = 0

        self.__gamebuttons = []

        self.__board = board

        self.__width = width

        self.__length = length

        self.__mines = 0

        #Miinojen määrä laudalla lasketaan tässä.

        for line in range(len(self.__board)):

            for index in range(len(self.__board[line])):

                if self.__board[line][index] == "*":

                    self.__mines += 1

        #Määritetään pääikkuna, johon luodaan pelilauta, missä esiinty pelikenttä.

        #Consoleframe-ikkunassa esiintyy voitto- sekä häviöilmoitukset, sekä

        # napit pelin uudelleen käynnistämiseen tai lopettamiseen.

        self.__mainwindow = Tk()

        self.__mainwindow.title("Minesweeper")

        self.__boardframe = Frame(self.__mainwindow)

        self.__consoleframe = Frame(self.__mainwindow)

        self.__losegamegrame = Frame(self.__mainwindow)

        self.__minecount = Label(self.__consoleframe, text="Mines: {}".format(self.__mines))

        self.__minecount.grid(row=0, column=0)

        self.__exitbutton = Button(self.__consoleframe, text="Exit", command=exit)

        self.__exitbutton.grid(row=0, column=5)

        #Tehdään minesweeperfunktiossa luotu pelilauta graafisesti, käymällä läpi jokainen

        #pelilaudan jäsen, ja määritellään sille painikekomento ja toiminnoit painaessa.

        #Y on pelilaudan rivi ja x sarake.

        for line in range (len(self.__board)):

            self.__boardframe.rowconfigure(line, weight=1)

            self.__gamebuttons.append([])

            for index in range(len(self.__board[line])):

                gamebutton = Button(self.__boardframe, text= "      ")

                gamebutton.grid(row = line, column = index)

                gamebutton.config(command= lambda x = index, y = line:self.reveal(y, x))

                gamebutton.bind("<Button-3>", lambda event, x = index, y = line:self.redmarks(y, x))

                self.__gamebuttons[line].append(gamebutton)

        self.__boardframe.grid(row=1, sticky=EW)

        self.__consoleframe.grid(row = 0)

        #Merkattujen nappuloiden lukumäärä esitetään pelaajalle.

        self.__markcountlabel= Label(self.__consoleframe, text="Marked: {}".format(self.__marked))

        self.__markcountlabel.grid(row = 0, column=7)

        restartbutton = Button(self.__consoleframe, text="Restart", command=self.restart)

        restartbutton.grid(row = 0, column=2)

        self.__restartbutton = restartbutton

    #Punaisten merkkien toiminnallisuus. Tarkastetaan onko nappula jo merkattu, ja sen

    #perusteella värjätään se  joko punaiseksi

    # tai poistetaan värjäys.

    def redmarks(self, line, index):

        # Merkkauksen voi poistaa painamalla oikeaa hiiren näppäintä uudestaan.

        if self.__gamebuttons[line][index].cget("background") == "red":

            self.__gamebuttons[line][index].config(background=self.__mainwindow.cget("background"))

            self.__marked -= 1

            self.__markcountlabel.config(text="Marked: {}".format(self.__marked))


        else:

            self.__gamebuttons[line][index].config(background="red")

            self.__marked += 1

            self.__markcountlabel.config(text="Marked: {}".format(self.__marked))

    #Metodi, jota käytetään pelin lopettamiseen/sulkemiseen.
    def stop(self):

        self.__mainwindow.destroy()

    #Metodi, joka käy läpi 0 paljastuneen painikkeen viereiset paikat, ja avaa ne.

    #Jos vieressä on toinen 0 joka paljastuu, se avaa samalla logiikalla viereiset paikat.

    def revealzero(self,line, index):

        for i in [-1, 1]:

            if line+i >= 0 and line+i <= self.__length-1:

                try:

                    if self.__board[line+i][index] == 0:

                        self.__gamebuttons[line+i][index].config(text="  {}  ".format(0), state='disabled')

                        self.__board[line+i][index] = 'R'

                        self.revealzero(line+i, index)

                    elif self.__board[line+i][index] != "*" and self.__board[line+i][index] != 'R' and self.__board[line+i][index] != 'K':

                        self.__gamebuttons[line+i][index].config(text="  {}  ".format(self.__board[line+i][index]), state="disabled")

                        self.__board[line+i][index] = 'K'

                #Merkataan 0 paikata R ja muut numerot K. Näin helpotetaan

                #avattujen paikkojen tunnistamista.

                except IndexError:

                    pass

            if index+i >= 0 and index+i <= self.__width - 1:

                try:

                    if self.__board[line][index+i] == 0:

                        self.__gamebuttons[line][index+i].config(text="  {}  ".format(0), state='disabled')

                        self.__board[line][index+i] = 'R'

                        self.revealzero(line, index+i)

                    elif self.__board[line][index+i] != "*" and self.__board[line][index+i] != 'R' and self.__board[line][index+i] != 'K':

                        self.__gamebuttons[line][index+i].config(text="  {}  ".format(self.__board[line][index+i]), state= 'disabled')

                        self.__board[line][index+i] = 'K'

                except IndexError:

                    pass

            for j in [-1, 1]:

                if index + i >= 0 and index + i <= self.__width - 1 and line + j >= 0 and line + j <= self.__length - 1:

                    try:

                        if self.__board[line+j][index+i] == 0:

                            self.__gamebuttons[line+j][index+i].config(text="  {}  ".format(0), state='disabled')

                            self.__board[line+j][index+i] = 'R'

                            self.revealzero(line+j, index+i)

                        elif self.__board[line+j][index+i] != "*" and self.__board[line+j][index+i] != 'R' and self.__board[line+j][index+i] != 'K':

                            self.__gamebuttons[line+j][index+i].config(text="  {}  ".format(self.__board[line+j][index+i]), state='disabled')

                            self.__board[line+j][index+i] = 'K'

                    except IndexError:

                        pass

    #Jos pelaaja astuu miinaan, tai voittaa pelin,

    # paljastetaan kaikki miinat kentältä.

    def revealmines(self):

        for line in range(len(self.__board)):

            for index in range(len(self.__board[line])):

                if self.__board[line][index] == "*":

                    self.__gamebuttons[line][index].config(text="  {}  ".format("*"))

    #Jos kaikki paitsi miinaluukut on avattu, pelaajalle paljastetaan miinat,

    # ja tulostetaan voittoilmoitus.

    def wingame(self):

        self.revealmines()

        self.__exitbutton.destroy()

        self.__restartbutton.destroy()

        self.__markcountlabel.destroy()

        self.__minecount.destroy()

        Wongamebutton = Button(self.__consoleframe, text="You have discovered every planted mine. Awesome! Play again?", command=self.restart)

        Wongamebutton.grid(row=0, column=3)

        quitgamebutton = Button(self.__consoleframe, text="Quit playing?", command= self.stop)

        quitgamebutton.grid(row=0, column=7)

        for line in self.__gamebuttons:

            for button in line:

                button.configure(state='disable')

    #Metodi, jota käytetään  luukkujen paljastamiseen.

    #Jos luukun alta paljastuu miina, paljastetaan muut miinat

    # ja tulostetaan häviöilmoitus.

    def reveal(self, line, index):

        number = self.__board[line][index]

        if number == "*":

            self.revealmines()

            self.__exitbutton.destroy()

            self.__restartbutton.destroy()

            self.__markcountlabel.destroy()

            self.__minecount.destroy()

            Lostgamebutton = Button(self.__consoleframe, text="BOOM! You stepped into a mine. Restart game?", command=self.restart)

            quitgamebutton = Button(self.__consoleframe, text="Quit playing?", command=self.stop)

            quitgamebutton.grid(row=0, column=7)

            Lostgamebutton.grid(row=0, column=3)

            for line in self.__gamebuttons:

                for button in line:

                    button.configure(state='disable')

        #Jos luukun alta paljastuu 0, paljastetaan viereiset luukut,

        # ja tarkistetaan, onko luukuissa

        # jäljellä enää miinoja.

        #Jos kaikki ei-miinoitetut luukut on avattu, pelaaja voittaa.

        elif number == 0:

            self.__gamebuttons[line][index].config(text="  {}  ".format(number), state='disabled')

            self.__board[line][index] = 'R'

            self.revealzero(line, index)

            for line in range(len(self.__board)):

                for index in range(len(self.__board[line])):

                    if self.__board[line][index] == 'K' or self.__board[line][index] == 'R':

                        self.__revealed += 1

            if int(self.__width) * int(self.__length) - int(self.__mines) == int(self.__revealed):

                self.wingame()

            else:

                self.__revealed = 0

        #Jos numero on muu kuin 0, paljastetaan vain kyisenen luukku.

        #Tarkastetaan samalla lailla kuin aijemmin, onko pelaaja voittanut.

        else:

            self.__gamebuttons[line][index].config(text="  {}  ".format(number), state='disabled')

            self.__board[line][index] = 'K'

            for line in range(len(self.__board)):

                for index in range(len(self.__board[line])):

                    if self.__board[line][index] == 'K' or self.__board[line][index] == 'R':

                        self.__revealed += 1

            if int(self.__width) * int(self.__length) - int(self.__mines) == int(self.__revealed):

                self.wingame()

            else:

                self.__revealed = 0

    #Metodi pelin käynnistämiseen.

    def start(self):

        self.__mainwindow.mainloop()

    #Metodi pelin uudelleenkäynnistämiseen.


    def restart(self):

        self.__mainwindow.destroy()

        restart()

#Funktio, jossa määritellään pelikentän koko.

#Myös miinojen määrä määritellään satunnaisesti

# tässä funktiossa.

def minesweeper(width, length, maxmines):

    board = []
    minmines = 1


    totalmines = 0

    #Luodaan pelikenttä, jossa i on korkeus ja j leveys.

    for i in range(length):

        board.append([])

        for j in range(width):

            board[i].append(0)

    #Määritetään miinojen määrä, ja lisätään ne pelikentälle.

    #

    for row in board:

        minesperline = random.randint(minmines, maxmines)

        totalmines += minesperline

        for i in range (0, minesperline):

            index = random.randint(0, width-1)

            if "*" != row[index]:

                row[index] = "*"

                minesperline -= 1

            if minesperline == 0:

                break

    #Käydään läpi ei-miinoitetut paikat,

    #ja merkataan ne niiden ympärille olevien

    # miinojen yhteenlasketulla lukumäärällä

    #yksi kerrallaan.

    for y in range(0, length):

        for x in range(0, width):

            if board[y][x] == "*":

                continue

            else:

                minesaround = 0

                for j in range(-1,2,1):

                    if y+j < 0 or y+j > length-1:

                        continue

                    else:

                        for i in range(-1, 2, 1):

                            if x+i < 0 or x+i > width-1:

                                continue

                            else:

                                if board[y+j][x+i] == "*":

                                     minesaround += 1

                board[y][x] = minesaround

    return board, width, length

    #Pääfunktio, jossa luodaan pelikenttä ja

    #otetaan se käytöön.

def main():
    #Otetaan pelin koko ja miinojen määrä Gamesize luokasta
    questions_ui = Gamesize()
    try:
        width, length, maxmines = questions_ui.start()
    except TclError:
        return
    questions_ui.destroy()

    board, width, length = minesweeper(int(width), int(length), int(maxmines),)
    ui = Userinterface(board, width, length)

    #Käynnistetään käyttöliittymä

    ui.start()

main()



