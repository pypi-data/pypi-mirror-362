import asyncio
from UndetectedChrome.undetected_chrome import UndetectedChrome, quick_browse

async def test_quick_browse():
    url = "https://www.tesla.com/careers/search/?site=US"
    result = await quick_browse(url)
    assert "html" in result
    assert "screenshot_path" in result
    assert "requests" in result
    assert "request_summary" in result
    print("Quick browse test passed.")

async def test_manual_browse():
    url = "https://www.tesla.com/careers/search/?site=US"
    request_url = "https://www.tesla.com/api/tesla/header/v1_1/careers"
    async with UndetectedChrome(headless=True, stealth_mode=True) as browser:
        await browser.navigate_to(url)
        html = await browser.get_html()
        assert html and isinstance(html, str)
        body = await browser.get_response_body_by_url(request_url)
        print(f"Request body length: {len(body) if body else 0}")
        print(f"Request body content: {body[:100]}...")  # Print first 100 characters
        print(f"Request Summary: {browser.get_request_summary()}")
        print("Manual browse test passed.")


async def main():
    await test_quick_browse()
    await test_manual_browse()
    await asyncio.sleep(1)  # Give subprocesses time to clean up

if __name__ == "__main__":
    asyncio.run(main())
