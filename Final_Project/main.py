import os
import threading
import time
from tkinter import *
from tkinter import filedialog, messagebox, ttk

from mutagen.mp3 import MP3
from pygame import mixer
from ttkthemes import ThemedTk

main_application = ThemedTk(theme="breeze")
main_application.title('Symphony - Keep Grooving!')
main_application.geometry('820x820')
main_application.wm_iconbitmap('Symphony.ico')

status_bar_label = ttk.Label(main_application, text='Welcome To Symphony', relief=GROOVE, borderwidth=2,
                             font=('Helvetica', 15, 'italic'))
status_bar_label.pack(side=BOTTOM, fill=X)

button_frame = Frame(main_application)
button_frame.pack(side=BOTTOM, fill=X)

length_frame = Frame(main_application)
length_frame.pack(side=BOTTOM, fill=X)

# -------------------------ICON CODE----------------------------

play_icon = PhotoImage(file='play.png')
stop_icon = PhotoImage(file='stop.png')
pause_icon = PhotoImage(file='pause.png')
openfile_icon = PhotoImage(file='file.png')
openfolder_icon = PhotoImage(file='folder.png')
exit_icon = PhotoImage(file='exit.png')
increase_volume_icon = PhotoImage(file='increase_volume.png')
decrease_volume_icon = PhotoImage(file='decrease_volume.png')
mute_icon = PhotoImage(file='mute.png')
playlist_icon = PhotoImage(file='playlist.png')
about_us_icon = PhotoImage(file='about_us.png')
music_player_icon = PhotoImage(file='symphony_resized.png')  # In About Us Section
main_frame_music_icon = PhotoImage(file='main_frame_music.png')
volume_icon = PhotoImage(file='volume.png')
mute_resize_icon = PhotoImage(file='mute_resize.png')
plus_icon = PhotoImage(file='plus.png')
forward_icon = PhotoImage(file='forward.png')
backward_icon = PhotoImage(file='backward.png')
next_song_icon = PhotoImage(file='next_song.png')
previous_song_icon = PhotoImage(file='previous_song.png')


# ---------------------------------COMMAND CODE---------------------------------

mixer.init()

stop_var = True
pause_var = False

mute_var = False

musicname = os.getcwd()
time_length = 0.0

total_time_label = ttk.Label(length_frame, text='-- : --')
total_time_label.grid(row=0, column=2, padx=1, pady=2)

current_time_label = ttk.Label(length_frame, text='-- : --')
current_time_label.grid(row=0, column=0, padx=1, pady=2)

playlist_var = False

playlist_frame = Frame()
playlist_btnframe = Frame()

index = 0
playlist_box = Listbox(main_application)
playlist_list = []

play_it = os.getcwd()

selected_song = ()

current_time = 0

currentformat = None


def previous_song():
    global play_it, selected_song, playlist_list, stop_var, pause_var
    if playlist_var:
        try:
            stopmusic()
            selected_song = selected_song - 1
            if selected_song == 0:
                selected_song = len(playlist_list) - 1

            play_it = playlist_list[selected_song]
            mixer.music.load(play_it)
            time.sleep(1)
            mixer.music.play()
            status_bar_label['text'] = 'Playing Music' + ' - ' + os.path.basename(play_it)
            status_bar_label['anchor'] = W
            play_btn.grid_forget()
            pause_btn.grid(row=0, column=0, padx=2, pady=2)
            pause_var = False
            stop_var = False
            total_time()

        except:
            messagebox.showerror('File Not Found', 'Could not find the file to play. Please check again')


def nextsong():
    global play_it, selected_song, playlist_list, stop_var, pause_var
    if playlist_var:
        try:
            stopmusic()
            selected_song = selected_song + 1
            if selected_song == len(playlist_list):
                selected_song = 0

            play_it = playlist_list[selected_song]
            mixer.music.load(play_it)
            time.sleep(1)
            mixer.music.play()
            status_bar_label['text'] = 'Playing Music' + ' - ' + os.path.basename(play_it)
            status_bar_label['anchor'] = W
            play_btn.grid_forget()
            pause_btn.grid(row=0, column=0, padx=2, pady=2)
            pause_var = False
            stop_var = False
            total_time()

        except:
            messagebox.showerror('File Not Found', 'Could not find file to play. Please check again')


