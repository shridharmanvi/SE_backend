from tweepy import streaming
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import csv
import json
import datetime
import time

consumer_key=' '
consumer_secret=' '

access_token=' '
axxess_secret_token=' '

apple_keywords=['iPad Air 2', 'iPad mini 3', 'iPhone 6 Plus', 'iPhone 6', 'iPad Air',
          'iPad mini 2', 'iPhone 5s', 'iPhone 5c', 'iPad mini',
          'iPad 4', 'iPhone 5', 'iPad 3',
          'iPhone 4s', 'iPad 2', 'iPad 2', 'iPad 2', 'iPhone 4', 
          'iPad', 'iPhone 3GS', 'iPhone 3G', 'iPhone','iPad Air2','iPadAir2', 'iPadAir 2', 'iPad mini3' ,'iPhone6Plus','iPhone 6Plus', 'iPhone6', 'iPadAir',
          'iPad mini2', 'iPhone 5s', 'iPhone 5c', 'iPad mini', 'iPad mini',
          'iPad4', 'iPhone5', 'iPad3', 'iPad 3','iPhone4s', 'iPad2', 'iPhone4','iPad', 'iPhone3GS', 'iPhone3G']

acer_keywords = ['Liquid Z410', 'LiquidZ410','Liquid Z 410','Liquid Jade S','LiquidJadeS','Liquid JadeS','Liquid Jade S', ' Liquid Z500 ','LiquidZ500','Liquid Z 500', 'Liquid X1','Liquid X 1','LiquidX1', ' Liquid Jade',
                 'Liquid E700','Liquid E 700','LiquidE700', 'Liquid E600','LiquidE600','Liquid E 600', 'Liquid Z200 ','LiquidZ200 ','Liquid Z 200', 'Iconia Tab8','Iconia Tab 8',
                 'Iconia Tab 7','Iconia Tab7', 'Iconia One 7', 'Iconia One7', 'Liquid E3 Duo Plus','Liquid E 3DuoPlus', 'Liquid E3','Liquid E 3',
                 'Liquid Z4',' Liquid Z 4', 'Iconia B1-721','Iconia B1721','Iconia B1 721', 'Iconia B1-720', 'Iconia A1-830','Iconia A1 830', ' Liquid Z5',' Liquid Z 5',
                 'Liquid S2','Liquid S 2', 'Liquid Z3','Liquid Z 3', 'Liquid S 1','Liquid S1 ', 'Iconia Tab A3','Iconia Tab A 3','Iconia Tab A 3', 'Iconia Tab A1','Iconia Tab A 1',
                 'Liquid E2','Liquid E 2', 'Liquid Z2',' Liquid Z 2', 'Liquid C1','Liquid C 1', 'Liquid E1','Liquid E 1', 'Iconia Tab  B1-710','Iconia Tab  B 1', 
                 'Iconia Tab A 110','Iconia Tab A110', 'Liquid Z110', 'Liquid Z 110', 'Liquid Gallant E350','Liquid Gallant E 350',
                 'Liquid Gallant DuoLiquid Glow E330 ', 'Liquid Gallant Duo Liquid Glow E330 ', 'CloudMobile S500', 'CloudMobile S 500', 'Iconia Tab A210 ','Iconia Tab A 210 ',
                 'Iconia Tab A200','Iconia Tab A 200', 'Iconia Tab A701 ','Iconia Tab A 701 ', 'Iconia Tab A700', 'Iconia Tab A 700', 'Iconia Tab A511', 'Iconia Tab A 511', 'Iconia Tab A 510','Iconia Tab A510',
                 'acer Allegro', 'Liquid Express E320','Liquid Express E 320', 'Iconia Tab A501', 'Iconia Tab A 501', 'Iconia Smart', 'Iconia Tab A500', 'Iconia Tab A 500'
                 'Iconia Tab A101','Iconia Tab A 101', 'Iconia Tab A100','Iconia Tab A 100','Liquid E', 'neoTouch P 400 ','neoTouch P 400 ', 'beTouch E 400','beTouch E400', ' neoTouch P300',' neoTouch P 300', 
                 'eTouch E110','eTouch E 110', 'beTouch E200','beTouch E 200', 'beTouch E100', 'beTouch E 100','beTouch E101', 'beTouch E 101','DX650','DX 650', 'acer M900','acer M 900', 'acer F900 ','acer F 900 ', 'X960','X 960'
                 'Liquid mini E310','Liquid mini E 310', 'beTouch E210 ', 'beTouch E 210 ', 'eTouch E140 ', 'eTouch E 140 ', 'Liquid mt', 'beTouch T500', 'beTouch T 500 ', 'beTouch E130', 'beTouch E 130','beTouch E120','beTouch E 120', 'Acer Stream']

