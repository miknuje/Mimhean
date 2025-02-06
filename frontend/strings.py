kv = """
ScreenManager:
    MainMenuScreen:
    LoginScreen:
    RegisterScreen:
    ChatScreen:

<MainMenuScreen>:
    name: "mainmenu"
    canvas:
        Color:
            rgba: 36/255, 35/255, 35/255, 1 
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        padding: 20
        spacing: 20
        orientation: "vertical"
        FloatLayout:
            Image:
                source: 'assets/images/logo.png'
                size_hint: None, None
                size: 200, 200
                pos_hint: {"center_x": 0.5, "center_y": 0.7}

        MDLabel:
            text: "Welcome to Mimhean"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: "Roboto"
            size_hint: (1, None)
            height: 50
            pos_hint: {"center_x": 0.5}
            font_size: 22

        BoxLayout:
            orientation: "vertical"
            spacing: 20
            size_hint_y: None
            height: self.minimum_height
            pos_hint: {"center_x": 0.5, "center_y": 0.3}

            MDFillRoundFlatButton:
                text: "Login"
                font_name: "assets/fonts/Roboto-Bold.ttf"
                font_size: 18
                md_bg_color: 94/255, 107/255, 145/255, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.6
                pos_hint: {"center_x": 0.5}
                on_release:
                    app.root.current = "login"
                    app.root.transition.direction = "left"

            MDFillRoundFlatButton:
                text: "Register"
                font_name: "assets/fonts/Roboto-Bold.ttf"
                font_size: 18
                md_bg_color: 94/255, 107/255, 145/255, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.6
                pos_hint: {"center_x": 0.5}
                on_release:
                    app.root.current = "register"
                    app.root.transition.direction = "left"

<LoginScreen>:
    name: "login"
    canvas:
        Color:
            rgba: 36/255, 35/255, 35/255, 1 
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: "vertical"
        spacing: 20
        padding: 20

        MDLabel:
            text: "Login"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: "Roboto"
            font_size: 22

        MDTextField:
            id: username
            hint_text: "Username"
            mode: "fill"
            color_mode: 'custom'
            helper_text: "Write your username here!"
            pos_hint: {"center_y": .5}
            line_color_focus: 0, 0, 0, 1
            text_color_focus: 0, 0, 0, 1
            hint_text_color_focus: 0, 0, 0, 1
            helper_text_color_focus: 1, 1, 1, 1
            font_style: "Roboto"
        
        MDTextField:
            id: password
            hint_text: "Password"
            mode: "fill"
            password: True
            color_mode: 'custom'
            helper_text: "Write your password here!"
            pos_hint: {"center_y": .5}
            line_color_focus: 0, 0, 0, 1
            text_color_focus: 0, 0, 0, 1
            hint_text_color_focus: 0, 0, 0, 1
            helper_text_color_focus: 1, 1, 1, 1
            font_style: "Roboto"

        MDFillRoundFlatButton:
            text: "Submit"
            font_size: 18
            md_bg_color: 94/255, 107/255, 145/255, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.6
            pos_hint: {"center_x": 0.5}
            font_name: "assets/fonts/Roboto-Bold.ttf"
            on_release: 
                root.login_user() 
                app.root.transition.direction = "left"

        MDFillRoundFlatButton:
            text: "Back"
            font_size: 18
            md_bg_color: 94/255, 107/255, 145/255, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.6
            pos_hint: {"center_x": 0.5}
            font_name: "assets/fonts/Roboto-Bold.ttf"
            on_release:
                app.root.current = "mainmenu"
                app.root.transition.direction = "right"

<RegisterScreen>:
    name: "register"
    canvas:
        Color:
            rgba: 36/255, 35/255, 35/255, 1 
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: "vertical"
        spacing: 20
        padding: 20

        MDLabel:
            text: "Register"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            font_style: "Roboto"
            font_size: 22

        MDTextField:
            id: email
            hint_text: "Email"
            mode: "fill"
            color_mode: 'custom'
            helper_text: "Write your email here!"
            pos_hint: {"center_y": .5}
            line_color_focus: 0, 0, 0, 1
            text_color_focus: 0, 0, 0, 1
            hint_text_color_focus: 0, 0, 0, 1
            helper_text_color_focus: 1, 1, 1, 1
            font_style: "Roboto"

        MDTextField:
            id: username
            hint_text: "Username"
            mode: "fill"
            color_mode: 'custom'
            helper_text: "Write your username here!"
            pos_hint: {"center_y": .5}
            line_color_focus: 0, 0, 0, 1
            text_color_focus: 0, 0, 0, 1
            hint_text_color_focus: 0, 0, 0, 1
            helper_text_color_focus: 1, 1, 1, 1
            font_style: "Roboto"

        MDTextField:
            id: password
            hint_text: "Password"
            mode: "fill"
            password: True
            color_mode: 'custom'
            helper_text: "Write your password here!"
            pos_hint: {"center_y": .5}
            line_color_focus: 0, 0, 0, 1
            text_color_focus: 0, 0, 0, 1
            hint_text_color_focus: 0, 0, 0, 1
            helper_text_color_focus: 1, 1, 1, 1
            font_style: "Roboto"

        MDTextField:
            id: passconf
            hint_text: "Confirm Password"
            mode: "fill"
            password: True
            color_mode: 'custom'
            helper_text: "Write again your password here!"
            pos_hint: {"center_y": .5}
            line_color_focus: 0, 0, 0, 1
            text_color_focus: 0, 0, 0, 1
            hint_text_color_focus: 0, 0, 0, 1
            helper_text_color_focus: 1, 1, 1, 1
            font_style: "Roboto"

        MDFillRoundFlatButton:
            text: "Submit"
            font_size: 18
            md_bg_color: 94/255, 107/255, 145/255, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.6
            pos_hint: {"center_x": 0.5}
            font_name: "assets/fonts/Roboto-Bold.ttf"
            on_release: 
                root.register_user()
                app.root.transition.direction = "left"

        MDFillRoundFlatButton:
            text: "Back"
            font_size: 18
            md_bg_color: 94/255, 107/255, 145/255, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.6
            pos_hint: {"center_x": 0.5}
            font_name: "assets/fonts/Roboto-Bold.ttf"
            on_release:
                app.root.current = "mainmenu"
                app.root.transition.direction = "right"

<ChatScreen>:
    name: "chat"
    canvas:
        Color:
            rgba: 36/255, 35/255, 35/255, 1 
        Rectangle:
            pos: self.pos
            size: self.size
    
    MDNavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: "vertical"
                    
                    MDTopAppBar:
                        title: "Mimhean"
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
                        md_bg_color: 94/255, 107/255, 145/255, 1
                        specific_text_color: 1, 1, 1, 1
                    
                    ScrollView:
                        MDBoxLayout:
                            id: chat_history
                            orientation: "vertical"
                            spacing: 10
                            size_hint_y: None
                            height: self.minimum_height
                            padding: 10
                            
                    BoxLayout:
                        size_hint_y: None
                        height: 60
                        spacing: 10
                        padding: [10, 5]
                        
                        MDTextField:
                            id: user_input
                            hint_text: "Write your message..."
                            helper_text: "Write your message here!"
                            mode: "fill"
                            size_hint_x: 0.8
                            multiline: False
                            line_color_focus: 0, 0, 0, 1
                            text_color_focus: 0, 0, 0, 1
                            hint_text_color_focus: 0, 0, 0, 1
                            helper_text_color_focus: 1, 1, 1, 1
                            md_bg_color: 94/255, 107/255, 145/255, 1
                            text_color: 1, 1, 1, 1
                            font_style: "Roboto"
                        
                        MDFillRoundFlatButton:
                            text: "Send"
                            size_hint_x: 0.2
                            md_bg_color: 94/255, 107/255, 145/255, 1
                            text_color: 1, 1, 1, 1
                            on_release: app.send_message()
        
        MDNavigationDrawer:
            id: nav_drawer
            size_hint_x: 0.6
            canvas:
                Color:
                    rgba: 36/255, 35/255, 35/255, 1 
                Rectangle:
                    pos: self.pos
                    size: self.size

            BoxLayout:
                orientation: "vertical"
                spacing: 10
                padding: 10

                MDLabel:
                    text: "Chat's"
                    font_style: "H5"
                    size_hint_y: None
                    height: 40
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                
                MDRaisedButton:
                    text: "New Chat"
                    md_bg_color: 94/255, 107/255, 145/255, 1
                    text_color: 1, 1, 1, 1
                    size_hint_x: 0.9
                    pos_hint: {"center_x": 0.5}
                    on_release: app.create_conversation()
                
                ScrollView:
                    MDList:
                        id: lista_conversas
                
                MDFillRoundFlatButton:
                    text: "Logout"
                    md_bg_color: 255/255, 69/255, 58/255, 1
                    text_color: 1, 1, 1, 1
                    size_hint_x: 0.9
                    pos_hint: {"center_x": 0.5}
                    on_release: app.logout()


"""