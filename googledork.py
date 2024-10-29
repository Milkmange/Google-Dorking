from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

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

# Expanded list of Google dorks
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
    'site:{site} intext:"sql syntax error"',
    'site:{site} "Apache/2.4.1 (Unix)" "PHP/5.4.0"',
    'site:{site} ext:swf',
    'site:{site} ext:db',
    'site:{site} ext:log',
    'site:{site} ext:bkf',
    'site:{site} ext:cfg',
    'site:{site} "SQL syntax" "mysql_fetch_array()" "supplied argument is not a valid MySQL result resource"',
    
    # Additional dangerous dorks
    'site:{site} inurl:/admin/ "Dashboard" -inurl:login',
    'site:{site} inurl:config.php',
    'site:{site} inurl:admin.php',
    'site:{site} "DB_PASSWORD" filetype:env',
    'site:{site} "auth" "unauthorized"',
    'site:{site} inurl:/config/ "db_password"',
    'site:{site} "SQL syntax" "error" "supplied argument is not a valid MySQL result resource"',
    'site:{site} inurl:admin/login "Dashboard"',
    'site:{site} "You have an error in your SQL syntax"',
    'site:{site} intitle:"Index of" inurl:/.git',
    'site:{site} intitle:"Index of" inurl:/.svn',
    'site:{site} inurl:".git/config"',
    'site:{site} inurl:".svn/entries"',
    'site:{site} inurl:/backups/ "Index of"',
    'site:{site} inurl:/uploads/ "Index of"',
    'site:{site} "Backup" "SQL"',
    'site:{site} inurl:phpinfo.php',
    'site:{site} "index of" "config"',
    
    # Additional common dorks
    'site:{site} "index of" .git',
    'site:{site} "index of" .svn',
    'site:{site} "server at" "Apache" "ServerRoot"',
    'site:{site} "Powered by" "Joomla!"',
    'site:{site} "Error" "Warning" "Exception"',
    'site:{site} "Admin" "Login"',
    'site:{site} intitle:"Welcome to" "default page"',
    'site:{site} "Backup" "Download"',
    'site:{site} filetype:pdf "confidential"',
    'site:{site} "Unprotected" "files"',
    'site:{site} "Error in MySQL query"',
    'site:{site} "database error" "MySQL"',
    'site:{site} inurl:admin "login" "username"',
    'site:{site} inurl:/phpmyadmin "Index of"',
    'site:{site} "index of" "backup"',
    'site:{site} inurl:admin "config" "password"',
    
    # GitHub dorks
    'site:github.com {site} "password"',
    'site:github.com {site} "secret"',
    'site:github.com {site} "private_key"',
    'site:github.com {site} "api_key"',
    'site:github.com {site} "access_token"',
    'site:github.com {site} "access_key"',
    'site:github.com {site} "access-token"',
    'site:github.com {site} "access_token"',
    'site:github.com {site} "accesstoken"',
    'site:github.com {site} "access_token_secret"',
    'site:github.com {site} "admin"',
    'site:github.com {site} "admin_pass"',
    'site:github.com {site} "admin_user"',
    'site:github.com {site} "algolia_admin_key"',
    'site:github.com {site} "algolia_api_key"',
    'site:github.com {site} "alias_pass"',
    'site:github.com {site} "alicloud_access_key"',
    'site:github.com {site} "amazonaws"',
    'site:github.com {site} "amazon_secret_access_key"',
    'site:github.com {site} "ansible_vault_password"',
    'site:github.com {site} "aos_key"',
    'site:github.com {site} "apidocs"',
    'site:github.com {site} "api.googlemaps AIza"',
    'site:github.com {site} "api.googlemaps+AIza"',
    'site:github.com {site} "api-key"',
    'site:github.com {site} "api_key"',
    'site:github.com {site} "apikey"',
    'site:github.com {site} "api_key_secret"',
    'site:github.com {site} "api_key_sid"',
    'site:github.com {site} "api_secret"',
    'site:github.com {site} "apiSecret"',
    'site:github.com {site} "api_secret_key"',
    'site:github.com {site} "api_token"',
    'site:github.com {site} "app_debug"',
    'site:github.com {site} "app_id"',
    'site:github.com {site} "app_key"',
    'site:github.com {site} "appkey"',
    'site:github.com {site} "appkeysecret"',
    'site:github.com {site} "application_key"',
    'site:github.com {site} "app_log_level"',
    'site:github.com {site} "app_secret"',
    'site:github.com {site} "appsecret"',
    'site:github.com {site} "appspot"',
    'site:github.com {site} "auth"',
    'site:github.com {site} "authentication"',
    'site:github.com {site} "authkey"',
    'site:github.com {site} "authorization"',
    'site:github.com {site} "authorization_bearer:"',
    'site:github.com {site} "authorization_key"',
    'site:github.com {site} "authorization_token"',
    'site:github.com {site} "authorizationToken"',
    'site:github.com {site} "authsecret"',
    'site:github.com {site} "auth_token"',
    'site:github.com {site} "authtoken"',
    'site:github.com {site} "aws_access"',
    'site:github.com {site} "aws_access_key_id"',
    'site:github.com {site} "aws_bucket"',
    'site:github.com {site} "aws_key"',
    'site:github.com {site} "aws_secret"',
    'site:github.com {site} "aws_secret_access_key"',
    'site:github.com {site} "aws_secret_key"',
    'site:github.com {site} "AWSSecretKey"',
    'site:github.com {site} "aws_token"',
    'site:github.com {site} "b2_app_key"',
    'site:github.com {site} "bashrc password"',
    'site:github.com {site} "bashrc+password"',
    'site:github.com {site} "bearer"',
    'site:github.com {site} "bintray_apikey"',
    'site:github.com {site} "bintray_gpg_password"',
    'site:github.com {site} "bintray_key"',
    'site:github.com {site} "bintraykey"',
    'site:github.com {site} "bluemix_api_key"',
    'site:github.com {site} "bluemix_pass"',
    'site:github.com {site} "bot_access_token"',
    'site:github.com {site} "browserstack_access_key"',
    'site:github.com {site} "bucket"',
    'site:github.com {site} "bucketeer_aws_access_key_id"',
    'site:github.com {site} "bucketeer_aws_secret_access_key"',
    'site:github.com {site} "bucket_password"',
    'site:github.com {site} "built_branch_deploy_key"',
    'site:github.com {site} "bx_password"',
    'site:github.com {site} "cache_driver"',
    'site:github.com {site} "cache_s3_secret_key"',
    'site:github.com {site} "cattle_access_key"',
    'site:github.com {site} "cattle_secret_key"',
    'site:github.com {site} "certificate_password"',
    'site:github.com {site} "ci_deploy_password"',
    'site:github.com {site} "client_id"',
    'site:github.com {site} "client_key"',
    'site:github.com {site} "client-secret"',
    'site:github.com {site} "client_secret"',
    'site:github.com {site} "clientsecret"',
    'site:github.com {site} "client_zpk_secret_key"',
    'site:github.com {site} "clojars_password"',
    'site:github.com {site} "cloudant_password"',
    'site:github.com {site} "cloud_api_key"',
    'site:github.com {site} "cloudflare_api_key"',
    'site:github.com {site} "cloudflare_auth_key"',
    'site:github.com {site} "cloudinary_api_secret"',
    'site:github.com {site} "cloudinary_name"',
    'site:github.com {site} "cloud_watch_aws_access_key"',
    'site:github.com {site} "codecov_token"',
    'site:github.com {site} "config"',
    'site:github.com {site} "connectionstring"',
    'site:github.com {site} "conn.login"',
    'site:github.com {site} "consumer_key"',
    'site:github.com {site} "ConsumerKey"',
    'site:github.com {site} "consumer_secret"',
    'site:github.com {site} "ConsumerSecret"',
    'site:github.com {site} "credentials"',
    'site:github.com {site} "cypress_record_key"',
    'site:github.com {site} "database_password"',
    'site:github.com {site} "database_schema_test"',
    'site:github.com {site} "datadog_api_key"',
    'site:github.com {site} "datadog_app_key"',
    'site:github.com {site} "DB_DATABASE="',
    'site:github.com {site} "DB_HOST="',
    'site:github.com {site} "dbpasswd"',
    'site:github.com {site} "db_password"',
    'site:github.com {site} "dbpassword"',
    'site:github.com {site} "DB_PASSWORD="',
    'site:github.com {site} "DB_PORT="',
    'site:github.com {site} "DB_PW="',
    'site:github.com {site} "db_server"',
    'site:github.com {site} "dbuser"',
    'site:github.com {site} "DB_USER="',
    'site:github.com {site} "db_username"',
    'site:github.com {site} "DB_USERNAME"',
    'site:github.com {site} "deploy_password"',
    'site:github.com {site} "digitalocean_ssh_key_body"',
    'site:github.com {site} "digitalocean_ssh_key_ids"',
    'site:github.com {site} "docker_hub_password"',
    'site:github.com {site} "dockerhub_password"',
    'site:github.com {site} "dockerhubpassword"',
    'site:github.com {site} "docker_key"',
    'site:github.com {site} "docker_pass"',
    'site:github.com {site} "docker_passwd"',
    'site:github.com {site} "docker_password"',
    'site:github.com {site} "dot-files"',
    'site:github.com {site} "dotfiles"',
    'site:github.com {site} "droplet_travis_password"',
    'site:github.com {site} "dynamoaccesskeyid"',
    'site:github.com {site} "dynamosecretaccesskey"',
    'site:github.com {site} "elastica_host"',
    'site:github.com {site} "elastica_port"',
    'site:github.com {site} "elasticsearch_password"',
    'site:github.com {site} "email"',
    'site:github.com {site} "encryption-key"',
    'site:github.com {site} "encryption_key"',
    'site:github.com {site} "encryptionkey"',
    'site:github.com {site} "encryption_password"',
    'site:github.com {site} "env.heroku_api_key"',
    'site:github.com {site} "env.sonatype_password"',
    'site:github.com {site} "eureka.awssecretkey"',
    'site:github.com {site} "fabricApiSecret"',
    'site:github.com {site} "facebook_secret"',
    'site:github.com {site} "fb_secret"',
    'site:github.com {site} "firebase"',
    'site:github.com {site} "flickr_api_key"',
    'site:github.com {site} "fossa_api_key"',
    'site:github.com {site} "ftp"',
    'site:github.com {site} "ftp_host"',
    'site:github.com {site} "ftp_password"',
    'site:github.com {site} "ftp_passwd"',
    'site:github.com {site} "ftppassword"',
    'site:github.com {site} "ftp_secret"',
    'site:github.com {site} "gh-token"',
    'site:github.com {site} "ghtoken"',
    'site:github.com {site} "github_access_token"',
    'site:github.com {site} "github_api_token"',
    'site:github.com {site} "github_key"',
    'site:github.com {site} "github_pass"',
    'site:github.com {site} "github_password"',
    'site:github.com {site} "github_secret"',
    'site:github.com {site} "gitlab_access_token"',
    'site:github.com {site} "gitlab_private_token"',
    'site:github.com {site} "gpg_passphrase"',
    'site:github.com {site} "gpgkey"',
    'site:github.com {site} "google_password"',
    'site:github.com {site} "google.secret"',
    'site:github.com {site} "gopass_secret"',
    'site:github.com {site} "gradle_password"',
    'site:github.com {site} "grant_type"',
    'site:github.com {site} "group_vars/all/vault_password"',
    'site:github.com {site} "GROUPID="',
    'site:github.com {site} "heroku_api_key"',
    'site:github.com {site} "heroku_git_url"',
    'site:github.com {site} "heroku_oauth_token"',
    'site:github.com {site} "heroku_secret"',
    'site:github.com {site} "heroku_secret_key"',
    'site:github.com {site} "herokutoken"',
    'site:github.com {site} "hostname"',
    'site:github.com {site} "host_password"',

    
    
    # SQL injection dorks
    'site:{site} inurl:"union select"',
    'site:{site} inurl:"select * from"',
    'site:{site} inurl:"and 1=1"',
    'site:{site} inurl:"or 1=1"',
    'site:{site} inurl:"error in"',
    'site:{site} inurl:"mysql_fetch_array"',
    
    # Added SQL injection dorks from your list
    'site:{site} inurl:view_items.php?id=',
    'site:{site} inurl:home.php?cat=',
    'site:{site} inurl:item_book.php?CAT=',
    'site:{site} inurl:www/index.php?page=',
    'site:{site} inurl:schule/termine.php?view=',
    'site:{site} inurl:goods_detail.php?data=',
    'site:{site} inurl:storemanager/contents/item.php?page_code=',
    'site:{site} inurl:view_items.php?id=',
    'site:{site} inurl:customer/board.htm?mode=',
    'site:{site} inurl:help/com_view.html?code=',
    'site:{site} inurl:n_replyboard.php?typeboard=',
    'site:{site} inurl:eng_board/view.php?T****=',
    'site:{site} inurl:prev_results.php?prodID=',
    'site:{site} inurl:bbs/view.php?no=',
    'site:{site} inurl:gnu/?doc=',
    'site:{site} inurl:zb/view.php?uid=',
    'site:{site} inurl:global/product/product.php?gubun=',
    'site:{site} inurl:m_view.php?ps_db=',
    'site:{site} inurl:productlist.php?tid=',
    'site:{site} inurl:product-list.php?id=',
    'site:{site} inurl:onlinesales/product.php?product_id=',
    'site:{site} inurl:garden_equipment/Fruit-Cage/product.php?pr=',
    'site:{site} inurl:product.php?shopprodid=',
    'site:{site} inurl:product_info.php?products_id=',
    'site:{site} inurl:productlist.php?tid=',
    'site:{site} inurl:showsub.php?id=',
    'site:{site} inurl:productlist.php?fid=',
    'site:{site} inurl:products.php?cat=',
    'site:{site} inurl:products.php?cat=',
    'site:{site} inurl:product-list.php?id=',
    'site:{site} inurl:product.php?sku=',
    'site:{site} inurl:store/product.php?productid=',
    'site:{site} inurl:products.php?cat=',
    'site:{site} inurl:productList.php?cat=',
    'site:{site} inurl:product_detail.php?product_id=',
    'site:{site} inurl:product.php?pid=',
    'site:{site} inurl:view_items.php?id=',
    'site:{site} inurl:more_details.php?id=',
    'site:{site} inurl:county-facts/diary/vcsgen.php?id=',
    'site:{site} inurl:idlechat/message.php?id=',
    'site:{site} inurl:podcast/item.php?pid=',
    'site:{site} inurl:products.php?act=',
    'site:{site} inurl:details.php?prodId=',
    'site:{site} inurl:socsci/events/full_details.php?id=',
    'site:{site} inurl:ourblog.php?categoryid=',
    'site:{site} inurl:mall/more.php?ProdID=',
    'site:{site} inurl:archive/get.php?message_id=',
    'site:{site} inurl:review/review_form.php?item_id=',
    'site:{site} inurl:english/publicproducts.php?groupid=',
    'site:{site} inurl:news_and_notices.php?news_id=',
    'site:{site} inurl:rounds-detail.php?id=',
    'site:{site} inurl:gig.php?id=',
    'site:{site} inurl:board/view.php?no=',
    'site:{site} inurl:index.php?modus=',
    'site:{site} inurl:news_item.php?id=',
    'site:{site} inurl:rss.php?cat=',
    'site:{site} inurl:products/product.php?id=',
    'site:{site} inurl:details.php?ProdID=',
    'site:{site} inurl:els_/product/product.php?id=',
    'site:{site} inurl:store/description.php?iddesc=',
    'site:{site} inurl:socsci/news_items/full_story.php?id=',
    'site:{site} inurl:naboard/memo.php?bd=',
    'site:{site} inurl:bookmark/mybook/bookmark.php?bookPageNo=',
    'site:{site} inurl:board/board.html?table=',
    'site:{site} inurl:kboard/kboard.php?board=',
    'site:{site} inurl:order.asp?lotid=',
    'site:{site} inurl:goboard/front/board_view.php?code=',
    'site:{site} inurl:bbs/bbsView.php?id=',
    'site:{site} inurl:boardView.php?bbs=',
    'site:{site} inurl:eng/rgboard/view.php?&bbs_id=',
    'site:{site} inurl:product/product.php?cate=',
    'site:{site} inurl:content.php?p=',
    'site:{site} inurl:page.php?module=',
    'site:{site} inurl:?pid=',
    'site:{site} inurl:bookpage.php?id=',
    'site:{site} inurl:cbmer/congres/page.php?LAN=',
    'site:{site} inurl:content.php?id=',
    'site:{site} inurl:news.php?ID=',
    'site:{site} inurl:photogallery.php?id=',
    'site:{site} inurl:index.php?id=',
    'site:{site} inurl:product/product.php?product_no=',
    'site:{site} inurl:nyheder.htm?show=',
    'site:{site} inurl:book.php?ID=',
    'site:{site} inurl:print.php?id=',
    'site:{site} inurl:detail.php?id=',
    'site:{site} inurl:book.php?id=',
    'site:{site} inurl:content.php?PID=',
    'site:{site} inurl:more_detail.php?id=',
    'site:{site} inurl:content.php?id=',
    'site:{site} inurl:view_items.php?id=',
    'site:{site} inurl:view_author.php?id=',
    'site:{site} inurl:main.php?id=',
    'site:{site} inurl:english/fonction/print.php?id=',
    'site:{site} inurl:magazines/adult_magazine_single_page.php?magid=',
    'site:{site} inurl:product_details.php?prodid=',
    'site:{site} inurl:magazines/adult_magazine_full_year.php?magid=',
    'site:{site} inurl:products/card.php?prodID=',
    'site:{site} inurl:catalog/product.php?cat_id=',
    'site:{site} inurl:e_board/modifyform.html?code=',
    'site:{site} inurl:community/calendar-event-fr.php?id=',
    'site:{site} inurl:products.php?p=',
    'site:{site} inurl:news.php?id=',
    'site:{site} inurl:StoreRedirect.php?product=',

    
]

