import time
import csv  # <--- This is the tool that talks to Excel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# --- 1. SETUP THE GHOST BROWSER ---
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

print("🕵️  Navigating to the target...")
driver.get("https://www.saucedemo.com/")
time.sleep(2)

# --- 2. LOGIN AUTOMATICALLY ---
print("🔐 Logging in...")
driver.find_element(By.ID, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()

print("✅ WE ARE IN! Access Granted.")
time.sleep(2) # Wait for products to load

# --- 3. STEAL DATA & SAVE TO EXCEL ---
print("📋 CREATING SPREADSHEET...")

# Create a file named 'sauce_data.csv'
file = open("sauce_data.csv", "w", newline="")
writer = csv.writer(file)

# Write the Top Header Row
writer.writerow(["PRODUCT NAME", "PRICE"]) 

# Find all the items on the page
names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")

# Loop through and write them to the file
for name, price in zip(names, prices):
    clean_name = name.text
    clean_price = price.text
    print(f"Saving: {clean_name}...")
    writer.writerow([clean_name, clean_price])

file.close()
print("-" * 40)
print("🎉 SUCCESS! Data saved to 'sauce_data.csv'")
print("-" * 40)