import json
import os
from jinja2 import Environment, FileSystemLoader

# 設定
DATA_FILE = 'data.json'
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = '.'  # 生成到根目錄，方便 GitHub Pages 部署

def load_data(filepath):
    """讀取 JSON 資料"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_site():
    """主建置函式"""
    # 1. 準備資料
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found!")
        return
    
    data = load_data(DATA_FILE)
    
    # 2. 設定 Jinja2 環境
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    
    # 3. 定義要生成的頁面 (模板檔名 -> 輸出檔名)
    pages = {
        'index_template.html': 'index.html',
        'zh_template.html': 'zh.html'
    }
    
    # 4. 渲染並寫入檔案
    for template_name, output_name in pages.items():
        try:
            template = env.get_template(template_name)
            # 將 data 變數傳入模板，這樣在模板中就可以使用 {{ data.common.name }}
            rendered_html = template.render(data=data)
            
            output_path = os.path.join(OUTPUT_DIR, output_name)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
            
            print(f"Successfully generated: {output_path}")
            
        except Exception as e:
            print(f"Error generating {output_name}: {e}")

if __name__ == "__main__":
    build_site()