import pandas as pd
import random
import csv

# Function to ask yes or no
def yes_or_no(question):
    reply = input(question + ' (yes/no): ').strip().lower()
    if reply in ('yes', 'no'):
        return reply == 'yes'
    else:
        exit()

df = None

# Ask the user which file they want to manipulate
while True:
    file = input("Please enter an option ('usuarios', 'citas' o 'rutinas'): ")
    if file.lower() in ['usuarios', 'citas', 'rutinas']:
        if file == "usuarios":
            print("Manipulating users\n")
            df = pd.read_csv("csv/users.csv", quoting=csv.QUOTE_MINIMAL)
        elif file == "citas":
            print("Manipulating appointments\n")
            df = pd.read_csv("csv/citas.csv", quoting=csv.QUOTE_MINIMAL)
        elif file == "rutinas":
            print("Manipulating routines\n")
            df = pd.read_csv("csv/rutinas.csv", quoting=csv.QUOTE_MINIMAL)
        break
    else:
        print("Invalid option. Please enter 'usuarios', 'citas' or 'rutinas'.")

# Remove trailing spaces and replace null values
if yes_or_no("Do you want to remove spaces and replace null values?"):
    df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
    reply = input("What do you want to replace them with?: ")
    df.fillna(reply, inplace=True)

# Replace specific characters
if yes_or_no("Do you want to replace specific characters?"):
    reply = input("Enter the character to replace: ")
    new_reply = input("Enter the new character: ")
    df.replace(reply, new_reply, regex=True, inplace=True)

# List of European countries
european_countries = [
    "Germany", "France", "Italy", "Spain", "Portugal", "Netherlands",
    "Belgium", "Greece", "Sweden", "Norway", "Finland", "Denmark",
    "Switzerland", "Austria", "Ireland", "Poland", "Hungary", "Czech Republic",
    "Slovakia", "Romania", "Bulgaria", "Croatia", "Slovenia", "Estonia",
    "Latvia", "Lithuania", "Malta", "Cyprus", "Luxembourg"
]

#Create a new column with a random European country
if yes_or_no("Do you want to create a new column?"):
    if file == "usuarios":
        df['pais'] = [random.choice(european_countries) for _ in range(len(df))]
    elif file == "citas":
        df['dia_semana'] = pd.to_datetime(df['fechaCita']).dt.day_name()
    elif file == "rutinas":
        print("Cannot create a new column in the routines file\n")
        print("Instead, the 'excercise' column will be deleted\n")
        df = df.drop(columns=['exercises'])

# Rename the 'id' column to '(file name) id'
if yes_or_no("Do you want to rename a column?"):
    if file == "usuarios":
        df.rename(columns={'id': 'Usuarios id'}, inplace=True)
    elif file == "citas":
        df.rename(columns={'id': 'Citas id'}, inplace=True)
    elif file == "rutinas":
        df.rename(columns={'id': 'Rutinas id'}, inplace=True)

output_file_path_with_title = file + '_manipulados.csv'

# Save the DataFrame with the new column name and title, without additional blank lines
if yes_or_no("Do you want to save the processed file?"):
    # Save the file with the title in uppercase
    with open(output_file_path_with_title, 'w', newline='') as f:
        if yes_or_no ("Do you want to add a title?"):
            reply = input("Enter the title: ")
            f.write(reply + '\n')
            # Create a CSV writer with the desired format
            df.to_csv(f, quoting=csv.QUOTE_MINIMAL, index=False)
            exit()
        else :
            # Create a CSV writer with the desired format
            df.to_csv(f, quoting=csv.QUOTE_MINIMAL, index=False)
            exit()

else:
    print("Process finished without saving the file.")
    exit()
