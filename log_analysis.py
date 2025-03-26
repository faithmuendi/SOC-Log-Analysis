import re  # Regular expressions for pattern matching
import pandas as pd  # Data analysis library
import matplotlib.pyplot as plt  # Data visualization
import seaborn as sns  # Enhancing plots

# Define log file path
log_file = "logs/auth.log"

# Define regex patterns for failed and successful logins
failed_login_pattern = r"Failed password for (invalid user )?(\S+) from (\d+\.\d+\.\d+\.\d+)"
successful_login_pattern = r"Accepted password for (\S+) from (\d+\.\d+\.\d+\.\d+)"

# Initialize lists to store login attempts
failed_logins = []
successful_logins = []

# Open and read the log file
with open(log_file, "r") as file:
    for line in file:
        failed_match = re.search(failed_login_pattern, line)
        success_match = re.search(successful_login_pattern, line)

        if failed_match:
            username = failed_match.group(2)  # Extract username
            ip_address = failed_match.group(3)  # Extract IP address
            failed_logins.append((username, ip_address))  # Add to list

        if success_match:
            username = success_match.group(1)  # Extract username
            ip_address = success_match.group(2)  # Extract IP address
            successful_logins.append((username, ip_address))  # Add to list

# Convert to DataFrames
df_failed = pd.DataFrame(failed_logins, columns=["Username", "IP Address"])
df_success = pd.DataFrame(successful_logins, columns=["Username", "IP Address"])

# **Enhancement 1: Count failed/successful login attempts per user/IP**
df_failed_count = df_failed.groupby(["Username", "IP Address"]).size().reset_index(name="Attempts")
df_success_count = df_success.groupby(["Username", "IP Address"]).size().reset_index(name="Attempts")

# Save results to CSV files
df_failed_count.to_csv("failed_logins.csv", index=False)
df_success_count.to_csv("successful_logins.csv", index=False)

# Print Summary
print("\n🔴 **Failed Logins Summary:**")
print(df_failed_count.sort_values(by="Attempts", ascending=False).head(10))  # Show top 10 attackers

print("\n🟢 **Successful Logins Summary:**")
print(df_success_count.sort_values(by="Attempts", ascending=False).head(10))  # Show top 10 successful logins

# **Enhancement 2: Data Visualization**
plt.figure(figsize=(12, 6))

# Bar plot for failed logins
sns.barplot(x="IP Address", y="Attempts", hue="Username", data=df_failed_count.sort_values(by="Attempts", ascending=False).head(10))
plt.xlabel("IP Address")
plt.ylabel("Failed Login Attempts")
plt.title("Top 10 Most Attacked Usernames/IPs")
plt.xticks(rotation=45)
plt.savefig("failed_logins_plot.png")
plt.show()

# Bar plot for successful logins
plt.figure(figsize=(12, 6))
sns.barplot(x="IP Address", y="Attempts", hue="Username", data=df_success_count.sort_values(by="Attempts", ascending=False).head(10))
plt.xlabel("IP Address")
plt.ylabel("Successful Login Attempts")
plt.title("Top 10 Most Successful Logins")
plt.xticks(rotation=45)
plt.savefig("successful_logins_plot.png")
plt.show()

