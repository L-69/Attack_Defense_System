import socket,re,os,time
from subprocess import PIPE, Popen
import tkinter.messagebox


# 获取主机的 IP 地址
def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # 使用 IPv4 地址族和 UDP 协议
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]  # 返回IP地址
    s.close()
    return ip
def get_interface_info(interface):
    file = 'arp_table_win.txt'
    p = Popen(f'arp /a /n {interface}',stdout=PIPE,stderr=PIPE)
    stdout,stderr = p.communicate()
    arp_table = stdout.decode('gbk', errors='ignore')
    with open(file,'w',encoding='utf-8') as f:
        f.writelines(arp_table)
    arp_dict = {}
    with open(file,'r',encoding='utf-8') as g:
        for line in g.readlines():
            if line:
                parts = line.split()
                if len(parts) == 3:
                    ip_address = parts[0]
                    physical_address = parts[1]
                    arp_dict[ip_address] = physical_address
    return arp_dict

def arp_detection(arp_dic):
    values = list(arp_dic.values())
    attack_result = []
    for v in set(values):
        if values.count(v) > 1 and v != "ff-ff-ff-ff-ff-ff":
            attack_result.extend([(k, v) for k in arp_dic if arp_dic[k] == v])
    return attack_result



if __name__ == '__main__':
    ip = get_host_ip()
    arp_dic = get_interface_info(ip)
    result = arp_detection(arp_dic)
    print("以下IP疑似存在Arp欺骗攻击，请排查：",result)


