from colorama import Fore, init
from msvcrt import getch
import sqlite3 as lite
import pyperclip
import random
import string

#Colorama init()
init(autoreset=True)

#Sqlite setup
db = lite.connect("password.db")
ex = db.cursor()
#Create table if not exists
ex.execute("CREATE TABLE IF NOT EXISTS passwords (app VARCHAR NOT NULL PRIMARY KEY, password VARCHAR NOT NULL)")

#Start Message
print(Fore.GREEN + "Welcome to Password Basement")
print("Password Basement is a application that creates specific passwords for every Website/app you want.\n")
print(Fore.YELLOW + "1) Add Password")
print(Fore.YELLOW + "2) Registered Passwords")
print(Fore.YELLOW + "3) Delete Record")
print(Fore.RED + "4) EXIT\n")

exit = False

while not exit:
	selection = input("Enter a operation: ")

	#Add Password
	if (selection == "1" or selection.lower() == "add password" or selection == "1) Add Password"):
		app = input("\nSelect Website/App name you want to create password: ")
		
		digitCorrect = False
		while not digitCorrect:
			try:
				length = int(input("How many digits you want to set in password: "))
				if (length < 1):
					print(Fore.RED + "Digit count is not valid, you have to enter a positive number.")
					digitCorrect = False
				else:
					digitCorrect = True
			except:
				print(Fore.RED + "Digit count is not valid")
				digitCorrect = False

		password = ''.join(random.SystemRandom().choice("."+","+"İ"+"Ğ"+"/"+"@"+"#"+"!" + string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(length))
		print("\n"+app+":"+Fore.GREEN+password)
		#Confirm operation
		confirm = input("Do you confirm it [Y/N]: ")
		if (confirm == "y" or confirm == "Y"):
			#Add datas to database
			try:
				ex.execute("INSERT INTO passwords VALUES (?, ?)",(app,password))
				print(Fore.GREEN+"Operation completed successfully.\n")
			except:
				#If website/app name already exists
				print(Fore.RED+"There is a problem while adding values to database.\n")
		else:
			print(Fore.GREEN + "Operation cancelled\n")

	#Registered Passwords
	elif (selection == "2" or selection.lower() == "registered password" or selection == "2) Registered Passwords"):
		#Get app names from database
		ex.execute("SELECT app FROM passwords")
		app_datas = ex.fetchall()

		if len(app_datas):
			for app_data in app_datas:
				#Print records
				print(Fore.YELLOW+app_data[0])

			#Record that will shown its password
			user_app = input("\nEnter app name: ")

			valid_user_data = False

			for app_data in app_datas:
				if user_app == app_data[0]:
					valid_user_data = True
					ex.execute("SELECT password FROM passwords WHERE app=?",(app_data[0],))
					app_password = ex.fetchone()
					print("Password: "+Fore.GREEN+app_password[0]+"\n")
					will_copy = input("Do you want to copy password to clipboard [Y/N]: ")
					if will_copy == "Y" or will_copy == "y":
						try:
							#Copy password
							pyperclip.copy(app_password[0])
							print(Fore.YELLOW+"Password has copied to clipboard!\n")
						except:
							print(Fore.RED+"An error has occurred while copying the password to clipboard.\n")
					break
			if not valid_user_data:
				print(Fore.RED+"Website/App can't be found!\n")
		else:
			print(Fore.YELLOW+"There is no password data\n")

	elif (selection == "3" or selection.lower() == "delete Record" or selection == "3) Delete Record"):
		#Get app names from database
		ex.execute("SELECT app FROM passwords")
		app_datas = ex.fetchall()

		if len(app_datas):
			for app_data in app_datas:
				#Print records
				print(Fore.YELLOW+app_data[0])
			#App that will be deleted
			delete_app = input("\nEnter the app name that will be deleted: ")
			for app_data in app_datas:
				if delete_app == app_data[0] or delete_app == app_data[0].lower():
					delete_confirm = input("Are you sure [Y/N]: ")
					if delete_confirm == "Y" or delete_confirm == "y":
						try:
							ex.execute("DELETE FROM passwords WHERE app=?",(app_data[0],))
							print(Fore.YELLOW+"Record Deleted!\n")
						except:
							print(Fore.RED+"An error occurred while deleting record!\n")

					else:
						print(Fore.YELLOW+"Operation cancelled!\n")
		else:
			print(Fore.YELLOW+"There is no password data")

	elif (selection == "4" or selection == "EXIT" or selection == "4) EXIT" or selection == "exit" or selection == "close"):
		exit = True

	else:
		print(Fore.RED + "Please enter a valid operation.\n")

#Close Database and commit operations
db.commit()
db.close()

print(Fore.GREEN + "Thank you for using Password Basement"); getch()