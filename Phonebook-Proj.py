# Sharanya Gargula KsuID: 000954778
#Please update text file path accordingly
namesdict = {}  # to store uniqid, name(fn + " " +ln) format
numbersdict = {}  # to store phone numbers uniqid, phone numbers list
phlist = []


def main():
    readfromfile()
    print("************Welcome to my phone book. Please select one of the option.************")
    while True:
        if phonemenu() == -1:
            break
    writingtofile()


# To display phone book menu
def phonemenu():
    ch = input("""
1: Create new contact
2: Update contact
3: Delete contact
4: Search for contact
5. Display all contacts
0: Save and Quit
Please enter your choice: """)
    if ch == "1":
        createnewcontact()
    elif ch == "2":
        updatecontact()
    elif ch == "3":
        deletecontact()
    elif ch == "4":
        searchphcontacts()
    elif ch == "5":
        displaycontacts()
    elif ch == "0":
        return -1
    else:
        print("You should enter one of the given option 1,2,3,4,5 or 0.")
        print("Please try once again")
        print("****************************************************")
        phonemenu()


# To create new contact
def createnewcontact():
    fn = input("Enter First Name: ")
    ln = input("Enter Last Name: ")
    ph = input("Enter Phone number: ")
    if len(fn) != 0 and len(ln) != 0:
        fn = fn.rstrip(" ")
        name = fn + " " + ln
        name = name.upper()
    else:
        print("Mandatory to provide firstname and lastname.")
        print("****************************************************")
        return
    if name in namesdict.values():  # if name already exist in phone book, append the new contact
        uniqId = get_nameId(name)
        phlist = numbersdict[uniqId].copy()
        if len(phlist) < 3:  # to validate maximum  phone numbers should be 3
            if (ph in phlist):
                print("Phone number already exist.")
            else:
                phlist.append(ph)
                numbersdict[uniqId] = phlist.copy()
                print("Contact already existed. Phone number added to the contact.")
                print("****************************************************")
        else:
            print("Maximum 3 phone numbers reached for corresponding contact.")
            print("****************************************************")
    else:  # if contact is new
        uniqId = len(namesdict) + 1
        while uniqId in namesdict:
            uniqId += 1
        namesdict[uniqId] = name
        if len(ph) != 0:
            numbersdict[uniqId] = [ph]
        elif ph == "":
            numbersdict[uniqId] = []
        print("Contact created successfully.")
        print("****************************************************")


# To update existing contact.
def updatecontact():
    uniqidlist = []
    new_name = ""
    uniqId = 0
    print("Enter contact details to search..")
    fn = input("Enter first name: ")
    ln = input("Enter last name: ")
    ph = input("Enter phone number: ")
    if len(fn) != 0 or len(ln) != 0 or len(ph) != 0:
        uniqidlist = searchcontact(fn, ln, ph)  # returns list of matching contacts
    else:
        print("One of the value should be not null.")
        print("****************************************************")
        return
    if len(uniqidlist) != 0:  # validate matching contact list is not empty
        struniqId = input("Please enter Id of the corresponding contact to update.")
        if struniqId.isnumeric():
            uniqId = int(struniqId)
        else:
            print("Please enter correct Id.")
            return
        try:
            oldname = namesdict[uniqId]
        except KeyError:
            print("Invalid Id.")
            return
        fullnamelist = str.split(oldname, " ")  # to get firstname and last name seperately
        if uniqId in uniqidlist:
            fn = input("Enter New First Name: ")
            ln = input("Enter New Last Name: ")
            updatech = ""
            phlist = numbersdict[uniqId].copy()
            while not (updatech in ["1", "2", "3"]):  # iterates through given contact choice untill it's within list.
                updatech = input("Enter contact to be updated 1 or 2 or 3: ")
                if len(phlist) == 0 and updatech == "":
                    updatech = "1"
                    break
                elif len(
                        phlist) == 0 and updatech == "1":  # if phlist is empty and user given 1 as an option break loop
                    break
                elif updatech == "":
                    break
                elif int(updatech) > len(phlist):  # if user gives contactnumber which is not existed.
                    print("Invalid contact number given. Cannot update the contact.")
                    print("Please try again.")
                    updatech = "0"

            newph = input("Enter New Phone number: ")
            if len(fn) != 0 and len(ln) != 0:
                new_name = fn + " " + ln
            elif len(fn) == 0 and len(ln) == 0:
                new_name = fullnamelist[0] + " " + fullnamelist[1]
            elif len(fn) == 0 and len(ln) != 0:
                new_name = fullnamelist[0] + " " + ln
            elif len(ln) == 0 and len(fn) != 0:
                new_name = fn + " " + fullnamelist[1]
            new_name = new_name.upper()
            ch = input("Are you really want to update contact" + updatech + "Y/N: ")
            if ch.upper() != "Y":
                return
            if new_name in namesdict.values():
                print("Given name already exist.")
            elif len(new_name) != 0:
                namesdict[uniqId] = new_name
            if len(newph) != "":
                if updatech == "1":
                    if len(phlist) != 0:
                        phlist[0] = newph
                    else:
                        phlist = [newph]
                elif updatech == "2":
                    phlist[1] = newph
                elif updatech == "3":
                    phlist[2] = newph
                elif updatech == "":
                    if len(phlist) == 0:
                        phlist = [newph]
                    print(end=' ')
                else:
                    print("please enter one of the above given option.")
                    return
            numbersdict[uniqId] = phlist.copy()
            print("Contact updated successfully.")
            print("****************************************************")
        else:
            print("Invalid Id entered.")
            print("****************************************************")

    else:
        print("Invalid Id entered.")
        print("****************************************************")


