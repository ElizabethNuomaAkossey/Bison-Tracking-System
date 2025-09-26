from nicegui import ui,app

# Exposing assets folder
app.add_static_files("/assets","assets")

@ui.page("/")
def homepage():
    ui.query('.nicegui-content').classes('m-0 p-0 gap-0')
    with ui.header().classes("bg-white w-full justify-center  bg-gray-200 items-center text-black py-3 text-xl"):
        with ui.row().classes("justify-center items-center"):
            ui.image("/assets/bison_logo.png").classes("w-10 h-10")
            ui.label("Bison Tracker").classes("text-lg font-bold")
    ui.query('.nicegui-content').classes('m-0 p-0 gap-0')
    with ui.element("div").classes("w-full h-screen overflow-hidden items-center"):
        with ui.element("div").classes("w-full h-full relative bg-[url('/assets/bison_hero_image.png')] bg-center bg-cover md:px-20 md:py-20 items-center justify-center flex"):
            ui.element("div").classes("absolute inset-0 bg-black/40")

            # google fonts
            ui.add_head_html('''
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Lobster&family=Poppins:wght@100&display=swap" rel="stylesheet">
            <style>
                    .font-poppins{font-family:'Poppins', sans-serif;}
                    .font-roboto {font-family; 'Roboto', sans-serif;}
                    .font-lobster {font-family: 'Lobster', cursive;}
                    .font {font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif}
            </style>              
            ''')

             # Container for typewriter text
            ui.add_head_html("""
                                <style>
                                @keyframes typing-loop {
                                0% { width: 0; }
                                40% { width: 100%; }
                                90% { width: 100%; }
                                100% { width: 0; }
                                }

                                .typewriter {
                                display: inline-block;
                                overflow: hidden;
                                white-space: nowrap;
                                width: 0;
                                animation: typing-loop 7s steps(12, end) infinite;
                                }
                                </style>
                """)

            with ui.element("div").classes(
                "relative z-10 flex flex-col items-center justify-center font-poppins text-white"
            ):
                ui.label("Welcome to the Bison Tracker").classes(
                    "text-4xl md:text-6xl font-bold text-center"
                )
                ui.label('"Empowering smart animal farming through AI-powered monitoring"').classes(
                    "text-base md:text-base text-center my-5"
                )
                ui.button
                ui.button("Start Tracking", on_click=lambda:ui.navigate.to("/livestream")) \
                    .props("no-caps flat") \
                    .classes("text-black font-bold text-lg rounded-full bg-green-600 text-center")

        

