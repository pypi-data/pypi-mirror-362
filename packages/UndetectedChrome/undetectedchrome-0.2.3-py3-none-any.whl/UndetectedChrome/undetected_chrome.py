import asyncio
from typing import Dict, List, Optional, Any
import os
import sys

try:
    from nodriver import start, loop, cdp
    from nodriver.cdp.emulation import set_device_metrics_override
except (ModuleNotFoundError, ImportError):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from nodriver import start, loop, cdp
    from nodriver.cdp.emulation import set_device_metrics_override

class UndetectedChrome:
    """
    A comprehensive browser automation class using nodriver with stealth mode,
    request capturing, HTML extraction, and screenshot functionality.
    """
    def __init__(
        self,
        headless: bool = True,
        window_size: tuple = (1920, 1080),
        custom_user_agent: Optional[str] = None,
        stealth_mode: bool = True
    ):
        self.headless = headless
        self.window_size = window_size
        self.stealth_mode = stealth_mode
        self.user_agent = custom_user_agent or (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        )
        self.browser = None
        self.page = None
        self.requests_info = {}
        self._request_handlers_setup = False

    async def start_browser(self) -> None:
        browser_args = [f'--user-agent={self.user_agent}']
        if self.stealth_mode:
            browser_args.extend([
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-dev-shm-usage',
                '--disable-images',
                '--disable-javascript-harmony-shipping',
                '--disable-background-timer-throttling',
                '--disable-renderer-backgrounding',
                '--disable-backgrounding-occluded-windows',
                '--disable-features=TranslateUI,BlinkGenPropertyTrees',
                '--disable-ipc-flooding-protection'
            ])
        try:
            self.browser = await start(
                headless=self.headless,
                window_size=self.window_size,
                browser_args=browser_args
            )
            print(f"Browser started - Headless: {self.headless}, Stealth: {self.stealth_mode}")
        except Exception as e:
            msg = str(e)
            if "Failed to connect to browser" in msg and "root" in msg:
                print("Error: Failed to connect to browser. You are NOT running as root. Please check your Chrome/Chromium installation and PATH.")
            else:
                print(f"Error: Failed to connect to browser: {msg}")
            raise

    async def setup_request_handlers(self) -> None:
        if not self.browser or self._request_handlers_setup:
            return
        self.requests_info.clear()
        self.browser[0].add_handler(
            cdp.network.ResponseReceived, 
            handler=self._response_received_handler
        )
        self.browser[0].add_handler(
            cdp.network.LoadingFinished, 
            handler=self._loading_finished_handler
        )
        self._request_handlers_setup = True
        print("Request handlers setup complete")

    async def _response_received_handler(self, ev: cdp.network.ResponseReceived, tab=None) -> None:
        if not ev.response.url.startswith("chrome://"):
            self.requests_info[ev.request_id] = {
                "url": ev.response.url,
                "type": str(ev.type_),
                "status": ev.response.status,
                "headers": dict(ev.response.headers) if ev.response.headers else {}
            }

    async def _loading_finished_handler(self, ev: cdp.network.LoadingFinished, tab=None) -> None:
        req_id = ev.request_id
        info = self.requests_info.get(req_id)
        if not info:
            return
        if not info["url"].startswith("http"):
            return
        try:
            body, base64encoded = await tab.send(cdp.network.get_response_body(req_id))
            self.requests_info[req_id].update({
                "body": body,
                "isBase64": base64encoded,
                "content_length": len(body) if body else 0
            })
        except Exception as e:
            self.requests_info[req_id]["error"] = str(e)

    async def navigate_to(self, url: str, wait_time: float = 2.0) -> None:
        if not self.browser:
            await self.start_browser()
        if not self._request_handlers_setup:
            await self.setup_request_handlers()
        self.page = await self.browser.get(url)
        await self.page.set_window_size(*self.window_size)
        await self.page.send(
            set_device_metrics_override(
                width=self.window_size[0],
                height=self.window_size[1],
                device_scale_factor=1,
                mobile=False,
                screen_width=self.window_size[0],
                screen_height=self.window_size[1]
            )
        )
        await asyncio.sleep(0.2)
        await asyncio.sleep(wait_time)
        await self.page.wait()
        print(f"Successfully navigated to: {url}")

    async def get_html(self) -> str:
        if not self.page:
            raise RuntimeError("No page loaded. Call navigate_to() first.")
        html = await self.page.get_content()
        return html

    async def take_screenshot(self, filename: str = "screenshot.png") -> str:
        if not self.page:
            raise RuntimeError("No page loaded. Call navigate_to() first.")
        await self.page.save_screenshot(filename)
        print(f"Screenshot saved as: {filename}")
        return filename

    def get_captured_requests(self, filter_type: Optional[str] = None) -> Dict[str, Any]:
        if filter_type:
            return {
                req_id: info for req_id, info in self.requests_info.items()
                if info.get("type") == filter_type
            }
        return self.requests_info.copy()

    def get_request_summary(self) -> Dict[str, int]:
        summary = {}
        for info in self.requests_info.values():
            req_type = info.get("type", "Unknown")
            summary[req_type] = summary.get(req_type, 0) + 1
        return summary

    async def close(self) -> None:
        if self.browser:
            try:
                stop_method = getattr(self.browser, "stop", None)
                if stop_method:
                    if asyncio.iscoroutinefunction(stop_method):
                        await stop_method()
                    else:
                        stop_method()
                await asyncio.sleep(0.1)
            except Exception as e:
                import websockets
                if not (isinstance(e, websockets.exceptions.ConnectionClosedOK) or e.__class__.__name__ == "ConnectionClosedOK"):
                    print(f"Error during browser shutdown: {e}")
            self.browser = None
            self.page = None
            self._request_handlers_setup = False
            print("Browser closed")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        await asyncio.sleep(0.1)

    async def get_response_body_by_url(self, url_or_urls):
        if not self.requests_info:
            raise RuntimeError("No requests captured yet.")
        if isinstance(url_or_urls, str):
            urls = [url_or_urls]
            single = True
        else:
            urls = list(url_or_urls)
            single = False
        bodies = []
        for req in self.requests_info.values():
            if req.get("url") in urls and "body" in req:
                bodies.append(req["body"])
        if single:
            return bodies[0] if bodies else None
        return bodies

