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
import rijndael
import base64

import time


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

urls = (
    '/', 'index',
    '/test','test',
    '/barn/(.*)','barn',
    '/commonlist/(.*)','commonlist',
    '/classroom/(.*)','classroom'

)
# Server
#db = web.database(dbn='mysql', user='root', pw='MIh3TioWViMDEpLQ', db='igothelp2015 ')
#Local
db = web.database(dbn='mysql', user='usr_barner', pw='MIh3TioWViMDEpLQ', db='db_barner')




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
        return ComFnObj.Decrypt("4X0NUZm6VkmgltrVQYqnAUSCuPq6yl4u0r+iP3zXCz8=")



#FOR REUSABLE FUNCTIONS
class Commonfunctions:

    KEY_SIZE = 16
    BLOCK_SIZE = 32
    KEY="345dsfdf32432SDGGF234dksj4djKJKJ"
    def SMSEmailLog(self,To,From,Type,API,Message):
        try:
              db.insert('smsEmailLog',recepient=To,frm=From,details=Type,apiCall=API,message=Message)

        except:
            self.PrintException("SMSEMailLog")
    def LogAction(self,API,message,ACT):
        try:
            
            entries = db.insert('actionLog', API=API,lineNumber=0,details=str(message),Type=ACT)
        except:
            pass
    def LogError(self, message, APICall, LineNo):
        try:
            
            entries = db.insert('actionLog', API=APICall,lineNumber=LineNo,details=str(message),Type="ERR")
        except:
            pass
    def SMSEmailLog(self,To,From,Type,API,Message):
        #try:
              db.insert('smsEmailLog',recepient=To,frm=From,details=Type,apiCall=API,message=Message)

        #except:
        #    self.ComFnObj.PrintException("SMSEMailLog")
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
            self.LogError(msg,API,lineno)
        except:
            pass


    def SendSMS(self, To, Msg):
        URL = "http://alerts.sinfini.com/api/web2sms.php?workingkey=663040hvmlrbxmd00792&to=" + str(To) + "&sender=GOTHLP&message=" + Msg
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

    def Encrypt(self,plaintext):
        try:

            padded_key = self.KEY.ljust(self.KEY_SIZE, '\0')
            padded_text = plaintext + (self.BLOCK_SIZE - len(plaintext) % self.BLOCK_SIZE) * '\0'
            r = rijndael.rijndael(padded_key, self.BLOCK_SIZE)
            ciphertext = ''
            for start in range(0, len(padded_text), self.BLOCK_SIZE):
                ciphertext += r.encrypt(padded_text[start:start+self.BLOCK_SIZE])
            encoded = base64.b64encode(ciphertext)
            encoded=encoded.replace("+","%2B")
            return encoded
        except Exception as e:
            print e
            return "-1"

    def Decrypt(self,ciphertext):
        try:
            ciphertext = ciphertext.replace("%2B", "+")
            padded_key = self.KEY.ljust(self.KEY_SIZE, '\0')

            decoded = base64.b64decode(ciphertext)

            r = rijndael.rijndael(padded_key, self.BLOCK_SIZE)

            padded_text = ''
            for start in range(0, len(decoded), self.BLOCK_SIZE):
                padded_text += r.decrypt(decoded[start:start+self.BLOCK_SIZE])

            plaintext = padded_text.split('\x00', 1)[0]

            return plaintext
        except Exception as e:

            return "-1"
    def Responser(self,response,message="",status='blank'):
    
        if status=='blank':
            status = {"status": "blank", "message": "This page is intentionally left blank.","data":[],"statusCode":200}
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(status)  
        elif status=='success':
            
            status = {"status": "success", "message": message,"data":response,"statusCode":200}
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return json.dumps(status)  
        elif status=='failure':
            
            status = {"status": "failed", "message": message,"data":response,"statusCode":200}
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Content-Type', 'application/json')
            return  json.dumps(status)  
        else:
            status = {"status": "error", "message": message,"data":response,"statusCode":500}
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

    def GetBarns(self, OPT='list', value=-1, datatype="S"): #S is single A is array
        try:
            JArray=[]
            JAminities=[]
            if OPT == "single":
                ID=self.Decrypt(value)
                print ID + ":"+ value
                Query="SELECT `barn_id`, `barn_location`, `barn_title`, `barn_poc`, `barn_phone`, `barn_address`, `barn_amenities` FROM `tbl_barn` where `barn_id`='"+ID+"'"
            elif OPT=="list":
                Query="SELECT `barn_id`, `barn_location`, `barn_title`, `barn_poc`, `barn_phone`, `barn_address`, `barn_amenities` FROM `tbl_barn`"
           
            elif OPT=="location":
                Query="SELECT `barn_id`, `barn_location`, `barn_title`, `barn_poc`, `barn_phone`, `barn_address`, `barn_amenities` FROM `tbl_barn` where `barn_location`='"+str(value)+"'"
           


            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    if row['barn_amenities']!="":
                        JAminities=self.GetAminities('closedlist',row['barn_amenities'])
                    
                    JObj={"id":self.Encrypt(str(row['barn_id'])),
                        "location":row['barn_location'],
                        "title":row['barn_title'],
                        "poc":row['barn_poc'],
                        "phone":row['barn_phone'],
                        "address":row['barn_address'],
                        "amenities":JAminities
                        
                        }
                    JArray.append(JObj);
            if OPT=="single":
                return JArray[0]
            else:
                return JArray
        except Exception as e:
            self.PrintException("FN_GetBarns");
            return e

    def GetAminities(self, OPT='list', value=-1, datatype="S"): #S is single A is array
        try:
            JArray=[]
            JResponse=collections.OrderedDict()
            if OPT == "single":
                Query="SELECT `amenities_id`, `amenities_title` FROM `tbl_amenities` WHERE `amenities_id`="+str(value)
            elif OPT=="list":
                Query="SELECT `amenities_id`, `amenities_title` FROM `tbl_amenities`"
            elif OPT=='closedlist':
                if value!='':
                    Query="SELECT `amenities_id`, `amenities_title` FROM `tbl_amenities` where `amenities_id` in ("+str(value)+")"
                    print Query
                else:
                    return []
            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    JObj={"id":self.Encrypt(str(row['amenities_id'])),
                            "title":row['amenities_title'],
                         }
                    JArray.append(JObj);
            if OPT=="single":
                return JArray[0]
            else:
                return JArray
        except Exception as e:
            self.PrintException("FN_GetAminities");
            return e

    def GetClassrooms(self, OPT='list', value=-1, datatype="S"):  # S is single A is array
        try:
            JArray = []
            JAminities = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT `classroom_id`, `barn_id_fk`, `classroom_capacity` FROM `tbl_classroom`  where `classroom_id`='" + ID + "'"
            elif OPT == "list":
                Query = "SELECT `classroom_id`, `barn_id_fk`, `classroom_capacity` FROM `tbl_classroom` "
            elif OPT == "barn":
                ID = self.Decrypt(value)
                Query = " SELECT `classroom_id`, `barn_id_fk`, `classroom_capacity` FROM `tbl_classroom`  where `barn_id_fk`='" + str(
                    ID) + "'"

            elif OPT == "capacity":
                Query = " SELECT `classroom_id`, `barn_id_fk`, `classroom_capacity` FROM `tbl_classroom`  where `classroom_capacity`='" + str(
                    value) + "'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    JObj = {"id": self.Encrypt(str(row['classroom_id'])),
                            "barn": self.GetBarns('single',self.Encrypt(str(row['barn_id_fk']))),
                            "capacity": row['classroom_capacity']
                            }
                    JArray.append(JObj);
            if OPT=="single":
                return JArray[0]
            else:
                return JArray
        except Exception as e:
            self.PrintException("FN_GetBarns");
            return e
    def GetBookingTypes(self, OPT='list', value=-1, datatype="S"): #S is single A is array
        try:
            JArray=[]
            JResponse=collections.OrderedDict()
            if OPT == "single":
                Query="SELECT `bookingtype_id`, `bookingtype_title` FROM `tbl_bookingtype` WHERE `amenities_id`="+str(value)
            elif OPT=="list":
                Query="SELECT `bookingtype_id`, `bookingtype_title` FROM `tbl_bookingtype`"
            elif OPT=='closedlist':
                if value!='':
                    Query="SELECT `bookingtype_id`, `bookingtype_title` FROM `tbl_bookingtype` where `bookingtype_id` in ("+str(value)+")"
                    print Query
                else:
                    return []
            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    JObj={"id":self.Encrypt(str(row['bookingtype_id'])),
                            "title":row['bookingtype_title'],
                         }
                    JArray.append(JObj);
            return JArray
        except Exception as e:
            self.PrintException("FN_GetBookingTypes");
            return e
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
        status = {"status": "Info", "message": "This page is intentionally left blank.","statusCode":200}
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
    def GET(self,barnid):
        try:
            ComFnObj = Commonfunctions()
            user_data = web.input(opt='list',value=-1)
            if barnid:
                user_data.opt='single'
                user_data.value=barnid
            Barns=ComFnObj.GetBarns(user_data.opt,user_data.value)
            return ComFnObj.Responser(Barns,"Barn list","success")
        except Exception as e:
            ComFnObj.PrintException("API_BARN_GET")
            
            return ComFnObj.Responser(str(e.message),"Error in fetching Barn list","error")
    def POST(self):

        try:

            t = db.transaction()
            ComFnObj = Commonfunctions()
            # user_data = json.loads(json_input)
            user_data = web.input(opt=1)
            print user_data.opt
            if  user_data.opt==str(1):
                entries = db.insert('tbl_barn', barn_title=user_data.title, \
                                    barn_location=user_data.location,barn_poc=user_data.poc, \
                                    barn_phone=user_data.phone, barn_address=user_data.address, \
                                   barn_amenities=user_data.amenities)
            elif user_data.opt==str(2):
                entries = db.update('tbl_barn', barn_title=user_data.title, \
                                    barn_location=user_data.location,barn_poc=user_data.poc, \
                                    barn_phone=user_data.phone, barn_address=user_data.address, \
                                   barn_amenities=user_data.amenities, where="barn_id='"+ComFnObj.Decrypt(str(user_data.id))+"'")
            else:
                return ComFnObj.Responser([],"opt must be 1 or 2","failure")    
        except Exception as e:
            t.rollback()
            
            ComFnObj.PrintException("API_BARN_POST")
            return ComFnObj.Responser([],str(e.message),"error")
        else:
            t.commit()
            return ComFnObj.Responser([],"Operation success","success")

