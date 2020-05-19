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
        data_list = self.driver.find_elements_by_xpath(
            '//*[@id="lbtable"]/tbody//tr')
        a=[]
        for data in data_list:
            code = data.find_element_by_xpath("./td[1]/a").text
            name = data.find_element_by_xpath("./td[2]/a").text
            people = data.find_element_by_xpath("./td[4]/a[2]").text
            com_name = data.find_element_by_xpath("./td[5]/a").text
            star = data.find_element_by_xpath("./td[6]").text
            than_star = data.find_element_by_xpath("./td[7]").text
            value = data.find_element_by_xpath("./td[8]").text
            str1=f"<p>基金代码: {code}, 基金名称: {name}, 基金经理: {people}, 基金公司: {com_name}, 3年评级: {star}, 较上期: {than_star},单位净值 : {value}</p>"
            a.append(str1)
        self.driver.quit()
        return a

if __name__ == '__main__':
    from public.send_email import SendMail
    work = Work()
    a=work.run()
    str1="".join(a)
    b = SendMail(smtp_server="smtp.qq.com",
                 smtp_port=465,
                 smtp_sender="664616581@qq.com",
                 smtp_senderpassword="xxxxx",
                 smtp_receiver=['664616581@qq.com', '1927265398@qq.com'],
                 smtp_subject="测试邮件！！",
                 smtp_body=str1)
    b.send_mail()
