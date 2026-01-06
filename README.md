# Ranchi University Result Scraper (Universal Edition) 🎓

**A cross-platform automation tool for aggregating public academic results.**

> **Note:** Developed by an NEP Student (2022-2026 Batch). Optimized for the post-COVID result format (2021+). It won't work for pre-COVID batches as the university used a different result system.

---

## ⚖️ Legal Disclaimer & Ethics Statement
**PLEASE READ BEFORE USING:**

1.  **Public Data Only:** This software is strictly an **automation tool**. It performs the same action as a human manually entering a roll number into the public university portal. It **does not** bypass authentication, exploit vulnerabilities, or access private/encrypted databases. All data retrieved is already publicly accessible on the internet.
2.  **Educational Purpose:** This repository is intended for educational purposes to demonstrate Python, Selenium, and data processing techniques.
3.  **No Liability:** The developer assumes **no liability** for any misuse of this software or any violations of the university's Terms of Service committed by end-users. You use this software at your own risk.
4.  **Responsible Use:**
    * **Do not** overwhelm the university servers with high-frequency requests.
    * **Do not** use this data for harassment, commercial data mining, or illegal activity.
    * **Respect Privacy:** Although the data is public, please treat the generated reports with respect for the privacy of your peers.

---

## 🚀 Key Features
* **Universal Compatibility:** Runs seamlessly on **Windows** and **Linux** (Ubuntu/Debian).
* **Multi-Browser Support:** Automatically configures drivers for **Chrome, Firefox, Brave, Opera,** and **Edge**.
* **Intelligent Parsing:** Extracts detailed metrics (SGPA, Grand Total) and hidden metadata (Name, Phone, DOB) from the page source.
* **Privacy Controls:** Interactive menu to toggle the extraction of sensitive fields like Phone Numbers.
* **Data Export:** Automatically compiles all results into a clean, structured `.xlsx` (Excel) database.

## 🛠️ Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/nemesislearns/ranchi-university-result-scraper.git](https://github.com/nemesislearns/ranchi-university-result-scraper.git)
    cd ranchi-university-result-scraper
    ```
    
3.  **Set up a Virtual Environment**

      **For Linux/Mac**
    ```bash
    python3 -m venv my_scraper_env
    source my_scraper_env/bin/activate
    ```
       **For Windows**
    ```bash
    python -m venv my_scraper_env
    my_scraper_env\Scripts\activate
    ```

3.  **Install Requirements**
    ```bash
    pip install -r requirements.txt
    ```

## 📋 Usage Guide
1.  Run the script:
    ```bash
    python ruresultscraper.py
    ```
2.  Follow the on-screen prompts to select your browser and operating system.
3.  Enter the **Course**, **Semester**, and **Stream** exactly as they appear on the official website (Case Sensitive).
4.  Input the Roll Number range (Start & End).

## 🐛 Feedback
If you encounter bugs specific to the new NEP format or Linux environments, please open an Issue in this repository.

---
