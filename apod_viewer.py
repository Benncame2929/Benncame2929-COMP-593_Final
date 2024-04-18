from tkinter import ttk
from tkinter import *
import inspect
import os
import apod_desktop
from PIL import ImageTk, Image
from tkcalendar import Calendar
from datetime import date, datetime
import image_lib
import sqlite3
import ctypes
import time

# Determine the path and parent directory of this script
script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
script_dir = os.path.dirname(script_path)

# Initialize the image cache
apod_desktop.init_apod_cache(script_dir)

# TODO: Create the GUI
#Creates window
root = Tk()
#Sets size of window
global window_width, window_height

window_width = 1200

window_height = 800

root.geometry(f'{window_width}x{window_height}')
#Gives window a title
root.title("Astronomy Picture of the Day Viewer")
#Creates calendar and adds to window

#These variables will be used later to limit the range of the calendar
mindate = date(1995, 6, 16)
maxdate = date.today()

global image_path

image_path = ''

root.image = image_path

global widget_list

widget_list = []



def open_calendar():  

    #Opens a 'top level' window
    top = Toplevel(root)

    #creates a calendar widget in the top level window
    cal = Calendar(top, selectmode = 'day', mindate=mindate, maxdate=maxdate)
    cal.grid(column = 0, row = 0)

    global cal_sel_button

    #creates and places a button that closes the calendar window when pressed
    cal_sel_button = Button(top, text="Select This Date", command=lambda: top.destroy())
    cal_sel_button.grid(column = 1, row = 1)

    widget_list.append(cal_button)

    #waits until the top window is closed to execute the next line

    top.wait_window(top)

    date_selected = cal.selection_get()
        
    return date_selected

def get_date_and_image_cal():

    screen_reset()

    apod_date = open_calendar()

    apod_id = apod_desktop.add_apod_to_cache(apod_date)

    apod_info = apod_desktop.get_apod_info(apod_id)

    image_path = apod_info['file_path']

    #was having trouble getting desktop button to remember image_path existed - this seems to fix it

    root.image = image_path

    image_info = apod_info['explanation']

    display_image_and_explanation(image_path, image_info)

def create_calendar_button():
    
    global cal_button

    cal_button = Button(root, text = "Open the Calendar to Select a Date", command=get_date_and_image_cal)
    
    cal_button.grid(column = 1, row = 2, sticky = "nsew")

    widget_list.append(cal_button)

def get_date_and_image_dropdown(apod_title):
    
    screen_reset()
    
    con = sqlite3.connect(apod_desktop.image_cache_db)

    cur = con.cursor()

    #Fetches the database ID of the image with the chosen title

    get_image_query = """
        SELECT id FROM images
        WHERE title = ?
    
    """

    cur.execute(get_image_query, (apod_title,))

    apod_id = cur.fetchone()[0]

    apod_info = apod_desktop.get_apod_info(apod_id)

    image_path = apod_info['file_path']

    root.image = image_path

    image_info = apod_info['explanation']

    display_image_and_explanation(image_path, image_info)

    con.close()   

def display_image_and_explanation(image_path, image_info):  

    window_width = root.winfo_width()

    window_height = root.winfo_height()

    img_to_display = Image.open(image_path)

    #Scale image to window size

    img_to_display.thumbnail((window_width, 0.7 * window_height))

    tk_image = ImageTk.PhotoImage(img_to_display)

    global apod_img_label

    apod_img_label = Label(image=tk_image)
    
    #This is a fix I found online to stop my image from being 'Garbage collected' - I guess the program decides tk_image can get thrown away
    # once we move far enough along ? Not sure

    apod_img_label.image = tk_image

    apod_img_label.grid(column = 0, row = 0, columnspan = 3, sticky = "nsew")

    widget_list.append(apod_img_label)

    global explanation_label

    explanation_label = Label(root, text = image_info, wraplength = window_width, bg = "deep pink", fg = "yellow")

    explanation_label.grid(column = 0, row = 1, columnspan = 3, sticky = "nsew")

    widget_list.append(explanation_label)
    
    #scales font size w/ amount of text & window size - weird things happened when it was a float value so we're just doing this :D

    global font_size

    font_size = 5

    min_height = 0.2 * window_height

    #Increases font size to fit the size of the window

    while explanation_label.winfo_reqheight() < min_height:
        font_size += 1
        explanation_label.config(font=("Comic Sans MS", font_size))
    
    return image_path
    
