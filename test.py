import tkinter as tk

class ChatWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        # create a canvas widget for chat messages
        self.msgs_canvas = tk.Canvas(self, width=400, height=400)
        self.msgs_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # create a frame widget inside the canvas for messages
        self.msgs_frame = tk.Frame(self.msgs_canvas)
        self.msgs_canvas.create_window((0,0), window=self.msgs_frame, anchor='nw')

        # create an input box for typing new messages
        self.input_box = tk.Entry(self, width=50)
        self.input_box.pack(side=tk.BOTTOM, fill=tk.X)

        # create a button for sending messages
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.BOTTOM)

        # set initial values for message ID and bubble color
        self.msg_id = 0
        self.bubble_color = '#DCF8C6'  # use a light green color for sent messages

    def add_message(self, msg, is_sent=False):
        # create a new label widget for the message
        lbl = tk.Label(self.msgs_frame, text=msg, wraplength=250)

        # create a rounded rectangle for the message bubble
        x, y, w, h = 0, 0, 0, 0
        if is_sent:
            x = 150
            w = max(50, lbl.winfo_width() + 20)
            h = max(20, lbl.winfo_height() + 10)
            bubble_shape = [(x, y), (x + w, y), (x + w, y + h), (x + 5, y + h), (x, y + h - 5), (x, y)]
            bubble_color = self.bubble_color
        else:
            w = max(50, lbl.winfo_width() + 20)
            h = max(20, lbl.winfo_height() + 10)
            bubble_shape = [(x, y), (x + w - 5, y), (x + w, y + 5), (x + w, y + h), (x, y + h), (x, y + 5)]
            bubble_color = '#Fa63FF'  # use white color for received messages

        # create a canvas widget to draw the message bubble
        canvas = tk.Canvas(self.msgs_frame, width=w, height=h, highlightthickness=0)
        canvas.create_polygon(bubble_shape, fill=bubble_color, outline=bubble_color)

        # add the label widget to the canvas
        canvas.create_window((x + 10, y + 5), window=lbl, anchor='nw')

        # add the canvas widget to the messages frame
        self.msgs_frame.update_idletasks()
        self.msgs_frame.config(height=self.msgs_frame.winfo_height())
        self.msgs_canvas.config(scrollregion=self.msgs_canvas.bbox(tk.ALL))

        self.msgs_canvas.yview_moveto(1.0)

        self.msg_id += 1

    def send_message(self):
        msg = self.input_box.get()
        if msg:
            self.add_message(msg, is_sent=True)
            self.input_box.delete(0, tk.END)

# create the chat window
root = tk.Tk()
root.title("Chat Window")
ChatWindow(root)
root.mainloop()
