import lxml.html
import urllib.request as urllib2
import pprint
import http.cookiejar as cookielib
from io import BytesIO
import lxml.html
from PIL import Image, ImageFilter, ImageOps, ImageChops
import pytesseract
import requests
#import base64

__author__ = "Dzhud"

def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


REGISTER_URL = 'http://tracuunnt.gdt.gov.vn/tcnnt/mstdn.jsp'
ty = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(ty))
html = opener.open(REGISTER_URL).read()
form = parse_form(html)
#Run this below to check if all is right. Should return the fields
#from the webpage including `'captcha': None,`
#pprint.pprint(form)


def get_captcha(html):
    tree = lxml.html.fromstring(html)
    img_data = tree.cssselect('div img')[0].get('src')
    #For base64 images
    #binary_img_data = base64.b64decode(img_data)
    img_link = 'http://tracuunnt.gdt.gov.vn'+ img_data
    response = requests.get(img_link)
    img = Image.open(BytesIO(response.content))
    return img

# Include tesseract executable in your path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = get_captcha(html)
# To see original image
img.save('captcha_initial.png')
img = img.filter(ImageFilter.MinFilter(3))
img = ImageOps.crop(img)
# (1, 0) and (-2, 0) seem to work fine too for offset()
img = ImageChops.offset(img, 0, -1)
img = img.effect_spread(1)
img = img.filter(ImageFilter.SHARPEN)
# To see newly adjusted image
img.save('newImage1.png')

#Convert image to text
wb = pytesseract.image_to_string(img)
print(wb)
