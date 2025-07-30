from UndetectedChrome import UndetectedChromeSync

with UndetectedChromeSync() as browser:
    browser.navigate_to("https://example.com")
    html = browser.get_html()
    print("HTML length:", len(html))
    # screenshot_path = browser.take_screenshot("screenshot.png")
    # print("Screenshot saved at:", screenshot_path)
    # requests = browser.get_captured_requests()
    # print("Request summary:", browser.get_request_summary())
    # body = browser.get_response_body_by_url("https://example.com/api/test")
    # print("Request body:", body)