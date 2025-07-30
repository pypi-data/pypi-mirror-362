from kapybara.shortcuts import (
    EC,
    By,
    WebDriverWait,
    TimeoutException,
    InvalidElementStateException,
    StaleElementReferenceException,
)
import logging
import time


class FormElement:
    """封装表单元素操作"""

    def __init__(
        self,
        friendly_name: str = '',
        locator: str = '',
        raise_if_not_found: bool = False,
    ):
        if not locator:
            locator = friendly_name
        self.locator = locator
        self.friendly_name = friendly_name
        self.raise_if_not_found = raise_if_not_found
        self.error = False
        from kapybara.shared_data import shared_data

        driver = shared_data.driver
        self.driver = driver

        self.wait = WebDriverWait(driver, 10)
        self._find_element()

    def _find_element(self):
        """根据 locator 查找元素"""
        try:
            if self.locator.startswith('//'):
                self.element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, self.locator))
                )
            elif self.locator.startswith('.'):
                self.element = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.locator))
                )
            else:
                self.element = self.wait.until(
                    EC.presence_of_element_located((By.ID, self.locator))
                )
            self.tag_name = self.element.get_attribute('tagName').lower()
            self.error = False
        except TimeoutException as e:
            logging.error(f'未找到元素{self.friendly_name}: {self.locator}')
            if self.raise_if_not_found:
                raise e
            self.error = True
            self.element = None
            self.tag_name = None

    def _execute_action(self, action, *args, **kwargs):
        """
        执行操作并处理 StaleElementReferenceException
        :param action: 一个接受 self.element 作为第一个参数的函数
        :param args: action 的位置参数
        :param kwargs: action 的关键字参数
        :return: action 的返回值
        """
        if self.error:
            return None
        try:
            return action(self.element, *args, **kwargs)
        except StaleElementReferenceException:
            logging.warning(f'元素 {self.friendly_name} 陈旧，正在尝试重新查找...')
            self._find_element()
            if self.error:
                return None
            return action(self.element, *args, **kwargs)
        except Exception as e:
            logging.error(f'执行 {self.friendly_name} 操作时出错: {e}')
            return None

    def set_value(self, value):
        def action(element, val):
            if self.tag_name == 'select':
                from selenium.webdriver.support.ui import Select

                select = Select(element)
                select.select_by_visible_text(str(val))
                return
            try:
                element.clear()
                element.send_keys(str(val))
            except InvalidElementStateException:
                pass

        return self._execute_action(action, value)

    def clear(self):
        def action(element):
            if self.tag_name == 'input':
                element.clear()

        return self._execute_action(action)

    def click(self):
        def action(element):
            # 等待元素可点击
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(element))
            self.driver.execute_script('arguments[0].scrollIntoView();', element)
            from selenium.common.exceptions import ElementClickInterceptedException

            time.sleep(0.5)  # 等待滚动
            try:
                element.click()
            except ElementClickInterceptedException:
                self.driver.execute_script('arguments[0].click();', element)

        return self._execute_action(action)

    def get_element(self):
        if self.error:
            return None
        return self.element

    @property
    def value(self):
        return self._execute_action(lambda el: el.get_attribute('value'))

    @property
    def text(self):
        return self._execute_action(lambda el: el.text)

    def is_selected(self):
        return self._execute_action(lambda el: el.is_selected())

    def wait_until_disappeared(self):
        if self.error:
            return
        WebDriverWait(self.driver, 300).until(
            EC.invisibility_of_element_located(self.element)
        )


def get_value(element_id: str) -> str:
    """获取表单元素的值"""
    return FormElement(element_id).value
