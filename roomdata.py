import roominfo


class User:
    def __init__(self, uid, name, gender, isadmin, level, fanlv, diamond):
        self.uid = uid
        self.name = name
        self.gender = gender
        self.isadmin = isadmin
        self.level = level
        self.fanlv = fanlv
        self.diamond = diamond

    def __repr__(self):
        return f"User(uid={self.uid}, name='{self.name}', gender={self.gender}, isadmin={self.isadmin}, level={self.level}, fanlv={self.fanlv}, diamond={self.diamond}"


# 礼物人员统计
members = []


# 使用sorted()函数对members列表进行排序，排序依据是每个User实例的gift属性
def sortmembers():
    global members
    members = sorted(members, key=lambda user: user.gift)


# 打印排序后的members列表
#for member in sorted_members:
#    print(member)


class Gift:
    def __init__(self, uid, name, count):
        self.uid = uid
        self.name = name
        self.count = count

    def __repr__(self):
        return f"Gift(uid={self.uid}, name = '{self.name})', count = {self.count}"


#礼物分类计数
gifts = []

#价值总数
diamonds = 0


def newgift(uid, name, gender, isadmin, level, fanlv, giftid, giftname, count, diamond):
    global members, diamonds
    diamonds += diamond

    ret = [user for user in members if user.uid == uid]

    #累计观众打赏额度
    if ret:
        user = ret[0]
        user.diamond += diamond
    else:
        #新增打赏用户
        members.append(User(uid, name, gender, isadmin, level, fanlv, diamond))

    #累计礼物分类数量
    global gifts
    ret = [gift for gift in gifts if gift.uid == giftid]
    if ret:
        gift = ret[0]
        gift.count += count
    else:
        gifts.append(Gift(giftid, giftname, count))

    refreshwindow()


def refreshwindow():
    global members, diamonds

    totaldiamond = "总Diamond：" + str(diamonds)
    #打赏排行榜
    i = 0
    userlist = ""
    for item in members:
        i += 1
        userlist += str(i) + ". " + item.name + "D:" + str(item.diamond)
        if i > 5:
            break
        else:
            userlist += "\n"

    #打赏累计列表
    giftlist = ""
    for gift in gifts:
        giftlist += str(i) + ". " + gift.name + "D:" + str(gift.count)
        giftlist += "\n"

    #roominfo.app.call_next(totaldiamond + "\n" + giftlist + "\n" + userlist)


wnd_app = None


def showWindow():
    global wnd_app
    if not wnd_app:
        wnd_app = roominfo.app
        roominfo.app.mainloop()
