import fnmatch
import os
from tkinter import *
from tkinter.dialog import Dialog
from tkinter import messagebox
from tkinter import commondialog
import pikepdf
from pikepdf import Pdf
from pikepdf import _cpphelpers

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        # widget can take all window
        self.pack(fill=BOTH, expand=1)


        title = Label(self, text="PDF encryption", fg="blue", font=("Roboto", 12))
        title.place(x=10, y=30)

        self.choose_file_button = Button(self, text="Choose file to be encrypted", command=self.chooseFile,)
        self.choose_file_button.place(x=20,y=60)
        self.errorFilename = Label(self, text="", fg="red", font=("Helvetica", 8))
        self.errorFilename.place(x=25, y=87)
        # self.filename = Label(self, text="File to be encrypted" )
        self.filename = Label(self, text="", )
        self.filename.place(x=20,y=107)

        choose_directory_button = Button(self, text="Choose destination", command=self.chooseDirectory,)
        choose_directory_button.place(x=20,y=130)
        self.errorDirectory = Label(self, text="", fg="red", font=("Helvetica", 8))
        self.errorDirectory.place(x=25, y=157)
        # self.saveDirectory = Label(self, text="Destination of the encrypted file" )
        self.saveDirectory = Label(self, text="")
        self.saveDirectory.place(x=20,y=177)

        passwordLabel = Label(self, text="Password")
        passwordLabel.place(x=20, y=200)

        self.sv = StringVar()
        self.errorPassword = Label(self, text="", fg="red", font=("Helvetica", 8))
        self.errorPassword.place(x=25, y=217)
        self.passwordField = Entry(self, textvariable=self.sv, validate="focusout", validatecommand=self.callback)
        self.passwordField.place(x=20,y=237)

        startButton = Button(self, text="Start encyption", command=self.clickStartButton, background="blue", fg="white")
        startButton.place(x=10,y=270)

        # exitButton = Button(self, text="Cancel", command=self.clickExitButton)
        # exitButton.place(x=10, y=300)

        developer_name = Label(master, text="Personal project by: Adrian Evenagelista",  fg="blue", font=("Helvetica", 8))
        developer_name.place(x=10,y=380)

    def clickStartButton(self):

        hasError = False
        if not isFileValid((self.filename["text"])):
            self.errorFilename["text"] = "Invalid file. Please choose valid pdf file."
            hasError = True

        if not isDirValid((self.saveDirectory["text"])):
            self.errorDirectory["text"] = "Invalid directory. please choose valid destination."
            hasError = True

        if len(self.passwordField.get()) == 0:
            self.errorPassword["text"] = "The password is empty. please input desired password"
            hasError = True

        if hasError:
            print("hasError")
            failureDialog()
            return

        try:
            encrypt(filename=self.filename["text"],
                    destination=self.saveDirectory["text"],
                    password=self.passwordField.get())
        except Exception as e:
            failureDialog(message=str(e))
            return


        encryptedFilename = self.saveDirectory["text"] + "/" + str(self.filename["text"]).split("/")[-1]
        succesDialog(encryptedFilename)

        print("no error")

    def callback(self):
        if len(self.sv.get()) > 0:
            self.errorPassword["text"] = ""
        return True


    def clickExitButton(self):
        exit()

    def chooseFile(self):
        filename = askopenfilename(filetypes=[("PDF", "*.pdf")])
        if isFileValid((filename)):
            self.errorFilename["text"] = ""
        self.filename["text"] = filename

    def chooseDirectory(self):
        directory = askdirectory()
        if isDirValid(directory):
            self.errorDirectory["text"] = ""
        self.saveDirectory["text"] = directory

def encrypt(filename, destination, password):
    if not isDirValid(destination):
        raise Exception("The file directory may be removed or renamed.\nPlease try again")

    if not isFileValid(filename):
        raise Exception("The file may be deleted or renamed.\nPlease try again")

    pdf = Pdf.open(filename)
    newName = filename.split("/")[-1].split(".")[0] + '_encrypted.pdf'
    pdf.save(destination+"/"+newName, encryption=pikepdf.Encryption(owner=password, user=password, R=4))

def succesDialog(encryptedFilename):
    messagebox.showinfo(title="Encryption successful",
                        message="Successfully encrypted the pdf file.\nthe new filename is {}".format(encryptedFilename))


def failureDialog(message="Encryption failed.\nPlease verify the details you inputed."):
    messagebox.showerror(title="Encryption failure",
                        message=message)


