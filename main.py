from selenium import webdriver
from selenium.webdriver.common.by import By
from openai import OpenAI

#这里配置你的登录名和密码
account = '   '             #这是登录名，把引号里面内容的改成你的
password = '   '           #同理这是密码


deepseekapi = '    '        #这里填你的deepseek  api，也可以问别的ai模型可以自行修改


#登录
def login(wd,account,password):
    wd.find_element(By.CSS_SELECTOR, '#btnLogin').click()
    wd.find_element(By.CSS_SELECTOR, '#topLogin_tbLoginName').send_keys(account)
    wd.find_element(By.CSS_SELECTOR, '#topLogin_tbPassword').send_keys(password)
    wd.find_element(By.CSS_SELECTOR, '#ucLogin > div.body-pw > div.btnlogin').click()
#获取题目
def read_subject(wd):
    element = wd.find_element(By.CSS_SELECTOR,'#divSubjectName')
    return element.text
#获取选项
def find_chooses(wd):
    elements = wd.find_elements(By.CSS_SELECTOR,'#divSubjectItem')
    return elements
#将题目和选项拼接
def Splicing_words(wd):
    subject = read_subject(wd)
    all_chooses = ''
    for choose in find_chooses(wd):
        all_chooses += choose.text

    final = subject + all_chooses
    return final
#获取答案  返回的是A,B,C,D
def ask_deepseek(wd):
    client = OpenAI(api_key=deepseekapi, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个选择题助手。我会给你一道选择题，你只需要告诉我应该选哪一个选项（如 A、B、C 或 D），不需要任何解释。"},
            {"role": "user", "content": Splicing_words(wd) },
        ],
        stream=False
    )
    return response.choices[0].message.content.upper()
#点击选项并且点击下一题
def choose_and_next(wd):
    while True:
        answer = ask_deepseek(wd)
        option_map = {'A': '(1)', 'B': '(2)', 'C': '(3)', 'D': '(4)'}
        num = option_map.get(answer)
        element = wd.find_element(By.CSS_SELECTOR,f'#divSubjectItem > div:nth-child{num} > a')
        element.click()
        try:
            next = wd.find_element(By.CSS_SELECTOR, '#next > a')
            next.click()

        except :
            submit = wd.find_element(By.CSS_SELECTOR, '#btnSubmit')
            submit.click()
            break


def main():
    wd = webdriver.Edge()
    wd.get('https://www.duifene.com/')
    login(wd, account, password)
    input('进入要答的题目界面后继续')
    while True:
        choose_and_next(wd)
        b = input('是否继续？（输入1继续否则退出）')
        if b == 1:
            break
    wd.quit()


if __name__ == '__main__':
    main()











