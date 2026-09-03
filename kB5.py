import os
import requests
import json
from datetime import datetime, timezone, timedelta

URL_CONFIGS = [
          {"name": "BetaVersionList","cat": "dna/game","custom_handler": "old01","template": "https://pan01-1-eo.shyxhy.com/Patches/FinalPatch/CN/Default/WindowsNoEditor/PC_OBT{obt}_Media_CN_Pub/VersionList.json","obt_range": (18, 11)},
          {"name": "BetaBaseVersion","cat": "dna/game","custom_handler": "old01","template": "https://pan01-1-eo.shyxhy.com/Packages/CN/WindowsNoEditor/PC_OBT{obt}_Media_CN_Pub/{v}/BaseVersion.json","obt_range": (18, 11),"v_range": (3, 1)},
          {"name":"PreDownloadVersion","cat":"dna/game","url":"https://pan01-1-eo.shyxhy.com/Packages/CN/WindowsNoEditor/PC_OBT_CN_Pub/PreDownloadVersion.json"},
]

class CDNFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.current_hour = datetime.now().strftime("%H")
        self.fetched_urls = {}
        self.fetched_data = {}

    def old01(self, config):
        obt_start, obt_end = config.get("obt_range", (18, 11))
        v_start, v_end = config.get("v_range", (3, 1))
        template = config["template"]
        
        has_v = "{v}" in template

        for obt in range(obt_start, obt_end - 1, -1):
            if has_v:
                for v in range(v_start, v_end - 1, -1):
                    target_url = template.format(obt=obt, v=v)
                    res = self.old02(target_url, config)
                    if res: return res
            else:
                target_url = template.format(obt=obt)
                res = self.old02(target_url, config)
                if res: return res
                
        return None

    def old02(self, url, config):
        try:
            time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
            res = self.session.get(url, timeout=10)
            if res.status_code == 200:
                config["url"] = url
                print(f"[{time}]✅ Success: {url}")
                return res
        except Exception:
            pass
        return None
    
    def default_fetch(self, config):
        method = config.get("method", "GET").upper()
        url = config["url"]
        
        if method == "POST":
            header = config.get('header',{})
            jsonData = config.get('jsonData',None)
            return self.session.post(url, json=jsonData, headers=header,timeout=10)
        return self.session.get(url, timeout=10)

    def run(self):
        os.makedirs("data", exist_ok=True)
        for conf in URL_CONFIGS:
            time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
            name, cat = conf["name"], conf["cat"]
            
            handler_name = conf.get("custom_handler", "default_fetch")
            handler = getattr(self, handler_name)
            
            print(f"[{time}]🚀 Processing: {name} ({cat})")
            try:
                response = handler(conf)
                if "url" in conf:
                    self.fetched_urls[name] = conf["url"]
                if response is not None and hasattr(response, 'status_code') and response.status_code == 200:
                    if hasattr(response, 'parsed_json_data'):
                        json_data = response.parsed_json_data
                    else:
                        json_data = response.json()
                        
                    self.fetched_data[name] = json_data
                    self.save_data(name, cat, url=conf["url"], data=json_data)
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

    def ref_fix(self, ref_key):
        if not ref_key:
            return None, None

        if ref_key in self.fetched_urls:
            ref_url = self.fetched_urls[ref_key]
            if ref_key in self.fetched_data:
                print(f"[{ref_key}]复用")
                return self.fetched_data[ref_key], ref_url
            
            try:
                res = self.session.get(ref_url, timeout=10)
                return (res.json() if res.status_code == 200 else None), ref_url
            except Exception as e:
                print(f"⚠️ 请求[{ref_key}] 失败: {e}")
                return None, ref_url

        if ref_key.startswith("http://") or ref_key.startswith("https://"):
            try:
                res = self.session.get(ref_key, timeout=10)
                return (res.json() if res.status_code == 200 else None), ref_key
            except Exception as e:
                print(f"⚠️ 请求[{ref_key}] 失败: {e}")
                return None, ref_key

        print(f"⚠️ 配置无效: {ref_key}")
        return None, None
if __name__ == "__main__":
    CDNFetcher().run()