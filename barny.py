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
from random import randint
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
    '/classroom/(.*)','classroom',
    '/table/(.*)', 'table',
    '/chair/(.*)', 'chair',
    '/floor/(.*)', 'floor',
    '/exhibit/(.*)', 'exhibit',
    '/organiser/(.*)', 'organiser',
    '/feestructure/(.*)', 'feestructure',
    '/course/(.*)', 'course',
    '/enroll/(.*)', 'enroll',
    '/profile/(.*)', 'profile',
    '/event/(.*)', 'event',


    '/register', 'register',
    '/login', 'login',



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
        return ComFnObj.Decrypt("nHLAnFapfNIc40df6j3YXquYqomLQm3kV7ADN2HPDX4=")



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

    def GetBarns(self, OPT='list', value=-1,page=1, datatype="S"): #S is single A is array
        try:
            start=int(page) * 5;
            end=5;
            JArray=[]
            JRespo=[]
            JAminities=[]
            if OPT == "single":
                ID=self.Decrypt(value)
                Query="SELECT `barn_id`, `barn_location`, `barn_title`, `barn_poc`, `barn_phone`, `barn_address`, `barn_amenities` FROM `tbl_barn` where `barn_id`='"+ID+"'"
            elif OPT=="list":
                Query="SELECT totalCount,`barn_id`, `barn_location`, `barn_title`, `barn_poc`, `barn_phone`, `barn_address`, `barn_amenities` FROM `tbl_barn`,(SELECT COUNT(*) totalCount FROM tbl_barn) c limit "+str(start)+","+str(end)
            elif OPT=="location":
                Query="SELECT totalCount,`barn_id`, `barn_location`, `barn_title`, `barn_poc`, `barn_phone`, `barn_address`, `barn_amenities` FROM `tbl_barn`,(SELECT COUNT(*) totalCount FROM tbl_barn where `barn_location`='"+str(value)+"') c where `barn_location`='"+str(value)+"' limit "+str(start)+","+str(end)
           
            entries = db.query(Query)
            rows = entries.list();
            if rows:
                print rows
                for row in rows:
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
                        "amenities":JAminities
                        
                        }
                    JArray.append(JObj);
            JCount=0
            if OPT=="single":
                return JArray[0]
            else:
                if row['totalCount']:
                    JCount=row['totalCount']
                    JRespo.append({"totalrecords":JCount,'data':JArray})
                return JRespo
        except Exception as e:
            self.PrintException("FN_GetBarns");
            return e
    def GetAminities(self, OPT='list', value=-1,page=1, datatype="S"): #S is single A is array
        try:
            start = int(page) * 5;
            end = 5;
            JArray=[]
            JRespo=[]
            JResponse=collections.OrderedDict()
            if OPT == "single":
                Query="SELECT `amenities_id`, `amenities_title`,`amenities_icon` FROM `tbl_amenities` WHERE `amenities_id`="+str(value)
            elif OPT=="list":
                Query="SELECT `totalCount`,`amenities_id`, `amenities_title`,`amenities_icon` FROM `tbl_amenities`,(SELECT COUNT(*) totalCount FROM tbl_amenities) c limit "+str(start)+","+str(end)
            elif OPT == "combo":
                Query = "SELECT `amenities_id`, `amenities_title`,`amenities_icon` FROM `tbl_amenities`"
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
                            "icon":row['amenities_icon'],
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
            self.PrintException("FN_GetAminities");
            return e
    def GetClassrooms(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
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
            self.PrintException("FN_GetClassroom");
            return e
    def GetTables(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:
            JArray = []
            JAminities = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT `table_id`, `table_number`, `barn_id_fk` FROM `tbl_table`  where `table_id`='" + ID + "'"
            elif OPT == "list":
                Query = "SELECT `table_id`, `table_number`, `barn_id_fk` FROM `tbl_table` "
            elif OPT == "barn":
                ID = self.Decrypt(value)
                Query = "SELECT `table_id`, `table_number`, `barn_id_fk` FROM `tbl_table`  where `barn_id_fk`='" + str(
                    ID) + "'"
            elif OPT == "number":
                 Query = "SELECT `table_id`, `table_number`, `barn_id_fk` FROM `tbl_table`  where `table_number`='" + str(value) + "'"
            elif OPT == "numberbarn": #Table number in barn
                BarnID = self.Decrypt(value[0])
                TableNumber =value[1]
                Query = "SELECT `table_id`, `table_number`, `barn_id_fk` FROM `tbl_table`  where `table_number`='" + str(
                    TableNumber) + "' and barn_id_fk='"+str(BarnID)+"'"

            #elif OPT == "capacity":
            #    Query = " SELECT `classroom_id`, `barn_id_fk`, `classroom_capacity` FROM `tbl_classroom`  where `classroom_capacity`='" + str(
            #        value) + "'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    JObj = {"id": self.Encrypt(str(row['table_id'])),
                            "barn": self.GetBarns('single',self.Encrypt(str(row['barn_id_fk']))),
                            "number": row['table_number']
                            }
                    JArray.append(JObj);
            if OPT=="single":
                return JArray[0]
            else:
                return JArray
        except Exception as e:
            self.PrintException("FN_GetTable");
            return e
    def GetChairs(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:
            JArray = []
            JAminities = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT `chair_id`, `chair_number`, `table_id_fk` FROM `tbl_chair`  where `chair_id`='" + ID + "'"
            elif OPT == "list":
                Query = "SELECT `chair_id`, `chair_number`, `table_id_fk` FROM `tbl_chair` "
            elif OPT == "table":
                ID = self.Decrypt(value)
                Query = "SELECT `chair_id`, `chair_number`, `table_id_fk` FROM `tbl_chair`  where `table_id_fk`='" + str(
                    ID) + "'"
            elif OPT == "number":
                ID = self.Decrypt(value)
                Query = "SELECT  `chair_id`, `chair_number`, `table_id_fk` FROM `tbl_chair`  where `chair_number`='" + str(
                    value) + "'"
            elif OPT == "numbertable": #Table number in barn
                TableID = self.Decrypt(value[0])
                ChairNumber =value[1]
                Query = "SELECT  `chair_id`, `chair_number`, `table_id_fk` FROM `tbl_chair`  where `chair_number`='" + str(
                    ChairNumber) + "' and table_id_fk='"+str(TableID)+"'"
            #elif OPT == "capacity":
            #    Query = " SELECT `classroom_id`, `barn_id_fk`, `classroom_capacity` FROM `tbl_classroom`  where `classroom_capacity`='" + str(
            #        value) + "'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    JObj = {"id": self.Encrypt(str(row['chair_id'])),
                            "table": self.GetTables('single',self.Encrypt(str(row['table_id_fk']))),
                            "number": row['chair_number']
                            }
                    JArray.append(JObj);
            if OPT=="single":
                return JArray[0]
            else:
                return JArray
        except Exception as e:
            self.PrintException("FN_GetChair");
            return e
    def GetFloors(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:
            JArray = []
            JAminities = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT  `floor_id`, `floor_capacity` FROM `tbl_floor`  where `barn_id_fk`='" + ID + "'"
            elif OPT == "list":
                Query = "SELECT  `floor_id`, `floor_capacity` FROM `tbl_floor` "

           # elif OPT == "capacity":
          #      Query = " SELECT  `barn_id_fk`, `floor_capacity` FROM `tbl_floor`  where `floor_capacity`='" + str(value) + "'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    JObj = {"id": self.Encrypt(str(row['floor_id'])),
                            "barn": self.GetBarns('single', self.Encrypt(str(row['floor_id']))),
                            "capacity": row['floor_capacity']
                            }
                    JArray.append(JObj);
            if OPT == "single":
                return JArray[0]
            else:
                return JArray
        except Exception as e:
            self.PrintException("FN_GetFloor");
            return e
    def GetExhibits(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:
            JArray = []
            JAminities = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT `exhibit_id`, `barn_id_fk`, `exhibit_capacity` FROM `tbl_exhibit`  where `exhibit_id`='" + ID + "'"
            elif OPT == "list":
                Query = "SELECT `exhibit_id`, `barn_id_fk`, `exhibit_capacity` FROM `tbl_exhibit` "
            elif OPT == "barn":
                ID = self.Decrypt(value)
                Query = " SELECT `exhibit_id`, `barn_id_fk`, `exhibit_capacity` FROM `tbl_exhibit`  where `barn_id_fk`='" + str(
                    ID) + "'"

            elif OPT == "capacity":
                Query = " SELECT `exhibit_id`, `barn_id_fk`, `exhibit_capacity` FROM `tbl_exhibit`  where `exhibit_capacity`='" + str(
                    value) + "'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    JObj = {"id": self.Encrypt(str(row['exhibit_id'])),
                            "barn": self.GetBarns('single',self.Encrypt(str(row['barn_id_fk']))),
                            "capacity": row['exhibit_capacity']
                            }
                    JArray.append(JObj);
            if OPT=="single":
                return JArray[0]
            else:
                return JArray
        except Exception as e:
            self.PrintException("FN_GetExhibit");
            return e
    def GetBookingTypes(self, OPT='list', value=-1,page=1, datatype="S"): #S is single A is array
        try:
            start = int(page) * 5;
            end = 5;
            JArray=[]
            JResponse=collections.OrderedDict()
            if OPT == "single":
                value = self.Decrypt(str(value))
                Query="SELECT 0 as totalCount,`bookingtype_id`, `bookingtype_title` FROM `tbl_bookingtype` WHERE `bookingtype_id`="+str(value)
            elif OPT=="list":
                Query="SELECT totalCount,`bookingtype_id`, `bookingtype_title` FROM `tbl_bookingtype`,(SELECT COUNT(*) totalCount FROM tbl_bookingtype) c limit "+str(start)+","+str(end)
            print Query
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
            start = int(page) * 5;
            end = 5;
            JArray = []
            JResponse = collections.OrderedDict()
            if OPT == "single":
                value = self.Decrypt(str(value))
                Query = "SELECT 0 as totalCount,`eventtype_id`, `eventtype_title` FROM `tbl_eventtype` WHERE `eventtype_id`=" + str(
                    value)
            elif OPT == "list":
                Query = "SELECT totalCount,`eventtype_id`, `eventtype_title` FROM `tbl_eventtype`,(SELECT COUNT(*) totalCount FROM tbl_eventtype) c limit " + str(
                    start) + "," + str(end)
            print Query
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
            start = int(page) * 5;
            end = 5;
            JArray = []
            JResponse = collections.OrderedDict()
            if OPT == "single":
                value = self.Decrypt(str(value))
                Query = "SELECT 0 as totalCount,`organisertype_id`, `organisertype_title` FROM `tbl_organisertype` WHERE `organisertype_id`=" + str(
                    value)
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
            if OPT == "single":
                return JArray[0]
            elif OPT == "closedlist" or OPT == "combo":
                return JArray
            else:
                JCount = row['totalCount']
                JRespo.append({"totalrecords": JCount, 'data': JArray})
                return JRespo

        except Exception as e:
            self.PrintException("FN_GetOrganiserTypes");
            return e
    def GetCourseTypes(self, OPT='list', value=-1,page=1, datatype="S"): #S is single A is array
        try:
            start = int(page) * 5;
            end = 5;
            JArray = []
            JResponse = collections.OrderedDict()
            if OPT == "single":
                value = self.Decrypt(str(value))
                Query = "SELECT 0 as totalCount,`coursetype_id`, `coursetype_title` FROM `tbl_coursetype` WHERE `coursetype_id`=" + str(
                    value)
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
            if OPT == "single":
                return JArray[0]
            elif OPT == "closedlist" or OPT == "combo":
                return JArray
            else:
                JCount = row['totalCount']
                JRespo.append({"totalrecords": JCount, 'data': JArray})
                return JRespo

        except Exception as e:
            self.PrintException("FN_GetOrganiserTypes");
            return e
    def GetTags(self, OPT='list', value=-1,page=1, datatype="S"): #S is single A is array
        try:
            start = int(page) * 5;
            end = 5;
            JArray=[]
            JResponse=collections.OrderedDict()
            if OPT == "single":
                value = self.Decrypt(str(value))
                Query="SELECT 0 as totalCount,`tag_id`, `tag_title` FROM `tbl_tags` WHERE `tag_id`="+str(value)
            elif OPT=="list":
                Query="SELECT totalCount,`tag_id`, `tag_title` FROM `tbl_tags`,(SELECT COUNT(*) totalCount FROM tbl_tags) c limit "+str(start)+","+str(end)
            print Query
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
    def GetOrganisers(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:
            JArray = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT `organiser_id`, `organisertype_id_fk`, `organiser_name`, `organiser_description`, `organiser_image` FROM `tbl_organiser` where `organiser_id`='" + str(ID) + "'"
            elif OPT == "list":
                Query = "SELECT `organiser_id`, `organisertype_id_fk`, `organiser_name`, `organiser_description`, `organiser_image` FROM `tbl_organiser`"

            elif OPT == "type":
                ID = self.Decrypt(value)
                Query = "SELECT `organiser_id`, `organisertype_id_fk`, `organiser_name`, `organiser_description`, `organiser_image` FROM `tbl_organiser` where `organisertype_id_fk`='" + str(
                    ID) + "'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    OrgId=self.Encrypt(str(row['organiser_id']))
                    JObj = {"id": OrgId,
                            "type": self.GetOrganiserTypes('single',self.Encrypt(str(row['organisertype_id_fk']))),
                            "name": row['organiser_name'],
                            "description": row['organiser_description'],
                            "image": row['organiser_image'],
                            }
                    JArray.append(JObj);
            if OPT == "single":
                return JArray[0]
            else:
                return JArray
        except Exception as e:
            self.PrintException("FN_GetOrganiser");
            return e
    def GetFeeStructure(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        #print str(value)+" "+OPT
        try:
            JArray = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT `feestructure_id`, `feestructure_title`, `feestructure_fee` FROM `tbl_feestructure`  where `feestructure_id`='" + str(ID) + "'"
            elif OPT == "list":
                Query = "SELECT `feestructure_id`, `feestructure_title`, `feestructure_fee` FROM `tbl_feestructure`"

            elif OPT == "course":
                ID = self.Decrypt(value)
                Query = "SELECT `feestructure_id`, `feestructure_title`, `feestructure_fee` `feestructure_id_fk` FROM" \
                        " `tbl_course` ,`tbl_feestructure` where `feestructure_id_fk`=`feestructure_id` and course_id='" + str(ID) + "'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    FeeId=self.Encrypt(str(row['feestructure_id']))
                    JObj = {"id": FeeId,
                            "title": row['feestructure_title'],
                            "structure": json.loads(row['feestructure_fee'])
                            }
                    JArray.append(JObj);
            if OPT == "single":
                return JArray[0]
            else:
                return JArray
        except Exception as e:
            self.PrintException("FN_GetFeeStructure");
            return e
    def GetCourse(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:

            JArray = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT `course_id`, `course_title`, `course_desc`, `course_duration`, `course_agelimit`, `course_image`, `course_status`," \
                        " `feestructure_id_fk`, `coursetype_id_fk`, `course_tags` FROM `tbl_course` WHERE course_id='" + str(ID) + "'"
            elif OPT == "list":
                Query = "SELECT `course_id`, `course_title`, `course_desc`, `course_duration`, `course_agelimit`, `course_image`," \
                        " `course_status`, `feestructure_id_fk`, `coursetype_id_fk`, `course_tags` FROM `tbl_course`"
            elif OPT == "type":
                ID = self.Decrypt(value)
                Query = "SELECT `course_id`, `course_title`, `course_desc`, `course_duration`, `course_agelimit`, " \
                        "`course_image`,  `course_status`,`feestructure_id_fk`, `coursetype_id_fk`, `course_tags` FROM " \
                        "`tbl_course` where `coursetype_id_fk`='" + str(ID) + "'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    CourseId = self.Encrypt(str(row['course_id']))
                    FeeStructure=self.GetFeeStructure("single", self.Encrypt(str(row['feestructure_id_fk'])))
                    CourseType=self.GetCourseTypes("single", self.Encrypt(str(row['coursetype_id_fk'])))

                    JObj = {"id": CourseId,
                            "title": row['course_title'],
                            "type":CourseType,
                            "fee":FeeStructure,
                            "description":row['course_desc'],
                            "duration":json.loads(row['course_duration']),
                            "agelimit":json.loads(row['course_agelimit']),
                            "image":row['course_image'],
                            "status":row['course_status'],
                            "tags":row['course_tags'],
                            }
                    JArray.append(JObj);
            if OPT == "single":
                return JArray[0]
            else:
                return JArray
        except Exception as e:
            self.PrintException("FN_GetCourse");
            return e
    def GetEnrolledCourse(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:

            JArray = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT `enrolled_id`, `user_id_fk`, `coursemap_id_fk`, `enrolled_date`, `enrolled_status` FROM `tbl_enrolled` WHERE `enrolled_id`='" + str(ID) + "'"
            elif OPT == "list":
                Query = "SELECT `enrolled_id`, `user_id_fk`, `coursemap_id_fk`, `enrolled_date`, `enrolled_status` FROM `tbl_enrolled`"
            elif OPT == "user":
                ID = self.Decrypt(value)
                Query = "SELECT `enrolled_id`, `user_id_fk`, `coursemap_id_fk`, `enrolled_date`, `enrolled_status` FROM `tbl_enrolled` where `user_id_fk`='" + str(ID) + "'"
            elif OPT=="isexist":
                print value
                userId = self.Decrypt(value[0])
                courseId = self.Decrypt(value[1])

                Query = "SELECT `enrolled_id`, `user_id_fk`, `coursemap_id_fk`, `enrolled_date`, `enrolled_status` FROM `tbl_enrolled`,`tbl_classcoursemap`" \
                        " WHERE `user_id_fk`='" + str(userId) + "' and `course_id_fk`='" + str(courseId) + "' and  `coursemap_id_fk`=`map_id`"


            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    EnrollId = self.Encrypt(str(row['enrolled_id']))
                    CourseMapId = self.Encrypt(str(row['coursemap_id_fk']))

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
                        "`user_email`, `user_status`, `isCollective`, `user_authcode` FROM `tbl_user` WHERE user_id='" + str(ID) + "'"
            elif OPT == "list":
                Query = " SELECT `user_id`, `user_name`, `user_dob`, `user_phone`, `user_email`, `user_status`, `isCollective`, `user_authcode` FROM `tbl_user`"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    UserId = self.Encrypt(str(row['user_id']))


                    JObj = {"id": UserId,
                            "enrolled": self.GetEnrolledCourse("user",UserId),
                            "name": row['user_name'],
                            "phone": row['user_phone'],
                            "email": row['user_email'],
                            "status": row['user_status'],
                            "iscollective": row['isCollective'],
                            "DOB":row['user_dob']
                        }
                    JArray.append(JObj);
            if OPT == "single":
                return JArray[0]
            else:
                return JArray
        except Exception as e:
            self.PrintException("FN_GetProfiles");
            return e
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
            entries = db.query(Query)
            rows = entries.list();
            if rows:
                if OPT=='getidfromcnb':
                    return self.Encrypt(str(rows[0]['map_id']))
                for row in rows:
                    CourseId = self.Encrypt(str(row['course_id_fk']))
                    print row['course_id_fk']
                    BarnId = self.Encrypt(str(row['barn_id_fk']))
                    MapId = self.Encrypt(str(row['map_id']))


                    JObj = {"id":MapId ,
                            "course": self.GetCourse("single",CourseId),
                            "barn": self.GetBarns("single",BarnId)
                           }
                    JArray.append(JObj);
            if OPT == "single" or OPT=="getidfromcnb":
                return JArray[0]
            else:
                return JArray
        except Exception as e:
            self.PrintException("FN_GetProfiles");
            return e
    def GetEvent(self, OPT='list', value=-1,page=1, datatype="S"):  # S is single A is array
        try:

            JArray = []
            if OPT == "single":
                ID = self.Decrypt(value)
                Query = "SELECT `event_event_id`, `event_title`, `event_decscription`, `event_headerImg`, `feestructure_id_fk`, `event_status`, `event_start_date`, `event_end_date`," \
                        " `organiser_id_fk`, `event_venue_id`, `eventtype_id_fk`, `event_tags` FROM `tbl_event` WHERE  event_id='" + str(
                    ID) + "'"
            elif OPT == "list":
                Query = "SELECT `event_id`, `event_title`, `event_decscription`, `event_headerImg`, `feestructure_id_fk`, `event_status`, `event_start_date`, `event_end_date`," \
                        " `organiser_id_fk`, `event_venue_id`, `eventtype_id_fk`, `event_tags` FROM `tbl_event`"
            elif OPT == "type":
                ID = self.Decrypt(value)
                Query = "SELECT `event_id`, `event_title`, `event_decscription`, `event_headerImg`, `feestructure_id_fk`, `event_status`, `event_start_date`, `event_end_date`, " \
                        "`organiser_id_fk`, `event_venue_id`, `eventtype_id_fk`, `event_tags` FROM `tbl_event` WHERE  `eventtype_id_fk`='" + str(ID) + "'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                for row in rows:
                    EventID = self.Encrypt(str(row['event_id']))
                    FeeStructure = self.GetFeeStructure("single", self.Encrypt(str(row['feestructure_id_fk'])))
                    EventType = self.GetEventTypes("single", self.Encrypt(str(row['eventtype_id_fk'])))
                    Organiser = self.GetOrganisers("single", self.Encrypt(str(row['organiser_id_fk'])))

                    JObj = {"id": EventID,
                            "title": row['event_title'],
                            "description": row['event_decscription'],
                            "image": row['event_headerImg'],
                            "fee": FeeStructure,
                            "type": EventType,
                            "status": row['event_status'],
                            "startdate": str(row['event_start_date']),
                            "enddate": str(row['event_end_date']),
                            "organiser":Organiser,
                            "venue": row['event_venue_id'],
                            "type": EventType,
                            "tags": row['event_tags'],
                            }
                    JArray.append(JObj);
            if OPT == "single":
                return JArray[0]
            else:
                return JArray
        except Exception as e:
            self.PrintException("FN_GetCourse");
            return e
    def QueryMaker(self,type,data):
        print data
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
            print Files
            NewFileName=Files['name']
            if NewFileName!="":
                Salt = "$343dddSS"
                Rnd = randint(2, 90000)
                String = NewFileName + str(Rnd) + Salt
                m = hashlib.md5()
                m.update(String)
                Random = m.hexdigest()
                NewFileName = str(Random) + "_" + NewFileName
                filecontent = str(Files['content'])
                decoded_string = base64.b64decode(filecontent)
                print filecontent
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

class checkregistration:
    def GET(self):

        ComFnObj = Commonfunctions()
        return ComFnObj.Responser([], "")


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
class login:
    def GET(self):
        ComFnObj = Commonfunctions()
        return ComFnObj.Responser([], "")


    def POST(self):
        ComFnObj = Commonfunctions()
        user_data = web.input()
        try:
            Query = "SELECT `user_id`, `user_name`, `user_dob`, `user_phone`, `user_email`, `user_password`," \
                    " `user_status`, `isCollective`, `user_authcode` FROM `tbl_user`" \
                    " WHERE `user_password`='"+ComFnObj.Encrypt(user_data.password)+"' and `user_email`='"+user_data.email+"'"

            entries = db.query(Query)
            rows = entries.list();
            if rows:

                row=rows[0]
                userid=row['user_id']
                JObj = {"id": userid,
                        "name": row['user_name'],
                        "DOB": row['user_dob'],
                        "phone": row['user_phone'],
                        "email": row['user_email'],
                        "status": row['user_status'],
                        "isCollective": row['isCollective'],
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
                print user_data
                if  user_data.opt==str(1):
                    user_data.amenities = json.loads(user_data.amenities)
                    amen=[]
                    for amenitits in user_data.amenities:
                        amen.append(ComFnObj.Decrypt(amenitits))
                    entries = db.insert('tbl_barn', barn_title=user_data.title, \
                                        barn_location=user_data.location,barn_poc=user_data.poc, \
                                        barn_phone=user_data.phone, barn_address=user_data.address, \
                                       barn_amenities=','.join(amen))
                elif user_data.opt==str(2):
                    amen = []
                    user_data.amenities = json.loads(user_data.amenities)
                    print user_data.amenities
                    if user_data.amenities != None:
                        for amenitits in user_data.amenities:
                            print amenitits
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
            t.rollback()
            ComFnObj.PrintException("API_BARN_POST")
            return ComFnObj.Responser([],str(e.message),"error")
        else:
            t.commit()
            return ComFnObj.Responser([],"Operation success","success")
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

                if user_data.opt == str(1):
                  print Query

                elif user_data.opt == str(2):
                    print Query
                else:
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
                user_data = web.input(opt='list', value=-1)
                if classid:
                    user_data.opt='single'
                    user_data.value=classid
                Classrooms = ComFnObj.GetClassrooms(user_data.opt, user_data.value)
                return ComFnObj.Responser(Classrooms, "Classroom list", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_CLASSROOM_GET")
            return ComFnObj.Responser(str(e.message), "Error in fetching Barn list", "error")

    def POST(self):

        try:

            ComFnObj = Commonfunctions()
            header = web.ctx.environ
            Authcode = header.get('HTTP_AUTHCODE')
            if ComFnObj.CheckAuth(Authcode):
                t = db.transaction()
                # user_data = json.loads(json_input)
                user_data = web.input(opt=1)
                BarnID=ComFnObj.Decrypt(user_data.barn)
                if user_data.opt == str(1):
                    entries = db.insert('tbl_classroom', barn_id_fk=BarnID, \
                                        classroom_capacity=user_data.capacity)
                elif user_data.opt == str(2):
                    entries = db.update('tbl_classroom', barn_id_fk=BarnID, \
                                        classroom_capacity=user_data.capacity,
                                        where="classroom_id='" + ComFnObj.Decrypt(str(user_data.id)) + "'")
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

                user_data = web.input(opt='list', value=-1)#barn,location,vacancy
                if tableid:
                    user_data.opt='single'
                    user_data.value=tableid
                Tables = ComFnObj.GetTables(user_data.opt, user_data.value)
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
                BarnID = ComFnObj.Decrypt(user_data.barn)
                TableData=ComFnObj.GetTables('numberbarn',[user_data.barn,user_data.number])
                if len(TableData)==0:

                    if user_data.opt == str(1):
                        entries = db.insert('tbl_table', barn_id_fk=BarnID, \
                                            table_number=user_data.number)
                    elif user_data.opt == str(2):
                        entries = db.update('tbl_table', barn_id_fk=BarnID, \
                                            table_number=user_data.number,
                                            where="table_id='" + ComFnObj.Decrypt(str(user_data.id)) + "'")
                    else:
                        return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
                else:
                    return ComFnObj.Responser([], "Same table number exist in the barn", "failure")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()

            ComFnObj.PrintException("API_TABLE_POST")
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
                ChairData = ComFnObj.GetChairs('numbertable', [user_data.table, user_data.number])
                if len(ChairData) == 0:
                    if user_data.opt == str(1):
                        entries = db.insert('tbl_chair', table_id_fk=TableID, \
                                            chair_number=user_data.number)
                    elif user_data.opt == str(2):
                        entries = db.update('tbl_chair', table_id_fk=TableID, \
                                            chair_number=user_data.number,
                                            where="table_id='" + ComFnObj.Decrypt(str(user_data.id)) + "'")
                    else:
                        return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
                else:
                    return ComFnObj.Responser([], "Same chair number exist in the table", "failure")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()

            ComFnObj.PrintException("API_CHAIR_POST")
            return ComFnObj.Responser([], str(e.message), "error")
        else:
            t.commit()
            return ComFnObj.Responser([], "Operation success", "success")

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
                user_data = web.input(opt='list', value=-1)
                if floorid:
                    user_data.opt='single'
                    user_data.value=floorid
                Floors = ComFnObj.GetFloors(user_data.opt, user_data.value)
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
                                        where="floor_id='" + ComFnObj.Decrypt(str(user_data.id)) + "'")
                else:
                    return ComFnObj.Responser([], "opt must be 1 or 2", "failure")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            t.rollback()

            ComFnObj.PrintException("API_FLOOR_POST")
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
                user_data = web.input(opt='list', value=-1)
                if exhibitid:
                    user_data.opt='single'
                    user_data.value=exhibitid
                Exhibits = ComFnObj.GetExhibits(user_data.opt, user_data.value)
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
                                        where="exhibit_id='" + ComFnObj.Decrypt(str(user_data.id)) + "'")
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

                user_data = web.input(opt='list', value=-1)
                if organiserid:
                    user_data.opt = 'single'
                    user_data.value = organiserid
                Organiser = ComFnObj.GetOrganisers(user_data.opt, user_data.value)
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
                print user_data.type
                if user_data.opt == str(1):
                    entries = db.insert('tbl_organiser', organisertype_id_fk=user_data.type,organiser_name=user_data.name,\
                                        organiser_description=user_data.description,\
                                        organiser_image=user_data.image)
                elif user_data.opt == str(2):
                    entries = db.update('tbl_organiser', organisertype_id_fk=user_data.type,organiser_name=user_data.name,\
                                        organiser_description=user_data.description,\
                                        organiser_image=user_data.image,
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
            user_data = web.input(opt='list', value=-1)
            if feestructureid:
                user_data.value = feestructureid
            print user_data
            FeeStructure = ComFnObj.GetFeeStructure(user_data.opt, user_data.value)
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
            print json.loads(user_data.structure)
            if user_data.opt == str(1):
                entries = db.insert('tbl_feestructure', feestructure_title=user_data.title,feestructure_fee=user_data.structure)
            elif user_data.opt == str(2):
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
                user_data = web.input(opt='list', value=-1)
                if courseid:
                    user_data.value = courseid
                Course = ComFnObj.GetCourse(user_data.opt, user_data.value)
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
                if user_data.opt == str(1):

                    entries = db.insert('tbl_course', course_title=user_data.title,course_desc=user_data.description,
    course_duration=user_data.duration,course_agelimit=user_data.agelimit,
    course_image=user_data.image,course_status=user_data.status,feestructure_id_fk=user_data.feestructure,
    coursetype_id_fk=user_data.coursetype,course_tags=user_data.tags)
                    locations=json.loads(user_data.location)
                    for location in locations:
                        db.insert('tbl_classcoursemap',course_id_fk=entries,barn_id_fk=ComFnObj.Decrypt(location))

                elif user_data.opt == str(2):
                    if courseid:
                        user_data.id = courseid
                        entries = db.update('tbl_course', course_title=user_data.title,course_desc=user_data.description,
    course_duration=user_data.duration,course_agelimit=user_data.agelimit,
    course_image=user_data.image,course_status=user_data.status,feestructure_id_fk=user_data.feestructure,
    coursetype_id_fk=user_data.coursetype,course_tags=user_data.tags,where="course_id='" + ComFnObj.Decrypt(str(user_data.id)) + "'")
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
                    print userid
                    if user_data.opt == str(1):
                        if ComFnObj.GetEnrolledCourse("isexist",[ComFnObj.Encrypt(str(userid)),courseid]):
                            raise ValueError("Already enrolled")

                        MapID=ComFnObj.Decrypt(ComFnObj.GetCourseClassMap("getidfromcnb",[user_data.location,courseid]))
                        entries = db.insert('tbl_enrolled',user_id_fk=userid,coursemap_id_fk=MapID,enrolled_status="STATUS")
                    elif user_data.opt == str(2):
                        MapID = ComFnObj.Decrypt(ComFnObj.GetCourseClassMap("getidfromcnb", [user_data.location, courseid]))
                        entries = db.update('tbl_enrolled',user_id_fk=userid,coursemap_id_fk=MapID,enrolled_status=user_data.status,
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
                print Profiles
                return ComFnObj.Responser(Profiles, "Profile list", "success")
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
                BarnID=ComFnObj.Decrypt(user_data.barn)
                if user_data.opt == str(1):
                    entries = db.insert('tbl_classroom', barn_id_fk=BarnID, \
                                        classroom_capacity=user_data.capacity)
                elif user_data.opt == str(2):
                    entries = db.update('tbl_classroom', barn_id_fk=BarnID, \
                                        classroom_capacity=user_data.capacity,
                                        where="classroom_id='" + ComFnObj.Decrypt(str(user_data.id)) + "'")
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
                user_data = web.input(opt='list', value=-1)
                if eventid:
                    user_data.value = eventid
                Event = ComFnObj.GetEvent(user_data.opt, user_data.value)
                return ComFnObj.Responser(Event, "Event", "success")
            else:
                return ComFnObj.Responser([], "Authcode failed", "failure")
        except Exception as e:
            ComFnObj.PrintException("API_COURSE_GET")

            return ComFnObj.Responser(str(e.message), "Error in  event list", "error")

    def POST(self,courseid):

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
                if user_data.opt == str(1):
                    entries = db.insert('tbl_event', event_title=user_data.title,event_decscription=user_data.description,
                    event_headerImg=user_data.image,event_start_date=user_data.start,event_end_date=user_data.end,
                    event_status=user_data.status,feestructure_id_fk=user_data.feestructure,
                    eventtype_id_fk=user_data.eventtype,event_venue_id=user_data.barn,event_tags=user_data.tags,organiser_id_fk=user_data.organiser)
                elif user_data.opt == str(2):
                    if courseid:
                        user_data.id = courseid
                    entries = db.update('tbl_event', event_title=user_data.title,event_decscription=user_data.description,
                    event_headerImg=user_data.image,event_start_date=user_data.start,event_end_date=user_data.end,
                    event_status=user_data.status,feestructure_id_fk=user_data.feestructure,
                    eventtype_id_fk=user_data.eventtype,event_venue_id=user_data.barn,event_tags=user_data.tags,organiser_id_fk=user_data.organiser,where="event_id='" + ComFnObj.Decrypt(str(user_data.id)) + "'")
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


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
else:
    application = web.application(urls, globals()).wsgifunc()