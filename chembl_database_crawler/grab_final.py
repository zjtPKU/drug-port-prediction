import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_chembl_targets(chEMBL_id, results_dir='results'):
    # 初始化 WebDriver
    driver_path = '/Users/zhoujt/Desktop/training-data_v3/chromedriver-mac-arm64/chromedriver'
    driver = webdriver.Chrome(executable_path=driver_path)
    
    try:
        # 构造目标 URL
        driver.get(f"https://www.ebi.ac.uk/chembl/web_components/embed/report_cards/compound/sections/activity_charts/{chEMBL_id}/")
        
        # 创建文件夹用于保存结果
        os.makedirs(results_dir, exist_ok=True)
        
        # 保存初始页面内容
        # with open(f'{results_dir}/{chEMBL_id}_chart.html', 'w') as f:
        #     f.write(driver.page_source)

        # 查找包含 "targets" 的链接
        link_elements = driver.find_elements(By.CSS_SELECTOR, "div.v-card__text a")
        for index, link_element in enumerate(link_elements):
            link_href = link_element.get_attribute('href')
            if "targets" in link_href:
                print(f"Opening Link {index + 1}: {link_href}")
                driver.get(link_href)

                # 保存页面内容
                with open(f'{results_dir}/{chEMBL_id}_target_summary_{index + 1}.html', 'w') as f:
                    f.write(driver.page_source)

                # 提取第一页的目标信息
                extract_targets(driver, chEMBL_id, results_dir, index)

                # 翻页并提取目标信息
                for i in range(2, 100):
                    try:
                        button = driver.find_element(By.CSS_SELECTOR, f'button[aria-label="Goto Page {i}"]')
                        button.click()
                        time.sleep(5)  # 等待页面加载
                        print(f"Clicked Page {i}")
                        with open(f'{results_dir}/{chEMBL_id}_target_summary_{index + 1}_page{i}.html', 'w') as f:
                            f.write(driver.page_source)

                        extract_targets(driver, chEMBL_id, results_dir, index, page=i)
                    except Exception as e:
                        print("Error clicking button:", e)
                        break  # 如果无法点击下一页，停止翻页
    finally:
        driver.quit()

def extract_targets(driver, chEMBL_id, results_dir, index, page=1):
    elements = driver.find_elements(By.XPATH, "//td[@class='text-start']//a")
    for element in elements:
        text = element.text
        with open(f"{results_dir}/{chEMBL_id}_targets.txt", 'a') as f:
            f.write(f"Page {page}: {text}\n")

def main(csv_file):
    # 读取 CSV 文件
    df = pd.read_csv(csv_file,header=None,index_col=None)
    df.columns = ['ID','CHEMBL_ID']
    
    print(df)   
    # 确保结果文件夹存在
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)

    # 遍历每个 CHEMBL_id 并爬取数据
    for chEMBL_id in df['CHEMBL_ID']:
        print(f"Processing {chEMBL_id}...")
        scrape_chembl_targets(chEMBL_id, results_dir=results_dir)

if __name__ == "__main__":
    csv_file = '/Users/zhoujt/Desktop/training-data_v3/chembl_results.csv'  # 你的 CSV 文件路径
    print(csv_file)
    main(csv_file)
