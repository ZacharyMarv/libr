# -*- coding:utf-8 -*-
# Created at 2015/7/20

"""
    Function:
        Convert Apk into Smali
"""
__author__ = 'Zachary Marv - 马子昂'

import json

input_d = "../data/dep2.dat"
output_d = "../data/tagged_dep2.dat"

lib_list = {
    "google": "Google",
    "org/apache/cordova": "Cordova",
    "org/apache/log4j/": "Log4j",
    "umeng": "友盟Umeng",
    "android/support/v4": "Android Support v4",
    "android/support/v7": "Android Support v7",
    "android/support/v13": "Android Support v13",
    "xamarin": "Xamarin",
    "opentk": "OpenTK",
    "admob": "Admob",
    "mono": "Mono",
    "corona": "Corona",
    "jsr166y": "JSR-166y Java 并行计算库",
    "pagerslidingtabstrip": "PagerSlidingTabStrip UI Framework",
    "aurelienribon": "AurelienRibon Animation Library",
    "opengl": "OpenGL",
    "facebook": "Facebook",
    "junit": "jUnit Java Unit Test",
    "bolts": "Bolts Base Library",
    "dagger": "Dagger: 一种Android平台的依赖注入框架",
    "okio": "OkHttp okio Framework",
    "roboguice": "roboguice依赖注入函数库",
    "rajawali/wallpaper": "rajawali WallPapper",
    "retrofit": "retrofit RESTful Library",
    "greendroid": "GreenDroid:增强型Android UI Library",
    "butterknife": "butterknife UI Framework",
    "flexjson": "FlexJson Library",
    "twitter": "Twitter",
    "kawa": "Kawa for Android",
    "javax": "javax",
    "amazon": "Amazon",
    "pdftron": "PDF Widget",
    "appmachine": "AppMachine App Generator 应用生成工具",
    "microsoft/mappoint": "Microsoft MapPoint",
    "jdeferred": "Java jdeferred Library",
    "kankan/wheel": "仿iPhone滚轮控件 Android scroller",
    "org/slf4j": "SLF4J",
    "oauth": "OAUTH 网页认证 an open standard for authorization",
    "andengine": "Andengine Game Engine",
    "openfeint": "OpenFeint",
    "flurry": "Flurry",
    "org/apache/http": "Apache Http",
    "aviary": "Aviary photo editing SDK",
    "com/scoreloop": "Scoreloop Game",
    "com/tencent/mm": "Tencent Wechat微信",
    "com/tencent": "Tencent",
    "weibo": "Weibo",
    "pinyin4j": "Pinyin4j",
    "nostra13": "Nostra13 Image Loading",
    "appmakr": "Appmakr",
    "qoppa": "Qoppa Software",
    "neoline": "Neoline",
    "org/apache/commons": "Apache Common",
    "com/mopub/nativeads": "Native Ads",
    "openuidi": "OpenUDID",
    "datamodel/v5": "Datamodel v5",
    "hamcrest": "hamcrest",
    "org/fmod": "Fmod",
    "appflood": "appflood",
    "appbrain": "appbrain",
    "pollfish": "pollfish",
    "scarysd": "scarySD",
    "applovin": "applovin",
    "urbanairship": "urbanairship",
    "startapp": "StartApp",
    "newrelic": "newrelic",
    "startapp": "startapp",
    "cocos2d": "cocos2d",
    "leadbolt": "Leadbolt",
    "inmobi": "inmobi",
    "com/mongodb": "mongoDB",
    "com/actionbarsherlock": "ActionBarSherlock",
    "org/htmlcleaner": "htmlCleaner",
    "com/subsplash": "subsplash",
    "org/dom4j": "Dom4j",
    "com/yixia": "Yixia",
    "com/inmobi": "Inmobi",
    "com/ngpinc/": "ngpinc",
    "anywheresoftware": "anywheresoftware",
    "org/kobjects/mime": "kobjects",
    "com/adobe": "Adobe",
    "com/parse": "Parse",
    "com/magtab": "Magtab",
    "org/appcelerator": "Appcelerator",
    "com/jirbo": "Jirbo",
    "org/mozilla": "Mozilla",
    "com/vercoop": "Vercoop",
    "com/phonegap": "PhoneGap",
    "com/appyet": "Appyet",
    "com/apache": "Apache",
    "com/millennialmedia": "millennialmedia",
    "com/papaya": "Papaya",
    "com/comscore": "comscore",
    "com/vpon": "Vpon",
    "com/adwhirl": "Adwhirl Ads",
    "com/revmob": "Revmob",
    "com/kakao/talk": "Kakao",
    "com/viewpagerindicator": "Android com/viewpagerindicator Widget",
    "org/kxml2": "Kxml2",
    "gnu/mapping": "GNU Mapping",
    "android/widget": "android widget",
    "com/mobfox": "mobfox",
    "gnu/xml": "GNU XML",
    "ti/map": "Ti Map",
    "com/deploygate": "com/deploygate",
    "com/dobao": "com/dobao",
    "com/crowdcompass": "crowdcompass",
    "adtech": "Adtech",
    "org/codehaus": "Codehaus",
    "com/doapps": "doapps",
    "com/crowdcompass": "crowdcompass",
    "com/thirdparty": "Thirdparty",
    "com/badlogic": "badlogic",
    "com/github": "Github",
    "com/goodbarber": "goodbarber",
    "com/samsung/spen": "Spen",
    "com/paypal":"PayPal",
    "com/fasterxml": "Fasterxml",
    "com/skplanet": "skplanet",
    "net/youmi": "Youmi",
    "com/doapps": "Doapps",
    "cn/domob": "domob",
    "com/qwapi": "qwapi",
    "com/j256": "J256",
    "com/handmark": "handmark",
    "com/myappengine": "myappengine",
    "com/qbiki": "qbiki",
    "com/biznessapps": "biznessapps",
    "com/baidu": "Baidu",
    "org/json": "Json org",
    "com/apperhand": "apperhand",
    "com/pocketchange/": "pocketchange",
    "com/unity3d": "Unity3D",
    "com/adsdk": "AdSDK",
    "com/alipay": "Alipay",
    "com/adsmogo": "adsmogo",
    "nineoldandroids": "Nine Old Androids",
    }

input = open(input_d, 'r')
output = open(output_d, 'w')
for line in input:
    i = json.loads(line)
    o = {}
    if i['b_total_call'] < 5:
        continue
    s_path = '/'.join(i[u'path_parts'])
    s_lower = s_path.lower()
    o['lib'] = ""
    for lib in lib_list:
        if lib in s_lower:
            o['lib'] = lib_list[lib]
            break;
    o['s_path'] = s_path
    o['b_hash'] = i['b_hash']
    o['b_total_num'] = i['b_total_num']
    o['b_total_call'] = i['b_total_call']
    output.write(json.dumps(o)+'\n')

input.close()
output.close()