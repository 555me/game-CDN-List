import os
import requests
import json
from datetime import datetime

URL_CONFIGS = [
]

class CDNFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.current_hour = datetime.now().strftime("%H")

    def default_fetch(self, config):
        method = config.get("method", "GET").upper()
        url = config["url"]
        
        if method == "POST":
            header = config.get('header',{})
            jsonData = config.get('jsonData',None)
            return self.session.post(url, json=jsonData, headers=header,timeout=30)
        return self.session.get(url, timeout=30)

    def run(self):
        os.makedirs("data", exist_ok=True)
        for conf in URL_CONFIGS:
            name, cat = conf["name"], conf["cat"]
            
            handler_name = conf.get("custom_handler", "default_fetch")
            handler = getattr(self, handler_name)
            
            print(f"🚀 Processing: {name} ({cat})")
            try:
                response = handler(conf)
                if response is not None and hasattr(response, 'status_code') and response.status_code == 200:
                    self.save_data(name, cat, url=conf["url"], data=response.json())
                elif response is not None:
                    print(f"❌ Failed: {conf['name']}: HTTP {response.status_code}")
            except Exception as e:
                print(f"⚠️ Error: {e}")
        
        self.write_report()

    def save_data(self, name, cat, url, data):
        dir_path = os.path.join("data", cat)
        os.makedirs(dir_path, exist_ok=True)
        
        data['metadata'] = {
            "name": name,
            "category": cat,
            "source_url": url
        }
        
        file_path = os.path.join(dir_path, f"{name}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def write_report(self):
        global_summary = {}
        data_root = "data"
        if not os.path.exists(data_root):
            return
        for root, dirs, files in os.walk(data_root):
            json_files = [f for f in files if f.endswith('.json')]
            if json_files:
                category = os.path.relpath(root, data_root)
                if category != ".":
                    global_summary[category] = len(json_files)
        summary_path = os.path.join(data_root, "fetch_summary.md")
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("# 数据获取报告\n\n## 获取统计\n\n")
            for cat in sorted(global_summary.keys()):
                count = global_summary[cat]
                f.write(f"- **{cat}**: {count} 个文件\n")

if __name__ == "__main__":
    CDNFetcher().run()