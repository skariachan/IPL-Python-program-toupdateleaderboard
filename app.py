from flask import Flask, request, render_template
import pandas as pd
import os

app = Flask(__name__)

FILE = "IPL_input.xlsx"

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name'].strip()
        team = request.form['team'].strip()

        # Convert amount safely
        try:
            amount = int(request.form['amount'])
        except:
            return "Invalid amount! Please enter a number."

        # New row
        new_data = pd.DataFrame([[name, team, amount]],
                                columns=["Name", "Team", "Bet-Amount"])

        if os.path.exists(FILE):
            df = pd.read_excel(FILE)

            # Ensure correct datatype
            if "Bet-Amount" in df.columns:
                df["Bet-Amount"] = pd.to_numeric(df["Bet-Amount"], errors='coerce')

            # Check if name exists
            if name in df["Name"].values:
                df.loc[df["Name"] == name, "Team"] = team
                df.loc[df["Name"] == name, "Bet-Amount"] = amount
            else:
                df = pd.concat([df, new_data], ignore_index=True)
        else:
            df = new_data

        # Save to Excel
        df.to_excel(FILE, index=False)

        return "Data updated successfully!"

    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)