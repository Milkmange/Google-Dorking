from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time
import random
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from urllib.parse import urlparse

# Initialize colorama
init(autoreset=True)

# ASCII Art and Branding
def print_banner():
    print(f"{Fore.LIGHTRED_EX}"
          "  ____  ___   ___   ____ _     _____   ____   ___  ____  _  __\n"
          " / ___|/ _ \\ / _ \\ / ___| |   | ____| |  _ \\ / _ \\|  _ \\| |/ /\n"
          "| |  _| | | | | | | |  _| |   |  _|   | | | | | | | |_) | ' / \n"
          "| |_| | |_| | |_| | |_| | |___| |___  | |_| | |_| |  _ <| . \\ \n"
          " \\____|\\___/ \\___/ \\____|_____|_____| |____/ \\___/|_| \\_\\_|\\_\\\n"
          f"{Style.RESET_ALL}=======================================\n"
          f"{Fore.WHITE}TOOL BY - thexm0g{Style.RESET_ALL}")

# Import the DORKS list from the original file
DORKS = [
    # Google dorks
    'site:{site} inurl:admin',
    'site:{site} inurl:login',
    'site:{site} inurl:wp-admin',
    'site:{site} intitle:index.of',
    'site:{site} "confidential"',
    'site:{site} "password" filetype:log',
    'site:{site} filetype:sql "dump"',
    'site:{site} filetype:xml "password"',
    'site:{site} filetype:env',
    'site:{site} "phpinfo.php"',
    'site:{site} filetype:bak',
    'site:{site} filetype:config',
    'site:{site} filetype:json',
    'site:{site} filetype:ini',
    # ... (keeping all the original dorks)
]

def validate_url(url):
    """Validate the provided URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def init_browser():
    """Initialize Firefox browser with improved options"""
    try:
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        # Set page load timeout
        driver.set_page_load_timeout(30)
        
        return driver
    except Exception as e:
        print(f"{Fore.RED}Error initializing browser: {str(e)}{Style.RESET_ALL}")
        return None

def google_search(driver, query):
    """Perform Google search with improved error handling and delays"""
    try:
        search_url = f"https://www.google.com/search?q={query}"
        driver.get(search_url)
        
        # Random delay between requests to avoid detection
        time.sleep(random.uniform(2, 4))
        
        # Wait for results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(("class name", "g"))
        )
        
        # Parse results
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = []
        
        for g in soup.find_all('div', class_='g'):
            link = g.find('a')
            if link and link.get('href'):
                url = link.get('href')
                if url.startswith('http'):
                    results.append(url)
        
        return results
    except Exception as e:
        print(f"{Fore.RED}Error during search: {str(e)}{Style.RESET_ALL}")
        return []

def save_results(results, filename):
    """Save results to file with error handling"""
    try:
        with open(filename, 'w') as file:
            for result in results:
                file.write(result + '\n')
        return True
    except Exception as e:
        print(f"{Fore.RED}Error saving results: {str(e)}{Style.RESET_ALL}")
        return False

def perform_dorking(site):
    """Main dorking function with improved error handling"""
    print_banner()
    
    # Validate URL
    if not validate_url(f"http://{site}"):
        print(f"{Fore.RED}Invalid URL format. Please provide a valid domain.{Style.RESET_ALL}")
        return
    
    # Initialize browser
    driver = init_browser()
    if not driver:
        return
    
    try:
        all_results = []
        
        for dork in DORKS:
            query = dork.format(site=site)
            print(f"{Fore.CYAN}Performing Google Dork: {Fore.YELLOW}{query}{Style.RESET_ALL}")
            
            results = google_search(driver, query)
            all_results.extend(results)
            
            print(f"{Fore.GREEN}Results for {Fore.YELLOW}{query}{Style.RESET_ALL}:")
            for result in results:
                print(f"{Fore.LIGHTBLUE_EX}{result}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}{'-' * 80}{Style.RESET_ALL}")
            
            # Random delay between dorks
            time.sleep(random.uniform(3, 5))
    
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}Search interrupted by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
    finally:
        # Clean up
        try:
            driver.quit()
        except:
            pass
        
        if all_results:
            save_option = input(f"{Fore.YELLOW}Do you want to save the results to a file? (y/n): {Style.RESET_ALL}").strip().lower()
            if save_option == 'y':
                filename = input(f"{Fore.YELLOW}Enter the filename (e.g., results.txt): {Style.RESET_ALL}").strip()
                if save_results(all_results, filename):
                    print(f"{Fore.GREEN}Results saved to {filename}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to save results.{Style.RESET_ALL}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Google Dorking Tool")
    parser.add_argument('site', help="Enter the site URL to perform dorking on")
    args = parser.parse_args()
    
    perform_dorking(args.site)