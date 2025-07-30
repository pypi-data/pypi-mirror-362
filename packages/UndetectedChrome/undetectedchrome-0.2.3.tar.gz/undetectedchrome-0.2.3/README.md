
## Build and Publish

To build the package (recommended):

```bash
python -m build
```

Or using setuptools directly:

```bash
python setup.py sdist bdist_wheel
```

To publish to PyPI:

```bash
pip install twine
twine upload dist/*
twine upload -u __token__ -p $PYPI dist/* # If using environment variable for token
```
## Running Tests

To run the synchronous example test:

```bash
python -m tests.test_example_sync
python -m tests.test_example_async
```


# UndetectedChrome

A comprehensive browser automation class using nodriver.

## Installation

```bash
pip install UndetectedChrome
```

## Usage

### Command Line Usage
After installing, you can use the CLI to fetch HTML from a URL:

```bash
uc https://example.com
```
This will print the HTML of the page to stdout.

### Synchronous API Example
You can use the synchronous wrapper for all major features:

```python
from UndetectedChrome.undetected_chrome import UndetectedChromeSync

browser = UndetectedChromeSync(headless=True)
browser.start_browser()
browser.navigate_to("https://example.com")
html = browser.get_html()
print("HTML length:", len(html))
screenshot_path = browser.take_screenshot("screenshot.png")
print("Screenshot saved at:", screenshot_path)
requests = browser.get_captured_requests()
print("Request summary:", browser.get_request_summary())
body = browser.get_response_body_by_url("https://example.com/api/test")
print("Request body:", body)
browser.close()
```

See `UndetectedChrome/undetected_chrome.py` for usage examples.
git clone https://github.com/yourusername/UndetectedChrome.git
cd UndetectedChrome
```

## Usage

### Quick Example
```python
import asyncio
from UndetectedChrome.undetected_chrome import quick_browse

async def main():
    result = await quick_browse(
        url="https://example.com",
        screenshot=True,
        capture_requests=True,
        headless=True
    )
    print("HTML length:", len(result["html"]))
    print("Screenshot saved at:", result["screenshot_path"])
    print("Request summary:", result["request_summary"])

asyncio.run(main())
```

### Full Control Example
```python
import asyncio
from UndetectedChrome.undetected_chrome import UndetectedChrome

async def main():
    async with NoDriverBrowser(headless=True, stealth_mode=True) as browser:
        await browser.navigate_to("https://example.com")
        html = await browser.get_html()
        print("HTML length:", len(html))
        # Get specific request body
        request_url = "https://example.com/api/test"
        body = await browser.get_response_body_by_url(request_url)
        print("Request body:", body)
        print("Request summary:", browser.get_request_summary())

asyncio.run(main())
```

## Capturing Requests
To get all captured requests:
```python
requests = browser.get_captured_requests()
```
To filter by type (e.g., 'Document', 'Script', 'Image'):
```python
scripts = browser.get_captured_requests(filter_type='Script')
```

## Testing
See `test_UndetectedChrome.py` for a test script.

## Requirements
- Python 3.8+
- nodriver

## License
MIT
