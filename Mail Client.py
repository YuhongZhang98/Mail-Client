from flask import Flask, render_template, request
from socket import *
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("client.html")

@app.route('/send', methods = ['POST'])
def send():
    sender = request.form['Sender']
    receiver = request.form['Receiver']
    msg = "\r\n" + request.form['Content']
    endmsg = '\r\n.\r\n'
    mailserver = 'smtp.nyu.edu'
    serverport = 25

    # Create socket called clientSocket and establish a TCP connection with mailserver
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver, serverport))
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '220':
        print('220 reply not received from server.')

    # Send HELO command and print server response.
    heloCommand = 'HELO Alice\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    mailFromComd = 'MAIL FROM: <' + sender + '>\r\n'
    clientSocket.send(mailFromComd.encode())
    recv2 = clientSocket.recv(1024).decode()
    print(recv2)
    if recv2[:3] != '250':
        print('250 reply not received from server')

    # Send RCPT TO command and print server response.
    rcptTo = 'RCPT TO: <' + receiver + '>\r\n'
    clientSocket.send(rcptTo.encode())
    recv3 = clientSocket.recv(1024).decode()
    print(recv3)
    if recv3[:3] != '250':
        print('250 reply not received from server')

    # Send DATA command and print server response.
    data = 'DATA\r\n'
    clientSocket.send(data.encode())
    recv4 = clientSocket.recv(1024).decode()
    print(recv4)
    if recv4[:3] != '354':
        print('354 reply not received from server')

    # Send message data.
    clientSocket.send(msg.encode())

    # Message ends with a single period.
    clientSocket.send(endmsg.encode())
    recv5 = clientSocket.recv(1024).decode()
    print(recv5)
    if recv5[:3] != '250':
        print('250 reply not received from server')

    # Send QUIT command and get server response.
    quit = 'QUIT\r\n'
    clientSocket.send(quit.encode())
    recv6 = clientSocket.recv(1024).decode()
    print(recv6)
    if recv6[:3] != '221':
        print('221 reply not received from server')

    return "<h1>The email has been sent to " + receiver + "</h1>"
if __name__ == '__main__':
    app.run()

