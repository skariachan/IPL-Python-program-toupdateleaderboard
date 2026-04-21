import pyautogui
import time
import pandas as pd
import pyperclip

# Load files
input_file = "IPL_input.xlsx"
main_file = "IPL.xlsx"

df_input = pd.read_excel(input_file)
df_main = pd.read_excel(main_file)

# Get match teams from T1 and T2
t1 = df_input["T1"].dropna().iloc[0]
t2 = df_input["T2"].dropna().iloc[0]

print(f"\nToday's match: {t1} vs {t2}")

# Ask winning team
while True:
    winner = input(f"Enter winning team ({t1} / {t2}): ").strip().upper()
    if winner in [t1.upper(), t2.upper()]:
        break
    print(f"Invalid! Please enter either '{t1}' or '{t2}'.")

# Calculate pool totals
df_input["Bet-Amount"] = pd.to_numeric(df_input["Bet-Amount"], errors="coerce").fillna(0)

total_pool = df_input["Bet-Amount"].sum()
winner_pool = df_input[df_input["Team"].str.upper() == winner]["Bet-Amount"].sum()

print(f"\nTotal Pool: {total_pool}")
print(f"Winning Pool: {winner_pool}")

# Update balances
for _, row in df_input.iterrows():
    name = row["Name"]
    team = str(row["Team"]).upper()
    bet = float(row["Bet-Amount"])

    idx = df_main[df_main["NAME"] == name].index
    if len(idx) == 0:
        print(f"Warning: {name} not found in IPL.xlsx, skipping.")
        continue

    i = idx[0]
    if team == winner:
        # Winner: proportional share of total pool
        df_main.loc[i, "Current"] += (bet / winner_pool) * total_pool - bet
    else:
        # Loser: deduct bet
        df_main.loc[i, "Current"] -= bet

# Save updated file
df_main.to_excel(main_file, index=False)
print("\nAll players updated successfully!")

# Sort leaderboard
sorted_df = df_main.sort_values(by="Current", ascending=False).reset_index(drop=True)

lines = ["Leaderboard 🏆", ""]

for i in range(len(sorted_df)):
    name = sorted_df.iloc[i]["NAME"]
    current = sorted_df.iloc[i]["Current"]

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
print("\n" + message)

print("\nSwitch to WhatsApp in 10 seconds...")
time.sleep(10)

pyperclip.copy(message)
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')

print("\nMessage sent successfully 🚀")