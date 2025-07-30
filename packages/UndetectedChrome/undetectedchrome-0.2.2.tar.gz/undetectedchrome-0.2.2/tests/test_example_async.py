import asyncio
from UndetectedChrome.undetected_chrome import UndetectedChrome

async def main():
    async with UndetectedChrome() as browser:
        await browser.navigate_to("https://example.com")
        html = await browser.get_html()
        print("HTML length:", len(html))
        # Get specific request body
        request_url = "https://example.com/"
        body = await browser.get_response_body_by_url(request_url)
        print("Request body:", body[:100] if body else "No body found")  # Print first 100 characters
        print("Request summary:", browser.get_request_summary())
        print("Request info:", browser.get_captured_requests())

asyncio.run(main())