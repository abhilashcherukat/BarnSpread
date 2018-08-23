import hashlib
import json
import smtplib
import datetime
import urllib
import re
import linecache
import sys
import os
import MySQLdb
import collections
import web
import random
import rijndael
import base64
import time
import requests
import urllib2
from Crypto.Cipher import AES

from pyfcm import FCMNotification
from firebase.firebase import FirebaseApplication, FirebaseAuthentication


import juspay as juspay




from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

urls = (
    '/', 'index',
    '/test','test',
    '/barn/(.*)','barn',
    '/commonlist/(.*)','commonlist',
    '/classroom/(.*)','classroom',
    '/table/(.*)', 'table',
    '/chair/(.*)', 'chair',
    '/floor/(.*)', 'floor',
    '/exhibit/(.*)', 'exhibit',
    '/organiser/(.*)', 'organiser',
    '/feestructure/(.*)', 'feestructure',
    '/course/(.*)', 'course',
    '/wishlist', 'wishlist',
    '/enroll/(.*)', 'enroll',
    '/profile/(.*)', 'profile',
    '/profileupdate', 'profile',
    '/event/(.*)', 'event',

    '/autoregister','autoregister',
    '/register', 'register',

    '/autologin', 'autologin',
    '/login', 'login',
    '/fcmtoken','fcmtoken',
    '/notifications','notifications',

    '/counts', 'couts',
    '/shchedule', 'shchedule',
    '/tour', 'tour',
    '/calanderpull','calanderpull',

    '/checkout','checkout',
    '/checkoutconfirm','checkoutconfirm',
    '/checkoutsite','checkoutsite',
    '/checkoutconfirmsite','checkoutconfirmsite',


    '/genpaymentlink','genpaymentlink',

    '/griduser','griduser'





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
        ComFnObj = Commonfunctions()
        user_data=web.input(value=1)
        Res=ComFnObj.SendNotifOnSignal(user_data.to, user_data.msg,user_data.title)
        return ComFnObj.Responser(Res, "","success")

    def GET(self):

        ComFnObj = Commonfunctions()


        Res=ComFnObj.SendNotifOnSignal(user_data.to, user_data.msg,user_data.title)
        return ComFnObj.Responser(Res, "","success")





#FOR REUSABLE FUNCTIONS
class Commonfunctions:

    KEY_SIZE = 16
    BLOCK_SIZE = 32
    KEY="345dsfdf32432SDGGF234dksj4djKJKJ"
    BASEDOC='http://ec2-13-126-133-191.ap-south-1.compute.amazonaws.com/BarnPort'
    BASEURL='http://ec2-13-126-133-191.ap-south-1.compute.amazonaws.com:8080/'
    BASEFOLDER='/var/www/html/BarnPort'
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
            #print exc_obj
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
            mail.login('dev@spread.ooo', 'dev@spread')
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
    def SendNotif(self, To, Msg,Title):
        try:
            push_service = FCMNotification(api_key="AAAAZdwjlrY:APA91bEeCt2WofMRc5EzYAe10xTjSGaWSiVlIGdjGfefPWH9J6FnWUnmePXMcB0cGOG5GUbgKLkb-3TYHpvuS25yqbXPfwAW-bUorJRtY0XxPe-bpZNB3c6ktWiMjPFdtoxQueCmx3Uf")
            registration_id = To
            message_title = Title
            message_body = Msg
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
            return result
        except Exception as e:

            return e
    def SendNotifOnSignal(self, To, Msg,Title):
        try:

            print To
            print To.split(",")
            headers = {'Content-Type': 'application/json',}
            params={"app_id": "83afddaa-785f-4bfc-9bdc-39804fe77c26",
            "include_player_ids": To.split(","),
            "data": {"foo": "bar"},
            "headings": {"en": Title},
            "contents": {"en": Msg}
                      }
            response = requests.post('https://onesignal.com/api/v1/notifications', headers=headers, json=params)
            json_data = json.loads(response.text)
            return json_data
        except Exception as e:
            return e


    def DecryptAES(self,enc=""):
        enc = enc[7:-7]
        return enc

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

            return e
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

            return e

    def Responser(self,response,message="",status='blank'):

        if status=='blank':
            status = {"status": "blank", "message": "This page is intentionally left blank.","data":[],"statusCode":200}
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Access-Control-Allow-Credentials', 'true')
            web.header('Content-Type', 'application/json')
            return  json.dumps(status)
        elif status=='success':
            status = {"status": "success", "message": message,"data":response,"statusCode":200}
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods','*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Access-Control-Allow-Credentials', 'true')
            web.header('Content-Type', 'application/json')
            return json.dumps(status)
        elif status == 'option':
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', 'Authcode')
            web.header('Access-Control-Allow-Credentials', 'true')
            web.header('Content-Type', 'application/json')
        elif status=='failure':

            status = {"status": "failed", "message": message,"data":response,"statusCode":200}
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Access-Control-Allow-Credentials', 'true')
            web.header('Content-Type', 'application/json')
            return  json.dumps(status)
        else:
            status = {"status": "error", "message": message,"data":response,"statusCode":500}
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', '*')
            web.header('Access-Control-Allow-Credentials', 'true')
            web.header('Content-Type', 'application/json')
            return  json.dumps(status)

    def GetCounts(self):#This is for portal dashboard display
        k = "SELECT(" \
            "SELECT COUNT(*) FROM tbl_organiser ) AS org_count,(" \
            "SELECT COUNT(*) FROM tbl_user) AS usr_count FROM dual"
        entries = db.query(k)
        rows = entries.list();
        if rows:
            for row in rows:
                JObj = {"organiser": row['org_count'],
                        "user": row['usr_count'],
                       }

        return JObj
    def GetTokenFromID(self, UserID):
        k = "user_id='" + UserID + "'"
        entries = db.select('tbl_user', what='fcm_token', where=k)
        rows = entries.list();
        if rows:
            return rows[0]['fcm_token']
        else:
            return -1
    def GetIdFromAuth(self, AuthCode):
        k = "user_authcode='" + AuthCode + "'"
        entries = db.select('tbl_user', what='user_id', where=k)
        rows = entries.list();
        if rows:
            return rows[0]['user_id']
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
            k = "user_authcode='" + str(AuthCode) + "'"
            entries = db.select('tbl_user', what='user_id', where=k)
            rows = entries.list();
            if rows:
                return True
            else:
                return False
        except Exception as e:
            return False
    def GenerateOTP(self,Phone,Count=4):
        m = hashlib.md5()
        now = datetime.datetime.now()
        mm = str(now.month)
        ss = str(now.second)
        rd=random.random()*1000
        Gen = str(Phone) + mm + ss+str(rd)
        m.update(Gen)
        Plain = m.hexdigest()
        k = re.findall(r'\d+', Plain)
        return "".join(k)[:Count]



    def GetBarns(self, OPT='list', value=-1,page=1, datatype="S"): #S is single A is array
        try:
            start=int(page) * 5;
            end=5;
            JArray=[]
            JRespo=[]
            JAminities=[]
            if OPT == "single":
                ID=self.Decrypt(value)
                Query="SELECT  0 as totalCount,`barn_id`, `barn_location`, `barn_title`, `barn_poc`, `barn_phone`, `barn_address`, `barn_amenities` FROM `tbl_barn` where `barn_id`='"+ID+"'"
            elif OPT == "limitlist":
                ID = self.Decrypt(value)
                Query = "SELECT  0 as totalCount,`barn_id`, `barn_location`, `barn_title`, `barn_poc`, `barn_phone`, `barn_address`, `barn_amenities` FROM `tbl_barn` where `barn_id`='" + ID + "'"

            elif OPT=="list":
                Query="SELECT totalCount,`barn_id`, `barn_location`, `barn_title`, `barn_poc`, `barn_phone`, `barn_address`, `barn_amenities` FROM `tbl_barn`,(SELECT COUNT(*) totalCount FROM tbl_barn) c limit "+str(start)+","+str(end)
            elif OPT == "combo":
                 Query = "SELECT  0 as totalCount,`barn_id`, `barn_location`, `barn_title`, `barn_poc`, `barn_phone`, `barn_address`, `barn_amenities` FROM `tbl_barn`"
            elif OPT=="location":
                Query="SELECT totalCount,`barn_id`, `barn_location`, `barn_title`, `barn_poc`, `barn_phone`, `barn_address`, `barn_amenities` FROM `tbl_barn`,(SELECT COUNT(*) totalCount FROM tbl_barn where `barn_location`='"+str(value)+"') c where `barn_location`='"+str(value)+"' limit "+str(start)+","+str(end)
            #print Query
            entries = db.query(Query)
            rows = entries.list();
            JCount = 0
            if rows:
                #print rows
                for row in rows:
                    if OPT!="combo" and OPT!='limitlist':
                        if row['barn_amenities']!="":
                            JAminities=self.GetAminities('closedlist',row['barn_amenities'])
                        else:
                            JAminities = []


                        JObj={"id":self.Encrypt(str(row['barn_id'])),
                            "location":row['barn_location'],
                            "title":row['barn_title'],
                            "poc":row['barn_poc'],
                            "phone":row['barn_phone'],
                            "address":row['barn_address'],
                            "amenities":JAminities,
                            "floor":self.GetCount("floor",row['barn_id']),
                            "exhibit":self.GetCount("exhibit",row['barn_id']),
                            "table":self.GetCount("table",row['barn_id']),
                            "classroom":self.GetCount("classroom",row['barn_id'])
                            }
                        JArray.append(JObj);
                    else:
                        JObj = {"id": self.Encrypt(str(row['barn_id'])),
                                "location": row['barn_location'],
                                "title": row['barn_title']
                                }
                        JArray.append(JObj);
                    if row['totalCount']:
                        JCount = row['totalCount']

            if OPT=="single" or OPT=='limitlist':
                return JArray[0]
            elif OPT == "closedlist" or OPT == "combo":
                return JArray
            else:
                JRespo.append({"totalrecords":JCount,'data':JArray})
                return JRespo
        except Exception as e:
            self.PrintException("FN_GetBarns");
            return e
    def GetAminities(self, OPT='list', value=-1,page=1, datatype="S"): #S is single A is array
        try:
            start = int(page) * 25;

            end = 25;
            JArray=[]
            JRespo=[]
            JResponse=collections.OrderedDict()
            if OPT == "single":
                Query="SELECT  0 as totalCount,`amenities_id`, `amenities_title`,`amenities_icon` FROM `tbl_amenities` WHERE `amenities_id`="+str(value)
            elif OPT=="list":
                Query="SELECT `totalCount`,`amenities_id`, `amenities_title`,`amenities_icon` FROM `tbl_amenities`,(SELECT COUNT(*) totalCount FROM tbl_amenities) c limit "+str(start)+","+str(end)
            elif OPT == "combo":
                Query = "SELECT  0 as totalCount,`amenities_id`, `amenities_title`,`amenities_icon` FROM `tbl_amenities`"
            elif OPT=='closedlist':
                if value!='':
                    Query="SELECT 0 as `totalCount`,`amenities_id`, `amenities_title`,`amenities_icon` FROM `tbl_amenities` where `amenities_id` in ("+str(value)+")"

                else:
                    return []
            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    JObj={"id":self.Encrypt(str(row['amenities_id'])),
                            "title":row['amenities_title'],
                            "icon":self.IsFilepresent('amenities',row['amenities_icon']),
                         }
                    JArray.append(JObj);
                    if row['totalCount']:
                        JCount = row['totalCount']

            if OPT=="single":
                return JArray[0]
            elif OPT == "closedlist" or OPT=="combo":
                return JArray
            else:
                JRespo.append({"totalrecords": JCount, 'data': JArray})
                return JRespo
        except Exception as e:
            self.PrintException("FN_GetAminities");
            return e
    def GetWishlist(self, OPT='list', value=-1,page=1, datatype="S"): #S is single A is array
        try:
            start = int(page) * 25;

            end = 25;
            JArrayC=[]
            JArrayE=[]


            JResponse=collections.OrderedDict()

            Query="SELECT `wishlist_id`, `user_id_fk`, `course_id_fk`, `wishlist_type`, `event_id_fk` FROM `tbl_wishlist` WHERE `user_id_fk`="+str(value)
            entries = db.query(Query)
            rows = entries.list();
            if rows:
                for row in rows:
                    if row['wishlist_type']=='COR':
                        JObj={"id":self.Encrypt(str(row['wishlist_id'])),"details":self.GetCourse('single',self.Encrypt(str(row['course_id_fk'])))}
                        JArrayC.append(JObj);

                    if row['wishlist_type']=='EVE':
                        JObj={"id":self.Encrypt(str(row['wishlist_id'])),"details":self.GetEvent('single',self.Encrypt(str(row['event_id_fk'])))}
                        JArrayE.append(JObj);
                return {"course":JArrayC,"event":JArrayE}
        except Exception as e:
            self.PrintException("FN_GetWishlists");
            return e
    def GetClassrooms(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:
            start = int(page) * 25;

            end = 25;
            JArray = []
            JAminities = []
            JCount=0
            JRespo=[]
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT 0 as totalCount,`classroom_id`,`classroom_name`, `barn_id_fk`, `classroom_capacity` FROM `tbl_classroom`  where `classroom_id`='" + ID + "'"
            elif OPT == "list":
                Query = "SELECT totalCount,`classroom_id`,`classroom_name`, `barn_id_fk`, `classroom_capacity` FROM `tbl_classroom`,(select " \
                        "count(*) as totalCount from tbl_classroom)c limit "+str(start)+","+str(end)
            elif OPT == "barn":
                ID = self.Decrypt(value)
                Query = " SELECT totalCount, `classroom_id`,`classroom_name`, `barn_id_fk`, `classroom_capacity` FROM `tbl_classroom` ,(select " \
                        "count(*) as totalCount from tbl_classroom where `barn_id_fk`="+ str(ID) +")c  where `barn_id_fk`='" + str(ID) + "' limit "+str(start)+","+str(end)

            elif OPT == "capacity":
                Query = " SELECT  0 as totalCount, `classroom_id`,`classroom_name`, `barn_id_fk`, `classroom_capacity` FROM `tbl_classroom`  where `classroom_capacity`='" + str(
                    value) + "'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    JObj = {"id": self.Encrypt(str(row['classroom_id'])),
                            "barn": self.GetBarns('limitlist',self.Encrypt(str(row['barn_id_fk']))),
                            "name": row['classroom_name'],
                            "capacity": row['classroom_capacity']
                            }
                    JArray.append(JObj);
                    if row['totalCount']:
                        JCount = row['totalCount']

            if OPT=="single":
                return JArray[0]
            elif OPT == "closedlist" or OPT=="combo":
                return JArray
            else:
                JRespo.append({"totalrecords": JCount, 'data': JArray})
                return JRespo
        except Exception as e:
            self.PrintException("FN_GetClassroom");
            return e
    def GetTables(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:
            start = int(page) * 25;

            end = 25;
            JArray = []
            JAminities = []
            JRespo=[]
            JCount=0
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT 0 as `totalCount`,`table_id`, `table_number`, `barn_id_fk` FROM `tbl_table`  where `table_id`='" + ID + "'"
            elif OPT == "list":
                Query = "SELECT `totalCount`,`table_id`, `table_number`, `barn_id_fk` FROM `tbl_table`,(SELECT COUNT(*) totalCount FROM tbl_table) c limit "+str(start)+","+str(end)
            elif OPT == "barn":
                ID = self.Decrypt(value)
                Query = "SELECT  0 as `totalCount`,`table_id`, `table_number`, `barn_id_fk` FROM `tbl_table`  where `barn_id_fk`='" + str(ID) + "'"
            elif OPT == "number":
                 Query = "SELECT 0 as `totalCount`, `table_id`, `table_number`, `barn_id_fk` FROM `tbl_table`  where `table_number`='" + str(value) + "'"
            elif OPT == "numberbarn": #Table number in barn
                BarnID = self.Decrypt(value[0])
                TableNumber =value[1]
                Query = "SELECT  0 as `totalCount`,`table_id`, `table_number`, `barn_id_fk` FROM `tbl_table`  where `table_number`='" + str(TableNumber) + "' and barn_id_fk='"+str(BarnID)+"'"
                # print Query
            #elif OPT == "capacity":
            #    Query = " SELECT `classroom_id`, `barn_id_fk`, `classroom_capacity` FROM `tbl_classroom`  where `classroom_capacity`='" + str(
            #        value) + "'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    JObj = {"id": self.Encrypt(str(row['table_id'])),
                            "barn": self.GetBarns('limitlist',self.Encrypt(str(row['barn_id_fk']))),
                            "number": row['table_number'],
                            "chair":self.GetChairs('table',self.Encrypt(str(row['table_id']))),
                            }
                    JArray.append(JObj);
                    if row['totalCount']:
                        JCount = row['totalCount']

            if OPT=="single":
                return JArray[0]
            elif OPT == "closedlist" or OPT=="combo":
                return JArray
            else:
                JRespo.append({"totalrecords": JCount, 'data': JArray})
                return JRespo
        except Exception as e:
            self.PrintException("FN_GetTable");
            return e
    def GetChairs(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:
            JArray = []
            JAminities = []
            JRespo=[]
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT 0 as totalCount,`chair_id`, `chair_number`, `table_id_fk` FROM `tbl_chair`  where `chair_id`='" + ID + "'"
            elif OPT == "list":
                Query = "SELECT totalCount,`chair_id`, `chair_number`, `table_id_fk` FROM `tbl_chair`,(SELECT COUNT(*) totalCount FROM tbl_chair) c"
            elif OPT == "table":
                ID = self.Decrypt(value)
                Query = "SELECT   totalCount,`chair_id`, `chair_number`, `table_id_fk` FROM `tbl_chair`,(SELECT COUNT(*) totalCount FROM tbl_chair where `table_id_fk`='" + str(ID) + "') c   where `table_id_fk`='" + str(ID) + "'"
            elif OPT == "number":
                Query = "SELECT   0 as totalCount,`chair_id`, `chair_number`, `table_id_fk` FROM `tbl_chair`  where `chair_number`='" + str(value) + "'"
            elif OPT == "numbertable": #Table number in barn
                TableID = self.Decrypt(value[0])
                ChairNumber =value[1]
                Query = "SELECT  0 as totalCount, `chair_id`, `chair_number`, `table_id_fk` FROM `tbl_chair`  where `chair_number`='" + str(ChairNumber) + "' and table_id_fk='"+str(TableID)+"'"
            #elif OPT == "capacity":
            #    Query = " SELECT `classroom_id`, `barn_id_fk`, `classroom_capacity` FROM `tbl_classroom`  where `classroom_capacity`='" + str(
            #        value) + "'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    JObj = {"id": self.Encrypt(str(row['chair_id'])),
                            #"table": self.GetTables('single',self.Encrypt(str(row['table_id_fk']))),
                            "number": row['chair_number'],
                            "bookinghistory":self.GetChairBookingHistory('single',self.Encrypt(str(row['chair_id'])))
                            }
                    JArray.append(JObj);
                    if row['totalCount']:
                        JCount = row['totalCount']

                if OPT == "single":
                    return JArray[0]
                else:

                    JRespo.append({"totalrecords": JCount, 'data': JArray})
                    return JRespo
            else:
                JRespo.append({"totalrecords": 0, 'data': []})
                return JRespo
        except Exception as e:
            self.PrintException("FN_GetChair");
            return e
    def GetChairBookingHistory(self, OPT='list', value=-1):
        try:
            JArray = []
            JAminities = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT `chairbooking_id`, `chair_id_fk`, DATE(`chairbooking_start_dt`)as start, DATE(`chairbooking_end_dt`)as end FROM `tbl_chairbooking` WHERE `chair_id_fk`='" + str(ID) + "' order by chairbooking_end_dt desc"
            elif OPT == "list":
                ID = self.Decrypt(value)
                Query = "SELECT `chairbooking_id`, `chair_id_fk`, DATE(`chairbooking_start_dt`)as start, DATE(`chairbooking_end_dt`)as end FROM `tbl_chairbooking` WHERE `chairbooking_id`='" + str(ID) + "'  order by chairbooking_end_dt desc"
            entries = db.query(Query)
            rows = entries.list();
            now = datetime.datetime.now()
            if rows:

                for row in rows:
                    #Snows = datetime.datetime.strptime(str(row['start']), '%Y-%m-%d').date()
                    #Enows = datetime.datetime.strptime(str(row['end']), '%Y-%m-%d').date()
                    #if Snows<=now.date() and now.date()<=Enows:
                    #    X="OCC"
                    #else:
                    #    X="VCC"
                    JObj = {"id": self.Encrypt(str(row['chairbooking_id'])),
                            "start": str(row['start']),
                            "end": str(row['end']),
                            "chairid": self.Encrypt(str(row['chair_id_fk'])),
                           }
                    JArray.append(JObj);

                return JArray
        except Exception as e:
            self.PrintException("FN_GetChairBookingHistory");
            return e
    def GetFloors(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:
            start = int(page) * 25;

            end = 25;
            JArray = []
            JCount = 0
            JRespo = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT 0 as totalCount, `floor_id`, `floor_capacity` FROM `tbl_floor`  where `floor_id`='" + ID + "'"
            elif OPT == "list":
                Query = "SELECT totalCount, `floor_id`, `floor_capacity` FROM `tbl_floor`,(select count(*) as totalCount from `tbl_floor`)c limit "+str(start)+","+str(end)
           # elif OPT == "capacity":
          #      Query = " SELECT  `barn_id_fk`, `floor_capacity` FROM `tbl_floor`  where `floor_capacity`='" + str(value) + "'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    JObj = {"id": self.Encrypt(str(row['floor_id'])),
                            "barn": self.GetBarns('limitlist', self.Encrypt(str(row['floor_id']))),
                            "capacity": row['floor_capacity']
                            }
                    JArray.append(JObj);
                    if row['totalCount']:
                        JCount = row['totalCount']

                if OPT == "single":
                    return JArray[0]
                elif OPT == "closedlist" or OPT == "combo":
                    return JArray
                else:
                    JRespo.append({"totalrecords": JCount, 'data': JArray})
                    return JRespo
        except Exception as e:
            self.PrintException("FN_GetFloor");
            return e

    def GetNotification(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:
            start = int(page) * 25;

            end = 25;
            JArray = []
            JCount = 0
            JRespo = []
            if OPT == "list":
                Query = "SELECT totalCount, `notification_id`, `notification_title`, \
                `notification_msg`, `dateofpublish`,`typeofmessage` FROM `tbl_notification`,\
                (select count(*) as totalCount FROM `tbl_notification`)c limit "+str(start)+","+str(end)

            entries = db.query(Query)
            rows = entries.list();
            if rows:
                for row in rows:
                    JObj = {"id": self.Encrypt(str(row['notification_id'])),
                            "title":row['notification_title'],
                            "message":row['notification_msg'],
                            "date":str(row['dateofpublish']),
                            "type":row['typeofmessage']
                            }
                    JArray.append(JObj);
                    if row['totalCount']:
                        JCount = row['totalCount']


                JRespo.append({"totalrecords": JCount, 'data': JArray})
            return JRespo


        except Exception as e:
            self.PrintException("FN_GetFloor");
            return e


    def GetExhibits(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:
            start = int(page) * 25;
            end = 25;
            JArray = []
            JAminities = []
            JCount = 0
            JRespo = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT 0 as totalCount,`exhibit_id`, `barn_id_fk`, `exhibit_capacity` FROM `tbl_exhibit`  where `exhibit_id`='" + ID + "'"
            elif OPT == "list":
                Query = "SELECT totalCount,`exhibit_id`, `barn_id_fk`, `exhibit_capacity` FROM `tbl_exhibit`,(select count(*) as totalCount from `tbl_exhibit`)c limit "+str(start)+","+str(end)
            elif OPT == "barn":
                ID = self.Decrypt(value)
                Query = "SELECT 0 as totalCount,`exhibit_id`, `barn_id_fk`, `exhibit_capacity` FROM `tbl_exhibit`  where `barn_id_fk`='" + str(ID) + "'"

            elif OPT == "capacity":
                Query = " SELECT 0 as totalCount,`exhibit_id`, `barn_id_fk`, `exhibit_capacity` FROM `tbl_exhibit`  where `exhibit_capacity`='" + str(value) + "'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:
                for row in rows:
                    JObj = {"id": self.Encrypt(str(row['exhibit_id'])),
                            "barn": self.GetBarns('limitlist',self.Encrypt(str(row['barn_id_fk']))),
                            "capacity": row['exhibit_capacity']
                            }
                    JArray.append(JObj);
                    if row['totalCount']:
                        JCount = row['totalCount']

            if OPT == "single":
                return JArray[0]
            elif OPT == "closedlist" or OPT == "combo":
                return JArray
            else:
                JRespo.append({"totalrecords": JCount, 'data': JArray})
                return JRespo
        except Exception as e:
            self.PrintException("FN_GetExhibit");
            return e
    def GetBookingTypes(self, OPT='list', value=-1,page=1, datatype="S"): #S is single A is array
        try:
            start = int(page) * 25;

            end = 25;
            JArray=[]
            JResponse=collections.OrderedDict()
            if OPT == "single":
                value = self.Decrypt(str(value))
                Query="SELECT 0 as totalCount,`bookingtype_id`, `bookingtype_title` FROM `tbl_bookingtype` WHERE `bookingtype_id`="+str(value)
            elif OPT=="list":
                Query="SELECT totalCount,`bookingtype_id`, `bookingtype_title` FROM `tbl_bookingtype`,(SELECT COUNT(*) totalCount FROM tbl_bookingtype) c limit "+str(start)+","+str(end)
            #print Query
            entries = db.query(Query)
            rows = entries.list();
            JRespo=[]
            if rows:

                for row in rows:
                    JObj={"id":self.Encrypt(str(row['bookingtype_id'])),
                            "title":row['bookingtype_title'],
                         }
                    JArray.append(JObj);
            if OPT=="single":
                return JArray[0]
            elif OPT == "closedlist" or OPT=="combo":
                return JArray
            else:
                JCount = row['totalCount']
                JRespo.append({"totalrecords": JCount, 'data': JArray})
                return JRespo
        except Exception as e:
            self.PrintException("FN_GetBooking");
            return e

    def GetEventTypes(self, OPT='list', value=-1,page=1, datatype="S"): #S is single A is array
        try:
            start = int(page) * 25;

            end = 25;
            JArray = []
            JResponse = collections.OrderedDict()
            if OPT == "single":
                value = self.Decrypt(str(value))
                Query = "SELECT 0 as totalCount,`eventtype_id`, `eventtype_title` FROM `tbl_eventtype` WHERE `eventtype_id`=" + str(value)
            if OPT == "combo":
                value = self.Decrypt(str(value))
                Query = "SELECT 0 as totalCount,`eventtype_id`, `eventtype_title` FROM `tbl_eventtype`"

            elif OPT == "list":
                Query = "SELECT totalCount,`eventtype_id`, `eventtype_title` FROM `tbl_eventtype`,(SELECT COUNT(*) totalCount FROM tbl_eventtype) c limit " + str(start) + "," + str(end)
            #print Query
            entries = db.query(Query)
            rows = entries.list();
            JRespo = []
            if rows:

                for row in rows:
                    JObj = {"id": self.Encrypt(str(row['eventtype_id'])),
                            "title": row['eventtype_title'],
                            }
                    JArray.append(JObj);
            if OPT == "single":
                return JArray[0]
            elif OPT == "closedlist" or OPT == "combo":
                return JArray
            else:
                JCount = row['totalCount']
                JRespo.append({"totalrecords": JCount, 'data': JArray})
                return JRespo

        except Exception as e:
            self.PrintException("FN_GeteventTypes");
            return e
    def GetOrganiserTypes(self, OPT='list', value=-1,page=1, datatype="S"): #S is single A is array
        try:
            start = int(page) * 25;

            end = 25;
            JArray = []
            JCount=0
            JResponse = collections.OrderedDict()
            if OPT == "single":
                value = self.Decrypt(str(value))
                Query = "SELECT 0 as totalCount,`organisertype_id`, `organisertype_title` FROM `tbl_organisertype` WHERE `organisertype_id`=" + str(
                    value)

            if OPT == "combo":
                value = self.Decrypt(str(value))
                Query = "SELECT 0 as totalCount, `organisertype_id`, `organisertype_title` FROM `tbl_organisertype`"
            elif OPT == "list":
                Query = "SELECT totalCount,`organisertype_id`, `organisertype_title` FROM `tbl_organisertype`,(SELECT COUNT(*) totalCount FROM tbl_organisertype) c limit " + str(
                    start) + "," + str(end)

            entries = db.query(Query)
            rows = entries.list();
            JRespo = []
            if rows:

                for row in rows:
                    JObj = {"id": self.Encrypt(str(row['organisertype_id'])),
                            "title": row['organisertype_title'],
                            }
                    JArray.append(JObj);
                    if row['totalCount']:
                        JCount = row['totalCount']

            if OPT == "single":
                return JArray[0]
            elif OPT == "closedlist" or OPT == "combo":
                return JArray
            else:
                JRespo.append({"totalrecords": JCount, 'data': JArray})
                return JRespo

        except Exception as e:
            self.PrintException("FN_GetOrganiserTypes");
            return e
    def GetCourseTypes(self, OPT='list', value=-1,page=1, datatype="S"): #S is single A is array
        try:
            start = int(page) * 25;

            end = 25;
            JArray = []
            JCount=0
            JResponse = collections.OrderedDict()
            if OPT == "single":
                value = self.Decrypt(str(value))
                Query = "SELECT 0 as totalCount,`coursetype_id`, `coursetype_title` FROM `tbl_coursetype` WHERE `coursetype_id`=" + str(
                    value)
            if OPT == "combo":
                Query = "SELECT 0 as totalCount,`coursetype_id`, `coursetype_title` FROM `tbl_coursetype`"
            elif OPT == "list":
                Query = "SELECT totalCount,`coursetype_id`, `coursetype_title` FROM `tbl_coursetype`,(SELECT COUNT(*) totalCount FROM tbl_coursetype) c limit " + str(start) + "," + str(end)

            entries = db.query(Query)
            rows = entries.list();
            JRespo = []
            if rows:

                for row in rows:
                    JObj = {"id": self.Encrypt(str(row['coursetype_id'])),
                            "title": row['coursetype_title'],
                            }
                    JArray.append(JObj);
                    if row['totalCount']:
                        JCount = row['totalCount']

            if OPT == "single":
                return JArray[0]
            elif OPT == "closedlist" or OPT == "combo":
                return JArray
            else:
                JRespo.append({"totalrecords": JCount, 'data': JArray})
                return JRespo

        except Exception as e:
            self.PrintException("FN_GetOrganiserTypes");
            return e
    def GetTags(self, OPT='list', value=-1,page=1, datatype="S"): #S is single A is array
        try:
            start = int(page) * 25;

            end = 25;
            JArray=[]
            JResponse=collections.OrderedDict()
            if OPT == "single":
                value = self.Decrypt(str(value))
                Query="SELECT 0 as totalCount,`tag_id`, `tag_title` FROM `tbl_tags` WHERE `tag_id`="+str(value)
            elif OPT=="list":
                Query="SELECT totalCount,`tag_id`, `tag_title` FROM `tbl_tags`,(SELECT COUNT(*) totalCount FROM tbl_tags) c limit "+str(start)+","+str(end)
           # print Query
            entries = db.query(Query)
            rows = entries.list();
            JRespo=[]
            if rows:

                for row in rows:
                    JObj={"id":self.Encrypt(str(row['tag_id'])),
                            "title":row['tag_title'],
                         }
                    JArray.append(JObj);
            if OPT=="single":
                return JArray[0]
            elif OPT == "closedlist" or OPT=="combo":
                return JArray
            else:
                JCount = row['totalCount']
                JRespo.append({"totalrecords": JCount, 'data': JArray})
                return JRespo
        except Exception as e:
            self.PrintException("FN_GetTags");
            return e
    def GetTalent(self,value=-1):
        try:
            
           
            JResponse=collections.OrderedDict()
            
            Query="SELECT `user_hashtag`, `user_description`, `user_talent`, `user_worklink`, `user_wanttodo`, `submitedDate` FROM `tbl_grid` WHERE `user_id_fk`="+str(value)
            entries = db.query(Query)
            rows = entries.list();
            
            if rows:

                row=rows[0]
                Talent=row['user_talent'].split(",")
                W=line = row['user_wanttodo'].replace('\r', '')
                W=line = W.replace('\n', '')
                Wanttodo=W.split(",")
                JObj={
                        "hashtag":str(row['user_hashtag']),
                        "hashtag":str(row['user_description']),
                        "talents":Talent,
                        "worklink":str(row['user_worklink']),
                        "user_wanttodo":Wanttodo
                    }
                return JObj
            else:
                return {}
        except Exception as e:
            self.PrintException("FN_GetTalent");
            return e
    def GetOrganisers(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:
            start = int(page) * 25;

            end = 25;
            JRespo=[]
            JArray = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT  0 as totalCount,`organiser_id`, `organisertype_id_fk`, `organiser_name`, `organiser_description`, `organiser_image` FROM `tbl_organiser` where `organiser_id`='" + str(ID) + "'"
            if OPT == "combo":
                ID = self.Decrypt(value)
                Query = "SELECT  0 as totalCount,`organiser_id`, `organisertype_id_fk`, `organiser_name`, `organiser_description`, `organiser_image` FROM `tbl_organiser`"

            elif OPT == "list":
                Query = "SELECT totalCount,`organiser_id`, `organisertype_id_fk`, `organiser_name`, `organiser_description`, `organiser_image` FROM `tbl_organiser` ,(SELECT COUNT(*) totalCount FROM tbl_organiser) c limit "+str(start)+","+str(end)

            elif OPT == "type":
                ID = self.Decrypt(value)
                Query = "SELECT  0 as totalCount,`organiser_id`, `organisertype_id_fk`, `organiser_name`, `organiser_description`, `organiser_image` FROM `tbl_organiser` where `organisertype_id_fk`='" + str(
                    ID) + "'"

            entries = db.query(Query)
            rows = entries.list();
            JCount=0
            if rows:

                for row in rows:
                    OrgId=self.Encrypt(str(row['organiser_id']))
                    JObj = {"id": OrgId,
                            "type": self.GetOrganiserTypes('single',self.Encrypt(str(row['organisertype_id_fk']))),
                            "name": row['organiser_name'],
                            "description": row['organiser_description'],
                            "image": self.IsFilepresent('organiser',row['organiser_image']),
                            }
                    JArray.append(JObj);
                    if row['totalCount']:
                        JCount = row['totalCount']

            if OPT == "single":
                return JArray[0]
            elif OPT == "closedlist" or OPT == "combo":
                return JArray
            else:
                JRespo.append({"totalrecords": JCount, 'data': JArray})
                return JRespo

        except Exception as e:
            self.PrintException("FN_GetOrganiser");
            return e
    def GetFeeStructure(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:
            start = int(page) * 25;

            end = 25;
            JRespo = []
            JArray = []
            JCount = 0
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT 0 as totalCount,`feestructure_id`, `feestructure_title`, `feestructure_fee` FROM `tbl_feestructure`  where `feestructure_id`='" + str(ID) + "'"
            elif OPT == "combo":
                Query = "SELECT 0 as totalCount,`feestructure_id`, `feestructure_title`, `feestructure_fee` FROM `tbl_feestructure`"
            elif OPT == "list":
                Query = "SELECT totalCount,`feestructure_id`, `feestructure_title`, `feestructure_fee` FROM `tbl_feestructure` ,(SELECT COUNT(*) totalCount FROM tbl_feestructure) c limit "+str(start)+","+str(end)

            entries = db.query(Query)
            rows = entries.list();
            if rows:
                for row in rows:
                    FeeId=self.Encrypt(str(row['feestructure_id']))
                    JObj = {"id": FeeId,
                            "title": row['feestructure_title'],
                            "structure": json.loads(row['feestructure_fee'])
                            }
                    JArray.append(JObj)
                    if row['totalCount']:
                        JCount = row['totalCount']

            if OPT == "single":
                return JArray[0]
            elif OPT == "closedlist" or OPT == "combo":
                return JArray
            else:
                JRespo.append({"totalrecords": JCount, 'data': JArray})
                return JRespo

        except Exception as e:
            self.PrintException("FN_GetFeeStructure");
            return e
    def GetCourse(self, OPT='list', value=-1,page=1, datatype="ALL"):  # S is single A is array
        try:
            start = int(page) * 25;

            end = 25;
            JRespo = []
            JArray = []
            JCount=0
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT 0 as totalCount,`course_id`, `course_title`, `course_desc`, `course_duration`, `course_agelimit`, `course_image`, `course_status`," \
                        " `feestructure_id_fk`,organiser_id_fk, `coursetype_id_fk`, `course_tags` FROM `tbl_course` WHERE course_id='" + str(ID) + "'"
            elif OPT == "combo":
                Query = "SELECT 0 as totalCount,`course_id`, `course_title`, `course_desc`, `course_duration`, `course_agelimit`, `course_image`, `course_status`," \
                        " `feestructure_id_fk`,organiser_id_fk, `coursetype_id_fk`, `course_tags` FROM `tbl_course`"
            elif OPT == "list":
                Query = "SELECT totalCount,`course_id`, `course_title`, `course_desc`, `course_duration`, `course_agelimit`, `course_image`," \
                        " `course_status`,organiser_id_fk, `feestructure_id_fk`, `coursetype_id_fk`, `course_tags` FROM `tbl_course`,(SELECT COUNT(*) totalCount FROM tbl_course) c limit "+str(start)+","+str(end)
            elif OPT == "type":
                ID = self.Decrypt(value)
                Query = "SELECT 0 as totalCount,`course_id`, `course_title`, `course_desc`, `course_duration`, `course_agelimit`, " \
                        "`course_image`,organiser_id_fk,  `course_status`,`feestructure_id_fk`, `coursetype_id_fk`, `course_tags` FROM " \
                        "`tbl_course` where `coursetype_id_fk`='" + str(ID) + "'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    CourseId = self.Encrypt(str(row['course_id']))
                    if datatype !='SIMPLE':

                        FeeStructure=self.GetFeeStructure("single", self.Encrypt(str(row['feestructure_id_fk'])))
                        CourseType=self.GetCourseTypes("single", self.Encrypt(str(row['coursetype_id_fk'])))
                        Organiser=self.GetOrganisers("single", self.Encrypt(str(row['organiser_id_fk'])))
                        Locations=self.GetCourseClassMap('course',CourseId)
                        JObj = {"id": CourseId,
                            "title": row['course_title'],
                            "type":CourseType,
                            "fee":FeeStructure,
                            "description":row['course_desc'],
                            "duration":json.loads(row['course_duration']),
                            "agelimit":json.loads(row['course_agelimit']),
                            "image":self.IsFilepresent('course',row['course_image']),
                            "status":row['course_status'],
                            "organiser":Organiser,
                            "tags":row['course_tags'],
                            "venues":Locations
                            }
                    else:
                        Organiser=self.GetOrganisers("single", self.Encrypt(str(row['organiser_id_fk'])))
                        CourseType=self.GetCourseTypes("single", self.Encrypt(str(row['coursetype_id_fk'])))
                        JObj = {"id": CourseId,
                            "title": row['course_title'],
                            "type":CourseType,

                            "description":row['course_desc'],
                            "duration":json.loads(row['course_duration']),
                            "agelimit":json.loads(row['course_agelimit']),
                            "image":self.IsFilepresent('course',row['course_image']),
                            "status":row['course_status'],
                            "organiser":Organiser,
                            "tags":row['course_tags'],
                            }
                    JArray.append(JObj);
                    if row['totalCount']:
                        JCount = row['totalCount']

            if OPT == "single":
                return JArray[0]
            elif OPT == "closedlist" or OPT == "combo":
                return JArray
            else:
                JRespo.append({"totalrecords": JCount, 'data': JArray})
                return JRespo

        except Exception as e:

           self.PrintException("FN_GetCourse");
           return e

    def GetBatch(self, OPT='list', value=-1):  # S is single A is array
        try:


            JArray = []
            JCount=0
            if OPT == "list":
                Query = "SELECT `batch_id`, `batch_code` , `from_date`, `to_date` FROM `tbl_batches` WHERE `classcoursemap_id_fk`="+ str(value) + " order by from_date asc"
            elif OPT=="indates":
                Query="SELECT `batch_id`, `batch_code`, `classcoursemap_id_fk`, `from_date`, `to_date` FROM `tbl_batches` \
                WHERE  `from_date` >=date_add('"+value+"',interval -DAY('"+value+"')+1 DAY) \
                and `from_date` <=date_add('"+value+"',interval -DAY('"+value+"')+DAY(LAST_DAY('"+value+"')) DAY)"
            #THis is for the upcoming batch
            elif OPT=="overflow":
                Query="SELECT `batch_id`, `batch_code`, `classcoursemap_id_fk`, `from_date`, `to_date` FROM `tbl_batches` \
                WHERE  `from_date` >'"+value+"' limit 0,2"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    BatchID = self.Encrypt(str(row['batch_id']))

                    JObj = {"id": BatchID,
                            "BatchCode": row['batch_code'],
                            "From": str(row['from_date']),
                            "enddate": str(row['to_date']),

                            }
                    if OPT=='indates' or OPT=='overflow':
                        JObj["course"]=self.GetCourseFromBatch(row['batch_id'])
                    JArray.append(JObj)
            return JArray


        except Exception as e:
            print e
            self.PrintException("FN_GetBatch");
            return e
    def GetCourseFromBatch(self,value=-1):
        try:
            JArray = []
            JCount=0
            Query="SELECT `batch_id`, `map_id`, `course_id_fk` FROM \
            `tbl_classcoursemap`,`tbl_batches` WHERE `map_id`=`classcoursemap_id_fk` and batch_id="+str(value)

            entries = db.query(Query)
            rows = entries.list();
            if rows:
                for row in rows:
                    return self.GetCourse("single",self.Encrypt(str(row['course_id_fk'])))
        except Exception as e:
            print e
            self.PrintException("FN_GetCourseFromBatch");
            return e

    def GetEnrolledCourse(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:

            JArray = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT `enrolled_id`, `user_id_fk`, `batch_id_fk`, `enrolled_date`, `enrolled_status` FROM `tbl_enrolled` WHERE `enrolled_id`='" + str(ID) + "'"
            elif OPT == "list":
                Query = "SELECT `enrolled_id`, `user_id_fk`, `batch_id_fk`, `enrolled_date`, `enrolled_status` FROM `tbl_enrolled`"
            elif OPT == "user":
                ID = self.Decrypt(value)
                Query = "SELECT `enrolled_id`, `user_id_fk`, `batch_id_fk`, `enrolled_date`, `enrolled_status` FROM `tbl_enrolled` where `user_id_fk`='" + str(ID) + "'"
            elif OPT=="isexist":
                #print value
                userId = self.Decrypt(value[0])
                courseId = self.Decrypt(value[1])

                Query = "SELECT map_id,batch_id,batch_code FROM `tbl_classcoursemap`,`tbl_batches`,`tbl_enrolled` where classcoursemap_id_fk=map_id and batch_id=batch_id_fk and course_id_fk="+ str(courseId) + " and `user_id_fk`=" + str(userId)

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    EnrollId = self.Encrypt(str(row['enrolled_id']))
                    CourseMapId = self.Encrypt(str(row['batch_id_fk']))

                    JObj = {"id": EnrollId,
                            "map": self.GetCourseClassMap("single",CourseMapId),
                            "date": str(row['enrolled_date']),
                            "status":row['enrolled_status']
                        }
                    JArray.append(JObj);
            if OPT == "single":
                return JArray[0]
            else:
                return JArray
        except Exception as e:
            self.PrintException("FN_GetEnrollCourse");
            return e

    def GetProfiles(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:
            JArray = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = " SELECT `user_id`, `user_name`, `user_dob`, `user_phone`, " \
                        "`user_email`, `user_status`,user_image, `isCollective`, `user_authcode` FROM `tbl_user` WHERE user_id='" + str(ID) + "'"
            elif OPT == "list":
                Query = " SELECT `user_id`, `user_name`,user_image, `user_dob`, `user_phone`, `user_email`, `user_status`, `isCollective`, `user_authcode` FROM `tbl_user`"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    UserId = self.Encrypt(str(row['user_id']))


                    JObj = {"id": UserId,
                            "enrolled": self.GetUserCourseAndBatch(row['user_id']),
                            "name": row['user_name'],
                            "griddetails":self.GetTalent(row['user_id']),
                            "phone": row['user_phone'],
                            "email": row['user_email'],
                            "status": row['user_status'],
                            "image": "https://i2.wp.com/ui-avatars.com/api/"+str(row['user_name'])+"/300?ssl=1",
                            "iscollective": row['isCollective'],
                            "DOB":str(row['user_dob'])
                        }
                    JArray.append(JObj);
            if OPT == "single":
                return JArray[0]
            else:
                return JArray
        except Exception as e:
            self.PrintException("FN_GetProfiles");
            return e
    def SetFCMToken(self,Token,Id):
        try:
            entries = db.update('tbl_user',fcm_token=Token,where="user_id="+str(Id))
        except Exception as e:
            self.PrintException("FN_SETFCM")
            return -1
        else:
            return 1

    def SetFirebaseDB(self,Id,value):

        SECRET = 'khkEcEs2TsNsFJ9XaDwJulESuhc2jVELOIkxDo3K'
        DSN = 'https://barnapp-4cc37.firebaseio.com'
        EMAIL = 'abhilash@spread.ooo'
        authentication = FirebaseAuthentication(SECRET,EMAIL)
        fb = FirebaseApplication(DSN, authentication=authentication)
        fb.put('/'+str(Id),"Status",value) #"path","property_Name",property_Value


    def GetCourseClassMap(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:

            JArray = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT `map_id`, `course_id_fk`, `barn_id_fk` FROM `tbl_classcoursemap` WHERE  map_id='" + str(ID) + "'"
            elif OPT == "list":
                Query = "SELECT `map_id`, `course_id_fk`, `barn_id_fk` FROM `tbl_classcoursemap`"
            elif OPT=='getidfromcnb':
                barnId = self.Decrypt(value[0])
                courseId = self.Decrypt(value[1])
                Query = "SELECT `map_id`, `course_id_fk`, `barn_id_fk` FROM `tbl_classcoursemap` WHERE" \
                        " `barn_id_fk`='" + str(barnId) + "' and `course_id_fk`='" + str(courseId) + "'"
            elif OPT=='course':
                courseId = self.Decrypt(value)
                Query = "SELECT `map_id`, `course_id_fk`, `barn_id_fk` FROM `tbl_classcoursemap` WHERE `course_id_fk`='" + str(courseId) + "'"
            entries = db.query(Query)
            rows = entries.list();
            if rows:
                if OPT=='getidfromcnb':
                    return self.Encrypt(str(rows[0]['map_id']))
                for row in rows:
                    CourseId = self.Encrypt(str(row['course_id_fk']))
                    #print row['course_id_fk']
                    BarnId = self.Encrypt(str(row['barn_id_fk']))
                    MapId = self.Encrypt(str(row['map_id']))


                    JObj = {"id":MapId,
                            "barn": self.GetBarns("limitlist",BarnId),
                            "batches":self.GetBatch("list",row['map_id'])
                           }
                    if OPT!='course':
                        JObj["course"]= self.GetCourse("single", CourseId),
                    JArray.append(JObj);
            if OPT == "single" or OPT=="getidfromcnb":
                return JArray[0]
            else:
                return JArray
        except Exception as e:
            self.PrintException("FN_CourseClassMap");
            return e
    def GetEvent(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:
            start = int(page) * 25;

            end = 25;
            JRespo = []
            JArray = []
            JCount=0
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT 0 as totalCount,`event_id`, `event_title`, `event_decscription`, `event_headerImg`, `feestructure_id_fk`, `event_status`, `event_start_date`, `event_end_date`," \
                        " `organiser_id_fk`, `event_venue_id`, `eventtype_id_fk`, `event_tags` FROM `tbl_event` WHERE  event_id='" + str(ID) + "'"
            elif OPT == "list":
                Query = "SELECT totalCount,`event_id`, `event_title`, `event_decscription`, `event_headerImg`, `feestructure_id_fk`, `event_status`, `event_start_date`, `event_end_date`," \
                        " `organiser_id_fk`, `event_venue_id`, `eventtype_id_fk`, `event_tags` FROM `tbl_event` ,(SELECT COUNT(*) totalCount FROM tbl_event) c limit "+str(start)+","+str(end)
            elif OPT == "type":
                ID = self.Decrypt(value)
                Query = "SELECT totalCount,`event_id`, `event_title`, `event_decscription`, `event_headerImg`, `feestructure_id_fk`, `event_status`, `event_start_date`, `event_end_date`, " \
                        "`organiser_id_fk`, `event_venue_id`, `eventtype_id_fk`, `event_tags` FROM `tbl_event`,(SELECT COUNT(*) totalCount FROM tbl_event  WHERE  `eventtype_id_fk`='" + str(ID) + ") c  WHERE  `eventtype_id_fk`='" + str(ID) + "' limit "+str(start)+","+str(end)
            elif OPT == "closedlist":
                Query = "SELECT 0 as totalCount,`event_id`, `event_title`, `event_decscription`, `event_headerImg`, `feestructure_id_fk`, `event_status`, `event_start_date`, `event_end_date`, " \
                        "`organiser_id_fk`, `event_venue_id`, `eventtype_id_fk`, `event_tags` FROM `tbl_event`"
            elif OPT=="indates":
                Query="SELECT 0 as totalCount,`event_id`, `event_title`, `event_decscription`, `event_headerImg`, `feestructure_id_fk`, `event_status`, `event_start_date`, \
                `event_end_date`, `organiser_id_fk`, `event_venue_id`, `eventtype_id_fk`, `event_tags` FROM `tbl_event`\
                 where event_start_date >=date_add('"+value+"',interval -DAY('"+value+"')+1 DAY)\
                 and event_start_date <=date_add('"+value+"',interval -DAY('"+value+"')+DAY(LAST_DAY('"+value+"')) DAY)"
            elif OPT=="overflow":
                Query="SELECT 0 as totalCount,`event_id`, `event_title`, `event_decscription`, `event_headerImg`, `feestructure_id_fk`, `event_status`, `event_start_date`, \
                `event_end_date`, `organiser_id_fk`, `event_venue_id`, `eventtype_id_fk`, `event_tags` FROM `tbl_event`\
                 where event_start_date >='"+value+"' limit 0,2"
            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    EventID = self.Encrypt(str(row['event_id']))
                    FeeStructure = self.GetFeeStructure("single", self.Encrypt(str(row['feestructure_id_fk'])))
                    EventType = self.GetEventTypes("single", self.Encrypt(str(row['eventtype_id_fk'])))
                    Organiser = self.GetOrganisers("single", self.Encrypt(str(row['organiser_id_fk'])))
                    Venue = self.GetBarns("limitlist", self.Encrypt(str(row['event_venue_id'])))

                    JObj = {"id": EventID,
                            "title": row['event_title'],
                            "description": row['event_decscription'],
                            "image": self.IsFilepresent('event',row['event_headerImg']),
                            "fee": FeeStructure,
                            "type": EventType,
                            "status": row['event_status'],
                            "startdate": str(row['event_start_date']),
                            "enddate": str(row['event_end_date']),
                            "organiser":Organiser,
                            "venue":Venue ,
                            "type": EventType,
                            "tags": row['event_tags'],
                            }
                    JArray.append(JObj)
                    if row['totalCount']:
                        JCount = row['totalCount']

            if OPT == "single":
                if len(JArray)>=1:
                    return JArray[0]
                else:
                    return []
            elif OPT == "closedlist" or OPT == "combo" or OPT=='indates':
                return JArray
            else:
                JRespo.append({"totalrecords": JCount, 'data': JArray})
                return JRespo

        except Exception as e:
            self.PrintException("FN_GetCourse");
            return e
    def QueryMaker(self,type,data):
        #print data
        fieldArr = {
            "booking": ["tbl_bookingtype", "bookingtype_id", "bookingtype_title"],
            "amenities": ["tbl_amenities", "amenities_id", "amenities_title","amenities_icon"],
            "tags": ["tbl_tags", "tag_id", "tag_title"],
            "organiser": ["tbl_organisertype", "organisertype_id", "organisertype_title"],
            "event": ["tbl_eventtype", "eventtype_id", "eventtype_title"],
            "course": ["tbl_coursetype", "coursetype_id", "coursetype_title"]
            }

        IStr="insert into "+str(fieldArr[type][0]);
        UStr="update "+str(fieldArr[type][0])+" set ";
        if type=='amenities':

            Files = json.loads(data.icon)
            #print Files
            NewFileName=Files['name']
            if NewFileName!="":
                Salt = "$343dddSS"
                Rnd = random.random()*90000
                String = NewFileName + str(Rnd) + Salt
                m = hashlib.md5()
                m.update(String)
                Random = m.hexdigest()
                NewFileName = str(Random) + "_" + NewFileName
                filecontent = str(Files['content'])
                decoded_string = base64.b64decode(filecontent)
                #print filecontent
                with open('/var/www/html/BarnPort/images/amenities/' + NewFileName, "wb") as fout:
                    fout.write(decoded_string)

            IStr=IStr+" (amenities_title,amenities_icon)values('"+str(data.title)+"','"+str(NewFileName)+"')"
            if NewFileName=="":
                UStr =UStr+" amenities_title='" + str(data.title) + "' where amenities_id=" + str(self.Decrypt(data.id))
            else:
                UStr =UStr+" amenities_title='" + str(data.title) + "',amenities_icon='" + str(NewFileName) + "' where amenities_id=" + str(self.Decrypt(data.id))
        else:

            IStr = IStr + " (`"+fieldArr[type][2] +"`) values('" + str(data.title) + "')"
            UStr = UStr +" `"+fieldArr[type][2]+"`='" + str(data.title) + "' where `"+fieldArr[type][1]+"`=" + str(self.Decrypt(data.id))


        if data.opt==str(2):
            return UStr
        else:
            return IStr

    def DelQueryMaker(self,type):

        # print data
        fieldArr = {
            "booking": ["tbl_bookingtype", "bookingtype_id", "bookingtype_title"],
            "amenities": ["tbl_amenities", "amenities_id", "amenities_title", "amenities_icon"],
            "tags": ["tbl_tags", "tag_id", "tag_title"],
            "organiser": ["tbl_organisertype", "organisertype_id", "organisertype_title"],
            "event": ["tbl_eventtype", "eventtype_id", "eventtype_title"],
            "course": ["tbl_coursetype", "coursetype_id", "coursetype_title"]
        }

        IStr = "delete from " + str(fieldArr[type][0])+ " where "+str(fieldArr[type][1])+"=";
        return IStr

    def GetUserCourseAndBatch(self, value):
        try:

            JArray = []
            Query = "SELECT batch_id_fk,enrolled_date,enrolled_id,classcoursemap_id_fk,batch_code,course_id_fk FROM `tbl_enrolled`,`tbl_batches`,`tbl_classcoursemap` where batch_id=batch_id_fk and map_id=classcoursemap_id_fk and user_id_fk=" +str(value)
            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    CourseId = self.Encrypt(str(row['course_id_fk']))
                    EnrolledId = self.Encrypt(str(row['enrolled_id']))
                    BatchID = self.Encrypt(str(row['batch_id_fk']))



                    JObj = {"id":EnrolledId,
                            "batchid":BatchID,
                            "batchcode":row['batch_code'],
                            "enrolleddate":str(row['enrolled_date']),
                            "course":self.GetCourse("single", CourseId)
                           }

                    JArray.append(JObj);

                return JArray
        except Exception as e:
            self.PrintException("FN_BatchHelper");
            return e

    def GetCount(self, OPT, value=-1):  # S is single A is array
        try:

            JArray = []
            JResponse = collections.OrderedDict()
            if OPT == "classroom":
                Query = "SELECT count(*) as totalCount FROM `tbl_classroom` WHERE `barn_id_fk`=" + str(value)
            elif OPT == "floor":
                Query = "SELECT count(*) as totalCount FROM `tbl_floor` WHERE `floor_id`=" + str(value)
            elif OPT == "exhibit":
                Query = "SELECT count(*) as totalCount FROM `tbl_exhibit` WHERE `barn_id_fk`=" + str(value)
            elif OPT == "table":
                Query = "SELECT count(*) as totalCount FROM `tbl_table` WHERE `barn_id_fk`=" + str(value)
            #print Query
            entries = db.query(Query)
            rows = entries.list();
            if rows:
                for row in rows:
                    Count =row['totalCount']
            else:
                Count=0
            return Count

        except Exception as e:
            self.PrintException("FN_GetCount_"+OPT);
            return e
    def diff(self,first, second):
        second = set(second)
        return [item for item in first if item not in second]
    def GetObjNumber(self,OPT,id):
        if OPT=="table":
      
            Query = "SELECT  `table_number` FROM `tbl_table`  where `barn_id_fk`='" + str(id) + "'"
            entries = db.query(Query)
            rows = entries.list();
            RowArr=[]
            Arr=list(range(1,100))
            print Arr
            print str(type(Arr))+" "+str(type(RowArr))

            if rows:
                
                for row in rows:
                   RowArr.append(int(row['table_number']))
                print RowArr

                X=self.diff(Arr,RowArr)
                return X[0]
            else:
                
                return 1
        elif OPT=="chair":
      
            Query = "SELECT  `chair_number` FROM `tbl_chair`  where `table_id_fk`='" + str(id) + "'"
            entries = db.query(Query)
            rows = entries.list();
            RowArr=[]
            Arr=list(range(1,100))
            print Arr
            print str(type(Arr))+" "+str(type(RowArr))

            if rows:
                
                for row in rows:
                   RowArr.append(int(row['chair_number']))
                print RowArr

                X=self.diff(Arr,RowArr)
                return X[0]
            else:
                
                return 1
    def IsFilepresent(self,OPT,file):

        if OPT=='amenities':
            X=os.path.exists(self.BASEFOLDER+'/images/amenities/'+str(file))
            if X==False or file=='' or file==None:
                return self.BASEDOC+'/images/amenities/placeholder.png'
            else:
                return self.BASEDOC+'/images/amenities/'+str(file)
        elif OPT=='organiser':
            X = os.path.exists(self.BASEFOLDER+'/images/organiser/' + str(file))
            if X==False or file=='':
                return self.BASEDOC+'/images/organiser/placeholder.png'
            else:
                return self.BASEDOC+'/images/organiser/' + str(file)
        elif OPT == 'event':
            X = os.path.exists(self.BASEFOLDER + '/images/event/' + str(file))
            if X==False or file == '':
                return self.BASEDOC + '/images/event/placeholder.png'
            else:
                return self.BASEDOC + '/images/event/' + str(file)
        elif OPT == 'course':
            print "FILE NAME:"+self.BASEFOLDER + '/images/course/' + str(file)
            X = os.path.exists(self.BASEFOLDER + '/images/course/' + str(file))
            print str(X) +  str(file)
            if X==False or file == '':
                return self.BASEDOC + '/images/course/placeholder.png'
            else:
                return self.BASEDOC + '/images/course/' + str(file)
        else:
            print "Last hit"
            return self.BASEDOC + '/images/course/placeholder.png'
    def GetTour(self, OPT='list',value=-1):
            try:

                JArray = []
                Slots = [0,0,0,0]

                if OPT == "list":

                    Query = "SELECT `tourcalander_date`,tourcalander_timeslot,count(*) as Count FROM `tbl_tourcalander` where tourcalander_date='" +str(value)+"' group by tourcalander_timeslot"
                    entries = db.query(Query)
                    rows = entries.list();

                    if rows:

                        for row in rows:

                            if row['Count']<5:
                                Slots[row['tourcalander_timeslot']]=int(row['Count'])
                                JObj = {"date": str(row['tourcalander_date']),"slots": Slots}
                                JArray.append(JObj);


                return Slots
            except Exception as e:
                self.PrintException("FN_GetTour");
                return e



class checkregistration:
    def GET(self):

        ComFnObj = Commonfunctions()
        return ComFnObj.Responser([], "")


    def POST(self):
        ComFnObj = Commonfunctions()
        data = web.input(Phone='')
        #print data
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

                return ComFnObj.Responser(JResponse, "","success")

        except Exception as e:
            return ComFnObj.Responser({}, "Some error happened:"+str(e), "error")
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
class autoregister:

        def GET(self):
            ComFnObj = Commonfunctions()
            return ComFnObj.Responser([],"")


        def POST(self):
            JResponse=collections.OrderedDict();
            try:
                t = db.transaction()
                ComFnObj = Commonfunctions()
                # user_data = json.loads(json_input)
                user_data = web.input(noemail='')
                Salt = "$343dddSS"
                String = user_data.fullname + user_data.email + Salt
                m = hashlib.md5()
                m.update(String)
                Authcode = m.hexdigest()
                password = ComFnObj.GenerateOTP(user_data.phone,8)

                entries = db.insert('tbl_user', user_name=user_data.fullname,user_email=user_data.email,user_password=ComFnObj.Encrypt(password),user_status="JST_RGIST",isCollective=0,user_authcode=Authcode)
                if user_data.noemail != 'NOEMAIL':
                    """Message = "Please verify your phone number using this OTP " + OTP
                    'ComFnObj.SendSMS(user_data.phone, Message)"""
                    render = web.template.render('/var/www/html/')
                    Returner=render.Emailer(user_data.fullname,password,user_data.email)
                    MailBody=Returner['__body__']
                    MailBodyPlain="Registration     Complete"
                    X=ComFnObj.SendMail(user_data.email,"dev@spread.ooo","Welcome to Spread learning",MailBody,MailBodyPlain)

            except MySQLdb.IntegrityError, e:
                t.rollback()
                if e[0]==1062:
                    return ComFnObj.Responser([], "Email address already exist", "error")
                return ComFnObj.Responser([], str(e), "error2")
            except Exception as e:
                t.rollback()
                return ComFnObj.Responser([], "Registration:"+str(e), "error")
            else:
                t.commit()
                return ComFnObj.Responser([], "Registration", "success")
class register:
    def GET(self):
        ComFnObj = Commonfunctions()
        return ComFnObj.Responser([],"")


    def POST(self):
        JResponse=collections.OrderedDict();
        try:
            t = db.transaction()
            ComFnObj = Commonfunctions()
            # user_data = json.loads(json_input)
            user_data = web.input()
            Salt = "$343dddSS"
            String = user_data.fullname + user_data.email + Salt
            m = hashlib.md5()
            m.update(String)
            Authcode = m.hexdigest()
            #OTP = ComFnObj.GenerateOTP(user_data.phone,4)

            entries = db.insert('tbl_user', user_name=user_data.fullname,user_email=user_data.email,user_password=ComFnObj.Encrypt(user_data.password),user_status="JST_RGIST",isCollective=0,user_authcode=Authcode)

            """Message = "Please verify your phone number using this OTP " + OTP
            'ComFnObj.SendSMS(user_data.phone, Message)
            #render = web.template.render('/var/www/html/Templates')
            'render = web.template.render('Templates')
            'USERNAME=user_data.firstname+" "+user_data.lastname
            'Returner=render.Welcome(USERNAME)
            'MailBody=Returner['__body__']
            'MailBodyPlain="Registration Complete"
            'ComFnObj.SendMail(user_data.email,"support@igothelp.com","Welcome to I Got Helps",MailBody,MailBodyPlain)"""

        except MySQLdb.IntegrityError, e:
            t.rollback()
            if e[0]==1062:
                return ComFnObj.Responser([], "Email address already exist", "error")
            return ComFnObj.Responser([], str(e), "error2")
        except Exception as e:
            t.rollback()
            return ComFnObj.Responser([], "Registration:"+str(e), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Registration", "success")

class autologin:
    def GET(self):
        ComFnObj = Commonfunctions()
        return ComFnObj.Responser([], "")


    def POST(self):
        ComFnObj = Commonfunctions()
        user_data = web.input()
        try:
            Query = "SELECT `user_id`, `user_name`, `user_dob`, `user_phone`, `user_email`," \
                    " `user_status`, `isCollective`, `user_authcode` FROM `tbl_user`" \
                    " WHERE  `user_email`='"+user_data.email+"'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                row=rows[0]
                userid=ComFnObj.Encrypt(str(row['user_id']))
                JObj = {"id": userid,
                        "name": row['user_name'],
                        "DOB": row['user_dob'],
                        "phone": row['user_phone'],
                        "email": row['user_email'],
                        "status": row['user_status'],
                        "isCollective": row['isCollective'],
                        "image": "https://i2.wp.com/ui-avatars.com/api/"+str(row['user_name'])+"/300?ssl=1",
                        "authcode": row['user_authcode'],
                        }
                return ComFnObj.Responser(JObj, "User details", "success")
            else:
                return ComFnObj.Responser({}, "Login Failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_LOGIN_GET")
            return ComFnObj.Responser(str(e.message), "Error in login", "error")
class login:
    def OPTIONS(self,X):
        ComFnObj = Commonfunctions()
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self):
        ComFnObj = Commonfunctions()
        return ComFnObj.Responser([], "")


    def POST(self):
        ComFnObj = Commonfunctions()
        user_data = web.input()
        try:
            email=user_data.email.replace("'","")
            Query = "SELECT `user_id`, `user_name`, `user_dob`, `user_phone`, `user_email`," \
                    " `user_status`, `isCollective`, `user_authcode` FROM `tbl_user`" \
                    " WHERE `user_password`='"+ComFnObj.Encrypt(user_data.password)+"' and `user_email`='"+email+"'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                row=rows[0]
                userid=ComFnObj.Encrypt(str(row['user_id']))
                JObj = {"id": userid,
                        "name": row['user_name'],
                        "DOB": str(row['user_dob']),
                        "phone": row['user_phone'],
                        "email": row['user_email'],
                        "status": row['user_status'],
                        "isCollective": row['isCollective'],
                        "image": "https://i2.wp.com/ui-avatars.com/api/"+str(row['user_name'])+"/300?ssl=1",
                        "authcode": row['user_authcode'],
                        }
                return ComFnObj.Responser(JObj, "User details", "success")
            else:
                return ComFnObj.Responser({}, "Login Failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_LOGIN_GET")
            return ComFnObj.Responser(str(e.message), "Error in login", "error")
class barn:
    def OPTIONS(self,X):
        ComFnObj = Commonfunctions()
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self,barnid):
        try:
            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                user_data = web.input(opt='list',value=-1,page=1)
                user_data.page = int(user_data.page) -1
                if barnid:
                    user_data.opt='single'
                    user_data.value=barnid
                Barns=ComFnObj.GetBarns(user_data.opt,user_data.value,user_data.page)
                return ComFnObj.Responser(Barns,"Barn list","success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_BARN_GET")
            return ComFnObj.Responser(str(e.message),"Error in fetching Barn list","error")
    def POST(self,barnid=-1):

        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')

            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                # user_data = json.loads(json_input)
                user_data = web.input(opt=1)
                #print user_data
                if  user_data.opt==str(1):
                    user_data.amenities = json.loads(user_data.amenities)
                    amen=[]
                    #print user_data.amenities
                    for amenitits in user_data.amenities:
                        amen.append(ComFnObj.Decrypt(amenitits))
                    entries = db.insert('tbl_barn', barn_title=user_data.title, \
                                        barn_location=user_data.location,barn_poc=user_data.poc, \
                                        barn_phone=user_data.phone, barn_address=user_data.address, \
                                       barn_amenities=','.join(amen))

                elif user_data.opt==str(2):
                    amen = []
                    user_data.amenities = json.loads(user_data.amenities)
                    #print user_data.amenities
                    if user_data.amenities != None:
                        for amenitits in user_data.amenities:
                            #print amenitits
                            amen.append(ComFnObj.Decrypt(amenitits))
                    entries = db.update('tbl_barn', barn_title=user_data.title, \
                                        barn_location=user_data.location,barn_poc=user_data.poc, \
                                        barn_phone=user_data.phone, barn_address=user_data.address, \
                                       barn_amenities=','.join(amen), where="barn_id='"+ComFnObj.Decrypt(str(barnid))+"'")
                else:
                    return ComFnObj.Responser([],"opt must be 1 or 2","failure")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            if e[0]==1062:
                message="Title already exist"
            else:
                message=str(e)
            ComFnObj.PrintException("API_BARN_POST")
            return ComFnObj.Responser([], message, "error")

        else:
            t.commit()
            #print entries
            return ComFnObj.Responser(ComFnObj.Encrypt(str(entries)),"Operation success","success")
    def DELETE(self,delid):
        try:
            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                db.query("delete from tbl_barn where barn_id="+str(ComFnObj.Decrypt(delid)))
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_BARN_DEL")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
class commonlist:
    def OPTIONS(self,X):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self, type):
        try:
            Jlist=[]
            ComFnObj = Commonfunctions()
            user_data = web.input(id=-1, page=1,opt='list')
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):

                user_data.page = int(user_data.page) -1
                if type == "amenities":
                    if user_data.id!=-1:
                        Jlist = ComFnObj.GetAminities("single",ComFnObj.Decrypt(user_data.id))
                    else:
                        Jlist = ComFnObj.GetAminities(user_data.opt,-1,user_data.page)
                elif type == "booking":
                    if user_data.id!=-1:
                        Jlist = ComFnObj.GetBookingTypes("single",user_data.id)
                    else:
                        Jlist = ComFnObj.GetBookingTypes(user_data.opt,-1,user_data.page)
                elif type == "tags":
                    if user_data.id!=-1:
                        Jlist = ComFnObj.GetTags("single",user_data.id)
                    else:
                        Jlist = ComFnObj.GetTags(user_data.opt,-1,user_data.page)
                elif type == "event":
                    if user_data.id!=-1:
                        Jlist = ComFnObj.GetEventTypes("single",user_data.id)
                    else:
                        Jlist = ComFnObj.GetEventTypes(user_data.opt,-1,user_data.page)
                elif type == "organiser":
                    if user_data.id!=-1:
                        Jlist = ComFnObj.GetOrganiserTypes("single",user_data.id)
                    else:
                        Jlist = ComFnObj.GetOrganiserTypes(user_data.opt,-1,user_data.page)
                elif type == "course":
                    if user_data.id!=-1:
                        Jlist = ComFnObj.GetCourseTypes("single",user_data.id)
                    else:
                        Jlist = ComFnObj.GetCourseTypes(user_data.opt,-1,user_data.page)
                return ComFnObj.Responser(Jlist, type+" list", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_COMMONLIST_GET")
            return ComFnObj.Responser(str(e.message), "Error in fetching "+type+" list", "error")

    def POST(self, type):

        try:
            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                user_data = web.input(opt=1,_unicode=False)
                Query = ComFnObj.QueryMaker(type, user_data)
                if user_data.opt != str(1) and  user_data.opt != str(2):
                   return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
                entries=db.query(Query)
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            if e[0]==1062:
                message="Title already exist"
            else:
                message=str(e)
            ComFnObj.PrintException("API_COMMONLISTING_POST")
            return ComFnObj.Responser([], message, "error")

        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
    def DELETE(self,type):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            user_data = web.input(id=-1)
            Authcode = header.get('HTTP_AUTHCODE')

            if ComFnObj.CheckAuth(Authcode):
                delid=ComFnObj.Decrypt(user_data.id)
                Query=ComFnObj.DelQueryMaker(type)
                Query=Query+str(delid)
                db.query(Query)
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:

            ComFnObj.PrintException("API_COMMONLIST_DEL")
            return ComFnObj.Responser([], str(e.message), "error")
        else:

            return ComFnObj.Responser([], "Operation success", "success")
class classroom:
    def OPTIONS(self,X):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self,classid):
        try:
            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                user_data = web.input(opt='list', value=-1, page=1)
                user_data.page=int(user_data.page)-1
                if classid:
                    user_data.opt='single'
                    user_data.value=classid
                Classrooms = ComFnObj.GetClassrooms(user_data.opt, user_data.value,user_data.page)
                return ComFnObj.Responser(Classrooms, "Classroom list", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_CLASSROOM_GET")
            return ComFnObj.Responser(str(e.message), "Error in fetching Barn list", "error")

    def POST(self,classid):

        try:
            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                # user_data = json.loads(json_input)
                user_data = web.input(opt=1,name=-1)
                BarnID=ComFnObj.Decrypt(user_data.barn)
                if user_data.name==-1:
                    DummyNames = ["Besit", "bests", "Betid", "betis", "bider", "bides", "Bidet", "biers", "birde", "birds",
                             "Birse",
                             "bises", "biset", "bited", "Biter",
                             "bites", "bredi", "Brest", "bride", "bries", "brise", "briss", "brist", "Brite", "brits",
                             "btise",
                             "debit", "debts", "deist", "diets",
                             "dirts", "distr", "diter", "dites", "dress", "drest", "dribs", "dries", "edits", "idest",
                             "iters",
                             "rebid", "reist", "resid", "resit",
                             "rests", "ribes", "rides", "rises", "Risse", "rites", "sesti", "Sider", "sides", "siest",
                             "sired",
                             "sires", "Siser", "sited", "sites",
                             "steid", "steri", "stied", "Sties", "stire", "stirs", "Strid", "tiber", "tides", "tiers",
                             "tired",
                             "tires", "Tress", "Tribe", "Tride",
                             "Tried", "tries"]
                    m = hashlib.md5()
                    now = datetime.datetime.now()
                    mm = str(now.month)
                    ss = str(now.second)
                    rd = random.random() * 90000
                    Gen = mm + ss + str(rd)
                    m.update(Gen)
                    Plain = m.hexdigest()
                    k = re.findall(r'\d+', Plain)

                    R = "".join(k)[:2]
                    L = int(R) % 80
                    DummyName = DummyNames[int(L)]
                else:
                    DummyName=user_data.name
                if user_data.opt == str(1):
                    entries = db.insert('tbl_classroom', barn_id_fk=BarnID, \
                                        classroom_name=DummyName,classroom_capacity=user_data.capacity)
                elif user_data.opt == str(2):
                    entries = db.update('tbl_classroom', barn_id_fk=BarnID, \
                                        classroom_name=DummyName,classroom_capacity=user_data.capacity,
                                        where="classroom_id='" + ComFnObj.Decrypt(str(classid)) + "'")
                else:
                    return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()

            ComFnObj.PrintException("API_CLASSROOM_POST")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
    def DELETE(self,delid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                db.query("delete from tbl_classroom where classroom_id="+str(ComFnObj.Decrypt(delid)))
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_CLASS_DEL")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
class table:
    def OPTIONS(self,X):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self,tableid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):

                user_data = web.input( page=1,opt='list', value=-1)#barn,location,vacancy
                user_data.page = int(user_data.page) - 1
                if tableid:
                    user_data.opt='single'
                    user_data.value=tableid
                Tables = ComFnObj.GetTables(user_data.opt, user_data.value,user_data.page)
                #print Tables
                return ComFnObj.Responser(Tables, "Table list", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_TABLE_GET")
            return ComFnObj.Responser(str(e.message), "Error in fetching table list", "error")

    def POST(self,tableid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                # user_data = json.loads(json_input)
                user_data = web.input(opt=1)
                BarnID = ComFnObj.Decrypt(str(user_data.barn))
                TableData=ComFnObj.GetObjNumber('table',BarnID)
                print TableData
                if user_data.opt == str(1):

                    entries = db.insert('tbl_table', barn_id_fk=BarnID, \
                                            table_number=TableData)
                elif user_data.opt == str(2):

                    entries = db.update('tbl_table', barn_id_fk=BarnID, \
                                            table_number=TableData,
                                            where="table_id='" + ComFnObj.Decrypt(str(user_data.id)) + "'")
                else:
                    return ComFnObj.Responser([], "opt must be 1 or 2", "failure")

            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()

            ComFnObj.PrintException("API_TABLE_POST")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
    def DELETE(self,delid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                db.query("delete from tbl_table where table_id="+str(ComFnObj.Decrypt(delid)))
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_EVENT_POST")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
class chair:
    def OPTIONS(self,X):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self,chairid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):

                user_data = web.input(opt='list', value=-1)#barn,location,vacancy
                if chairid:
                    user_data.opt='single'
                    user_data.value=chairid
                Chairs = ComFnObj.GetChairs(user_data.opt, user_data.value)
                return ComFnObj.Responser(Chairs, "Chair list", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_TABLE_GET")
            return ComFnObj.Responser(str(e.message), "Error in fetching chair list", "error")

    def POST(self,chairid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                user_data = web.input(opt=1)
                TableID = ComFnObj.Decrypt(user_data.table)
                if user_data.opt == str(1):
                    ChairNumber=ComFnObj.GetObjNumber('chair',TableID)
                    Query="INSERT INTO `tbl_chair` (`chair_number`, `table_id_fk`) VALUES("+str(ChairNumber)+"," +str(TableID) +")"
                    entries=db.query(Query)
                    #entries = db.insert('tbl_chair', table_id_fk=TableID,chair_number=user_data.number)
                elif user_data.opt == str(2):
                    ChairData = ComFnObj.GetChairs('numbertable', [user_data.table, user_data.number])
                    if len(ChairData) == 0:
                        entries = db.update('tbl_chair', table_id_fk=TableID, \
                                        chair_number=user_data.number,
                                        where="table_id='" + ComFnObj.Decrypt(str(user_data.id)) + "'")
                    else:
                        return ComFnObj.Responser([], "Same chair number exist in the table", "failure")
                else:
                    return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()

            ComFnObj.PrintException("API_CHAIR_POST")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
    def DELETE(self,delid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                db.query("delete tbl_chair from chair_id"+str(ComFnObj.Decrypt(delid)))
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_CHAIR_DEL")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")

class couts:
    def GET(self):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):

                Chairs = ComFnObj.GetCounts()
                return ComFnObj.Responser(Chairs, "Counts", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_COUNT_GET")
            return ComFnObj.Responser(str(e.message), "Error in fetching chair list", "error")

class tour:
    def OPTIONS(self,X):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                user_data = web.input(opt='list', value=-1)

                TourSlots = ComFnObj.GetTour(user_data.opt, user_data.value)
                return ComFnObj.Responser(TourSlots, "Tour Slots", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_TOURSLOTS_GET")
            return ComFnObj.Responser(str(e.message), "Error in fetching floor list", "error")

    def POST(self):

        try:
            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                user_data = web.input(opt=1)

                if user_data.opt == str(1):
                    entries = db.insert('tbl_tourcalander', tourcalander_date=user_data.tourdate, \
                                        tourcalander_timeslot=user_data.timeslot, \
                                        guest_name=user_data.name,guest_phone=user_data.phone,\
                                        guest_email=user_data.email,tourcalander_status="REQST")

                else:
                    return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_FLOOR_POST")
            if e[0]==1062:
                return ComFnObj.Responser([], "Barn can only have one floor", "error")
            else:
                return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
    """def DELETE(self,delid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                db.query("delete from tbl_floor where floor_id="+str(ComFnObj.Decrypt(delid)))
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_EVENT_POST")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")"""


class floor:
    def OPTIONS(self,X):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self,floorid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                user_data = web.input(opt='list', value=-1,page=1)
                user_data.page=int(user_data.page)-1
                if floorid:
                    user_data.opt='single'
                    user_data.value=floorid
                Floors = ComFnObj.GetFloors(user_data.opt, user_data.value,user_data.page)
                return ComFnObj.Responser(Floors, "Floor list", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_FLOOR_GET")
            return ComFnObj.Responser(str(e.message), "Error in fetching floor list", "error")

    def POST(self,floorid):

        try:
            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                user_data = web.input(opt=1)
                BarnID=ComFnObj.Decrypt(user_data.barn)
                if user_data.opt == str(1):
                    entries = db.insert('tbl_floor', floor_id=BarnID, \
                                        floor_capacity=user_data.capacity)
                elif user_data.opt == str(2):
                    entries = db.update('tbl_floor', floor_id=BarnID, \
                                        floor_capacity=user_data.capacity,
                                        where="floor_id='" + ComFnObj.Decrypt(str(floorid)) + "'")
                else:
                    return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_FLOOR_POST")
            if e[0]==1062:
                return ComFnObj.Responser([], "Barn can only have one floor", "error")
            else:
                return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
    def DELETE(self,delid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                db.query("delete from tbl_floor where floor_id="+str(ComFnObj.Decrypt(delid)))
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_EVENT_POST")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
class exhibit:
    def OPTIONS(self,X):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self,exhibitid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                user_data = web.input(opt='list', value=-1,page=1)
                user_data.page=int(user_data.page)-1
                if exhibitid:
                    user_data.opt='single'
                    user_data.value=exhibitid
                Exhibits = ComFnObj.GetExhibits(user_data.opt, user_data.value,user_data.page)
                return ComFnObj.Responser(Exhibits, "Exhibit list", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_EXHIBIT_GET")
            return ComFnObj.Responser(str(e.message), "Error in fetching Barn list", "error")

    def POST(self,exhibitid):

        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                user_data = web.input(opt=1)
                BarnID=ComFnObj.Decrypt(user_data.barn)
                if user_data.opt == str(1):
                    entries = db.insert('tbl_exhibit', barn_id_fk=BarnID, \
                                        exhibit_capacity=user_data.capacity)
                elif user_data.opt == str(2):
                    entries = db.update('tbl_exhibit', barn_id_fk=BarnID, \
                                        exhibit_capacity=user_data.capacity,
                                        where="exhibit_id='" + ComFnObj.Decrypt(str(exhibitid)) + "'")
                else:
                    return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()

            ComFnObj.PrintException("API_EXHIBIT_POST")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
    def DELETE(self,delid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                db.query("delete from tbl_exhibit where exhibit_id="+str(ComFnObj.Decrypt(delid)))
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_EXHIBIT_DEL")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
class organiser:
    def OPTIONS(self,X):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self, organiserid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):

                user_data = web.input(opt='list', value=-1,page=1,_unicode=False)
                if organiserid:
                    user_data.opt = 'single'
                    user_data.value = organiserid
                user_data.page=int(user_data.page)-1
                Organiser = ComFnObj.GetOrganisers(user_data.opt, user_data.value,user_data.page)
                return ComFnObj.Responser(Organiser, "Organiser list", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_ORGANISER_GET")

            return ComFnObj.Responser(str(e.message), "Error in fetching Organiser list", "error")

    def POST(self,organiserid):

        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                user_data = web.input(opt=1)
                user_data.type=ComFnObj.Decrypt(user_data.type)
                #print user_data.type
                if user_data.opt == str(1):
                    Files = json.loads(user_data.image)
                    # print Files
                    NewFileName = Files['name']
                    if NewFileName != "":
                        Salt = "$343dddSS"
                        Rnd = random.random() * 90000
                        String = NewFileName + str(Rnd) + Salt
                        m = hashlib.md5()
                        m.update(String)
                        Random = m.hexdigest()
                        NewFileName = str(Random) + "_" + NewFileName
                        filecontent = str(Files['content'])
                        decoded_string = base64.b64decode(filecontent)
                        # print filecontent
                        with open('/var/www/html/BarnPort/images/organiser/' + NewFileName, "wb") as fout:
                            fout.write(decoded_string)

                    entries = db.insert('tbl_organiser', organisertype_id_fk=user_data.type,organiser_name=user_data.name,\
                                        organiser_description=user_data.description,\
                                        organiser_image=NewFileName)
                elif user_data.opt == str(2):
                        Files = json.loads(user_data.image)
                        NewFileName = Files['name']
                        if NewFileName != "":
                            Salt = "$343dddSS"
                            Rnd = random.random() * 90000
                            String = NewFileName + str(Rnd) + Salt
                            m = hashlib.md5()
                            m.update(String)
                            Random = m.hexdigest()
                            NewFileName = str(Random) + "_" + NewFileName
                            filecontent = str(Files['content'])
                            decoded_string = base64.b64decode(filecontent)
                            # print filecontent
                            with open('/var/www/html/BarnPort/images/organiser/' + NewFileName, "wb") as fout:
                                fout.write(decoded_string)

                        entries = db.update('tbl_organiser', organisertype_id_fk=user_data.type,organiser_name=user_data.name,\
                                        organiser_description=user_data.description,\
                                        organiser_image=NewFileName,
                                        where="organiser_id='" + ComFnObj.Decrypt(str(user_data.id)) + "'")
                else:
                    return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_ORGANISER_POST")

            if e[0]==1452:
                return ComFnObj.Responser([], "Organiser type not in list", "error")
            else:
                return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
    def DELETE(self,delid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                db.query("delete from tbl_organiser where organiser_id="+str(ComFnObj.Decrypt(delid)))
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_EVENT_POST")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
class feestructure:
    def OPTIONS(self,X):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self, feestructureid):
        try:
            ComFnObj = Commonfunctions()
            user_data = web.input(opt='list', value=-1,page=1)
            if feestructureid:
                user_data.value = feestructureid
                user_data.opt='single'
            user_data.page = int(user_data.page) - 1
            FeeStructure = ComFnObj.GetFeeStructure(user_data.opt, user_data.value,user_data.page)
            return ComFnObj.Responser(FeeStructure, "Fee structure", "success")
        except Exception as e:
            ComFnObj.PrintException("API_FEESTRUCTURE_GET")

            return ComFnObj.Responser(str(e.message), "Error in fetching fee structure list", "error")

    def POST(self,feestructureid):

        try:

            t = db.transaction()
            ComFnObj = Commonfunctions()
            # user_data = json.loads(json_input)

            user_data = web.input(opt=1)
            #print json.loads(user_data.structure)
            if user_data.opt == str(1):
                entries = db.insert('tbl_feestructure', feestructure_title=user_data.title,feestructure_fee=user_data.structure)
            elif user_data.opt == str(2):
                if feestructureid:
                    user_data.id=feestructureid
                entries = db.update('tbl_feestructure', feestructure_title=user_data.title,feestructure_fee=user_data.structure,where="feestructure_id='" + ComFnObj.Decrypt(str(user_data.id)) + "'")
            else:
                return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_FEESTRUCTURE_POST")

            if e[0]==1062:
                return ComFnObj.Responser([], "Title already exist", "error")
            else:
                return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
    def DELETE(self,delid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                db.query("delete from tbl_feestructure where feestructure_id="+str(ComFnObj.Decrypt(delid)))
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_FEE_DEL")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
class course:
    def OPTIONS(self,X):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self, courseid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                user_data = web.input(opt='list', value=-1,page=1)
                user_data.page=int(user_data.page)-1
                #print user_data.page
                if courseid:
                    user_data.value = courseid
                    user_data.opt='single'
                Course = ComFnObj.GetCourse(user_data.opt, user_data.value,user_data.page)

                return ComFnObj.Responser(Course, "Course", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_COURSE_GET")

            return ComFnObj.Responser(str(e.message), "Error in course structure list", "error")

    def POST(self,courseid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                user_data = web.input(opt=1)
                user_data.feestructure = ComFnObj.Decrypt(str(user_data.feestructure))
                user_data.coursetype = ComFnObj.Decrypt(str(user_data.coursetype))
                user_data.organiser = ComFnObj.Decrypt(str(user_data.organiser))
                Files = json.loads(user_data.image)
                # print Files
                NewFileName = Files['name']
                if NewFileName != "":
                    Salt = "$343dddSS"
                    Rnd = random.random() * 90000
                    String = NewFileName + str(Rnd) + Salt
                    m = hashlib.md5()
                    m.update(String)
                    Random = m.hexdigest()
                    NewFileName = str(Random) + "_" + NewFileName.replace(" ", "")
                    filecontent = str(Files['content'])
                    decoded_string = base64.b64decode(filecontent)
                    # print filecontent
                    with open('/var/www/html/BarnPort/images/course/' + NewFileName, "wb") as fout:
                        fout.write(decoded_string)
                if user_data.opt == str(1):

                    entries = db.insert('tbl_course', course_title=user_data.title,course_desc=user_data.description,
                    course_duration=user_data.duration,course_agelimit=user_data.agelimit,
                    course_image=NewFileName,course_status=user_data.status,feestructure_id_fk=user_data.feestructure,
                    coursetype_id_fk=user_data.coursetype,course_tags=user_data.tags,organiser_id_fk=user_data.organiser)

                    locations=json.loads(user_data.location)
                    for location in locations:
                        db.insert('tbl_classcoursemap',course_id_fk=entries,barn_id_fk=ComFnObj.Decrypt(location))

                elif user_data.opt == str(2):
                    if courseid:
                        user_data.id = ComFnObj.Decrypt(courseid)

                        entries = db.update('tbl_course',course_title=user_data.title,course_desc=user_data.description,
                                            course_duration=user_data.duration,course_agelimit=user_data.agelimit,
                                            course_image=NewFileName,course_status=user_data.status,feestructure_id_fk=user_data.feestructure
                                            ,organiser_id_fk=user_data.organiser,coursetype_id_fk=user_data.coursetype,course_tags=user_data.tags,where="course_id='" + user_data.id + "'")
                        Query="delete from tbl_classcoursemap where course_id_fk="+user_data.id
                        db.query(Query)
                        locations = json.loads(user_data.location)
                        for location in locations:
                            #print str(location)+":"+str(ComFnObj.Decrypt(location))
                            db.insert('tbl_classcoursemap', course_id_fk=user_data.id, barn_id_fk=ComFnObj.Decrypt(location))
                else:
                    return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_COURSE_POST")

            if e[0]==1062:
                return ComFnObj.Responser([], "Title already exist", "error")
            else:
                return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
    def DELETE(self,delid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                db.query("delete from tbl_course where course_id="+str(ComFnObj.Decrypt(delid)))
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_COURSE_POST")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
class enroll:
    def OPTIONS(self,X):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self, courseid):
        try:
            ComFnObj = Commonfunctions()
            return ComFnObj.Responser([], "", "blank")
        except:
            return ComFnObj.Responser([], "", "blank")

    def POST(self,courseid):
        ComFnObj = Commonfunctions()
        try:

            if courseid=="":
                raise ValueError('Course ID not found')
            else:
                courseid2=ComFnObj.Decrypt(courseid)
                header = web.ctx.environ
                Authcode = header.get('HTTP_AUTHCODE')
                if ComFnObj.CheckAuth(Authcode):
                    t = db.transaction()
                    user_data = web.input(opt=1)
                    userid=ComFnObj.GetIdFromAuth(Authcode)
                    #print userid
                    if user_data.opt == str(1):
                        if ComFnObj.GetEnrolledCourse("isexist",[ComFnObj.Encrypt(str(userid)),courseid]):
                            raise ValueError("Already enrolled")

                        MapID=ComFnObj.Decrypt(str(user_data.batchid))
                        entries = db.insert('tbl_enrolled',user_id_fk=userid,batch_id_fk=MapID,enrolled_status="STATUS")
                    elif user_data.opt == str(2):
                        MapID = ComFnObj.Decrypt(str(user_data.batchid))
                        entries = db.update('tbl_enrolled',user_id_fk=userid,batch_id_fk=MapID,enrolled_status=user_data.status,
                                            where="enrolled_id='" + ComFnObj.Decrypt(str(user_data.id)) + "'")
                    else:
                        return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
                else:
                    return ComFnObj.Responser([], "Authcode failed", "failure")
        except ValueError as e:
            ComFnObj.PrintException("API_ENROLLED_POST")
            return ComFnObj.Responser([], str(e), "error")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_ENROLLED_POST")

            if e[0]==1452:
                return ComFnObj.Responser([], "Course not in list", "error")
            else:
                return ComFnObj.Responser([], str(e), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")

class profile:
    def OPTIONS(self,X):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self,profileid):
        try:
            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                user_data = web.input(opt='list', value=-1)
                if profileid:
                    user_data.opt='single'
                    user_data.value=profileid

                    Profiles = ComFnObj.GetProfiles(user_data.opt, user_data.value)

                    return ComFnObj.Responser(Profiles, "Profile list", "success")
                else:
                    return ComFnObj.Responser([], "Profile ID not sent", "failure")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_PROFILE_GET")
            return ComFnObj.Responser(str(e.message), "Error in fetching profile list", "error")

    def POST(self):

        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                # user_data = json.loads(json_input)
                user_data = web.input(opt=1)
                userID=ComFnObj.GetIdFromAuth(Authcode)
                if user_data.opt == "name":
                    entries = db.update('tbl_user',
                                        user_name=user_data.value,
                                        where="user_id="+str(userID))
                elif user_data.opt == "phone":
                    entries = db.update('tbl_user',
                                        user_phone=user_data.value,
                                        where="user_id="+str(userID))
                elif user_data.opt == "email":
                    entries = db.update('tbl_user',
                                        user_email=user_data.value,
                                        where="user_id="+str(userID))
                elif user_data.opt == "password":
                    entries = db.update('tbl_user',
                                        user_password=ComFnObj.Encrypt(str(user_data.value)),
                                        where="user_id="+str(userID))
                else:
                    return ComFnObj.Responser([], "opt not in the list", "failure")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()

            ComFnObj.PrintException("API_PROFILE_POST")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")
class fcmtoken:
    def GET(self):
        status = {"status": "Info", "message": "This page is intentionally left blank.","statusCode":121}
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', '*')
        web.header('Content-Type', 'application/json')
        return  json.dumps(status)
    def POST(self):

        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                userid=ComFnObj.GetIdFromAuth(Authcode)
                user_data = web.input()
                entries = db.update('tbl_user', fcm_token=user_data.token, where="user_id='" + str(userid) + "'")
                return ComFnObj.Responser([], "Operation success", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_FCMTOCKEN_POST")
            return ComFnObj.Responser([], str(e.message), "error")
class notifications:
    def OPTIONS(self,X):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                user_data = web.input(opt='list', value=-1,page=1)
                user_data.page=int(user_data.page)-1
                Notification = ComFnObj.GetNotification(user_data.opt, user_data.value,user_data.page)
                return ComFnObj.Responser(Notification, "Notification list", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_NOTIFICATION_GET")
            return ComFnObj.Responser(str(e.message), "Error in fetching notification list", "error")

    def POST(self):

        try:
            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            Responder=[]
            UserIDs=[]
            if ComFnObj.CheckAuth(Authcode):
                user_data = web.input()
                print user_data.users
                users=json.loads(user_data.users)
                print users
                for user in users:
                    UserID=ComFnObj.Decrypt(str(user)) #Encrypted userid will come
                    fcmId=ComFnObj.GetTokenFromID(UserID)
                    Res=ComFnObj.SendNotifOnSignal(fcmId, user_data.message,user_data.title)
                    Responder.append(Res) #To store what was the output
                    UserIDs.append(UserID) #To Store whome we sent
                entries = db.insert('tbl_notification', notification_title=user_data.title, notification_msg=user_data.message,typeofmessage=user_data.type,sentto=json.dumps(UserIDs),response=json.dumps(Res))
                return ComFnObj.Responser(Responder, "Operation success", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:

            ComFnObj.PrintException("API_NOTIFICATION_POST")
            return ComFnObj.Responser([], str(e.message), "error")




class event:
    def OPTIONS(self,X):
        ComFnObj = Commonfunctions()
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self, eventid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                user_data = web.input(opt='list', value=-1,page=1)
                if eventid:
                    user_data.opt='single'
                    user_data.value = eventid
                user_data.page=int(user_data.page)-1
                Event = ComFnObj.GetEvent(user_data.opt, user_data.value,user_data.page)
                return ComFnObj.Responser(Event, "Event", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_COURSE_GET")

            return ComFnObj.Responser(str(e.message), "Error in  event list", "error")

    def POST(self,eventid):

        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                user_data = web.input(opt=1)
                user_data.feestructure = ComFnObj.Decrypt(str(user_data.feestructure))
                user_data.eventtype = ComFnObj.Decrypt(str(user_data.eventtype))
                user_data.barn = ComFnObj.Decrypt(str(user_data.barn))
                user_data.organiser = ComFnObj.Decrypt(str(user_data.organiser))
                Files = json.loads(user_data.image)
                # print Files
                NewFileName = Files['name']
                if NewFileName != "":
                    Salt = "$343dddSS"
                    Rnd = random.random() * 90000
                    String = NewFileName + str(Rnd) + Salt
                    m = hashlib.md5()
                    m.update(String)
                    Random = m.hexdigest()
                    NewFileName = str(Random) + "_" + NewFileName
                    filecontent = str(Files['content'])
                    decoded_string = base64.b64decode(filecontent)
                    # print filecontent
                    with open('/var/www/html/BarnPort/images/event/' + NewFileName, "wb") as fout:
                        fout.write(decoded_string)

                if user_data.opt == str(1):
                    entries = db.insert('tbl_event', event_title=user_data.title,event_decscription=user_data.description,
                    event_headerImg=NewFileName,event_start_date=user_data.start,event_end_date=user_data.end,
                    event_status=user_data.status,feestructure_id_fk=user_data.feestructure,
                    eventtype_id_fk=user_data.eventtype,event_venue_id=user_data.barn,event_tags=user_data.tags,organiser_id_fk=user_data.organiser)
                elif user_data.opt == str(2):
                    if eventid:
                        user_data.id = eventid
                        entries = db.update('tbl_event', event_title=user_data.title,event_decscription=user_data.description,
                        event_headerImg=NewFileName,event_start_date=user_data.start,event_end_date=user_data.end,
                        event_status=user_data.status,feestructure_id_fk=user_data.feestructure,
                        eventtype_id_fk=user_data.eventtype,event_venue_id=user_data.barn,event_tags=user_data.tags,organiser_id_fk=user_data.organiser,where="event_id='" + ComFnObj.Decrypt(str(user_data.id)) + "'")
                    else:
                        return ComFnObj.Responser([], "No ID", "failure")
                else:
                    return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_COURSE_POST")

            if e[0]==1062:
                return ComFnObj.Responser([], "Title already exist", "error")
            else:
                return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")

    def DELETE(self,delid):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                db.query("delete from tbl_event where event_id="+str(ComFnObj.Decrypt(delid)))
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()
            ComFnObj.PrintException("API_EVENT_POST")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")

class wishlist:
    def GET(self):
        ComFnObj = Commonfunctions()
        header = web.ctx.environ
        Authcode = header.get('HTTP_AUTHCODE')

        if ComFnObj.CheckAuth(Authcode):
            userid=ComFnObj.GetIdFromAuth(Authcode)
            Responder=ComFnObj.GetWishlist('list',userid)
            return ComFnObj.Responser(Responder,"Wishlist","success")
        else:
            return ComFnObj.Responser([], "Authcode failed", "failure")



    def POST(self):
        JResponse=collections.OrderedDict();
        ComFnObj = Commonfunctions()
        try:

            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')

            if ComFnObj.CheckAuth(Authcode):

                userid=ComFnObj.GetIdFromAuth(Authcode)


                # user_data = json.loads(json_input)
                user_data = web.input()
                ID=ComFnObj.Decrypt(user_data.id)

                if user_data.opt==str(1):
                    k = "SELECT `wishlist_id` FROM `tbl_wishlist` WHERE `course_id_fk`=" + str(ID) + " and wishlist_type='COR' and user_id_fk="+str(userid)
                    entries = db.query(k)
                    rows = entries.list();
                    if rows:
                        return ComFnObj.Responser([], "Already in wishlist","failure")
                    else:
                        Query="INSERT INTO `tbl_wishlist`( `user_id_fk`, `course_id_fk`, `wishlist_type`, `event_id_fk`) VALUES ("+str(userid)+","+str(ID)+",'COR',NULL)"
                elif user_data.opt==str(2):
                    k = "SELECT `wishlist_id` FROM `tbl_wishlist` WHERE `event_id_fk`=" + str(ID) + " and wishlist_type='EVE' and user_id_fk="+str(userid)
                    entries = db.query(k)
                    rows = entries.list();
                    if rows:
                        return ComFnObj.Responser([], "Already in wishlist","failure")
                    else:
                        Query="INSERT INTO `tbl_wishlist`( `user_id_fk`, `course_id_fk`, `wishlist_type`, `event_id_fk`) VALUES ("+str(ID)+",NULL,'EVE',"+str(userid)+")"
                else:
                    return ComFnObj.Responser([], "Option should be 1 or 2","failure")
                print Query
                entries = db.query(Query)

            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")

        except Exception as e:
            if e[0]==1452:
                return ComFnObj.Responser([], "Course/Event not on list", "error")
            return ComFnObj.Responser([], "Wishlist:"+str(e), "error")
        else:

            return ComFnObj.Responser([], "Wishlist", "success")
class calanderpull:
    def GET(self):
        JResponse=collections.OrderedDict();
        ComFnObj = Commonfunctions()
        try:

            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')

            if ComFnObj.CheckAuth(Authcode):

                user_data = web.input()
                Date=user_data.dates
                Events=ComFnObj.GetEvent("indates",Date)
                Batchs=ComFnObj.GetBatch("indates",Date)
                OEvents=ComFnObj.GetEvent("overflow",Date)
                OBatchs=ComFnObj.GetBatch("overflow",Date)
                JObj={"events":Events,"batch":Batchs,"upcomming":{"events":OEvents,"batch":OBatchs}}
                return json.dumps(JObj)
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:

            return ComFnObj.Responser([], "Calander:"+str(e), "error")
        else:

            return ComFnObj.Responser(JResponse, "Calander", "success")

class shchedule:
    def OPTION(self):
        ComFnObj = Commonfunctions()
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self):
        try:
            ComFnObj = Commonfunctions()
            Events=ComFnObj.GetEvent("closedlist")


            JArr=[]
            JColor=['','#ff1975','#965994','#00eb92']
            for Event in Events:

                JObj={
                    'title': str(Event['title'])+", "+Event['venue']['title']+", "+Event['organiser']['name'],
                    'start': Event['startdate'],
                    'end': Event['enddate'],
                    'color': JColor[int(ComFnObj.Decrypt(Event['type']['id']))]
                }
                JArr.append(JObj)
            web.header('Access-Control-Allow-Origin', '*')
            web.header('Access-Control-Allow-Methods', '*')
            web.header('Access-Control-Allow-Headers', 'Authcode')
            web.header('Access-Control-Allow-Credentials', 'true')
            web.header('Content-Type', 'application/json')
            return json.dumps(JArr)

        except Exception as e:
            return e

class checkout:
    def POST(self):
        ComFnObj = Commonfunctions()
        try:
            juspay.api_key = '82995B0CB0524D79AA10CECE73CF3506'
            juspay.environment = 'production'


            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                user_data = web.input(opt='C', id=-1,amount=0)
                id=ComFnObj.Decrypt(user_data.id)
                if user_data.opt=='C':
                    Data=ComFnObj.GetCourse("single",user_data.id)
                elif user_data.opt=='E':
                    Data=ComFnObj.GetEvent("single",user_data.id)
                else:
                    return ComFnObj.Responser([], "Option out of list", "error")

                #JData=json.loads(Data)

                URL=ComFnObj.BASEURL+"checkoutconfirm"
                Amounttopay=int(Data['fee']['structure']['base']['value'])
                my_new_order = juspay.Orders.create(order_id=str(int(time.time())), amount=Amounttopay  , currency="INR",return_url=URL)
                """for attr, value in my_new_order.__dict__.iteritems():
                    print attr, value"""

                Responder={'status':my_new_order.status,
                              'amount_refunded': my_new_order.amount_refunded,
                              'status_id': my_new_order.status_id,
                              'order_id': my_new_order.order_id,
                              'refunded': my_new_order.refunded,
                              'currency': my_new_order.currency,
                              'amount': my_new_order.amount,
                              'merchant_id':my_new_order.merchant_id,
                              'payment_method':my_new_order.payment_method,
                              'bank_error_code':my_new_order.bank_error_code,
                              'billing_address':my_new_order.billing_address,
                              'id':my_new_order.id,
                              'gateway_id':my_new_order.gateway_id,
                              'gateway_response':my_new_order.gateway_response,
                              'customer_id':my_new_order.customer_id,
                              'customer_email':my_new_order.customer_email,
                              'description':my_new_order.description,
                              'customer_phone':my_new_order.customer_phone,
                              'product_id':my_new_order.product_id,
                              'payment_method_type':my_new_order.payment_method_type,
                              'bank_error_message':my_new_order.bank_error_message,
                              'shipping_address':my_new_order.shipping_address,
                              'return_url':my_new_order.return_url,
                              'url':{"mobile":my_new_order.payment_links.mobile,"iframe":my_new_order.payment_links.iframe,"web":my_new_order.payment_links.web}
                         }

                return ComFnObj.Responser(Responder,"Order details", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "error")
        except Exception as exception:
            # Output unexpected Exceptions.
            ComFnObj.PrintException("API_CHECKOUT_POST")
            return ComFnObj.Responser(json.loads(exception.message),"Error", "error")
class checkoutconfirm:
    def POST(self):
        user_data = web.input(opt=1)
        return user_data
    def GET(self):
        user_data = web.input()
        ComFnObj = Commonfunctions()
        if user_data.status=="CHARGED":
            ComFnObj.SetFirebaseDB(user_data.order_id,"PAYMENT DONE")
        else:
            ComFnObj.SetFirebaseDB(user_data.order_id,"PAYMENT ERROR")
        return user_data

class checkoutsite:
    def POST(self):
        ComFnObj = Commonfunctions()
        try:
            #juspay.api_key = '1CFD660F0AD3405BA8435F5EA354EA5F'
            #juspay.environment = 'sandbox'
            juspay.api_key = '82995B0CB0524D79AA10CECE73CF3506'
            juspay.environment = 'production'


            user_data = web.input(opt='C', id=-1,amount=0)
            id=ComFnObj.Decrypt(str(user_data.id))
            paymentid=ComFnObj.GenerateOTP(user_data.phone,5)+str(int(time.time()))
            if user_data.opt=='C':
                Data=ComFnObj.GetCourse("single",user_data.id)
                Query="VALUES ('"+user_data.name+"','"+user_data.phone+"','"+user_data.email+"','"+id+"','','C','Start','"+paymentid+"')"
            elif user_data.opt=='E':
                Data=ComFnObj.GetEvent("single",user_data.id)
                Query="VALUES ('"+user_data.name+"','"+user_data.phone+"','"+user_data.email+"','','"+id+"','E','Start','"+paymentid+"')"
            else:
                return ComFnObj.Responser([], "Option out of list", "error")


            Query="INSERT INTO `tbl_siteenrolled`(`username`, `phone`, `email`, `courseid`, `eventid`, `booking_type`, `payment_status`, `orderid`) "+Query
            entries = db.query(Query)

            URL=ComFnObj.BASEURL+"checkoutconfirmsite"
            Amounttopay=int(Data['fee']['structure']['base']['value'])
            my_new_order = juspay.Orders.create(order_id=paymentid, amount=Amounttopay  , currency="INR",return_url=URL)


            Responder={'status':my_new_order.status,
                              'amount_refunded': my_new_order.amount_refunded,
                              'status_id': my_new_order.status_id,
                              'order_id': my_new_order.order_id,
                              'refunded': my_new_order.refunded,
                              'currency': my_new_order.currency,
                              'amount': my_new_order.amount,
                              'merchant_id':my_new_order.merchant_id,
                              'payment_method':my_new_order.payment_method,
                              'bank_error_code':my_new_order.bank_error_code,
                              'billing_address':my_new_order.billing_address,
                              'id':my_new_order.id,
                              'gateway_id':my_new_order.gateway_id,
                              'gateway_response':my_new_order.gateway_response,
                              'customer_id':my_new_order.customer_id,
                              'customer_email':my_new_order.customer_email,
                              'description':my_new_order.description,
                              'customer_phone':my_new_order.customer_phone,
                              'product_id':my_new_order.product_id,
                              'payment_method_type':my_new_order.payment_method_type,
                              'bank_error_message':my_new_order.bank_error_message,
                              'shipping_address':my_new_order.shipping_address,
                              'return_url':my_new_order.return_url,
                              'url':{"mobile":my_new_order.payment_links.mobile,"iframe":my_new_order.payment_links.iframe,"web":my_new_order.payment_links.web}
                         }
            web.redirect(my_new_order.payment_links.web)
            #return ComFnObj.Responser(Responder,"Order details", "success")

        except Exception as exception:
            # Output unexpected Exceptions.
            ComFnObj.PrintException("API_CHECKOUT_POST")
            return ComFnObj.Responser(json.loads(exception.message),"Error", "error")

class checkoutconfirmsite:
    def POST(self):
        user_data = web.input(opt=1)
        return user_data
    def GET(self):
        user_data = web.input()
        ComFnObj = Commonfunctions()
        if user_data.status=="CHARGED":
            Query="update `tbl_siteenrolled` set `payment_status`='"+user_data.status+"' where `orderid` ='"+user_data.order_id+"'"
            entries = db.query(Query)
            X=ComFnObj.SendMail('manya@spread.ooo',"dev@spread.ooo","New Payment Done",user_data.order_id,user_data.order_id)
            web.redirect("http://spread.ooo/confirmpayment.php?n=y&o="+user_data.order_id+"&u="+user_data.status)
        else:
            Query="update `tbl_siteenrolled` set `payment_status`='"+user_data.status+"' where `orderid` ='"+user_data.order_id+"'"
            entries = db.query(Query)
            X=ComFnObj.SendMail('manya@spread.ooo',"dev@spread.ooo","Payment Error",user_data.order_id,user_data.order_id)
            web.redirect("http://spread.ooo/confirmpayment.php?n=n&o="+user_data.order_id+"&u="+user_data.status)
        return user_data

class genpaymentlink:
    def POST(self):
        ComFnObj = Commonfunctions()
        try:
            #juspay.api_key = '1CFD660F0AD3405BA8435F5EA354EA5F'
            #juspay.environment = 'sandbox'
            juspay.api_key = '82995B0CB0524D79AA10CECE73CF3506'
            juspay.environment = 'production'


            user_data = web.input(opt='C', id=-1,amount=0)
            id=ComFnObj.Decrypt(str(user_data.id))
            paymentid=ComFnObj.GenerateOTP(user_data.phone,5)+str(int(time.time()))
            if user_data.opt=='C':
                Data=ComFnObj.GetCourse("single",user_data.id)
                Query="VALUES ('"+user_data.name+"','"+user_data.phone+"','"+user_data.email+"','"+id+"','','C','Start','"+paymentid+"')"
            elif user_data.opt=='E':
                Data=ComFnObj.GetEvent("single",user_data.id)
                Query="VALUES ('"+user_data.name+"','"+user_data.phone+"','"+user_data.email+"','','"+id+"','E','Start','"+paymentid+"')"
            else:
                return ComFnObj.Responser([], "Option out of list", "error")

            Query="INSERT INTO `tbl_siteenrolled`(`username`, `phone`, `email`, `courseid`, `eventid`, `booking_type`, `payment_status`, `orderid`) "+Query
            entries = db.query(Query)

            URL=ComFnObj.BASEURL+"checkoutconfirmsite"
            Amounttopay=user_data.amount
            my_new_order = juspay.Orders.create(order_id=paymentid, amount=Amounttopay  , currency="INR",return_url=URL)

            #MailBody="<html><head><style><style><title>Spread Payment</title></head><body>"
            #MailBody+="<p>Hello <b>'"+user_data.name+"'</b>.</p><a href='"+my_new_order.payment_links.web+"'>Open in browser</a><a href='"+my_new_order.payment_links.mobile+"'>Open in mobile</a></body></html>"
            #ComFnObj.SendMail(user_data.email,"noreply@spread.ooo","Payment pending for your course.",MailBody,my_new_order.payment_links.web)

            Responder="<a href='"+my_new_order.payment_links.mobile+"'>Mobile Link</a><br><a href='"+my_new_order.payment_links.web+"'>Web Link</a><br>"
            render = web.template.render('/var/www')
            Returner=render.Paylink(user_data.name,my_new_order.payment_links.web,my_new_order.payment_links.mobile)
            MailBody=Returner['__body__']
            MailBodyPlain="Registration Complete"
            ComFnObj.SendMail(user_data.email,"noreply@spread.ooo","Payment pending for your course.",MailBody,MailBodyPlain)

            return Responder

        except Exception as exception:
            # Output unexpected Exceptions.
            ComFnObj.PrintException("API_GetLinks_POST")
            return ComFnObj.Responser(json.loads(exception.message),"Error", "error")


class griduser:
    def OPTIONS(self):
        ComFnObj = Commonfunctions()
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', '*')
        web.header('Access-Control-Allow-Headers', 'Authcode')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        return ""
    def GET(self):    

        ComFnObj = Commonfunctions()
        user_data = web.input()
        try:
           
            Query = "SELECT `user_id`, `user_name`, `user_dob`, `user_phone`, `user_email`," \
                    " `user_status`, `isCollective` FROM `tbl_user`" \
                    " WHERE `isCollective`=1"

            entries = db.query(Query)
            rows = entries.list();
            JArr=[]
            if rows:

                for row in rows:
                    userid=ComFnObj.Encrypt(str(row['user_id']))
                    JObj = {"id": userid,
                        "name": row['user_name'],
                        "DOB": str(row['user_dob']),
                        "phone": row['user_phone'],
                        "email": row['user_email'],
                        "status": row['user_status'],
                        "isCollective": row['isCollective'],
                        "griddetails":ComFnObj.GetTalent(row['user_id']),
                        "image": "https://i2.wp.com/ui-avatars.com/api/"+str(row['user_name'])+"/300?ssl=1",
                        
                        }
                    JArr.append(JObj)

                return ComFnObj.Responser(JArr, "User details", "success")
            else:
                return ComFnObj.Responser([], "No Collective", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_GRID_GET")
            return ComFnObj.Responser(str(e.message), "Error in grid", "error")
    def POST(self):

        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            user_data = web.input()
            if ComFnObj.CheckAuth(Authcode):
                UserId=ComFnObj.GetIdFromAuth(Authcode)

                Query="INSERT INTO `tbl_grid`(`user_id_fk`, `user_hashtag`, `user_description`, `user_talent`, `user_worklink`, `user_wanttodo`) \
                VALUES ('"+str(UserId)+"','"+str(user_data.hashtag)+"','"+str(user_data.description)+"','"+str(user_data.talent)+"','"+str(user_data.worklink)+"','"+str(user_data.wanttodo)+"')"
                entries = db.query(Query)

                Query = "update `tbl_user` set  `isCollective`=2  WHERE `user_id`="+str(UserId)
                entries = db.query(Query)

                return ComFnObj.Responser([], "Grid selection request sent", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            if e[0]==1062:
                    return ComFnObj.Responser([], "Request already sent", "error")
                
            ComFnObj.PrintException("API_COURSE_POST")
            return ComFnObj.Responser([], str(e.message), "error")
        
    def PUT(self):
        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            
            if ComFnObj.CheckAuth(Authcode):
                UserId=ComFnObj.GetIdFromAuth(Authcode)

               
                Query = "update `tbl_user` set  `isCollective`=1  WHERE `user_id`="+str(UserId)
                entries = db.query(Query)
                return ComFnObj.Responser([], "Grid selection request accepted", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
           
            ComFnObj.PrintException("API_COURSE_POST")
            return ComFnObj.Responser([], str(e.message), "error")


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
else:
    application = web.application(urls, globals()).wsgifunc()
