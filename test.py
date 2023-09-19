import csv

# Function to get user input within the character limit
def get_user_input():
    while True:
        user_input = input("Enter text (max 140 characters): ")
        if len(user_input) <= 140:
            return user_input
        else:
            print("Input exceeds the character limit. Please try again.")

# Get user input
user_text = get_user_input()

# Write the input to a CSV file
csv_file_path = 'user_input.csv'

with open(csv_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['User Input'])
    writer.writerow([user_text])

print(f'User input written to {csv_file_path}.')