celkon_keywords = ['Millennia OCTA510','Millennia OCTA 510', 'celkon Win 400', 'celkon Win400', 'Campus Whizz Q42', 'Campus Whizz Q 42', 'Millennia Epic Q550', 'Millennia Epic Q 550', 'Xion s CT695','Xion s CT 695'
                   'Campus Colt A401','Campus Colt A 401', 'Campus Crown Q40', 'Campus Crown Q 40', 'Glory Q5',  'Glory Q 5', 'Campus One A354C', 'Campus One A 354C','Campus Nova A352E', 'Campus Nova A 352E',
                   'celkon A43','celkon A 43', 'celkon A42','celkon A 42', 'Q500 Millennium Ultra', 'Q 500 Millennium Ultra', 'celkon Q44','celkon Q 44', 'celkon A500', 'celkon A 500', 'celkon A21','celkon A 21', 'celkon A115', 'celkon A 115','celkon Q455', 'celkon Q 455','celkon Q470','celkon Q 470', 'celkon Q3000','celkon Q 3000', 'celkon A35k','celkon A 35k',
                   'celkon A125', 'celkon A 125','celkon C7010','celkon C 7010', 'celkon C5055', 'celkon C 5055', 'celkon C9 Jumbo','celkon C 9 Jumbo', 'celkon C7 Jumbo','celkon C 7 Jumbo', 'C6 Star','C 6 Star', 'C44 Duos','C 44 Duos', 'celkon C366','celkon C 366', 'celkon C619','celkon C 619', 'celkon C51','celkon C 51', 'celkon C340','celkon C 340',
                   'celkon C348+','celkon C 348+','celkon C348+','celkon C 348 +', 'celkon C349+','celkon C 349+','celkon C 349 +','celkon C 349+', 'celkon C779','celkon C 779', 'celkon C66+','celkon C 66+', 'celkon A64','celkon A 64', 'celkon A66','celkon A 66', 'celkon A9 Dual','celkon A 9 Dual', 'celkon A 107+','celkon A 107 +', 'celkon C4040','celkon C 4040', 'celkon ARR35', 'celkon CT 7', 'CT-888',
                   'celkon C820', 'celkon C720', 'celkon S1', 'celkon A40', 'celkon AR50', 'celkon AR40', 'celkon AR45', 'celkon A15', 'celkon C7045', 'celkon C605', 'celkon C399', 'celkon C76', 'celkon C64', 'celkon C63',
                   'celkon C 820', 'celkon C 720', 'celkon S 1', 'celkon A 40', 'celkon AR 50', 'celkon AR 40', 'celkon AR 45', 'celkon A 15', 'celkon C 7045', 'celkon C 605', 'celkon C 399', 'celkon C 76', 'celkon C 64', 'celkon C 63',
                   'Monalisa 5', 'celkon A112', 'celkon A63', 'celkon A60', 'celkon A20', 'celkon A10', 'C5050 Star', 'celkon C7030', 'celkon A105', 'celkon C349i', 'celkon C297', 'celkon C69',
                   'Monalisa 5', 'celkon A 112', 'celkon A 63', 'celkon A 60', 'celkon A 20', 'celkon A 10', 'C 5050 Star', 'celkon C 7030', 'celkon A 105', 'celkon C 349i', 'celkon C 297', 'celkon C 69',
                   'celkon C67+', 'celkon C74', 'celkon CT-910+', 'celkon A118', 'celkon A107', 'celkon A9+', 'celkon A119Q Signature HD', 'celkon A119 Signature HD', 'celkon CT-910', 'celkon A87',
                   'celkon C 67+','celkon C 67 +', 'celkon C74', 'celkon C 74', 'celkon CT-910+', 'celkon CT 910+', 'celkon CT-910 +', 'celkon A 118', 'celkon A 107', 'celkon A 9+', 'celkon A119Q Signature HD', 'celkon A 119 Signature HD', 'celkon CT 910', 'celkon A 87',
                   'celkon A86', 'celkon A69', 'celkon A67', 'celkon A98', 'celkon A225', 'celkon C7050', 'celkon C7070', 'celkon C44 Star', 'celkon C54', 'celkon GC10', 'celkon C3333', 'celkon C356', 'celkon C355', 'celkon A75',
                   'celkon A 86', 'celkon A 69', 'celkon A 67', 'celkon A 98', 'celkon A 225', 'celkon C 7050', 'celkon C 7070', 'celkon C 44 Star', 'celkon C 54', 'celkon GC 10', 'celkon C 3333', 'celkon C 356', 'celkon C 355', 'celkon A 75',
                   'celkon A59', 'celkon A220', 'celkon A27', 'celkon A79', 'celkon A83', 'celkon A77', 'celkon CT 9', 'celkon A200', 'celkon C19', 'celkon A900', 'celkon A85', 'celkon A22', 'celkon CT 2',
                   'celkon A 59', 'celkon A 220', 'celkon A 27', 'celkon A 79', 'celkon A 83', 'celkon A 77', 'celkon CT 9', 'celkon A 200', 'celkon C 19', 'celkon A 900', 'celkon A 85', 'celkon A 22', 'celkon CT 2']

