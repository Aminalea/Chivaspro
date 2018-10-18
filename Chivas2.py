# -*- coding: utf-8 -*-
from linepy import *
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup
from datetime import datetime, date
from gtts import gTTS
import time,random,sys,json,codecs,urllib,urllib3,requests,threading,glob,os,subprocess,multiprocessing,re,ast,shutil,calendar,tempfile,string,six,timeago
from random import randint

#Login Bots
client = LINE('EwVfiDXGy37yzRbO7vV8.LAGOirLjpgcOT3QvvspyEa.dz8mYMYLZfQxpsQ3mns8CawymBX7QbbU3vcJKtA6FYs=')
client.log("Auth Token : " + str(client.authToken))
oepoll = OEPoll(client)
clientmid = client.getProfile().mid




Bots=["u726174c3b25f9267053ab8050b7aca42","u6c2657d27eed2ebac6a961875201141f","u3e90db10578c0da3938f3fea1a173166","u95a8282119493c60a8b77a955523d878","uc1c86f9bad6ede76f6e22e1b59021f9c","uc28e7bc5e338853aebd63057c1ff7579","u7d902e538f00d0db02d4e4a27ce6220f","u80d7df3fbb139de4fa5478225269a8a8","u8d81426e0cf9d2dfc9a53010639fd1ba","ub18982a8cb38cf8b085fe8627257062b"]
Owner = ["uf1799cb51bd0ee8aa2cfe862cffbcc89","u533f29c24cab4fb44b0b315b4b2691eb","u71aaf512f0dc3ffe9a284fc761a8d2c2"]
KAC = [client]

#JSON Save
#with open('wait2.1.json', 'r') as fp:
    #wait2 = json.load(fp)
with open('wait1.json', 'r') as fp:
    wait = json.load(fp)
with open('ban1.json', 'r') as fp:
    ban = json.load(fp)

with open('Admin.json', 'r') as fp:
    Admin = json.load(fp)

with open('Staff.json', 'r') as fp:
    Staff = json.load(fp)



def download_page(url):
    version = (3,0)
    cur_version = sys.version_info
    if cur_version >= version:     
        import urllib.request    
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers = headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:                        
        import urllib2
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers = headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except:
            return"Page Not found"



def sendMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@zeroxyuuki "
    if mids == []:
        raise Exception("Invalid mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mids")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
        textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    client.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)





def NOTIFIED_UPDATE_GROUP(op):
    try:


        if op.param2 in Owner + Bots + Admin + Staff:
            return


        if op.param1 in wait["prourl"]:
            X = client.getGroup(op.param1)
            X.preventedJoinByTicket = True
            client.updateGroup(X)
            client.kickoutFromGroup(op.param1,[op.param2])
            ban["blacklist"][op.param2] = True
            banned()
        else:
            pass



        if op.param1 in wait['pname']:
            group = client.getGroup(op.param1)
            try:
                group.name = wait["pro_name"][op.param1]
                client.updateGroup(group)
                client.kickoutFromGroup(op.param1,[op.param2])
                ban["blacklist"][op.param2] = True
                banned()
            except:
                group.name = wait["pro_name"][op.param1]
                client.updateGroup(group)
                client.kickoutFromGroup(op.param1,[op.param2])
                ban["blacklist"][op.param2] = True
                banned()
    except:
        pass
oepoll.addOpInterruptWithDict({
    OpType.NOTIFIED_UPDATE_GROUP: NOTIFIED_UPDATE_GROUP
})



def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content

def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)
            page = page[end_content:]
    return items

def NOTIFIED_READ_MESSAGE(op):
    if op.param1 in wait2['readPoint']:
        wait2['ROM'][op.param1][op.param2] = op.param2
        wait2['setTime'][op.param1][op.param2] = op.createdTime
        backupjson2()
    else:
        pass

oepoll.addOpInterruptWithDict({
    OpType.NOTIFIED_READ_MESSAGE: NOTIFIED_READ_MESSAGE
})


def NOTIFIED_KICKOUT_FROM_GROUP(op):


        if op.param2 in Owner + Bots + Admin + Staff:
            return


        if op.param2 not in Owner + Bots + Admin + Staff:
             client.kickoutFromGroup(op.param1,[op.param2])
             ban["blacklist"][op.param2] = True
             banned()



        if op.param3 in Owner + Bots + Admin + Staff:
             client.findAndAddContactsByMid(op.param3)
             client.inviteIntoGroup(op.param1,[op.param3])

        if op.param3 in Owner + Bots + Admin + Staff:
             ban["blacklist"][op.param2] = True
             banned()



oepoll.addOpInterruptWithDict({
    OpType.NOTIFIED_KICKOUT_FROM_GROUP: NOTIFIED_KICKOUT_FROM_GROUP
})

def NOTIFIED_LEAVE_GROUP(op):



        if op.param2 in Owner + Admin + Staff:
             client.findAndAddContactsByMid(op.param2)
             client.inviteIntoGroup(op.param1,[op.param2])







oepoll.addOpInterruptWithDict({
    OpType.NOTIFIED_LEAVE_GROUP: NOTIFIED_LEAVE_GROUP
})




