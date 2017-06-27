from __future__ import absolute_import, unicode_literals
import os


from PIL import Image
from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery import shared_task
from resizeimage import resizeimage

from dTBack import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dTBack.settings')

app = Celery('dTBack')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@shared_task
def resizeImage(source, width):

    print('Resizing {0}'.format(source))
    fromImage = os.path.join(settings.MEDIA_ROOT, source)
    toPath = os.path.join(settings.STATIC_ROOT, 'images', 'posts')

    filename, file_extension = os.path.splitext(source)

    if not os.path.exists(fromImage) or not os.path.exists(toPath):
        return

    theImage = Image.open(fromImage)
    for key in settings.WEB_RESPONSIVE_DIMENSIONS.keys():
        newImage = resizeimage.resize_width(theImage, settings.WEB_RESPONSIVE_DIMENSIONS.get(key))
        newFilename = filename + "-" + key + file_extension
        newImage.save(os.path.join(toPath, newFilename))

#    theImage = resizeimage.resize_width(theImage, width)
#    theImage.save(os.path.join(toPath, source))
