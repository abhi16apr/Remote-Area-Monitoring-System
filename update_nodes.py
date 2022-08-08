import requests
from source.util.settings import Settings
from source.util.timekeeper import Timestamps
from urllib.request import Request, urlopen
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UpdateNodes:
    def __init__(self):
        self.ts = Timestamps()
        self.config = Settings('general.config')
        self.url = 'http://' + self.config.get_setting('website', 'ip_address') + ':' + \
                   self.config.get_setting('website', 'port') + '/update'
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        print(self.url)
        chromedriver_autoinstaller.install()
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

    def update(self):
        count = 1
        start = 0
        interval = self.config.get_int_setting('mesh_network', 'query_interval')
        while True:
            if self.ts.get_timestamp() - start > interval:
                print('Mesh Network Query:', count)
                start = self.ts.get_timestamp()
                self.driver.get(self.url)
                try:
                    element = WebDriverWait(self.driver, interval).until(
                        EC.presence_of_element_located((By.ID, 'update-complete'))
                    )
                except Exception as e:
                    print(e)
                    continue
                # finally:
                #     self.driver.quit()
                # webbrowser.open_new(self.url)
                # req = Request(self.url)
                # webpage = urlopen(req).read()
                # print(webpage)
                # print(requests.get(self.url))
                # print(requests.get('http://' + self.config.get_setting('website', 'ip_address') + ':' +
                #                    self.config.get_setting('website', 'port') + '/_dash-layout'))
                # print(requests.get('http://' + self.config.get_setting('website', 'ip_address') + ':' +
                #                    self.config.get_setting('website', 'port') + '/_dash-dependencies'))
                count += 1


def main():
    updater = UpdateNodes()
    updater.update()


if __name__ == '__main__':
    main()