def NOTIFIED_INVITE_INTO_GROUP(op):
    try:

        if op.param2 in Owner + Bots + Admin:
             client.acceptGroupInvitation(op.param1)


        if op.param3 in ban["blacklist"]:
             client.cancelGroupInvitation(op.param1, [op.param3])

        if op.param3 in Owner + Bots + Admin + Staff:
            return


        if op.param2 in Owner + Bots + Admin + Staff:
            return
        if op.param1 in wait["protectinv"]:
            try:
                X = client.getGroup(op.param1)
                client.cancelGroupInvitation(op.param1, [op.param3])
                client.kickoutFromGroup(op.param1,[op.param2])
                ban["blacklist"][op.param2] = True
                banned()
            except:
                pass
    except:
        pass



        









oepoll.addOpInterruptWithDict({
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP
})





def NOTIFIED_ACCEPT_GROUP_INVITATION(op):

        if ban["blacklist"][op.param2] == True:
             client.kickoutFromGroup(op.param1,[op.param2])



oepoll.addOpInterruptWithDict({
    OpType.NOTIFIED_ACCEPT_GROUP_INVITATION: NOTIFIED_ACCEPT_GROUP_INVITATION
})





def RECEIVE_MESSAGE(op):
            msg = op.message
            clienttxt = msg.text
            msg_id = msg.id
            sky = msg.to
            sender = msg._from


            if msg.contentType == 7:
                if wait["Addsticker"] == True:
                 try:
                    wait["Sticker"][wait["Img"]] = msg.contentMetadata
                    client.sendMessage(sky, "「 Sticker 」\n✧ Type: Add Sticker ♪\n✧ Status: Success Add Sticker ♪")
                 except Exception as e:
                    client.sendMessage(sky,"「 Respond Error 」\n"+str(e))
                wait["Img"] = {}
                wait["Addsticker"] = False
                backupjson()
            if msg.contentType == 1:
                if wait["ChangeDP"] == True:
                    try:
                        client.downloadObjectMsg(msg_id,'path','dataSeen/dpku.jpg')
                        client.updateProfilePicture('dataSeen/dpku.jpg')
                        client.sendMessage(sky,"「 Pictures 」\n✧ Type: Change Disiplay Pictures ♪\n✧ Status: Disiplay Picture Has Been Changed ♪")
                    except Exception as e:
                        client.sendMessage(sky,"「 Respond Error 」\n"+str(e))
                    wait["ChangeDP"] = False
                if wait["ChangeGP"] == True:
                    try:
                        client.downloadObjectMsg(msg_id,'path','dataSeen/dpgrup.jpg')
                        client.updateGroupPicture(sky,'dataSeen/dpgrup.jpg')
                        client.sendMessage(sky,"「 Pictures 」\n✧ Type: Change Group Pictures ♪\n✧ Status: Group Picture Has Been Changed ♪")
                    except Exception as e:
                        client.sendMessage(sky,"「 Respond Error 」\n"+str(e))
                    wait["ChangeGP"] = False



            if msg.contentType == 13:
             if sender in Admin + Owner:
                if wait["wblacklist"] == True:
                    if msg.contentMetadata["mid"] in ban["blacklist"]:
                        client.sendMessage(msg.to,"Not in My blacklist")
                        wait["wblacklist"] = False
                    else:
                        ban["blacklist"][msg.contentMetadata["mid"]] = True
                        wait["wblacklist"] = False
                        banned()
                        client.sendMessage(msg.to,"Done")
                if wait["dblacklist"] == True:
                    if msg.contentMetadata["mid"] in ban["blacklist"]:
                        del ban["blacklist"][msg.contentMetadata["mid"]]
                        banned()
                        client.sendMessage(msg.to,"Done")
                        wait["dblacklist"] = False
                    else:
                        wait["dblacklist"] = False
                        client.sendMessage(msg.to,"Done")


                if wait["alist"] == True:
                    if msg.contentMetadata["mid"] in wait["invitelist"]:
                        key = ("mid")
                        client.sendMessage(msg.to,"error")
                        wait["alist"] = False
                    else:
                        wait["invitelist"][msg.contentMetadata["mid"]] = True
                        wait["alist"] = False
                        midd = msg.contentMetadata["mid"]
                        client.findAndAddContactsByMid(midd)
                        client.inviteIntoGroup(msg.to,[midd])
                        client.sendMessage(msg.to,"Done")








            if msg.contentType == 0:


             if sender in Admin + Owner:
               if clienttxt.lower() == "pro2help":help(sky,'')
               if clienttxt.lower() == "blacklist":defblacklist(sky,'')
               if clienttxt.lower() == "pro2 speed":speed(sky,'')
               if clienttxt.lower() == "proinv on":
                    wait['pro_invite'][msg.to] = client.getGroup(msg.to).name
                    protectinvon(sky)
               if clienttxt.lower() == "kick":kick(sky,'')
               if clienttxt.lower() == "lurking":lurking(sky,'')
               if clienttxt.lower() == "proinv off":
                    del wait['pro_invite'][msg.to]
                    protectinvoff(sky)
               if clienttxt.lower() == "pro2 changedp":changedp(sky)
               if clienttxt.lower() == "pro2 changegp":changegp(sky)
               if clienttxt.lower() == "welcome on":welcomeon(sky)
               if clienttxt.lower() == "leave on":leaveon(sky)
               if clienttxt.lower() == "welcome off":welcomeoff(sky)
               if clienttxt.lower() == "leave off":leaveoff(sky)
               if clienttxt.lower() == "pro2 list sticker":liststicker(sky)
               if clienttxt.lower() == "pqr on":
                    wait['pro_qr'][msg.to] = client.getGroup(msg.to).name
                    qron(sky)
               if clienttxt.lower() == "pqr off":
                    del wait['pro_qr'][msg.to]
                    protectinvoff(sky)
               if clienttxt.lower() == "protect":defprotect(sky,'')
               if clienttxt.lower() == 'restart':restart_program(sky,'')
               if clienttxt.lower() == 'pro2 blist':blist(sky,'')


             if clienttxt.lower() == 'owner':
                  client.sendMessage(sky,text=None,contentMetadata={'mid': 'u533f29c24cab4fb44b0b315b4b2691eb'} , contentType=13)


             if clienttxt.lower() == 'pro2 adminlist':
                  if sender in Admin + Owner:
                   if Admin == []:
                    client.sendMessage(msg.to,"The adminlist is empty")
                   else:
                    client.sendMessage(msg.to,"Admin list:")
                    mc = ""
                    for mi_d in Admin:
                        mc += "->" +client.getContact(mi_d).displayName + "\n"
                    client.sendMessage(msg.to,mc)


             if clienttxt.lower() == 'pro2 stafflist':
                  if sender in Admin + Owner:
                   if Staff == []:
                    client.sendMessage(msg.to,"The staff is empty")
                   else:
                    client.sendMessage(msg.to,"Staff list:")
                    mc = ""
                    for mi_d in Staff:
                        mc += "->" +client.getContact(mi_d).displayName + "\n"
                    client.sendMessage(msg.to,mc)


             if clienttxt.lower() == 'pro2 plist':
                  if sender in Admin + Owner:
                            if wait["pro_name"] == {}:
                                      client.sendMessage(sky, "No Groupt in protect name")
                            else: 
                                 groups = client.groups
                                 ret_ = "╔══[ Protect name listgroup ]"
                                 no = 0 + 1
                                 for gid in wait["pro_name"]:
                                    group = client.getGroup(gid)
                                    ret_ += "\n╠ {}. {}".format(str(no), str(group.name))
                                    no += 1
                                 ret_ += "\n╚══[ Total {} Groups ]".format(str(len(wait["pro_name"])))
                                 client.sendMessage(sky, str(ret_))

                            if wait["pro_invite"] == {}:
                                      client.sendMessage(sky, "No Groupt in protect invite")
                            else: 
                                 groups = client.groups
                                 ret_ = "╔══[ Protect invite listgroup ]"
                                 no = 0 + 1
                                 for gid in wait["pro_invite"]:
                                    group = client.getGroup(gid)
                                    ret_ += "\n╠ {}. {}".format(str(no), str(group.name))
                                    no += 1
                                 ret_ += "\n╚══[ Total {} Groups ]".format(str(len(wait["pro_invite"])))
                                 client.sendMessage(sky, str(ret_))


                            if wait["pro_qr"] == {}:
                                      client.sendMessage(sky, "No Groupt in protect link")
                            else: 
                                 groups = client.groups
                                 ret_ = "╔══[ Protect link listgroup ]"
                                 no = 0 + 1
                                 for gid in wait["pro_qr"]:
                                    group = client.getGroup(gid)
                                    ret_ += "\n╠ {}. {}".format(str(no), str(group.name))
                                    no += 1
                                 ret_ += "\n╚══[ Total {} Groups ]".format(str(len(wait["pro_qr"])))
                                 client.sendMessage(sky, str(ret_))

             elif msg.text.startswith("Groupmember "):
                  if sender in Admin + Owner:
                            text = msg.text.split()
                            number = text[1]
                            if number.isdigit():
                                groups = client.getGroupIdsJoined()
                                if int(number) < len(groups) and int(number) >= 0:
                                    groupid = groups[int(number)]
                                    group = client.getGroup(groupid)
                                    if group.creator:
                                        creator = group.creator
                                    else:
                                        creator.displayName = "unknown"
                                    number = 1
                                    membertext = "═══════════════════\nName: %s\nCreator: %s\n═════[List Member]═════"%(group.name,creator.displayName)
                                    for member in group.members:
                                        membertext += "\n%s. %s"%(number,member.displayName)
                                        number += 1
                                    client.sendMessage(msg.to,membertext)

             elif msg.text.startswith("pro2join "):
                  if sender in Admin + Owner:
                            text = msg.text.split()
                            number = text[1]
                            if number.isdigit():
                                groups = client.getGroupIdsJoined()
                                if int(number) < len(groups) and int(number) >= 0:
                                    groupid = groups[int(number)]
                                    group = client.getGroup(groupid)
                                    target = sender
                                    try:
                                        client.getGroup(groupid)
                                        client.inviteIntoGroup(groupid, [target])
                                        client.sendMessage(msg.to,"Succes invite to " + str(group.name))
                                    except:
                                        client.sendMessage(msg.to,"I no there baby")


             elif msg.text.startswith("leave "):
                  if sender in Admin + Owner:
                            text = msg.text.split()
                            number = text[1]
                            if number.isdigit():
                                groups = client.getGroupIdsJoined()
                                if int(number) < len(groups) and int(number) >= 0:
                                    groupid = groups[int(number)]
                                    group = client.getGroup(groupid)
                                    target = sender
                                    try:
                                        client.getGroup(groupid)
                                        client.leaveGroup(groupid)
                                        client.sendMessage(msg.to,"Succes leave in " + str(group.name))
                                    except:
                                        client.sendMessage(msg.to,"I no there baby")


             elif msg.text.startswith("protect "):
                  if sender in Admin + Owner:
                            text = msg.text.split()
                            number = text[1]
                            if number.isdigit():
                                groups = client.getGroupIdsJoined()
                                if int(number) < len(groups) and int(number) >= 0:
                                    groupid = groups[int(number)]
                                    group = client.getGroup(groupid)
                                    target = sender
                                    try:
                                        client.getGroup(groupid)
                                        wait['pro_invite'][groupid] = client.getGroup(groupid).name
                                        protectinvon(groupid)
                                        wait['pro_qr'][groupid] = client.getGroup(groupid).name
                                        qron(groupid)
                                        wait['pname'].append(groupid)
                                        wait['pro_name'][groupid] = client.getGroup(groupid).name
                                        backupjson()
                                        client.sendMessage(msg.to,"Succes protect group " + str(group.name))
                                    except:
                                        client.sendMessage(msg.to,"I no there baby")


             elif msg.text.startswith("unprotect "):
                  if sender in Admin + Owner:
                            text = msg.text.split()
                            number = text[1]
                            if number.isdigit():
                                groups = client.getGroupIdsJoined()
                                if int(number) < len(groups) and int(number) >= 0:
                                    groupid = groups[int(number)]
                                    group = client.getGroup(groupid)
                                    target = sender
                                    try:
                                        client.getGroup(groupid)
                                        del wait['pro_invite'][groupid] 
                                        protectinvoff(groupid)
                                        del wait['pro_qr'][groupid] 
                                        qroff(groupid)
                                        wait['pname'].remove(groupid)
                                        del wait['pro_name'][groupid] 
                                        backupjson()
                                        client.sendMessage(msg.to,"Succes unprotect group " + str(group.name))
                                    except:
                                        client.sendMessage(msg.to,"I no there baby")



             if clienttxt.lower() == 'pro2 glist':
                                    groups = client.groups
                                    ret_ = "╔══[ Group List ]"
                                    no = 0 
                                    for gid in groups:
                                        group = client.getGroup(gid)
                                        ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                                        no += 0 + 1
                                    ret_ += "\n╚══[ Total {} Groups ]".format(str(len(groups)))
                                    client.sendMessage(sky, str(ret_))


             if "Admin add @" in msg.text:
                if sender in Owner:
                    print ("[Command]admin add executing")
                    _name = msg.text.replace("Admin add @","")
                    _nametarget = _name.rstrip('  ')
                    gs = client.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        client.sendMessage(msg.to,"Contact not found.")
                    else:
                        for target in targets:
                            try:
                                Admin.append(target)
                                with open('Admin.json', 'w') as fp:
                                    json.dump(Admin, fp, sort_keys=True, indent=4)
                                client.sendMessage(msg.to,"Admin Added")
                            except:
                                pass
                    print ("[Command]Admin add executed")
                else:
                    client.sendMessage(msg.to,"Command denied.")
                    client.sendMessage(msg.to,"Creator permission required.")

             if "Expel admin @" in msg.text:
                if sender in Owner:
                    print ("[Command]Admin remove executing")
                    _name = msg.text.replace("Expel admin @","")
                    _nametarget = _name.rstrip('  ')
                    gs = client.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        client.sendMessage(msg.to,"Contact not found")
                    else:
                        for target in targets:
                            try:
                                Admin.remove(target)
                                with open('Admin.json', 'w') as fp:
                                    json.dump(Admin, fp, sort_keys=True, indent=4)
                                client.sendMessage(msg.to,"Removed to the admin list")
                            except:
                                pass
                    print ("[Command]admin remove executed")
                else:
                    client.sendMessage(msg.to,"Command denied.")
                    client.sendMessage(msg.to,"Creator permission required.")



             if "Staff add @" in msg.text:
                if sender in Admin + Owner:  
                    print ("[Command]admin add executing")
                    _name = msg.text.replace("Staff add @","")
                    _nametarget = _name.rstrip('  ')
                    gs = client.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        client.sendMessage.sendText(msg.to,"Contact not found.")
                    else:
                        for target in targets:
                            try:
                                Staff.append(target)
                                with open('Staff.json', 'w') as fp:
                                    json.dump(Staff, fp, sort_keys=True, indent=4)
                                client.sendMessage(msg.to,"Staff Added")
                            except:
                                pass
                    print ("[Command]Admin add executed")
                else:
                    client.sendMessage(msg.to,"Command denied.")
                    client.sendMessage(msg.to,"Creator permission required.")

             if "Expel staff @" in msg.text:
                if sender in Owner:
                    print ("[Command]staff remove executing")
                    _name = msg.text.replace("Expel staff @","")
                    _nametarget = _name.rstrip('  ')
                    gs = client.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        client.sendMessage(msg.to,"Contact not found")
                    else:
                        for target in targets:
                            try:
                                Staff.remove(target)
                                with open('Staff.json', 'w') as fp:
                                    json.dump(Staff, fp, sort_keys=True, indent=4)
                                client.sendMessage(msg.to,"Removed to the admin list")
                            except:
                                pass
                    print ("[Command]admin remove executed")
                else:
                    client.sendMessage(msg.to,"Command denied.")
                    client.sendMessage(msg.to,"Creator permission required.")


             if clienttxt.lower() == 'proname':
                  if sender in Admin + Owner:
                    profile = client.getProfile()
                    text = profile.displayName + ""
                    client.sendMessage(msg.to, "Kenzi Stay Bos")


             if clienttxt.lower() == 'pro2 getban':
                  if sender in Admin + Owner:
                            if ban["blacklist"] == {}:
                                client.sendMessage(msg.to,"No have blacklist")
                            else:
                                client.sendMessage(msg.to,"List of blacklist")
                                h = ""
                                for i in ban["blacklist"]:
                                    client.sendContact(sky, i)


             if clienttxt.lower() == 'pro2 @bye':
                  if sender in Admin + Owner:
                                ginfo = client.getGroup(msg.to)
                                try:
                                    client.leaveGroup(msg.to)
                                except:
                                    pass



             if clienttxt.lower() == 'pro bye':
                  if sender in Admin + Owner:
                                ginfo = client.getGroup(msg.to)
                                try:
                                    client.leaveGroup(msg.to)
                                except:
                                    pass


             if clienttxt.lower() == 'prosp':
                  if sender in Admin + Owner:
                    start = time.time() /3
                    client.sendMessage(msg.to, "??Tunggu??........??")
                    elapsed_time = time.time() /3 - start
                    client.sendMessage(msg.to, "%sseconds" % (elapsed_time))





             if clienttxt.lower() == 'pro2 lurk on':
               if sender in Admin + Owner:
                if msg.to in wait2['readPoint']:
                    client.sendMessage(sky, "「 Lurking 」\n✧ Status: Lurk Already Set")
                else:
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['setTime'][msg.to]
                    except:
                        pass
                    wait2['readPoint'][msg.to] = msg.id
                    wait2['setTime'][sky]  = {}
                    wait2['ROM'][sky] = {}
                    backupjson2()
                    client.sendMessage(sky, "「 Lurking 」\n✧ Status: Lurk Point Has Been Set")


             if clienttxt.lower() == 'pro invite':
               if sender in Admin + Owner:
                     wait["alist"] = True
                     client.sendMessage(msg.to,"send contact")



             if 'Ban:on' in clienttxt:
               if sender in Admin + Owner:
                     wait["wblacklist"] = True
                     client.sendMessage(msg.to,"send contact")



             if 'Unban:on' in clienttxt:
               if sender in Admin + Owner:
                     wait["dblacklist"] = True
                     client.sendMessage(msg.to,"send contact")



             if clienttxt.lower() == 'pro2 lurk off':
               if sender in Admin + Owner:
                if msg.to not in wait2['readPoint']:
                    client.sendMessage(sky, "「 Lurking 」\n✧ Status: Lurk Already Off")
                else:
                    try:
                       del wait2['readPoint'][msg.to]
                       del wait2['setTime'][msg.to]
                    except:
                       pass
                    client.sendMessage(sky, "「 Lurking 」\n✧ Status: Lurk Point Has Been Delete")



             if clienttxt.lower() == 'pro2 lurk result':
               if sender in Admin + Owner:
                try:
                  if sky in wait2['readPoint']:
                      chiya = []
                      for rom in wait2["ROM"][sky].items():
                          chiya.append(rom[1])
                      sidertag(sky,'',chiya)
                      wait2['setTime'][sky]  = {}
                      wait2['ROM'][sky] = {}
                      backupjson2()
                  else:
                      client.sendMessage(sky, "「 Lurking 」\n✧ Status: Lurk Point Disabled")
                except Exception as e:
                  client.sendMessage(sky, "Error: "+str(e))

             if "kickall" in clienttxt:
               if sender in Admin + Owner:
                    _name = clienttxt.replace("kickall","")
                    gs = client.getGroup(sky)
                    client.sendMessage(sky,"Just some casual cleansing ")
                    targets = []
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                          if not target in Bots + Admin + Owner:
                               try:
                                client.kickoutFromGroup(sky,[target])
                               except:
                                client.sendMessage(sky,"Group cleanse")


             if clienttxt.lower() == 'killbl':
               if sender in Admin + Owner:
                try:
                    group = client.getGroup(sky)
                    gMembers = [contact.mid for contact in group.members]
                    matched_list = []
                    for tag in ban["blacklist"]:
                        matched_list+=filter(lambda str: str == tag, gMembers)
                    if matched_list == []:
                        client.sendMessage(msg.to,"There was no blacklist user")
                        return
                    for jj in matched_list:
                        client.kickoutFromGroup(sky,[jj])
                        client.sendMessage(sky,"「 Blacklist 」\n✧ Type: Kick Blacklist User\n✧ Status: Success Kick Blacklist User")
                except Exception as e:
                    client.sendMessage(sky, "Error: "+ str(e))
