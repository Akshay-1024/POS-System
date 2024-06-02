import tkinter as tk
import json
import os

# Function to load orders
def load_orders():
    if not os.path.exists('orders.json'):
        with open('orders.json', 'w') as f:
            pass  # Create an empty file if it doesn't exist

    with open('orders.json', 'r') as f:
        orders = [json.loads(line) for line in f if line.strip()]
    return orders

# Function to update the order status
def update_status(order_id, new_status):
    orders = load_orders()
    updated_orders = []
    for order in orders:
        if order['order_id'] == order_id:
            if new_status != 'Delivered':
                order['status'] = new_status
                updated_orders.append(order)
        else:
            updated_orders.append(order)

    with open('orders.json', 'w') as f:
        for order in updated_orders:
            json.dump(order, f)
            f.write('\n')
    display_orders()

# Function to display orders
def display_orders():
    for widget in frame.winfo_children():
        widget.destroy()

    orders = load_orders()
    for order in orders:
        order_frame = tk.Frame(frame, bd=2, relief='sunken', padx=10, pady=5)
        order_frame.pack(fill='x', padx=5, pady=5)

        tk.Label(order_frame, text=f"Order ID: {order['order_id']}", font=('Arial', 12, 'bold')).pack(anchor='w')
        tk.Label(order_frame, text=f"Items: {', '.join(order['items'])}", font=('Arial', 12)).pack(anchor='w')
        tk.Label(order_frame, text=f"Status: {order['status']}", font=('Arial', 12)).pack(anchor='w')

        btn_frame = tk.Frame(order_frame)
        btn_frame.pack(anchor='w', pady=5)

        tk.Button(btn_frame, text='Preparing', command=lambda oid=order['order_id']: update_status(oid, 'Preparing'), bg='yellow', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(btn_frame, text='Ready', command=lambda oid=order['order_id']: update_status(oid, 'Ready'), bg='orange', font=('Arial', 10)).pack(side='left', padx=5)
        tk.Button(btn_frame, text='Delivered', command=lambda oid=order['order_id']: update_status(oid, 'Delivered'), bg='green', font=('Arial', 10)).pack(side='left', padx=5)

def check_for_update():
    if os.path.exists('refresh_signal.txt'):
        os.remove('refresh_signal.txt')
        display_orders()
    kds.after(500, check_for_update)  # Check every second

# Create the KDS GUI
kds = tk.Tk()
kds.title('KDS System')

screen_width = kds.winfo_screenwidth()
screen_height = kds.winfo_screenheight()
kds.geometry(f'{screen_width//2}x{screen_height}+{screen_width//2}+0')

# Create a canvas and a scrollbar for the orders
canvas = tk.Canvas(kds)
scrollbar = tk.Scrollbar(kds, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

frame = scrollable_frame

check_for_update()  # Start checking for updates

kds.mainloop()
