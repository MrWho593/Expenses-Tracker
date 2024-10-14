import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from datetime import datetime
import json
import os

# Class to manage financial entries and calculations
class FinanceTracker:
    def __init__(self):
        self.entries = []

    def record_entry(self, entry_type, amount, category, date):
        # Record a new financial entry
        try:
            amount = float(amount)
        except ValueError:
            return "Invalid amount. Please enter a valid number."

        if entry_type not in ['income', 'expense']:
            return "Invalid entry type. Please enter 'income' or 'expense.'"

        entry = {
            'type': entry_type,
            'amount': amount,
            'category': category,
            'date': date
        }
        self.entries.append(entry)
        return "Entry recorded successfully."

    def view_all_entries(self):
        # Retrieve all recorded entries
        return self.entries

    def calculate_totals(self):
        # Calculate total income, total expenses, and net income
        total_income = sum(entry['amount'] for entry in self.entries if entry['type'] == 'income')
        total_expenses = sum(entry['amount'] for entry in self.entries if entry['type'] == 'expense')
        net_income = total_income - total_expenses
        return total_income, total_expenses, net_income

    def view_summary_by_month(self, month):
        # Retrieve entries for a specific month
        month_entries = [entry for entry in self.entries if datetime.strptime(entry['date'], '%Y-%m-%d').month == month]
        return month_entries

    def save_to_file(self):
        # Save financial data to a JSON file with a timestamped filename
        current_directory = os.getcwd()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"finance_data_{timestamp}.json"
        full_path = os.path.join(current_directory, filename)

        with open(full_path, 'w') as file:
            json.dump(self.entries, file)

        return f"Data saved successfully to {full_path}."

    def load_from_file(self, filename):
        # Load financial data from a JSON file
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                self.entries = json.load(file)
            return "Data loaded successfully."
        else:
            return "File not found."

