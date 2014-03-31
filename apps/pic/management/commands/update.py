from django.core.management.base import BaseCommand, CommandError
# from optparse import make_option
from pic.models import Pic

class Command(BaseCommand):
    option_list = BaseCommand.option_list
# + (
        # make_option('--delete',
        #     action='store_true',
        #     dest='delete',
        #     default=False,
        #     help='Some help '),
        # )

    def handle(self, *args, **options):
        for fn in args:
            try:
                Pic.SaveFilename(fn)
            except Exception as e:
                raise CommandError('Error' + str(e))
