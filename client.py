from Tkinter import *
import ttk
import requests
from PIL import ImageTk, Image
import socket
import time
import select
import threading
import errno

class RouteThread(threading.Thread):
    def init(self):
        super(RouteThread, self).__init__()
        print "new Route"

    def run(self):
       print "newRoute"

       HOST, PORT = '127.0.0.1', 8181
       listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
       listen_socket.bind((HOST, PORT))
       print time.asctime(), "Listen socket - %s:%s" % (HOST, PORT)
       # http_response = "Response"
       # readlist = [listen_socket]

       print time.asctime(), "Server Starts - %s:%s" % (HOST, PORT)

       # tupla dove viene salvata la lista dei client in formto < g , n >
       # log = tuple(['SOT'])  # StartOfTuple
       nemo= True
       while nemo:
           listen_socket.listen(5)
           readlist = [listen_socket]
           # ciclo while di esecuzione del server
           print("Listening on port %s..." % PORT)
           sread, swrite, sexc = select.select(readlist, [], [], 10)
           for s in sread:
               if s == listen_socket:
                   print "waiting for accept"
                   client_connection, client_address = listen_socket.accept()
           # client_connection, client_address = listen_socket.accept()
           time.sleep(2)
           try:
               print('#########################################')
               print('###                                   ###')
               print('###      Starting New Connection      ###')
               print('###                                   ###')
               print('#########################################')

               message = client_connection.recv(1024)
               print message
               nemo = False


           except socket.error as Exception:
               print "ciao"
               if Exception.errno != errno.EACCES:
                   print Exception.errno
               print(Exception.message)
               try:
                   client_connection.shutdown(1)
                   client_connection.close()
               except Exception:
                   print(Exception.message)

           finally:
               try:
                   client_connection.shutdown(1)
                   client_connection.close()
               except Exception:
                   print(Exception.message)

               finally:
                   # fine della connessione
                   print('#########################################')
                   print('###                                   ###')
                   print('###        Closing  Connection        ###')
                   print('###                                   ###')
                   print('#########################################')

       # elif s == sys.stdin:
       #     # handle standard input
       #     print('stdin handler')
       # else:
       #     # handle all other sockets
       #     print('err handler')

       listen_socket.close();
       print('Closing Socket...')

class MainFrame(Frame):
    def __init__(self, parent):
        #self.main_window = main_window
        #self.frame = Tk.frame(parent)
        Frame.__init__(self, parent)
        self.parent = parent

        #self.pack()

        self.user_entry = Entry(parent)
        self.user_entry.place(bordermode=INSIDE, height=30, width=100, relx=0.5, rely=0.3, anchor=CENTER)

        self.password_entry = Entry(parent, show="*")
        self.password_entry.place(bordermode=INSIDE, height=30, width=100, relx=0.5, rely=0.4, anchor=CENTER)

        self.login_button = Button(parent, text="Login", command=self.command_login)
        self.login_button.pack()
        self.login_button.place(bordermode=INSIDE, height=50, width=100, relx=0.5, rely=0.5, anchor=CENTER)

        self.new_user_button = Button(parent, text="New User", command=self.command_new_user)
        self.new_user_button.pack()
        self.new_user_button.place(bordermode=INSIDE, height=50, width=100, relx=0.5, rely=0.62, anchor=CENTER)

    def command_login(self):
        inserted_user = self.user_entry.get()
        inserted_password = self.password_entry.get()
        payload = {'command': 'login', 'user': inserted_user, 'pass': inserted_password}
        print payload
        payload_len = len(payload)
        headers = {'content-length': str(payload_len), 'content-type': 'application/json', 'Connection': 'close'}
        r = requests.post('http://localhost:8080/login', json=payload, headers=headers)
        print 'Qualcosa'
        print r.headers
        print r.status_code
        if r.status_code == 200:
            print 'Prepara la nuova pagina per il client'
            self.user_entry.destroy()
            self.password_entry.destroy()
            self.login_button.destroy()
            self.new_user_button.destroy()
            PlayerFrame(self.parent)
        else:
            print 'Reinserisci le credenziali di accesso'

    def command_new_user(self):
        self.user_entry.destroy()
        self.password_entry.destroy()
        self.login_button.destroy()
        self.new_user_button.destroy()
        NewUserFrame(self.parent)


