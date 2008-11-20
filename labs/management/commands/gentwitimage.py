from blogdor.models import Post
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
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
        
        height = width = 300
        line_height = 15
        
        background_color = (0,0,0,0)
        font_color_dark = (0,0,0)
        font_color_light = (100,100,100)
        
        block_height = (height - (top_margin * 2)) / 3
        
        wpid_lookup = {}
        
        if not username or not path:
            raise CommandError('Usage is gentwitimage %s' % self.args)
        
        img = Image.new("RGBA", (width, height), background_color)
        draw = ImageDraw.Draw(img)
        
        font = ImageFont.truetype(settings.FONT_PATH, 10)
        
        message = "What Twitter has taught me is that you can really cram an awful lot of stuff into 140 characters. What has Twitter taught you?"
        #message = "What Twitter has taught me is that you can really cram?"
        
        for i in range(0, 3):
        
            top_offset = (block_height * i) + top_margin
            
            draw.text((left_margin - 10, top_offset), "jcarbaugh", fill=font_color_dark, font=font)
            for line in textwrap.wrap(message, 40):
                top_offset += line_height
                draw.text((left_margin, top_offset), line, fill=font_color_light, font=font)
                
        img = img.rotate(-10, Image.BICUBIC)
        img.save(open(path, "w"), "PNG")