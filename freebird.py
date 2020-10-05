import numpy as np
import pandas as pd
from tkinter import *
import tkinter.scrolledtext as scrolledtext
from tkinter import ttk
import nltk
from nltk.corpus import wordnet as wn

global search_term
global matches
global match_listbox
global new_word
global num_label
global id_label
global word_label
global stem_word_label
global changed_word_label
global game_name_label
global remark_label

global desc_text
global target
global word_list
global names_for_list
global all_matches_list

##SET SOME VALUES
global num
num = 0
global quote
quote="<-- Search for a word to get a list of matches"
global names_for_list
names_for_list = []
global number_of_buttons
number_of_buttons = 15
global syn_butts
syn_butts = []
global syn_labs
syn_labs = []
global vert_offset
vert_offset = 5
global matches
matches = []
global bot_text
game_desc = "Game description goes here.."
global start_pos
start_pos = 0
global end_pos
end_pos = ''
global end_pos2
end_pos2 = ''
global skip_var

def next_button():
    global num
    global all_matches_list
    global check1_t1
    global c
    global scrollbar
    global checklist


    #print("Num is: {}".format(num))

    keep_skipping = True
    skip_num = 0
    count = 0
    want_skip = skip_var.get()

    if want_skip == 1:
        while keep_skipping == True:

            count += 1

            #print("Next word is: {}".format(df.iloc[num + count].word))
            
            if df.iloc[num + count].changed_word != "nan":
                skip_num+=1
                #print("Changed word = {}".format(df.iloc[num + count].changed_word))
                #print("skipping...")
            else:
                #print("Changed word = {}".format(df.iloc[num + count].changed_word))
                #print("stopping...")
                keep_skipping = False
    
    num = num + 1 + skip_num

    #print("Num + skipnum is: {}".format(num))
    
    change_info()
    find_syns(df.iloc[num].word)
    show_desc(df.iloc[num].id, df.iloc[num].word)

    for check in check1_t1: 
        check.destroy()

    for label in labelList:
        label.destroy()


    c.destroy()
    scrollbar.destroy()
    checklist.destroy()
    
    show_checks(df.iloc[num].stemmed_word)

def prev_button():
    global num
    want_skip = skip_var.get()

    
    #print("Num is: {}".format(num))

    keep_skipping = True
    skip_num = 0
    count = 0

    if want_skip == 1:
        while keep_skipping == True:

            count += 1

            #print("Next word is: {}".format(df.iloc[num - count].word))
          
            if df.iloc[num - count].changed_word != "nan":
                skip_num+=1
                #print("Changed word = {}".format(df.iloc[num - count].changed_word))
                #print("skipping...")
            else:
                #print("Changed word = {}".format(df.iloc[num - count].changed_word))
                #print("stopping...")
                keep_skipping = False

    
    
    num = num - 1 - skip_num

    #print("Num ({}) + skipnum({}) is: {}".format(num,skip_num,num-skip_num))
    
    change_info()
    find_syns(df.iloc[num].word)
    show_desc(df.iloc[num].id, df.iloc[num].word)

    for check in check1_t1: 
        check.destroy()
        
    for label in labelList:
        label.destroy()
    
    show_checks(df.iloc[num].stemmed_word)

def search_word():
    global search_term
    global matches
    global names_for_list
    global match_listbox
    global new_word

    search_term = search_input.get()

    find_syns(search_term)

    for check in check1_t1: 
        check.destroy()
        
    for label in labelList:
        label.destroy()

    
    show_checks(search_term)

