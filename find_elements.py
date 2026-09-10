from pywinauto import Application

# app = Application().start("C:\\Path\\To\\frista.exe")

# Connect to the application
app = Application(backend="win32").connect(title="Login Frista (Face Recognition BPJS Kesehatan)")

# Get the main dialog
dlg = app.window(title="Login Frista (Face Recognition BPJS Kesehatan)")

# Interact with the text bar in the rectangle
text_bar = dlg.rectangle().child_window(control_type="Pane", top=1320, bottom=1355, left=1390, right=1695)

# Set text in the text bar
text_bar.set_text("123")
