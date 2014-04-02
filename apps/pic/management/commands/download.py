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
RES_CHOICE = ['1920x1080', '1280x720', '2560x1440', '1680x1050', '1600x900']


def abs_path(*args):
    return os.path.join(settings.ROOT, *args)


def parse_page(page=1, res=''):
    url = BASE_URL % int(page)

    headers  = {
        'User-Agent': UA
    }
    r = requests.get(url, headers=headers)

    regex = re.compile(r'(?i)/wallpaper[^"]+?%s' % RES)
    ret = regex.findall(r.content)
    ret = sorted(set(ret))
    if res and res != RES:
        ret = [r.replace(RES, res + '.jpg') for r in ret]
    return ["%s%s" % (DOMAIN, r) for r in ret]


def is_url_downloaded(url):

    basename = os.path.basename(url)
    return Pic.Query(basename) is not None


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
        make_option(
            '-r', '--resolution',
            choices=RES_CHOICE,
            dest='res',
            default='1920x1080',
            help='the resolution of the pics to download. default: 1920x1080. Choose from: %r' % RES_CHOICE,
        ),
        make_option(
            '-a', '--start-page',
            dest='start',
            type=int,
            default=1,
            help='Start page number, default: 1'
        ),
        make_option(
            '-z', '--stop-page',
            dest='stop',
            type=int,
            default=2,
            help='stop page number, default: 2'
        ),
    )

    def handle(self, *args, **options):

        page = options.get('start')
        end_page = options.get('stop')

        while page < end_page:

            print "Processing page %s..." % page
            for url in parse_page(page, res=options.get('res')):
                if not is_url_downloaded(url):
                    print "Downloading %s ..." % url
                    download_url(url)
                    print "Url %s downloaded." % url
            page += 1

        self.stdout.write('Done!\n')
