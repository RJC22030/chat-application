
import streamlit as st
import socket
import threading
 
# Setting up the chat server connection
HOST = '127.0.0.1'  # Server IP
PORT = 12345  # Server Port
 
# Global chat message list
chat_history = []
 
# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                chat_history.append(message)
        except:
            st.write("Disconnected from the server.")
            break
 
# Streamlit app layout
st.title("Real-Time Chat App with File Sharing")
 
# Username and server connection
username = st.text_input("Enter your username", value="")
 
if st.button("Connect"):
    # Connect to the chat server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.send(username.encode('utf-8'))
 
    # Start a thread to listen for incoming messages
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
 
# Display chat history in real-time
st.subheader("Chat Room")
for msg in chat_history:
    st.write(msg)
 
# Message input and send button
message = st.text_input("Type your message here...")
if st.button("Send Message"):
    if message:
        client_socket.send(f"{username}: {message}".encode('utf-8'))
 
# File upload section
uploaded_file = st.file_uploader("Choose a file to send")
if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    # Code to send file bytes to the server via UDP or TCP
    # client_socket.send(file_bytes)
    st.write(f"Sent file: {uploaded_file.name}")
