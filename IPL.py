import pyautogui
import time
import pandas as pd
import pyperclip
# Load file
file = "IPL.xlsx"
df = pd.read_excel(file)

Total_pool = float(input("Enter total pool amount: "))
Winner_pool = float(input("Enter Winning pool amount: "))

# Update balances
for i in range(len(df)):
    name = df.loc[i, "NAME"]
    
    print(f"\n{name}'s current balance: {df.loc[i, 'Current']}")
    bet = float(input(f"Enter betting amount for {name}: "))
    c = input("Did he win? (y/n): ").lower()

    if c == "n":
        df.loc[i, "Current"] -= bet
    else:
        df.loc[i, "Current"] += (bet / Winner_pool) * Total_pool - bet

# Save updated file
df.to_excel(file, index=False)
print("\nAll players updated successfully!")

# Sort leaderboard
sorted_df = df.sort_values(by="Current", ascending=False).reset_index(drop=True)



lines = ["Leaderboard 🏆", ""]

for i in range(len(sorted_df)):
    name = sorted_df.iloc[i]["NAME"]
    current = sorted_df.iloc[i]["Current"]
    
    # medals
    if i == 0:
        medal = "🥇"
    elif i == 1:
        medal = "🥈"
    elif i == 2:
        medal = "🥉"
    else:
        medal = ""
    
    lines.append(f"{i+1}) {name} : {current:.2f}/- {medal}")
message = "\n".join(lines)
print("\nSwitch to WhatsApp in 10 seconds...")
time.sleep(10)

pyperclip.copy(message)

# Paste (CTRL + V)
pyautogui.hotkey('ctrl', 'v')
# Final send
pyautogui.press('enter')

print("\nMessage sent successfully 🚀")