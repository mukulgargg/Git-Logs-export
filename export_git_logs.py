import os
import subprocess

import pandas as pd


# Function to process a single line of commit log
def process_commit_line(line):
    parts = line.split()
    project_name = parts[0]
    commit_id = parts[1]
    day = parts[2]
    month_date = parts[4] + "/" + parts[3] + "/" + parts[6]
    timestamp = parts[5]
    year = parts[6]
    timezone = parts[7]
    message = " ".join(parts[9:-2])
    lines_added = parts[-2]
    lines_removed = parts[-1]

    return [project_name, commit_id, day, month_date, timestamp, year, timezone, message, lines_added, lines_removed]


# Function to read the file, process each line, and create a DataFrame
def create_commit_df(file_path):
    structured_data = []
    with open(file_path, 'r') as file:
        for line in file:
            if (len(line.strip().split()) > 1):
                structured_data.append(process_commit_line(line.strip()))

    # Convert structured data into a DataFrame
    columns = ["Project", "Commit ID", "Day", "Month", "Timestamp", "Year", "Time Zone", "Message", "Lines Added",
               "Lines Removed"]
    df_commits = pd.DataFrame(structured_data, columns=columns)
    return df_commits


# Function to execute sh file and store output to a file
def execute_shell_script(script_path, file_path, param1, param2):
    try:
        result = subprocess.run(["bash", script_path, param1, param2], check=True, capture_output=True, text=True)

        with open(file_path, "w") as f:
            f.write(result.stdout)

        if result.stderr:
            f.write("\nScript Error Output:\n")
            f.write(result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"Error executing the script: {e}")
        print(f"Exit code: {e.returncode}")
        print(f"Output: {e.output}")


script_path = "gitLogs.sh"
file_path = 'out.txt'
# taking data inputs
param1 = input("Enter from date in format yyyy-mm-dd: ")
param2 = input("Enter to date in format yyyy-mm-dd: ")
execute_shell_script(script_path, file_path, param1, param2)

df_commits = create_commit_df(file_path)

# deleting text file
if os.path.exists(file_path):
    os.remove(file_path)
# Save to Excel file
excel_file_path = 'structured_commit_logs.xlsx'
df_commits.to_excel(excel_file_path, index=False)

print(f'Logs are saved to: {excel_file_path}')
