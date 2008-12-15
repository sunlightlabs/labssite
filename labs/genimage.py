from djitter.models import Account
from django.conf import settings
import base64
import cStringIO
import datetime
import httplib
import hmac
import Image, ImageDraw, ImageFont
import md5
import sha
import textwrap

def generate_image(username=None, path=None):
    
    assert hasattr(settings, 'FONT_PATH')
    
    if not username:
        username = settings.TWITTER_USERNAME
    
    top_margin = 30
    left_margin = 40
    
    height = 220
    width = 300
    line_height = 15
    
    background_color = (0,0,0,0)
    font_color_dark = (0,0,0)
    font_color_light = (100,100,100)
    
    block_height = (height - (top_margin * 2)) / 2
    
    wpid_lookup = {}
    
    img = Image.new("RGBA", (width, height), background_color)
    draw = ImageDraw.Draw(img)
    
    font = ImageFont.truetype(settings.FONT_PATH, 12)
    
    account = Account.objects.get(username=username)
    dms = account.direct_messages().filter(sender__username__in=settings.ALLOWED_TO_DM)[:2]
    
    i = 0
    
    for dm in dms:
        
        message = dm.message
    
        top_offset = (block_height * i) + top_margin
        
        draw.text((left_margin - 10, top_offset), dm.sender.username, fill=font_color_dark, font=font)
        for line in textwrap.wrap(message, 35):
            top_offset += line_height
            draw.text((left_margin, top_offset + 5), line, fill=font_color_light, font=font)
        
        i += 1
            
    img = img.rotate(-10, Image.BICUBIC)
    
    if path:
        img.save(open(path, 'wb'), "PNG")
    else:
        imgbuffer = cStringIO.StringIO()
        img.save(imgbuffer, "PNG")
        s3_upload(imgbuffer.getvalue())
        imgbuffer.close()

def s3_upload(content):
    
    bucket = settings.AWS_BUCKET
    path = '/tweets.png'
    
    now = datetime.datetime.utcnow()
    rfc_now = now.strftime("%a, %d %b %Y %X GMT")
    expires = now + datetime.timedelta(1)
    content_type = 'image/png'
    
    s3_conn = httplib.HTTPConnection(bucket)
    checksum = base64.b64encode(md5.new(content).digest())

    to_sign = "\n".join(["PUT", checksum, content_type, rfc_now, "x-amz-acl:public-read", "/%s%s" % (bucket, path)])
    sig = base64.encodestring(hmac.new(settings.AWS_SECRET, to_sign, sha).digest()).strip()

    headers = {
        "x-amz-acl": "public-read",
        "Expires": expires.strftime("%a, %d %b %Y %H:%M:%S UTC"),
        "Content-Type": content_type,
        "Content-Length": len(content),
        "Content-MD5": checksum,
        "Date": rfc_now,
        "Authorization": "AWS %s:%s" % (settings.AWS_KEY, sig)
    }

    s3_conn.request("PUT", path, content, headers)
    response = s3_conn.getresponse()
    s3_conn.close()