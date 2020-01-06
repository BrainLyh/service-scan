import time
import socket
from ftplib import FTP
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool


class Ftp(object):

    def __init__(self):
        self.save_path = "./result.txt"
        self.ip_list = []
        self.avleableList = ""

    def port_scan(self, ip):

        print("[+] Testing ports of : " + str(ip) + "\n")
        # scan_port(line.strip())
        # 测试ftp端口是否开放
        sk1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk1.settimeout(1)
        url2 = ip
        # try_login_ftp(url2, save_path)
        try:
            res1 = sk1.connect_ex((ip, 21))
            # print(res1)
            if res1 == 0:
                print("\n[+] " + str(url2) + "s ftp service is ok! try to login...\r\n")
                self.try_login_ftp(url2)

        except Exception as e:
            print("\n[+] " + str(url2) + "s ftp service is bad!" + e + "\r\n")
        sk1.close()
        return

    def try_login_ftp(self, ip):

        # 如果输出 user 和 pwd 为空则说明该 ftp 服务允许匿名访问
        try:
            ftp = FTP()
            ftp.connect(ip)
            with open("ftp_dict.txt", 'r') as f:
                for line in f.readlines():
                    # print line.strip()
                    user = line.strip().split("|")[0]
                    pwd = line.strip().split("|")[1]
                    try:
                        ftp.login(user, pwd)  # 匿名访问
                        # 访问成功
                        print(
                            "[+] " + str(ip) + "s FTP service login successful！username= " +
                            user + "pwd = " + pwd + "\r\n")
                    except Exception as e:
                        # print("\n[+] " + str(ip) + "s ftp login failed.")
                        break
                    # 将结果写入文件 result.txt
                    self.avleableList += "\rftp service -- " + str(time.asctime()) + " ip: " + \
                                    str(ip) + " username | pwd : " + str(user) + " | " + str(pwd)
                    self.save_result(self.avleableList)
                    # 尝试读取目录
                    try:
                        print("\n[+] " + str(ip) + "s ftp 文件目录为：")
                        ftp.dir()
                    except Exception as e:
                        print("读取目录失败")
                        break
        except Exception as e:
            print(e)
            print("\n[+] " + str(ip) + "s ftp service login failed!\r\n")
            pass
        return

    def save_result(self, result_list):
        s = open(self.save_path, "a")
        # print(result_list)
        s.write(result_list)
        s.close()
        return

    def PrintResult(self):

        return self.avleableList

    def threadpool(self):

        with open('iprange.txt', 'rb') as f:
            for line in f.readlines():
                self.ip_list.append(line.strip())

        # self.ip_list.append(ip)
        print(self.ip_list)
        t1 = datetime.now()
        # 线程数为20
        pool = ThreadPool(processes=20)
        try:
            pool.map(self.port_scan, self.ip_list)
        except Exception as e:
            print(e)
        pool.close()
        pool.join()
        # print(self.save_result())
        print('Multiprocess Scanning Completed in  ', datetime.now() - t1)
        # port_scan(save_path="./result.txt")
        return
