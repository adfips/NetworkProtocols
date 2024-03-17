import argparse


import PrettyTable
import requests
import subprocess
import re


def get_data_ipapi(list_ip):
    for ip in list_ip:
        response = requests.get(f'http://ip-api.com/json/{ip}?fields=27137')
        data = response.json()
        if data['status'] == 'success':
            return [data['query'], data['as'].split()[0], data['country'], data['isp']]
        else:
            return [ip, 'local', 'local', 'local']


def get_ip_tracert(ip):
    output = subprocess.run(["tracert", "-d", ip], stdout=subprocess.PIPE).stdout.decode("cp437")
    pattern = re.compile("\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}")
    return pattern.findall(output)[1:]


def format_answer(iterable_ip):
    table = PrettyTable(["hop", "ip", "as", "country", "provider"])
    for i, record in enumerate(iterable_ip):
        table.add_row([i + 1] + record)
    print(table)


def main():
    parser = argparse.ArgumentParser(
        description="Run traceroute and get IP information"
    )
    parser.add_argument("target_ip", help="Target IP address or dns name")
    args = parser.parse_args()

    list_ip = get_ip_tracert(args.target_ip)
    generate_data = (get_data_ipapi(ip) for ip in list_ip)
    format_answer(generate_data)


if __name__ == "__main__":
    main()