def playlist():
    global playlist_var, photo_frame, index, playlist_list, playlist_box, playlist_btnframe, playlist_frame
    if not playlist_var:
        photo_frame.pack_forget()

        playlist_btnframe = ttk.Frame(main_application)
        playlist_btnframe.pack(side=BOTTOM, fill=BOTH)

        playlist_frame = ttk.Frame(main_application)
        playlist_frame.pack(side=TOP, fill=BOTH)

        playlist_box = Listbox(playlist_frame, height=30, selectbackground='green', relief=GROOVE, borderwidth=5)
        playlist_box.insert(0, 'Please select an audio file')
        playlist_box.pack(side=TOP, fill=BOTH)

        playlist_photolabel = Label(playlist_box, height=420, image=music_player_icon)
        playlist_photolabel.pack(side=RIGHT)

        playlist_var = True

        index = 0

        def add_to_playlist():
            global index, playlist_list, playlist_box
            playlist_filename_path = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select Files',
                                                                filetypes=(
                                                                    ('Audio Files', '*.mp3'), ('Audio Files', '*.wav'),
                                                                    ('Audio Files', '*.ogg'), ('Audio Files', '*.m4a'),
                                                                    ('All Files', '*.*')))
            playlist_filename = os.path.basename(playlist_filename_path)
            if index == 0:
                playlist_box.delete(0)
                playlist_box.insert(index, playlist_filename)
                playlist_list.insert(index, playlist_filename_path)

            else:
                playlist_box.insert(index, playlist_filename)
                playlist_list.insert(index, playlist_filename_path)

            index += 1

        def delete_playlist():
            delete_song = playlist_box.curselection()
            delete_song = int(delete_song[0])
            playlist_box.delete(delete_song)
            playlist_list.pop(delete_song)

        def clear_all():
            playlist_box.delete(0, last=len(playlist_list) - 1)

        playlist_addbtn = ttk.Button(playlist_btnframe, text='Add', command=add_to_playlist)
        playlist_addbtn.grid(row=0, column=0, padx=3, pady=3)

        playlist_deletebtn = ttk.Button(playlist_btnframe, text='Delete', command=delete_playlist)
        playlist_deletebtn.grid(row=0, column=1, padx=3, pady=3)

        playlist_clearbtn = ttk.Button(playlist_btnframe, text='Clear All', command=clear_all)
        playlist_clearbtn.grid(row=0, column=2, padx=3, pady=3)

    else:
        playlist_btnframe.pack_forget()
        playlist_frame.pack_forget()
        photo_frame.pack(side=BOTTOM, fill=BOTH)
        playlist_var = False


def current_time_length(t):
    global pause_var, current_time, currentformat, playlist_list, selected_song
    current_time = 0
    try:
        while current_time <= t and mixer.music.get_busy():
            if not pause_var:
                minute, second = divmod(current_time, 60)
                currentformat = '{:02d} : {:02d}'.format(minute, second)
                current_time_label['text'] = currentformat
                scalelength.set(current_time)
                time.sleep(1)
                current_time += 1

                if current_time == t and selected_song < len(playlist_list):
                    nextsong()

                elif current_time == t and selected_song == len(playlist_list):
                    previous_song()

            else:
                continue

    except:
        stopmusic()


def total_time():
    global time_length, playlist_var, play_it
    if playlist_var:
        file_data = os.path.splitext(play_it)

        if file_data[1] == '.mp3':
            audio = MP3(play_it)
            total_length = audio.info.length

        else:
            file = mixer.Sound(play_it)
            total_length = file.get_length()

    else:
        file_data = os.path.splitext(musicname)

        if file_data[1] == '.mp3':
            audio = MP3(musicname)
            total_length = audio.info.length

        else:
            file = mixer.Sound(musicname)
            total_length = file.get_length()

    total_length = round(total_length)
    time_length = total_length
    mins, seconds = divmod(total_length, 60)
    timeformat = '{:02d} : {:02d}'.format(mins, seconds)
    total_time_label['text'] = timeformat
    scalelength['to'] = time_length

    t1 = threading.Thread(target=current_time_length, args=(total_length,))
    t1.start()


