from djitter.models import Account
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import Image, ImageDraw, ImageFont
import MySQLdb
import textwrap
 
class Command(BaseCommand):
    
    help = "Generate images of direct messages for Twitter user"
    args = '[username] [path]'
    
    requires_model_validation = False
    
    def handle(self, username=None, path=None, *args, **options):
        
        assert hasattr(settings, 'FONT_PATH')
        
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
        
        if not username or not path:
            raise CommandError('Usage is gentwitimage %s' % self.args)
        
        img = Image.new("RGBA", (width, height), background_color)
        draw = ImageDraw.Draw(img)
        
        font = ImageFont.truetype(settings.FONT_PATH, 11)
        
        account = Account.objects.get(username='sunlightlabs')
        dms = account.direct_messages().filter(sender__username__in=settings.ALLOWED_TO_DM)[:2]
        
        i = 0
        
        for dm in dms:
            
            message = dm.message
        
            top_offset = (block_height * i) + top_margin
            
            draw.text((left_margin - 10, top_offset), dm.sender.username, fill=font_color_dark, font=font)
            for line in textwrap.wrap(message, 40):
                top_offset += line_height
                draw.text((left_margin, top_offset), line, fill=font_color_light, font=font)
            
            i += 1
                
        img = img.rotate(-10, Image.BICUBIC)
        img.save(open(path, "w"), "PNG")