# Class for the GUI of the finance tracker
class FinanceTrackerGUI:
    def __init__(self, master):
        self.type_combobox = None
        self.date_entry = None
        self.master = master
        self.tracker = FinanceTracker()

        self.master.title('Finance Tracker')

        self.style = ThemedStyle(self.master)
        self.style.set_theme("plastik")

        self.create_widgets()

    def create_widgets(self):
        # Create various GUI elements
        frame = ttk.Frame(self.master, padding=10, style="TFrame")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Finance Tracker", font="Arial 16 bold", style="TLabel").grid(row=0, column=0, columnspan=3, pady=10, padx=10)

        ttk.Label(frame, text="Finance Tracker Menu", font="Arial 12 bold", style="TLabel").grid(row=1, column=0, columnspan=3)

        self.create_entry_widgets(frame)
        self.create_action_buttons(frame)
        self.create_feedback_label(frame)
        self.create_entries_treeview(frame)  # Modified to use Treeview instead of Listbox

    def create_entry_widgets(self, frame):
        # Create entry-related GUI elements
        ttk.Label(frame, text="Type (income/expense):", style="TLabel").grid(row=2, column=0, sticky=tk.E)
        self.type_combobox = ttk.Combobox(frame, values=['income', 'expense'], style="TCombobox")
        self.type_combobox.grid(row=2, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Amount:", style="TLabel").grid(row=3, column=0, sticky=tk.E)
        self.amount_entry = ttk.Entry(frame, style="TEntry")
        self.amount_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Category:", style="TLabel").grid(row=4, column=0, sticky=tk.E)
        self.category_entry = ttk.Entry(frame, style="TEntry")
        self.category_entry.grid(row=4, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame, text="Date (YYYY-MM-DD):", style="TLabel").grid(row=5, column=0, sticky=tk.E)
        self.date_entry = ttk.Entry(frame, style="TEntry")
        self.date_entry.grid(row=5, column=1, sticky=(tk.W, tk.E))

    def create_action_buttons(self, frame):
        # Create buttons for various actions
        ttk.Button(frame, text="Record a new entry", command=self.record_entry, style="TButton").grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="View all entries", command=self.view_all_entries, style="TButton").grid(row=7, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Calculate totals", command=self.calculate_totals, style="TButton").grid(row=8, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="View summary for a specific month", command=self.view_summary, style="TButton").grid(row=9, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Save data to file", command=self.save_to_file, style="TButton").grid(row=10, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Load data from file", command=self.load_from_file, style="TButton").grid(row=11, column=0, columnspan=2, pady=5)
        ttk.Button(frame, text="Exit", command=self.master.destroy, style="TButton").grid(row=12, column=0, columnspan=2, pady=10)

    def create_feedback_label(self, frame):
        # Create a label for providing feedback
        self.feedback_label = ttk.Label(frame, text="", foreground="red", style="TLabel")
        self.feedback_label.grid(row=13, column=0, columnspan=2, pady=10)

    def create_entries_treeview(self, frame):  # Modified to use Treeview
        # Create a Treeview widget for displaying entries
        columns = ('Type', 'Amount', 'Category', 'Date')
        self.entries_treeview = ttk.Treeview(frame, columns=columns, show='headings', height=10, style="Treeview")
        for col in columns:
            self.entries_treeview.heading(col, text=col)
            self.entries_treeview.column(col, width=100, anchor=tk.CENTER)
        self.entries_treeview.grid(row=3, column=3, rowspan=30, sticky=(tk.W, tk.E))
    def record_entry(self):
        # Record a new financial entry based on user input
        entry_type = self.type_combobox.get().lower()
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()

        feedback = self.tracker.record_entry(entry_type, amount, category, date)
        self.set_feedback(feedback)
        self.refresh_entries_treeview()

    def view_all_entries(self):
        # Display all recorded entries
        entries = self.tracker.view_all_entries()
        self.display_records(entries)

    def calculate_totals(self):
        # Calculate and display total income, total expenses, and net income
        total_income, total_expenses, net_income = self.tracker.calculate_totals()
        feedback = f'Total Income: {total_income}\nTotal Expenses: {total_expenses}\nNet Income: {net_income}'
        self.set_feedback(feedback)

    def view_summary(self):
        # Display entries for a specific month
        try:
            month = int(self.type_combobox.get())
        except ValueError:
            self.set_feedback("Invalid month. Please enter a number between 1 and 12.")
            return

        month_entries = self.tracker.view_summary_by_month(month)
        self.display_records(month_entries)

    def save_to_file(self):
        # Save financial data to a file
        feedback = self.tracker.save_to_file()
        self.set_feedback(feedback)

    def load_from_file(self):
        # Load financial data from a file
        feedback = self.tracker.load_from_file("finance_data_20240117192443.json")

        self.set_feedback(feedback)
        self.refresh_entries_treeview()

    def display_records(self, records):
        # Display financial records in the Treeview widget
        self.entries_treeview.delete(*self.entries_treeview.get_children())
        if not records:
            self.set_feedback("No records found.")
        else:
            for entry in records:
                self.entries_treeview.insert('', tk.END, values=(entry['type'], entry['amount'], entry['category'], entry['date']))

    def set_feedback(self, message):
        # Set the feedback label with a given message
        self.feedback_label.config(text=message, foreground="red")

    def refresh_entries_treeview(self):
        # Refresh the Treeview widget with the latest financial entries
        entries = self.tracker.view_all_entries()
        self.display_records(entries)

if __name__ == "__main__":
    # Create the main Tkinter window and the FinanceTrackerGUI instance
    root = tk.Tk()
    style = ThemedStyle(root)
    style.set_theme("plastik")

    # Add custom styles
    style.configure("TFrame", background="#ADD8E6")  # Light Blue
    style.configure("TLabel", background="#ADD8E6", foreground="#000080")  # Light Blue background, Dark Blue text
    style.configure("TEntry", fieldbackground="#FFFFFF")  # White background for Entry
    style.configure("TButton", background="#4682B4", foreground="#000000")  # Steel Blue background, White text
    style.map("TButton", background=[("active", "#35586C")])  # Darker Steel Blue when pressed
    style.configure("TCombobox", fieldbackground="#FFFFFF")  # White background for Combobox
    style.map("TCombobox", background=[("active", "#FFFFFF")])  # White background when active
    style.configure("Treeview", background="#ADD8E6", fieldbackground="#ADD8E6", foreground="#000080")  # Light Blue background, Dark Blue text

    app = FinanceTrackerGUI(root)
    root.mainloop()