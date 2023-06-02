import os

import pytest

if __name__ == '__main__':
    pytest.main(['-s','day/Test_Web.py','--alluredir','./tmp'])
    os.system('allure generate ./tmp -o ./report --clean')