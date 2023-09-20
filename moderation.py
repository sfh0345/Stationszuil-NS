import csv

file_path = 'input.csv'
accepted_file_path = 'accepted_feedback.csv'
denied_file_path = 'denied_feedback.csv'


def extract_feedbacks(file_path):
    feedbacks = []

    with open(file_path, 'r') as csvfile:
        lines = csvfile.readlines()

        feedback = []
        inside_feedback = False

        for line in lines:
            if line.strip() == '-------------------------------------------------------------':
                if inside_feedback:
                    feedbacks.append(feedback)
                    feedback = []
                    inside_feedback = False
                else:
                    inside_feedback = True
            elif inside_feedback:
                feedback.append(line.strip())

        if inside_feedback and feedback:
            feedbacks.append(feedback)

    return feedbacks


def print_feedback(feedback):
    print('Feedback:')
    for line in feedback:
        print(line)

    print()  # Separate feedbacks with a blank line


def write_to_file(file_path, feedbacks):
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for feedback in feedbacks:
            # Add separator before feedback
            writer.writerow(['-------------------------------------------------------------'])

            # Write the feedback
            for line in feedback:
                writer.writerow([line])

            # Add separator after feedback
            writer.writerow(['-------------------------------------------------------------'])


def confirm_feedback(feedback):
    print_feedback(feedback)
    while True:
        choice = input("Do you confirm this feedback? (yes/no): ").lower()
        if choice in ['yes', 'no']:
            return choice == 'yes'
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")


feedbacks = extract_feedbacks(file_path)

# Print the first feedback and ask for confirmation
if feedbacks:
    if confirm_feedback(feedbacks[0]):
        # If confirmed, append the feedback to the accepted feedback file
        accepted_feedbacks = [feedbacks[0]]
        write_to_file(accepted_file_path, accepted_feedbacks)

        # Remove the feedback from the original file
        with open(file_path, 'r') as f:
            lines = f.readlines()

        with open(file_path, 'w') as f:
            feedback_started = False
            feedback_to_delete = False
            for line in lines:
                if line.strip() == '-------------------------------------------------------------':
                    feedback_started = not feedback_started
                    if feedback_started:
                        feedback_to_delete = True
                        continue
                    if not feedback_started and feedback_to_delete:
                        feedback_to_delete = False
                        continue
                if not feedback_to_delete:
                    f.write(line)
    else:
        # If denied, append the feedback to the denied feedback file
        denied_feedbacks = [feedbacks[0]]
        write_to_file(denied_file_path, denied_feedbacks)

        # Remove the feedback from the original file
        with open(file_path, 'r') as f:
            lines = f.readlines()

        with open(file_path, 'w') as f:
            feedback_started = False
            feedback_to_delete = False
            for line in lines:
                if line.strip() == '-------------------------------------------------------------':
                    feedback_started = not feedback_started
                    if feedback_started:
                        feedback_to_delete = True
                        continue
                    if not feedback_started and feedback_to_delete:
                        feedback_to_delete = False
                        continue
                if not feedback_to_delete:
                    f.write(line)
else:
    print('No feedback found in the CSV file.')
