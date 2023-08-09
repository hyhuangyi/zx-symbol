import pandas as pd

df = pd.read_excel('d:/已解密_第二批邮箱导入.xlsx', keep_default_na=False)

data = df.values
for item in data:
    name = item[0]
    receiverName = item[1]
    receiverMail = item[2]

    sql = "update `project` set receiver_name=" + "'" + receiverName + "',receiver_mail=" + "'" + receiverMail + "' where name=" + "'" + name + "';"

    print(sql)
