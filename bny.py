import os
import requests
import json
from datetime import datetime

URL_CONFIGS = [
          {"name":"background_3.1.0","cat":"ww/launcher","url":"https://prod-cn-alicdn-gamestarter.kurogame.com/launcher/10003_Y8xXrXk65DqFHEDgApn3cpK5lfczpFx5/G152/background/SH3ufRtnpVr3oAI4ViFe8oFusBdHjdMS/zh-Hans.json"},
          {"name":"notice","cat":"ww/game","url":"https://aki-gm-resources-back.aki-game.com/gamenotice/G152/76402e5b20be2c39f095a152090afddc/zh-Hans.json"},
          {"name":"OperationLauncherUpdateLogProductionChinaonline","cat":"dna/launcher","url":"https://pan01-cdn-dna-ali.shyxhy.com/OperationLauncherUpdateLog/OperationLauncherUpdateLogProductionChinaonline.json"},
          {"name":"OperationLauncherNoticeProductionChinaonline","cat":"dna/launcher","url":"https://pan01-cdn-dna-ali.shyxhy.com/OperationLauncherNotice/OperationLauncherNoticeProductionChinaonline.json"},
          {"name":"OperationLauncherHeadImageProductionChinaonline","cat":"dna/launcher","url":"https://pan01-cdn-dna-ali.shyxhy.com/OperationLauncherHeadImage/OperationLauncherHeadImageProductionChinaonline.json"},
          {"name":"BaseVersion","cat":"dna/game","base_url_template":"https://pan01-1-eo.shyxhy.com/Packages/CN/WindowsNoEditor/PC_OBT_CN_Pub/{v}/BaseVersion.json","custom_handler":"dnaver_base","start_version":20,"end_version":9},
          {"name":"VersionList","cat":"dna/game","url":"https://pan01-1-eo.shyxhy.com/Patches/FinalPatch/CN/Default/WindowsNoEditor/PC_OBT_CN_Pub/VersionList.json"},
          {"name":"bulletinListCn","cat":"ak/game","url":"https://ak-webview.hypergryph.com/api/game/bulletinList?target=Windows"},
          {"name":"bulletinListJp","cat":"ak/game","url":"https://ak-webview.arknights.jp/api/game/bulletinList?target=IOS"},
          {"name":"bulletinListTw","cat":"ak/game","url":"https://ak-webview-tw.gryphline.com/api/game/bulletinList?target=IOS"},
          {"name":"info","cat":"ak/gate","url":"https://ak-webview.hypergryph.com/api/gate/info/Windows"},
          {"name":"meta","cat":"ak/gate","url":"https://ak-webview.hypergryph.com/api/gate/meta/Windows"},
          {"name":"infomation","cat":"ww/launcher","url":"https://prod-cn-alicdn-gamestarter.kurogame.com/launcher/10003_Y8xXrXk65DqFHEDgApn3cpK5lfczpFx5/G152/information/zh-Hans.json"},
          {"name":"winPack","cat":"ak/game","url":"https://launcher.hypergryph.com/api/game/get_latest?appcode=GzD1CpaWgmSq1wew&channel=1&version=68.0.0&platform=Windows&sub_channel=1&source=game"},
          {"name":"andPack","cat":"ak/game","url":"https://launcher.hypergryph.com/api/game/get_latest_game_info?appcode=GzD1CpaWgmSq1wew&channel=1&version=2.6.82&platform=Android&sub_channel=1&source=game"},
          {"name":"aggregate_gate","cat":"ef/game","url":"https://game-hub.hypergryph.com/bulletin/v2/aggregate?lang=zh-cn&platform=Windows&channel=1&type=1&code=endfield_5SD9TN&hideDetail=0"},
          {"name":"aggregate_game","cat":"ef/game","url":"https://game-hub.hypergryph.com/bulletin/v2/aggregate?lang=zh-cn&platform=Windows&channel=1&type=0&code=endfield_5SD9TN&hideDetail=0"},
          {"name":"winVer","cat":"ef/game","api_template":"https://launcher.hypergryph.com/api/game/get_latest_resources?appcode=6LL0KJuqHBVz33WK&platform=Windows&game_version={game_version}&version={version}&rand_str={rand_str}","api_source":"https://launcher.hypergryph.com/api/game/get_latest?sub_channel=1&platform=Windows&channel=1&appcode=6LL0KJuqHBVz33WK&source=game&client_version=1.0.13&version=1.0.10","custom_handler":"ake_res"},
          {"name":"PreDownloadVersion","cat":"dna/game","url":"https://pan01-1-eo.shyxhy.com/Packages/CN/WindowsNoEditor/PC_OBT_CN_Pub/PreDownloadVersion.json"},
          {"name":"VersionList","cat":"dna/launcher","url":"https://pan01-1-eo.shyxhy.com/Patches/FinalPatch/CN/Launcher/PC_OBT_CN_Pub/VersionList.json"}
    # 示例：POST 请求 (满足需求2)
    # {"name":"winPack","cat":"ak/game","url":"https://launcher.hypergryph.com/api/game/get_latest","method":"POST","payload": {"appcode": "GzD1CpaWgmSq1wew", "platform": "Windows"} },
    
    # 示例：带自定义处理逻辑的任务 (满足需求2 & 3)
    # {"name": "dynamic_task","cat": "custom/task","url": "https://api.example.com/data","custom_handler": "handle_special_logic" }
]

class CDNFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.current_hour = datetime.now().strftime("%H")


    def dnaver_base(self, config):
        start = config.get("start_version", 20)
        end = config.get("end_version", 10)
        template = config["base_url_template"]
        
        for v in range(start, end - 1, -1):
            target_url = template.format(v=v)
            
            try:
                response = self.session.get(target_url, timeout=15)
                if response.status_code == 200:
                    print(f"✅ Found active version: {v}")
                    config["url"] = target_url 
                    return response
                elif response.status_code == 404:
                    continue
            except Exception as e:
                print(f"⚠️ Connection error at v{v}: {e}")
                
        return response
    def ake_res(self, config):
        config["url"] = config.get("api_source", "unknown")
        
        try:
            source_res = self.session.get(config["api_source"], timeout=15)
            if source_res.status_code != 200:
                return source_res
            
            source_data = source_res.json()
            version = source_data.get("version")
            file_path = source_data.get("pkg", {}).get("file_path", "")
            if not version or not file_path:
                print(f"⚠️ Data missing in API response for {config['name']}")
                return source_res

            game_version = '.'.join(version.split('.')[:2])

            clean_path = file_path.rstrip('/').replace('/files', '')
            rand_str = clean_path.split('_')[-1]
            
            final_url = config["api_template"].format(
                game_version=game_version, 
                version=version, 
                rand_str=rand_str
            )
            config["url"] = final_url 
            
            print(f"✅ Extracted: game_v={game_version}, v={version}, rand_str={rand_str}")
            return self.session.get(final_url, timeout=15)

        except Exception as e:
            print(f"⚠️ Endfield update handler error details: {type(e).__name__} - {e}")
            return None

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