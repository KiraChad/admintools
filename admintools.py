import threading
import os
import configparser
import time 
import random 
import requests
import glob
import traceback
import sys
import vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
from PIL import Image
from queue import Queue

print('\033[38;5;80m⠀⠀⠀⠀⠀⠀⢀⡤⣢⠟⢁⣴⣾⡿⠋⢉⠱⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠑⠒⠦⢄⣀⣴⠟⢡⣠⣼⣿⡿⢳⣄⡀⠀⠀\n⠀⠀⠀⠀⠀⢀⣾⡿⠃⣠⣿⣿⠿⠂⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢲⡿⠋⢰⣾⣿⣿⡟⠀⠀⠈⠙⢆⠀\n⠀⠀⠀⠀⠀⡜⠻⣷⣾⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣁⣰⢸⣿⢻⠟⢀⠀⠀⠀⠀⠀⠁\n⠀⠀⠀⠀⠰⠀⠀⢙⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣯⡀⠀⢃⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⢠⠎⠀⠀⠀⠀⠀⠀⣼⠀⢀⠀⠀⠀⠀⠀⢠⣷⡀⠀⠀⠀⠀⡀⠄⠀⠀⠀⠀⢻⣿⣿⣿⣧⠑⠀⣢⡄⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⡰⠃⢀⠄⠀⠀⠀⠀⣼⡿⡆⢸⠀⠀⠀⠀⠀⠈⣿⢷⡄⠀⠀⠀⠱⡀⠰⡀⠀⠀⠈⢿⣿⣿⣿⣧⠀⢸⣧⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠡⢢⠋⠀⠀⠀⠀⣼⡟⠀⣇⢸⡆⠀⠀⠀⡄⠀⢿⠀⢳⡄⠀⠀⠀⢳⠀⢳⠀⠀⠀⠈⣿⣿⣿⣿⣷⣘⡟⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⢀⠇⠀⠀⠀⠀⣸⡿⢤⠤⠸⡸⣷⠀⠀⠀⢱⠀⣾⡤⠤⢿⡤⢀⡀⠀⢧⠘⡆⠀⠀⠀⢸⡟⠻⢿⠟⣿⣷⡄⠀⠀⠀\n⠀⠀⠀⠀⠀⡞⠀⠀⠀⠀⢰⡿⢠⠇⠀⠀⢳⣿⢇⠀⠀⠈⡇⣿⡇⠀⠀⠻⣄⠀⠀⠘⡆⡇⠀⠀⠀⠀⣇⢀⡏⠀⣿⡿⣄⠀⠀⠀\n⠀⠀⠀⠀⢰⠁⠀⠀⠀⠀⣿⠁⣄⣀⣀⡀⠈⢿⡜⡄⠀⠀⢹⣿⡇⠐⢄⣀⠘⢧⡀⠀⠹⣿⠀⠀⠀⠀⢸⣿⣷⣶⣿⡇⢹⡇⠀⠀\n⠀⠀⠀⠀⠾⠀⠀⠀⠀⢸⣧⣾⠟⢉⣽⣿⣦⠈⢷⡘⣆⠀⠸⡟⣷⣶⠟⠛⢻⣷⣦⣀⠀⢻⠀⠀⠀⠀⢸⣏⣩⣼⣿⡇⠈⣷⠀⠀\n⠀⠀⠀⠃⠀⠀⠀⠀⠀⣿⡿⠁⠀⣠⣾⣿⣿⠀⠈⢿⠺⡆⠀⣧⢸⠀⠀⢀⣹⣿⣿⣿⣷⣼⣤⠀⠀⠀⢸⣿⣿⣿⣿⠀⠀⣿⠀⠀\n⠀⠀⣠⠄⣀⠀⠀⠀⢠⣿⡇⠀⠀⢻💙⢿⠀⠀⠈⠣⠈⠓⠾⠀⠀⠀⣿💙⣿⣿⠘⡇⡞⠀⠀⢠⣾⣿⣿⣿⡏⠀⠀⢹⠀⠀\n⠀⠀⠛⠀⣿⠀⠀⠀⢸⣿⣿⡀⠀⠈⠃⠐⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣄⣐⣠⠏⢠⣿⠁⠀⠀⢸⣿⣿⣿⣿⠀⠀⠀⢸⠀⠀\n⠀⠀⠀⠀⢹⡆⠰⡀⢸⡟⠩⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⢸⣿⣿⣿⠟⠀⠀⠀⠘⠀⠀\n⠀⠀⠀⠀⢎⣿⡀⢱⢞⣁⣀⡿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⡏⡼⠀⠀⠀⣾⣿⠋⠁⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠈⠿⠻⡇⠀⠀⠒⠢⢵⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣽⠁⠀⠀⢠⡿⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀\n ⠀⠀⠀⠀⠀⠀⡟⣦⡀⠀⠀⠀⠈⠓⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⢿⡇⠀⠀⡄⣸⣇⣼⣀⣀⣀⠀⠀⠀⠀⠀⠀\n ⠀⠀⠀⠀⠀⢰⠇⣿⢸⣦⡀⠀⠀⠀⠀⠈⠲⣄⡀⠀⠀⠀⠀⠀⣀⡤⠒⢉⡴⠃⣸⠀⠀⢰⣿⣿⣿⠃⡤⠊⠁⠉⠑⢄⠀⠀⠀\n ⠀⠀⠀⠀⠀⢸⠀⣿⣾⣿⢿⠲⣄⠀⠀⠀⠀⠘⠟⣦⣤⣴⡒⠉⢀⡠⠖⠉⠀⣠⠃⠀⣠⣿⣿⡿⠁⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⢸⠀⣿⠛⢿⠈⢢⠏⠀⠀⠀⠀⠀⣰⣏⣀⣿⠗⠊⠁⠀⠀⣠⣾⠃⢀⡴⠿⠛⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⢸⢀⠇⠀⠈⢠⠃⠀⠀⠀⠀⠀⢰⠟⠁⠀⢹⢇⠀⣀⠴⠊⡱⠥⠔⠋⠀⠀⢰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⢸⡟⠀⢀⡴⠁⠀⠀⠀⠀⠀⢠⡟⠀⠀⣰⢿⡘⣾⡅⠀⠀⠀⠀⢀⠄⠀⢠⠏⢀⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⢸⠀⣰⣿⠀⠀⠀⠀⠀⠀⢠⣿⠃⢀⡾⡇⠘⠻⡿⢷⡀⠀⠀⠒⠁⠀⢠⠏⢀⠏⣸⠃⢻⠏⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⣧⣾⣹⣿⠀⠀⠀⠀⠀⢠⠏⢉⠀⡞⣰⡇⠀⣴⣥⠞⢷⠀⠀⠀⠀⣠⠎⠀⠸⣶⠋⣠⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[0m')

