from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from algoritma_rsa import *
import time
import os


public = (0,0)
private = (0,0)

# Append file, sign adalah string signature NOT TESTED
def appendSignature(filename, mode, sign):
    with open(filename, "a+") as f:
        f.seek(0)
        data = f.read(100)
        if len(data) > 0 :
            f.write("\n")
        f.write(sign)

def signature():
    appendSignature()

def digiSign():
    global public, private
    # Get key and mode
    mode = var1.get()
    mode2 = var2.get()
    message = openFile('.temporary','r')

    if(lbl_public_text['text']==''):
        computeKey()

    if(mode2 == '2'): #file key
        public = (int(openFile('.temporary-public', 'r').split()[0]), int(openFile('.temporary-public', 'r').split()[1]))

    if(mode == '1'): #input message
        lbl_result_text['text'] = sign(message, public)
        
    elif(mode == '2'): #file message
        # text = (openFile('.temporary','r'))
        # appendSignature(text, 'r', sign(text, public))

        text = sign(openFile('.temporary','r'), public)
        result = message + text
        f = openFile('.temporary','r')
        #namafile = f.name
        # filename = '.temporary' + '.' + 'txt'
        writeFile(result, openFile('.temporary', 'r'), 'w')
        lbl_result_text['text'] = 'Success! Saved in ' 
    

def computeKey():
    try:
        global public, private
        public, private = generateKey()
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
        if (mode==2):
            writeFile(f.read(),'.temporary-verify-file', 'wb')
            btn_open_file_verify['text'] = 'Opened'
        if (mode==3):
            writeFile(f.read(),'.temporary-signature', 'wb')
            btn_open_signature['text'] = 'Opened'
        if (mode==4):
            writeFile(f.read(),'.temporary-public', 'wb')
            btn_open_public_key['text'] = 'Opened'

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
def saveToNewDoc():
  #  if(not(ent_file_name.get() and ent_file_ext.get())):
  #      messagebox.showerror('Error', 'Enter file name and extension!')
  #      return
  #  text = bytearray(lbl_result_text['text'], 'latin-1')
  #  filename = ent_file_name.get() + '.' + ent_file_ext.get()
  #  writeFile(text, filename, 'wb')
  #  lbl_result_text['text'] = 'Success! Saved in ' + filename

    global public, private
    # Get key and mode
    mode = var1.get()
    mode2 = var2.get()
    message = openFile('.temporary','r')
    
    if(mode == '2'): #file message
        text = sign(openFile('.temporary','r'), public)
        result = message + text
        f = open('.temporary','r')
        filename = ent_file_name.get() + '.' + ent_file_ext.get()
        writeFile(result, filename, 'w')
        lbl_result_text['text'] = 'Success! Saved in ' + filename

def reset():
    btn_open_file_verify['text'] = 'Open file'
    btn_open_signature['text'] = 'Open signature'
    btn_open_public_key['text'] = 'Open public key'

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


# File
btn_open = Button(master=frm_form, text='Open message', width=15, command= lambda: askOpenFile(1))
btn_open.grid(row=3, column=1, padx=5, pady=5, sticky='w')
lbl_file_status = Label(master=frm_form)
lbl_file_status.grid(row=4, column=1, padx=5, pady=5, sticky='w')

btn_clear = Button(master=frm_form, text='Clear', width=5, command=clear)
btn_clear.grid(row=3, column=1, padx=5, pady=5, sticky='e')


btn_compute_key = Button(master=frm_form, text='Compute key', width=15, command=computeKey)
btn_compute_key.grid(row=4, column=1, padx=5, pady=5, sticky='w')

btn_save = Button(master=frm_form, text='Save key to file', width=15, command=saveKey)
btn_save.grid(row=4, column=1, padx=5, pady=5, sticky='e')

lbl_file_status = Label(master=frm_form, text='Status:')
lbl_file_status.grid(row=5, column=0, padx=5, pady=5, sticky="w")
lbl_file_status = Label(master=frm_form)
lbl_file_status.grid(row=5, column=1, padx=5, pady=5, sticky='w')


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
var3 = StringVar()
var3.set(1)

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
btn_compute = Button(master=frm_form, text='Sign!', width=10, height=2, command=digiSign)
btn_compute.grid(row=15, column=1, padx=5, pady=5, sticky='w')

# Result label
lbl_result = Label(master=frm_form, text='Result:')
lbl_result_text = Label(master=frm_form, text='Click button above to see magic')
lbl_result.grid(row=16, column=0, padx=5, pady=5, sticky="w")
lbl_result_text.grid(row=16, column=1, padx=5, pady=5, sticky="w")

# File option
lbl_file_name = Label(master=frm_form, text='File name:')
ent_file_name = Entry(master=frm_form, width=50)
lbl_file_name.grid(row=19, column=0, padx=5, pady=5, sticky="w")
ent_file_name.grid(row=19, column=1, padx=5, pady=5)
lbl_file_ext = Label(master=frm_form, text='File extension:')
ent_file_ext = Entry(master=frm_form, width=50)
lbl_file_ext.grid(row=20, column=0, padx=5, pady=5, sticky="w")
ent_file_ext.grid(row=20, column=1, padx=5, pady=5)


btn_save = Button(master=frm_form, text='Sign and save signature to other doc', width=35, height = 2, command = saveToNewDoc) ## belum ada fungsinya
btn_save.grid(row=22, column=1, padx=5, pady=5, sticky="w")

# verify
lbl_file_ext = Label(master=frm_form, text='Digital Signature Embedded:')
lbl_file_ext.grid(row=23, column=0, padx=5, pady=5, sticky="w")
ent_file_ext.grid(row=23, column=1, padx=5, pady=5)

lbl_verify = Label(master=frm_form, text='Verifying File')
lbl_verify.grid(row=24, column=0, padx=5, pady=5, sticky='w')

btn_open_file_verify = Button(master=frm_form, text='Open file', command=lambda: askOpenFile(2))
btn_open_file_verify.grid(row=25, column=1, padx=5, pady=5, sticky='w')

btn_open_signature = Button(master=frm_form, text='Open signature', command=lambda: askOpenFile(3))
btn_open_signature.grid(row=25, column=1, padx=5, pady=5, sticky='e')

btn_open_public_key = Button(master=frm_form, text='Open public key', command=lambda: askOpenFile(4))
btn_open_public_key.grid(row=26, column=1, padx=5, pady=5, sticky='w')

btn_reset = Button(master=frm_form, text='Reset', command=lambda: reset())
btn_reset.grid(row=26, column=1, padx=5, pady=5, sticky='e')

btn_verify = Button(master=frm_form, text='Verify')
btn_verify.grid(row=27, column=1, padx=5, pady=5, sticky='w')

lbl_verify_status = Label(master=frm_form, text='Status:')
lbl_verify_status.grid(row=28, column=0, padx=5, pady=5, sticky='w')

btn_exit = Button(master=frm_form, text='Exit', width=5, command=qExit)
btn_exit.grid(row=29, column=1, padx=5, pady=5, sticky='e')




# Keeps window alive 
window.mainloop()