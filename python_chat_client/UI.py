import PySimpleGUI as sg

sg.theme("DarkAmber")




message_frame = sg.Frame(
                            title = "",
                            layout = [],
                            background_color = "#303030",
                            size = (500,0),
                            expand_y = True,
                            expand_x = True,
                            key = "-MESSAGE FRAME-"
                        )

connected_clients_frame = sg.Frame(
                                    title = "Connected Clients",
                                    layout = [],
                                    background_color = "#303030",
                                    expand_y = True,
                                    expand_x = True,
                                    key = "-CONNECTED CLIENTS FRAME-"
                                  )  


layout = [
            [message_frame, sg.VerticalSeparator(), connected_clients_frame],
            [sg.Input(expand_x=True, key="-MESSAGE-", do_not_clear=False), sg.Button("send")]
         ]

def chat_window():
    window = sg.Window("GAY ASS FART", layout, size=(800,700), resizable= False, finalize=True)
    window["-MESSAGE-"].bind("<Return>", "_Enter")


    while True:
        event, values = window.read()
        if values["-MESSAGE-"] != None:
            if event == "send" or event == "-MESSAGE-" + "_Enter":
                if main.is_client:
                    client.send(values["-MESSAGE-"])
                else:
                    server.send(values["-MESSAGE-"])
                print_message(main.USER, values(["-MESSAGE-"]))
        if event == sg.WIN_CLOSED:
            break

    window.close()



def login_popup(is_first_time):
    if is_first_time:
        event, values = sg.Window("LOGIN",
                                  [[sg.Text("LOGIN")], 
                                   [sg.Input("USERNAME")],
                                   [sg.Input("PASSWORD")],
                                   [sg.Button("LOGIN"), sg.Button("PASSWORD")]]).read(close=True)
    else:
        event, values = sg.Window("LOGIN",
                                  [[sg.Text("LOGIN")],
                                   [sg.Text("LOGIN UNSUCCESSFUL", text_color="#990100")],
                                   [sg.Input("USERNAME")],
                                   [sg.Input("PASSWORD")],
                                   [sg.Button("LOGIN"), sg.Button("PASSWORD")]]).read(close=True)
 
    return (event, values)


def connect_popup():
    event, values = sg.Window("ENTER IP AND PORT",
                              [[sg.Text("ENTER IP")],
                               [sg.Input("IP")],
                               [sg.Text("ENTER PORT")],
                               [sg.Input("PORT")],
                               [sg.Button("CONNECT", key="-CONNECT-")]],
                              resizable=False).read(close=True)
    
    PORT = int(values[1])
    ADDR = (values[0], PORT)
    return ADDR

def print_message(user, message):
    window.extend_layout(window["-MESSAGE FRAME-"], [[ sg.Text(user) , sg.Text(message) ]] )


