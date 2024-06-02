import tkinter as tk
import json
from datetime import datetime

# Function to save the order
def save_order():
    order = {
        'order_id': datetime.now().strftime("%Y%m%d%H%M%S"),
        'items': current_order,
        'status': 'New'
    }
    
    with open('orders.json', 'a') as f:
        json.dump(order, f)
        f.write('\n')
    
    # Create a signal file to indicate that KDS should refresh
    with open('refresh_signal.txt', 'w') as f:
        f.write('refresh')

    # Clear the current order
    current_order.clear()
    update_order_display()

# Function to add item to the current order
def add_item(item):
    current_order.append(item)
    update_order_display()

# Function to update the order display
def update_order_display():
    order_display.config(text=f"Current Order: {', '.join(current_order)}")

# Create the POS GUI
pos = tk.Tk()
pos.title('POS System')

screen_width = pos.winfo_screenwidth()
screen_height = pos.winfo_screenheight()
pos.geometry(f'{screen_width//2}x{screen_height}')

menu_items = ['Pizza', 'Burger', 'Fries', 'Soda']
current_order = []

# Display buttons for each menu item
menu_frame = tk.Frame(pos)
menu_frame.pack(pady=10)

for item in menu_items:
    button = tk.Button(menu_frame, text=item, command=lambda i=item: add_item(i), width=15, height=2)
    button.pack(padx=5, pady=5)

# Display current order
order_display = tk.Label(pos, text="Current Order: ", font=('Arial', 14))
order_display.pack(pady=10)

# Submit order button
submit_button = tk.Button(pos, text='Submit Order', command=save_order, bg='green', fg='white', font=('Arial', 14), width=20, height=2)
submit_button.pack(pady=10)

pos.mainloop()