#------------------------------------------Config------------------------------------------#

def createConfig(path):
    config = configparser.ConfigParser()
    
    config.add_section("Settings")
    config.set("Settings", "token", input('\033[38;5;29mAccess token:\033[0m'))
    
    with open(path, "w", encoding='utf-8') as config_file:
        config.write(config_file)
        
def crudConfig(path):
    if not os.path.exists(path):
        createConfig(path)
        
    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')
    
    # Читаем некоторые значения из конфиг. файла.
    global token
    token = config.get("Settings", "token")

    # Меняем значения из конфиг. файла.
    #config.set("Settings", "font_size", "12")
    
    # Удаляем значение из конфиг. файла.
    #config.remove_option("Settings", "font_style")
    
    # Вносим изменения в конфиг. файл.
    with open(path, "w", encoding='utf-8') as config_file:
        config.write(config_file)

def get_config(path):
    if not os.path.exists(path):
        create_config(path)
    
    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')
    return config

def get_setting(path, section, setting, silent=None):
    config = get_config(path)
    value = config.get(section, setting)
    
    if silent == None:
        msg = "{section} {setting} is {value}".format(
        section=section, setting=setting, value=value
        )
        
        print(msg)
    return value

def update_setting(path, section, setting, value):
    config = get_config(path)
    config.set(section, setting, value)
    with open(path, "w", encoding='utf-8') as config_file:
        config.write(config_file)

def delete_setting(path, section, setting):
    config = get_config(path)
    config.remove_option(section, setting)
    with open(path, "w", encoding='utf-8') as config_file:
        config.write(config_file)

