# NeoChat - Real-Time TCP Chat Application

## 📖 **Project Overview**
**NeoChat** is a real-time chat application built using **Python** with a **TCP server-client architecture**. It allows multiple clients to connect to a server, exchange messages, and supports **user authentication** (registration and login). The application uses **SQLite** for **user credential storage**, **bcrypt** for **password hashing**, and **socket programming** for **network communication**.

---

## 🚀 **Key Features**
- **Real-Time Messaging:** Supports broadcasting messages to all connected clients.
- **User Authentication:**
  - **Registration:** Securely stores usernames and hashed passwords in an SQLite database.
  - **Login:** Validates credentials against the database.
- **Message Broadcasting:** Displays messages in the `username: message` format.
- **Password Security:** Uses the **getpass** module to hide passwords during input and **bcrypt** for secure password hashing.
- **Error Handling:** Includes robust error handling for connection issues and invalid inputs.

---

## 🛠️ **Tech Stack**
- **Programming Language:** Python
- **Libraries:** `socket`, `threading`, `sqlite3`, `bcrypt`, `getpass`
- **Database:** SQLite

---

## 📂 **Project Structure**
```
NeoChat/
│
├─ client.py              # Client-side application
├─ server.py              # Server-side application
├─ users.db               # SQLite database file created after running code. Stores user credentials
└─ project_flow.png       # Flow diagram of server-client communication
```

---

## 🧠 **How It Works**
1. **Server Initialization:** Starts listening for incoming client connections.
2. **Client Connection:** Connects to the server using a specified IP and port.
3. **User Registration/Login:**
   - **Sign Up:** Prompts for a username and password, stores them securely in database.
   - **Sign In:** Verifies credentials and grants chat access.
4. **Messaging:** Allows users to send and receive messages in a chatroom-style format.
5. **Error Handling:** Manages disconnections and invalid inputs gracefully.

---

## ⚙️ **Installation & Setup**
### **Prerequisites:**
- **Python 3.10+**
- **Required Libraries:**
```bash
pip install bcrypt
```

### **Steps:**
1. **Clone the repository:**
```bash
git clone https://github.com/stephonOG/NeoChat.git
cd NeoChat
```

2. **Run the Server:**
```bash
python3 server.py
```

3. **Run the Client:**
```bash
python3 client.py
```

4. **Follow the prompts:**
- **Register** a new user or **Login** with existing credentials.
- Start **chatting** with connected users!

---

## 🚦 **Future Enhancements**
- **GUI Interface**
- **Private Messaging:** Allow direct messages between users.
- **File Transfer:** Support sending files over the chat.
- **Encryption:** Implement **SSL/TLS** for secure communication.
- **Mobile Compatibility:** Extend to mobile platforms .

## 📄 **License**
This project is licensed under the **MIT License**. Feel free to use and modify the code as needed.