def show_checks(target_word):
    global checkboxList
    global check1_t1
    global all_matches_list
    global labelList
    global c
    global scrollbar
    global checklist
    global skip_var

    want_skip = skip_var.get()

    
    all_matches_list = []

    if want_skip == 1:

        all_matches_list = df.loc[df['stemmed_word'].str.contains(target_word) & df['changed_word'].str.contains("nan"), ['game_num','id','word','game_name','changed_word']].values.tolist()
        print(all_matches_list)

    else:
        all_matches_list = df.loc[df['stemmed_word'].str.contains(target_word), ['game_num','id','word','game_name','changed_word']].values.tolist()
        #all_matches_list = df[df['stemmed_word'].str.contains(target_word), ['game_num','id','word','game_name','changed_word']].tolist()
        print(all_matches_list)

    new_list = []
    
    checkboxList = []
    labelList = []

    c = Canvas(frame1, bg='grey', width=450, height=850)
    c.place(x=10,y=10)

    scrollbar = Scrollbar(c)
    scrollbar.pack(side=RIGHT, fill=Y)

    checklist = Text(c, width=58, height=40, wrap="none")
    checklist.pack()    

    check1_t1 = []

    for line in all_matches_list:
        temp = map(str, line)
        new_list.append(' - '.join(temp))

    for i in range(len(new_list)):
        labelList.append(Label(checklist, text=new_list[i]))
        labelList[i].description = new_list[i]
        labelList[i].config(background = "grey2", foreground= 'white', font = ('Arial', 10, 'bold'))
        labelList[i].bind("<Enter>", on_enter)
        labelList[i].bind("<Leave>", on_leave)
        checkboxList.append(IntVar())
        check1_t1.append(Checkbutton(checklist, text='', variable=checkboxList[i]))
        checklist.window_create("end", window=check1_t1[i])
        #checklist.insert("end", "\n")
        checklist.window_create("end", window=labelList[i])
        checklist.insert("end", "\n")

    for x in check1_t1:
        x.select()    

def show_desc(game_id, target):
    global desc_text
    global start_pos
    global end_pos
    global game_desc
    
    game_desc = df['game_description'][df['id'] == game_id].iloc[0]

    #target = str(target)
    #target.replace('_', ' ', regex=True, inplace=True)
    target.replace('_', ' ')
    
    desc_text.delete('1.0', END)
    desc_text.insert(1.0, game_desc)
    
    start_pos = desc_text.search(target, '1.0', stopindex=END)
    #in case the word is capitalized b/c first word in sentence
    if not start_pos:
        start_pos = desc_text.search(target.capitalize(), '1.0', stopindex=END)
    #in case the word is all uppercase letters   
    if not start_pos:
        start_pos = desc_text.search(target.upper(), '1.0', stopindex=END)
    #in case the word has hyphens   
    if not start_pos:
        start_pos = desc_text.search(target.replace(" ","-"), '1.0', stopindex=END)
    if start_pos:
        if end_pos:
            desc_text.tag_remove('highlight', start_pos, end_pos)
        end_pos = '{}+{}c'.format(start_pos, len(target))            
        desc_text.tag_add('highlight', start_pos, end_pos)
        desc_text.tag_config('highlight', background='yellow', foreground = "black")

def find_syns(term):
    global syn_butts
    global syn_labs
    
    term_syns = wn.synsets(term)    
    try:
        for i in range(len(syn_butts)):
            syn_butts[i].destroy()
            syn_labs[i].destroy()
    except Exception as e:
        print(e)
    syn_butts = []       
    syn_labs = []
    for i in range(len(term_syns)):
        try:
            syn_butts.append(Button(frame4, text=term_syns[i].lemmas()[0].name()))
            term_def = str(term_syns[i].definition())
            syn_labs.append(Label(frame4, text=term_def))
        except Exception as e:
            print(e)
    vert_offset=-20
    for i in range(len(term_syns)):
        vert_offset += 50
        syn_butts[i].place(x=5, y=vert_offset)
        syn_butts[i].configure(background = "red4", foreground="white")
        syn_labs[i].place(x=5, y=vert_offset+25)
        syn_labs[i].configure(background = "red4", foreground="white")

