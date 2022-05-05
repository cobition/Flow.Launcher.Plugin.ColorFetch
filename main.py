# -*- coding: utf-8 -*-


import sys,os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flowlauncher import FlowLauncher

from PIL import Image, ImageGrab
import pyperclip
import numpy as np


# 读取剪切板内图片
def read_img_from_clipboard():
    img = ImageGrab.grabclipboard()
    # print(type(img))  
    return img       

# 按图片中颜色数量排序
def my_sort(item):
    return item[0]

# 提取图片中颜色值列表, 返回数量排名前5的颜色
def get_color_from_clipboard():
    img = read_img_from_clipboard()
    color = Image.Image.getcolors(img)
    color.sort(key=my_sort, reverse=True)
    return color[:6]

def generate_color(height, width, hex, name):
    color = Hex_to_RGB(hex)
    r = color[0]
    g = color[1]
    b = color[2]
    # alpha = color[3]
    img = np.ones((height, width, 3), dtype=np.uint8)
    for i, v in enumerate((r, g, b,)):
        img[:,:,i] = v
    # print(img[:,:,0])
    img = Image.fromarray(img)
    # img.show()
    img.save('./CachedImages/' + str(name) + '.png')


# RGB格式颜色转换为16进制颜色格式   
def RGB_to_Hex(color):    
    r = color[0]
    g = color[1]
    b = color[2]           
    color = '#'
    for i in (r, g, b,):
        num = int(i)
        # 将R、G、B分别转化为16进制拼接转换并大写  hex() 函数用于将10进制整数转换成16进制，以字符串形式表示
        color += str(hex(num))[-2:].replace('x', '0').upper()
    return color   


# 16进制颜色格式颜色转换为RGB格式
def Hex_to_RGB(hex):
    r = int(hex[1:3],16)
    g = int(hex[3:5],16)
    b = int(hex[5:7], 16)
    return (r, g, b)
 
    
class Main(FlowLauncher): 
    
    def query(self, keyword):

        results = list()
        if ImageGrab.grabclipboard() and Image.Image.getcolors(ImageGrab.grabclipboard()):
            color = get_color_from_clipboard()
            for i in color:
                out_hex = RGB_to_Hex(i[1])
                # out = str(i[1][0]) + ' ' + str(i[1][1]) + ' ' + str(i[1][2])
                generate_color(32, 32, out_hex, out_hex)
                             
                results.append({
                        "Title": out_hex,
                        "SubTitle": 'Copy to clipboard.',
                        "IcoPath": './CachedImages/' + out_hex + '.png',
                        "JsonRPCAction": {
                            "method": 'clip',
                            "parameters": [out_hex],
                        }
                    }) 
        else:
            results.append({
                "Title": '剪贴板内未检测到截图（或者截图所包含颜色过多）。',
                "SubTitle": '请将截图添加至剪贴板进行颜色识别（或者缩小截图区域）。',
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": None,
                    "parameters": None,
                }
            })
              
        return results
    def clip(self,keyword):
        pyperclip.copy(keyword)
        
         
    


if __name__ == "__main__":
    Main()

