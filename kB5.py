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
        payload = config.get("payload", None)
        
        if method == "POST":
            return self.session.post(url, json=payload, timeout=30)
        return self.session.get(url, timeout=30)

    def run(self):
        summary = {}
        for conf in URL_CONFIGS:
            name, cat = conf["name"], conf["cat"]
            
            handler_name = conf.get("custom_handler", "default_fetch")
            handler = getattr(self, handler_name)
            
            print(f"🚀 Processing: {name} ({cat})")
            try:
                response = handler(conf)
                if response.status_code == 200:
                    self.save_data(name, cat, url=conf["url"], data=response.json())
                    summary[cat] = summary.get(cat, 0) + 1
                else:
                    print(f"❌ Failed: HTTP {response.status_code}")
            except Exception as e:
                print(f"⚠️ Error: {e}")
        
        self.write_report(summary)

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

    def write_report(self, summary):
        with open("data/fetch_summary.md", "w", encoding="utf-8") as f:
            f.write("# 数据获取报告\n\n## 获取统计\n\n")
            for cat, count in summary.items():
                f.write(f"- **{cat}**: {count} 个文件\n")

if __name__ == "__main__":
    CDNFetcher().run()