dell_keywords = ['Venue 8 7000', 'Venue 8', 'Venue 7', 'Venue7', 'XPS 10','XPS10', 'Streak Pro D43','Streak Pro D 43', 'Streak 10 Pro','Streak 10Pro', 'Streak 7','Streak7',
                 'dell Venue', 'XCD35','XCD 35', 'XCD28','XCD 28','dell Smoke','dell Smoke', 'dell Flash', 'Venue Pro', 'dell Streak', 'dell Aero', 'Mini 3i', 'Mini 3iX']

huawei_keywords = ['Ascend Y540','Ascend Y 540', 'Ascend Y520','Ascend Y 520', 'Ascend Y221','Ascend Y221', 'Ascend GX1','Ascend G X1', 'Honor 6 Plus', 'Honor 6Plus', 'Ascend Mate7 Monarch','Ascend Mate 7 Monarch',
                   'Honor 4X','Honor 4 X', 'Honor Holly', 'Honor Tablet', 'Honor 4 Play', 'Honor 4Play', 'Ascend G620s','Ascend G 620s', 'Ascend Y550', 'Ascend Y 550', 'Ascend G7','Ascend G 7',
                   'Ascend P7 Sapphire Edition','Ascend P 7 Sapphire Edition', 'Ascend Mate7','Ascend Mate 7', 'Honor 3C Play',  'Honor 3 C Play', 'Honor 6','Honor6', 'Honor 3X Pro', 'Honor 3C',
                   'Ascend G535', 'Y300II', 'Ascend G630', 'Ascend Y330', 'Ascend Plus', 'Ascend P7', 'Mulan', 'Ascend P7 mini',
                   'Ascend G 535', 'Ascend G 630', 'Ascend Y 330', 'Ascend Plus', 'Ascend P 7', 'Mulan', 'Ascend P 7 mini',
                   'Ascend G730','Ascend G 730', 'Ascend Y600','Ascend Y 600', 'MediaPad 10 Link+','MediaPad 10 Link +', 'Ascend G6','Ascend G 6', 'MediaPad M1','MediaPad M 1', 'MediaPad X1',
                   'Ascend Y530', 'MediaPad 7 Youth2', 'Ascend P6 S', 'Ascend Mate2 4G', 'Ascend Y320', 'Ascend Y220', 'Honor 3X G750',
                   'Ascend Y 530', 'MediaPad 7 Youth 2', 'Ascend P 6 S', 'Ascend Mate 2', 'Ascend Y 320', 'Ascend Y 220', 'Honor 3X G 750',
                   'Honor 3C', 'Ascend G740', 'Ascend Y511', 'Ascend W2', 'huawei G6153', 'huawei G3621L', 'Honor 3', 'Ascend G700', 'huawei G610s', 'huawei U8687 Cronos',
                   'Honor 3C', 'Ascend G 740', 'Ascend Y 511', 'Ascend W 2', 'huawei G 6153', 'huawei G 3621L', 'Honor3', 'Ascend G 700', 'huawei G 610s', 'huawei U 8687 Cronos',
                   'Ascend G525', 'MediaPad 7 Youth', 'MediaPad 7 Vogue', 'Ascend P6', 'Ascend Y300', 'Premia 4G M931', 'Ascend Y210D', 'Ascend P2',
                   'Ascend G 525', 'MediaPad 7 Youth', 'MediaPad 7 Vogue', 'Ascend P 6', 'Ascend Y 300', 'Premia M 931', 'Ascend Y 210D', 'Ascend P 2',
                   'Ascend G615', 'Ascend G526', 'Ascend G350', 'Ascend G312', 'Ascend W1', 'Ascend Mate', 'Ascend D2', 'Ascend G510', 'Ascend G500',
                   'Ascend G 615', 'Ascend G 526', 'Ascend G 350', 'Ascend G 312', 'Ascend W1', 'Ascend Mate', 'Ascend D 2', 'Ascend G 510', 'Ascend G 500',
                   'Ascend Y201 Pro', 'MediaPad 10 Link', 'Honor 2', 'Ascend Y'
                   'Ascend Y 201 Pro', 'MediaPad 10 Link', 'Honor2', 'AscendY']

