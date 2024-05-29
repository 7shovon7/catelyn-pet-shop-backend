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
