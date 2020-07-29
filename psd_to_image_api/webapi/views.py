from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from pdf2image import convert_from_bytes, convert_from_path
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from datetime import datetime


@api_view(['POST'])
def upload(request):
    file = request.FILES['pdf']
    timestamp = datetime.timestamp(datetime.now())
    path = default_storage.save('media/' + str(timestamp) + '.pdf', ContentFile(file.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    print(tmp_file)
    images = convert_from_path(tmp_file)
    count = 0
    content = []
    for image in images:
        temp = {}
        count = count + 1
        temp['page'] = count
        real_image = "media/" + str(timestamp) + str(count) + ".webp"
        image.save(real_image, "WEBP")
        temp['image'] = real_image
        image.thumbnail((200, 200))
        thumb = "media/" + str(timestamp) + str(count) + "-thumb.webp"
        image.save(thumb, "WEBP")
        temp['thumb'] = thumb
        content.append(temp)
    return Response(content, status=status.HTTP_200_OK)
# except ValueError:
#     content = {
#         'message': "Please upload the file"
#     }
# return Response(content, status=status.HTTP_400_BAD_REQUEST)
