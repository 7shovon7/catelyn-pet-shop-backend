from io import BytesIO
import sys
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def optimize_image(img, desired_height: int = 800):
    im = Image.open(img)
    im_format = im.format
    w, h = im.size
    if h > desired_height:
        aspect_ratio = w / h
        w = int(desired_height * aspect_ratio)
        h = desired_height
    im = im.resize((w, h), Image.LANCZOS)
    output = BytesIO()
    
    im.save(output, format=im_format, optimize=True, quality=50)    
    output.seek(0)
    
    return output, im_format


def optimize_image_in_upload_model(img, desired_height=800):
        
    output, im_format = optimize_image(img=img, desired_height=desired_height)
    
    modified_file = InMemoryUploadedFile(
        file=output,
        field_name='ImageField',
        name=img.name,
        content_type=f'image/{im_format.lower()}',
        size=sys.getsizeof(output),
        charset=None,
    )
    
    return modified_file


def change_filename(folder_path, original_filename, given_filename):
    file_parts = original_filename.split('.')
    if len(file_parts) > 1:
        updated_filename = f"{folder_path}/{given_filename}.{file_parts[-1]}"
    else:
        updated_filename = f"{folder_path}/{original_filename}"
    return updated_filename


def change_profile_image_filename(instance, filename):
    return change_filename(
        folder_path=f"profile/{instance.user.id}",
        original_filename=filename,
        given_filename='profile_image'
    )
    
    
def generate_username_from_email(email: str):
    return email.strip().lower().replace('@', '_')
