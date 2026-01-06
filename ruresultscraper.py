import os
import sys
import time
import re
import shutil
import platform
import pandas as pd
from bs4 import BeautifulSoup

# --- SELENIUM IMPORTS ---
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- DRIVER MANAGERS ---
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# ==========================================
# CONSTANTS
# ==========================================
URL = "https://www.exam.ranchiuniversity.co.in/result"

# ==========================================
# BROWSER SETUP LOGIC
# ==========================================

def get_system_browser():
    """Interactive menu to select OS and Browser."""
    print("\n==========================================")
    print("   RANCHI UNIVERSITY RESULT SCRAPER")
    print("==========================================")
    
    # 1. Detect OS (Auto-detect usually works best)
    current_os = platform.system()
    print(f"Detected System: {current_os}")
    
    # 2. Select Browser
    print("\nSelect your Browser:")
    print("1. Firefox (Recommended for stability)")
    print("2. Google Chrome")
    print("3. Brave Browser")
    print("4. Opera")
    print("5. Opera GX")
    print("6. Microsoft Edge (Windows only)")
    
    choice = input("Enter number (1-6): ").strip()
    
    return current_os, choice

def setup_driver(os_type, browser_choice):
    """Configures the WebDriver based on user selection."""
    print("\nConfiguring Driver...")
    driver = None
    
    try:
        # --- FIREFOX ---
        if browser_choice == '1':
            options = webdriver.FirefoxOptions()
            # Snap Fix for Linux
            if os_type == "Linux":
                local_profile = os.path.join(os.getcwd(), "firefox_temp_profile")
                if not os.path.exists(local_profile): os.makedirs(local_profile)
                options.add_argument("-profile")
                options.add_argument(local_profile)
            
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)

        # --- CHROME ---
        elif browser_choice == '2':
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

        # --- BRAVE (Chromium based) ---
        elif browser_choice == '3':
            options = webdriver.ChromeOptions()
            # Auto-detect Brave path
            if os_type == "Windows":
                binary_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
            else: # Linux
                binary_path = "/usr/bin/brave-browser"
            
            if not os.path.exists(binary_path):
                print(f"\nError: Brave binary not found at default location: {binary_path}")
                binary_path = input("Please paste the full path to brave.exe: ").strip('"')
            
            options.binary_location = binary_path
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

        # --- OPERA (Chromium based) ---
        elif browser_choice == '4':
            options = webdriver.ChromeOptions()
            if os_type == "Windows":
                binary_path = os.path.expanduser("~\\AppData\\Local\\Programs\\Opera\\launcher.exe")
            else:
                binary_path = "/usr/bin/opera"
            
            if not os.path.exists(binary_path):
                print(f"\nError: Opera not found at: {binary_path}")
                binary_path = input("Please paste path to Opera executable: ").strip('"')

            options.binary_location = binary_path
            # Opera needs specific experimental option to work with ChromeDriver
            options.add_experimental_option('w3c', True)
            
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

        # --- OPERA GX (Chromium based) ---
        elif browser_choice == '5':
            options = webdriver.ChromeOptions()
            if os_type == "Windows":
                binary_path = os.path.expanduser("~\\AppData\\Local\\Programs\\Opera GX\\launcher.exe")
            else:
                print("Opera GX is not standard on Linux. Using manual path.")
                binary_path = input("Enter path to Opera GX executable: ").strip('"')

            options.binary_location = binary_path
            options.add_experimental_option('w3c', True)
            
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

        else:
            print("Invalid browser selection.")
            sys.exit()

        return driver

    except Exception as e:
        print(f"\nCRITICAL DRIVER ERROR: {e}")
        print("Tip: Ensure you have the browser installed.")
        sys.exit()

# ==========================================
# USER INPUTS
# ==========================================

def get_scraping_config():
    """Get search parameters from user."""
    print("\n--- CONFIGURATION ---")
    target_course = input("Enter Course (e.g. NEP, UG, PG): ").strip()
    target_semester = input("Enter Semester (e.g. 1, 2, 3, 4, 5, 6): ").strip()
    target_stream = input("Enter Stream (Arts, Science, Commerce): ").strip()
    if not target_stream: target_stream = None

    print("\n--- ROLL NUMBERS ---")
    start_roll = input("Enter START Roll Number: ").strip()
    end_roll = input("Enter END Roll Number:   ").strip()
    
    print("\n--- DATA TO EXTRACT (y/n) ---")
    options = {
        "phone": input("Phone Number? : ").lower() == 'y',
        "dob": input("Date of Birth?: ").lower() == 'y',
        "blood": input("Blood Group?  : ").lower() == 'y'
    }
    
    roll_list = generate_roll_range(start_roll, end_roll)
    if not roll_list:
        print("Error generating roll numbers. Exiting.")
        sys.exit()
        
    return target_course, target_semester, target_stream, roll_list, options

def generate_roll_range(start, end):
    if len(start) != len(end): return []
    common_prefix = os.path.commonprefix([start, end])
    start_suffix = start[len(common_prefix):]
    end_suffix = end[len(common_prefix):]
    
    if not (start_suffix.isdigit() and end_suffix.isdigit()): return []
    
    roll_list = []
    for i in range(int(start_suffix), int(end_suffix) + 1):
        roll_list.append(common_prefix + str(i).zfill(len(start_suffix)))
    return roll_list

