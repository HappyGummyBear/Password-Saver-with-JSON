from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

#Fake email for the program
EMAIL = "kirk.faux.email@gmail.com"


# ---------------------------- SEARCH FOR PASSWORD AND EMAIL ------------------------------- #


def search_website():
    '''Function to search the json file. If website specified in the website entry exist then a message box will
    display the email and password for the the website'''

    find_website = website_text.get().lower()   #Get the entry from the website entry in lowercase to allow any
                                                                                                # form of entry
    try: #Try to open the file
        with open("data.json", "r") as data_file: #Open json file
            data = json.load(data_file) #Load data
    except FileNotFoundError: #Show messagebox if ile doesnt exist
        messagebox.showinfo(title="File not found",message="File does not exist")
    else: #Get email and password from the file
            try: #Try to get email and password from the file
                #Show a messagebox with information found
                messagebox.showinfo(title="Website found", message=f"Email: {data[find_website]['email']}\n"
                                                                   f" Password: {data[find_website]['password']}")
            except KeyError: #If website specified doesnt exist
                #Show a message box telling the user the input is wrong
                messagebox.showinfo(title="Website not found", message="That website does not exist on the file")
            finally: #No matter what clear, the website entry
                website_text.delete(0, END)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    '''Function that will use list of character to create a unique password'''

    #Clears password incase it is not empty
    password_text.delete(0, END)

    # List of chars for password generator
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
               'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    #List comprehention to create list for number, symbols, and letters for the generated password
    password_letter = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_number = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_symbol = [random.choice(symbols) for _ in range(random.randint(2, 4))]


    password_list = password_letter + password_number + password_symbol

    #Rearrange the lists in password_list
    random.shuffle(password_list)
    #Join all the lists into one string
    password = "".join(password_list)
    #Copy the password to user clipboard
    pyperclip.copy(password)
    password_text.insert(END, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_info():
    '''Function to save info on the GUI to the CSV file'''
    #Get information from users entries to the program
    website = website_text.get()
    email = email_text.get()
    password = password_text.get()
    new_dict = {
        website.lower():{
            "email": email,
            "password": password
        }
    }
    #Checks if any input is blank and shows a message indicating user to fix the issue
    if len(website) < 1 or len(password) < 1:
        messagebox.showerror(title="Something is missing...", message="Don't leave any fields empty!")
    else:
        try: #Try to open json file if it exist
            with open("data.json", "r") as data_file: #Opens file in read mode
                data_json = json.load(data_file) #Load the file
        except FileNotFoundError: #If file doesn't exist
            with open("data.json", "w") as data_file: #Create the file in write mode
                json.dump(new_dict, data_file, indent=4) #Add data to the file
        else: #If file exist
            with open("data.json", "w") as data_file: #Open file in write mode
                data_json.update(new_dict)  # Update the file with the new entry
                json.dump(data_json, data_file, indent=4) #Write the new data to the file
        finally:
            #Clears the inputs for new entry except for email
            website_text.delete(0,END)
            password_text.delete(0,END)

            website_text.focus()


# ---------------------------- UI SETUP ------------------------------- #

#Create window for GUI
window = Tk()
window.title("Password Manager")
window.config(padx=30, pady=30)

#Canvas to hold the logo of the program
canvas = Canvas(width=200, height=200, highlightthickness=0)
lock_photo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_photo)
canvas.grid(column=1, row=0)

#Label for user to know where to input website
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

#Space for user to enter website for storage
website_text = Entry(width=32)
website_text.focus()
website_text.grid(column=1, row=1, columnspan=1)

#Label for user to know where to input email or username
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

#Space for user to enter email/username
email_text = Entry(width=50)
email_text.insert(END, EMAIL)
email_text.grid(column=1, row=2, columnspan=2)

#Label for user to know where to enter password
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

#Space for user to enter password
password_text = Entry(width=32)
password_text.grid(column=1, row=3)

#Button that will call the generate_password function and create a password
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3)

#Button that will call add_info and save it to a file
add_button = Button(text="Add", width=43, command=add_info)
add_button.grid(column=1, row=4, columnspan=2)

#Button that will search for the email and password for the website specified
search_button = Button(text="Search", width=14, command=search_website)
search_button.grid(column=2, row=1, columnspan=2)

#Function to keep window open
window.mainloop()
