"""
***PHONEBOOK MANAGEMENT SYSTEM ON PYTHON***
==> Use menu to navigate around program

############################
1) Sorting doesnot work if the initial of the name is small letter => fixed
2) Added date needs some more work => fixed
3) Searching is still left to improve => fixed
4) CSV is only written to if exit is selected on menu => fixed data is saved once it is added or deleated
Coded by sadikshapokharel
"""


from csv import DictReader,  DictWriter
from datetime import datetime

filename = "phonebook_python.csv"

def add_item(phonebook, *, name, number, email, addedOn):
    bookitem = {"fullname": "", "number": "", "email": "", "addedOn": ""}
    bookitem["fullname"] = name
    bookitem["number"] = number
    bookitem["email"] = email
    bookitem["addedOn"] = addedOn

    isDataAlreadyExist, index = is_duplicate(phonebook, name, number)

    if isDataAlreadyExist:
    	phonebook[index] = bookitem
    else:
    	phonebook.append(bookitem)
        
def search_item(phonebook, keyword):
    for index, item in enumerate(phonebook):
            
        if keyword in item["fullname"] or keyword in item["number"] or keyword in ["email"]:
            print("Record Found: Name:{}\tNumber:{}\tEmail:{} Index: {}".format(item["fullname"], item["number"], item["email"], index))
                    

def is_duplicate(phonebook, name, number):
    for index, item in enumerate(phonebook):
            if name == item["fullname"] and number == item["number"]:
                    print("Data already exist, overwriting on that ")
                    return (True, index)
    
    return (False, -1)
        
def list_items(phonebook):
    print("***Sorted on the basis of Fullname***")
    print("Sn\tFullname\tPhoneNumber\tEmail\t\t Added On")
    print("=" * 70)
    i =0
    for item in phonebook:
        i += 1
        print("{}\t{} | \t {} | \t {}\t | {}".format(i, item["fullname"], item["number"], item["email"], item["addedOn"]))

    print("=" * 70)
        
def add_action():
        
    items = []

    while True:
        while True:
            fullname = input("Enter name: ").capitalize()
            if fullname != "":
            	break
            print("Error: Name cannot be empty/null")

        if not fullname.strip():
                print("Fullname cannnot be empty. Please Continue")
                continue

        
        while True:
            ph_number = input("Enter Phone Number: ")
            if ph_number != "":
           		break
            print("Error: Phone number cannot be empty/null")


        while True:
            email = input("Enter Email: ")
            if email != "":
                    break
            print("Error: Email cannot be empty/null")

        dt = datetime.now()
        addedOn = dt.strftime("%Y-%m-%d %H:%M:%S")



        items.append((fullname, ph_number, email, addedOn))

        char = input("Press [y/yes] if you want to continue]: ")

        if not (char.lower() == "y" or char.lower() == "yes"):
            break
    return items

def update_item():
    pass
        
def write_to_csv(phonebook, filename):
    with open(filename, "w+") as csvfile:
        writer = DictWriter(csvfile, fieldnames = ["fullname", "number", "email", "addedOn"])
        writer.writeheader()
        for each in phonebook:
            writer.writerow(each)
    
def cli():
    global filename
    phonebook = [ ]

    try:
        with open(filename, "r") as csvfile:
            reader = DictReader(csvfile,  fieldnames = ["fullname", "number", "email", "addedOn"])

            try:     
                next(reader)
                phonebook.extend(reader)

            except (StopIteration):
                print("The file is empty")
    
    except (FileNotFoundError, IOError):
        print("File not found creating one")  

        with open(filename, "w") as csvfile:
            writer = DictWriter(csvfile, fieldnames = ["fullname", "number", "email", "addedOn"])
            writer.writeheader()

    while True:
        print("""
        A: Add
        L: List
        S: Search
        R: Remove
        U: Update
        E: Exit
        """ )

        action = input("Please select a action: ")

        if action.upper() == "A":
            collected_items = add_action()

            for name, number, email,addedOn in collected_items:
                add_item(phonebook, name=name, email=email, number=number, addedOn=addedOn)

            write_to_csv(phonebook, filename)

        elif action.upper() == "L":
            phonebook = sorted(phonebook, key=lambda k: k['fullname']) #sorting on basis of fullname
            list_items(phonebook)

        elif action.upper() == "S":
            '''
            print("""
          1. Search by Name
          2. Search by Number
          3. Search by Email
          """)
            ch = input("What do you want to search by? : ")'''

            keyword = input("'Enter a keyword to search: ")
            search_item(phonebook,keyword)

        elif action.upper() == "R":
            list_items(phonebook)
            keyword = input("Enter SN to remove: ")

            try:
                phonebook.pop(int(keyword) - 1) # Removing Data using index 
                list_items(phonebook)
                write_to_csv(phonebook, filename)

            except (IndexError):
                print("The SN as not found. Please select a valid Serial Number. ")
                continue

        elif action.upper() == "U":
        	list_items(phonebook)
        	up = input("Enter SN to update: ")

        	try:
        		while True:

		        	print("""
		        		N: Name
		        		P: Phone no
		        		E: Email
		        		""")

		        	action = input("Please select an action: ")


		        	if action.upper() == "N":
		        		phonebook[int(up)-1]['fullname'] = input("Enter new name: ")
		        	elif action.upper() == 'P':
		        		phonebook[int(up)-1]['number'] = input("Enter new number: ")
		        	elif action.upper() == 'E':
		        		phonebook[int(up)-1]['email'] = input("Enter new email: ")


		        	check = input("Press [y] if you want to continue update this contact: ")
		        	if not check.lower() == "y":
		        		break

		        write_to_csv(phonebook, filename)
        	except (IndexError):
        		print("The SN as not found. Please select a valid Serial Number. ")
        		continue

        	

        elif action.upper() == "E":
            break
        else:
            print("Invalid action selected")
                        
if __name__ == "__main__":
	cli()