def browse_file():
    global pause_var, musicname, stop_var, time_length
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File', filetypes=(
        ('Audio Files', '*.mp3'), ('Audio Files', '*.wav'), ('Audio Files', '*.ogg')))
    musicname = filename
    mixer.music.load(filename)
    mixer.music.play()
    status_bar_label['text'] = 'Playing Music' + ' - ' + os.path.basename(filename)
    status_bar_label['anchor'] = W
    play_btn.grid_forget()
    pause_btn.grid(row=0, column=0, padx=2, pady=2)
    pause_var = False
    stop_var = False
    total_time()


def pausemusic():
    global pause_var, stop_var
    if not pause_var:
        mixer.music.pause()
        status_bar_label['text'] = "Music Paused"
        status_bar_label['anchor'] = W
        pause_btn.grid_forget()
        play_btn.grid(row=0, column=0, padx=2, pady=2)
        pause_var = True
        stop_var = True


def playmusic():
    global pause_var, stop_var, playlist_var, playlist_list, playlist_box, play_it, selected_song
    try:
        if pause_var:
            mixer.music.unpause()
            status_bar_label['text'] = 'Playing Music' + ' - ' + os.path.basename(musicname)
            status_bar_label['anchor'] = W
            play_btn.grid_forget()
            pause_btn.grid(row=0, column=0, padx=2, pady=2)
            pause_var = False
            stop_var = False

        else:
            if playlist_var:
                selected_song = playlist_box.curselection()
                selected_song = int(selected_song[0])
                play_it = playlist_list[selected_song]
                mixer.music.load(play_it)
                mixer.music.play()
                status_bar_label['text'] = 'Playing Music' + ' - ' + os.path.basename(play_it)
                status_bar_label['anchor'] = W
                play_btn.grid_forget()
                pause_btn.grid(row=0, column=0, padx=2, pady=2)
                pause_var = False
                stop_var = False
                total_time()

            else:
                mixer.music.load(musicname)
                mixer.music.play()
                status_bar_label['text'] = 'Playing Music' + ' - ' + os.path.basename(musicname)
                status_bar_label['anchor'] = W
                play_btn.grid_forget()
                pause_btn.grid(row=0, column=0, padx=2, pady=2)
                pause_var = False
                stop_var = False
                total_time()


    except:
        messagebox.showerror('File Not Found', 'Could not find file. Please select a music file to play')


play_btn = ttk.Button(button_frame, image=play_icon, command=playmusic)
play_btn.grid(row=0, column=0, padx=2, pady=2)


def stopmusic():
    global pause_var, stop_var
    if not stop_var:
        mixer.music.stop()
        status_bar_label['text'] = "Music Stopped"
        status_bar_label['anchor'] = W
        pause_btn.grid_forget()
        play_btn.grid(row=0, column=0, padx=2, pady=2)
        pause_var = False
        stop_var = True

    else:
        messagebox.showerror('File Not Found',
                             'Could not find file to stop. Please click on play button to play the song')


def forward_music():
    global current_time, time_length, currentformat
    while current_time <= time_length and mixer.music.get_busy():
        if not pause_var:
            current_time = current_time + 5
            minute, second = divmod(current_time, 60)
            currentformat = '{:02d} : {:02d}'.format(minute, second)
            current_time_label['text'] = currentformat
            scalelength.set(current_time)
            mixer.music.set_pos(current_time)
            break


def backward_music():
    global current_time, time_length,currentformat
    while current_time <= time_length and mixer.music.get_busy():
        if not pause_var:
            current_time = current_time - 5
            minute, second = divmod(current_time, 60)
            currentformat = '{:02d} : {:02d}'.format(minute, second)
            current_time_label['text'] = currentformat
            scalelength.set(current_time)
            mixer.music.set_pos(current_time)
            break


stop_btn = ttk.Button(button_frame, image=stop_icon, command=stopmusic)
stop_btn.grid(row=0, column=3, padx=2, pady=2)

pause_btn = ttk.Button(button_frame, image=pause_icon, command=pausemusic)

plus_btn = ttk.Button(button_frame, image=plus_icon, command=playlist)
plus_btn.grid(row=0, column=6, padx=2, pady=2)

forward_btn = ttk.Button(button_frame, image=forward_icon, command=forward_music)
forward_btn.grid(row=0, column=4, padx=2, pady=2)

backward_btn = ttk.Button(button_frame, image=backward_icon, command=backward_music)
backward_btn.grid(row=0, column=2, padx=2, pady=2)

next_song_btn = ttk.Button(button_frame, image=next_song_icon, command=nextsong)
next_song_btn.grid(row=0, column=5, padx=2, pady=2)

