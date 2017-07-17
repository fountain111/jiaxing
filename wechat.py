import itchat
import datetime
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    if msg.text == '出差':
        location = msg.text[2:3]
        today = datetime.date.today()  # 获取今天日期
        deltadays = datetime.timedelta(days=1)  # 确定日期差额，如前天 days=2
        tomorrow = today + deltadays


        msg.text = location+tomorrow
        print(msg.text)


    return msg.text[0]

itchat.auto_login()
itchat.run()