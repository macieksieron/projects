from tkinter import *
import ToolTip 

def update(index):
    global population,money
    frame = world[index]
    population += population_increase
    money += money_increase
    population_txt.configure(text = "Population: " + str(round(population)) + " | " + str(round(money)) + "$" + " (" + str(round(population_increase*(1000/60))) + " people/s" + ", " + str(round(money_increase*(1000/60))) + "$/s)",foreground="black")
    index += 1
    if index == 124:
        index = 0
    label.configure(image=frame)
    window.after(speed,update,index)

def changeSpeed():
    global speed,button
    if speed == 60:
        speed = 30
        button.configure(text="x2")
    elif speed == 30:
        speed = 15
        button.configure(text="x3")
    elif speed == 15:
        speed = 60
        button.configure(text="x1")

def add_temple():
    global temples,population_increase,money_increase,money
    if money>=5:
        temples+=1
        population_increase+=lalladog
        money_increase+=lalladog
        money-=5
        temples_txt.config(text=str(temples))

def add_castle():
    global castles,population_increase,money_increase,money
    if money>=100:
        castles+=1
        castles_txt.config(text=str(castles))
        population_increase+=100*lalladog
        money_increase+=25*lalladog
        money-=100

def add_house():
    global houses,population_increase,money_increase,money
    if money>=500:
        population_increase+=1000*lalladog
        money_increase+=100*lalladog
        money-=500
        houses+=1
        houses_txt.config(text=str(houses))

def add_village():
    global villages,population_increase,money_increase,money
    if money>=10000:
        villages+=1
        villages_txt.config(text=str(villages))
        population_increase+=10000*lalladog
        money_increase+=1000*lalladog
        money-=10000

def add_skyscraper():
    global skyscrapers,population_increase,money_increase,money
    if money>=100000:
        skyscrapers+=1
        skyscrapers_txt.config(text=str(skyscrapers))
        population_increase+=100000*lalladog
        money_increase+=20000*lalladog
        money-=100000

def add_space():
    global spaces,population_increase,money_increase,money
    if money>=1000000:
        spaces+=1
        spaces_txt.config(text=str(spaces))
        population_increase+=1000000*lalladog
        money_increase+=100000*lalladog
        money-=1000000

speed = 60
population = 0
lalladog = 1/(1000/60)
money = 10
population_increase = 0
money_increase = 0

temples = 0
castles = 0
houses = 0
skyscrapers = 0
spaces = 0
villages = 0

window = Tk()
window['bg']= '#f8f4fc'
window.title('Vorld')
window.geometry("800x600+300+100")

world = [PhotoImage(file='resources/world.gif',format = 'gif -index %i' %(i)) for i in range(124)]

button = Button(window, text="x1",command=changeSpeed)
button.place(x=10,y=10)
button['bg']= '#f8f4fc'

population_txt = Label(window)
population_txt['bg']= '#f8f4fc'
population_txt.place(x=10,y=45)

label = Label(window)
label.config(height=300,width=300)
label['bg']= '#f8f4fc'
label.place(x=400,y=100)

temple_png = PhotoImage(file="resources/temple.png")
temple = Label(window,image=temple_png)
temple.place(x=20,y=80)

castle_png = PhotoImage(file="resources/castle.png")
castle = Label(window,image=castle_png)
castle.place(x=20,y=160)

house_png = PhotoImage(file="resources/house.png")
house = Label(window,image=house_png)
house.place(x=20,y=240)

village_png = PhotoImage(file="resources/village.png")
village = Label(window,image=village_png)
village.place(x=20,y=320)

skyscraper_png = PhotoImage(file="resources/skyscraper.png")
skyscraper = Label(window,image=skyscraper_png)
skyscraper.place(x=20,y=400)

space_png = PhotoImage(file="resources/space.png")
space = Label(window,image=space_png)
space.place(x=20,y=480)

plus_png = PhotoImage(file="resources/plus.png")

temples_txt = Label(window,text=str(temples))
temples_txt.place(x=140,y=100)

castles_txt = Label(window,text=str(castles))
castles_txt.place(x=140,y=180)

houses_txt = Label(window,text=str(houses))
houses_txt.place(x=140,y=260)

villages_txt = Label(window,text=str(villages))
villages_txt.place(x=140,y=340)

skyscrapers_txt = Label(window,text=str(skyscrapers))
skyscrapers_txt.place(x=140,y=420)

spaces_txt = Label(window,text=str(spaces))
spaces_txt.place(x=140,y=500)

add_temple_btn = Button(window,image=plus_png,command=add_temple)
add_temple_btn.place(x=90,y=92)

add_castle_btn = Button(window,image=plus_png,command=add_castle)
add_castle_btn.place(x=90,y=172)

add_house_btn = Button(window,image=plus_png,command=add_house)
add_house_btn.place(x=90,y=252)

add_village_btn = Button(window,image=plus_png,command=add_village)
add_village_btn.place(x=90,y=332)

add_skyscraper_btn = Button(window,image=plus_png,command=add_skyscraper)
add_skyscraper_btn.place(x=90,y=412)

add_space_btn = Button(window,image=plus_png,command=add_space)
add_space_btn.place(x=90,y=492)

ToolTip.CreateToolTip(temple, text = "Temple | Cost: 5$ | 1p/s | 1$/s")
ToolTip.CreateToolTip(castle, text = "Castle | Cost: 100$ | 100p/s | 25$/s")
ToolTip.CreateToolTip(house, text = "House | Cost: 500$ | 1000p/s | 100$/s")
ToolTip.CreateToolTip(village, text = "Village | Cost: 10000$ | 10000p/s | 1000$/s")
ToolTip.CreateToolTip(skyscraper, text = "Skyscraper | Cost: 100000$ | 100000p/s | 20000$/s")
ToolTip.CreateToolTip(space, text = "Space Station | Cost: 1000000$ | 1000000p/s | 100000$/s")

update(0)
window.mainloop()



