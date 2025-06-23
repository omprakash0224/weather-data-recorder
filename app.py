import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pandas as pd
from datetime import datetime
import os
import platform
import subprocess
from tkinter import messagebox

weather_data = []
recorded_dates = set()

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def add_entry():
    date = date_var.get()
    temp = temp_var.get()
    condition = condition_var.get()

    if not is_valid_date(date):
        messagebox.showerror("Invalid Date", "Please use YYYY-MM-DD format.")
        return

    if date in recorded_dates:
        messagebox.showwarning("Duplicate", "This date already has data.")
        return

    try:
        temperature = float(temp)
    except ValueError:
        messagebox.showerror("Invalid Input", "Temperature must be a number.")
        return

    weather_data.append({"Date": date, "Temperature": temperature, "Condition": condition})
    recorded_dates.add(date)
    messagebox.showinfo("Success", "Weather data added successfully.")
    date_var.set("")
    temp_var.set("")
    condition_var.set("")

def view_data():
    if not weather_data:
        messagebox.showinfo("No Data", "No entries yet.")
        return

    view_window = ttk.Toplevel(root)
    view_window.title("All Weather Entries")

    text = ttk.ScrolledText(view_window, width=60, height=15)
    text.pack(padx=10, pady=10)

    for entry in weather_data:
        text.insert(END, f"{entry['Date']} | {entry['Temperature']}°C | {entry['Condition']}\n")

def summarize_and_export():
    if not weather_data:
        messagebox.showinfo("No Data", "Nothing to summarize.")
        return

    df = pd.DataFrame(weather_data)

    summary = {
        "Average Temperature": df['Temperature'].mean(),
        "Max Temperature": df['Temperature'].max(),
        "Min Temperature": df['Temperature'].min(),
        "Std Dev": df['Temperature'].std(),
        "Most Common Condition": df['Condition'].mode()[0],
        "Trend": "Increasing" if df.sort_values(by="Date")["Temperature"].diff().mean() > 0 else "Decreasing"
    }

    summary_msg = "\n".join([f"{k}: {round(v, 2) if isinstance(v, float) else v}" for k, v in summary.items()])
    messagebox.showinfo("Summary", summary_msg)

    df.to_csv("weather_data.csv", index=False)
    with open("weather_summary.txt", "w", encoding="utf-8") as f:
        f.write("Weather Data Summary\n")
        f.write("====================\n")
        f.write(summary_msg)
    open_file("weather_data.csv")
    open_file("weather_summary.txt")

def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.run(["open", path])
    else:
        subprocess.run(["xdg-open", path])

# --- Modern GUI Setup ---
# Initialize the main window
root = ttk.Window(title="🌤️ Weather Data Recorder", themename="solar")
root.state('zoomed')  # Fullscreen on Windows

# Main Frame
main_frame = ttk.Frame(root, padding=40)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Define variables
date_var = ttk.StringVar()
temp_var = ttk.StringVar()
condition_var = ttk.StringVar()

# Date input
ttk.Label(main_frame, text="📅 Date (YYYY-MM-DD):", font=("Segoe UI", 10)).pack(pady=5)
ttk.Entry(main_frame, textvariable=date_var, width=30).pack()

# Temperature input
ttk.Label(main_frame, text="🌡 Temperature (°C):", font=("Segoe UI", 10)).pack(pady=5)
ttk.Entry(main_frame, textvariable=temp_var, width=30).pack()

# Condition input
ttk.Label(main_frame, text="☁️ Condition (e.g., Sunny,Rainy etc):", font=("Segoe UI", 10)).pack(pady=5)
ttk.Entry(main_frame, textvariable=condition_var, width=30).pack(pady=(0, 20))

# Buttons with modern rounded styles
ttk.Button(main_frame, text="➕ Add Entry", command=lambda: add_entry(), bootstyle="success-outline").pack(pady=10, fill='x')
ttk.Button(main_frame, text="📄 View Entries", command=lambda: view_data(), bootstyle="info-outline").pack(pady=5, fill='x')
ttk.Button(main_frame, text="📊 Summarize & Export", command=lambda: summarize_and_export(), bootstyle="warning-outline").pack(pady=5, fill='x')
ttk.Button(main_frame, text="❌ Exit", command=root.quit, bootstyle="danger-outline").pack(pady=10, fill='x')

root.mainloop()

