import os
import requests
import json
from datetime import datetime, timezone, timedelta

URL_CONFIGS = [
          {"name":"notice","cat":"ww/game","url":"https://aki-gm-resources-back.aki-game.com/gamenotice/G152/76402e5b20be2c39f095a152090afddc/zh-Hans.json"},
          {"name":"OperationLauncherUpdateLogProductionChinaonline","cat":"dna/launcher","url":"https://pan01-cdn-dna-ali.shyxhy.com/OperationLauncherUpdateLog/OperationLauncherUpdateLogProductionChinaonline.json"},
          {"name":"OperationLauncherNoticeProductionChinaonline","cat":"dna/launcher","url":"https://pan01-cdn-dna-ali.shyxhy.com/OperationLauncherNotice/OperationLauncherNoticeProductionChinaonline.json"},
          {"name":"OperationLauncherHeadImageProductionChinaonline","cat":"dna/launcher","url":"https://pan01-cdn-dna-ali.shyxhy.com/OperationLauncherHeadImage/OperationLauncherHeadImageProductionChinaonline.json"},
          {"name":"VersionList","cat":"dna/game","url":"https://pan01-1-eo.shyxhy.com/Patches/FinalPatch/CN/Default/WindowsNoEditor/PC_OBT_CN_Pub/VersionList.json"},
          {"name":"bulletinListCn","cat":"ak/game","url":"https://ak-webview.hypergryph.com/api/game/bulletinList?target=Windows"},
          {"name":"bulletinListJp","cat":"ak/game","url":"https://ak-webview.arknights.jp/api/game/bulletinList?target=Windows"},
          {"name":"bulletinListTw","cat":"ak/game","url":"https://ak-webview-tw.gryphline.com/api/game/bulletinList?target=IOS"},
          {"name":"info","cat":"ak/gate","url":"https://ak-webview.hypergryph.com/api/gate/info/Windows"},
          {"name":"meta","cat":"ak/gate","url":"https://ak-webview.hypergryph.com/api/gate/meta/Windows"},
          {"name":"infomation","cat":"ww/launcher","url":"https://prod-cn-alicdn-gamestarter.kurogame.com/launcher/10003_Y8xXrXk65DqFHEDgApn3cpK5lfczpFx5/G152/information/zh-Hans.json"},
          {"name":"winPack","cat":"ak/game","url":"https://launcher.hypergryph.com/api/game/get_latest?appcode=GzD1CpaWgmSq1wew&channel=1&version=68.0.0&platform=Windows&sub_channel=1&source=game"},
          {"name":"andPack","cat":"ak/game","url":"https://launcher.hypergryph.com/api/game/get_latest_game_info?appcode=GzD1CpaWgmSq1wew&channel=1&version=2.6.82&platform=Android&sub_channel=1&source=game"},
          {"name":"aggregate_gate","cat":"ef/game","url":"https://game-hub.hypergryph.com/bulletin/v2/aggregate?lang=zh-cn&platform=Windows&channel=1&type=1&code=endfield_5SD9TN&hideDetail=0"},
          {"name":"aggregate_game","cat":"ef/game","url":"https://game-hub.hypergryph.com/bulletin/v2/aggregate?lang=zh-cn&platform=Windows&channel=1&type=0&code=endfield_5SD9TN&hideDetail=0"},
          {"name":"VersionList","cat":"dna/launcher","url":"https://pan01-1-eo.shyxhy.com/Patches/FinalPatch/CN/Launcher/PC_OBT_CN_Pub/VersionList.json"},
          {"name":"pkgWin","cat":"ef/launcher","url":"https://launcher.hypergryph.com/api/game/get_latest?appcode=6LL0KJuqHBVz33WK&platform=Windows&channel=1&sub_channel=1","custom_handler":"ake_ver"},
          {"name":"pkgAnd","cat":"ef/launcher","url":"https://launcher.hypergryph.com/api/game/get_latest_game_info?appcode=6LL0KJuqHBVz33WK&sub_channel=1&platform=Android&channel=1&source=game&client_version=1.1.0&version=1.1.0","custom_handler":"ake_ver"},
          {"name":"notice","cat":"cwsj/game","url":"http://139.196.236.54:8100/notice","method":"POST","header":{"Content-Type":"application/x-www-form-urlencoded","User-Agent":"ProductName/20 CFNetwort/1406.0.4 Darwin/22.4.0","X-Unity-Version":"2020.3.48f1c1","Accept-Language":"zh-CN,zh-Hans;q=0.9","Accept":"*/*"}},
          {"name":"notice","cat":"dna/game","url":"http://pan01-1-eo.shyxhy.com/OperationGameNotice/OperationGameNotice10001"},
          {"name":"noticeBeta","cat":"ww/game","url":"https://aki-gm-resources-back-beta.aki-game2.com/gamenotice/G152/f9e0fc655c1931bc03ad976e9fc14473/zh-Hans.json"},
          {"name":"noticeCN","cat":"nte/game","url":"https://serverlist-yh.wmupd.com/notice_test5/zh-CN/Notice/9_9/Notice.json"},
          {"name":"notcieOS","cat":"nte/game","url":"https://plist-yhglo.perfectworld.com/notice_test5/zh-CN/Notice/11/Notice.json"},
          {"name":"noticeBeta","cat":"dna/game","url":"http://pan01-1-eo.shyxhy.com/OperationGameNotice/OperationGameNotice80001"},
          {"name":"config","cat":"nte/game","url":"https://yhcdn1.wmupd.com/clientRes/publish_PC/Version/Windows/config.xml","custom_handler":"ntever"},
          {"name":"VersionManifest","cat":"dna/game","url":"https://pan01-1-eo.shyxhy.com/Packages/CN/WindowsNoEditor/PC_OBT_CN_Pub/VersionManifest.json"},
          {"name":"PreVersionManifest","cat":"dna/game","url":"https://pan01-1-eo.shyxhy.com/Packages/CN/WindowsNoEditor/PC_OBT_CN_Pub/PreVersionManifest.json"},
          {"name":"testPack","cat":"ef/launcher","url":"https://launcher.hypergryph.com/api/game/get_latest?appcode=DtPIU2c3bP4Y9Rpo&sub_channel=1&platform=Windows&channel=1"},


          {"name":"winVer","cat":"ef/game","base":"https://launcher.hypergryph.com/api/game/get_latest_resources?appcode=6LL0KJuqHBVz33WK&platform=Windows&game_version={game_version}&version={version}&rand_str={rand_str}","url":"pkgWin","custom_handler":"ake_res"},
          {"name":"background","cat":"ww/launcher","base":"https://prod-cn-alicdn-gamestarter.kurogame.com/launcher/10003_Y8xXrXk65DqFHEDgApn3cpK5lfczpFx5/G152/background/{code}/zh-Hans.json","url":"https://prod-cn-alicdn-gamestarter.kurogame.com/launcher/launcher/10003_Y8xXrXk65DqFHEDgApn3cpK5lfczpFx5/G152/index.json","custom_handler":"wwbg"},
          {"name":"HPatchDiffMd5","cat":"dna/game","base":"https://pan01-1-eo.shyxhy.com/Packages/CN/WindowsNoEditor/PC_OBT_CN_Pub/{v1}/{v2}/full_{v2}/HPatchDiffMd5.json","custom_handler":"dnahp","url":"VersionManifest"},
          {"name":"PreHPatchDiffMd5","cat":"dna/game","base":"https://pan01-1-eo.shyxhy.com/Packages/CN/WindowsNoEditor/PC_OBT_CN_Pub/{v1}/{v2}/full_{v2}/HPatchDiffMd5.json","custom_handler":"dnahp","url":"PreVersionManifest"},
]

class CDNFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.current_hour = datetime.now().strftime("%H")
        self.fetched_urls = {}
        self.fetched_data = {}

    def ake_res(self, config):
        to_ref = config.get("url", "")
        source_data, ref_url = self.ref_fix(to_ref)
        config["url"] = ref_url or "unknow"
        try:
            time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
            version = source_data.get("version")
            file_path = source_data.get("pkg", {}).get("file_path", "")
            if not version or not file_path:
                print(f"[{time}]⚠️ Data missing in API response for {config['name']}")
                return None

            game_version = '.'.join(version.split('.')[:2])

            clean_path = file_path.rstrip('/').replace('/files', '')
            rand_str = clean_path.split('_')[-1]
            
            final_url = config["base"].format(
                game_version=game_version, 
                version=version, 
                rand_str=rand_str
            )
            config["url"] = final_url 
            
            print(f"[{time}]✅ Extracted: game_v={game_version}, v={version}, rand_str={rand_str}")
            return self.session.get(final_url, timeout=10)

        except Exception as e:
            print(f"⚠️ Endfield update handler error details: {type(e).__name__} - {e}")
            return None


    def ake_ver(self, config):
        uri = config["url"]
        local_file = os.path.join("data", config["cat"], f"{config['name']}.json")
        time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")

        try:
            res = self.session.get(uri, timeout=10)
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
                            print(f"[{time}]✅ {config['name']} version {apiv} is unchanged. Skipping update.")
                            return None
                    except Exception as e:
                        print(f"读取本地文件失败，准备覆盖更新: {e}")
            print(f"[{time}]🚀 New version found for {config['name']}: {apiv}")
            return res
        except Exception as e:
            print(f"⚠️ check_and_fetch error for {config['name']}: {e}")
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
                response = self.session.post(url, json=jsonData, headers=header, timeout=10)
            else:
                response = self.session.get(url, timeout=10)
                
            if response.status_code != 200:
                return response

            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            response.parsed_json_data = self.xml_dec(root)
            return response

        except Exception as e:
            print(f"⚠️ XML 解析或请求失败 {config['name']}: {e}")
            return None
        
    def wwbg(self, config):
        into = self.session.get(config['url'],timeout=10)
        time = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        if into.status_code != 200:
            return into
        
        get = into.json()
        bgc = get.get('functionCode',{}).get('background','')

        bgu = config['base'].format(
            code=bgc
        )
        config['url'] = bgu
        print(f'[{time}]✅ latest code: {bgc}')
        return self.session.get(bgu, timeout=10)

    def dnahp(self, config):
        manifest_data, uurrll = self.ref_fix(config.get("url",""))
        diff_template = config.get("base")
        try:
            v1 = manifest_data.get("latest_version_number") or manifest_data.get("pre_download_version_number")
            v2 = manifest_data.get("latest_version") or manifest_data.get("pre_download_version")

            final_url = diff_template.format(v1=v1, v2=v2)
            
            config["url"] = final_url
            
            print(f"✅ 成功提取版本参数: v1={v1}, v2={v2}")

            return self.session.get(final_url, timeout=10)

        except Exception as e:
            print(f"⚠️ dna_manifest_diff 发生异常 {config['name']}: {e}")
            return None
        
    def default_fetch(self, config):
        method = config.get("method", "GET").upper()
        url = config["url"]
        payload = config.get("payload", None)
        
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
                    print(f"[{time}]❌ Failed: {conf['name']}: HTTP {response.status_code}")
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
