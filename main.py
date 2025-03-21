from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from music import Ui_MusicApp
import os # Import the os module this module provides a portable way of using operating system-dependent functionality and it is used to interact with the operating system


class ModernMusicPlayer(QMainWindow, Ui_MusicApp): # Create a class that inherits from QMainWindow and Ui_MusicApp
    def __init__(self): # Constructor
        super().__init__() # Call the parent class constructor
        self.window = QMainWindow() # Create a QMainWindow object
        self.setupUi(self) # Setup the UI

        #Remove default title bar
        self.setAttribute(Qt.WA_TranslucentBackground) # Set the background to transparent
        self.setWindowFlag(Qt.FramelessWindowHint) # Remove the title bar
        

        # Initlial position of the window
        self.initialPosition = self.pos() # Get the initial position of the window
        
        # Connections
        # Default Page
        self.add_songs_btn.clicked.connect(self.add_songs)

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

    # Add Songs
    def add_songs(self):
        files, _ = QFileDialog.getOpenFileNames( # Get the files from the user the variabile files will contain the files selected by the user and the variable _ will contain the filter selected by the user
            self, 
            caption = 'Add Songs to the app', directory =  ':\\', # Set the caption and the directory of the file dialog
            filter='Supported Files (*.mp3;*.mpeg;*.ogg;*.m4a;*.MP3;*.wma;*.acc;*.amr;*.wav;*.ogg;*.flac)' # Filter the files that the user can select to only the supported files 
            ) # Get the files from the user # :\\ is the default directory, it will always remember the last directory
        
        if files:
            for file in files:
                self.loaded_songs_listWidget.addItem(
                    QListWidgetItem(
                        QIcon(':/img/utils/images/MusicListItem.png'),
                        os.path.basename(file) # Get the base name of the file
                    )
                ) # Add the files to the list widget