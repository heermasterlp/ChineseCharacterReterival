# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re



class ChineseCharactersDictoryScrapy(object):
    def __init__(self):
        self.browser = webdriver.Firefox(executable_path="/Users/liupeng/Documents/PythonProjects/geckodriver")

    def __del__(self):
        self.browser.close()

    def get_page(self, url):
        self.browser.get(url)
        page_source = self.browser.page_source
        return page_source

    def parse_page(self, page_source):
        html = BeautifulSoup(page_source, "html5lib")

        return html


if __name__ == '__main__':
    character_dict = ChineseCharactersDictoryScrapy()
    basic_url = "http://xh.5156edu.com/html3/"

    with open("Character_bishu.xml", "a", newline="", encoding='utf-8-sig') as f:
        # f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        # f.write('   <RADICALS>\n')

        for index in range(15041, 22526):
            print("Process: ", index)
            url = basic_url + str(index) + ".html"
            page_source = character_dict.get_page(url)
            html = character_dict.parse_page(page_source)

            table3 = html.find("table", id="table3")
            table1s = table3.find_all("table", id="table1")

            if len(table1s) < 2:
                print("table1 not two")
                break
            else:
                table1 = table1s[1]

                trs = table1.find_all("tr")
                char_str = trs[0].find_all("td")[0].text
                # print(trs[0].find_all("td")[0].text)
                bishu_str = ""

                tds = table3.find_all("td")
                for td in tds:
                    if "笔顺编号：" in td.text:
                        contents = td.text.replace("\xa0", "")
                        # print(repr(contents))
                        p = re.compile('笔顺编号：[0-9]+')
                        m = p.findall(contents)
                        if m:
                            bishu_str = m[0].replace("笔顺编号：", "")

                        break

                f_str = '       <RADICAL TAG="' + char_str + '">\n'
                f_str += "          <BISHUN>" + bishu_str + "</BISHUN>\n"
                f_str += "      </RADICAL>\n"

                f.write(f_str)
                f.flush()

            time.sleep(3)

        f.write('   </RADICALS>\n')






