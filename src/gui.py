from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from algoritma_rsa import *
import time
import os


public = (0,0)
private = (0,0)


def encryptGUI():
    global public, private
    # Get key and mode
    mode = var1.get()
    mode2 = var2.get()
    message = ent_message.get()

    if(lbl_public_text['text']==''):
        computeKey()

    if(mode2 == '2'): #file key
        public = (int(openFile('.temporary-public', 'r').split()[0]), int(openFile('.temporary-public', 'r').split()[1]))

    if(mode == '1'): #input message
        startTime = time.perf_counter()
        lbl_result_text['text'] = encrypt(public, message)
        endTime = time.perf_counter()
    elif(mode == '2'): #file message
        startTime = time.perf_counter()
        if(not(ent_file_name.get() and ent_file_ext.get())):
            messagebox.showerror('Error', 'Enter file name and extension!')
            return
        text = encrypt(public, openFile('.temporary','r'))
        filename = ent_file_name.get() + '.' + ent_file_ext.get()
        writeFile(' '.join(text), filename, 'w')
        lbl_result_text['text'] = 'Success! Saved in ' + filename
        checkFileSize(filename)
        endTime = time.perf_counter()
    lbl_time_text['text'] = endTime - startTime


def decryptGUI():
    global public, private
    # Get key and mode
    mode = var1.get()
    mode2 = var2.get()
    message = ent_message.get()

    if(lbl_public_text['text']==''):
        computeKey()

    if(mode2 == '2'): #file key
        private = (int(openFile('.temporary-private', 'r').split()[0]), int(openFile('.temporary-private', 'r').split()[1]))

    if(mode == '1'): #input message
        startTime = time.perf_counter()
        lbl_result_text['text'] = ''.join(chr(i) for i in decrypt(private, message.split()))
        endTime = time.perf_counter()
    elif(mode == '2'): #file message
        startTime = time.perf_counter()
        if(not(ent_file_name.get() and ent_file_ext.get())):
            messagebox.showerror('Error', 'Enter file name and extension!')
            return
        text = decrypt(private, openFile('.temporary', 'r').split())
        filename = ent_file_name.get() + '.' + ent_file_ext.get()
        writeFile(''.join(chr(i) for i in text), filename, 'w')
        lbl_result_text['text'] = 'Success! Saved in ' + filename
        checkFileSize(filename)
        endTime = time.perf_counter()
    lbl_time_text['text'] = endTime - startTime


def computeKey():
    try:
        global public, private
        if not (ent_p.get().isnumeric() and ent_q.get().isnumeric()):
            raise Exception("Enter p and q please!")
        public, private = generateKey(int(ent_p.get()), int(ent_q.get()))
        lbl_public_text['text'] = public
        lbl_private_text['text'] = private
    except Exception as e:
        messagebox.showerror('Error', e)


def checkErrorInput():
    status = True
    if(ent_message.get() == ''):
        messagebox.showerror('Error', 'Enter message!')
        status = False
    elif(ent_p.get() == '') or (ent_q.get() == ''):
        messagebox.showerror('Error', 'Enter key!')
        status = False
    return status

def checkErrorFile():
    status = True
    if(lbl_file_status['text'] == ''):
        messagebox.showerror('Error', 'Open file first!')
        status = False
    else:
        try:
            openFile('.temporary')
        except: # failed to open file
            lbl_file_status['text'] = ''
            messagebox.showerror('Error', 'Open file first!')
            status = False
        else: # success
            if(ent_key.get() == ''):
                messagebox.showerror('Error', 'Enter key!')
                status = False
            elif(not(ent_file_name.get() and ent_file_ext.get())):
                messagebox.showerror('Error', 'Enter file name and extension!')
                status = False
    return status

def askOpenFile(mode):
    global public, private
    f = askopenfile(mode ='rb') 
    if f is not None: 
        if (mode==1):
            writeFile(f.read(),'.temporary', 'wb')
            var1.set(2)
            lbl_file_status['text'] = 'Message file successfully loaded'
        elif (mode==2):
            writeFile(f.read(),'.temporary-public', 'wb')
            public = (int(openFile('.temporary-public', 'r').split()[0]), int(openFile('.temporary-public', 'r').split()[1]))
            lbl_public_text['text'] = public
            var2.set(2)
            lbl_file_status['text'] = 'Public key successfully loaded'
        elif (mode==3):
            writeFile(f.read(),'.temporary-private', 'wb')
            private = (int(openFile('.temporary-private', 'r').split()[0]), int(openFile('.temporary-private', 'r').split()[1]))
            lbl_private_text['text'] = private
            var2.set(2)
            lbl_file_status['text'] = 'Private key successfully loaded'

