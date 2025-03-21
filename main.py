from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from music import Ui_MusicApp
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QTimer
import time
import songs
import os # Import the os module this module provides a portable way of using operating system-dependent functionality and it is used to interact with the operating system


class ModernMusicPlayer(QMainWindow, Ui_MusicApp): # Create a class that inherits from QMainWindow and Ui_MusicApp
    def __init__(self): # Constructor
        super().__init__() # Call the parent class constructor
        self.window = QMainWindow() # Create a QMainWindow object
        self.setupUi(self) # Setup the UI

        #Remove default title bar
        self.setAttribute(Qt.WA_TranslucentBackground) # Set the background to transparent
        self.setWindowFlag(Qt.FramelessWindowHint) # Remove the title bar

        # Globals
        global stopped # Declare the stopped variable as a global variable this variable will be used to check if the song is stopped
        global looped   # Declare the looped variable as a global variable this variable will be used to check if the song is looped
        global is_shuffled  # Declare the is_shuffled variable as a global variable this variable will be used to check if the song is shuffled

        stopped = False
        looped = False
        is_shuffled = False

        # Create Player
        self.player = QMediaPlayer() # Create a QMediaPlayer object

        self.initial_volume = 20 # Set the initial volume to 20
        self.player.setVolume(self.initial_volume) # Set the volume of the player
        self.volume_dial.setValue(self.initial_volume) # Set the value of the volume dial
        self.volume_label.setText(str(self.initial_volume)) # Set the text of the volume label
        

        # Initlial position of the window
        self.initialPosition = self.pos() # Get the initial position of the window

        # Slider Timer
        self.timer = QTimer() # Create a QTimer object
        self.timer.start(1000) # Start the timer with an interval of 1000 milliseconds (1 second)
        self.timer.timeout.connect(self.move_slider) # Connect the timer to the move_slider function
        
        # Connections
        # Default Page
        self.music_slider.sliderMoved.connect(self.player.setPosition) # Connect the sliderMoved signal of the music slider to the setPosition function of the player
        self.music_slider.sliderPressed.connect(self.player.pause) # Connect the sliderPressed signal of the music slider to the pause function of the player
        self.music_slider.sliderReleased.connect(self.player.play) # Connect the sliderReleased signal of the music slider to the play function of the player
        self.add_songs_btn.clicked.connect(self.add_songs)
        self.play_btn.clicked.connect(self.play_song)
        self.pause_btn.clicked.connect(self.pause_unpause)
        self.stop_btn.clicked.connect(self.player.stop)
        self.next_btn.clicked.connect(self.next_song)
        self.previous_btn.clicked.connect(self.previous_song)

        self.volume_dial.valueChanged.connect(self.volume_changed) # Connect the volume dial to the volume changed function to change the volume we use lambda to pass the value of the volume dial to the function

        self.show() # Show the window

        def moveApp(event):
            if event.buttons() == Qt.LeftButton: # Check if the left button is pressed
                self.move(self.pos() + event.globalPos() - self.initialPosition) # Move the window to the new position 
                self.initialPosition = event.globalPos() # Update the initial position to the new position
                event.accept() # Accept the event

        self.title_frame.mouseMoveEvent = moveApp # Call the moveApp function when the mouse is moved
    
    # Function to handle mouse position
    def mousePressEvent(self, event):
        self.initialPosition = event.globalPos() # Update the initial position to the new position
        event.accept() # Accept the event

    # Function to move the slider
    def move_slider(self):
        if stopped:
            return
        else:
            # Update the slider position
            if self.player.state() == QMediaPlayer.PlayingState: # Check if the player is playing the song and if it is playing the song set the slider position to the current position of the player
                self.music_slider.setMinimum(0) # Set the minimum value of the slider to 0 so the slider will start from 0
                self.music_slider.setMaximum(self.player.duration()) # Set the maximum value of the slider to the duration of the song
                slider_position = self.player.position() # Get the position of the player and set it to the slider position
                self.music_slider.setValue(slider_position) # Set the value of the slider to the slider position

                # Change time labels
                current_time = time.strftime("%H:%M:%S", time.gmtime(self.player.position() / 1000)) # Get the current time of the song; time.strftime() is used to format the time for example %H is used to get the hour %M is used to get the minute and %S is used to get the second; time.gmtime() is used to convert the time in seconds to a time tuple for example (hour, minute, second) 
                song_duration = time.strftime("%H:%M:%S", time.gmtime(self.player.duration() / 1000)) # Get the duration of the song

                self.time_label.setText(f"{current_time} / {song_duration}") # Set the text of the time label to the current time and the duration of the song

                #print(f"Duration: {self.player.duration()}")
                #print(f"Current: {slider_position}")

    # Add Songs
    def add_songs(self):
        files, _ = QFileDialog.getOpenFileNames( # Get the files from the user the variabile files will contain the files selected by the user and the variable _ will contain the filter selected by the user
            self, 
            caption = 'Add Songs to the app', directory =  ':\\', # Set the caption and the directory of the file dialog. This gives me a problem, an alternative solution is to put '' in the directory
            filter='Supported Files (*.mp3;*.mpeg;*.ogg;*.m4a;*.MP3;*.wma;*.acc;*.amr;*.wav;*.ogg;*.flac)' # Filter the files that the user can select to only the supported files 
            ) # Get the files from the user # :\\ is the default directory, it will always remember the last directory
        
        if files:
            for file in files:
                songs.current_song_list.append(file) # Add the files to the current song list in the songs.py file
                self.loaded_songs_listWidget.addItem(
                    QListWidgetItem(
                        QIcon(':/img/utils/images/MusicListItem.png'),
                        os.path.basename(file) # Get the base name of the file
                    )
                ) # Add the files to the list widget
    
    # Play The Song
    def play_song(self):
        try:
            current_selection = self.loaded_songs_listWidget.currentRow() # Get the current row of the list widget
            current_song = songs.current_song_list[current_selection] # Get the current song from the current song list

            song_url = QMediaContent(QUrl.fromLocalFile(current_song)) # Create a media content object from the current song file path
            """
            QMediaContent is a class that provides a container for media content. It is used to create a media content object that will be used to play the song.
            QUrl is a class that provides a convenient interface for working with URLs. It is used to create a URL object from the current song file path.
            fromLocalFile is a static method of the QUrl class that creates a URL object from a local file path.
            """
            self.player.setMedia(song_url) # Set the media content to the player; setMedia is a method of the QMediaPlayer class that sets the media content to the player
            self.player.play() # Play the song

            self.current_song_name.setText(os.path.basename(current_song)) # Set the current song name to the label
            self.current_song_path.setText(current_song) # Set the current song path to the label
        except Exception as e:
            print(f"Play song error: {e}")

            """
            Explanation of the code above:
            1. Get the current selection from the list widget (current row)
            2. Get the current song from the current song list
            3. Create a media content object from the current song file path that will be used to play the song
            4. Set the media content to the player
            5. Play the song
            """

    # Pause and unpause
    def pause_unpause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    # Function to change the volume
    def volume_changed(self):
        try:
            self.initial_volume = self.volume_dial.value() # Get the value of the volume dial
            self.player.setVolume(self.initial_volume) # Set the volume of the player
        except Exception as e:
            print(f"Volume changed error: {e}")

    # Play the next song
    def next_song(self):
        try:
            song_index = self.loaded_songs_listWidget.currentRow() # Get the current row of the list widget
            next_song_index = song_index + 1 # Get the index of the next song
            next_song = songs.current_song_list[next_song_index] # Get the next song from the current song list

            song_url = QMediaContent(QUrl.fromLocalFile(next_song)) # Create a media content object from the next song file path
            self.player.setMedia(song_url) # Set the media content to the player
            self.player.play() # Play the song
            self.loaded_songs_listWidget.setCurrentRow(next_song_index) # Set the current row of the list widget to the next song index

            self.current_song_name.setText(os.path.basename(next_song)) # Set the current song name to the label
            self.current_song_path.setText(next_song) # Set the current song path to the label

        except Exception as e:
            print(f"Next song error: {e}")

            """
            Explanation of the code above:
            1. Get the current selection from the list widget (current row)
            2. Get the next song from the current song list
            3. Create a media content object from the next song file path that will be used to play the song
            4. Set the media content to the player
            5. Play the song
            6. Set the current row of the list widget to the next song index so the next song will be selected because the current song is playing
            7. Set the current song name to the label
            """

    # Previous Song
    def previous_song(self):
        try:
            song_index = self.loaded_songs_listWidget.currentRow() # Get the current row of the list widget
            previous_song_index = song_index - 1 # Get the index of the previous song
            previous_song = songs.current_song_list[previous_song_index] # Get the previous song from the current song list

            song_url = QMediaContent(QUrl.fromLocalFile(previous_song)) # Create a media content object from the previous song file path
            self.player.setMedia(song_url) # Set the media content to the player
            self.player.play() # Play the song
            self.loaded_songs_listWidget.setCurrentRow(previous_song_index) # Set the current row of the list widget to the previous song index

            self.current_song_name.setText(os.path.basename(previous_song)) # Set the current song name to the label
            self.current_song_path.setText(previous_song) # Set the current song path to the label

        except Exception as e:
            print(f"Previous song error: {e}")