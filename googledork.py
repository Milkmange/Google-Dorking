from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import chromedriver_autoinstaller
import time
import random
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from fake_useragent import UserAgent

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

def init_browser():
    """Initialize Chrome browser with proper version"""
    try:
        # Automatically install the correct chromedriver version
        chromedriver_autoinstaller.install()
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Use random user agent
        ua = UserAgent()
        options.add_argument(f'user-agent={ua.random}')
        
        # Additional stealth settings
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)
        
        return driver
    except Exception as e:
        print(f"{Fore.RED}Error initializing browser: {str(e)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Try updating Chrome to the latest version or run: pip install --upgrade chromedriver-autoinstaller{Style.RESET_ALL}")
        return None

def google_search(driver, query):
    """Perform Google search with improved stealth"""
    results = []
    try:
        # Add random delay before search
        time.sleep(random.uniform(2, 5))
        
        search_url = f"https://www.google.com/search?q={query}"
        driver.get(search_url)
        
        # Random scroll behavior
        for _ in range(random.randint(1, 3)):
            driver.execute_script(f"window.scrollTo(0, {random.randint(100, 500)});")
            time.sleep(random.uniform(0.5, 1.5))
        
        # Wait for results
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        
        # Extract results using both methods
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Method 1: Parse citation links
        for cite in soup.find_all('cite'):
            if cite.text.strip().startswith(('http', 'www')):
                results.append(cite.text.strip())
                
        # Method 2: Parse regular result links
        for div in soup.find_all('div', class_='yuRUbf'):
            link = div.find('a')
            if link and link.get('href'):
                results.append(link['href'])
                
        return list(set(results))  # Remove duplicates
        
    except TimeoutException:
        print(f"{Fore.YELLOW}Warning: Page took too long to load{Style.RESET_ALL}")
    except WebDriverException as e:
        print(f"{Fore.RED}Browser error: {str(e)}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error during search: {str(e)}{Style.RESET_ALL}")
    
    return results

def perform_dorking(site):
    print_banner()
    driver = init_browser()
    if not driver:
        return
    
    try:
        all_results = []
        total_dorks = len(DORKS)
        
        for i, dork in enumerate(DORKS, 1):
            query = dork.format(site=site)
            print(f"\n{Fore.CYAN}[{i}/{total_dorks}] Performing Google Dork: {query}{Style.RESET_ALL}")
            
            results = google_search(driver, query)
            
            if results:
                print(f"\n{Fore.GREEN}Found {len(results)} results:{Style.RESET_ALL}")
                for result in results:
                    print(f"{Fore.LIGHTBLUE_EX}→ {result}{Style.RESET_ALL}")
                all_results.extend(results)
            else:
                print(f"{Fore.YELLOW}No results found{Style.RESET_ALL}")
            
            # Add longer random delay between searches
            if i < total_dorks:
                wait_time = random.uniform(8, 15)
                print(f"\n{Fore.CYAN}Waiting {wait_time:.1f} seconds before next search...{Style.RESET_ALL}")
                time.sleep(wait_time)
                
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Search interrupted by user{Style.RESET_ALL}")
    finally:
        if driver:
            driver.quit()
        
        if all_results:
            save = input(f"\n{Fore.YELLOW}Save results to file? (y/n): {Style.RESET_ALL}").lower()
            if save == 'y':
                filename = input(f"{Fore.YELLOW}Enter filename: {Style.RESET_ALL}")
                with open(filename, 'w') as f:
                    for result in all_results:
                        f.write(result + '\n')
                print(f"{Fore.GREEN}Results saved to {filename}{Style.RESET_ALL}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Google Dorking Tool")
    parser.add_argument('site', help="Target site URL")
    args = parser.parse_args()
    perform_dorking(args.site)