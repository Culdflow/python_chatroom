import PySimpleGUI as sg

sg.theme("DarkAmber")


def popup_get_2string(prompt, button1, button2, default1, default2):
    event, values = sg.Window(prompt, [[sg.Text(prompt)], [sg.Input(default_text=default1)], [sg.Input(default2)], [sg.Button(button1), sg.Button(button2)]]).read(close=True)
    return (event, values)

print(popup_get_2string("hello", "login", "cancel", "gey", "ass"))

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

window = sg.Window("GAY ASS FART", layout, size=(800,700), resizable= False, finalize=True)
window["-MESSAGE-"].bind("<Return>", "_Enter")

while True:
    event, values = window.read()
    if values["-MESSAGE-"] != "":
        if event == "send" or event == "-MESSAGE-" + "_Enter":
            window.extend_layout(window["-MESSAGE FRAME-"], [[ sg.Text( values["-MESSAGE-"] ) ]] )
            window.extend_layout(window["-CONNECTED CLIENTS FRAME-"], [[ sg.Text( values["-MESSAGE-"] ) ]] ) 
            print(values["-MESSAGE-"])
    if event == sg.WIN_CLOSED:
        break

window.close()



