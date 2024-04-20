import csv
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Button, Frame, Label, Style

def scrape_amazon():
    # Open a file dialog to select the HTML file
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    if not file_path:
        messagebox.showerror("Error", "No file selected")
        return
    
    # Read the HTML file
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    
    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all divs with the specified class
    product_divs = soup.find_all("div", class_="puis-card-container s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-vbok7i09ua2q62ek5q2l21tt78 s-latency-cf-section puis-card-border")
    
    # Open an Excel file and write the data
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not save_path:
        messagebox.showerror("Error", "No file selected")
        return
    
    with open(save_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Product Name", "Product Price", "Product Ratings"])
        
        for div in product_divs:
            # Find the product name
            product_name_tag = div.find("span", class_="a-size-medium a-color-base a-text-normal")
            product_name = product_name_tag.text.strip() if product_name_tag else " "
            
            # Find the product price
            product_price_tag = div.find("span", class_="a-price-whole")
            product_price = product_price_tag.text.strip() if product_price_tag else " "
            
            # Find the product ratings
            product_ratings_tag = div.find("span", class_="a-size-base s-underline-text")
            product_ratings = product_ratings_tag.text.strip() if product_ratings_tag else " "
            
            # Write the data to the CSV file
            writer.writerow([product_name, product_price, product_ratings])
    
    messagebox.showinfo("Success", f"Data has been saved to {save_path}")

# Create the main window
root = tk.Tk()
root.title("Website Scraper")

# Set the style
style = Style()
style.configure('TButton', font=('Arial', 12), padding=10)

# Create a frame for the content
content_frame = Frame(root)
content_frame.pack(pady=20)

# Add a label
label = Label(content_frame, text="Click the button below to scrape Website", font=('Arial', 14))
label.pack(pady=10)

# Add a button to trigger the scraping process
scrape_button = Button(content_frame, text="Scrape Website", style='TButton', command=scrape_amazon)
scrape_button.pack()

# Run the Tkinter event loop
root.mainloop()