#==============================[ Message Command ]==============================#
             if "bye " in clienttxt:
               if sender in Admin + Owner:
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            client.kickoutFromGroup(sky,[target])
                        except Exception as e:
                            client.sendMessage(sky,str(e))
                else:
                    client.sendMessage(sky,"「 Kick 」\nYou need to mention a user♪")
#==============================[ Message Command ]==============================#
             if clienttxt.lower() == "pro2 openqr":
              if sender in Admin + Owner:
               if msg.toType == 2:
                x = client.getGroup(sky)
                if x.preventedJoinByTicket == True:
                   x.preventedJoinByTicket = False
                   Ticket = client.reissueGroupTicket(sky)
                   client.updateGroup(x)
                   client.sendMessage(sky,'「 URL Group 」\n✧ Type: Open URL Group\n✧ URL Group: 「 http://line.me/R/ti/g/'+Ticket+" 」\n✧ Status: Success Open URL Group")
                else:
                   client.updateGroup(x)
                   client.sendMessage(sky,'「 URL Group 」\n✧ Type: Open URL Group\n✧ Status: URL Group URL Group Already Open')
#==============================[ Message Command ]==============================#
             if clienttxt.lower() == "pro2 closeqr":
              if sender in Admin + Owner:
               if msg.toType == 2:
                x = client.getGroup(sky)
                if x.preventedJoinByTicket == False:
                   x.preventedJoinByTicket = True
                   client.updateGroup(x)
                   client.sendMessage(sky,'「 URL Group 」\n✧ Type: Close URL Group\n✧ Status: Success Close URL Group')
                else:
                   client.updateGroup(x)
                   client.sendMessage(sky,'「 URL Group 」\n✧ Type: Close URL Group\n✧ Status: URL Group URL Group Already Close')