def change_info():
    global num_label
    global id_label
    global word_label
    global game_name_label
    global stem_word_label
    global changed_word_label
    global change_to_input
    global remark_label
    
    num_label.destroy()
    id_label.destroy()
    word_label.destroy()
    stem_word_label.destroy()
    game_name_label.destroy()
    changed_word_label.destroy()
    remark_label.destroy()
    
    num_label = Label(topFrame, text=df.iloc[num].game_num)
    num_label.place(x=10, y=35)
    num_label.configure(background = "black", foreground="white")
    
    id_label = Label(topFrame, text=df.iloc[num].id)
    id_label.place(x=125, y=35)
    id_label.configure(background = "black", foreground="white")    

    word_label = Label(topFrame, text=df.iloc[num].word)
    word_label.place(x=200, y=35)
    word_label.configure(background = "black", foreground="white")    

    stem_word_label = Label(topFrame, text=df.iloc[num].stemmed_word)
    stem_word_label.place(x=350, y=35)
    stem_word_label.configure(background = "black", foreground="white")
       
    changed_word_label = Label(topFrame, text=df.iloc[num].changed_word)
    changed_word_label.place(x=500, y=35)
    changed_word_label.configure(background = "black", foreground="white")

    remark_label = Label(topFrame, text=df.iloc[num].remark)
    remark_label.place(x=500, y=85)
    remark_label.configure(background = "black", foreground="white")
    
    game_name_label = Label(topFrame, text=df.iloc[num].game_name)
    game_name_label.place(x=150, y=85)
    game_name_label.configure(background = "black", foreground="white")
   
    change_to_input.delete(0, END)
    change_to_input.insert(0, "{}_".format(df.iloc[num].stemmed_word))

def on_enter(event):
    global desc_text2
    global start_pos2
    global end_pos2
    
    description = getattr(event.widget, "description", "")
    game_id = description.split(" - ")[1]
    target2 = description.split(" - ")[2]

    desc_text2.tag_config('warning', background="black", foreground="white")

    
    description = str(df['game_description'][df['id'] == int(game_id)].iloc[0])   
    desc_text2.delete('1.0', END)
    desc_text2.insert(1.0, description, 'warning')

    
        
    start_pos2 = desc_text2.search(target2, '1.0', stopindex=END)
    #in case the word is capitalized b/c first word in sentence
    if not start_pos2:
        start_pos2 = desc_text2.search(target2.capitalize(), '1.0', stopindex=END)
    #in case the word is all uppercase letters   
    if not start_pos:
        start_pos2 = desc_text2.search(target2.upper(), '1.0', stopindex=END)
    #in case the word has hyphens   
    if not start_pos2:
        start_pos2 = desc_text2.search(target2.replace(" ","-"), '1.0', stopindex=END)
    if start_pos2:
        if end_pos2:
            desc_text2.tag_remove('highlight', start_pos2, end_pos2)
        end_pos2 = '{}+{}c'.format(start_pos2, len(target2))            
        desc_text2.tag_add('highlight', start_pos2, end_pos2)
        desc_text2.tag_config('highlight', background='yellow', foreground = "black")

def on_leave(enter): 
    desc_text2.delete('1.0', END)

def set_remark(remark_type):
    
    global all_selected_matches_list
    all_selected_matches_list = []
    
    finalValue = []
    for x in checkboxList:
        finalValue.append(x.get())

    for i in range(len(finalValue)):
        #print(finalValue[i])
        if finalValue[i] == 1:
            all_selected_matches_list.append(all_matches_list[i])

    #print(all_selected_matches_list)

    new_word = change_to_input.get()
        
    for i in range(len(all_selected_matches_list)):
        game_number = all_selected_matches_list[i][1]
        old_word = all_selected_matches_list[i][2]   
        #print("changing old word: {} in game #{} to new word: {}".format(old_word, game_number, new_word))
        #word = df[(df.word.str.contains(old_word)) & (df.id == game_number)].word
        #print(word.loc[0])
        df['changed_word'][(df.word.str.contains(old_word)) & (df.id == game_number)] = new_word
        
        #print(df[df.id == all_selected_matches_list[i][1]])

    remark = remark_type
        
    for i in range(len(all_selected_matches_list)):
        game_number = all_selected_matches_list[i][1]
        old_word = all_selected_matches_list[i][2]   
        #print("changing old word: {} in game #{} to new word: {}".format(old_word, game_number, remark))
        word = df[(df.word.str.contains(old_word)) & (df.id == game_number)].word
        #print(word.loc[0])
        df['remark'][(df.word.str.contains(old_word)) & (df.id == game_number)] = remark
        
        #print(df[df.id == all_selected_matches_list[i][1]])

    write_to_file()
    change_info()

def check_all():
    for x in check1_t1:
        x.select()

def uncheck_all():
    for i in check1_t1:
        i.deselect()