# To delete contact from phone book
def deletecontact():
    print("Enter contact details to search..")
    fn = input("Enter first name: ")
    ln = input("Enter last name: ")
    ph = input("Enter phone number: ")
    uniqIdlist = []
    uniqId = 0
    if len(fn) != 0 or len(ln) != 0 or len(ph) != 0:
        uniqIdlist = searchcontact(fn, ln, ph)
    else:
        print("One of the value should be not null.")
        print("****************************************************")
        return
    if len(uniqIdlist) > 0:  # validate uniqid list is greater than 0 to makesure we have atleast one matching contact
        struniqId = input("Please enter Id of the corresponding contact to delete.")
        if struniqId.isnumeric():
            uniqId = int(struniqId)
        else:
            print("Please enter correct uniq id.")
            return
        if uniqId in uniqIdlist:  # to validate user entered correct uniqid
            updatech = 0
            phlist = numbersdict[uniqId].copy()
            while not (updatech in [1, 2, 3, 9]):
                strupdatech = input("Enter contact to be deleted 1 or 2 or 3 or 9 to delete entire contact: ")
                if strupdatech.isnumeric():
                    updatech = int(strupdatech)
                else:
                    print("Please enter correct Id.")
                    return
                if len(phlist) == 0 and updatech == 1:
                    break
                elif updatech != 9 and (updatech > len(phlist)):
                    print("Invalid contact given. Cannot delete the contact.")
                    print("****************************************************")
                    updatech = 0
                    return
                ch = input("Are you really want to delete contact" + "Y/N: ")
                if ch.upper() != "Y":
                    updatech = 0

            if updatech == 9:  # to delete entire contact from phone book
                try:
                    del namesdict[uniqId]
                    del numbersdict[uniqId]
                    print("Contact deleted successfully.")
                    print("****************************************************")
                except KeyError:
                    print("Key not found")
                    print("****************************************************")
            else:  # to delete subcontact for contact.
                phlist = numbersdict[uniqId]
                try:
                    del phlist[updatech - 1]
                    numbersdict[uniqId] = phlist.copy()
                    print("Contact deleted successfully.")
                    print("****************************************************")
                except KeyError:
                    print("Key not found")
                    print("****************************************************")
        else:
            print("Invalid Id entered.")
            print("****************************************************")
    else:
        print()


def searchphcontacts():
    fn = input("Enter first name: ")
    ln = input("Enter last name: ")
    ph = input("Enter phone number: ")
    if len(fn) != 0 or len(ln) != 0 or ph != "":
        searchcontact(fn, ln, ph)
    else:
        print("One of the value should be not null.")
    print("Search completed.")
    print("****************************************************")


