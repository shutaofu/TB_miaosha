'''
@time:2020-06-16 16:50
@author: MADAO
程序利用自动测试工具模拟用户下单操作，完成商品的抢购
仅作为学习过程中的实践，无商业用途
'''
import threading
from queue import Queue

from selenium import webdriver
import datetime
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TaoBaoBuy():

    def __init__(self):
        self.username = 'xxx'   # 淘宝账号
        self.password = 'xxxxxxxxxx'   # 密码
        self.url_queue = Queue()

    def get_url_list(self):
        """
        获取商品url列表
        :return:
        """
        url_list = [
            {"url": "https://item.taobao.com/item.htm?spm=a1z0k.6846577.0.0.2e714843qqT0kr&id=563988926234&_u=t2dmg8j26111", "buy_time": "2020-06-16 15:00:00"},
            {"url": "https://item.taobao.com/item.htm?spm=a1z0k.6846577.0.0.2e714843qqT0kr&id=617201942509&_u=t2dmg8j26111", "buy_time": "2020-06-16 15:00:00"}
        ]
        for i in url_list:
            self.url_queue.put(i)

        return url_list


    def parse_url(self):
        url_data = self.url_queue.get()
        print(url_data)
        driver = webdriver.Chrome(executable_path=r'C:\Users\cyl\Anaconda3\chromedriver.exe')
        driver.implicitly_wait(10)
        driver.maximize_window()  # 窗口最大化显示
        self.login(url_data, driver)
        self.buy(url_data, driver)
        self.url_queue.task_done()


    #   该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
    def isElementExist(self, element, driver):
        flag = True
        try:
            driver.find_element_by_class_name(element)
            return flag
        except:
            flag = False
            return flag

    def login(self, url_data, driver):
        '''
        url:商品的链接
        '''
        goods_url = url_data.get('url')

        driver.get(goods_url)
        print(driver.get_cookies())
        if "taobao" in goods_url:   # 淘宝的商品
            element = WebDriverWait(driver, 0.5).until(
                EC.presence_of_element_located((By.LINK_TEXT, "亲，请登录"))
            )
            element.click()
            time.sleep(1)
            driver.find_element_by_id("fm-login-id").send_keys(self.username)
            driver.find_element_by_id("fm-login-password").send_keys(self.password)
        elif "tmall" in goods_url:   # 天猫的商品手动扫码登陆
            # self.driver.find_element_by_link_text('请登录').click()
            element = WebDriverWait(driver, 0.5).until(
                EC.presence_of_element_located((By.LINK_TEXT, "请登录"))
            )
            element.click()
            time.sleep(1)
            driver.find_element_by_name("fm-login-id").send_keys(self.username)
            driver.find_element_by_id("fm-login-password").send_keys(self.password)
        else:
            print('商品不是淘宝系的')
            return

        # 判断是否存在滑动操作
        if driver.find_element_by_id('nc_1_n1z').is_displayed():
            bar_element = driver.find_element_by_id('nc_1_n1z')
            ActionChains(driver).drag_and_drop_by_offset(bar_element, 310, 0).perform()  # 滑块验证
            time.sleep(1.5)
        while True:
            if self.isElementExist("fm-btn", driver):
                driver.find_element_by_class_name("fm-btn").click()
                time.sleep(1)
            else:
                print('登录成功')
                break


    def buy(self, url_data, driver):
        '''
        购买函数
        '''
        print('请在页面提前选择好商品类型...')
        time.sleep(3)
        i = 1
        while True:
            # 现在时间大于预设时间则开售抢购
            # self.driver.refresh()
            now = datetime.datetime.now()
            if now.strftime('%Y-%m-%d %H:%M:%S') >= url_data.get('buy_time'):
                try:
                    print('开始抢购...')
                    if driver.find_element_by_link_text('立即购买'):
                        driver.find_element_by_link_text('立即购买').click()
                        print('点击立即购买成功...')
                        break

                    time.sleep(0.01)
                except:
                    time.sleep(0.1)
            i += 1

        while True:
            try:
                if driver.find_element_by_link_text('提交订单'):
                    driver.find_element_by_link_text('提交订单').click()
                    # 下单成功，跳转至支付页面
                    print("购买成功,请到未支付订单页面支付")
                    break
            except:
                time.sleep(0.3)



    def run(self):
        thread_list = []
        # 遍历登录购买
        for j in range(len(self.get_url_list())):
            t_parse = threading.Thread(target=self.parse_url)
            thread_list.append(t_parse)



        for t in thread_list:
            t.setDaemon(True)  # 把子线程设置为守护线程，当前这个线程不重要，主线程结束，子线程结束
            t.start()

        for q in [self.url_queue]:
            q.join()  # 让主线程阻塞，等待队列的计数为0，

        print('主线程结束')



if __name__ == "__main__":
    tb = TaoBaoBuy()
    tb.run()
