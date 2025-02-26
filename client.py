import threading
import socket
from getpass import getpass

def handle_signup():
    signup_username = input('Enter username for sign-up: ')
    client.send(signup_username.encode('utf-8'))
    signup_password = getpass('Enter password for sign-up: ')
    client.send(signup_password.encode('utf-8'))

def handle_login():
    login_username = input('Enter username for login: ')
    client.send(login_username.encode('utf-8'))
    login_password = getpass('Enter password for login: ')
    client.send(login_password.encode('utf-8'))

def handle_authentication():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                continue

            print(message)  # Print server message

            if message == 'Sign up (R) or Login (L)':
                choice = input('>>> ').strip().lower()
                client.send(choice.encode('utf-8'))
                
                if choice == 'r':
                    handle_signup()
                elif choice == 'l':
                    handle_login()
                
            elif message == 'Login successful!':
                return True
            
            elif 'successful' in message or 'try again' in message:
                continue  # Keep authentication loop going
                
        except Exception as e:
            print(f'Authentication error: {e}')
            return False

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(message)
        except:
            print("\nDisconnected from server")
            break

def send_messages():
    while True:
        try:
            message = input()
            if message.lower() == '/quit':
                client.send('/quit'.encode('utf-8'))
                client.close()
                break
            elif message:  # Only send non-empty messages
                client.send(message.encode('utf-8'))
        except:
            break
# Main client code
        
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 59000))
    print("Connected to server!")

    # Handle authentication first
    if handle_authentication():
        print("\nAuthentication successful! You can now chat.")
        print("Type '/quit' to exit\n")
        
        # Start message threads only after successful authentication
        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.daemon = True  # Thread will close when main program exits
        receive_thread.start()

        send_thread = threading.Thread(target=send_messages)
        send_thread.daemon = True
        send_thread.start()
        
        # Keep main thread alive
        send_thread.join()
    else:
        print("Authentication failed. Closing connection.")
        client.close()

except Exception as e:
    print(f"Connection error: {e}")
    client.close()