# project_name/views.py
from django.shortcuts import render
import os
from django.http import FileResponse, HttpResponseNotFound

def returnImgResponse(request, rootFolder, fileName):
    folder_path = os.path.join('media', rootFolder)
    file_path = os.path.join(folder_path, fileName)

    if os.path.exists(file_path) and os.path.isfile(file_path):
        response = FileResponse(open(file_path, 'rb'))

        if fileName.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            response['Content-Type'] = 'image/jpeg'
        else:
            response['Content-Type'] = 'application/octet-stream'

        return response
    else:
        return HttpResponseNotFound("File not found!")