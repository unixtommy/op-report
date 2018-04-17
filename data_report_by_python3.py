#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from datetime import datetime, time
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEBase
from email.mime.text import MIMEText
import smtplib

"""
    AUTHOR: unixtommy 
    Email: unixtommy@gmail.com
"""
str_mon = "2123332,11,2017-12-16 10:00:00,2017-12-16 10:00:11"
str_fri = "8804324,2223332,11,2017-12-18 10:00:00,2017-12-19 10:00:11"
file_mon = "/mnt/167_tmp/data_Monday"
file_fri = "/mnt/167_tmp/data_Friday"

if os.path.exists(file_mon):
    str_mon = open(file_mon).read().split("\n")[1]
else:
    print("%s不存在" % file_mon)
if os.path.exists(file_fri):
    str_fri = open(file_fri).read().split("\n")[1]
else:
    print("%s不存在" % file_fri)

now = datetime.now()
list_mon = str_mon.split(",")
list_fri = str_fri.split(",")
# 周一统计的url提交数量
data_mon = list_mon[0]
# 周五统计的url提交数量
data_fri = list_fri[1]
# 本周工作日提交数量
data_diff = int(data_fri) - int(data_mon)

if len(list_fri) == 5:
    # 舆情临时库记录总量
    content = list_fri[0]
# 获取从数据库中查出来的最近记录写入时间
end = list_fri[3].split(" ")[0]

# 获取当前周的周五
# 0，1，2，3，4，5，6 分别代表周一到周日
cur_monday = now - timedelta(datetime.now().weekday() - 0)
cur_friday = now - timedelta(datetime.now().weekday() - 4)
monday = cur_monday.strftime("%Y-%m-%d")
friday = cur_friday.strftime("%Y-%m-%d")
print("时间范围:%s~%s" % (monday, friday))

if friday != end:
    spider_status = "异常"
    weekday = now.strftime("%A")
    spider_status_content = "异常原因：爬虫状态不正常,数据库中存储的最近一条信息创建时间为: " + str(list_fri[3]) + " 当前时间为: " + str(now) + weekday
else:
    spider_status = "正常"
    spider_status_content = ""
    print("爬虫状态正常")


def send_mail(to_list, sub):
    me = mail_user
    msg = MIMEMultipart()
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ",".join(to_list)

    # 构造html
    html = """\
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>运维日常数据统计报告</title>
<body>
<div id="container">
  <p><strong>运维日常数据统计报告</strong></p>
  <p>采集时间: """ + monday + "~" + friday + """</p>
  <div id="content">
   <table  border="1" bordercolor="black" >
  <tr>
    <td>舆情临时库记录总量（截止到周末的数量）</td>
    <td>关键词导入状态</td>
    <td>URL提交数量（周一）</td>
    <td>URL提交数量（周五）</td>
    <td>本周提交url总数</td>
    <td>本周工作日平均url数量</td>
  </tr>
  <tr>
    <td>""" + content + """</td>
    <td>""" + spider_status + """</td>
    <td>""" + data_mon + """</td>
    <td>""" + data_fri + """</td>
    <td>""" + str(data_diff) + """</td>
    <td>""" + str(data_diff / 5) + """</td>
    
  </tr>
 
</table>
  </div>
</div>
<p><strong>""" + spider_status_content + """</strong> </p>

</div>
</body>
</html>
    """
    context = MIMEText(html, _subtype='html', _charset='utf-8')  # 解决乱码
    msg.attach(context)
    try:
        send_smtp = smtplib.SMTP()
        send_smtp.connect(mail_host)
        send_smtp.login(mail_user, mail_pass)
        send_smtp.sendmail(me, to_list, msg.as_string())
        send_smtp.close()
        return True
    except Exception as e:
        print(e)
        return False


""""""
if __name__ == '__main__':
    # 设置服务器名称、用户名、密码以及邮件后缀
    mail_host = 'smtp.163.com'
    mail_user = 'zabbix_xx@163.com'
    mail_pass = 'password'
    # mailto_lists = sys.argv[1]
    # mailto_list = mailto_lists.split(',')   #发送多人
    # sub= sys.argv[2]
    mailto_list = ['unixtommy@gmail.com', ]
    sub = "运维日常数据统计报告--" + "采集时间:" + monday + "~" + friday
    # send_mail(mailto_list, sub)
    if send_mail(mailto_list, sub):
        print("Send Mail Success !!!")
    else:
        print("Send mail Failed !!!")