lenovo_keywords = ['lenovo P70', 'Tab 2 A7-30', 'Tab 2 A7-10', 'lenovo A6000', 'lenovo P90', 'Vibe X2 Pro', 'lenovo K3', 'Golden Warrior Note 8', 'lenovo A916',
                   'P 70', 'Tab 2 A730', 'Tab 2 A710', 'lenovo A 6000', 'lenovo P 90', 'Vibe X 2 Pro', 'lenovo K 3', 'Golden Warrior Note 8', 'lenovo A 916',
                   'lenovo A319', 'lenovo S856', 'lenovo S580', 'S90 Sisley', 'lenovo A606', 'Yoga Tablet 2 Pro', 'Yoga Tablet 2 10.1', 'Yoga Tablet 2 8.0',
                   'lenovo A 319', 'lenovo S 856', 'lenovo S 580', 'S90 Sisley', 'lenovo A 606', 'Yoga Tablet 2 Pro', 'Yoga Tablet 2 10.1', 'Yoga Tablet 2 8.0',
                   'Tab S8', 'Vibe X2', 'Vibe Z2', 'A850+', 'Vibe Z2 Pro', 'Golden Warrior A8', 'Golden Warrior S8', 'lenovo S939', 'lenovo S750',
                   'Tab S 8', 'Vibe X 2', 'Vibe Z 2', 'A 850+','A 850+', 'Vibe Z2 Pro', 'Golden Warrior A 8', 'Golden Warrior S 8', 'lenovo S 939', 'lenovo S 750',
                   'lenovo A889', 'lenovo A680', 'lenovo A316i', 'lenovo A328', 'lenovo A536', 'lenovo A526', 'lenovo A10-70 A7600', 'lenovo A8-50 A5500', 'A7-50 A3500', 'A7-30 A3300',
                   'lenovo A 889', 'lenovo A 680', 'lenovo A 316i', 'lenovo A 328', 'lenovo A 536', 'lenovo A 526', 'lenovo A10-70 A7600', 'lenovo A8-50 A5500', 'A7-50 A3500', 'A7-30 A3300',
                   'Yoga Tablet 10 HD+', 'lenovo S860', 'lenovo S850', 'lenovo S660', 'lenovo A880', 'lenovo A859', 'lenovo S930', 'lenovo S650', 'Vibe Z K910', 'Yoga Tablet 10',
                   'Yoga Tablet 10 HD+', 'Yoga Tablet 10 HD +','lenovo S 860', 'lenovo S 850', 'lenovo S 660', 'lenovo A 880', 'lenovo A 859', 'lenovo S 930', 'lenovo S 650', 'Vibe Z K910', 'Yoga Tablet 10',
                   'Yoga Tablet 8', 'lenovo A630', 'lenovo A516', 'Vibe X S960', 'lenovo S5000', 'lenovo A850', 'lenovo A706', 'lenovo P780', 'lenovo S820', 'lenovo A390', 'lenovo A369i', 'lenovo A269i',
                   'Yoga Tablet 8', 'lenovo A 630', 'lenovo A 516', 'Vibe X S960', 'lenovo S 5000', 'lenovo A 850', 'lenovo A 706', 'lenovo P 780', 'lenovo S 820', 'lenovo A 390', 'lenovo A 369i', 'lenovo A 269i',
                   'S920', 'IdeaTab S6000H', 'IdeaTab S6000F', 'IdeaTab S6000L', 'IdeaTab S6000', 'IdeaTab A3000', 'IdeaTab A1000', 'lenovo K900',
                   'lenovo S 920', 'lenovo IdeaTab S 6000H','lenovo IdeaTab S 6000 H', 'IdeaTab S 6000 F','IdeaTab S 6000F', 'IdeaTab S6000 L','IdeaTab S 6000 L','IdeaTab S 6000 L', 'IdeaTab S6000','IdeaTab S 6000', 'IdeaTab A3000','IdeaTab A 3000', 'IdeaTab A1000','IdeaTab A 1000', 'lenovo K 900',
                   'lenovo S890', 'IdeaTab A2107', 'lenovo A830', 'lenovo A820', 'lenovo A800', 'lenovo A789',
                   'lenovo S 890', 'IdeaTab A 2107', 'lenovo A 830', 'lenovo A 820', 'lenovo A 800', 'lenovo A 789']

