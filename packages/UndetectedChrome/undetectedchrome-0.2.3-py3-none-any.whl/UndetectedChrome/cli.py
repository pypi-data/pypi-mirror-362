import argparse
from UndetectedChrome.undetected_chrome import UndetectedChromeSync

def main():
    parser = argparse.ArgumentParser(description="Fetch HTML from a URL using UndetectedChrome.")
    parser.add_argument("url", help="URL to fetch")
    args = parser.parse_args()

    browser = UndetectedChromeSync()
    url = args.url
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    browser.navigate_to(url)
    html = browser.get_html()
    print(html)

if __name__ == "__main__":
    main()
