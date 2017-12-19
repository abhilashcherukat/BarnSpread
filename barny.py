import hashlib
import json
import smtplib
from datetime import datetime
import urllib
import re
import linecache
import sys
import MySQLdb
import collections
import web
import random

import time
import dicttoxml
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import fromstring, Element

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

urls = (
    '/', 'index',
    
)
# Server
db = web.database(dbn='mysql', user='root', pw='igothelp2015', db='igothelp2015 ')
#Local
db = web.database(dbn='mysql', user='root', pw='igothelp2015', db='igothelp2015V3')




class index:
    def GET(self):
        status = {"status": "Info", "message": "This page is intentionally left blank.","statusCode":121}
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', '*')
        web.header('Content-Type', 'application/json')
        return  json.dumps(status)


class test:
    def POST(self):
      return 1

    def GET(self):
        ComFnObj = Commonfunctions()
        return json.dumps(ComFnObj.GetCallLogs(27))
        return 1



#FOR REUSABLE FUNCTIONS
class Commonfunctions:


    def LogError(self, message, APICall, LineNo):
        try:
            now = datetime.now()
            date = str(now.year)+"-"+str(now.month)+"-"+str(now.day)+" "
            time = str(now.hour)+":"+str(now.minute)+":"+str(now.second)
            entries = db.insert('errorLog', time=date+time,API=APICall,\
                                        lineNumber=LineNo,details=str(message))
        except:
            pass
    def SMSEmailLog(self,To,From,Type,API,Message):
        #try:
              db.insert('smsEmailLog',recepient=To,frm=From,details=Type,apiCall=API,message=Message)

        #except:
        #    self.PrintException("SMSEMailLog")
    def PrintException(self,API):
        try:
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            print exc_obj
            line = linecache.getline(filename, lineno, f.f_globals)
            linepart=line.strip()
            #linePart="".join(linePart)
            msg=str(exc_obj)+"[" + linepart + "...]"
            return self.LogError(msg,API,lineno)#
        except:
            pass
    def SendSMS(self, To, Msg):
        URL = "http://alerts.sinfini.com/api/web2sms.php?workingkey=663040hvmlrbxmd00792&to=" + str(
            To) + "&sender=GOTHLP&message=" + Msg
        response = urllib.urlopen(URL)
        return response
    def SendMail(self, To, From, Subject, Html,Plain):
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = Subject
            msg['From'] = From
            msg['To'] = To
            part1 = MIMEText(Plain, 'plain',"utf-8")
            part2 = MIMEText(Html, 'html')
            msg.attach(part1)
            msg.attach(part2)
            # Send the message via local SMTP server.
            #mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('abhilash.c@spurtreetech.com', 'Ab4i7@$h')
            mail.sendmail(From,To, msg.as_string())
            mail.quit()
            status = {"status": "Sucess", "message": "Mail Sent","statusCode":200,"MailSent":True}
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(status)
        except smtplib.SMTPAuthenticationError:
            self.PrintException("Mail Sent Function")
            status = {"status": "Error", "message": "Authentication Error","statusCode":500,"MailSent":False}
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(status)

        except Exception as e:
            self.PrintException("Mail Sent Function")
            status = {"status": "Error", "message": "Error Try Later","statusCode":str(e)}
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(status)

    def GetIdFromAuth(self, AuthCode):
        k = "AuthCode='" + AuthCode + "'"
        entries = db.select('user', what='ID', where=k)
        rows = entries.list();
        if rows:
            return rows[0]['ID']
        else:
            return -1
    def GetIdFromPhone(self, Number, Type):  #Type= 'USR' for User and 'DOC for Doctor'
        if Type == "USR":
            table = "user"
        else:
            table = "Doctor"

        entries = db.select(table, what='ID', where='Phone='+Number)
        rows = entries.list();
        if rows:
            return rows[0]["ID"]
        else:
            return -1
    def CheckAuth(self, AuthCode):
        try:
            JResponse=collections.OrderedDict()
            print "Authcode Passed",str(AuthCode)
            k = "AuthCode='" + str(AuthCode) + "'"
            entries = db.select('user', where=k)
            rows = entries.list();
            if rows:
                for row in rows:
                    JArray={"ID":str(row['ID']),\
                         "FirstName":row['FirstName'],\
                         "LastName":row['LastName'],\
                         "Phone":row['Phone'],\
                         "Email":row['Email'],\
                         "Birthday":row['BirthDate'],\
                         "Gender":row['Gender'],\
                         "BloodGroup":row['BloodGroup'],\
                         "RegistrationDate":row['RegistrationDate'],\
                         "AuthCode":row['AuthCode']\
                        }
                JResponse["SubscriptionData"]=JArray
                JResponse["Success"] =True
                JResponse["StatusCode"]=777
                JResponse["Message"] ="Record retrived successfully"
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods', '*')
                web.header('Access-Control-Allow-Headers', '*')
                web.header('Content-Type', 'application/json')
                return  json.dumps(JResponse)
            else:
                JResponse["SubscriptionData"]={}
                JResponse["Success"] =True
                JResponse["StatusCode"]=121
                JResponse["Message"] ="No user exist"
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods', '*')
                web.header('Access-Control-Allow-Headers', '*')
                web.header('Content-Type', 'application/json')
                return  json.dumps(JResponse)
        except Exception as e:
            JResponse["Info"]={}
            JResponse["Success"] =False
            JResponse["StatusCode"]=600
            JResponse["Message"] ="Some Error Happened"+str(e)
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(JResponse)
    def GenerateOTP(self,Phone,Count=4):
        m = hashlib.md5()
        now = datetime.now()
        mm = str(now.month)
        ss = str(now.second)
        rd=random.random()*1000
        Gen = str(Phone) + mm + ss+str(rd)
        m.update(Gen)
        Plain = m.hexdigest()
        k = re.findall(r'\d+', Plain)
        return "".join(k)[:Count]
    def GetCategoryFromID(self,CatId):

        entries = db.select("doctorcategory",where="ID="+str(CatId))
        rows = entries.list();
        JArray=[]
        if rows:
            JArray={"ID":rows[0]['ID'], "Title":rows[0]['Title']}
        return JArray

