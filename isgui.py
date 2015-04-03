import Tkinter as tk
import tkMessageBox, tkFileDialog
import image_scrambler as isc
import steganography as steg
from PIL import Image, ImageTk


class ImageMain(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Image Processing Application")

        # data member for holding images
        self.image_in = None

        # image loader to grab image for processing
        self.img_loader = ImageLoader(self)
        self.img_loader.grid(row = 0, column = 0, columnspan = 2, sticky = "nsew")

        # drop down menu for selecting menu
        self.label_ddmenu = tk.Label(self, text = "Select operation:")
        self.label_ddmenu.grid(row = 2, column = 0, pady = 20)

        self.menu_map = {"Scramble" : ScrambleMenu, "Unscramble" : ScrambleMenu,\
                        "Encode" : EncodeMenu, "Decode" : DecodeMenu}
        self.ddmenu_var = tk.StringVar(self)
        self.ddmenu_var.set("Scramble")
        self.ddmenu = tk.OptionMenu(self, self.ddmenu_var, *self.menu_map.keys(),\
                                    command = self.get_menu)
        self.ddmenu.grid(row = 2, column = 1)

        # container for different menus
        self.container = tk.LabelFrame(self)
        self.container.grid(row = 3, column = 0, columnspan = 2, sticky = "nsew")

        self.frames = {}

        for F in (ScrambleMenu, EncodeMenu, DecodeMenu):
            frame = F(self.container, self.image_in)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(ScrambleMenu)
        
    # methods 
    def update(self):
        self.image_in = self.img_loader.image
        for key in self.frames:
            self.frames[key].image_in = self.img_loader.image

    def show_frame(self, c):
        frame = self.frames[c]
        frame.tkraise()

    def get_menu(self, operation):
        self.show_frame(self.menu_map[operation])

class ImageLoader(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master

        self.image = None

        # layout
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        # add core widgets
        self.button_load = tk.Button(self, text = "Load Image", command = self.get_img)
        self.button_load.grid(row = 0, column = 0, columnspan = 2)

        self.label_status1 = tk.Label(self, text = "No image loaded")
        self.label_status1.grid(row = 1, column = 0)

        self.button_view = ButtonViewImage(self, text = "View Image",\
                                      command = lambda: self.button_view.show_img(self.image))
        self.button_view.grid(row = 1, column = 1)

    # methods
    def get_img(self):
        imgname = tkFileDialog.askopenfilename()
        try:
            self.image = Image.open(imgname)
            self.master.update()
            self.label_status1.configure(text = imgname)
        except:
            tkMessageBox.showwarning(
                "Error",
                "Could not open image\n" + \
                "Make sure file is an appropriate type"
            )


class ScrambleMenu(tk.Frame):
    def __init__(self, master, Image):
        tk.Frame.__init__(self, master)
        self.master = master

        self.image_in = Image
        self.image_out = None

        # layout
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        # add widgets
        self.button_scramble = tk.Button(self, text = "SCRAMBLE",\
                                         command = lambda: self.process_img(True))
        self.button_scramble.grid(row = 0, rowspan = 2,\
                                  column = 0, columnspan = 1,\
                                  sticky = "ew")

        self.button_unscramble = tk.Button(self, text = "UNSCRAMBLE",\
                                         command = lambda: self.process_img(False))
        self.button_unscramble.grid(row = 0, rowspan = 2,\
                                  column = 1, columnspan = 1,\
                                  sticky = "ew")

        self.label_status2 = tk.Label(self, text = "No output")
        self.label_status2.grid(row = 2, column = 0)

        self.button_view = ButtonViewImage(self, text = "View Image",\
                            command = lambda: self.button_view.show_img(self.image_out))
        self.button_view.grid(row = 2, column = 1)

        self.button_save = tk.Button(self, text = "Save Output",\
                                     command = self.save_output)
        self.button_save.grid(row = 3, column = 0, columnspan = 2)

    # methods
    def save_output(self):

        outputname = tkFileDialog.asksaveasfilename()
        
        try:
            self.image_out.save(outputname)
        except:
            tkMessageBox.showwarning(
                "Error",
                "Something went wrong!"
            )

    def process_img(self, switch):
        try:
            if switch:
                self.image_out = isc.scramblePILimage(self.image_in)
            else:
                self.image_out = isc.unscramblePILimage(self.image_in)

            self.label_status2.configure(text = "Done")
        except:
            tkMessageBox.showwarning("Error", "Image processing failed")


class EncodeMenu(tk.Frame):
    def __init__(self, master, Image):
        tk.Frame.__init__(self, master)
        self.master = master

        self.image_in = Image
        self.image_out = None

        # layout
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        # add widgets
        self.label_msg1 = tk.Label(self, text = "Enter secret message here:")
        self.label_msg1.grid(row = 0, column = 0, columnspan = 2)

        self.text_msg = tk.Text(self)
        self.text_msg.insert(tk.END, "Enter secret message")
        self.text_msg.grid(row = 1, column = 0, columnspan = 2)

        self.button_encode = tk.Button(self, text ="ENCODE",\
                                command = self.encode_img)
        self.button_encode.grid(row = 2, column = 0, columnspan = 2)

        self.label_status2 = tk.Label(self, text = "No output")
        self.label_status2.grid(row = 3, column = 0)

        self.button_view = ButtonViewImage(self, text = "View Image",\
                            command = lambda: self.button_view.show_img(self.image_out))
        self.button_view.grid(row = 3, column = 1)

        self.button_save = tk.Button(self, text = "Save Output",\
                            command = self.save_output)
        self.button_save.grid(row = 4, column = 0, columnspan = 2)

    # methods
    def save_output(self):

        outputname = tkFileDialog.asksaveasfilename()
        
        try:
            self.image_out.save(outputname)
        except:
            tkMessageBox.showwarning(
                "Error",
                "Something went wrong!"
            )

    def encode_img(self):

        try:
            # 1- based? using 0 does not work
            secret_msg = self.text_msg.get(1.0, tk.END)
            self.image_out = steg.encodePILimage(self.image_in, secret_msg)
            self.label_status2.configure(text = "Done")
            
        except Exception as e:
            tkMessageBox.showwarning("Error", "Image encoding failed")
            print e


class DecodeMenu(tk.Frame):
    def __init__(self, master, Image):
        tk.Frame.__init__(self, master)
        self.master = master

        self.image_in = Image
        self.secret_msg = ""

        # layout
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        # add widgets
        self.button_decode = tk.Button(self, text ="DECODE",\
                                command = self.decode_img)
        self.button_decode.grid(row = 0, column = 0, columnspan = 2)

        self.label_msg1 = tk.Label(self, text = "Nothing has been decoded yet")
        self.label_msg1.grid(row = 1, column = 0, columnspan = 2)

        self.text_msg = tk.Text(self)
        self.text_msg.grid(row = 2, column = 0, columnspan = 2)

        self.button_save = tk.Button(self, text = "Save Output",\
                            command = self.save_message)
        self.button_save.grid(row = 3, column = 0, columnspan = 2)

    # methods
    def save_message(self):
        outputname = tkFileDialog.asksaveasfilename()     
        try:
            outfile = open(outputname, 'w')
            outfile.write(self.secret_msg)
        except:
            tkMessageBox.showwarning(
                "Error",
                "Could not write to file"
            )

    def decode_img(self):
        try:
            self.secret_msg = steg.decodePILimage(self.image_in)
            self.text_msg.insert(tk.END, self.secret_msg)
            self.label_msg1.configure(text = "Decoded message below")
            
        except Exception as e:
            tkMessageBox.showwarning("Error", "Image decoding failed")
            print e


class ImageWindow(tk.Toplevel):
    def __init__(self, master, Image):
        tk.Toplevel.__init__(self, master)
        self.title("Image")

        # image passed as argument
        self.image = Image
        # convert to a tkinter photo
        self.photo = ImageTk.PhotoImage(self.image)
        
        # add widgets
        self.label_img = tk.Label(self, image = self.photo)
        self.label_img.pack()
        
        self.button_cancel = tk.Button(self, text = "Cancel", command = self.destroy)
        self.button_cancel.pack()

class ButtonViewImage(tk.Button):
    def __init__(self, master, *args, **kwargs):
        tk.Button.__init__(self, master, *args, **kwargs)

    def show_img(self, image):
        if image == None:
             tkMessageBox.showwarning("Error", "No image loaded")
             return None

        try:
            img_win1 = ImageWindow(self, image)
        except Exception as e:
            tkMessageBox.showwarning(
                "Error",
                "Could not display image"
            )
            print e

if __name__ == "__main__":
    #root = tk.Tk()
    #root.title("Image Scrambler")
    #isgui = imageLoader(root)
    #root.mainloop()

    root = ImageMain()
    root.mainloop()
