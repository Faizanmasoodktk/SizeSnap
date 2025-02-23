from django.shortcuts import render
import cv2
from io import BytesIO
import base64
from django.http import JsonResponse
from rembg import remove
from PIL import Image

# Create your views here.
def remove_background(asset_image):
    """This function will remove the background from image"""
    try: 
        pil_image = Image.open(asset_image) # this will open the image through pillow library for processing
        print(f"This is image after pillow {pil_image}")
        image_with_no_bg = remove(pil_image) # this will remove the background from image

        buffer = BytesIO() # this will creat a buffer -> buffer is temperory storage like space in ram, which can hold bytes data for us
        if asset_image.content_type.split("/")[-1].lower() == "jpeg" or asset_image.content_type.split("/")[-1].lower() == "jpg":
            image_with_no_bg.save(buffer, format="PNG") # this will save the image in the buffer temporary, here save method also 
        else:
            image_with_no_bg.save(buffer, format=asset_image.content_type.split("/")[-1].upper()) # this will save the image in the buffer temporary, here save method also 
                                                    # take format option like .save(buffer, format="PNG") 

        # here b64encode only take byte value, so have to convert the to bytes, which done in upper line,
        encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8') # then now we have to fetch the value from buffer
        print(f'Background remove from {asset_image.name}')
    except Exception as e:
        print(e)
        encoded_image = ""
    finally: 
        buffer.close()
        return encoded_image # this will return the image


def process(request):
    print('request came in process after editing')
    session = request.session
    try:
        process_image_list = session.get('process_images', []) # this will retreuve the process images if not found, intiaized with empty

    except:
        pass

    if request and request.method == 'POST':
        images = request.FILES.getlist('images')

        for image in images:

            base64_image_no_bg = remove_background(image)

            image_data = {
                "name" : image.name, # this will set the name for image
                "data" : base64_image_no_bg, # this will set the data of image from which we can prepare image again
                "type" : image.content_type, # this will set the conten type of image like png, jpg etc
            }
            
            process_image_list.append(image_data)
            print(f'{image.name} added to list')
        session["process_images"] = process_image_list
        return JsonResponse({'status': 'success', 'message': 'Images successfully uploaded'})

    return render(request, 'home.html')