#------------------------------------------Anything------------------------------------------#

def do_something_with_exception(e):
    path = os.path.abspath(__file__)
    exc_type, exc_value, exc_tb = sys.exc_info()
    
    exc_line = exc_tb.tb_lineno # <- на всякий случай
    exc_name = exc_tb.tb_frame.f_code.co_name # <- на всякий случай
    while exc_tb is not None:
        exc_file = exc_tb.tb_frame.f_code.co_filename
        if exc_file == path:
            exc_line = exc_tb.tb_lineno
            exc_name = exc_tb.tb_frame.f_code.co_name
            exc_tb = exc_tb.tb_next
        else:
            break
     
    if exc_type.__name__ == 'ApiError' or str(exc_value) == 'PhotoMinSize':
        if str(exc_value).startswith('[22] Upload error: owner photo min size') or str(exc_value) == 'PhotoMinSize':
            print('{}[{}] {}Photo min size {}200x200, 0.25 < aspect < 3{}'.format(
            Clr('Pink'), exc_name, Clr('Cactus'), Clr('Lime'), Clr('NoneColor')))
            
        elif exc_type.__name__ == 'ApiError':
            if str(exc_value) == '[5] User authorization failed: no access_token passed.' or str(exc_value) == '[5] User authorization failed: invalid access_token (4).':
                print('{}Access token exception{}'.format(
                Clr('Cactus'), Clr('NoneColor')))
                token = input('{}Enter valid access token:{}'.format(
                Clr('Cactus'), Clr('NoneColor')))
                update_setting(path, "Settings", "token", token)
         
        else:
            print ('{}Handling {}{}{} exception with message "{}{}{}" in {}[{}]{}, line {}{}{}'.format(
            Clr('Red'), Clr('Carrot'), exc_type.__name__, Clr('Red'), Clr('Carrot'), exc_value, Clr('Red'), Clr('Carrot'), exc_name, Clr('Red'), Clr('Carrot'), exc_line, Clr('NoneColor'))) #threading.current_thread().name
    
    elif exc_type.__name__ == 'Captcha' and onecaptcha == False:
        captcha_handler(captcha)
        
    
    print ('{}Handling {}{}{} exception with message "{}{}{}" in {}[{}]{}, line {}{}{}'.format(
    Clr('Red'), Clr('Carrot'), exc_type.__name__, Clr('Red'), Clr('Carrot'), exc_value, Clr('Red'), Clr('Carrot'), exc_name, Clr('Red'), Clr('Carrot'), exc_line, Clr('NoneColor'))) #threading.current_thread().name
        
solution = None
onecaptcha = False   
def captcha_handler(captcha):
    try:
        global onecaptcha
        
        if onecaptcha == False:
            onecaptcha = True
            
            p = requests.get(captcha.get_url())
            out = open("captcha.jpg", "wb")
            out.write(p.content)
            out.close()
            
            solution = input('{}Solve captcha:{}'.format
            (Clr('Cactus'), Clr('NoneColor')))
            captcha.try_again(solution)
            onecaptcha = False
    except Exception as e:
        do_something_with_exception(e)
        
def ImgDownload(response, nameofimg = 'image'):
    try:
        sizes = tuple('wzyxms')
        for line in response[::-1]:
            size_type = line.get('type')
            for size in sizes:
                if size_type == size:
                    height = line.get('height')
                    width = line.get('width')
                    if height >= 200 and width >= 200:
                        url = line.get('url')
                        p = requests.get(url)
                        out = open(nameofimg + ".jpg", "wb")
                        out.write(p.content)
                        out.close()
                        return True
                    else:
                        raise Exception('PhotoMinSize')
    except Exception as e:
        do_something_with_exception(e)

def ImgUpload(chatid, nameofimg = 'image'):
    try:
        path = open(nameofimg + ".jpg", 'rb')
        img = {'photo': path}
        url = vk.photos.getChatUploadServer(chat_id = chatid)#есть еще messagesuploadserver
        resp = requests.post(url['upload_url'], files=img).json()
        path.close()
        os.remove(nameofimg + ".jpg")
        return resp['response']
        ids = vk.photos.saveMessagesPhoto(photo = resp['photo'], server = resp['server'], hash = resp['hash'])[0]
        image = "photo{}_{}".format(ids['owner_id'], ids['id'])
        return image
    except IndexError:
        print('Photo not found')
    except Exception as e:
        do_something_with_exception(e)
        
