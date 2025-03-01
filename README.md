# Google Dorking Tool

<p align="center">
  <img src="https://github.com/thexM0G/thexM0G/blob/main/googledork.png" alt="H4CK_N4S4 " />
</p>


A Python tool to automate Google Dorking, helping cybersecurity professionals uncover sensitive information through advanced search queries. The tool supports a wide range of Google dorks for targeting specific data types like login pages, configuration files, and more, including GitHub and SQL injection-specific dorks.

## Features
- Extensive Google dork list for various search targets (e.g., GitHub, SQL errors).
- Automatic result parsing using BeautifulSoup and Selenium.
- Option to save search results to a custom file.
- User-friendly with a colorful command-line interface.
- you can add your own dork in to the tool fully customizable 

## Requirements
- **Python 3.8+**.
- Install dependencies using:
  ```bash
  pip install -r requirements.txt

## Usage
- **Clone the repository:**
```bash
git clone https://github.com/thexM0G/Google-Dorking
cd google-dorking-tool
```

- **Install dependencies:**
  ```bash
  pip install -r requirements.txt
  ```

  - **Run The Tool**
    ```bash
    python googledork.py <site-url>
    
