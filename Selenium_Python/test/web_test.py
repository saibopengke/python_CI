import time
import unittest
import allure
import configparser
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


@allure.feature("测试百度WebUI")
class ISelenium(unittest.TestCase):

    def get_config(self):
        """
        读取配置文件 cd ～ ===> pwd
        :return:
        """
        config = configparser.ConfigParser()
        config.read(os.path.join(os.environ['HOME'], 'configs/selenium.ini'))
        return config

    def setUp(self) -> None:
        config = self.get_config()
        try:
            using_headless = os.environ['using_headless']
        except KeyError:
            using_headless = None
            print('没有配置环境变量 using_headless, 按照有界面方式运行自动化测试')

        chrome_options = Options()
        if using_headless is not None and using_headless.lower() == 'true':
            print("无界面方式运行")
            chrome_options.add_argument("--headless")
        # 参考selenium.ini模版
        self.driver = webdriver.Chrome(executable_path=config.get('driver', "chrome_driver"),
                                       options=chrome_options)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.quit()

    @allure.story("keyword 汽车之家")
    def test_web_1(self):
        self._test_baidu('汽车之家', 'test_web_1')

    @allure.story("keyword dota2")
    def test_web_2(self):
        self._test_baidu('dota2', 'test_web_2')

    def _test_baidu(self, keyword, testcase_name):
        self.driver.get("https://www.baidu.com")
        print("----打开百度浏览器----")
        assert f"百度一下" in self.driver.title

        ele = self.driver.find_element_by_name("wd")
        ele.send_keys(f"{keyword}{Keys.RETURN}")
        print(f"搜索关键词{keyword}")
        time.sleep(5)
        self.assertTrue(f'{keyword}' in self.driver.title, msg=f'{testcase_name}校验点 pass')
