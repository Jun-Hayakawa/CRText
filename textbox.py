import numpy as np
import random
from tkinter import *
import pygame as pg

def right_shift(string, n):
    if not string:
        return string
    n %= len(string)
    return string[-n:] + string[:-n]

def left_shift(string, n):
    if not string:
        return string
    n %= len(string)
    return string[n:] + string[:n]

def zigzag(string, n, amt):
    width = 8
    n %= 16
    if n < width:
        return right_shift(string, amt)
    else:
        return right_shift(string, 2*width - amt)

def extend(string, length):
    n = int(np.ceil(length/len(string)))
    return string * n

def noise(string):
    for i in range(noise_slider.get()):
        chance = random.randint(0, 5)
        if chance == 1:
            length = len(string)
            altered_index = random.randint(0, length - 1)
            random_index = random.randint(0, length - 1)
            string = string[:altered_index] + string[random_index] + string[altered_index+1:]
    return string

def left_shift_effect(string, size, height):
    concatenated_output = ""
    for i in range(height):
        output = left_shift(string, int(i * tuning_slider.get()/100))
        noised_output = noise(output)
        trimmed_output = noised_output[:size]
        concatenated_output = concatenated_output + trimmed_output + "\n"
    return concatenated_output

def right_shift_effect(string, size, height, scroll_count):
    scroll = scroll_count % height
    concatenated_output = ""
    for i in range(height):
        if scroll_count != 0:
            if i <= scroll:
                output = right_shift(string, int(i * tuning_slider.get()/100) + 15)
            else: 
                output = right_shift(string, int(i * tuning_slider.get()/100))
        else: 
                output = right_shift(string, int(i * tuning_slider.get()/100))
        noised_output = noise(output)
        trimmed_output = noised_output[:size]
        concatenated_output += trimmed_output + "\n"
    return concatenated_output

def zigzag_effect(string, size):
    concatenated_output = ""
    for i in range(height):
        output = zigzag(string, i, int(i * tuning_slider.get()/100))
        noised_output = noise(output)
        trimmed_output = noised_output[:size]
        concatenated_output += trimmed_output + "\n"
    return concatenated_output

size = 100

"""GUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII"""
i = 0

def music_play(filepath):
    pg.mixer.stop()
    pg.mixer.init()
    pg.mixer.music.load(filepath)
    pg.mixer.music.set_volume(.4)
    pg.mixer.music.play(-1)

def choose_statement():
    statements = ["are you lost too? ", "a small project by jun hayakawa. ", "haha    ", "wake up.                           ", "死んだら、海に帰る。         ", "you're dreaming right now ", "ENRON ULTRASOFTWARE CORPORATION® 1998 ", "afterlife waiting room simulation #4 ", "you're safe here   ", "...                  ", "watch the screen closely ", "do you remember? ", "first snow /// falling /// on the half-finished bridge /// ", "i missed you :) ", "stay here with me ", "where does the time go...?     "]
    select = random.randint(0, len(statements) - 1)
    return statements[select]

root = Tk()
root.geometry("600x720")
root.configure(bg="blue")

entry = Entry(root, width=75)
entry.insert(0, choose_statement())
entry.pack(pady=20)

display = Label(root, text=" ", bg="blue", fg="white")
display.pack(anchor='center', pady=30)

button_frame = Frame(root, bg="blue")
button_frame.pack()

def mute():
    global mute_toggle
    if mute_toggle:
        mute_toggle = False
        mute_button.config(bg="white")
        pg.mixer.music.set_volume(.4)
    else:
        mute_toggle = True
        mute_button.config(bg="gray")
        pg.mixer.music.set_volume(0)

shift = i
def update_loop_channel1():
    global i
    global shift
    if entry.get():
        extended = extend(entry.get(), size)
        extended_shifted = right_shift(extended, shift)
        print_me = right_shift_effect(extended_shifted, size, height, i)
        display.config(text=print_me)
    else:
        display.config(text=" ")
    i += 1
    shift += 1
    if i % height == 0:
        shift += 15
    if i == 10000:
        i = 0
    if shift == 10000:
        shift = 0

