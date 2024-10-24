import csv
import requests
import time

http_ports = [80,8080,8880,2052,2082,2086,2095]
tls_ports = [443,2053,2083,2087,2096,8443]
# 查询 IP 的国家代码
def get_country_code(ip):
    try:
        # 使用 ip-api.com 查询 IP 的地理信息
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=countryCode")
        data = response.json()
        print(data)
        if response.status_code == 200 and "countryCode" in data:
            return data["countryCode"]
        else:
            return "XX"  # 无法获取国家代码时返回 XX
    except Exception as e:
        print(f"Error querying IP {ip}: {e}")
        return "XX"


# 读取 CSV 文件并进行转换，保存为 txt 文件，且只处理前 N 行
def convert_csv_to_txt_with_country(csv_file_path, txt_file_path, trojan_file_path,N):
    tls_port_index = 0
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile, \
            open(txt_file_path, 'w', encoding='utf-8') as txtfile,\
            open(trojan_file_path, 'w', encoding='utf-8') as trojanfile:

        reader_csv = csv.reader(csvfile)
        next(reader_csv)  # 跳过表头

        count = 0  # 行数计数器

        for row in reader_csv:
            if count >= N:
                break  # 只处理前 N 行，超出后跳出循环

            ip = row[0]  # IP 地址
            download_speed = float(row[5])  # 下载速度 (MB/s)

            # 只处理下载速度 >= 10 的节点
            if download_speed >= 10:
                # 查询 IP 的国家代码
                country_code = get_country_code(ip)
                if tls_port_index > len(tls_ports)-1:
                    tls_port_index = 0
                port = tls_ports[tls_port_index]
                # 下载速度乘以100并转换为整数，输出格式: IP 地址:443#国家代码+下载速度*100
                txtfile.write(f"{ip}:{port}#P{port}{country_code}{int(download_speed * 100)}@Vless\n")
                trojanfile.write(f"{ip}:{port}#P{port}{country_code}{int(download_speed * 100)}@Trojan\n")
                tls_port_index += 1
            count += 1  # 每处理一行，计数器加1
            # time.sleep(1)  # 加上延时以避免请求过于频繁


# 调用函数，传入 CSV 文件路径、输出的 TXT 文件路径、和要处理的行数 N
convert_csv_to_txt_with_country('./cfscan/result.csv', './cfscan/toutput-vl.txt', './cfscan/toutput-tj.txt',N=10)
