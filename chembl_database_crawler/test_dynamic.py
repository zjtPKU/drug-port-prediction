from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver_path = '/Users/zhoujt/Desktop/training-data_v3/chromedriver-mac-arm64/chromedriver'
driver = webdriver.Chrome(executable_path=driver_path)  # 或使用 Firefox、Edge 等

# driver.get("https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL545/")
chEMBL_id = "CHEMBL545"
driver.get(f"https://www.ebi.ac.uk/chembl/web_components/embed/report_cards/compound/sections/activity_charts/{chEMBL_id}/")
with open('chart.html', 'w') as f:
    f.write(driver.page_source)



link_elements = driver.find_elements(By.CSS_SELECTOR, "div.v-card__text a")

for index, link_element in enumerate(link_elements):
    link_href = link_element.get_attribute('href')
    
    # 检查 href 中是否包含 "targets"
    if "targets" in link_href:
        print(f"Opening Link {index + 1}: {link_href}")
        
        # 打开包含 "targets" 的链接
        driver.get(link_href)

        # 可选：你可以在这里保存页面内容或进一步操作
        with open(f'target_summary_{index + 1}.html', 'w') as f:
            f.write(driver.page_source)
        # driver.back()
        # 先搞第一页
        elements = driver.find_elements(By.XPATH, "//td[@class='text-start']//a")
        for element in elements:
            
            print(element)  # 输出: P22771, P24524, P07727, P20781
            text = element.text
            with open(f"{chEMBL_id}_targets.txt", 'a') as f:
                f.write(f"{text}\n")
        for i in range(2,100):
            button = driver.find_element(By.CSS_SELECTOR, f'button[aria-label="Goto Page {i}"]')
            print(button)
            try:
        # 点击按钮
                button.click()
                driver.implicitly_wait(10)
                time.sleep(10)
                print("Clicked")
                page_source = driver.page_source
                with open(f'target_summary_{index + 1}_page{i}.html', 'w') as f:
                    f.write(page_source)
                elements = driver.find_elements(By.XPATH, "//td[@class='text-start']//a")
                for element in elements:
                    
                    print(element)  # 输出: P22771, P24524, P07727, P20781
                    text = element.text
                    with open(f"{chEMBL_id}_targets.txt", 'a') as f:
                        f.write(f"{text}\n")
            except Exception as e:
                print("Error clicking button:", e) 
                pass
        
        # button = driver.find_elements(By.XPATH, '//*[@id="app"]/div/main/div/div[1]/div[2]/div/div/div/div/div[4]/div[2]/div[1]/div/div[2]/div/div/div/div[3]/div[2]/div/nav/ul/li[3]/button')
    # 提取文本内容
        

driver.quit()


# https://www.ebi.ac.uk/chembl/web_components/explore/targets/STATE_ID:YM4bXW8JPvo7KTPNovtQ_g%3D%3D
# https://www.ebi.ac.uk/chembl/web_components/explore/targets/STATE_ID:YM4bXW8JPvo7KTPNovtQ_g%3D%3D