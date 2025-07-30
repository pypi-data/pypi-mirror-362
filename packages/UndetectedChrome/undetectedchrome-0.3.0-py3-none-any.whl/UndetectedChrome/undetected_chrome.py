import asyncio
from typing import Dict, List, Optional, Any, Union
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
    Browser automation class using nodriver, with stealth, request capture, HTML extraction, and screenshot.
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
        self.requests_info: Dict[str, Any] = {}
        self._request_handlers_setup = False

    async def start_browser(self) -> None:
        browser_args = [f'--user-agent={self.user_agent}']
        if self.stealth_mode:
            browser_args += [
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
            ]
        try:
            self.browser = await start(
                headless=self.headless,
                window_size=self.window_size,
                browser_args=browser_args
            )
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
        # Use browser[0] for first tab, nodriver style
        tab = self.browser[0]
        tab.add_handler(cdp.network.ResponseReceived, handler=self._response_received_handler)
        tab.add_handler(cdp.network.LoadingFinished, handler=self._loading_finished_handler)
        self._request_handlers_setup = True

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
        if not info or not info["url"].startswith("http"):
            return
        try:
            body, base64encoded = await tab.send(cdp.network.get_response_body(req_id))
            info.update({
                "body": body,
                "isBase64": base64encoded,
                "content_length": len(body) if body else 0
            })
        except Exception as e:
            info["error"] = str(e)

    async def navigate_to(self, url: str, wait_time: float = 0.0) -> None:
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
        await asyncio.sleep(wait_time)
        await self.page.wait()

    async def get_html(self) -> str:
        if not self.page:
            raise RuntimeError("No page loaded. Call navigate_to() first.")
        return await self.page.get_content()

    async def take_screenshot(self, filename: str = "screenshot.png") -> str:
        if not self.page:
            raise RuntimeError("No page loaded. Call navigate_to() first.")
        await self.page.save_screenshot(filename)
        return filename

    def get_captured_requests(self, filter_type: Optional[str] = None) -> Dict[str, Any]:
        if filter_type:
            return {req_id: info for req_id, info in self.requests_info.items() if info.get("type") == filter_type}
        return self.requests_info.copy()

    def get_request_summary(self) -> Dict[str, int]:
        summary: Dict[str, int] = {}
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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        await asyncio.sleep(0.1)

    async def get_response_body_by_url(self, url_or_urls: Union[str, List[str]]) -> Union[str, List[str], None]:
        if not self.requests_info:
            raise RuntimeError("No requests captured yet.")
        urls = [url_or_urls] if isinstance(url_or_urls, str) else list(url_or_urls)
        bodies = [req["body"] for req in self.requests_info.values() if req.get("url") in urls and "body" in req]
        if isinstance(url_or_urls, str):
            return bodies[0] if bodies else None
        return bodies

class UndetectedChromeSync:
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
        self._browser_async = UndetectedChrome(
            headless=self.headless,
            window_size=self.window_size,
            custom_user_agent=self.custom_user_agent,
            stealth_mode=self.stealth_mode
        )
        self._loop.run_until_complete(self._browser_async.start_browser())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def start_browser(self):
        self._loop.run_until_complete(self._browser_async.start_browser())

    def setup_request_handlers(self):
        self._loop.run_until_complete(self._browser_async.setup_request_handlers())

    def navigate_to(self, url, wait_time=0.0):
        self._loop.run_until_complete(self._browser_async.navigate_to(url, wait_time))

    def get_html(self):
        return self._loop.run_until_complete(self._browser_async.get_html())

    def take_screenshot(self, filename="screenshot.png"):
        return self._loop.run_until_complete(self._browser_async.take_screenshot(filename))

    def get_captured_requests(self, filter_type=None):
        return self._browser_async.get_captured_requests(filter_type)

    def get_request_summary(self):
        return self._browser_async.get_request_summary()

    def get_response_body_by_url(self, url_or_urls):
        return self._loop.run_until_complete(self._browser_async.get_response_body_by_url(url_or_urls))

    def close(self):
        if self._browser_async is not None:
            self._loop.run_until_complete(self._browser_async.close())
            self._browser_async = None

    def quick_browse_sync(self, url: str, screenshot: bool = True, capture_requests: bool = True, headless: bool = True, wait_time: float = 0.0) -> Dict[str, Any]:
        """
        Synchronous version of quick_browse using UndetectedChromeSync, with wait_time.
        """
        with UndetectedChromeSync(headless=headless) as browser:
            browser.navigate_to(url, wait_time=wait_time)
            result = {
                "html": browser.get_html(),
                "url": url
            }
            if screenshot:
                result["screenshot_path"] = browser.take_screenshot()
            if capture_requests:
                result["requests"] = browser.get_captured_requests()
                result["request_summary"] = browser.get_request_summary()
            browser.close()
            return result

async def quick_browse(
    url: str,
    screenshot: bool = True,
    capture_requests: bool = True,
    headless: bool = True,
    wait_time: float = 0.0
) -> Dict[str, Any]:
    async with UndetectedChrome(headless=headless) as browser:
        await browser.navigate_to(url, wait_time=wait_time)
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