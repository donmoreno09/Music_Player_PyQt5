import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="xdonny",
            password="amethysthope",  
            database="musicplayer"
        )
        print("Connessione a MySQL riuscita!")
        return connection
    except Error as e:
        print(f"Si è verificato un errore: '{e}'")
        return None

def create_tables(connection, table_name):
    cursor = connection.cursor()
    try:
        # Crea tabella songs
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (song TEXT)")
        connection.commit()  # Salva le modifiche
        print(f"Tabella {table_name} creata con successo!")
    except Error as e:
        print(f"Si è verificato un errore durante la creazione delle tabelle: '{e}'")
    finally:
        cursor.close()  

# Add a song to a database table
def add_song_to_database_table(connection, table_name, song):
    cursor = connection.cursor()
    try:
        cursor.execute(f"INSERT INTO {table_name} (song) VALUES ('{song}')")
        # altro modo per inserire i valori
        # cursor.execute(f"INSERT INTO {table_name} (song) VALUES (%s)", (song,))
        # oppure cursor.execute(f"INSERT INTO {table_name} (song) VALUES (?)", (song,))
        connection.commit()
        print(f"Canzone '{song}' aggiunta con successo alla tabella {table_name}")
    except Error as e:
        print(f"Si è verificato un errore durante l'aggiunta della canzone alla tabella: '{e}'")
    finally:
        cursor.close()

# Control if a song is already added in favourites
def check_song_in_database_table(connection, table_name, song):
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name} WHERE song = '{song}'")
        record = cursor.fetchone()
        if record:
            return True
        else:
            return False
    except Error as e:
        print(f"Si è verificato un errore durante il controllo della canzone nella tabella: '{e}'")
    finally:
        cursor.close()

# Delete a song from a database table
def delete_song_from_database_table(connection, table_name, song):
    cursor = connection.cursor()
    try:
        cursor.execute(f"DELETE FROM {table_name} WHERE song = '{song}'")
        connection.commit()
        print(f"Canzone '{song}' eliminata con successo dalla tabella {table_name}")
    except Error as e:
        print(f"Si è verificato un errore durante l'eliminazione della canzone dalla tabella: '{e}'")
    finally:
        cursor.close()

# Delete all songs from a database table
def delete_all_songs_from_database_table(connection, table_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"DELETE from {table_name}")
        connection.commit()
        print(f"Tutte le canzoni sono state eliminate dalla tabella {table_name}")
    except Error as e:
        print(f"Si è verificato un errore durante l'eliminazione delle canzoni dalla tabella: '{e}'")
    finally:
        cursor.close()

# Fetch all songs from a database table
def fetch_all_songs_from_database_table(connection, table_name):#Ques
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT song FROM {table_name}")
        song_data = cursor.fetchall()
        data = [song[0] for song in song_data] # Questo è un modo per estrarre i valori da una lista di tuple
        # oppure in modo classico e semplice
        # data = []
        # for song in song_data:
        #     data.append(song[0])
        print(f"Canzoni recuperate con successo dalla tabella {table_name}")
    except Error as e:
        print(f"Si è verificato un errore durante il recupero delle canzoni dalla tabella: '{e}'")
    finally:
        cursor.close()

    return data

# Get All Tables from a database
def get_playlist_tables(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        tables = [table[0] for table in tables]
        print("Tabelle recuperate con successo!")
    except Error as e:
        print(f"Si è verificato un errore durante il recupero delle tabelle: '{e}'")
    finally:
        cursor.close()

    return tables

# Delete a table from a database
def delete_table(connection, table_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"DROP TABLE {table_name}")
        connection.commit()
        print(f"Tabella {table_name} eliminata con successo!")
    except Error as e:
        print(f"Si è verificato un errore durante l'eliminazione della tabella: '{e}'")
    finally:
        cursor.close()