class commonlist:
    def GET(self, type):
        try:
            ComFnObj = Commonfunctions()
            user_data = web.input()
            if type == "amenities":
                Jlist = ComFnObj.GetAminities()
            elif type == "booking":
                Jlist = ComFnObj.GetBookingTypes()
            return ComFnObj.Responser(Jlist, type+" list", "success")
        except Exception as e:
            ComFnObj.PrintException("API_BARN_GET")
            return ComFnObj.Responser(str(e.message), "Error in fetching "+type+" list", "error")

    def POST(self, type):

        try:

            t = db.transaction()
            ComFnObj = Commonfunctions()
            # user_data = json.loads(json_input)
            user_data = web.input(opt=1)
            fieldArr={
                "booking":["tbl_bookingtype","bookingtype_id", "bookingtype_title"],
                "amenities": ["tbl_amenities","amenities_id", "amenities_title"]

            }

            if user_data.opt == str(1):
                Query="insert into `"+fieldArr[type][0]+"` (`"+fieldArr[type][2]+"`) values('"+user_data.title+"')"
                entries = db.query(Query)
                #entries = db.insert(fieldArr[type][0], fieldArr[type][2]=user_data.title)

            elif user_data.opt == str(2):
                Query = "update `" + fieldArr[type][0] + "` set `" + fieldArr[type][2] + "`='" + user_data.title + "' where " +fieldArr[type][1]+" = '" + ComFnObj.Decrypt(str(user_data.id)) + "'"
                entries = db.query(Query)
                print entries
                if entries<=0:
                    return ComFnObj.Responser([], "No record updated", "failure")
            else:
                return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
        except Exception as e:
            t.rollback()
            if e[0]==1062:
                message="Title already exist"
            else:
                message=str(e.message)
            ComFnObj.PrintException("API_COMMONLISTING_POST")
            return ComFnObj.Responser([], message, "error")

        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")