#==============================[ Message Command ]==============================#
             if "Ubl " in clienttxt:
               if sender in Admin + Owner:
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        delbl(sky,target)
                else:
                    separate = clienttxt.split(" ")
                    text = clienttxt.replace(separate[0] + " ","")
                    cond = text.split("~")
                    if len(cond) == 2:
                            num = int(cond[1])
                            if num <= len(ban["blacklist"]):
                                bl = ban["blacklist"][num-1]
                                delbl(sky,bl)

             if "Abl " in clienttxt:
               if sender in Admin + Owner:
                if 'MENTION' in msg.contentMetadata.keys()!=None:
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        addbl(sky,target)



             if clienttxt.startswith('pro1 delstick'):
               if sender in Admin + Owner:
                separate = clienttxt.split("er ")
                text = clienttxt.replace(separate[0]+"er ","")
                del wait["Sticker"][text]
                del wait["Img"]
                backupjson()
                client.sendMessage(sky," 「 Sticker 」\n✧ Type: Delete Sticker\nMessage Sticker: "+text+"\n✧ Status: Sticker Has Been Delete")
#==============================[ Message Command ]==============================#
             if clienttxt.startswith('pro1 addstick'):
               if sender in Admin + Owner:
                separate = clienttxt.split("er ")
                text = clienttxt.replace(separate[0]+"er ","")
                wait["Sticker"][text] = '%s' % text
                wait["Img"] = '%s' % text
                wait["Addsticker"] = True
                client.sendMessage(sky, " 「 Sticker 」\n✧ Type: Add Sticker ♪\n✧ Status: Send Sticker... ♪")
