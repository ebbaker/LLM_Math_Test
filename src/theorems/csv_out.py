import csv

def create_csv(file_name):
    # Define column names
    fieldnames = ['thm_name', 'proof_steps', 'thm_solved', 'num_hints', 'compiler_responses', 'notes']
    # Create a new csv file
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write the header row
        writer.writeheader()

def add_new_csv_line(file_name, thm_name, proof_steps, thm_solved, num_hints, compiler_responses, notes):
    # Define column names
    fieldnames = ['thm_name', 'proof_steps', 'thm_solved', 'num_hints', 'compiler_responses', 'notes']
    # Open the existing csv file in append mode ('a')
    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write a new row with provided values
        writer.writerow({
            'thm_name': thm_name,
            'proof_steps': proof_steps,
            'thm_solved': thm_solved,
            'num_hints': num_hints,
            'compiler_responses': compiler_responses,
            'notes': notes,
        })

