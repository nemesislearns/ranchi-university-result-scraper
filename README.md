# Ranchi University Result Scraper (Universal Edition) 🎓

**A cross-platform automation tool for aggregating public academic results.**

> **Note:** Developed by an NEP Student (2022-2026 Batch). Optimized for the post-COVID result format (2021+). It won't work for pre-COVID batches as Ranchi University used different method to show results.

---

## ⚖️ Legal Disclaimer & Ethics Statement

**Please Read This Before You Start Using**

1. **Public Data Only:** This software is really an **automation tool**. It does the thing that a person would do if they were to manually type a roll number into the public university portal. The **automation tool** does not get around security checks find weaknesses to exploit or look at secret databases. All the information the **automation tool** gets is already there, on the internet for anyone to see.
2.  **Educational Purpose:** This repository is meant to help people learn about Python and Selenium and how to work with data. It is, for purposes only to show people how to use Python, Selenium and data processing techniques.
3.  **No Liability:** The developer takes **no responsibility** for any things that happen when people use this software in the wrong way or break the universitys rules. You are using this software. It is all, on you. The developer has **no liability** if something goes wrong.
4.  **Responsible Use:** * **Do not** overwhelm the university servers with high-frequency requests.
   
* Please do not use this data for things, like harassing people collecting data for use or doing anything against the law.
* **Respect Privacy:** Even though the information is out in the open please be kind and think about the privacy of the people around you when you look at the reports that are made. Remember that the reports are about your peers so please treat the information with respect, for the privacy of your peers.

---

## 🚀 Key Features

* **Universal Compatibility:** Runs on **Windows** and **Linux** (Ubuntu/Debian).
* The system works with browsers. It sets up the drivers, for Chrome, Firefox, Brave, Opera and Edge automatically. This means you can use Chrome, Firefox, Brave, Opera and Edge without any problems.
* **Intelligent Parsing:** Extracts detailed metrics (SGPA, Grand Total) and hidden metadata (Name, Phone, DOB) from the public page source.
* **Privacy Controls:** Options to toggle the extraction of sensitive fields like Phone Numbers.
* **Data Export:** This is where the system puts all the results together in an Excel file that you can easily look at. It is saved as a.xlsx file. The **Data Export** makes it easy to get all the **Data Export** results, in one place.

## 🛠️ Installation

1.  **Clone the Repository**

\`\`\`bash
git clone https://github.com/nemesislearns/ranchi-university-result-scraper.git
cd ranchi-university-result-scraper
\`\`\`

2.  **Install Requirements**

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## 📋 Usage Guide

1.  Run the script:

\`\`\`bash
python ruresultscraper.py
\`\`\`

2.  Follow the on-screen prompts to select your browser and operating system.

3. When you are filling out the form you need to enter the **Course** the **Semester** and the **Stream** exactly as you see them on the website of the institution. You should enter the **Course** and the **Stream** and the **Semester** just like they are written on the website.

4.  Input the Roll Number range (Start & End).

## 🐛 Feedback

If you find bugs that're specific, to the new NEP format or that happen in Linux environments please open an Issue in this repository.