# Open file in read only
def openFile(file, mode):
    with open(file, mode) as f:
        return f.read()

# Write file in write
def writeFile(text, filename, mode):
    with open(filename, mode) as f:
        f.write(text)

# Clear function
def clear():
    ent_message.delete(0,END)
    ent_p.delete(0,END)
    ent_q.delete(0,END)
    ent_file_name.delete(0,END)
    ent_file_ext.delete(0,END)
    var1.set(1)
    var2.set(1)
    lbl_file_status['text'] = ''
    lbl_public_text['text'] = ''
    lbl_private_text['text'] = ''
    lbl_result_text['text'] = 'Click button above to see magic'
    lbl_time_text['text'] = ''
    lbl_filesize_text['text'] = ''

# Copy function
def copy():
    if(lbl_result_text['text'] == 'Click button above to see magic'):
        messagebox.showerror('Error', 'Encrypt something please!')
        return
    window.clipboard_clear()
    window.clipboard_append(lbl_result_text['text'])

# Save key function
def saveKey():
    if(lbl_public_text['text'] == ''):
        messagebox.showerror('Error', 'Enter key please!')
        return
    text_public = bytearray(lbl_public_text['text'], 'latin-1')
    text_private = bytearray(lbl_private_text['text'], 'latin-1')
    filename_public = 'public-key.pub'
    filename_private = 'private-key.pri'
    writeFile(lbl_public_text['text'], filename_public, 'w')
    writeFile(lbl_private_text['text'], filename_private, 'w')
    lbl_file_status['text'] = 'Success! Saved in ' + filename_public + ' and ' + filename_private

# Save function
def save():
    if(lbl_result_text['text'] == 'Click button above to see magic'):
        messagebox.showerror('Error', 'Encrypt something please!')
        return
    if(not(ent_file_name.get() and ent_file_ext.get())):
        messagebox.showerror('Error', 'Enter file name and extension!')
        return
    text = bytearray(lbl_result_text['text'], 'latin-1')
    filename = ent_file_name.get() + '.' + ent_file_ext.get()
    writeFile(text, filename, 'wb')
    checkFileSize(filename)
    lbl_result_text['text'] = 'Success! Saved in ' + filename

def checkFileSize(filename):
    file = open(filename)
    file.seek(0, os.SEEK_END)
    lbl_filesize_text['text'] = file.tell(), "bytes"

# Exit function 
def qExit(): 
    window.destroy() 




# Main window
window = Tk()
window.title('Encrypt & Decrypt')

# Title label
lbl_title = Label(text='Welcome to RSA Encryption!')
lbl_title.pack()

frm_form = Frame(relief=RIDGE, borderwidth=3)
frm_form.pack()

# Message label
lbl_text = Label(master=frm_form, text='Enter message:')
ent_message = Entry(master=frm_form, width=50)
lbl_text.grid(row=0, column=0, padx=5, pady=5, sticky="w")
ent_message.grid(row=0, column=1, padx=5, pady=5)

# Key label
lbl_p = Label(master=frm_form, text='Enter p:')
ent_p = Entry(master=frm_form, width=50)
lbl_p.grid(row=1, column=0, padx=5, pady=5, sticky='w')
ent_p.grid(row=1, column=1, padx=5, pady=5)

# Key label
lbl_q = Label(master=frm_form, text='Enter q:')
ent_q = Entry(master=frm_form, width=50)
lbl_q.grid(row=2, column=0, padx=5, pady=5, sticky='w')
ent_q.grid(row=2, column=1, padx=5, pady=5)

# File
btn_open = Button(master=frm_form, text='Open message', width=15, command= lambda: askOpenFile(1))
btn_open.grid(row=3, column=1, padx=5, pady=5, sticky='w')
lbl_file_status = Label(master=frm_form)
lbl_file_status.grid(row=4, column=1, padx=5, pady=5, sticky='w')

btn_clear = Button(master=frm_form, text='Clear', width=5, command=clear)
btn_clear.grid(row=3, column=1, padx=5, pady=5, sticky='e')

# Key file
btn_open = Button(master=frm_form, text='Open public key', width=15, command= lambda: askOpenFile(2))
btn_open.grid(row=4, column=1, padx=5, pady=5, sticky='w')
btn_open = Button(master=frm_form, text='Open private key', width=15, command= lambda: askOpenFile(3))
btn_open.grid(row=4, column=1, padx=5, pady=5, sticky='e')


btn_compute_key = Button(master=frm_form, text='Compute key', width=15, command=computeKey)
btn_compute_key.grid(row=5, column=1, padx=5, pady=5, sticky='w')