xiaomi_keywords = ['Mi Note Pro', 'Mi Note', 'Redmi 2', 'Mi 4 LTE', 'Redmi Note 4G', 'Mi 4', 'Mi Pad 7.9', 'Redmi Note', 'Mi 3',
                   'Redmi 1S','Redmi 1 S', 'Redmi', 'Mi 2A','Mi 2 A', 'Mi 2S','Mi 2 S', 'xiaomi Mi 2', 'xiaomi Mi 1S']

asus_keywords = ['Fonepad 7 FE375CL', 'Zenfone C ZC451CG', 'Fonepad 7 FE171CG', 'Zenfone Zoom ZX550', 'Zenfone 2 ZE551ML',
                 'asus Pegasus', 'Zenfone 5 Lite A502CG', 'Memo Pad 10 ME103K', 'PadFone X mini', 'Memo Pad 7 ME572CL', 'Memo Pad 7 ME572C',
                 'Zenfone 5 A500KL', 'Zenfone 4 A450CG', 'Memo Pad 8 ME581CL', 'Memo Pad 8 ME181C', 'Memo Pad 7 ME176C', 'Fonepad 8 FE380CG',
                 'Fonepad 7 FE375CXG', 'Fonepad 7 FE375CG', 'Transformer Pad TF303CL', 'Transformer Pad TF103C', 'Fonepad 7', 'PadFone X',
                 'PadFone S', 'PadFone Infinity Lite', 'PadFone E', 'Zenfone 6 A601CG', 'Zenfone 6', 'Zenfone 5', 'Zenfone 4', 'PadFone mini (Intel)',
                 'PadFone mini', 'Transformer Book Trio', 'PadFone Infinity 2', 'Memo Pad 10', 'Memo Pad 8 ME180A']