def List(nameoflist):
    try:
        NotifyState('List')
        if not os.path.exists(nameoflist + '.txt'):
            f = open(nameoflist + '.txt', 'w')
            f.close()
            
        with open(nameoflist + '.txt', 'r+') as f:
            listf = [i.replace("\n","") for i in list(f)]
            if nameoflist == 'AdminList' and myid not in listf:
                f.write(myid + '\n')
                f.seek(0)
                listf = [i.replace("\n","") for i in list(f)]
            NotifyState('List', False)
            return str(listf)
    except Exception as e:
        do_something_with_exception(e)
        
def ListEditor(nameoflist, mess, remove = False):
    try:
        NotifyState('ListEditor')
        if mess != '':
            if mess == 'очистить':
                f = open(nameoflist + '.txt', 'w')
                f.close()
                userid = 'None'
                print('{}[ListEditor] {}The {}{}{} cleared.{}'.format
                (Clr('Pink'), Clr('Cactus'), Clr('Lime'), nameoflist, Clr('Cactus'), Clr('NoneColor')))
            else:
                try:
                    userid = mess.split('d', 1)[1].split('|')[0]
                except:
                    print('{}[ListEditor] {}Id "{}{}{}" was wrong.{}'.format
                    (Clr('Pink'), Clr('Cactus'), Clr('Lime'), mess, Clr('Cactus'), Clr('NoneColor')))
                    userid = 'None'

            if userid.isdigit() or userid.startswith('!'):
                with open(nameoflist + '.txt', 'r+') as f:
                    listf = [i.replace("\n","") for i in list(f)]
                    
                    if userid not in listf:
                        if remove:
                            print('{}[ListEditor] {}Id "{}{}{}" was not in the {}{}{}'.format(
                            Clr('Pink'), Clr('Cactus'), Clr('Lime'), userid, Clr('Cactus'), Clr('Lime'), nameoflist, Clr('NoneColor')))
                        else:
                            f.write(userid + '\n')
                            print('{}[ListEditor] {}Id "{}{}{}" has been added to the {}{}{}'.format(
                            Clr('Pink'), Clr('Cactus'), Clr('Lime'), userid, Clr('Cactus'), Clr('Lime'), nameoflist, Clr('NoneColor')))
                    else:
                        if remove:
                            f.seek(0)
                            lines = list(f)
                            lines.remove(userid + '\n')
                            with open(nameoflist + '.txt', 'w') as f:
                                for line in lines:
                                    f.write(line)
                            print('{}[ListEditor] {}Id "{}{}{}" has been deleted from the {}{}{}'.format(
                            Clr('Pink'), Clr('Cactus'), Clr('Lime'), userid, Clr('Cactus'), Clr('Lime'), nameoflist, Clr('NoneColor')))
                        else:
                            print('{}[ListEditor] {}Id "{}{}{}" was already in the {}{}{}'.format(
                            Clr('Pink'), Clr('Cactus'), Clr('Lime'), userid, Clr('Cactus'), Clr('Lime'), nameoflist, Clr('NoneColor')))
        NotifyState('ListEditor', False)
    except Exception as e:
        do_something_with_exception(e)

def Clr(color = 'Demonstration'):
    colors = {
    'Blue':'1;34',
    'LightBlue': '38;5;80',
    'Cactus':'38;5;29',
    'Lime':'1;32',
    'Pink':'1;38;5;198',
    'Red':'0;31',
    'Carrot':'38;5;167',
    'NoneColor':'0'
    }
    
    if color in colors:
        color = '\033[' + colors[color] + 'm'
        return color
    elif color == 'Demonstration':
        text = []
        for line in colors:
            text.append('\033[' + colors[line] + 'm' + line)
        print(*text)

def NotifyState(nameoffunction, start = True, active = False):
    if active:
        if start:
            print('{}[{}] started.{}'.format(
            Clr('Pink'), nameoffunction, Clr('NoneColor')))
        else:
            print('{}[{}] stopped.{}'.format(
            Clr('Pink'), nameoffunction, Clr('NoneColor')))
    else:
        pass

