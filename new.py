import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import IntVar
from tkinter import Tk
from tkinter import Frame
from tkinter import Label
from tkinter import Button
from tkinter import Checkbutton
from tkinter import Entry
from tkinter import Canvas
from tkinter import Scrollbar
from tkinter import Text
from tkinter import ttk

import tkinter.scrolledtext as st

# SET UP WINDOW
root = Tk()

# GLOBAL VARIABLES
global currentRow
currentRow = 0
global skipVar

global numInfo
global idInfo
global wordInfo
global gameDescInfo
global gameDescTxt
global searchInput

# FUNCTIONS
def prev_row():
    global currentRow

    keepSkipping = True
    skipNum = 0
    count = 0
    wantSkip = skipVar.get()
    if wantSkip == 1:
        while keepSkipping == True:
            count += 1
            if df.iloc[currentRow + count].changed_word != "nan":
                skipNum+=1
            else:
                keepSkipping = False
    currentRow = currentRow - 1 - skipNum

    destroy_info()
    update_info()

def next_row():
    global currentRow

    keepSkipping = True
    skipNum = 0
    count = 0
    wantSkip = skipVar.get()
    if wantSkip == 1:
        while keepSkipping == True:
            count += 1
            if df.iloc[currentRow + count].changed_word != "nan":
                skipNum+=1
            else:
                keepSkipping = False
    currentRow = currentRow + 1 + skipNum    

    destroy_info()
    update_info()

def load():
    global df
    df = pd.read_csv("all_words_coded.csv", index_col ="index")

def destroy_info():
    global numInfo
    global idInfo
    global wordInfo
    global gameDescInfo
    global gameDescTxt
    global searchInput
    numInfo.destroy()
    idInfo.destroy()
    wordInfo.destroy()
    gameDescInfo.destroy()
    gameDescTxt.delete('1.0', tk.END)
    searchInput.delete(0, 'end')

def update_info():
    global numInfo
    global idInfo
    global wordInfo
    global gameDescInfo
    global gameDescTxt
    global searchInput
    numInfo = Label(frame1, text=df.iloc[currentRow].game_num)
    numInfo.place(x=10, y=35)
    numInfo.configure(background = "black", foreground="white")
    idInfo = Label(frame1, text=df.iloc[currentRow].id)
    idInfo.place(x=100, y=35)
    idInfo.configure(background = "black", foreground="white")    
    wordInfo = Label(frame1, text=df.iloc[currentRow].changed_word)
    wordInfo.place(x=200, y=35)
    wordInfo.configure(background = "black", foreground="white")
    gameDescInfo = Label(frame1, text=df.iloc[currentRow].game_name)
    gameDescInfo.place(x=10, y=130)
    gameDescInfo.configure(background = "black", foreground="white")
    gameDescTxt.insert(1.0, "{}".format(df.iloc[currentRow].game_description))
    searchInput.insert(0, df.iloc[currentRow].changed_word)
    highlight_word()

def highlight_word():
    global start_pos
    start_pos = 0
    global end_pos
    end_pos = ''
    gameDescTxt.delete('1.0', tk.END)
    gameDescTxt.insert(1.0, df.iloc[currentRow].game_description, 'warning')
    h_word = df.iloc[currentRow].word.replace(" ","_")
    start_pos = gameDescTxt.search(h_word, '1.0', stopindex=tk.END)
    #in case the word is capitalized b/c first word in sentence
    if not start_pos:
        start_pos = gameDescTxt.search(h_word.capitalize(), '1.0', stopindex=tk.END)
    #in case the word is all uppercase letters   
    if not start_pos:
        start_pos = gameDescTxt.search(h_word.upper(), '1.0', stopindex=tk.END)
    #in case the word has hyphens   
    if not start_pos:
        start_pos = gameDescTxt.search(h_word.replace(" ","-"), '1.0', stopindex=tk.END)
    if start_pos:
        if end_pos:
            gameDescTxt.tag_remove('highlight', start_pos, end_pos)
        end_pos = '{}+{}c'.format(start_pos, len(h_word))            
        gameDescTxt.tag_add('highlight', start_pos, end_pos)
        gameDescTxt.tag_config('highlight', background='yellow', foreground = "black")