def vertical_shift(string, shift):
    lines = string.split('\n')
    if not lines[-1]:  # remove the last empty line if exists
        lines = lines[:-1]
    shift %= len(lines)  # in case the shift is larger than the number of lines
    return '\n'.join(lines[-shift:] + lines[:-shift])

def update_loop_channel2():
    global i
    if entry.get():
        extended = extend(entry.get(), size)
        extended_leftshifted = left_shift(extended, i)
        extended_rightshifted = right_shift(extended, i)
        forward = right_shift_effect(extended_rightshifted, size, 8, 0)
        backward = left_shift_effect(extended_leftshifted, size, 8)
        concatenated = forward + backward + forward + backward
        display.config(text=concatenated)
    else:
        display.config(text=" ")
    i += 1
    if i == 10000:
        i = 0

def update_loop_channel3():
    global i
    if entry.get():
        i_mod = i % 32
        extended = extend(entry.get(), size)
        #extended_shifted = left_shift(extended, i)
        concatenated = zigzag_effect(extended, size)
        print_me = vertical_shift(concatenated, int(i_mod))
        display.config(text=print_me)
    else:
        display.config(text=" ")
    i += 1
    if i == 100000:
        i = 0


def blank():
    pass
mute_toggle = False
mute_button = Button(button_frame, text="mute", command=mute)
mute_button.pack(side=LEFT, padx=30)
update_loop = blank
height = 8

def channel1_select():
    global update_loop
    global height
    global channel1_toggle
    global channel2_toggle
    global channel3_toggle
    if not channel1_toggle:
        channel1_toggle = True
        channel1_button.config(bg="gray")
        #music_play("textbox/soundtrack.wav")
        update_loop = update_loop_channel1
        height = 32
        if channel2_toggle:
            channel2_select()
            channel2_toggle = False
        if channel3_toggle:
            channel3_select()
            channel3_toggle = False
    else:
        if channel2_toggle or channel3_toggle:
            channel1_button.config(bg="white")


channel1_toggle = False
channel1_button = Button(button_frame, bg="white", activebackground="gray", text="channel one", command=channel1_select)
channel1_button.pack(side=LEFT, padx=30)
pg.mixer.init()
music_play("soundtrack.wav")

def channel2_select():
    global height
    global update_loop
    global channel1_toggle
    global channel2_toggle
    global channel3_toggle
    if not channel2_toggle:
        channel2_toggle = True
        channel2_button.config(bg="gray")
        update_loop = update_loop_channel2
        #height = 8
        if channel1_toggle:
            channel1_select()
            channel1_toggle = False
        if channel3_toggle:
            channel3_select()
            channel3_toggle = False
    else:
        if channel1_toggle or channel3_toggle:
            channel2_button.config(bg="white")

channel2_toggle = False
channel2_button = Button(button_frame, activebackground="gray", text="channel two", command=channel2_select)
channel2_button.pack(side=LEFT, padx=30)

def channel3_select():
    global channel1_toggle
    global channel2_toggle
    global channel3_toggle
    global update_loop
    if not channel3_toggle:
        channel3_toggle = True
        channel3_button.config(bg="gray")
        update_loop = update_loop_channel3
        if channel2_toggle:
            channel2_select()
            channel2_toggle = False
        if channel1_toggle:
            channel1_select()
            channel1_toggle = False
    else:
        if channel2_toggle or channel1_toggle:
            channel3_button.config(bg="white")

channel3_toggle = False
channel3_button = Button(button_frame, activebackground="gray", text="channel three", command=channel3_select)
channel3_button.pack(side=LEFT, padx=30)

slider_frame = Frame(root, bg="blue")
slider_frame.pack(pady = 15)

tuning_slider = Scale(slider_frame, from_=-1000, to=1000, orient=HORIZONTAL, showvalue=0, label="tune", length=300)
tuning_slider.pack(side=LEFT, padx=10)
tuning_slider.set(100)

noise_slider = Scale(slider_frame, from_=150, to=0, orient=HORIZONTAL, showvalue=0, label="resolve", length=300)
noise_slider.pack(side=LEFT, padx=10)
noise_slider.set(150)

channel1_select()
def schedule():
    global update_loop
    update_loop()
    root.after(50, schedule)
schedule()

root.mainloop()