# to search for contact based on atleast one of given parameter
# phone number has most highest prioriy, if we have phone number search based on phone number.
def searchcontact(firstname, lastname, phonenumber):
    uniqIdlist = []
    name_value = ""
    if len(phonenumber) != 0:  # if phone number is given, search is based on phone number.
        uniqId = get_phoneId(phonenumber)
        if uniqId == 'None':  # if phone doesnot exist
            print("No match found.")
        else:  # if matching contact exist
            uniqIdlist.append(uniqId)
            phlist = numbersdict[uniqId].copy()
            name = namesdict[uniqId]
            print("ID: " + str(uniqId), "FullName: " + name, end=' ')
            for ph in phlist:
                print(",contact" + str(phlist.index(ph) + 1) + ": " + str(ph), end=' ')
            print()
    else:  # if phone number is not given search is based on first name/last name
        if len(firstname) != 0 and len(lastname) != 0:
            name_value = firstname + " " + lastname
        elif len(firstname) != 0:
            name_value = firstname
        elif len(lastname) != 0:
            name_value = lastname
        name_value = name_value.upper()
        nameslist = [val for key, val in namesdict.items() if name_value in val]
        for name in nameslist:
            uniqId = get_nameId(name)
            uniqIdlist.append(uniqId)
            phlist = numbersdict[uniqId].copy()
            print("ID: " + str(uniqId), "FullName: " + name, end=' ')
            for ph in phlist:
                print(",contact" + str(phlist.index(ph) + 1) + ": " + str(ph), end=' ')
            print()
        if len(uniqIdlist) == 0:
            print("Did not find matching contacts.")
    return uniqIdlist


# to display all the contacts in phone book
def displaycontacts():
    print("*****Displaying all the contacts of phone book.*****")
    print("ID    ", "Name       ", "Phone    ")
    for uniqId in namesdict:
        try:
            print(uniqId, "   " + namesdict[uniqId], "     ", numbersdict[uniqId])
        except KeyError:
            print("Invalid Id.")
    print("****************************************************")


# to get the id from names dictionary based on input value
def get_nameId(inVal):
    for key, val in namesdict.items():
        if inVal == val:
            return key
    return "None"


# to get the id from phone numbers dictionary based on input value
def get_phoneId(inVal):
    for key, phlist in numbersdict.items():
        if inVal in phlist:
            return key
    return "None"


# write data phone book contacts to file.
def writingtofile():
    print("Saving data to file ")
    file = open(".\\contacts.txt", "w")  # Please update the path accordingly
    for id in namesdict:
        record = ""
        name = namesdict[id]
        record = str(id)
        record += ","
        record += name
        record += ","
        phlist = numbersdict[id]
        for num in phlist:
            record += num
            record += ","
        record = record.rstrip(",")
        if len(phlist) != 0:
            record += "\n"
        else:
            record += "\r"
        file.write(record)
        record = ""
    print("completed.")
    file.close()


# to read contacts from saved file if exist.
def readfromfile():
    try:
        myphlist = []
        uniqId = 0
        name = ""
        file = open(".\\contacts.txt", "r")  # Please update the path accordingly
        for record in file:
            datalist = str.split(record, ",")
            if len(datalist) > 0:
                uniqId = int(datalist[0])
                name = datalist[1]
                myphlist.clear()
                if len(datalist) == 5:
                    myphlist.append((datalist[2]).rstrip("\n"))
                    myphlist.append((datalist[3]).rstrip("\n"))
                    myphlist.append((datalist[4]).rstrip("\n"))
                elif len(datalist) == 4:
                    myphlist.append((datalist[2]).rstrip("\n"))
                    myphlist.append((datalist[3]).rstrip("\n"))
                elif len(datalist) == 3:
                    myphlist.append((datalist[2]).rstrip("\n"))
            name = name.rstrip("\n")
            namesdict[uniqId] = name
            numbersdict[uniqId] = myphlist.copy()
    except IOError:
        print("File not available to read contacts.")


main()
