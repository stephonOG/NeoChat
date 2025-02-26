import threading
import socket
import sqlite3
import bcrypt

host = '127.0.0.1'
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
usernames = []

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
conn.commit()

def register_user(signup_username, signup_password):
    hashed_pw = bcrypt.hashpw(signup_password.encode(), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (signup_username, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(login_username, login_password):
    cursor.execute("SELECT password FROM users WHERE username=?", (login_username,))
    result = cursor.fetchone()
    if not result:
        return "Username not found"
    if not bcrypt.checkpw(login_password.encode(), result[0]):
        return "Incorrect password"
    return True

def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            client.send(message)

def handle_client(client):
    # Get the index of this client to find their username
    index = clients.index(client)
    username = usernames[index]
    
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                if message.lower() == 'quit':
                    # Handle quit command
                    broadcast(f'{username} has left the chat'.encode('utf-8'))
                    clients.remove(client)
                    usernames.remove(username)
                    client.close()
                    break
                else:
                    # Format message with username
                    formatted_message = f'{username}: {message}'
                    broadcast(formatted_message.encode('utf-8'), client)
        except:
            # Handle unexpected disconnection
            if client in clients:
                clients.remove(client)
                usernames.remove(username)
                broadcast(f'\n{username} has left the chat'.encode('utf-8'))
                client.close()
            break

def handle_authentication(client):
    while True:
        try:
            client.send('Sign up (R) or Login (L)'.encode('utf-8'))
            choice = client.recv(1024).decode().strip().lower()

            if choice == 'r':
                signup_username = client.recv(1024).decode().strip()
                signup_password = client.recv(1024).decode().strip()
                if register_user(signup_username, signup_password):
                    client.send('Registration successful! Please log in now.'.encode('utf-8'))
                else:
                    client.send('Username already exists. Please try again.'.encode('utf-8'))
                continue  # Loop back to auth prompt instead of closing

            elif choice == 'l':
                login_username = client.recv(1024).decode().strip()
                login_password = client.recv(1024).decode().strip()
                auth_result = authenticate_user(login_username, login_password)
                
                if auth_result == True:
                    client.send('Login successful!'.encode('utf-8'))
                    usernames.append(login_username)
                    clients.append(client)
                    broadcast(f'{login_username} has joined the chat.'.encode('utf-8'))
                    return True  # Authentication successful
                else:
                    client.send(f'{auth_result}. Please try again.'.encode('utf-8'))
                    continue  # Loop back to auth prompt instead of closing
                    
        except Exception as e:
            print(f"Authentication error: {e}")
            return False

def receive():
    print('Server is running and listening..')
    while True:
        client, address = server.accept()
        print(f'Connection from {address}')
        
        if handle_authentication(client):
            threading.Thread(target=handle_client, args=(client,)).start()
        else:
            client.close()

if __name__ == "__main__":
    receive()