## 项目简介
这是一个基于Python的网络设备配置自动备份脚本，支持通过SSH自动连接Cisco系列防火墙、路由器和交换机，定时获取并保存设备配置到本地文件。方便网络运维人员定期备份设备配置，防止配置丢失。

## 功能特点
- 支持多设备批量备份，设备列表可用JSON或CSV格式管理
- 根据设备类型自动执行对应的配置获取命令
- 备份文件命名规范，包含设备主机名、IP和时间戳
- 错误日志记录，方便排查连接失败或异常情况
- 可结合系统定时任务（Windows任务计划程序或Linux crontab）实现自动定时备份

## 使用说明

### 1. 安装依赖
确保已安装Python 3和`netmiko`库：

pip install netmiko
2. 准备设备清单
项目目录下有两个设备清单文件示例：

devices.json（JSON格式）

devices.csv（CSV格式）

可根据格式编辑设备IP、用户名、密码和设备类型。

3. 运行脚本
命令行进入项目目录，运行：

python netmiko_backup.py devices.json
或
python netmiko_backup.py devices.csv
4. 备份结果
备份配置文件会以 {主机名}_{IP}_{时间戳}.txt 形式保存在当前目录

连接或执行异常会记录在 error.log

5. 定时备份建议
Windows用户可用“任务计划程序”添加定时任务

Linux用户可用crontab设置定时任务

设备支持
目前支持的设备类型及其配置命令：

Cisco IOS

Cisco XE

Cisco XR

Cisco NX-OS

Cisco ASA

可根据需求扩展其他设备类型。