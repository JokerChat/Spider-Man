from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Work(object):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=chrome_options)

    def run(self):
        """ url 的规则 http://fund.eastmoney.com/data/fundrating_4_2019-09-30.html """
        self.driver.get("http://fund.eastmoney.com/data/fundrating_4.html")
        data_list = self.driver.find_elements_by_xpath('//*[@id="lbtable"]/tbody//tr')
        for data in data_list:
            code = data.find_element_by_xpath("./td[1]/a").text
            name = data.find_element_by_xpath("./td[2]/a").text
            people = data.find_element_by_xpath("./td[4]/a[2]").text
            com_name = data.find_element_by_xpath("./td[5]/a").text
            star = data.find_element_by_xpath("./td[6]").text
            than_star = data.find_element_by_xpath("./td[7]").text
            print(f"code: {code}, name: {name}, people: {people}, com_name: {com_name}, star: {star}, than_star: {than_star}")
        self.driver.quit()


if __name__ == '__main__':
    work = Work()
    work.run()
