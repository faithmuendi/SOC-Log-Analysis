import pandas as pd
import re

# Path to the log file
log_file_path = "logs/auth.log"

# Read the log file
try:
    with open(log_file_path, "r") as file:
        logs = file.readlines()
except FileNotFoundError:
    print(f"Error: Log file '{log_file_path}' not found.")
    exit()

# Define a pattern to extract failed login attempts
failed_login_pattern = re.compile(r"Failed password for (\w+) from (\d+\.\d+\.\d+\.\d+)")

# Store extracted data
failed_attempts = []

for line in logs:
    match = failed_login_pattern.search(line)
    if match:
        username = match.group(1)
        ip_address = match.group(2)
        failed_attempts.append({"Username": username, "IP Address": ip_address})

# Convert to DataFrame
df = pd.DataFrame(failed_attempts)

# Display summary
if not df.empty:
    print("\nSummary of Failed Login Attempts:")
    print(df.value_counts().reset_index().rename(columns={0: "Count"}))
else:
    print("\nNo failed login attempts found.")

# Save results to CSV
df.to_csv("failed_logins.csv", index=False)
print("\nResults saved to 'failed_logins.csv'.")