def init_browser():
    # Initialize Firefox browser
    options = FirefoxOptions()
    options.add_argument("--headless")  # Run in headless mode (no UI)
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    return driver

def google_search(driver, query):
    search_url = f"https://www.google.com/search?q={query}"
    driver.get(search_url)
    time.sleep(2)  # Wait for the page to load
    
    # Parse the result page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = []
    
    for g in soup.find_all('div', class_='g'):
        link = g.find('a')
        if link:
            results.append(link.get('href'))
    
    return results

def save_results(results, filename):
    with open(filename, 'w') as file:
        for result in results:
            file.write(result + '\n')

def perform_dorking(site):
    print_banner()  # Print banner
    driver = init_browser()
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

    driver.quit()

    # Ask user if they want to save the results
    save_option = input(f"{Fore.YELLOW}Do you want to save the results to a file? (y/n): {Style.RESET_ALL}").strip().lower()
    if save_option == 'y':
        filename = input(f"{Fore.YELLOW}Enter the filename (e.g., results.txt): {Style.RESET_ALL}").strip()
        save_results(all_results, filename)
        print(f"{Fore.GREEN}Results saved to {filename}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Results not saved.{Style.RESET_ALL}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Google Dorking Tool")
    parser.add_argument('site', help="Enter the site URL to perform dorking on")
    args = parser.parse_args()

    perform_dorking(args.site)
