import socket,re,os,time
from subprocess import PIPE, Popen
import tkinter.messagebox


def get_interface_info():
    file = 'arp_table_linux.txt'
    p = Popen('arp -a',stdout=PIPE,stderr=PIPE,shell=True)
    stdout,stderr = p.communicate()
    arp_table = stdout.decode('gbk', errors='ignore')
    with open(file,'w',encoding='utf-8') as f:
        f.writelines(arp_table)
    arp_dict = {}
    with open(file,'r',encoding='utf-8') as g:
        for line in g.readlines():
            if line:
                parts = line.split()
                if len(parts) == 7:
                    ip_address = parts[1]
                    physical_address = parts[3]
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
    arp_dic = get_interface_info()
    result = arp_detection(arp_dic)
    print("以下IP疑似存在Arp欺骗攻击，请排查：",result)


