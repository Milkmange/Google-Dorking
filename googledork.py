from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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

# Keep your original DORKS list
DORKS = [
    'site:{site} inurl:admin',
    'site:{site} inurl:login',
    # ... rest of your dorks ...
]

def init_browser():
    """Initialize Firefox browser with improved options"""
    try:
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Add user agent to appear more like a regular browser
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_page_load_timeout(30)
        
        return driver
    except Exception as e:
        print(f"{Fore.RED}Error initializing browser: {str(e)}{Style.RESET_ALL}")
        return None

def google_search(driver, query):
    """Perform Google search with improved error handling and detection avoidance"""
    try:
        # Encode the query for URL
        search_url = f"https://www.google.com/search?q={query}"
        driver.get(search_url)
        
        # Random delay between 2-4 seconds
        time.sleep(random.uniform(2, 4))
        
        try:
            # Wait for either search results or captcha
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "search")) or
                EC.presence_of_element_located((By.ID, "captcha-form"))
            )
        except TimeoutException:
            print(f"{Fore.YELLOW}Warning: Page took too long to load{Style.RESET_ALL}")
            return []

        # Check for CAPTCHA
        if "Our systems have detected unusual traffic" in driver.page_source:
            print(f"{Fore.RED}Google CAPTCHA detected! Waiting longer before next request...{Style.RESET_ALL}")
            time.sleep(random.uniform(30, 60))  # Longer wait when CAPTCHA is detected
            return []

        # Parse results using both methods
        results = set()  # Use set to avoid duplicates
        
        # Method 1: Parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for result in soup.find_all('div', class_=['g', 'rc']):
            link = result.find('a')
            if link and link.get('href'):
                url = link.get('href')
                if url.startswith('http'):
                    results.add(url)

        # Method 2: Direct Selenium approach
        try:
            links = driver.find_elements(By.CSS_SELECTOR, 'div.g a')
            for link in links:
                url = link.get_attribute('href')
                if url and url.startswith('http'):
                    results.add(url)
        except NoSuchElementException:
            pass

        return list(results)

    except Exception as e:
        print(f"{Fore.RED}Error during search: {str(e)}{Style.RESET_ALL}")
        return []

def perform_dorking(site):
    """Main dorking function with improved error handling and rate limiting"""
    print_banner()
    
    driver = init_browser()
    if not driver:
        return
    
    try:
        all_results = []
        
        for i, dork in enumerate(DORKS):
            query = dork.format(site=site)
            print(f"\n{Fore.CYAN}[{i+1}/{len(DORKS)}] Performing Google Dork: {Fore.YELLOW}{query}{Style.RESET_ALL}")
            
            results = google_search(driver, query)
            
            if results:
                all_results.extend(results)
                print(f"\n{Fore.GREEN}Found {len(results)} results:{Style.RESET_ALL}")
                for result in results:
                    print(f"{Fore.LIGHTBLUE_EX}→ {result}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}No results found{Style.RESET_ALL}")
            
            print(f"{Fore.MAGENTA}{'-' * 80}{Style.RESET_ALL}")
            
            # Random delay between searches (5-10 seconds)
            if i < len(DORKS) - 1:  # Don't wait after the last dork
                wait_time = random.uniform(5, 10)
                print(f"{Fore.CYAN}Waiting {wait_time:.1f} seconds before next search...{Style.RESET_ALL}")
                time.sleep(wait_time)
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Search interrupted by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
    finally:
        try:
            driver.quit()
        except:
            pass
        
        if all_results:
            save_option = input(f"\n{Fore.YELLOW}Do you want to save the results to a file? (y/n): {Style.RESET_ALL}").strip().lower()
            if save_option == 'y':
                filename = input(f"{Fore.YELLOW}Enter the filename (e.g., results.txt): {Style.RESET_ALL}").strip()
                try:
                    with open(filename, 'w') as f:
                        for result in all_results:
                            f.write(result + '\n')
                    print(f"{Fore.GREEN}Results saved to {filename}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Error saving results: {str(e)}{Style.RESET_ALL}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Google Dorking Tool")
    parser.add_argument('site', help="Enter the site URL to perform dorking on")
    args = parser.parse_args()
    
    perform_dorking(args.site)