def add_word():
    global df
    global ps
    add_word_word = add_word_input.get()

    last_entry = len(df.num)
    
    new_row = {'num':last_entry+1,
               'game_num':df.iloc[num].game_num,
               'id':df.iloc[num].id,
               'word':add_word_word,
               'leo':df.iloc[num].leo,
               'andrew':df.iloc[num].andrew,
               'thijs':df.iloc[num].thijs,
               'picked':df.iloc[num].picked,
               'final':df.iloc[num].final,
               'remark':"nan",
               'game_name':df.iloc[num].game_name,
               'game_description':df.iloc[num].game_description,
               'changed_word':"nan",
               'stemmed_word':ps.stem(add_word_word)}

    df = df.append(new_row, ignore_index=True)

def jump_to_num():
    global num
    global all_matches_list
    global check1_t1
    
    game_to_jump = int(jump_input.get())
    df_temp = df[df['game_num'] == game_to_jump].index.values
    num =  df_temp[0]  
    change_info()
    find_syns(df.iloc[num].word)
    show_desc(df.iloc[num].id, df.iloc[num].word)

    for check in check1_t1: 
        check.destroy()

    for label in labelList:
        label.destroy()
        
    show_checks(df.iloc[num].stemmed_word)

def load_from_file():
    global df
    global ps
  
    
    df = pd.read_csv("C:/Users/gaoan/Code/Freebird/{}.csv".format(input_file_input.get()), index_col ="index")

    #print(df.head)
    print(len(df))
    
    ## SET UP DATAFRAME
    pd.set_option('display.width', 800)
    pd.options.display.max_columns = 50
    ##df = pd.read_csv("data.csv", index_col ="index")
    df = df.astype({"num":int,"game_num": int, "id": int, "word": str, "leo": int, "andrew": int, "thijs": int,
                    "picked": int, "final": int, "remark": str, "game_name": str, "game_description": str})
    #df = df[df['word'].str.islower()]
    #df = df[df['remark'] == "nan"]
    df = df[df['final'] == 1]
    df['word'] = pd.Categorical(df['word'])
    #word_list = df['word'].cat.categories
    df['word'] = df['word'].astype(str)
    #df['changed_word'] = "NA"
    df['changed_word'] = df['changed_word'].astype(str)

    ## dont know why but this throws an error on other computers
    #df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    df.replace(' ', '_', regex=True,inplace=True)
    df['game_description'].replace('_', ' ', regex=True,inplace=True)
    
    # RESET THE INDEX
    df = df.reset_index(drop=True)

    #print(df.head)

    # SET UP STEMMED WORDS COLUMN
    from nltk.stem import PorterStemmer
    ps = PorterStemmer() 
    word_list = df['word'].tolist()
    for i in range(len(word_list)): 
        word_list[i] = ps.stem(word_list[i])
    df['stemmed_word'] = word_list

    #print(df.head)

    find_syns(df.iloc[num].word)
    show_checks(df.iloc[num].word)
    show_desc(df.iloc[num].id, df.iloc[num].word)

def write_to_file():
    
    df.to_csv('C:/Users/gaoan/Code/Freebird/data_output.csv', index=True, index_label="index")

def write_to_new_file():
    df.to_csv('C:/Users/gaoan/Code/Freebird/{}.csv'.format(output_file_input.get()), index=True, index_label="index")    

# SET UP WINDOW
root = Tk()
#size of the window
rootWidth = 1800
rootHeight = 1000
root.geometry('{}x{}+50+50'.format(rootWidth, rootHeight))
root.resizable(width=False, height=False)

## SET FRAME DIMENSIONS
topFrame = Frame(root, width=1800, height=250)
topFrame.place(x=0,y=0)

frame1 = Frame(root, width=500, height=700)
frame1.place(x=0,y=250)

frame2 = Frame(root, width=400, height=700)
frame2.place(x=500,y=250)

frame3 = Frame(root, width=475, height=700)
frame3.place(x=900,y=250)

frame4 = Frame(root, width=425, height=700)
frame4.place(x=1375,y=250)

botFrame = Frame(root, width=1800, height=50)
botFrame.place(x=0,y=950)