class classroom:
    def GET(self,classid):
        try:
            ComFnObj = Commonfunctions()
            user_data = web.input(opt='list', value=-1)
            if classid:
                user_data.opt='single'
                user_data.value=classid
            Classrooms = ComFnObj.GetClassrooms(user_data.opt, user_data.value)
            return ComFnObj.Responser(Classrooms, "Classroom list", "success")
        except Exception as e:
            ComFnObj.PrintException("API_BARN_GET")
            return ComFnObj.Responser(str(e.message), "Error in fetching Barn list", "error")

    def POST(self):

        try:
            t = db.transaction()
            ComFnObj = Commonfunctions()
            # user_data = json.loads(json_input)
            user_data = web.input(opt=1)
            BarnID=ComFnObj.Decrypt(user_data.barn)
            if user_data.opt == str(1):
                entries = db.insert('tbl_classroom', barn_id_fk=BarnID, \
                                    classroom_capacity=user_data.capacity)
            elif user_data.opt == str(2):
                entries = db.update('tbl_classroom', barn_id_fk=BarnID, \
                                    classroom_capacity=user_data.capacity,
                                    where="barn_id='" + ComFnObj.Decrypt(str(user_data.id)) + "'")
            else:
                return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
        except Exception as e:
            t.rollback()

            ComFnObj.PrintException("API_CLASSROOM_POST")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")

class table:
    def GET(self,tableid):
        try:
            ComFnObj = Commonfunctions()
            user_data = web.input(opt='list', value=-1)#barn,location,vacancy
            if tableid:
                user_data.opt='single'
                user_data.value=tableid
            Tables = ComFnObj.GetTables(user_data.opt, user_data.value)
            return ComFnObj.Responser(Tables, "Classroom list", "success")
        except Exception as e:
            ComFnObj.PrintException("API_BARN_GET")
            return ComFnObj.Responser(str(e.message), "Error in fetching Barn list", "error")

    def POST(self):

        try:
            t = db.transaction()
            ComFnObj = Commonfunctions()
            # user_data = json.loads(json_input)
            user_data = web.input(opt=1)
            BarnID=ComFnObj.Decrypt(user_data.barn)
            if user_data.opt == str(1):
                entries = db.insert('tbl_classroom', barn_id_fk=BarnID, \
                                    classroom_capacity=user_data.capacity)
            elif user_data.opt == str(2):
                entries = db.update('tbl_classroom', barn_id_fk=BarnID, \
                                    classroom_capacity=user_data.capacity,
                                    where="barn_id='" + ComFnObj.Decrypt(str(user_data.id)) + "'")
            else:
                return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
        except Exception as e:
            t.rollback()

            ComFnObj.PrintException("API_CLASSROOM_POST")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
else:
    application = web.application(urls, globals()).wsgifunc()