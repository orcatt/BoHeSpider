# 🔥 薄荷平台爬虫🕷️BoHeSpider🔥 


> **免责声明：**
> 
> 大家请以学习为目的使用本仓库⚠️⚠️⚠️⚠️，[爬虫违法违规的案件](https://github.com/HiddenStrawberry/Crawler_Illegal_Cases_In_China)  <br>
>
>本仓库的所有内容仅供学习和参考之用，禁止用于商业用途。任何人或组织不得将本仓库的内容用于非法用途或侵犯他人合法权益。本仓库所涉及的爬虫技术仅用于学习和研究，不得用于对其他平台进行大规模爬虫或其他非法行为。对于因使用本仓库内容而引起的任何法律责任，本仓库不承担任何责任。使用本仓库的内容即表示您同意本免责声明的所有条款和条件。
>
> 点击查看更为详细的免责声明。[点击跳转](#disclaimer)

# 仓库描述

**薄荷平台爬虫**
目前能抓取薄荷平台的食物数据。

原理：利用selenium模拟浏览器操作，抓取食物数据、营养信息、度量单位、缩略图等，并写入数据库。


# 安装部署方法
> 开源不易，希望大家可以Star一下BoHeSpider仓库！！！！十分感谢！！！ <br>

## 创建并激活 python 虚拟环境
> 如果是爬取抖音和知乎，需要提前安装nodejs环境，版本大于等于：`16`即可 <br>
   ```shell   
  # 创建新的虚拟环境
  python3 -m venv pachong

  # 激活新环境
  source pachong/bin/activate    # Mac/Linux
  # 或
  pachong\Scripts\activate    # Windows
  ```

## 安装依赖库
  ```shell
  pip install mysql-connector-python
  pip install selenium
  pip install requests
  ```

## 安装浏览器驱动 chromedriver
## 运行爬虫程序

## 数据保存
- 支持关系型数据库Mysql中保存（需要提前创建配置数据库）
    - 数据库sql 参考：
    ```shell  
      -- 1. foods_info 表（存储食物的基本信息）
        CREATE TABLE foods_info (
            id INT AUTO_INCREMENT PRIMARY KEY,           -- 主键
            name VARCHAR(255) NOT NULL,                  -- 食物名称
            category VARCHAR(255) NOT NULL,              -- 分类
            calories_per_100g DECIMAL(10, 2) NOT NULL    -- 每100克热量
            image_path VARCHAR(255) DEFAULT NULL;        -- 图片路径
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

      -- 2. food_aliases 表（存储别名）
        CREATE TABLE food_aliases (
            id INT AUTO_INCREMENT PRIMARY KEY,           -- 主键
            food_id INT NOT NULL,                        -- 外键，关联 foods_info 表
            alias_name VARCHAR(255) NOT NULL,            -- 别名
            CONSTRAINT fk_food_aliases_food_id FOREIGN KEY (food_id)
                REFERENCES foods_info(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

      -- 3. food_nutrition 表（存储营养信息）
        CREATE TABLE food_nutrition (
            id INT AUTO_INCREMENT PRIMARY KEY,           -- 主键
            food_id INT NOT NULL,                        -- 外键，关联 foods_info 表
            nutrient_name VARCHAR(255) NOT NULL,         -- 营养素名称
            amount_per_100g DECIMAL(10, 2) NOT NULL,     -- 每100克的含量
            CONSTRAINT fk_food_nutrition_food_id FOREIGN KEY (food_id)
                REFERENCES foods_info(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

      -- 4. food_measurement 表（存储度量单位）
        CREATE TABLE food_measurement (
            id INT AUTO_INCREMENT PRIMARY KEY,           -- 主键
            food_id INT NOT NULL,                        -- 外键，关联 foods_info 表
            unit_name VARCHAR(255) NOT NULL,             -- 度量单位名称
            weight DECIMAL(10, 2) NOT NULL,              -- 单位对应的重量（克）
            calories DECIMAL(10, 2) NOT NULL,            -- 热量
            CONSTRAINT fk_food_measurement_food_id FOREIGN KEY (food_id)
                REFERENCES foods_info(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

     ```



# 免责声明
<div id="disclaimer"> 

## 1. 项目目的与性质
本项目（以下简称“本项目”）是作为一个技术研究与学习工具而创建的，旨在探索和学习网络数据采集技术。本项目专注于数据爬取技术研究，旨在提供给学习者和研究者作为技术交流之用。

## 2. 法律合规性声明
本项目开发者（以下简称“开发者”）郑重提醒用户在下载、安装和使用本项目时，严格遵守中华人民共和国相关法律法规，包括但不限于《中华人民共和国网络安全法》、《中华人民共和国反间谍法》等所有适用的国家法律和政策。用户应自行承担一切因使用本项目而可能引起的法律责任。

## 3. 使用目的限制
本项目严禁用于任何非法目的或非学习、非研究的商业行为。本项目不得用于任何形式的非法侵入他人计算机系统，不得用于任何侵犯他人知识产权或其他合法权益的行为。用户应保证其使用本项目的目的纯属个人学习和技术研究，不得用于任何形式的非法活动。

## 4. 免责声明
开发者已尽最大努力确保本项目的正当性及安全性，但不对用户使用本项目可能引起的任何形式的直接或间接损失承担责任。包括但不限于由于使用本项目而导致的任何数据丢失、设备损坏、法律诉讼等。

## 5. 知识产权声明
本项目的知识产权归开发者所有。本项目受到著作权法和国际著作权条约以及其他知识产权法律和条约的保护。用户在遵守本声明及相关法律法规的前提下，可以下载和使用本项目。

## 6. 最终解释权
关于本项目的最终解释权归开发者所有。开发者保留随时更改或更新本免责声明的权利，恕不另行通知。
</div>


## 感谢JetBrains提供的免费开源许可证支持
<a href="https://www.jetbrains.com/?from=MediaCrawler">
    <img src="https://www.jetbrains.com/company/brand/img/jetbrains_logo.png" width="100" alt="JetBrains" />
</a>
