# Google Dorking Tool

A Python tool to automate Google Dorking, helping cybersecurity professionals uncover sensitive information through advanced search queries. The tool supports a wide range of Google dorks for targeting specific data types like login pages, configuration files, and more, including GitHub and SQL injection-specific dorks.

## Features
- Extensive Google dork list for various search targets (e.g., GitHub, SQL errors).
- Automatic result parsing using BeautifulSoup and Selenium.
- Option to save search results to a custom file.
- User-friendly with a colorful command-line interface.

## Requirements
- **Python 3.8+**.
- Install dependencies using:
  ```bash
  pip install -r requirements.txt

Usage
#Clone the repository:
- **git clone https://github.com/your-username/google-dorking-tool.git**
- **cd google-dorking-tool**

#Install dependencies:
- **pip install -r requirements.txt**

#Run the tool:
- **python googledork.py <site-url>**