# ==========================================
# MAIN SCRAPER LOGIC
# ==========================================

def main():
    # 1. Setup Environment
    os_type, browser_choice = get_system_browser()
    driver = setup_driver(os_type, browser_choice)
    
    # 2. Get Search Config
    TARGET_COURSE, TARGET_SEMESTER, TARGET_STREAM, ROLL_NUMBERS, OPTIONS = get_scraping_config()
    
    final_database = []
    print(f"\nStarting Scraper for {len(ROLL_NUMBERS)} students...")

    try:
        driver.get(URL)
        time.sleep(3) 

        for index, roll in enumerate(ROLL_NUMBERS):
            try:
                print(f"[{index+1}/{len(ROLL_NUMBERS)}] {roll}...", end="")

                # --- STEP 1: RE-SELECT DROPDOWNS ---
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//select[contains(@ng-model, 'search.course')]")))
                    Select(driver.find_element(By.XPATH, "//select[contains(@ng-model, 'search.course')]")).select_by_visible_text(TARGET_COURSE)
                    time.sleep(0.2)
                    Select(driver.find_element(By.XPATH, "//select[contains(@ng-model, 'search.semester')]")).select_by_visible_text(TARGET_SEMESTER)
                    time.sleep(0.2)
                    if TARGET_STREAM:
                        try: Select(driver.find_element(By.XPATH, "//select[contains(@ng-model, 'search.stream')]")).select_by_visible_text(TARGET_STREAM)
                        except: pass 
                except:
                    print(" -> Resetting...")
                    driver.get(URL)
                    continue

                # --- STEP 2: SEARCH ---
                driver.find_element(By.ID, "rollno").clear()
                driver.find_element(By.ID, "rollno").send_keys(roll)
                driver.find_element(By.ID, "btn_result").click()

                # --- STEP 3: WAIT ---
                try:
                    WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CLASS_NAME, "neptable")))
                except:
                    print(" -> No Result")
                    driver.get(URL) 
                    continue

                # --- STEP 4: EXTRACT ---
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                student_record = {"Roll Number": roll}

                # JS EXTRACTION
                try:
                    name_match = re.search(r'"name"\s*:\s*"([^"]+)"', page_source)
                    student_record["Name"] = name_match.group(1) if name_match else "N/A"

                    if OPTIONS["phone"]:
                        ph = re.search(r'"mobileno"\s*:\s*"([^"]+)"', page_source)
                        student_record["Mobile"] = ph.group(1) if ph else "N/A"
                    if OPTIONS["dob"]:
                        db = re.search(r'"dob"\s*:\s*"([^"]+)"', page_source)
                        student_record["DOB"] = db.group(1) if db else "N/A"
                    if OPTIONS["blood"]:
                        bg = re.search(r'"blood_group"\s*:\s*"([^"]+)"', page_source)
                        student_record["Blood Group"] = bg.group(1) if bg else "N/A"
                except: pass

                # TABLE EXTRACTION
                table = soup.find("table", class_="neptable")
                if table:
                    rows = table.find_all("tr")
                    for row in rows[2:]: 
                        cols = row.find_all("td")
                        if len(cols) > 10:
                            student_record[cols[1].get_text(strip=True)] = cols[10].get_text(strip=True)
                        elif row.find("b") and "Grand Total" in row.find("b").get_text():
                            text = row.find("b").get_text()
                            gt = re.search(r"Grand Total:\s*(\d+)", text)
                            pc = re.search(r"Percentage:\s*([\d\.]+)", text)
                            sg = re.search(r"SGPA\s*:\s*([\d\.]+)", text)
                            res = re.search(r"RESULT\s*:\s*(\w+)", text)
                            
                            if gt: student_record["Grand Total"] = gt.group(1)
                            if pc: student_record["Percentage"] = pc.group(1)
                            if sg: student_record["SGPA"] = sg.group(1)
                            if res: student_record["Result Status"] = res.group(1)
                
                final_database.append(student_record)
                print(f" -> Found: {student_record.get('Name')}")

                # --- STEP 5: RESET ---
                try:
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-warning"))).click()
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "rollno")))
                except:
                    driver.get(URL)

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Loop Error: {e}")
                driver.get(URL)

    finally:
        driver.quit()
        # Cleanup Firefox temp folder if it exists
        local_profile = os.path.join(os.getcwd(), "firefox_temp_profile")
        if os.path.exists(local_profile):
            try: shutil.rmtree(local_profile)
            except: pass

    # SAVE
    if final_database:
        df = pd.DataFrame(final_database)
        cols = ['Roll Number', 'Name', 'SGPA', 'Result Status', 'Grand Total', 'Percentage', 'Mobile', 'DOB', 'Blood Group']
        final_cols = [c for c in cols if c in df.columns]
        for c in df.columns:
            if c not in final_cols: final_cols.append(c)
        
        df = df.reindex(columns=final_cols)
        df.to_excel("Results.xlsx", index=False)
        print("\nDONE! Saved to 'Results.xlsx'")
    else:
        print("No data.")

if __name__ == "__main__":
    main()