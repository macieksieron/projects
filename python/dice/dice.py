import re
from timeit import repeat
from tkinter import *
import random 

which = random.randrange(0,6)
which2 = random.randrange(0,6)
which3 = random.randrange(0,6)
which4 = random.randrange(0,6)
which5 = random.randrange(0,6)

def getResult(which,which2,which3,which4,which5):
    numbers = [which,which2,which3,which4,which5]
    repeats = [numbers.count(0),numbers.count(1),numbers.count(2),numbers.count(3),numbers.count(4),numbers.count(5)]
    if 5 in repeats:
        return "5 of a kind"
    elif 4 in repeats:
        return "4 of a kind"
    elif 3 in repeats:
        if 2 in repeats:
            return "Full"
        else:
            return "3 of a kind"
    elif repeats == [1,1,1,1,1,0]:
            return "Small Straight"
    elif repeats == [0,1,1,1,1,1]:
            return "Big Straight"
    elif repeats.count(2)==2:
        return "Two pairs"
    elif 2 in repeats:
        return "One pair"
    else:
        return ":("

def roll(index,number,number2,number3,number4,number5):
    global which,which2,which3,which4,which5
    result.configure(text = "")
    frame = number[index]
    frame2 = number2[index]
    frame3 = number3[index]
    frame4 = number4[index]
    frame5 = number5[index]
    index += 1
    if index == len(number) or index == len(number2) or index == len(number3) or index == len(number4) or index == len(number5):
        result.configure(text = getResult(which,which2,which3,which4,which5),foreground="black")
        which = random.randrange(0,6)
        which2 = random.randrange(0,6)
        which3 = random.randrange(0,6)
        which4 = random.randrange(0,6)
        which5 = random.randrange(0,6)
        return
    label.configure(image=frame)
    label2.configure(image=frame2)
    label3.configure(image=frame3)
    label4.configure(image=frame4)
    label5.configure(image=frame5)
    window.after(35,roll,index,number,number2,number3,number4,number5)

window = Tk()
window.title('Dice')
window['bg']="white"
window.geometry("1350x600+50+100")

button = Button(window, text="roll",command=lambda:roll(0,rolls[which],rolls[which2],rolls[which3],rolls[which4],rolls[which5]))
button.place(x=10,y=10)
button['bg']= 'white'

one = [PhotoImage(file='resources/one.gif',format = 'gif -index %i' %(i)) for i in range(53)]
two = [PhotoImage(file='resources/two.gif',format = 'gif -index %i' %(i)) for i in range(49)]
three = [PhotoImage(file='resources/three.gif',format = 'gif -index %i' %(i)) for i in range(51)]
four = [PhotoImage(file='resources/four.gif',format = 'gif -index %i' %(i)) for i in range(50)]
five = [PhotoImage(file='resources/five.gif',format = 'gif -index %i' %(i)) for i in range(50)]
six = [PhotoImage(file='resources/six.gif',format = 'gif -index %i' %(i)) for i in range(48)]

rolls = []
rolls.append(one)
rolls.append(two)
rolls.append(three)
rolls.append(four)
rolls.append(five)
rolls.append(six)

label = Label(window)
label.config(height=230,width=200)
label.place(x=85,y=85)
label['bg']= 'white'

label2 = Label(window)
label2.config(height=230,width=200)
label2.place(x=350,y=85)
label2['bg']= 'white'

label3 = Label(window)
label3.config(height=230,width=200)
label3.place(x=600,y=85)
label3['bg']= 'white'

label4 = Label(window)
label4.config(height=230,width=200)
label4.place(x=850,y=85)
label4['bg']= 'white'

label5 = Label(window)
label5.config(height=230,width=200)
label5.place(x=1100,y=85)
label5['bg']= 'white'

result = Label(window,font=("Arial",25))
result.config(height=5,width=10)
result.place(x=600,y=400)
result['bg']= 'white'

window.mainloop()


