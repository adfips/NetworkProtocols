import requests
import subprocess
import re

def get_data_ipapi(list_ip):
    for ip in list_ip:
        response = requests.get(f'http://ip-api.com/json/{ip}?fields=10753')
        get = response.json()
        yield get


def get_ip_tracert(ip):
    output = subprocess.run(["tracert", "-d", ip], stdout=subprocess.PIPE).stdout.decode("cp437")
    pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
    list_ip = re.findall(pattern, output)
    return list_ip


def main():
    list_ip = get_ip_tracert("vk.com")
    for json in get_data_ipapi(list_ip):
        for key, value in json.items():
            print(key, value)
        print()


if __name__ == "__main__":
    main()
