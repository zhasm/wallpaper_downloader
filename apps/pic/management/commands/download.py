from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from pic.models import Pic
import os.path
import re
import requests
from django.conf import settings
import os

BASE_URL = "http://interfacelift.com/wallpaper/downloads/date/hdtv/1080p/index%d.html"
DOMAIN = 'http://interfacelift.com'
RES = '1920x1080.jpg'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'

def abs_path(*args):
    return os.path.join(settings.ROOT, *args)

def parse_page(page = 1):
    url = BASE_URL % page

    headers  = {
        'User-Agent': UA
    }
    r = requests.get(url, headers=headers)

    regex = re.compile(r'(?i)/wallpaper[^"]+?%s' % RES)
    ret = regex.findall(r.content)
    ret = sorted(set(ret))
    return ["%s%s" % (DOMAIN, r) for r in ret]


def is_url_downloaded(url):

    basename = os.path.basename(url)
    return Pic.Query(basename) is None

def download_url(url, dest=''):
    if not dest:
        dest = abs_path('download')

    cmd = '''wget -U '%(ua)s' -P '%(path)s' %(url)s''' % {
        'ua': UA,
        'path': dest,
        'url': url,
    }
    print os.popen(cmd).read()

    Pic.SaveFilename(url)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-p', '--page',
            dest='page',
            type=int,
            default=1,
            help='Page number, default = 1.'),
        )

    def handle(self, *args, **options):
        page = options.get('page')
        for url in parse_page(page):
            if not is_url_downloaded(url):
                download_url(url)


        self.stdout.write('Done!\n')
