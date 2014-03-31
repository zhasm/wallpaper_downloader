from django.db import models
import os.path


# Create your models here.
class Pic(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=256, null=True)
    time = models.DateTimeField(auto_now=True, blank=True)

    @classmethod
    def fields(cls):
        return ['id', 'name', 'url', 'time']

    @classmethod
    def Save(cls, **kwargs):

        obj = Pic()

        for k in cls.fields():
            v = kwargs.get(k)
            if v != None:
                setattr(obj, k, v)

        return obj.save()

    @classmethod
    def SaveFilename(cls, fn):

        basename = os.path.basename(fn)
        obj = cls.Query(name=basename)

        if obj:
            print 'Duplicate record entry found! id=%s, name=%s' % (
                obj.id,
                obj.name
            )
            return

        cls.Save(name=basename)
        print "%s has been saved!" % basename

    @classmethod
    def Query(cls, name=''):
        ret = None
        if name:
            ret = cls.objects.filter(name=name)

        if ret:
            return ret[0]
