import os
import shutil
import uuid
from Classes.tkinterwidgets.getfileswidget import GetImagesWidget
from tkinter import PhotoImage


# Generate list of photoimage objects ready to be used as image=Photoimage_object
def generate_PhotoImage_list(self, list_packed_images_path: str, _subsample=4):
    list_unpacked_images_path = self.unpack_db_images_path(
        list_packed_images_path)
    photo_image_object_list = []
    for _image_path in list_unpacked_images_path:
        try:
            photo_image_object_list.append(PhotoImage(
                file=_image_path).subsample(_subsample))
        except:
            pass  # image doesn't exist
        self.image_references.extend(photo_image_object_list)
    return photo_image_object_list  # PhotoImage object list


# Takes the amalgam string that holds the path to all images and unpacks it into a list
def unpack_db_images_path(self, packed_images_path: str):
    list_unpacked_images_path = []
    if packed_images_path != '':
        list_packed_images_path = packed_images_path.split('#{@!#')
        for _image_path in list_packed_images_path:
            try:
                if _image_path != '':
                    list_unpacked_images_path.append(
                        _image_path.strip('#{@!#'))
            except:
                pass  # image doesn't exist
    return list_unpacked_images_path


# Tries to delete the actual images on disk that are referred in the image_path_list
def delete_images(self, image_path_list):
    for image in image_path_list:
        try:
            os.remove(image)
        except:
            pass


# this works in association with getimageswidget
# Once the user submits, it gets the current paths and calculates the difference of before and after
# the user has inputted his images
# the images that were already there will stay in their saved folder, the removed ones, it removes them
# and the added ones will be copied to the save foler and be renamed to a unique name (uuid1)
# it will then take all of the paths of the current images and concatenate them into a string to be
# returned to the user
# the string is ready to be saved on the database
def get_image_paths_str_DB_ready(self, __wgt: GetImagesWidget):
    images_path_list = __wgt.get_PATHS()
    removed_list, added_list = __wgt.get_difference()
    images_db_list = ''
    if not os.path.exists('Images'):
        os.makedirs('Images')
    for image in images_path_list:
        if image in added_list:
            destination = './Images/' + str(int(uuid.uuid1()))
            __extension = ''
            for j in range(image.rindex('.'), len(image)):
                __extension += image[j]
            destination += __extension
            shutil.copyfile(image, destination)
        else:
            destination = image
        images_db_list += destination + '#{@!#'
    self.delete_images(removed_list)
    return images_db_list
