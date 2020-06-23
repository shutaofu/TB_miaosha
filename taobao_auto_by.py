'''
@time:2020-06-16 16:50
@author: MADAO
程序利用自动测试工具模拟用户下单操作，完成商品的抢购
仅作为学习过程中的实践，无商业用途
'''


from selenium import webdriver
import datetime
import time
from selenium.webdriver import ActionChains


class TaoBaoBuy():

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r'C:\Users\cyl\Anaconda3\chromedriver.exe')
        self.driver.implicitly_wait(10)
        self.driver.maximize_window() # 窗口最大化显示
        self.goods_url = r'https://item.taobao.com/item.htm?spm=a1z0k.6846577.0.0.2e714843qqT0kr&id=563988926234&_u=t2dmg8j26111'  # 商品连接
        self.buy_time = "2020-06-15 18:59:50"  # 请输入开售时间【2020-06-15 18:59:50】
        self.username = 'xxx'
        self.password = 'xxxxxxxxxxxxx'

    #   该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
    def isElementExist(self, element):
        flag = True
        try:
            self.driver.find_element_by_class_name(element)
            return flag
        except:
            flag = False
            return flag

    def login(self):
        '''
        自动登录
        '''
        self.driver.get(self.goods_url)
        print(self.driver.get_cookies())
        if "taobao" in self.goods_url:   # 淘宝的商品
            self.driver.find_element_by_link_text('亲，请登录').click()
            time.sleep(1)
            self.driver.find_element_by_id("fm-login-id").send_keys(self.username)
            self.driver.find_element_by_id("fm-login-password").send_keys(self.password)
        elif "tmall" in self.goods_url:   # 天猫的商品手动扫码登陆
            self.driver.find_element_by_link_text('请登录').click()
            time.sleep(1)
            self.driver.find_element_by_name("fm-login-id").send_keys(self.username)
            self.driver.find_element_by_id("fm-login-password").send_keys(self.password)
        else:
            print('商品不是淘宝系的')

        # 判断是否存在滑动操作
        if self.driver.find_element_by_id('nc_1_n1z').is_displayed():
            bar_element = self.driver.find_element_by_id('nc_1_n1z')
            ActionChains(self.driver).drag_and_drop_by_offset(bar_element, 310, 0).perform()  # 滑块验证
            time.sleep(1.5)
        while True:
            if self.isElementExist("fm-btn"):
                self.driver.find_element_by_class_name("fm-btn").click()
                time.sleep(1)
            else:
                print('登录成功')
                break


    def buy(self):
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
            if now.strftime('%Y-%m-%d %H:%M:%S') >= self.buy_time:
                try:
                    print('开始抢购...')
                    if self.driver.find_element_by_link_text('立即购买'):
                        self.driver.find_element_by_link_text('立即购买').click()
                        print('点击立即购买成功...')
                        break

                    time.sleep(0.01)
                except:
                    time.sleep(0.1)
            i += 1

        while True:
            try:
                if self.driver.find_element_by_link_text('提交订单'):
                    self.driver.find_element_by_link_text('提交订单').click()
                    # 下单成功，跳转至支付页面
                    print("购买成功,请到未支付订单页面支付")
                    break
            except:
                time.sleep(0.3)



    def run(self):
        self.login()
        self.buy()



if __name__ == "__main__":
    tb = TaoBaoBuy()
    tb.run()