class NewUserFrame(Frame):
    def __init__(self, parent):
        # self.main_window = main_window
        # self.frame = Tk.frame(parent)
        Frame.__init__(self, parent)
        self.parent = parent
        self.new_user_entry = Entry(parent)
        self.new_user_entry.place(bordermode=INSIDE, height=30, width=100, relx=0.6, rely=0.3, anchor=CENTER)
        self.new_user_label = Label(parent, text='Nuovo Utente')
        self.new_user_label.place(bordermode=INSIDE, height=30, width=100, relx=0.4, rely=0.3, anchor=CENTER)

        self.new_pass_entry = Entry(parent, show="*")
        self.new_pass_entry.place(bordermode=INSIDE, height=30, width=100, relx=0.6, rely=0.4, anchor=CENTER)
        self.new_pass_label = Label(parent, text='Nuova Password')
        self.new_pass_label.place(bordermode=INSIDE, height=30, width=100, relx=0.387, rely=0.4, anchor=CENTER)

        self.confirm_pass_entry = Entry(parent, show="*")
        self.confirm_pass_entry.place(bordermode=INSIDE, height=30, width=100, relx=0.6, rely=0.5, anchor=CENTER)
        self.confirm_pass_label = Label(parent, text='Conferma Nuova Password')
        self.confirm_pass_label.place(bordermode=INSIDE, height=30, width=170, relx=0.324, rely=0.5, anchor=CENTER)

        self.create_user_button = Button(parent, text="Crea Nuovo Utente", command=self.command_create_user)
        self.create_user_button.pack()
        self.create_user_button.place(bordermode=INSIDE, height=30, width=150, relx=0.5, rely=0.6, anchor=CENTER)

        self.exit_button = Button(parent, text="Indietro", command=self.command_exit)
        self.exit_button.pack()
        self.exit_button.place(bordermode=INSIDE, height=30, width=150, relx=0.5, rely=0.72, anchor=CENTER)


    def command_exit(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        MainFrame(self.parent)

            # self.new_user_entry.destroy()
        # self.new_user_label.destroy()
        # self.new_pass_entry.destroy()
        # self.new_pass_label.destroy()
        # self.

    def command_create_user(self):
        username = self.new_user_entry.get()
        password = self.new_pass_entry.get()
        confirmed_password = self.confirm_pass_entry.get()
        if password == confirmed_password:
            payload = {'command': 'new_user', 'user': username, 'pass': password}
            print payload
            payload_len = len(payload)
            headers = {'content_length': str(payload_len), 'content-type': 'application/json', 'Connection': 'close'}
            r = requests.post('http://localhost:8080/login', json=payload, headers=headers)
            print r
            self.command_exit()
        else:
            self.error_pass_label = Label(self.parent, text='Password diverse')
            self.error_pass_label.place(bordermode=INSIDE, height=30, width=170, relx=0.5, rely=0.67, anchor=CENTER)


class PlayerFrame(Frame):
    def __init__(self, parent):
        #self.main_window = main_window
        #self.frame = Tk.frame(parent)
        Frame.__init__(self, parent)
        self.parent = parent

        # command = command_nuova_partita
        self.nuova_partita_button = ttk.Button(self.parent, text="Nuova Partita", command=self.command_nuova_partita)
        self.nuova_partita_button.pack()
        self.nuova_partita_button.place(bordermode=INSIDE, height=50, width=100, relx=0.5, rely=0.3, anchor=CENTER)

        # command = command_statistiche
        self.statistiche_button = ttk.Button(self.parent, text="Statistiche")
        self.statistiche_button.pack()
        self.statistiche_button.place(bordermode=INSIDE, height=50, width=100, relx=0.5, rely=0.4, anchor=CENTER)

        # command = command_profilo
        self.profilo_button = ttk.Button(self.parent, text="Profilo")
        self.profilo_button.pack()
        self.profilo_button.place(bordermode=INSIDE, height=50, width=100, relx=0.5, rely=0.5, anchor=CENTER)

        self.exit_button = Button(parent, text="Indietro", command=self.command_exit)
        self.exit_button.pack()
        self.exit_button.place(bordermode=INSIDE, height=30, width=150, relx=0.5, rely=0.72, anchor=CENTER)

    def command_exit(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        MainFrame(self.parent)

    def command_nuova_partita(self):
        routeThr= RouteThread()
        routeThr.start()
        payload = {'user': 'alex', 'addr': '127.0.0.1'}
        print payload
        headers = {'content_length': 'payload_len', 'content-type': 'application/json'}
        r = requests.post('http://localhost:8080/newgame', json=payload, headers=headers)
        print r.headers



def main():
    root = Tk()
    root.title("Snake CFP")
    root.config(width=500, height=500)
    MainFrame(root)
    root.mainloop()


if __name__ == '__main__':
    main()