## CHANGE FRAME COLORS
topFrame.config(bg="grey4")
frame1.config(bg="white")
frame2.config(bg="red")
frame3.config(bg="white")
frame4.config(bg="red")
botFrame.config(bg="grey4")

## TOP FRAME
col_label_num = Label(topFrame, text="Game number:")
col_label_num.place(x=10, y=10)
col_label_num.configure(background = "black", foreground="white")

num_label = Label(topFrame, text="X")
num_label.place(x=10, y=35)
num_label.configure(background = "black", foreground="white")

col_label_id = Label(topFrame, text="Game ID:")
col_label_id.place(x=100, y=10)
col_label_id.configure(background = "black", foreground="white")

id_label = Label(topFrame, text="X")
id_label.place(x=100, y=35)
id_label.configure(background = "black", foreground="white")

col_label_word = Label(topFrame, text="Word:")
col_label_word.place(x=200, y=10)
col_label_word.configure(background = "black", foreground="white")

word_label = Label(topFrame, text="X")
word_label.place(x=200, y=35)
word_label.configure(background = "black", foreground="white")

col_label_stem_word = Label(topFrame, text="Stemmed Word:")
col_label_stem_word.place(x=350, y=10)
col_label_stem_word.configure(background = "black", foreground="white")

stem_word_label = Label(topFrame, text="X")
stem_word_label.place(x=350, y=35)
stem_word_label.configure(background = "black", foreground="white")

col_label_changed_word = Label(topFrame, text="Changed Word:")
col_label_changed_word.place(x=500, y=10)
col_label_changed_word.configure(background = "black", foreground="white")

changed_word_label = Label(topFrame, text="X")
changed_word_label.place(x=500, y=35)
changed_word_label.configure(background = "black", foreground="white")

col_label_game_name = Label(topFrame, text="Game name:")
col_label_game_name.place(x=150, y=60)
col_label_game_name.configure(background = "black", foreground="white")

game_name_label = Label(topFrame, text="X")
game_name_label.place(x=150, y=85)
game_name_label.configure(background = "black", foreground="white")


col_label_remark = Label(topFrame, text="Remark:")
col_label_remark.place(x=500, y=60)
col_label_remark.configure(background = "black", foreground="white")

remark_label = Label(topFrame, text="X")
remark_label.place(x=500, y=85)
remark_label.configure(background = "black", foreground="white")

prev_button = Button(topFrame, text="Previous", command=prev_button, padx=2, pady=2)
prev_button.place(x=10,y=65)
prev_button.configure(background = "black", foreground="white")

next_button = Button(topFrame, text="Next", command=next_button, padx=2, pady=2)
next_button.place(x=85,y=65)
next_button.configure(background = "black", foreground="white")

jump_button = Button(topFrame, text="Jump to", command=jump_to_num, padx=2, pady=2)
jump_button.place(x=10,y=115)
jump_button.configure(background = "black", foreground="white")

jump_input = Entry(topFrame, width=48, justify = "left", font=('Consolas', 10, 'bold'))
jump_input.place(x=100,y=115)

search_button = Button(topFrame, text="Search", command=search_word, padx=2, pady=2)
search_button.place(x=10,y=155)
search_button.configure(background = "black", foreground="white")

search_input = Entry(topFrame, width=48, justify = "left", font=('Consolas', 10, 'bold'))
search_input.place(x=100,y=155)

add_word_button = Button(topFrame, text="Add word", command=add_word, padx=2, pady=2)
add_word_button.place(x=10,y=205)
add_word_button.configure(background = "black", foreground="white")

add_word_input = Entry(topFrame, width=48, justify = "left", font=('Consolas', 10, 'bold'))
add_word_input.place(x=100,y=205)


desc_text = scrolledtext.ScrolledText(topFrame, undo=True, width=140, height=14, wrap="word", bg = "black", fg = "white")
desc_text.place(x=650, y=10)

nav_label = Label(topFrame, text="Check to skip changed words")
nav_label.place(x=450, y=150)
nav_label.configure(background = "black", foreground="white")

skip_var = IntVar()
nav_button = Checkbutton(topFrame, text='', variable=skip_var)
nav_button.place(x=500,y=175)


## FRAME 1

#show_checks(df.iloc[num].word)