class UndetectedChromeSync:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    """
    Synchronous wrapper for UndetectedChrome async API.
    """
    def __init__(self, headless=True, window_size=(1920, 1080), custom_user_agent=None, stealth_mode=True):
        self.headless = headless
        self.window_size = window_size
        self.custom_user_agent = custom_user_agent
        self.stealth_mode = stealth_mode
        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        browser_instance = UndetectedChrome(
            headless=self.headless,
            window_size=self.window_size,
            custom_user_agent=self.custom_user_agent,
            stealth_mode=self.stealth_mode
        )
        async def runner():
            await browser_instance.start_browser()
        self._loop.run_until_complete(runner())
        self._browser_async = browser_instance

    def start_browser(self):
        browser_instance = UndetectedChrome(
            headless=self.headless,
            window_size=self.window_size,
            custom_user_agent=self.custom_user_agent,
            stealth_mode=self.stealth_mode
        )
        async def runner():
            await browser_instance.start_browser()
        self._loop.run_until_complete(runner())
        self._browser_async = browser_instance

    def setup_request_handlers(self):
        async def runner():
            await self._browser_async.setup_request_handlers()
        self._loop.run_until_complete(runner())

    def navigate_to(self, url, wait_time=2.0):
        async def runner():
            await self._browser_async.navigate_to(url, wait_time)
        self._loop.run_until_complete(runner())

    def get_html(self):
        async def runner():
            return await self._browser_async.get_html()
        return self._loop.run_until_complete(runner())

    def take_screenshot(self, filename="screenshot.png"):
        async def runner():
            return await self._browser_async.take_screenshot(filename)
        return self._loop.run_until_complete(runner())

    def get_captured_requests(self, filter_type=None):
        return self._browser_async.get_captured_requests(filter_type)

    def get_request_summary(self):
        return self._browser_async.get_request_summary()

    def get_response_body_by_url(self, url_or_urls):
        async def runner():
            return await self._browser_async.get_response_body_by_url(url_or_urls)
        return self._loop.run_until_complete(runner())

    def close(self):
        if self._browser_async is None:
            return
        async def runner():
            await self._browser_async.close()
        self._loop.run_until_complete(runner())
        self._browser_async = None

async def quick_browse(
    url: str,
    screenshot: bool = True,
    capture_requests: bool = True,
    headless: bool = True
) -> Dict[str, Any]:
    async with UndetectedChrome(headless=headless) as browser:
        await browser.navigate_to(url)
        result = {
            "html": await browser.get_html(),
            "url": url
        }
        if screenshot:
            result["screenshot_path"] = await browser.take_screenshot()
        if capture_requests:
            result["requests"] = browser.get_captured_requests()
            result["request_summary"] = browser.get_request_summary()
        return result