#==============================[ Message Command ]==============================#
             if 'pname ' in clienttxt:
               if sender in Admin + Owner:
                spl = clienttxt.replace('pname ','')
                grup = client.getGroup(sky)
                namagrup = grup.name
                gcreator = grup.creator.mid
                if spl == 'on':
                    if sky in wait['pname']:
                        a="「 Protection Protection name group 」\n\n✧ Type: Name Lock\n✧ Name Group: "+namagrup+"\n✧ Creator Group: "
                        zx = ""
                        zxc = a.title()
                        zx2 = []
                        pesan2 = "@a"" "
                        xlen = str(len(zxc))
                        xlen2 = str(len(zxc)+len(pesan2)-1)
                        zx = {'S':xlen, 'E':xlen2, 'M':gcreator}
                        zx2.append(zx)
                        zxc += pesan2
                        text = zxc+"\n✧ Status: Success Enabled Lock Group Name"
                        contentMetadata = {'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}
                        client.sendMessage(sky, text, contentMetadata)
                    else:
                        a="「 Protection name group 」\n\n✧ Type: Name Lock\n✧ Name Group: "+namagrup+"\n✧ Creator Group: "
                        zx = ""
                        zxc = a.title()
                        zx2 = []
                        pesan2 = "@a"" "
                        xlen = str(len(zxc))
                        xlen2 = str(len(zxc)+len(pesan2)-1)
                        zx = {'S':xlen, 'E':xlen2, 'M':gcreator}
                        zx2.append(zx)
                        zxc += pesan2
                        text = zxc+"\n✧ Status: Already Enabled Lock Group Name"
                        contentMetadata = {'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}
                        client.sendMessage(sky, text, contentMetadata)
                        wait['pname'].append(sky)
                        wait['pro_name'][msg.to] = client.getGroup(msg.to).name
                        backupjson()
                if spl == 'off':
                    if sky in wait['pname']:
                        a="「 Protection Protection name group 」\n\n✧ Type: Name Lock\n✧ Name Group: "+namagrup+"\n✧ Creator Group: "
                        zx = ""
                        zxc = a.title()
                        zx2 = []
                        pesan2 = "@a"" "
                        xlen = str(len(zxc))
                        xlen2 = str(len(zxc)+len(pesan2)-1)
                        zx = {'S':xlen, 'E':xlen2, 'M':gcreator}
                        zx2.append(zx)
                        zxc += pesan2
                        text = zxc+"\n✧ Status: Success Disabled Lock Group Name"
                        contentMetadata = {'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}
                        client.sendMessage(sky, text, contentMetadata)
                        wait['pname'].remove(sky)
                        del wait['pro_name'][msg.to]
                        backupjson()
                    else:
                        a="「 Protection Protection name group 」\n\n✧ Type: Name Lock\n✧ Name Group: "+namagrup+"\n✧ Creator Group: "
                        zx = ""
                        zxc = a.title()
                        zx2 = []
                        pesan2 = "@a"" "
                        xlen = str(len(zxc))
                        xlen2 = str(len(zxc)+len(pesan2)-1)
                        zx = {'S':xlen, 'E':xlen2, 'M':gcreator}
                        zx2.append(zx)
                        zxc += pesan2
                        text = zxc+"\n✧ Status: Already Disabled Lock Group Name"
                        contentMetadata = {'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}
                        client.sendMessage(sky, text, contentMetadata)
#==============================[ Message Command ]==============================#
             if clienttxt in wait["Sticker"]:
               if sender in Admin + Owner:
                try:
                    client.sendMessage(sky,text=None,contentMetadata=wait['Sticker'][clienttxt], contentType=7)
                except Exception as e:
                    client.sendMessage(sky,"「 Respond Error 」\n"+str(e))



oepoll.addOpInterruptWithDict({
   OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE
})




def speed(to, text):
    start = time.time() /3
    client.sendMessage(to, "「Loading ✪✪✪✪✪」")
    elapsed_time = time.time() /3 - start
    client.sendMessage(to,"「 Speed 」\n✧ Type: Check Speed bots ♪\n✧ Speed: {}s".format(str(elapsed_time)))
def qron(to):
    if to in wait["prourl"]:
        client.sendMessage(to,"Protect URL turn on")
    else:
        wait["prourl"].append(to)
        backupjson()
        client.sendMessage(to,"Protect URL Has Been Enabled")
def qroff(to):
    if to not in wait["prourl"]:
        client.sendMessage(to,"「 Link Protection 」\nProtect Link set to off")
    else:
        wait["prourl"].remove(to)
        backupjson()
        client.sendMessage(to,"「 Link Protection 」\nProtect Link already off")
def changedp(to):
    wait["ChangeDP"] = True
    client.sendMessage(to,"「 Pictures 」\n✧ Type: Change Disiplay Picture ♪\n✧ Status: Send Images... ♪")
def changegp(to):
    wait["ChangeGP"] = True
    client.sendMessage(to,"「 Pictures 」\n✧ Type: Change Group Picture ♪\n✧ Status: Send Image.... ♪")
def help(to, text):
    a="╔═════[ ??Help Protect?? ]\n╠ " \
    +"pro Speed\n╠ " \
    +"Proinv 「 On/Off 」\n╠ " \
    +"pro2 Lurk 「 On/Off 」\n╠ " \
    +"Pname 「 On/Off 」\n╠ " \
    +"Welcome 「 On/Off 」\n╠ " \
    +"Leave 「 On/Off 」\n╠ " \
    +"Pqr 「 On/Off 」\n╠ " \
    +"pro2 Changedp\n╠ " \
    +"pro2 Changegp\n╠ " \
    +"pro2 List Sticker\n╠ " \
    +"Reboot\n╠ " \
    +"pro2 Blist\n╠ " \
    +"pro2 Lurk Result\n╠ " \
    +"pro2 Kickall\n╠ " \
    +"pro2 Killbl\n╠ " \
    +"pro2 Openqr\n╠ " \
    +"pro2 Closeqr\n╠ " \
    +"pro2 Addsticker 「 Title 」\n╠ " \
    +"pro2 Delsticker 「 Title 」\n╠ " \
    +"pro Bye 「 @ 」\n╠ " \
    +"Abl 「 @ 」\n╠ " \
    +"Ubl 「 @ 」\n╚═════" \
    +"[ ??TeamBots Joker killer??  ]"
    client.sendMessage(to, a)




def leaveon(to):
    try:
     if to not in wait["left"]:
        wait["left"].append(to)
        client.sendMessage(to,"「 Leave 」\n✧ Type: Notified Leave Members\n✧ Status: Leave Notified Has Been Enabled")
     else:
        client.sendMessage(to,"「 Leave 」\n✧ Type: Notified Leave Members\n✧ Status: Already Enabled Leave Notified")
    except Exception as error:
        print(str(error))
def leaveoff(to):
    try:
     if to in wait["left"]:
        wait["left"].remove(to)
     else:
        client.sendMessage(to,"「 Leave 」\n✧ Type: Notified Leave Members\n✧ Status: Already Disabled Leave Notified")
    except Exception as error:
        print(str(error))
def welcomeon(to):
    try:
     if to not in wait["welcome"]:
        wait["welcome"].append(to)
        client.sendMessage(to,"「 Welcome 」\n✧ Type: Notified Welcome Join Members\n✧ Status: Welcome Notified Has Been Enabled")
     else:
        client.sendMessage(to,"「 Welcome 」\n✧ Type: Notified Welcome Join Members\n✧ Status: Already Enabled Welcome Notified")
    except Exception as error:
        print(str(error))
def welcomeoff(to):
    try:
     if to in wait["welcome"]:
        wait["welcome"].remove(to)
        client.sendMessage(to,"「 Welcome 」\n✧ Type: Notified Welcome Join Member\n✧ Status: Welcome Notified Has Been Disabled")
     else:
        client.sendMessage(to,"「 Welcome 」\n✧ Type: Notified Welcome Join Member\n✧ Status: Already Disabled Welcome Notified")
    except Exception as error:
        print(str(error))
def blist(to, text):
    if ban["blacklist"] == {}:
        client.sendMessage(to,"「 Blacklist 」\nStatus: No User Blacklist")
    else:
        pass
        mc = ""
        for mi_d in ban["blacklist"]:
            mc += "✧ " +client.getContact(mi_d).displayName + "\n"
        client.sendMessage(to,"User Blacklist: \n" + mc + "\nTotal User Blacklist: " + str(len(ban["blacklist"])))
def restart_program(to, text):
    client.sendMessage(to,"「 Restart Program 」\n✧ Type: Restart Bots\n✧ Status: Restarting...")
    python = sys.executable
    os.execl(python, python, * sys.argv)
def liststicker(to):
  try:
    if wait["Sticker"] == {}:
        client.sendMessage(to,"「 Sticker List 」\nNo Sticker")
    else:
        num=1
        msgs=" 「 List Sticker 」"
        for a in wait["Sticker"]:
            msgs+="\n%i. %s" % (num, a)
            num=(num+1)
        msgs+="\n\nTotal Sticker: %i" % len(wait["Sticker"])
        client.sendMessage(to, msgs)
  except Exception as e:
     client.sendMessage("「Respond Error」\n"+str(e))
def addbl(to,mid):
    if mid not in ban["blacklist"]:
        ban["blacklist"][mid] = True
        banned()
        client.sendMessage(to,"Success Blacklist Target")
    else:
        client.sendMessage(to,"Already To Blacklist Target")
def protectinvon(to):
    try:
     if to not in wait["protectinv"]:
        wait["protectinv"].append(to)
        backupjson()
        client.sendMessage(to, "Enabled Protect Invite")
     else:
        client.sendMessage(to, "Protect Invite Has Been Enabled")
    except Exception as e:
        print("Error: "+str(e))
def protectinvoff(to):
    try:
     if to in wait["protectinv"]:
        wait["protectinv"].remove(to)
        backupjson()
        client.sendMessage(to, "Disabled Protect Invite")
     else:
        client.sendMessage(to, "Protect Invite Has Been Disabled")
    except Exception as e:
        print("Error: "+str(e))
def sidertag(to, text='', dataMid=[]):
    now = datetime.now()
    arr = []
    list_text='「 Reader 」\n Lurkers: %i People'%(len(dataMid))
    if '[list]' in text:
        i=0
        for l in dataMid:
            list_text+='\n@[list-'+str(i)+']'
            i=i+1
        text=text.replace('[list]', list_text)
    elif '[list-' in text:
        text=text
    else:
        i=0
        no=0
        for l in dataMid:
            z = ""
            chiya = []
        for rom in wait2["setTime"][to].items():
            chiya.append(rom[1])
        for b in chiya:
            a = str(timeago.format(now,b/1000))
            no+=1
            list_text+='\n\n '+str(no)+'. @[list-'+str(i)+'] 「 '+a+" 」"
            i=i+1
        list_text +="\n\n Lurk Time: "+datetime.now().strftime('%H:%M:%S')
        text=text+list_text
    i=0
    for l in dataMid:
        mid=l
        name='@[list-'+str(i)+']'
        ln_text=text.replace('\n',' ')
        if ln_text.find(name):
            line_s=int( ln_text.index(name) )
            line_e=(int(line_s)+int( len(name) ))
        arrData={'S': str(line_s), 'E': str(line_e), 'M': mid}
        arr.append(arrData)
        i=i+1
    contentMetadata={'MENTION':str('{"MENTIONEES":' + json.dumps(arr).replace(' ','') + '}')}
    client.sendMessage(to, text, contentMetadata)
def delbl(to,mid):
    try:
     if mid in ban["blacklist"]:
        del ban["blacklist"][mid]
        banned()
        client.sendMessage(to,"Success Unblacklist")
     else:
        client.sendMessage(to,"Not in Blacklist")
    except Exception as e:
        print("Error: "+str(e))
def backupjson():
    with open('wait1.json', 'w') as fp:
        json.dump(wait, fp, sort_keys=True, indent=4)
def backupjson2():
    with open('wait2.1.json', 'w') as fp:
        json.dump(wait2, fp, sort_keys=True, indent=4)
def banned():
    with open('ban1.json', 'w') as fp:
        json.dump(ban, fp, sort_keys=True, indent=4)
while True:
    oepoll.trace()
