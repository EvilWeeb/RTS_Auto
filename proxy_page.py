# proxy_page.py
import datetime, os

class LoggingLocator:
    def __init__(self, locator, logger, store_code, desc, page):
        self._locator = locator
        self._logger = logger
        self._store_code = store_code
        self._desc = desc
        self._page = page

    def _log(self, action, success=True, exception=None):
        if self._store_code == "__init__":
            return
        if success:
            self._logger.log_success(self._store_code, f"{action}: {self._desc}")
        else:
            self._logger.log_failure(self._store_code, f"{action}: {self._desc}", exception)

    def _screenshot(self, action):
        if self._store_code == "__init__":
            return
        path = self._logger.get_screenshot_path(self._store_code, action)
        try:
            self._page.screenshot(path=path, full_page=True)
            print(f"📸 截图已保存：{path}")
        except Exception as e:
            print(f"⚠️ 截图失败：{e}")

    def click(self, *args, **kwargs):
        try:
            result = self._locator.click(*args, **kwargs)
            self._log("click")
            return result
        except Exception as e:
            self._log("click", False, e)
            self._screenshot("click")
            raise

    def fill(self, value, *args, **kwargs):
        try:
            result = self._locator.fill(value, *args, **kwargs)
            self._log("fill")
            return result
        except Exception as e:
            self._log("fill", False, e)
            self._screenshot("fill")
            raise

    # def hover(self, *args, **kwargs):
    #     try:
    #         result = self._locator.hover(*args, **kwargs)
    #         self._log("hover")
    #         return result
    #     except Exception as e:
    #         self._log("hover", False, e)
    #         self._screenshot("hover")
    #         raise

    def __getattr__(self, name):
        return getattr(self._locator, name)

class ProxyPage:
    def __init__(self, page, logger, store_code):
        self._page = page
        self._logger = logger
        self._store_code = store_code

    def get_by_text(self, *args, **kwargs):
        desc = f"text={args[0] if args else ''}"
        locator = self._page.get_by_text(*args, **kwargs)
        return LoggingLocator(locator, self._logger, self._store_code, desc, self._page)

    def get_by_role(self, *args, **kwargs):
        desc = f"role={args[0] if args else ''} name={kwargs.get('name', '')}"
        locator = self._page.get_by_role(*args, **kwargs)
        return LoggingLocator(locator, self._logger, self._store_code, desc, self._page)

    def get_by_placeholder(self, *args, **kwargs):
        desc = f"placeholder={args[0] if args else ''}"
        locator = self._page.get_by_placeholder(*args, **kwargs)
        return LoggingLocator(locator, self._logger, self._store_code, desc, self._page)

    def locator(self, *args, **kwargs):
        desc = f"locator={args[0] if args else ''}"
        locator = self._page.locator(*args, **kwargs)
        return LoggingLocator(locator, self._logger, self._store_code, desc, self._page)
    
    def __getattr__(self, name):
        return getattr(self._page, name)
