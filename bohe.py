import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests

# 设置 Chrome 驱动路径
driver_path = "./chromedriver-mac-x64/chromedriver"  # 修改为相对路径
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# 数据库连接配置
db_config = {
    'host': 'xxx.xxx.xxx.xxx',
    'user': "xxx",
    'password': "xxx",
    'database': "xxx",
    'port': 3306  # 添加端口号配置
}

# 连接数据库
def connect_to_database():
    try:
        connection = mysql.connector.connect(**db_config)
        print("数据库连接成功！")
        return connection
    except mysql.connector.Error as err:
        print(f"数据库连接失败: {err}")
        return None

connection = connect_to_database()

def clean_amount(value):
    if isinstance(value, str):
        value = value.strip()
    if value in ['-', '']:
        return None
    if value == '0':
        return 0
    try:
        return float(value)
    except ValueError:
        return None
    

def download_image(image_url):
    # 获取文件名（从 URL 中提取）
    image_name = image_url.split("/")[-1]
    local_image_path = f"./images/{image_name}"

    if not os.path.exists("./images"):
        os.makedirs("./images")

    # 下载图片
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(local_image_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"成功下载图片: {local_image_path}")
            return local_image_path
        else:
            print(f"图片下载失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"下载图片出错: {e}")
        return None

def insert_food_info(name, calories, category, image_path):
    if connection:
        try:
            cursor = connection.cursor()
            sql = """
            INSERT INTO foods_info (name, calories_per_100g, category, image_path)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (name, calories, category, image_path))
            connection.commit()
            print(f"成功插入食物信息: {name}, {calories}, {category}, {image_path}")
            return cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"插入数据失败: {err}")
            return None

def insert_food_aliases(food_id, aliases):
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO food_aliases (food_id, alias_name) VALUES (%s, %s)"
            for alias in aliases:
                cursor.execute(sql, (food_id, alias))
            connection.commit()
            print(f"成功插入别名: {aliases}")
        except mysql.connector.Error as err:
            print(f"插入别名失败: {err}")

def insert_food_nutrition(food_id, nutrition):
    if connection:
        try:
            cursor = connection.cursor()
            sql = """
            INSERT INTO food_nutrition (food_id, nutrient_name, amount_per_100g)
            VALUES (%s, %s, %s)
            """
            for nutrient_name, amount in nutrition:
                cleaned_amount = clean_amount(amount)
                cursor.execute(sql, (food_id, nutrient_name, cleaned_amount))
            connection.commit()
            print(f"成功插入营养信息: {nutrition}")
        except mysql.connector.Error as err:
            print(f"插入营养信息失败: {err}")

def insert_food_measurement(food_id, measurements):
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO food_measurement (food_id, unit_name, calories) VALUES (%s, %s, %s)"
            for unit_name, calories in measurements:
                calories_number = re.sub(r"[^\d.]", "", calories)
                calories_value = float(calories_number) if calories_number else None
                cursor.execute(sql, (food_id, unit_name, calories_value))
            connection.commit()
            print(f"成功插入度量单位: {measurements}")
        except mysql.connector.Error as err:
            print(f"插入度量单位失败: {err}")

def open_page(group, page):
    url = f"https://www.boohee.com/food/group/{group}?page={page}"
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#main .widget-food-list .food-list"))
    )

def click_and_process_items():
    items = driver.find_elements(By.CSS_SELECTOR, "#main .widget-food-list .food-list .item .text-box h4 a")
    for item in items:
        item.click()
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[1])

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h2.crumb"))
        )

        try:
            crumb = driver.find_element(By.CSS_SELECTOR, "h2.crumb")
            food_name = crumb.text.split('/')[-1].strip()
            
            # 提取图片 URL
            img_element = driver.find_element(By.CSS_SELECTOR, ".food-pic a img")
            image_url = img_element.get_attribute("src")

            # 下载图片并获取本地路径
            local_image_path = download_image(image_url)

            # 拼接存储在数据库中的图片路径
            if local_image_path:
                image_path_in_db = f"static/images/{os.path.basename(local_image_path)}"

            calorie_element = driver.find_element(By.CSS_SELECTOR, "#food-calory .stress.red1")
            calories = calorie_element.text.strip()

            category_element = driver.find_element(By.CSS_SELECTOR, ".basic-infor li strong a")
            category = category_element.text.strip()
            food_id = insert_food_info(food_name, calories, category, image_path_in_db)
            
            # 获取别名：首先找到li:nth-child(1)，检查是否有id="food-calory"
            aliases = []
            try:
                alias_li_element = driver.find_element(By.CSS_SELECTOR, ".basic-infor li:nth-child(1)")
                # 检查li:nth-child(1)下是否包含id="food-calory"的元素
                if not alias_li_element.find_elements(By.ID, "food-calory"):
                    # 如果没有food-calory元素，说明这是别名字段
                    alias_text = alias_li_element.text.replace("别名：", "").strip()
                    if alias_text:
                        aliases = alias_text.split("、")
            except Exception as e:
                print(f"提取别名失败: {e}")


            # 只有在别名存在时才插入
            if aliases:
                insert_food_aliases(food_id, aliases)
            else:
                print(f"别名: 无")

            # 清理无效的营养信息
            nutrition_elements = driver.find_elements(By.CSS_SELECTOR, ".nutr-tag .content dl:not(.header)")
            nutrition = []
            for dl in nutrition_elements:
                dd_elements = dl.find_elements(By.CSS_SELECTOR, "dd")  # 查找所有 dd 元素
                for dd in dd_elements:
                    try:
                        dt = dd.find_element(By.CSS_SELECTOR, ".dt").text.strip()
                        dd_value_element = dd.find_element(By.CSS_SELECTOR, ".dd")
                        amount = "".join([span.text for span in dd_value_element.find_elements(By.CSS_SELECTOR, "span")]) or dd_value_element.text.strip()
                        
                        # 清理无效的营养信息
                        if amount and amount not in ['-', ''] and dt:  # 确保数值和营养素名称都不为空
                            cleaned_amount = clean_amount(amount)  # 使用已有的 clean_amount 函数清理数值
                            if cleaned_amount is not None:  # 只添加有效的数值
                                nutrition.append((dt, amount))
                            
                    except Exception as e:
                        print(f"提取营养信息失败: {e}")

            if food_id and nutrition:  # 只在有食物ID和有效营养信息时才插入
                insert_food_nutrition(food_id, nutrition)

            try:
                widget_unit = driver.find_element(By.CSS_SELECTOR, ".widget-unit .content tbody")
                rows = widget_unit.find_elements(By.CSS_SELECTOR, "tr")
                measurements = []
                for row in rows:
                    unit_name_td = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)")
                    calories_td = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)")
                    unit_name = unit_name_td.text.strip()
                    calories = calories_td.text.strip()
                    measurements.append((unit_name, calories))

                if food_id and measurements:
                    insert_food_measurement(food_id, measurements)

            except Exception as e:
                print(f"没有找到 widget-unit 标签或提取度量单位失败: {e}")

        except Exception as e:
            print(f"提取食物信息失败: {e}")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

def process_group(group):
    for page in range(8, 11):
        open_page(group, page)
        click_and_process_items()

def main():
    for group in range(9, 11):
        process_group(group)

    driver.quit()

if __name__ == "__main__":
    main()
    if connection:
        connection.close()
