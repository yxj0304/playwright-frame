# 通过yaml方式运行用例
import allure
import pytest
import yaml
from playwright.sync_api import sync_playwright

f = open("day/loginCases.yaml", mode="r", encoding="utf-8")

case_dict = yaml.safe_load(f)

@allure.feature('登录中*软*')
class Test_Web:
    @classmethod
    def setup_class(self):
        self.playwright = sync_playwright().start()
        for browser_type in [self.playwright.chromium]:
            self.browser = browser_type.launch(channel="msedge", headless=False, args=['--start-maximized'],
                                               downloads_path="C:\\tmp")
            self.context = self.browser.new_context(no_viewport=True)
            self.page = self.context.new_page()

    def run_step(self, func, value):
        func(*value)

    def run_case(self, POCases):
        allure.dynamic.title(POCases['title'])
        allure.dynamic.description(POCases['des'])
        cases = POCases['cases']
        try:
            for case in cases:
                func = self.page.__getattribute__(case['method'])
                valuelist = list(case.values())
                with allure.step(case['name']):
                  self.run_step(func, valuelist[2:])
        except Exception:
            allure.attach(self.page.screenshot(),'用例报错图',allure.attachment_type.PNG)
            pytest.fail("测试用例执行失败")
        allure.attach(self.page.screenshot(), '用例执行图', allure.attachment_type.PNG)

    @pytest.mark.parametrize('POCases', case_dict['loginPage'])
    @allure.story('登录')
    def test_login(self, POCases):
        self.run_case(POCases)
        self.page.wait_for_timeout(3000)

    @classmethod
    def teardown_class(self):
        self.browser.close()
        self.playwright.stop()