def isDirValid(directory):
    if directory is None or len(directory) == 0:
        print("invalid directory")
        return False

    if not os.path.isdir(directory):
        return False
    return  True

def isFileValid(filename):
    if filename is None or len(filename) == 0:
        print("invalid filename")
        return False

    if not os.path.isfile(filename):
        return False

    return True


def askopenfilename(**options):
    "Ask for a filename to open"

    return Open(**options).show()

class _Dialog(commondialog.Dialog):

    def _fixoptions(self):
        try:
            # make sure "filetypes" is a tuple
            self.options["filetypes"] = tuple(self.options["filetypes"])
        except KeyError:
            pass

    def _fixresult(self, widget, result):
        if result:
            # keep directory and filename until next time
            # convert Tcl path objects to strings
            try:
                result = result.string
            except AttributeError:
                # it already is a string
                pass
            path, file = os.path.split(result)
            self.options["initialdir"] = path
            self.options["initialfile"] = file
        self.filename = result # compatibility
        return result

class Open(_Dialog):
    "Ask for a filename to open"

    command = "tk_getOpenFile"

    def _fixresult(self, widget, result):
        if isinstance(result, tuple):
            # multiple results:
            result = tuple([getattr(r, "string", r) for r in result])
            if result:
                path, file = os.path.split(result[0])
                self.options["initialdir"] = path
                # don't set initialfile or filename, as we have multiple of these
            return result
        if not widget.tk.wantobjects() and "multiple" in self.options:
            # Need to split result explicitly
            return self._fixresult(widget, widget.tk.splitlist(result))
        return _Dialog._fixresult(self, widget, result)

#
# file dialogs

class Open(_Dialog):
    "Ask for a filename to open"

    command = "tk_getOpenFile"

    def _fixresult(self, widget, result):
        if isinstance(result, tuple):
            # multiple results:
            result = tuple([getattr(r, "string", r) for r in result])
            if result:
                path, file = os.path.split(result[0])
                self.options["initialdir"] = path
                # don't set initialfile or filename, as we have multiple of these
            return result
        if not widget.tk.wantobjects() and "multiple" in self.options:
            # Need to split result explicitly
            return self._fixresult(widget, widget.tk.splitlist(result))
        return _Dialog._fixresult(self, widget, result)


class SaveAs(_Dialog):
    "Ask for a filename to save as"

    command = "tk_getSaveFile"


# the directory dialog has its own _fix routines.
class Directory(commondialog.Dialog):
    "Ask for a directory"

    command = "tk_chooseDirectory"

    def _fixresult(self, widget, result):
        if result:
            # convert Tcl path objects to strings
            try:
                result = result.string
            except AttributeError:
                # it already is a string
                pass
            # keep directory until next time
            self.options["initialdir"] = result
        self.directory = result # compatibility
        return result

#
# convenience stuff


def askopenfilename(**options):
    "Ask for a filename to open"

    return Open(**options).show()


def asksaveasfilename(**options):
    "Ask for a filename to save as"

    return SaveAs(**options).show()


def askopenfilenames(**options):
    """Ask for multiple filenames to open
    Returns a list of filenames or empty list if
    cancel button selected
    """
    options["multiple"]=1
    return Open(**options).show()

# FIXME: are the following  perhaps a bit too convenient?


def askopenfile(mode = "r", **options):
    "Ask for a filename to open, and returned the opened file"

    filename = Open(**options).show()
    if filename:
        return open(filename, mode)
    return None


def askopenfiles(mode = "r", **options):
    """Ask for multiple filenames and return the open file
    objects
    returns a list of open file objects or an empty list if
    cancel selected
    """

    files = askopenfilenames(**options)
    if files:
        ofiles=[]
        for filename in files:
            ofiles.append(open(filename, mode))
        files=ofiles
    return files


def asksaveasfile(mode = "w", **options):
    "Ask for a filename to save as, and returned the opened file"

    filename = SaveAs(**options).show()
    if filename:
        return open(filename, mode)
    return None


def askdirectory (**options):
    "Ask for a directory, and return the file name"
    return Directory(**options).show()

def start():
    # initialize tkinter
    root = Tk()
    app = Window(root)

    # set window title
    root.wm_title("PDF encryption")
    root.geometry("600x400")

    # show window
    root.mainloop()

if __name__ == "__main__":
    start()