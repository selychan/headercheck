# Header Checker Tool

## Description

This project allows us to contain many domains of scope. It checks the security headers of websites, identifies missing headers, and generates detailed reports.

## Features
- **Parallel Scanning:** Scans multiple domains simultaneously using threads.
- **Security Header Detection:** Identifies essential security headers such as HSTS, CSP, X-Frame-Options, and more.
- **Report Generation:** Outputs scan results into a text file for easy reference.
- **Colored Terminal Output:** Provides clear and colored feedback in the terminal.

## How to Use

### Prerequisites
- Python 3.x installed on your system.
- Required Python libraries installed. You can install them using:
  ```bash
  pip install -r requirements.txt
  ```

### Running the Tool
1. Create a text file (e.g., `domains.txt`) containing the list of domains you want to scan, with one domain per line.
2. Run the script using the following command:
   ```bash
   python headercheck.py -l domains.txt
   ```
3. The results will be displayed in the terminal and saved to a `security_report.txt` file.

## Example Output
![image-Photoroom (1)](https://github.com/user-attachments/assets/38f2f37f-4144-496c-b342-55e4109435e0)