check_all_button = Button(frame1, text="Check all", command=check_all, padx=2, pady=2)
check_all_button.place(x=10,y=660)

uncheck_all_button = Button(frame1, text="Uncheck all", command=uncheck_all, padx=2, pady=2)
uncheck_all_button.place(x=110,y=660)

## FRAME 2

change_to_label = Label(frame2, text="Change selected to:")
change_to_label.place(x=100, y=5)
change_to_label.configure(background = "red4", foreground="white")

change_to_input = Entry(frame2, width=50, justify = "left")
change_to_input.place(x=10, y=35)
change_to_input.configure(background = "red4", foreground="white")

type_button_name = Button(frame2, text="Name", command = lambda: set_remark("name"), padx=2, pady=2)
type_button_name.place(x=10,y=65)
type_button_name.configure(background = "red4", foreground="white")

type_button_world = Button(frame2, text="World", command = lambda: set_remark("world"), padx=2, pady=2)
type_button_world.place(x=10,y=105)
type_button_world.configure(background = "red4", foreground="white")

type_button_franch = Button(frame2, text="Franchise", command = lambda: set_remark("franchise"), padx=2, pady=2)
type_button_franch.place(x=10,y=145)
type_button_franch.configure(background = "red4", foreground="white")

type_button_persp = Button(frame2, text="Perspective", command = lambda: set_remark("perspective"), padx=2, pady=2)
type_button_persp.place(x=10,y=185)
type_button_persp.configure(background = "red4", foreground="white")

type_button_avatar = Button(frame2, text="Avatar", command = lambda: set_remark("avatar"), padx=2, pady=2)
type_button_avatar.place(x=10,y=225)
type_button_avatar.configure(background = "red4", foreground="white")

type_button_event = Button(frame2, text="Event", command = lambda: set_remark("event"), padx=2, pady=2)
type_button_event.place(x=10,y=265)
type_button_event.configure(background = "red4", foreground="white")

type_button_genre = Button(frame2, text="Genre", command = lambda: set_remark("genre"), padx=2, pady=2)
type_button_genre.place(x=10,y=305)
type_button_genre.configure(background = "red4", foreground="white")

type_button_genre = Button(frame2, text="Mode", command = lambda: set_remark("mode"), padx=2, pady=2)
type_button_genre.place(x=10,y=345)
type_button_genre.configure(background = "red4", foreground="white")



type_button_other = Button(frame2, text="Other", command = lambda: set_remark("{}".format(type_input.get())), padx=2, pady=2)
type_button_other.place(x=10,y=385)
type_button_other.configure(background = "red4", foreground="white")

type_input = Entry(frame2, width=48, justify = "left")
type_input.place(x=10,y=425)
type_input.configure(background = "red4", foreground="white")


## FRAME 3

desc_text2 = scrolledtext.ScrolledText(frame3, undo=True, width=50, height=45, wrap="word")
desc_text2.place(x=10, y=10)    
desc_text2.insert(1.0, "DESCRIPTION GOES HERE..")

## FRAME 4
#show_all_matches(df.iloc[num].word)
#find_syns(df.iloc[num].word)

## BOTTOM FRAME

input_file_label = Label(botFrame, text="File name: ")
input_file_label.place(x=10, y=10)
input_file_label.configure(background = "black", foreground="white")

input_file_input = Entry(botFrame, width=22, justify = "left", font=('Consolas', 10, 'bold'))
input_file_input.place(x=150,y=10)

input_file_button = Button(botFrame, text="Load", command=load_from_file, padx=2, pady=2)
input_file_button.place(x=400,y=10)
input_file_button.configure(background = "black", foreground="white")

output_file_label = Label(botFrame, text="File name: ")
output_file_label.place(x=1350, y=10)
output_file_label.configure(background = "black", foreground="white")

output_file_input = Entry(botFrame, width=22, justify = "left", font=('Consolas', 10, 'bold'))
output_file_input.place(x=1450,y=10)

output_file_button = Button(botFrame, text="Save", command=write_to_new_file, padx=2, pady=2)
output_file_button.place(x=1700,y=10)
output_file_button.configure(background = "black", foreground="white")


## MAIN LOOP
root.mainloop()


