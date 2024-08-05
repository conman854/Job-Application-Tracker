from datetime import date
import sys

nextId = 0

print ("""=== Welcome to the Job Application Tracker ===
Enter command or type \"HELP\" for list of commands.\n""")

"""
Command list:

- Add new app
- Remove app
- Get stats
- Update status

Application Properties:

- Date applied
- Employer name
- Role
- App status

"""

class Application:
    date = []
    employer = ""
    role = ""
    status = 0
    id = 0

    def __init__(self, id, employer, role, day, status = '0'):
        self.id = id
        self.employer = employer
        self.role = role
        self.status = status
        if day == 'today':
            today = date.today()
            self.date = today.strftime("%m/%d/%Y").split('/')
        else:
            self.date = day.split('/')

    def __str__(self):
        status = self.status
        if status == '0': 
            statstr = "No Response"
        elif status == '1': 
            statstr = "Rejected"
        elif status == '2': 
            statstr = "Interview"
        else: 
            statstr = "Offer"

        return ("%s\n%s\nApplied: %s/%s/%s\nStatus: %s\n" % (self.employer, self.role, self.date[0], self.date[1], self.date[2], statstr))

    def updateStatus(self, status):
        # Updates status to represent application status. 0 = No Response, 1 = Rejection, 2 = Interview, 3 = Offered

        self.status = status
    
def getData(filename):
    global nextId
    file = open(filename, "r")
    line = file.readline()
    data = []

    while line:
        line = line[:-1]
        parms = line.split("|")
        app = Application(parms[0], parms[1], parms[2], parms[3], parms[4])
        data.append(app)
        if int(parms[0]) >= nextId:
            nextId = int(parms[0]) + 1
        line = file.readline()

    file.close()
    return data

def appSearch(data, search):
    results = []
    search = search.lower()
    for app in data:
        if search in app.employer.lower() or search in app.role.lower():
            results.append(app)
    
    return results

def singleSearch(data):
    inp = input("\nSearch for employer or job title: ")
    result = appSearch(data, inp)

    if len(result) == 0:
        print('\nNo matching applications found.')
        return 'N'
    elif len(result) == 1:
        return result[0]
    else:
        print('Multiple applications containing "%s" were found:\n\n' % inp)
        for i in range(0, len(result)):
            print("Application #%d:\n%s" % (i + 1, str(result[i])))
        
        inp = input('\nEnter the application number of the desired application: ')
        while True:
            try:
                inp = int(inp)
            except:
                inp = 0
            
            if inp < 1 or inp > len(result):
                inp = input('Invalid input. Enter one of the application numbers above: ')
                continue

            break

        return result[inp - 1]
    
def save(data):
    file = open('JobAppData.txt', 'w')
    savedata = ''

    for app in data:
        day = app.date[0] + '/' + app.date[1] + '/' + app.date[2]
        savedata = savedata + str(app.id) + '|' + app.employer + '|' + app.role + '|' + day + '|' + app.status + '\n'
    
    file.write(savedata)

data = getData("JobAppData.txt")

command = input('>>> ').lower()

saved = True

