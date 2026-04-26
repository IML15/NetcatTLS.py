import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
    if not cmd:
        return
    # Uses directly the string cmd with shlex
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()


class NetCat:

    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:
                # We receive the reply or the prompt
                data = self.socket.recv(4096)
                if not data:
                    break
                # We print what we get (result/prompt)
                print(data.decode(), end='')
                # If what we receive ends in our prompt, we request an input
                if "BHP: #>" in data.decode():
                    buffer = input("")  # The prompt has been sent by the server
                    buffer += "\n"
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print("User terminated.")
            self.socket.close()
            sys.exit()

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()

    def handle(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())

        elif self.args.upload:
            file_buffer = b""
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break

            with open(self.args.upload, "wb") as f:
                f.write(file_buffer)
            message = f"Saved file: {self.args.upload}"
            client_socket.send(message.encode())


        elif self.args.command:

            cmd_buffer = b""
            while True:
                try:
                    client_socket.send(b"BHP: #> ")
                    # We read until we find the '\n'
                    while b"\n" not in cmd_buffer:
                        data = client_socket.recv(64)
                        if not data:  # If there isn't any data, the cliente has disconnected
                            break
                        cmd_buffer += data
                    if not cmd_buffer:
                        break
                    response = execute(cmd_buffer.decode().strip())  # .strip() clean spaces/jumps
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b""  # We clean for the next command
                except Exception as e:
                    print(f"Error handling client: {e}")
                    break  # We just got out of this client's loop
            client_socket.close()  # We just CLOSE this client's socket

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="BHP Net Tool",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent("""Example:
                                     netcat.py -t 192.168.1.108 -p 5555 -l -c #command shell
                                     netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt #upload to file
                                     netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" #execute command
                                     echo "ABC" | ./netcat.py -t 192.168.1.108 -p 135 #echo text to server port 135
                                     netcat.py -t 192.168.1.108 -p 5555 #connect to server"""))

    parser.add_argument("-c", "--command", action="store_true", help="command shell")
    parser.add_argument("-e", "--execute", help="execute specified command")
    parser.add_argument("-l", "--listen", action="store_true", help="listen")
    parser.add_argument("-p", "--port", type=int , default=5555, help="specified port")
    parser.add_argument("-t", "--target", default="0.0.0.0", help="specified IP")
    parser.add_argument("-u", "--upload", help="upload file")
    args = parser.parse_args()
    if args.listen:
        buffer = ""
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    nc.run()
