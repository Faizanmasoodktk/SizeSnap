from django.shortcuts import render
import cv2
from io import BytesIO
import base64
from django.http import JsonResponse
from rembg import remove
from PIL import Image

# def remove_background(asset_image):

#     try: 
#         pil_image = Image.open(asset_image) # this will open the image through pillow library for processing
#         print(f"This is image after pillow {pil_image}")
#         image_with_no_bg = remove(pil_image) # this will remove the background from image

#         buffer = BytesIO() # this will creat a buffer -> buffer is temperory storage like space in ram, which can hold bytes data for us
#         if asset_image.content_type.split("/")[-1].lower() == "jpeg" or asset_image.content_type.split("/")[-1].lower() == "jpg":
#             image_with_no_bg.save(buffer, format="PNG") # this will save the image in the buffer temporary, here save method also 
#         else:
#             image_with_no_bg.save(buffer, format=asset_image.content_type.split("/")[-1].upper()) # this will save the image in the buffer temporary, here save method also 
#                                                     # take format option like .save(buffer, format="PNG") 

#         # here b64encode only take byte value, so have to convert the to bytes, which done in upper line,
#         encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8') # then now we have to fetch the value from buffer
#         print(f'Background remove from {asset_image.name}')
#     except Exception as e:
#         print(e)
#         encoded_image = ""
#     finally: 
#         buffer.close()
#         return encoded_image # this will return the image


def home(request):
    print('request cam here')


    return render(request, 'home.html')

# This is imple process function just storing the data in session and showed to user we make it for practice
# def process(request):
#     print('request came in process aftee editing')
#     session = request.session
#     try:
#         print('it came in try block')
#         process_image_list = session.get('process_images', []) # this will retreuve the process images if not found, intiaized with empty
#         # print(process_images)
#         print('this is the length and type of process images', len(process_image_list), type(process_image_list))
#         for image in process_image_list:
#             print(image['name'])
#             print(image['type'])
#             # print(f"this is stored image type name  {image.name}\n and this is data  \nand this is type{image.type}")
#     except:
#         pass

#     if request and request.method == 'POST':
#         images = request.FILES.getlist('images')

#         for image in images:
#             # if image.name in process_image_list.values():
#             #     print('This image is present in sesssion')
#             #     continue
#             image_bytes = BytesIO(image.read()) # here read function will read the image, then bytesio funtion convert
#                                                 # it into in memory bytes, in memory can easily store in ram, with out
#                                                 # using data of hard disk, 
#             print("\n this is bytes io images type", image_bytes)
#             base64_image = base64.b64encode(image_bytes.getvalue()).decode('utf-8')
#             """ Here first getvalue() function get the value from bytes image, then we encoded that value in 
#             base64, b64 is normal text like endcoding, so we convert in memory bytes data ascii text which is normal 
#             encoding, it is best but we then convert that data to utf-8 encoding method which is good for html"""
#             # print('\nthis is bytes 64 image type : ', base64_image)

#             image_data = {
#                 "name" : image.name, # this will set the name for image
#                 "data" : base64_image, # this will set the data of image from which we can prepare image again
#                 "type" : image.content_type, # this will set the conten type of image like png, jpg etc
#             }
            
#             process_image_list.append(image_data)
#             print(f'{image.name} added to list')
#         session["process_images"] = process_image_list
#         return JsonResponse({'status': 'success', 'message': 'Images successfully uploaded'})

#     return render(request, 'home.html')


# def process(request):
#     print('request came in process aftee editing')
#     session = request.session
#     try:
#         process_image_list = session.get('process_images', []) # this will retreuve the process images if not found, intiaized with empty

#     except:
#         pass

#     if request and request.method == 'POST':
#         images = request.FILES.getlist('images')

#         for image in images:

#             base64_image_no_bg = remove_background(image)

#             image_data = {
#                 "name" : image.name, # this will set the name for image
#                 "data" : base64_image_no_bg, # this will set the data of image from which we can prepare image again
#                 "type" : image.content_type, # this will set the conten type of image like png, jpg etc
#             }
            
#             process_image_list.append(image_data)
#             print(f'{image.name} added to list')
#         session["process_images"] = process_image_list
#         return JsonResponse({'status': 'success', 'message': 'Images successfully uploaded'})

#     return render(request, 'home.html')


def show_images(request):
    images = []
    try:
        images = request.session["process_images"]
    except:
        pass
    if images and len(images) > 0 and "name" in images[0]:
        print(f'it come in show images,  {images[0]["type"]}')

    context = {
        "images" : images,
    }
    return render(request, "home.html", context=context)


def clear_session(request):
    print(f'it come in clear session')
    try:
        del request.session["process_images"]
    except:
        pass
    return render(request, 'home.html', {"message": "Session cleared Successfully."})
    
    