previous_song_btn = ttk.Button(button_frame, image=previous_song_icon, command=previous_song)
previous_song_btn.grid(row=0, column=1, padx=2, pady=2)


def set_vol(val):
    global mute_var,volume
    volume = float(val) / 100  # The volume or scale method automatically sends value in form of string
    if not mute_var:
        mixer.music.set_volume(volume)

    else:
        volume = volume * 100
        scale.set(volume)


def aboutus_func():
    about_us_dialog = Toplevel()
    about_us_dialog.geometry("600x300")
    about_us_dialog.title("About Us")
    about_us_dialog.iconbitmap(r'about_us.ico')
    about_us_dialog.resizable(0, 0)

    photo = ttk.Label(about_us_dialog, image=music_player_icon)
    photo.pack(side=LEFT)

    text = ttk.Label(about_us_dialog, text='Symphony Music Player', font=('Arial', 28, 'bold'))
    text.pack(side=TOP)

    text1 = ttk.Label(about_us_dialog, text='Keep Grooving', font=('Arial', 14))
    text1.pack(side=TOP)

    text2 = ttk.Label(about_us_dialog,
                      text='\nSymphony is a Music Player made by:\nAqsa, Aviral, Divyansh, Gunjan and '
                           'Michela.\n\nUnder the guidance of Dr. Sudhanshu Gonge.\n\nSymphony can read almost all '
                           'music files and formats.\n\nHope you guys like it!',
                      font=('Helvetica', 12))
    text2.pack(side=TOP)


status_bar_var = BooleanVar()
status_bar_var.set(True)


# Statusbar hide and show
def hide_status_bar():
    global status_bar_var, playlist_frame, playlist_btnframe
    if status_bar_var:
        status_bar_label.pack_forget()
        status_bar_var = False

    else:
        if not playlist_var:
            button_frame.pack_forget()
            length_frame.pack_forget()
            photo_frame.pack_forget()
            status_bar_label.pack(side=BOTTOM, fill=X)
            button_frame.pack(side=BOTTOM, fill=X)
            length_frame.pack(side=BOTTOM, fill=X)
            photo_frame.pack(side=BOTTOM)
            status_bar_var = True

        else:
            button_frame.pack_forget()
            length_frame.pack_forget()
            playlist_frame.pack_forget()
            playlist_btnframe.pack_forget()
            status_bar_label.pack(side=BOTTOM, fill=X)
            button_frame.pack(side=BOTTOM, fill=X)
            length_frame.pack(side=BOTTOM, fill=X)
            playlist_btnframe.pack(side=BOTTOM, fill=X)
            playlist_frame.pack(side=TOP, fill=BOTH)
            status_bar_var = True


scalelength = ttk.Scale(length_frame, from_=0, to=500, orient=HORIZONTAL, length=500)
scalelength.set(0)
scalelength.grid(row=0, column=1, padx=1, pady=1)

scale = Scale(button_frame, from_=0, to=100, showvalue=1, orient=HORIZONTAL, command=set_vol)
scale.set(50)
volume = 50
mixer.music.set_volume(volume / 100)
scale.grid(row=0, column=8, padx=2, pady=2)

scale_vol_photo = ttk.Label(button_frame, image=volume_icon)
scale_vol_photo.grid(row=0, column=7, padx=4, pady=2)

mute_photo = ttk.Label(button_frame, image=mute_resize_icon)


def increase_volume():
    global volume, mute_var
    if not mute_var:
        volume = float(volume) + 5
        scale.set(volume)
        mixer.music.set_volume(volume)

    else:
        volume = float(volume) + 5
        scale.set(volume)


def decrease_volume():
    global volume, mute_var
    if not mute_var:
        volume = float(volume) - 5
        scale.set(volume)
        mixer.music.set_volume(volume)

    else:
        volume = float(volume) - 5
        scale.set(volume)


def mute():
    global volume, mute_var
    if not mute_var:
        mixer.music.set_volume(0)
        mute_var = True
        scale_vol_photo.grid_forget()
        mute_photo.grid(row=0, column=7, padx=4, pady=2)

    else:
        mute_photo.grid_forget()
        scale_vol_photo.grid_forget()
        scale_vol_photo.grid(row=0, column=7, padx=4, pady=2)
        mixer.music.set_volume(volume)
        mute_var = False


