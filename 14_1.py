from  tkinter import *

def menu_hide(st='hidden'):
    global menu_option_id
    for menuoption in menu_option_id:
        canvas.itemconfig(menuoption,state=st)

def menu_hide_skins(st='hidden'):
    global menu_option_id_skins
    for menuoption in menu_option_id_skins:
        canvas.itemconfig(menuoption,state=st)

def game_go():
    global menu_mode
    menu_mode = False
    menu_hide()
    canvas.itemconfig(text, state='normal')
    canvas.itemconfig(text_id, state='normal')
    update()

def menu_create_skins(canvas):
    global is_skins
    offset_skin = 0
    for menu_option_s in menu_options_skins:
        option_s = canvas.create_text(game_with//2, 20+ offset_skin, anchor=CENTER, font=('Arial', '25'), text=menu_option_s, fill='black')
        menu_option_id_skins.append(option_s)
        offset_skin += 50
    is_skins = True

def collision_menu_s(x, y):
    global  s , actor , photos , menu_mode_skins , menu_mode
    p = -1
    for index, menu_option in enumerate(menu_option_id_skins):
        position_1 = canvas.bbox(menu_option)
        if position_1[0]<x<position_1[2] and position_1[1]<y<position_1[3]:
            p = index
    if p == -1:
        return
    if p ==4:
        menu_hide("normal")
        menu_mode_skins = False
        menu_mode = True
        menu_hide_skins()
        return
    s = p +1
    photos = [PhotoImage(file=f'e_{i}s_{s}.png') for i in range(1, 5)]
    actor = canvas.create_image(10, 10, image=photos[0], anchor='nw')

def menu_skins():
    global menu_mode , menu_mode_skins, is_skins
    menu_mode = False
    menu_mode_skins = True
    menu_hide()
    if is_skins:
        menu_hide_skins("normal")
    else:
        menu_create_skins(canvas)

def menu_click(r):
    if r ==0:
        game_go()
    elif r ==1:
        menu_skins()
    elif r ==2:
        print('Выходим из игры')
        exit()

def menu_create(canvas):
    offset = 0
    for menu_option in menu_options:
        option_id = canvas.create_text(game_with//2, 20+ offset, anchor=CENTER, font=('Arial', '25'), text=menu_option, fill='black')
        menu_option_id.append(option_id)
        offset += 50

def collision_menu(x, y):
    r = -1
    for index, menu_option in enumerate(menu_option_id):
        position_1 = canvas.bbox(menu_option)
        if position_1[0]<x<position_1[2] and position_1[1]<y<position_1[3]:
            r = index
    menu_click(r)


def animate_frame(frame=0):
    canvas.itemconfigure(actor,image= photos[frame],anchor='nw')
    canvas.after(50 , animate_frame, (frame + 1) % len(photos))

def game_over():
    canvas.itemconfig(text_id, text=f"game over", fill="red")

def mouse_click(e): #обработка клика мышкки

    global mouse_x, mouse_y, menu_mode
    mouse_x, mouse_y = e.x, e.y
    if menu_mode:
        collision_menu(e.x, e.y)
    if menu_mode_skins:
        collision_menu_s(e.x,e.y)

def collision_detection(x, y):
    position = canvas.coords(actor)
    left = position[0]
    top = position[1]
    right = position[0]+actor_size
    bottom = position[1]+actor_size
    return left < x < right and top < y < bottom


def update_text_speed():
    canvas.itemconfig(text_id,text =actor_speed, fill = "black")
    canvas.itemconfig(text, text=f"{i}", fill="black")
    if actor_speed >=8:
        canvas.itemconfig(text_id, text=actor_speed, fill="red")





def update():
    global actor_vx, actor_vy , actor_speed , mouse_x, mouse_y, i, PAUSE
    coords = canvas.coords(actor)
    x_left = coords[0]
    y_top = coords[1]
    if x_left + actor_size > game_with:
        actor_vx = -actor_vx
    elif y_top + actor_size > game_height-10:
        actor_vy = -actor_vy
        actor_speed +=1
        update_text_speed()
    elif x_left  < 0:
        actor_vx = -actor_vx
    elif y_top <0:
        actor_vy = -actor_vy

    if collision_detection(mouse_x , mouse_y):
        actor_speed -= 1
        print("попал")
        update_text_speed()
        mouse_x = mouse_y = - 1
        if actor_speed >= 7:
            i += 1
            update_text_speed()

    if actor_speed >= 13 or actor_speed <= 0 :
        game_over()
        return


    canvas.move(actor , actor_vx * actor_speed , actor_vy * actor_speed)
    window.after(frame_time, update)


game_with = 400
game_height = 300
frame_time = 30
actor_size = 100
actor_vx = 1
actor_vy = 1
actor_speed = 5
i = 0
s= 1
mouse_x = mouse_y = - 1
window_width = 800
window_height = 600
menu_options =['Новая игра','Персонажи','Выход']
menu_options_skins =['Злая птичка','Птичка','Добрая птичка','Муха', "Главное меню"]
menu_option_id = []
menu_option_id_skins = []
menu_mode = True
menu_mode_skins = False
gameover = False
is_skins = False
# об. создания окна и виджетов
window = Tk()
window.title('ПТИЦА!!!')
window.resizable(width= False, height=False)
canvas = Canvas(window, width=game_with, height=game_height, background='white')


#объекты
#menu = canvas.create_text(game_with//2, game_height//2, fill = 'black', font = ('Times', '30', 'bold'), text = menu_options, anchor= CENTER)
window_pictures = PhotoImage(file='images.png')
window_id = canvas.create_image(-50, 0, image=window_pictures, anchor='nw')
photos = [PhotoImage(file=f'e_{i}s_{s}.png')for i in range(1,5)]
actor = canvas.create_image(10,10, image = photos[0],anchor = 'nw')
actor_line = canvas.create_rectangle(0, 290, game_with, game_with , fill= "blue", width=0)
text_id = canvas.create_text(game_with//2, game_height//2, fill = 'black', font = ('Times', '30', 'bold'), text = 'Счетчик', anchor= CENTER)
canvas.itemconfig(text_id, state='hidden')
text = canvas.create_text(game_with//2, game_height//3, fill = "black", font= "Times 20 bold", text=f"очки", anchor= CENTER)
canvas.itemconfig(text, state = 'hidden')

animate_frame()
menu_create(canvas)
#update()

canvas.bind('<Button>', mouse_click)
canvas.pack()
window.mainloop()