while True:
    if command == 'help':
        print("""\nList of valid commands:\n
              - Help    | Gives list of valid commands
              - Add     | Add a new application
              - Display | Show all submitted applications
              - Update  | Update the status of an application
              - Search  | Find applications
              - Data    | Shows statistics related to hte job search
              - Save    | Save changes and overwrite previous data
              - Remove  | Remove an application from the list
              - Reset   | Remove ALL applications from the list
              - Exit    | Leave the program""")
        
    elif command == 'add':
        employer = input("\nEnter employer name: ").replace('|','')
        role = input("Enter job title: ").replace('|','')
        day = input('Enter application data (Enter "today" or "mm/dd/yyyy"): ').lower().replace('|','')

        while True:
            if day == 'today':
                break

            try:
                datesplit = day.split('/')
                if len(datesplit) != 3:
                    raise Exception
                
                m = int(datesplit[0])
                d = int(datesplit[1])
                y = int(datesplit[2])

                if m < 1 or m > 12 or d < 1 or d > 31 or y < 1:
                    raise Exception
                if (m in [4, 6, 9, 11] and d > 30) or (m == 2 and d > 29):
                    raise Exception
            except:
                day = input('Invalid input. Enter a valid date in the format "mm/dd/yyyy" or enter "today": ')
                continue
            
            break

        app = Application(nextId, employer, role, day)
        
        data.append(app)
        print("\nApplication added!\n")
        print(app)
        
        nextId += 1
        saved = False

    elif command == 'display':
        if len(data) == 0:
            print('There are no applications to display. Use the "add" command to add a new application.')
            command = input('\n>>> ').lower()
            continue

        print('\n')
        for app in data:
            print(str(app) + '\n')

    elif command == 'update':
        if len(data) == 0:
            print('There are no applications to update. Use the "add" command to add a new application.')
            command = input('\n>>> ').lower()
            continue

        app = singleSearch(data)
        if app == 'N':
            command = input('\n>>> ').lower()
            continue

        print('\nApplication Found!\n')
        print(app)
        
        inp = input('Status Options:\n0 - No Response\n1 - Rejected\n2 - Interview\n3 - Offer\n\nEnter new status: ')
        while True:
            if inp == '0' or inp.lower() == 'no response':
                app.status = '0'
            elif inp == '1' or inp.lower() == 'rejected':
                app.status = '1'
            elif inp == '2' or inp.lower() == 'interview':
                app.status = '2'
            elif inp == '3' or inp.lower() == 'offer':
                app.status = '3'
            else:
                inp = input('Invalid input. Try again: ')
                continue

            break

        print('\nUpdate Successful!\n')
        saved = False
        print(app)

    elif command == 'search':
        if len(data) == 0:
            print('There are no applications to search for. Use the "add" command to add a new application.')
            command = input('\n>>> ').lower()
            continue

        inp = input('\nSearch for employer name or job title: ')
        result = appSearch(data, inp)

        if len(result) == 0:
            print('\nNo applications containing "%s" were found.' % (inp))
        elif len(result) == 1:
            print('\nApplication found:\n%s' % (result[0]))
        else:
            print('\n%d Applications containing "%s" were found:\n' % (len(result), inp))
            for app in result:
                print(app)

    elif command == 'data':
        if len(data) == 0:
            print('There are no applications to show data for. Use the "add" command to add a new application.')
            command = input('\n>>> ').lower()
            continue

        print('\nJob search statistics:\n')

        total = len(data)
        no, reject, inter, offer = 0, 0, 0, 0
        for app in data:
            if app.status == '0':
                no += 1
            elif app.status == '1':
                reject += 1
            elif app.status == '2':
                inter += 1
            else:
                offer += 1
        
        print('Total Applications: %d' % (total))
        print('%.2f%% No Response' % (100 * no / total))
        print('%.2f%% Rejection' % (100 * reject / total))
        print('%.2f%% Interview' % (100 * inter / total))
        print('%.2f%% Offer' % (100 * offer / total))

    elif command == 'save':
        save(data)
        saved = True
    
    elif command == 'remove':
        if len(data) == 0:
            print('There are no applications to remove. Use the "add" command to add a new application.')
            command = input('\n>>> ').lower()
            continue

        app = singleSearch(data)
        if app == 'N':
            command = input('\n>>> ').lower()
            continue

        print('\nApplication Found!\n')
        print(app)
        inp = input('Remove Application?: ')
        inp = inp.lower()

        while inp != 'y' and inp != 'yes' and inp != 'n' and inp != 'no':
            inp = input('Invalid input. Answer "yes" or "no": ')
            inp = inp.lower()
        
        if inp == 'y' or inp == 'yes':
            data.remove(app)
            print('Application removed!')
            saved = False

    elif command == 'reset':
        print('\n===== WARNING =====\nYou are about to permanately delete all existing job applications.\nThis cannot be undone.')
        inp = input('\nAre you sure you want to do this?: ')

        while inp != 'y' and inp != 'yes' and inp != 'n' and inp != 'no':
            inp = input('Invalid input. Answer "yes" or "no": ')
            inp = inp.lower()
        
        if inp == 'y' or inp == 'yes':
            file = open('JobAppData.txt', 'w')
            file.close()
            data = []
            saved = True

    elif command == 'exit':
        if saved:
            sys.exit()
        
        print('You have made unsaved changes to the application list.')
        inp = input('Do you want to save before exiting?: ')

        while inp != 'y' and inp != 'yes' and inp != 'n' and inp != 'no':
            inp = input('Invalid input. Answer "yes" or "no": ')
            inp = inp.lower()
        
        if inp == 'y' or inp == 'yes':
            save(data)

        sys.exit()

    else:
        print('Invalid command. Use the "help" command to view all valid commands.')

    command = input('\n>>> ').lower()







