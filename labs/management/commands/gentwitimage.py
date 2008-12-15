from djitter.models import Account
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from sunlightlabs.labs import genimage
import Image, ImageDraw, ImageFont
import textwrap
 
class Command(BaseCommand):
    
    help = "Generate images of direct messages for Twitter user"
    args = '[username] [path]'
    
    requires_model_validation = False
    
    def handle(self, username=None, path=None, *args, **options):
        
        assert hasattr(settings, 'FONT_PATH')
        
        if not username:
            raise CommandError('Usage is gentwitimage %s' % self.args)
        
        genimage.generate_image(username, path)