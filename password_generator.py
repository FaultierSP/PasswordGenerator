import random
#import tkinter
from tkinter import *
from tkinter import font
from functools import partial
from pprint import pprint

#from tkinter import ttk

consonants=["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z"]
password=""
vowels=["a","e","i","o","u"]
special_ch=[".",",","?","!","#","@"]
num_syllables=3
num_numbers=4
num_chunks=2
divide_with_ch=True
num_passwords=3
textField=[]
padding=4

randclass=random.SystemRandom()

root=Tk()
root.title("Passwort-Generator")
fontObject=font.Font(size=12)

optionsFrame=Frame(root)
optionsFrame.grid(row=num_passwords,column=0)

buttonFrame=Frame(root)
buttonFrame.grid(row=num_passwords+1,column=0)

inputNumChunks=Spinbox(optionsFrame,from_=1,to=4,font=fontObject,width=3)
inputNumSyllables=Spinbox(optionsFrame,from_=1,to=4,font=fontObject,width=3)
inputNumNumbers=Spinbox(optionsFrame,from_=0,to=4,font=fontObject,width=3)
inputSpecialSymbolsIsChecked=IntVar()
inputSpecialSymbols=Checkbutton(optionsFrame,variable=inputSpecialSymbolsIsChecked)

def make_chunk():
    global password

    for sl in range (num_syllables):
        if randclass.getrandbits(1):
            password+=str(randclass.choice(consonants)).upper()
        else:
            password+=str(randclass.choice(consonants))

        password+=str(randclass.choice(vowels))

    for nb in range(num_numbers):
        password+=str(randclass.randint(1,9))

def make_password():
    global password

    password=""

    for nc in range(num_chunks):
        make_chunk()

        if(divide_with_ch and (nc+1)!=num_chunks):
            password+=str(randclass.choice(special_ch))

    return password

def copyToClipboard(ind):
    global root,textField

    root.clipboard_clear()
    root.clipboard_append(textField[ind].get())
    root.update()

def updateValue(inputObject,newValue):
    inputObject.delete(0,END)
    inputObject.insert(0,newValue)

def updateInputs():
    #global num_chunks,num_numbers,num_passwords,num_syllables#,inputNumChunks,inputNumNumbers,inputNumSyllables,inputSpecialSymbols

    updateValue(inputNumChunks,num_chunks)
    updateValue(inputNumSyllables,num_syllables)
    updateValue(inputNumNumbers,num_numbers)
    if divide_with_ch:
        inputSpecialSymbols.select()

def doYourThing():
    global root,textField,num_passwords

    for eo in range(num_passwords):
        entryObject=textField[eo]
        entryObject.configure(state="normal")
        entryObject.delete(0,END)
        entryObject.insert(0,make_password())
        entryObject.configure(state="readonly")

def updateVariables():
    global num_chunks,num_numbers,num_syllables,divide_with_ch

    num_chunks=int(inputNumChunks.get())
    num_numbers=int(inputNumNumbers.get())
    num_syllables=int(inputNumSyllables.get())
    divide_with_ch=bool(inputSpecialSymbolsIsChecked.get())

    doYourThing()

#Starts here
inputNumChunks.configure(command=updateVariables)
inputNumNumbers.configure(command=updateVariables)
inputNumSyllables.configure(command=updateVariables)
inputSpecialSymbols.configure(command=updateVariables)

for np in range(num_passwords):
    entryObject=Entry(root)
    entryObject.configure(state="readonly",font=fontObject,width=50,justify=CENTER)
    entryObject.grid(row=np,column=0,padx=padding,pady=padding)

    textField.append(entryObject)

    buttonObject=Button(root)
    buttonObject.configure(text="Kopieren",command=partial(copyToClipboard,np),font=fontObject)
    buttonObject.grid(row=np,column=1,padx=padding,pady=padding)

Label(optionsFrame,text="Anzahl Chunks",font=fontObject).grid(row=0,column=0,padx=padding,pady=padding)
inputNumChunks.grid(row=0,column=1,padx=padding,pady=padding)
Label(optionsFrame,text="Anzahl der Silben",font=fontObject).grid(row=1,column=0,padx=padding,pady=padding)
inputNumSyllables.grid(row=1,column=1,padx=padding,pady=padding)
Label(optionsFrame,text="Anzahl der Ziffern",font=fontObject).grid(row=0,column=2,padx=padding,pady=padding)
inputNumNumbers.grid(row=0,column=3,padx=padding,pady=padding)
Label(optionsFrame,text="Sonderzeichen",font=fontObject).grid(row=1,column=2,padx=padding,pady=padding)
inputSpecialSymbols.grid(row=1,column=3,padx=padding,pady=padding)

Button(buttonFrame,text="Neue Passwörter",command=doYourThing,font=fontObject).grid(padx=padding,pady=padding)
Button(buttonFrame,text="Tschüss",command=root.quit,font=fontObject).grid(row=0,column=1,padx=padding,pady=padding)

updateInputs()
doYourThing()

root.mainloop()
