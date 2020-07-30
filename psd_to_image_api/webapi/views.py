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
from .models import JsonData
import ast


@api_view(['POST'])
def upload(request):
    file = request.FILES['pdf']
    timestamp = datetime.timestamp(datetime.now())
    path = default_storage.save('media/' + str(timestamp) + '.pdf', ContentFile(file.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    images = convert_from_path(tmp_file, dpi=70)
    count = 0
    content = []
    for image in images:
        temp = {}
        count = count + 1
        temp['page'] = count
        real_image = "media/" + str(timestamp) + str(count) + ".webp"
        image.resize((1438, 922))
        image.save(real_image, "webp", optimize=True, quality=7)
        temp['image'] = real_image
        image.resize((119, 185))
        thumb = "media/" + str(timestamp) + str(count) + "-thumb.webp"
        image.save(thumb, "webp", optimize=True, quality=7)
        temp['thumb'] = thumb
        content.append(temp)
    finalc = JsonData.objects.create(
        content=content
    )
    finalc.save()
    return Response(content, status=status.HTTP_200_OK)


@api_view(['GET'])
def latest(request):
    data = JsonData.objects.all().order_by('-id')[0]
    return Response(ast.literal_eval(data.content), status=status.HTTP_200_OK)

# except ValueError:
#     content = {
#         'message': "Please upload the file"
#     }
# return Response(content, status=status.HTTP_400_BAD_REQUEST)