#------------------------------------------Command------------------------------------------#

def Command():
    try:
        vk.messages.send(chat_id = chatid, random_id = 0, message = "🔹🔷💙Ａｄｍｉｎ Ｔｏｏｌｓ💙🔷🔹\n🐥𝙁𝙤𝙧 𝙛𝙖𝙣𝙨:\n⠀⠀⠀ᴀнᴛон ʍуᴛ😁\n⠀⠀⠀ᴀнᴛон ᴄʙободᴀ💩\n⠀⠀⠀!ᴀʙᴀ {}🖼\n⠀⠀⠀⠀⠀ᐃ ʙ (ᴨᴇᴩᴇᴄᴧᴀнноʍ)ᴄообщᴇнии доᴧжᴇн/ы\n⠀⠀⠀⠀⠀нᴀходиᴛьᴄя изобᴩᴀжᴇниᴇ/я, ʍожно ʙыбᴩᴀᴛь\n⠀⠀⠀⠀⠀ᴋонᴛᴋᴩᴇᴛноᴇ.\n⠀⠀⠀!ᴋоʍᴀнды😐\n🐷𝙁𝙤𝙧 𝙖𝙙𝙢𝙞𝙣𝙨:\n⠀⠀⠀!ʍуᴛ {}😭\n⠀⠀⠀⠀⠀⇅ + очиᴄᴛиᴛь🧻 ᐅ очищᴀᴇᴛ ᴄᴨиᴄоᴋ ʍуᴛоʙ.\n⠀⠀⠀!ᴩᴀзʍуᴛ {}😃\n⠀⠀⠀!ᴀʙᴀ {} ᴄᴨᴀʍ/ᴄᴛоᴨ🖼\n⠀⠀⠀⠀⠀ᐃ ʍᴇняᴇᴛ ᴀʙу ᴇᴄᴧи онᴀ быᴧᴀ изʍᴇнᴇнᴀ.\n⠀⠀⠀!ᴀдʍин🐽\n⠀⠀⠀!ᴄᴛоᴨ🚫\n")
    except Exception as e:
        do_something_with_exception(e)
        
def Spam(): # в будущем..
    pass

def PinMessage():
    pass

def Reaction():
    pass
        
mute = False
def Mute(ev):
    NotifyState('Mute', active = True)
    global mute
    mute = True
    i = 0
    while mute:
        try:
            ev.wait()
            if messid != None and source_act == None and fromid in List('WhiteList'): # messid != None <- Проверка на случай если в размуте включена хуйня которая вырубает поток Mute отправляя None в очередь
                vk.messages.delete(message_ids = messid, peer_id = 2000000000 + chatid, delete_for_all = 1)
                print('{}[Mute] {}Message deleted: {}{}{}'.format(
                Clr('Pink'), Clr('LightBlue'), Clr('Blue'), str(i + 1), Clr('NoneColor')))
                i += 1
            ev.clear()
        except Exception as e:
            do_something_with_exception(e)
    else:
        NotifyState('Mute', False, active = True)
                      