btn_save = Button(master=frm_form, text='Save key to file', width=15, command=saveKey)
btn_save.grid(row=5, column=1, padx=5, pady=5, sticky='e')

lbl_file_status = Label(master=frm_form, text='Status:')
lbl_file_status.grid(row=6, column=0, padx=5, pady=5, sticky="w")
lbl_file_status = Label(master=frm_form)
lbl_file_status.grid(row=6, column=1, padx=5, pady=5, sticky='w')


# Result key label
lbl_public = Label(master=frm_form, text='Public key:')
lbl_public_text = Label(master=frm_form, text='')
lbl_public.grid(row=8, column=0, padx=5, pady=5, sticky="w")
lbl_public_text.grid(row=8, column=1, padx=5, pady=5, sticky="w")

lbl_private = Label(master=frm_form, text='Private key:')
lbl_private_text = Label(master=frm_form, text='')
lbl_private.grid(row=9, column=0, padx=5, pady=5, sticky="w")
lbl_private_text.grid(row=9, column=1, padx=5, pady=5, sticky="w")


# Initialize radio button
var1 = StringVar()
var1.set(1)
var2 = StringVar()
var2.set(1)

# Encryption mode
lbl_mode = Label(master=frm_form, text='Message mode:')
lbl_mode.grid(row=11, column=0, padx=5, pady=5, sticky="w")
rad_mode = Radiobutton(master=frm_form,text='Input Message', variable = var1, value=1)
rad_mode.grid(row=11, column=1, padx=5, pady=5, sticky='w')
rad_mode = Radiobutton(master=frm_form,text='File Message', variable = var1, value=2)
rad_mode.grid(row=11, column=1, padx=5, pady=5)



# Key mode
lbl_mode = Label(master=frm_form, text='Key mode:')
lbl_mode.grid(row=13, column=0, padx=5, pady=5, sticky="w")
rad_mode = Radiobutton(master=frm_form,text='Input Key', variable = var2, value=1)
rad_mode.grid(row=13, column=1, padx=5, pady=5, sticky='w')
rad_mode = Radiobutton(master=frm_form,text='File Key', variable = var2, value=2)
rad_mode.grid(row=13, column=1, padx=5, pady=5)



# Encrypt/decrypt
btn_compute = Button(master=frm_form, text='Encrypt', width=10, height=2, command=encryptGUI)
btn_compute.grid(row=15, column=1, padx=5, pady=5, sticky='w')
btn_compute = Button(master=frm_form, text='Decrypt', width=10, height=2, command=decryptGUI)
btn_compute.grid(row=15, column=1, padx=5, pady=5, sticky='e')

# Result label
lbl_result = Label(master=frm_form, text='Result:')
lbl_result_text = Label(master=frm_form, text='Click button above to see magic')
lbl_result.grid(row=16, column=0, padx=5, pady=5, sticky="w")
lbl_result_text.grid(row=16, column=1, padx=5, pady=5, sticky="w")


# Processing time label
lbl_time = Label(master=frm_form, text='Processing Time:')
lbl_time_text = Label(master=frm_form, text='')
lbl_time.grid(row=17, column=0, padx=5, pady=5, sticky="w")
lbl_time_text.grid(row=17, column=1, padx=5, pady=5, sticky="w")

# Action button
btn_copy = Button(master=frm_form, text='Copy result', width=10, command=copy)
btn_copy.grid(row=18, column=1, padx=5, pady=5, sticky='w')


# File option
lbl_file_name = Label(master=frm_form, text='File name:')
ent_file_name = Entry(master=frm_form, width=50)
lbl_file_name.grid(row=19, column=0, padx=5, pady=5, sticky="w")
ent_file_name.grid(row=19, column=1, padx=5, pady=5)
lbl_file_ext = Label(master=frm_form, text='File extension:')
ent_file_ext = Entry(master=frm_form, width=50)
lbl_file_ext.grid(row=20, column=0, padx=5, pady=5, sticky="w")
ent_file_ext.grid(row=20, column=1, padx=5, pady=5)


# File size information
lbl_filesize = Label(master=frm_form, text='File size:')
lbl_filesize_text = Label(master=frm_form, text='')
lbl_filesize.grid(row=21, column=0, padx=5, pady=5, sticky="w")
lbl_filesize_text.grid(row=21, column=1, padx=5, pady=5, sticky="w")


btn_save = Button(master=frm_form, text='Save ciphertext to file', width=18, command=save)
btn_save.grid(row=22, column=1, padx=5, pady=5, sticky="w")
btn_exit = Button(master=frm_form, text='Exit', width=5, command=qExit)
btn_exit.grid(row=22, column=1, padx=5, pady=5, sticky='e')




# Keeps window alive 
window.mainloop()