blackberry_keywords = ['Classic Non Camera', "Porsche Design P'9983", 'blackberry Passport', 'blackberry Classic', 'blackberry Z3', "Porsche Design P'9982", 'blackberry Z30', 'blackberry 9720',
                       'blackberry Q5', 'blackberry Z10', 'blackberry Q10', 'LTE PlayBook', 'Curve 9320', 'Curve 9220', 'Curve 9380', 'Bold 9790', "Porsche Design P'9981",
                       'Curve 9370', 'Curve 9360', 'Curve 9350', 'Torch 9810', 'Torch 9860', 'Torch 9850', 'Bold Touch 9900', 'Bold Touch 9930',
                       '4G PlayBook HSPA+', 'PlayBook WiMax', 'PlayBook', 'Bold 9780', 'Style 9670', 'Curve 3G 9330', 'Curve 3G 9300', 'Torch 9800',
                       'Pearl 3G 9105', 'Pearl 3G 9100', 'Bold 9650']


keywords = apple_keywords+acer_keywords+celkon_keywords+dell_keywords+lenovo_keywords+xiaomi_keywords+asus_keywords+blackberry_keywords;
#keywords = apple_keywords#+acer_keywords+celkon_keywords+dell_keywords+lenovo_keywords+xiaomi_keywords+asus_keywords+blackberry_keywords;
tweet={}

keywords_no_space = [];

for i in range (0, len(keywords)):
    #print i
    keywords_no_space.append( keywords[i].replace(" ","").lower());
    
 
#keywords.sort();

keywords_no_space.sort(key=len, reverse=True);
print keywords_no_space;

#keywords_lower = keywords_lower[:len(keywords_lower)-1];

#print keywords_lower;
keywords = keywords[0:400];

#keys =keywords.sort(key = lambda s: len(s));
#print keys;


def CheckIfOmitWordsExist(tweet_words, omit_words):

    #print "**** the tweet",tweet_words
        
    for i in range(0,len(omit_words)-1):
        #print omit_words[i]
        
        if omit_words[i] in tweet_words:
            #print '***the word', omit_words[i]
            return 1;
    #print
    return 0;
     

def CheckIfKeyWordPresent(tweet_no_space, keyword_no_space):
    for i in range (0,len(keyword_no_space)-1):
        #print '***i',i
        if keyword_no_space[i] in tweet_no_space:
            return i
    return -1


class listener(StreamListener):    
    def on_status(self,status):
        omitwords=['price','USD','Price','$','case','iphonegames','deals','game','sale','advertisement','sex','porn','pornography','food','gold','coins','#followtrick\n']
        tweet_text=status.text.encode("utf-8")
 
        tweet_words = tweet_text.lower().split();
        exists_omitwords= CheckIfOmitWordsExist(tweet_text.lower(), omitwords);

        #print tweet_words;
        if exists_omitwords == 0:

            #print tweet_text.lower();
            try:
                tweet_text.decode('ascii')
                tweet_no_space=tweet_text.lower().replace(" ","")
                index=CheckIfKeyWordPresent(tweet_no_space,keywords_no_space);
                #print "index",index
                if  index> -1:
                
                    print tweet_text.lower(), "key -",keywords_no_space[index];
            except UnicodeDecodeError:
                pass
            
            

    def on_error(self, status):
        print(status)
            
'''
            for word in omitwords:
                if(word not in tweet_text.lower().split()):
                    for words in tweet_text.lower().split():
                        if(words in keywords_lower):
                        
                            tweet_id=int(status.id)
                            if(tweet_id not in tweet.keys()):    
                                tweet_created=status.created_at.date()
                                a= [[tweet_id,tweet_created,tweet_text,words]]
                                tweet[tweet_id]= a
                                print(tweet)
                                f=open('tweets.csv', 'a+')
                                writer = csv.writer(f)
                                writer.writerows(a)
                else:
                    x=1
            else:
                k=1            
'''

        

    

auth= OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,axxess_secret_token)
twitterStream= Stream(auth,listener())
#twitterStream.filter(track=['iphone,iphone5s,iphone6plus,iphone6,6plus,iphone6+,iphone5'],languages = ['en'])
twitterStream.filter(track=keywords,languages = ['en'])


