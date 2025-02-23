from django.shortcuts import render
import numpy as np
import cv2
import base64
from django.http import JsonResponse
# Create your views here.
# https://www.instagram.com/p/DE2d8WwM-eo/comments/
def resize(request):
    """This function will resize the image"""
    print(f'request came to resize')
    session = request.session
    try:
        process_image_list = session.get('process_images', [])

    except Exception as e:
        pass

    if request and request.method == 'POST':
        images = request.FILES.getlist("images")
        width = int(round(float(request.POST.get("width"))))
        height = int(round(float(request.POST.get("height"))))
        print(f'this is width {type(width)}, height {type(height)}')
        print(f'this is width {width}, height {height}')
        try:
            for image in images:
                image_type = image.content_type
                image_name = image.name
                print(f'this is image type {image_type} and this is name {image_name}')
                # start processing
                image_byte = image.read() # this will read the image and convert it into bytes
                print(f'image readout')
                image_np_array = np.frombuffer(image_byte, np.uint8) # this will create an numpy 1D numpy array
                print(f'image convert to numpy array')
                image = cv2.imdecode(image_np_array, cv2.IMREAD_UNCHANGED) # THIS WILL creat 2D or 3D array of numpy for image, and reading for resize
                print(f'image decoded')
                # the resize function take image is source(required), and dimension(required), while the interpolation
                # is optional, interpolation is simply fill the gap b/w pixel, during scaling or shrinking
                # here inner_area will the gap based on the average which is better choice in our case as it preserve quality
                resize_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
                print(f'image resized')
                # it return the encoded image in format desired and one flag tells about sucess or fail
                print(f'this is image type {image_type} and this is slipted {image_type.split("/")[-1]}')
                status, image = cv2.imencode(f".{image_type.split('/')[-1]}", resize_image)
                print(f'image encoded')
                base64_image_reized = base64.b64encode(image.tobytes()).decode('utf-8') # we convert the image to base 64 for safe transfer
                image_data = {
                    "name" : image_name, # this will set the name for image
                    "data" : base64_image_reized, # this will set the data of image from which we can prepare image again
                    "type" : image_type, # this will set the conten type of image like png, jpg etc
                }

                # append it the list
                process_image_list.append(image_data)
                print(f'{image_name} added to list')

        except Exception as e:
            print(f'some exception occured in proccessing the image {e}')
            return JsonResponse({'status': 'fail', 'message': 'Some error occured in processing'})

        session["process_images"] = process_image_list
        return JsonResponse({'status': 'success', 'message': 'Images successfully resized'})
    
    return render(request, 'home.html', )