class checkregistration:
    def GET(self):

        status = {"status": "Info", "message": "This page is intentionally left blank.","statusCode":121,"success":True}
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', '*')
        web.header('Content-Type', 'application/json')
        return  json.dumps(status)


    def POST(self):
        ComFnObj = Commonfunctions()
        data = web.input(Phone='')
        print data
        JResponse=collections.OrderedDict()
        try:
            k = "Phone='" + data.phone + "'"
            entries = db.select('user', what='AuthCode', where=k)
            rows = entries.list();
            if rows:
                OTP = ComFnObj.GenerateOTP(data.phone,4)
                Message = "Please verify your phone number using this OTP " + str(OTP)

                Auth=rows[0]["AuthCode"]
                ComFnObj.SendSMS(data.phone, Message)
                db.query("update user set OTP="+str(OTP)+" where Phone='"+data.phone+"'")
                JResponse["Info"] ={}
                JResponse["Success"] =True
                JResponse["StatusCode"]=777
                JResponse["Message"] ="OTP Send"
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods', '*')
                web.header('Access-Control-Allow-Headers', '*')
                web.header('Content-Type', 'application/json')
                return  json.dumps(JResponse)

            else:
                JResponse["Info"] ={}
                JResponse["Success"] =True
                JResponse["StatusCode"]=121
                JResponse["Message"] ="Registration Required"
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods', '*')
                web.header('Access-Control-Allow-Headers', '*')
                web.header('Content-Type', 'application/json')
                return  json.dumps(JResponse)
        except Exception as e:
            JResponse["Info"] ={}
            JResponse["Success"] =False
            JResponse["StatusCode"]=600
            JResponse["Message"] ="Some error happened:"+str(e)
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(JResponse)
class verify:
    def GET(self):
        status = {"status": "Info", "message": "This page is intentionally left blank.","statusCode":121}
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', '*')
        web.header('Content-Type', 'application/json')
        return  json.dumps(status)
    def POST(self):
        ComFnObj = Commonfunctions()
        user_data = web.input()
        try:

            k = "Phone='"+user_data.phone+"'and OTP=" + user_data.OTP + ""
            entries = db.select('user', what='AuthCode', where=k)
            rows = entries.list();
            JResponse=collections.OrderedDict()
            if rows:
                row=rows[0]
                JResponse["Info"] =row["AuthCode"]
                JResponse["Success"] =True
                JResponse["StatusCode"]=777
                JResponse["Message"] ="Registration Success"
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods', '*')
                web.header('Access-Control-Allow-Headers', '*')
                web.header('Content-Type', 'application/json')
                return  json.dumps(JResponse)
            else:
                JResponse["Info"] ={}
                JResponse["Success"] =True
                JResponse["StatusCode"]=121
                JResponse["Message"] ="OTP Verification Failed"
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods', '*')
                web.header('Access-Control-Allow-Headers', '*')
                web.header('Content-Type', 'application/json')
                return  json.dumps(JResponse)
        except Exception as e:
            JResponse["Info"] ={}
            JResponse["Success"] =False
            JResponse["StatusCode"]=666
            JResponse["Message"] ="Some Error Happened:"+str(e.message)
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(JResponse)
class register:
    def GET(self):
        ComFnObj = Commonfunctions()
        status = {"status": "Info", "message": "This page is intentionally left blank.","statusCode":121,"success":True}
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', '*')
        web.header('Content-Type', 'application/json')
        return  json.dumps(status)


    def POST(self):
        JResponse=collections.OrderedDict();
        try:
            t = db.transaction()
            ComFnObj = Commonfunctions()
            # user_data = json.loads(json_input)
            user_data = web.input()
            Salt = "$343dddSS"
            String = user_data.firstname + user_data.phone + Salt
            m = hashlib.md5()
            m.update(String)
            Authcode = m.hexdigest()
            OTP = ComFnObj.GenerateOTP(user_data.phone,4)
            print OTP
            entries = db.insert('user', FirstName=user_data.firstname, \
                                    LastName=user_data.lastname, Phone=user_data.phone, \
                                    Email=user_data.email, BirthDate=user_data.dob, \
                                    Gender=user_data.gender, BloodGroup=user_data.bloodgroup, \
                                    AuthCode=Authcode,OTP=OTP)

            Message = "Please verify your phone number using this OTP " + OTP
            ComFnObj.SendSMS(user_data.phone, Message)
            #render = web.template.render('/var/www/html/Templates')
            render = web.template.render('Templates')
            USERNAME=user_data.firstname+" "+user_data.lastname
            Returner=render.Welcome(USERNAME)
            MailBody=Returner['__body__']
            MailBodyPlain="Registration Complete"
            ComFnObj.SendMail(user_data.email,"support@igothelp.com","Welcome to I Got Helps",MailBody,MailBodyPlain)

        except MySQLdb.IntegrityError, e:
            t.rollback()
            JResponse["Info"] ={}
            JResponse["Success"] =False
            JResponse["StatusCode"]=600
            JResponse["Message"] ="Some error happened:"+str(e)
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(JResponse)
        except Exception as e:
            t.rollback()
            JResponse["Info"] ={}
            JResponse["Success"] =False
            JResponse["StatusCode"]=600
            JResponse["Message"] ="Some error happened:"+str(e)
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(JResponse)
        else:
            t.commit()
            JResponse["Info"] ={}
            JResponse["Success"] =True
            JResponse["StatusCode"]=777
            JResponse["Message"] ="OTP Send"
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(JResponse)
class login:
    def GET(self):
        ComFnObj = Commonfunctions()
        user_data = web.input()
        print user_data.Phone
        status = {"status": "Info", "message": "This page is intentionally left blank.","statusCode":121,"success":True}
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', '*')
        web.header('Content-Type', 'application/json')
        return  json.dumps(status)


    def POST(self):
        ComFnObj = Commonfunctions()
        user_data = web.input()
        header = web.ctx.environ
        Authcode = header.get('HTTP_AUTHCODE')
        JResponse=collections.OrderedDict();
        try:
            flag = 0
            Id1 = ComFnObj.GetIdFromPhone(user_data.Phone, "USR")
            Id2 = ComFnObj.GetIdFromAuth(Authcode)
            if (Id1 != Id2):
                JResponse["Info"] ={}
                JResponse["Success"] =True
                JResponse["StatusCode"]=777
                JResponse["Message"] ="Login Successfull"
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods', '*')
                web.header('Access-Control-Allow-Headers', '*')
                web.header('Content-Type', 'application/json')
                return  json.dumps(JResponse)
            else:
                JResponse["Info"] ={}
                JResponse["Success"] =True
                JResponse["StatusCode"]=121
                JResponse["Message"] ="Login Failed"
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Access-Control-Allow-Methods', '*')
                web.header('Access-Control-Allow-Headers', '*')
                web.header('Content-Type', 'application/json')
                return  json.dumps(JResponse)
        except:
            JResponse["Info"] ={}
            JResponse["Success"] =False
            JResponse["StatusCode"]=600
            JResponse["Message"] ="Some Error happened"
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(JResponse)
class barn:
    def POST(self):
        JResponse=collections.OrderedDict()
        try:

                t = db.transaction()
                ComFnObj = Commonfunctions()
                # user_data = json.loads(json_input)
                user_data = web.input(Type=1)
                if user_data.Type==1:
                    entries = db.insert('patientprofile', FirstName=user_data.firstname, \
                                        LastName=user_data.lastname,BirthDate=user_data.dob, \
                                        Gender=user_data.gender, BloodGroup=user_data.bloodgroup, \
                                       User_ID=user_data.ID,Relationship=user_data.relationship)
                else:
                    entries = db.update('patientprofile', FirstName=user_data.firstname, \
                                        LastName=user_data.lastname,BirthDate=user_data.dob, \
                                        Gender=user_data.gender, BloodGroup=user_data.bloodgroup\
                                       ,Relationship=user_data.relationship, where="User_ID='"+str(user_data.ID)+"'")
        except Exception as e:
            t.rollback()
            JResponse["Info"] ={}
            JResponse["Success"] =False
            JResponse["StatusCode"]=600
            JResponse["Message"] ="Some error happened:"+str(e)
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(JResponse)
        else:
            Msg=[]
            Msg[1]="Added Successfully"
            Msg[2]="Updated Successfully"

            t.commit()
            JResponse["Info"] ={}
            JResponse["Success"] =True
            JResponse["StatusCode"]=777
            JResponse["Message"] =Msg[user_data.Type]
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(JResponse)



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
else:
    application = web.application(urls, globals()).wsgifunc()