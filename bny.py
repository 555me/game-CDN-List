import os
import requests
import json
from datetime import datetime

URL_CONFIGS = [
          {"name":"background_3.4.0","cat":"ww/launcher","url":"https://prod-cn-alicdn-gamestarter.kurogame.com/launcher/10003_Y8xXrXk65DqFHEDgApn3cpK5lfczpFx5/G152/background/hdKmyCwuX4KO5td8P5yRMB6YmcTXgviF/zh-Hans.json"},
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
          {"name":"VersionList","cat":"dna/launcher","url":"https://pan01-1-eo.shyxhy.com/Patches/FinalPatch/CN/Launcher/PC_OBT_CN_Pub/VersionList.json"},
          {"name":"pkgWin","cat":"ef/launcher","url":"https://launcher.hypergryph.com/api/game/get_latest?sub_channel=1&platform=Windows&channel=1&appcode=6LL0KJuqHBVz33WK&source=game&client_version=1.1.0&version=1.1.0","custom_handler":"ake_ver"},
          {"name":"pkgAnd","cat":"ef/launcher","url":"https://launcher.hypergryph.com/api/game/get_latest_game_info?sub_channel=1&platform=Android&channel=1&appcode=6LL0KJuqHBVz33WK&source=game&client_version=1.1.0&version=1.1.0","custom_handler":"ake_ver"},
          {"name":"notice","cat":"cwsj/game","url":"http://139.196.236.54:8100/notice","method":"POST","header":{"Content-Type":"application/x-www-form-urlencoded","User-Agent":"ProductName/20 CFNetwort/1406.0.4 Darwin/22.4.0","X-Unity-Version":"2020.3.48f1c1","Accept-Language":"zh-CN,zh-Hans;q=0.9","Accept":"*/*"}},
          {"name":"notice","cat":"dna/game","url":"http://pan01-1-eo.shyxhy.com/OperationGameNotice/OperationGameNotice10001"},
          {"name": "BetaBaseVersion","cat": "dna/game","custom_handler": "dnabeta","template": "https://pan01-1-eo.shyxhy.com/Packages/CN/WindowsNoEditor/PC_OBT{obt}_Media_CN_Pub/{v}/BaseVersion.json","obt_range": (18, 11),"v_range": (3, 1)},
          {"name": "BetaVersionList","cat": "dna/game","custom_handler": "dnabeta","template": "https://pan01-1-eo.shyxhy.com/Patches/FinalPatch/CN/Default/WindowsNoEditor/PC_OBT{obt}_Media_CN_Pub/VersionList.json","obt_range": (18, 11)},
          {"name":"noticeBeta","cat":"ww/game","url":"https://aki-gm-resources-back-beta.aki-game2.com/gamenotice/G152/f9e0fc655c1931bc03ad976e9fc14473/zh-Hans.json"},
          {"name":"noticeCN","cat":"nte/game","url":"https://serverlist-yh.wmupd.com/notice_test5/zh-CN/Notice/9_9/Notice.json"},
          {"name":"notcieOS","cat":"nte/game","url":"https://plist-yhglo.perfectworld.com/notice_test5/zh-CN/Notice/11/Notice.json"},
          {"name":"noticeBeta","cat":"dna/game","url":"http://pan01-1-eo.shyxhy.com/OperationGameNotice/OperationGameNotice80001"},
          {"name":"config","cat":"nte/game","url":"https://yhcdn1.wmupd.com/clientRes/publish_PC/Version/Windows/config.xml","custom_handler":"ntever"},
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


    def ake_ver(self, config):
        uri = config["url"]
        local_file = os.path.join("data", config["cat"], f"{config['name']}.json")

        try:
            res = self.session.get(uri, timeout=15)
            if res.status_code != 200:
                return res
            
            apiv = res.json().get("version")
            
            if not apiv:
                print(f"⚠️ Could not find version in remote API for {config['name']}")
                return res

            if os.path.exists(local_file):
                with open(local_file, 'r', encoding='utf-8') as f:
                    try:
                        local_data = json.load(f)
                        fve = local_data.get("version")
                        
                        if fve == apiv:
                            print(f"✅ {config['name']} version {apiv} is unchanged. Skipping update.")
                            return None
                    except Exception as e:
                        print(f"读取本地文件失败，准备覆盖更新: {e}")
            print(f"🚀 New version found for {config['name']}: {apiv}")
            return res
        except Exception as e:
            print(f"⚠️ check_and_fetch error for {config['name']}: {e}")
            return None
        
    def dnabeta(self, config):
        obt_start, obt_end = config.get("obt_range", (18, 11))
        v_start, v_end = config.get("v_range", (3, 1))
        template = config["template"]
        
        has_v = "{v}" in template

        for obt in range(obt_start, obt_end - 1, -1):
            if has_v:
                for v in range(v_start, v_end - 1, -1):
                    target_url = template.format(obt=obt, v=v)
                    res = self.beta_temp(target_url, config)
                    if res: return res
            else:
                target_url = template.format(obt=obt)
                res = self.beta_temp(target_url, config)
                if res: return res
                
        return None

    def beta_temp(self, url, config):
        try:
            res = self.session.get(url, timeout=10)
            if res.status_code == 200:
                config["url"] = url
                print(f"✅ Success: {url}")
                return res
        except Exception:
            pass
        return None
    
    def xml_dec(self, element):
        if len(element) == 0 and not element.attrib:
            return element.text.strip() if element.text else ""

        result = {}
        
        if element.attrib:
            for attr_name, attr_val in element.attrib.items():
                result[f"@{attr_name}"] = attr_val

        for child in element:
            child_data = self.xml_dec(child)
            tag = child.tag
            
            if tag in result:
                if not isinstance(result[tag], list):
                    result[tag] = [result[tag]]
                result[tag].append(child_data)
            else:
                result[tag] = child_data

        text = element.text.strip() if element.text else ""
        if text and len(element) > 0:
            result["#text"] = text

        return result

    def ntever(self, config):
        url = config["url"]
        method = config.get("method", "GET").upper()
        header = config.get('header', {})
        
        try:
            if method == "POST":
                jsonData = config.get('jsonData', None)
                response = self.session.post(url, json=jsonData, headers=header, timeout=30)
            else:
                response = self.session.get(url, timeout=30)
                
            if response.status_code != 200:
                return response

            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            response.parsed_json_data = self.xml_dec(root)
            return response

        except Exception as e:
            print(f"⚠️ XML 解析或请求失败 {config['name']}: {e}")
            return None
        
    def default_fetch(self, config):
        method = config.get("method", "GET").upper()
        url = config["url"]
        payload = config.get("payload", None)
        
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
                    if hasattr(response, 'parsed_json_data'):
                        json_data = response.parsed_json_data
                    else:
                        json_data = response.json()
                        
                    self.save_data(name, cat, url=conf["url"], data=json_data)
                elif response is not None:
                    print(f"❌ Failed: {conf['name']}: HTTP {response.status_code}")
            except Exception as e:
                print(f"⚠️ Error: {e}")
        
        self.write_report()

    def save_data(self, name, cat, url, data):
        dir_path = os.path.join("data", cat)
        os.makedirs(dir_path, exist_ok=True)
        if isinstance(data, dict):
            data["metadata"] = {
                "name": name,
                "category": cat,
                "source_url": url
            }
        elif isinstance(data, list):
            data = {
                "list_data": data,
                "metadata": {
                    "name": name,
                    "category": cat,
                    "source_url": url
                }
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
