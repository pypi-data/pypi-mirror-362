from dataclasses import dataclass
from typing import Literal
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver

from common_utils.logger import create_logger



@dataclass
class DriverAction:
    action: Literal["url", "get", "sleep", "click", "send_keys", "get_text", "get_texts", "get_class", "get_classes", "get_href", "get_hrefs", "scroll_down", "save_url", "save_all_tabs_urls", "save_last_tab_url", "close_tab"]
    result_key: str | None = None
    value: str | int | float | None = None
    css_identifier: str | None = None
    delim: str | None = None
    delim_idx: int | None = None



class SeleniumHandler:
    log = create_logger("SeleniumHandler")

    def __init__(self,
                 headless: bool = False,
                 undetected: bool = False,
                 verbose: bool = True,
                 raise_exceptions: bool = True,
                 download_driver: bool = False
                 ) -> None:
        self.headless = headless
        self.undetected = undetected
        self.verbose = verbose
        self.raise_exceptions = raise_exceptions
        self.download_driver = download_driver

    def log_msg(self, message: str, level: Literal["debug", "info", "warning", "error"] = "info"):
        if self.verbose is False:
            return
        match level:
            case "debug":
                self.log.debug(message)
            case "info":
                self.log.info(message)
            case "warning":
                self.log.warning(message)
            case "error":
                self.log.error(message)
            case _:
                self.log.info(message)

    def get_driver(self):
        kwargs = {}
        if self.download_driver and not self.undetected:
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            kwargs['service'] = Service(ChromeDriverManager().install())

        if self.headless and self.undetected:
            options = uc.ChromeOptions()
            options.add_argument("--headless")
            kwargs['options'] = options
        elif self.headless:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            kwargs['options'] = options

        if self.undetected:
            import undetected_chromedriver as uc
            return uc.Chrome(**kwargs)
        else:
            return webdriver.Chrome(**kwargs)

    def run_actions(self, actions: list[DriverAction], driver: webdriver.Chrome | None = None) -> dict[str, str | list[str] | None]:
        _driver = driver if driver is not None else self.get_driver()
        results = {}
        for action in actions:
            try:
                result = self.run_action(action, _driver)
                if action.result_key is not None:
                    assert action.result_key not in results, f"Result key already exists: {action.result_key}"
                    results[action.result_key] = result
            except Exception as e:
                self.log_msg(f"Error in action: {action}", level='warning')
                if self.raise_exceptions:
                    raise e
        if driver is None:
            _driver.quit()
        return results

    def run_action(self, action: DriverAction, driver: webdriver.Chrome) -> str | list[str] | None:
        result = None
        match action.action:
            case "url" | "get":
                driver.get(action.value)
                self.log_msg(f"Opened URL: {action.value}", level='debug')
            case "send_keys":
                driver.find_element(By.CSS_SELECTOR, action.css_identifier).send_keys(action.value)
                self.log_msg(f"Sent keys to {action.css_identifier}", level='debug')
            case "click":
                driver.find_element(By.CSS_SELECTOR, action.css_identifier).click()
                self.log_msg(f"Clicked on: {action.css_identifier}", level='debug')
            case "sleep":
                self.log_msg(f"Sleeping for: {action.value} seconds", level='debug')
                sleep(action.value)
            case "get_text":
                result = driver.find_element(By.CSS_SELECTOR, action.css_identifier).text
                self.log_msg(f"Storing text: {result.split('\n')[0]:30}..", level='debug')
            case "get_texts":
                result = [element.text for element in driver.find_elements(By.CSS_SELECTOR, action.css_identifier)]
                self.log_msg(f"Storing {len(result)} texts: {result}", level='debug')
            case "get_class":
                result = driver.find_element(By.CSS_SELECTOR, action.css_identifier).get_attribute("class")
                self.log_msg(f"Storing class: {result}", level='debug')
            case "get_classes":
                result = [element.get_attribute("class") for element in driver.find_elements(By.CSS_SELECTOR, action.css_identifier)]
                self.log_msg(f"Storing {len(result)} classes: {result}", level='debug')
            case "get_href":
                result = driver.find_element(By.CSS_SELECTOR, action.css_identifier).get_attribute(name='href')
                self.log_msg(f"Storing href: {result}", level='debug')
            case "get_hrefs":
                result = [element.get_attribute('href') for element in driver.find_elements(By.CSS_SELECTOR, action.css_identifier)]
                self.log_msg(f"Storing {len(result)} hrefs: {result}", level='debug')
            case "save_url":
                result = driver.current_url
            case "save_all_tabs_urls":
                result = []
                for handle in driver.window_handles:
                    driver.switch_to.window(handle)
                    result.append(driver.current_url)
            case "close_tab":
                if len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                else:
                    self.log_msg(f"Cannot close Tab as it is the only one", level='warning')
            case "scroll_down":
                if action.css_identifier:
                    scroll_element = driver.find_element(By.CSS_SELECTOR, value=action.css_identifier)
                    driver.execute_script(f"arguments[0].scrollBy(0, {action.value});", scroll_element)
                else:
                    driver.execute_script(f"window.scrollBy(0, {action.value})")
            case _:
                self.log_msg(f"Invalid action: {action.action}", level='error')
                if self.raise_exceptions:
                    raise ValueError(f"Invalid action: {action.action}")
        if action.delim:
            result = result.split(sep=action.delim)
            if action.delim_idx is not None and len(result) > action.delim_idx:
                result = result[action.delim_idx]
            elif action.delim_idx is not None:  # not enough results
                self.log_msg(f"Not enough values [{len(result)} for delim index {action.delim_idx}, returning List")
        return result


if __name__ == '__main__':
    ud = SeleniumHandler(undetected=True).get_driver()
    ud.get("https://www.google.com")
    sleep(2)

    ud2 = SeleniumHandler(undetected=True, headless=True).get_driver()
    ud2.get("https://www.google.com")
    google_text = ud2.find_element(By.CSS_SELECTOR, 'body').text
    print(google_text)