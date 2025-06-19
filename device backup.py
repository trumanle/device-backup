"""
自动备份多台网络设备配置脚本
依赖：pip install netmiko
用法：python netmiko_backup.py devices.json
"""

import os
import sys
import json
import csv
import datetime
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

# 支持的设备类型及其获取配置命令
DEVICE_COMMANDS = {
    'cisco_ios': 'show running-config',
    'cisco_xe': 'show running-config',
    'cisco_xr': 'show running-config',
    'cisco_nxos': 'show running-config',
    'cisco_asa': 'show running-config',
    # 可扩展其他类型
}

def load_devices(file_path):
    """从JSON或CSV文件加载设备信息"""
    devices = []
    if file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            devices = json.load(f)
    elif file_path.endswith('.csv'):
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                devices.append(row)
    else:
        print('仅支持JSON或CSV格式的设备清单文件！')
        sys.exit(1)
    return devices

def log_error(msg):
    """记录错误日志到error.log"""
    with open('error.log', 'a', encoding='utf-8') as f:
        f.write(f"{datetime.datetime.now()} - {msg}\n")

def backup_device_config(device):
    """连接设备并备份配置"""
    ip = device.get('ip')
    device_type = device.get('device_type')
    command = DEVICE_COMMANDS.get(device_type)
    if not command:
        msg = f"[跳过] 设备 {ip} 类型 {device_type} 暂不支持自动备份。"
        print(msg)
        log_error(msg)
        return
    try:
        print(f"[连接] 正在连接 {ip} ...")
        conn = ConnectHandler(**device)
        hostname = conn.find_prompt().strip('#>\\n ')
        print(f"[成功] 登录 {hostname} ({ip})，获取配置...")
        output = conn.send_command(command)
        date_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{hostname}_{ip}_{date_str}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"[完成] 配置已保存到 {filename}\\n")
        conn.disconnect()
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        msg = f"[错误] 连接 {ip} 失败: {e}"
        print(msg)
        log_error(msg)
    except Exception as e:
        msg = f"[异常] 处理 {ip} 时发生未知错误: {e}"
        print(msg)
        log_error(msg)

def main():
    if len(sys.argv) != 2:
        print(f"用法: python {os.path.basename(sys.argv[0])} <设备清单文件.json/csv>")
        sys.exit(1)
    file_path = sys.argv[1]
    devices = load_devices(file_path)
    print(f"共加载 {len(devices)} 台设备，开始备份...\\n")
    for device in devices:
        backup_device_config(device)
    print("全部设备处理完毕。")

if __name__ == '__main__':
    main()