def exit_command():
    global stop_var
    stop_var = False
    stopmusic()
    main_application.destroy()


def open_folder():
    global playlist_box, playlist_list, playlist_var, musicname, selected_song, play_it
    dirname_path = filedialog.askdirectory(initial=os.getcwd(), title='Select Folder')
    dirname = list(os.listdir(dirname_path))
    playlist()
    for i in range(len(dirname)):
        if i == 0:
            playlist_box.delete(0)
        if dirname[i].endswith(".mp3"):
            playlist_box.insert(i, dirname[i])
            r = os.path.join(dirname_path, dirname[i])
            playlist_list.insert(i, r)

        elif dirname[i].endswith(".wav"):
            playlist_box.insert(i, dirname[i])
            r = os.path.join(dirname_path, dirname[i])
            playlist_list.insert(i, r)

        elif dirname[i].endswith(".ogg"):
            playlist_box.insert(i, dirname[i])
            r = os.path.join(dirname_path, dirname[i])
            playlist_list.insert(i, r)


def multiple_files():
    global playlist_list, playlist_box
    multiple_filename_path = filedialog.askopenfilenames(initialdir=os.getcwd(), title='Select Files', filetypes=(
        ('Audio Files', '*.mp3'), ('Audio Files', '*.wav'), ('Audio Files', '*.ogg')))
    playlist()
    for i in range(len(multiple_filename_path)):
        if i == 0:
            playlist_box.delete(0)
        playlist_box.insert(i, (os.path.basename(multiple_filename_path[i])))
        playlist_list.insert(i, multiple_filename_path[i])


photo_frame = Label(main_application, image=main_frame_music_icon)
photo_frame.pack(side=BOTTOM, fill=BOTH)

# ----------------------------- End Command Code -----------------------------

# ------------------------------MENU BAR CODE-----------------------------------

main_menu = Menu()

media_menu = Menu(main_menu, tearoff=False)
audio_menu = Menu(main_menu, tearoff=False)
view_menu = Menu(main_menu, tearoff=False)
help_menu = Menu(main_menu, tearoff=False)

main_menu.add_cascade(label='Media', menu=media_menu)
main_menu.add_cascade(label='Audio', menu=audio_menu)
main_menu.add_cascade(label='View', menu=view_menu)
main_menu.add_cascade(label='Help', menu=help_menu)

media_menu.add_command(label='Open File', image=openfile_icon, compound=LEFT, accelerator='Ctrl + O',
                       command=browse_file)
media_menu.add_command(label='Multiple Files', image=openfile_icon, compound=LEFT, accelerator='Ctrl + Shift + O',
                       command=multiple_files)
media_menu.add_separator()
media_menu.add_command(label='Open Folder', image=openfolder_icon, compound=LEFT, accelerator='Ctrl + F',
                       command=open_folder)
media_menu.add_separator()
media_menu.add_command(label='Exit', image=exit_icon, compound=LEFT, accelerator='Ctrl + Q', command=exit_command)

audio_menu.add_command(label='Increase Volume', image=increase_volume_icon, compound=LEFT, command=increase_volume)
audio_menu.add_command(label='Decrease Volume', image=decrease_volume_icon, compound=LEFT, command=decrease_volume)
audio_menu.add_command(label='Mute', image=mute_icon, compound=LEFT, command=mute)

view_menu.add_checkbutton(label='Playlist', onvalue=True, offvalue=False, variable=playlist_var, image=playlist_icon,
                          compound=LEFT, command=playlist)
view_menu.add_separator()
view_menu.add_checkbutton(label='Status Bar', onvalue=True, offvalue=False, variable=status_bar_var, compound=LEFT,
                          command=hide_status_bar)

help_menu.add_command(label='About Us', image=about_us_icon, compound=LEFT, command=aboutus_func)

main_application.config(menu=main_menu)


# ----------------------------- End Menu Bar Code -----------------------------

def on_closing():
    global stop_var
    stop_var = False
    stopmusic()
    main_application.destroy()


main_application.protocol("WM_DELETE_WINDOW", on_closing)

# Bind Shortcut keys
main_application.bind("<Control-o>", browse_file)
main_application.bind("<Control-Shift-o>", multiple_files)
main_application.bind("<Control-f>", open_folder)
main_application.bind("<Control-q>", exit_command)

main_application.mainloop()