def search_word():
    global checkList
    global checkBoxList
    global checkBoxes
    global labelList
    search_term = searchInput.get()
    searchCanvas = Canvas(frame2, bg='green', width=420, height=800)
    searchCanvas.place(x=10,y=100)
    checkList = st.ScrolledText(searchCanvas, width=50, height=50, wrap="none")
    checkList.pack() 
    matchDf = df['changed_word'][df['changed_word'].str.contains(search_term, na=False)].unique()
    matchList = []
    for i in range(len(matchDf)):
        matchList.append(matchDf[i])
    checkBoxList = []
    checkBoxes = []
    labelList = []
    for i in range(len(matchList)):
        labelList.append(Label(checkList, text=matchList[i]))
        labelList[i].description = matchList[i]
        labelList[i].config(background = "grey2", foreground= 'white', font = ('Arial', 10, 'bold'))
        checkBoxList.append(IntVar())
        checkBoxes.append(Checkbutton(checkList, text='', variable=checkBoxList[i]))
        checkList.window_create("end", window=checkBoxes[i])
        checkList.window_create("end", window=labelList[i])
        checkList.insert("end", "\n")



###################################################################################################
###################################################################################################

# SET WINDOW SIZE
rootWidth = 1800
rootHeight = 1000
root.geometry('{}x{}+25+25'.format(rootWidth, rootHeight))
root.resizable(width=False, height=False)

# SET FRAME DIMENSIONS
frame1 = Frame(root, width=450, height=1000)
frame1.place(x=0,y=0)
frame1.config(bg="grey22")
frame2 = Frame(root, width=450, height=1000)
frame2.place(x=450,y=0)
frame2.config(bg="grey44")
frame3 = Frame(root, width=450, height=1000)
frame3.place(x=900,y=0)
frame3.config(bg="grey66")
frame4 = Frame(root, width=450, height=1000)
frame4.place(x=1350,y=0)
frame4.config(bg="grey88")

# FRAME 1
numTitle = Label(frame1, text="Game number:")
numTitle.place(x=10, y=10)
numTitle.configure(background = "black", foreground="white")
numInfo = Label(frame1, text="NA")
numInfo.place(x=10, y=35)
numInfo.configure(background = "black", foreground="white")
idTitle = Label(frame1, text="Game ID:")
idTitle.place(x=100, y=10)
idTitle.configure(background = "black", foreground="white")
idInfo = Label(frame1, text="NA")
idInfo.place(x=100, y=35)
idInfo.configure(background = "black", foreground="white")
wordTitle = Label(frame1, text="Word:")
wordTitle.place(x=200, y=10)
wordTitle.configure(background = "black", foreground="white")
wordInfo = Label(frame1, text="NA")
wordInfo.place(x=200, y=35)
wordInfo.configure(background = "black", foreground="white")
prevBtn= Button(frame1, text="Previous", command=prev_row, padx=2, pady=2)
prevBtn.place(x=10,y=65)
prevBtn.configure(background = "black", foreground="white")
nextBtn = Button(frame1, text="Next", command=next_row, padx=2, pady=2)
nextBtn.place(x=85,y=65)
nextBtn.configure(background = "black", foreground="white")

skipVar = IntVar()
skipBtn = Checkbutton(frame1, text='', variable=skipVar)
# skipBtn.configure(background = "black", foreground="white")
skipBtn.place(x=145,y=65)

navTitle = Label(frame1, text="Check to skip changed words")
navTitle.place(x=180, y=65)
navTitle.configure(background = "black", foreground="white")
gameDescTitle = Label(frame1, text="Game:")
gameDescTitle.place(x=10, y=100)
gameDescTitle.configure(background = "black", foreground="white")
gameDescInfo = Label(frame1, text="NA")
gameDescInfo.place(x=10, y=130)
gameDescInfo.configure(background = "black", foreground="white")
gameDescTxt = st.ScrolledText(frame1, undo=True, width=50, height=25, wrap="word", bg = "black", fg = "white")
gameDescTxt.place(x=10, y=160)
gameDescTxt.insert(1.0, "DESCRIPTION GOES HERE..")

# FRAME 2
searchBtn = Button(frame2, text="Search", command=search_word, padx=2, pady=2)
searchBtn.place(x=10,y=40)
searchBtn.configure(background = "black", foreground="white")
searchInput = Entry(frame2, width=42, justify = "left", font=('Consolas', 10, 'bold'))
searchInput.place(x=75,y=42)

# EXECUTE ON STARTUP
load()
update_info()

# MAIN LOOP
root.mainloop()