
import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk

#Creating a class of CarRentalApp.
class CarRentalApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Rental Application")
        self.master.geometry("800x600")  # Set the size of the application window.
        self.master.configure(bg='black')  # Set background color.
        self.master.attributes('-fullscreen', True)

        # Create labels and buttons for the main window.
        tk.Label(self.master, text="AJ's Cars.!!! 🏎️ 🚙", font=('Brush Script MT', 56), fg='yellow', bg='black').pack(pady=30)
        tk.Button(self.master, text="Car Info", command=self.open_car_info_window, font=('Courier', 25), fg='blue', bg='black').pack(pady=30)
        tk.Button(self.master, text="Customer Rental Info", command=self.open_customer_rental_info_window, font=('Courier', 25), fg='blue', bg='black').pack(pady=30)
        tk.Button(self.master, text="Exit", command=self.master.destroy, font=('Courier', 25), fg='red', bg='black').pack(pady=200)

    def open_car_info_window(self):
        car_info_window = tk.Toplevel(self.master)
        car_info_window.title("Car Information")
        car_info_window.geometry("800x600")  
        car_info_window.configure(bg='light blue')

        # Function to close car information window.
        def close_car_info_window():
            car_info_window.destroy()

        # Function to open customer details window.
        def open_customer_details_window():
            customer_details_window = tk.Toplevel(car_info_window)
            customer_details_window.title("Customer Details")
            customer_details_window.geometry("800x600")  
            customer_details_window.configure(bg='light blue')  

            # Function to close customer details window.
            def close_customer_details_window():
                customer_details_window.destroy()

            # Function to save customer details and show thank you message.
            def save_customer_details():
                # Retrieve input values
                customer_name = name_entry.get()
                customer_phone = phone_entry.get()
                customer_email = email_entry.get()
                address = address_entry.get()
                car_choosed = car_choosed_entry.get()


                # Validate if any field is empty
                if not (customer_name and customer_phone and customer_email and address and car_choosed):
                    messagebox.showerror("Empty Fields", "Please enter valid information.")
                    return

                # Validate customer name (check if it contains only alphabets).
                if not customer_name.isalpha():
                    messagebox.showerror("Invalid Input", "Please enter a valid name.")
                    return

                # Validate phone number (check if it contains only digits and has a length of 10).
                if not customer_phone.isdigit() or len(customer_phone) != 10:
                    messagebox.showerror("Invalid Input", "Please enter a valid 10-digit phone number.")
                    return

                # Validate address (check if it contains only alphabets and spaces).
                if not address.replace(' ', '').isalpha():
                    messagebox.showerror("Invalid Input", "Please enter a valid Address.")
                    return

                # Validate car choice (check if it exists in the cars table).
                conn = sqlite3.connect('car_rental.db')
                c = conn.cursor()
                c.execute("SELECT Car_name FROM Cars")
                available_cars = [car[0] for car in c.fetchall()]
                conn.close()

                if car_choosed not in available_cars:
                    messagebox.showerror("Invalid Car Choice", "This car is not available. Sorry for the inconvenience!")
                    return

                # Save customer details to customers_rental_info database.
                conn = sqlite3.connect('customers_rental_info.db')
                c = conn.cursor()
                c.execute(
                    "INSERT INTO Cars (Customer_name, Customer_phone, Customer_emailid, Customer_address, Car_choosed) VALUES (?, ?, ?, ?, ?)",
                    (customer_name, customer_phone, customer_email, address, car_choosed))
                conn.commit()
                conn.close()

                messagebox.showinfo("Thank You", "Thank you for choosing a car from us! Drive safely.")

                # Close the customer details window.
                close_customer_details_window()

                # Open Feedback Form.
                feedback_form = FeedbackForm(self.master)

            # Create labels and entry widgets for customer details.
            tk.Label(customer_details_window, text="Customer Name:", font=('Arial', 25), bg='light blue',fg='black').grid(row=1, column=21, padx=25, pady=10, sticky="e")
            tk.Label(customer_details_window, text="Phone No:", font=('Arial', 25), bg='light blue',fg='black').grid(row=3, column=21, padx=25, pady=10, sticky="e")
            tk.Label(customer_details_window, text="Email ID:", font=('Arial', 25), bg='light blue',fg='black').grid(row=5, column=21, padx=25, pady=10, sticky="e")
            tk.Label(customer_details_window, text="Address:", font=('Arial', 25), bg='light blue',fg='black').grid(row=7, column=21, padx=25, pady=10, sticky="e")
            tk.Label(customer_details_window, text="Car Choosed:", font=('Arial', 25), bg='light blue',fg='black').grid(row=9, column=21, padx=25, pady=10, sticky="e")

            name_entry = tk.Entry(customer_details_window)
            name_entry.grid(row=1, column=23, padx=15, pady=15, sticky="e")
            phone_entry = tk.Entry(customer_details_window)
            phone_entry.grid(row=3, column=23, padx=15, pady=15, sticky="e")
            email_entry = tk.Entry(customer_details_window)
            email_entry.grid(row=5, column=23, padx=15, pady=15, sticky="e")
            address_entry = tk.Entry(customer_details_window)
            address_entry.grid(row=7, column=23, padx=15, pady=15, sticky="e")
            car_choosed_entry = tk.Entry(customer_details_window)
            car_choosed_entry.grid(row=9, column=23, padx=15, pady=15, sticky="e")

            # Create buttons for customer details window.
            tk.Button(customer_details_window, text="Cancel", font=('Courier', 25), command=close_customer_details_window, fg='red',bg='black').grid(row=11, column=20, padx=50, pady=30, sticky="e")
            tk.Button(customer_details_window, text="Save", font=('Courier', 25), command=save_customer_details,fg='green', bg='black').grid(row=11, column=24, padx=50, pady=30, sticky="e")

        # Create buttons for car information window.
        tk.Button(car_info_window, text="Cancel", font=('Courier', 25), command=close_car_info_window, fg='red',bg='black').pack(side=tk.LEFT, padx=30)
        tk.Button(car_info_window, text="Next >", font=('Courier', 25), command=open_customer_details_window, fg='green', bg='black').pack(side=tk.RIGHT,padx=30)

        # Create a treeview to display car information.
        tree = ttk.Treeview(car_info_window)
        tree["columns"] = ("Sr.No", "Car_name", "Car_number", "Car_rent", "Fuel_type", "Car_seats", "Transmission", "Empty")
        tree.heading("#1", text="Sr.No")
        tree.heading("Car_name", text="Car Name")
        tree.heading("Car_number", text="Car Number")
        tree.heading("Car_rent", text="Car Rent")
        tree.heading("Fuel_type", text="Fuel Type")
        tree.heading("Car_seats", text="Car Seats")
        tree.heading("Transmission", text="Transmission")

        # Fetch data from the Cars table.
        conn = sqlite3.connect('car_rental.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Cars")
        cars_data = c.fetchall()

        # Insert data into the treeview.
        for car in cars_data:
            tree.insert("", tk.END, values=car)

        tree.pack(side='top',pady=50)

    def open_customer_rental_info_window(self):
        customer_rental_info_window = tk.Toplevel(self.master)
        customer_rental_info_window.title("Customer Rental Information")
        customer_rental_info_window.geometry("800x600")  
        customer_rental_info_window.configure(bg='light yellow')  

        # Function to close customer rental info window.
        def close_customer_rental_info_window():
            customer_rental_info_window.destroy()

        # Create a treeview to display customer rental information.
        tree = ttk.Treeview(customer_rental_info_window)
        tree["columns"] = ("Sr.No", "Customer_name", "Customer_phone", "Customer_emailid", "Customer_address", "Car_choosed", "Empty")
        tree.heading("#1", text="Sr.No")
        tree.heading("Customer_name", text="Customer Name")
        tree.heading("Customer_phone", text="Phone")
        tree.heading("Customer_emailid", text="Email ID")
        tree.heading("Customer_address", text="Address")
        tree.heading("Car_choosed", text="Car Choosed")

        # Fetch data from the Cars table in customers_rental_info database.
        conn = sqlite3.connect('customers_rental_info.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Cars")
        customers_data = c.fetchall()

        # Insert data into the treeview.
        for customer in customers_data:
            tree.insert("", tk.END, values=customer)

        tree.pack(side='top',pady=50)

        # Create button to close customer rental info window.
        tk.Button(customer_rental_info_window, text="Close", font=('Courier', 25),command=close_customer_rental_info_window, fg='red', bg='black').pack(side=tk.BOTTOM, anchor='s',pady=100)


class FeedbackForm:
    def __init__(self, master):
        self.master = master
        self.feedback_window = tk.Toplevel(self.master)
        self.feedback_window.title("Feedback Form")
        self.feedback_window.geometry("800x600")  
        self.feedback_window.configure(bg='light green') 

        # Feedback questions.
        questions = [
            "How satisfied are you with our car rental service? (1-5)",
            "Would you recommend our service to others? (Yes/No)",
            "Any suggestions or comments for improvement?"
        ]

        self.feedback_entries = []

        # Create labels and entry widgets for feedback.
        for i, question in enumerate(questions):
            tk.Label(self.feedback_window, text=question, font=('Arial', 20), bg='light green', fg='black').pack(
                pady=10)
            entry = tk.Entry(self.feedback_window, font=('Arial', 20))
            entry.pack(pady=10)
            self.feedback_entries.append(entry)

        # Create a button to submit feedback.
        tk.Button(self.feedback_window, text="Submit Feedback", font=('Courier', 25), command=self.submit_feedback, fg='blue', bg='black').pack(pady=20)

    def submit_feedback(self):
        # Retrieve feedback responses.
        feedback_responses = [entry.get() for entry in self.feedback_entries]

        # Save feedback to the database.
        conn = sqlite3.connect('feedbacks.db')
        c = conn.cursor()

        # Create a table if it doesn't exist.
        c.execute('''CREATE TABLE IF NOT EXISTS Feedbacks 
                     (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                      SatisfactionRating INTEGER,
                      RecommendService TEXT,
                      Suggestions TEXT)''')

        # Insert feedback into the table.
        c.execute("INSERT INTO Feedbacks (SatisfactionRating, RecommendService, Suggestions) VALUES (?, ?, ?)",
                  (feedback_responses[0], feedback_responses[1], feedback_responses[2]))

        conn.commit()
        conn.close()

        # Show thank you message.
        messagebox.showinfo("Thank You", "Thank you for your feedback!")

        # Close the feedback window.
        self.feedback_window.destroy()

# Create the main window.
root = tk.Tk()
app = CarRentalApp(root)

# Start the Tkinter loop.
root.mainloop()