avatar = False
def Avatar(mess, ev):
    try:
        if mess != '' and mess[0].isdigit():
            num = mess[0] 
        
            if num == '0':
                num = num.replace('0', '1')
        else:
            num = '1'
            
        reply = event.attachments.get('reply')
        if reply != None:
            chat_messid = str(json.loads(reply).get('conversation_message_id'))
        else:
            chat_messid = 'нету'
        

        attach_type = event.attachments.get('attach' + num + '_type')
        #attach_id = event.attachments.get('attach' + num)
        if attach_type == 'photo' or chat_messid.isdigit():
            if attach_type == 'photo':
                attachments = vk.messages.getById(message_ids = messid)['items'][0]['attachments']
            elif chat_messid.isdigit():
                attachments = vk.messages.getByConversationMessageId(peer_id = 2000000000 + chatid, conversation_message_ids = chat_messid)['items'][0]['attachments']
                
            if attachments != []:
                if int(num) > len(attachments):
                    num = '1'

                if attachments[int(num)-1]['type'] == 'photo':
                    response = attachments[int(num)-1]['photo']['sizes']
                    if ImgDownload(response, 'Avatar'):
                        response = ImgUpload(chatid, 'Avatar')
                        vk.messages.setChatPhoto(file = response)
                        event.from_me = True
                        print('{}[Avatar] {}Avatar changed{}'.format(
                        Clr('Pink'), Clr('LightBlue'), Clr('NoneColor')))

                    if 'спам' in mess:
                        global avatar
                        if not avatar:
                            NotifyState('Avatar', active = True)
                            i = 0
                            avatar = True
                            while avatar:
                                ev.wait()
                                #print(event.from_me, source_act)
                                if not event.from_me and (source_act == 'chat_photo_remove' or source_act == 'chat_photo_update'):
                                    vk.messages.setChatPhoto(file = response)
                                    print('{}[Avatar] {}Avatar changed: {}{}{}'.format(
                                    Clr('Pink'), Clr('LightBlue'), Clr('Blue'), str(i + 1), Clr('NoneColor')))
                                    i+=1
                                ev.clear()
                        
        elif 'стоп' in mess and avatar:
            avatar = False
            ev.clear()
            NotifyState('Avatar', start = False, active = True)

    except Exception as e:
        do_something_with_exception(e)
    
#------------------------------------------Main------------------------------------------#

if __name__ == "__main__":
    path = "config.txt"
    crudConfig(path)
    
    started = False
    while True:
        try:
            session = vk_api.VkApi(token = get_setting(path, "Settings", "token", True))
            vk = session.get_api()
            longpoll = VkLongPoll(session)
            myid = str(vk.users.get()[0]['id'])
            first_name = str(vk.users.get()[0]['first_name'])
            last_name = str(vk.users.get()[0]['last_name'])
            if not started:
                print('\033[38;5;80m💙Hello\033[1;34m', first_name, last_name + '\033[38;5;80m:3\033[0m')
                started = True
                
            ev = threading.Event()
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.from_chat:
                        #print(event.__dict__)
                        ev.set()
                        mess = event.text
                        mess = mess.lower()
                        messid = event.message_id
                        chatid = event.chat_id
                        fromid = str(event.user_id)
                        source_act = event.extra_values.get('source_act')
                        
                        if fromid not in List('WhiteList') or fromid in List('AdminList'):
                            if mess == '!команды':
                                threading.Thread(target=Command, daemon = True).start()
                                
                            elif mess.startswith('антон'):
                                if mess[6:] == 'мут':
                                    threading.Thread(target=ListEditor, args=('WhiteList', 'd!548711395|'), daemon = True).start()
                                    
                                    if not mute:
                                        threading.Thread(target=Mute, daemon = True).start()
                            
                                elif mess[6:] == 'свобода':
                                    threading.Thread(target=ListEditor, args=('WhiteList', 'd!548711395|', True), daemon = True).start()
                                    
                            elif mess.startswith('!ава'):
                                threading.Thread(target=Avatar, args=(mess[5:], ev,), daemon = True).start()

                        if fromid in List('AdminList'):
                            if mess.startswith('!размут'):
                                threading.Thread(target=ListEditor, args=('WhiteList', mess[8:], True), daemon = True).start()
                                '''
                                if mute:
                                    mute = False
                                    q.put(None)
                                '''
                                
                            elif mess.startswith('!мут'):
                                threading.Thread(target=ListEditor, args=('WhiteList', mess[5:]), daemon = True).start()
                                
                                if not mute:
                                    threading.Thread(target=Mute, args=(ev,), daemon = True).start()
                            
                            elif mess.startswith('!админ'):
                                threading.Thread(target=ListEditor, args=('AdminList', mess[7:]), daemon = True).start()
                            
                            elif mess == '!стоп':
                                print('\033[38;5;80mОстановлен by "\033[1;34m' + fromid + '\033[38;5;80m"..\033[0m')
                                sys.exit() 
                        '''
                        print('threads: ', threading.active_count())
                        for thread in threading.enumerate():
                            print(thread.name)  
                        '''
        except vk_api.exceptions.Captcha as captcha:
            do_something_with_exception(captcha)
            
        except KeyboardInterrupt:
            print('\033[38;5;80mКончил..\033[0m')
            sys.exit()

        except Exception as e:
            do_something_with_exception(e)
