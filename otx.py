#!/usr/bin/python3
import urllib3, sys, json, os

class Recon():
    def __init__(self):
        self.domain = sys.argv[1]
        self.http = urllib3.PoolManager()
        try:
            os.mkdir(sys.argv[1])
        except Exception:
            pass
    def passive_dns(self):
        r = self.http.request("GET",f"https://otx.alienvault.com/otxapi/indicator/hostname/passive_dns/{self.domain}")
        return json.loads(r.data.decode('utf-8'))
    def urls(self,sub):
        r = self.http.request("GET",f"https://otx.alienvault.com/otxapi/indicator/hostname/url_list/{sub}")
        return json.loads(r.data.decode('utf-8'))

bot = Recon()

print("[*] Looking for subdomains.....")
for i in bot.passive_dns()["passive_dns"]:
    with open(f"./{bot.domain}/subdomains.txt","a") as save_file:
        if bot.domain in i["hostname"]:
            save_file.write(i["hostname"]+"\n")
            print(i["hostname"])
    save_file.close()


print("[*] Looking for urls.....")
for i in bot.passive_dns()["passive_dns"]:
    if bot.domain in i["hostname"]:
        # print(bot.urls(i["hostname"]))
        for b in bot.urls(i["hostname"])["url_list"]:
            with open(f"./{bot.domain}/urls.txt","a") as save_file:
                save_file.write(b["url"]+"\n")
                print(b["url"])
            save_file.close()