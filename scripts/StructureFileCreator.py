import os
import argparse
import shutil
import pandas as pd

from PIL import Image


class StructureFileCreator:

    """
    Scan input directory and looking for png file, convert this file to jpg. Divide folder of images to subfolder base on svn file with data about type and decor name.
    This structure is preparation to tensorflow script.

    Structure look like (for traditional-decor-patterns):

        output_path             
            - product
                - Gorodets
                - Gzhel
            - pattern
                - Gorodets
                - Gzhel
        generally:
        output_path
            - type_1
                - name_1
                - name_2
            - type_2
                - name_1
                - name_2

    """

    def __init__(self, image_path, output_path, decor_svn_path, process_pattern=False):
        """
        Initial function to set parameters
        :param image_path: string containing path to folder with images
        :param output_path: string with path to output folder 
        :param decor_svn_path: string to svn file containing data about images, use type and decor columns
        :param process_pattern: bool default=False, if True pattern type will be processed 
        """
        self.image_path = image_path
        self.path_to_jpg = output_path
        self.process_pattern = process_pattern
        self.decor_svn_path = decor_svn_path
        self.image_width = None
        self.image_height = None

        try:
            self.decor_data = pd.read_csv(self.decor_svn_path)
        except Exception as error:
            print("Error: {0}".format(error))
        if not self.process_pattern:
            self.decor_data = self.decor_data[self.decor_data.type != 'pattern']

    def set_size(self, image_width=None, image_height=None):
        """
        Set width and height of loaded image, all image must have the same size, 
        if parameters are none fuction find first png image and get his size as size all images.
        :param image_width: default None, width of each image
        :param image_height: default None, height of each image
        """
        if not image_height or not image_width:
            for file in os.listdir(os.path.abspath(self.image_path)):
                filename = os.fsdecode(file)
                if filename.endswith(".png"):
                    image = Image.open(os.path.join(self.image_path, filename))
                    self.image_width, self.image_height = image.size
                    break
        else:
            self.image_width = image_width
            self.image_height = image_height

    def run(self,):
        """
        Create structures of folders and subfolders, convert image ans save this image. 
        """
        if not self.image_width or not self.image_height:
            self.set_size()

        directory = os.path.abspath(self.image_path)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".png"):
                rgb_image = get_jpg_from_png_image(os.path.join(
                    self.image_path, filename))
                new_file_name = os.path.splitext(filename)[0] + '.jpg'
                decor_name = self.decor_data[
                    self.decor_data.file == filename]['decor'].values
                decor_type = self.decor_data[
                    self.decor_data.file == filename]['type'].values
                if decor_name:
                    new_file_path = os.path.join(self.path_to_jpg,
                                                 decor_type[0],
                                                 decor_name[0])
                    if not os.path.exists(new_file_path):
                        os.makedirs(new_file_path)
                    rgb_image.save(os.path.join(new_file_path, new_file_name))

    def remove_directory_contain_not_enough_images(self,):
        for folder in os.listdir(self.path_to_jpg):
            subfolder_path = os.path.join(self.path_to_jpg, folder)
            for subfolder in os.listdir(subfolder_path):
                decor_path = os.path.join(subfolder_path, subfolder)
                files = [file for file in os.listdir(
                    decor_path) if file.endswith(".jpg")]
                if len(files) < 20:
                    shutil.rmtree(decor_path, ignore_errors=True)


def get_jpg_from_png_image(file):
    """
    Function which convert input file (image) to rgb image.
    :param file: path to file which will be converted.
    :return rgb_image: pillow image converted with RGB
    """
    image = Image.open(file)
    rgb_image = image.convert('RGB')
    return rgb_image


if __name__ == '__main__':

    # Initial values
    image_path = None
    output_path = None
    decor_svn_path = None
    process_pattern = False
    image_width = 0
    image_height = 0

    # Script arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'image_path', help='string containing path to folder with images', type=str)
    parser.add_argument(
        'output_path', help='string containing path to folder with images', type=str)
    parser.add_argument(
        'decor_svn_path', help='string to svn file containing data about images', type=str)
    parser.add_argument(
        '--process_pattern', help=' bool default=False, if True pattern type will be processed', type=bool)
    parser.add_argument(
        '--image_width', help=' int, width of image', type=int)
    parser.add_argument(
        '--image_height', help=' int, height of image', type=int)

    args = parser.parse_args()

    if args.process_pattern:
        process_pattern = args.process_pattern
    if args.image_path:
        image_path = args.image_path
    if args.output_path:
        output_path = args.output_path
    if args.decor_svn_path:
        decor_svn_path = args.decor_svn_path
    if args.image_width:
        image_width = args.image_width
    if args.image_height:
        image_height = args.image_height

    # Creating structure
    structure_creator = StructureFileCreator(
        image_path=image_path,
        output_path=output_path,
        decor_svn_path=decor_svn_path,
        process_pattern=process_pattern)
    structure_creator.set_size(image_width, image_height)

    # Print final message
    if not structure_creator.run():
        print("Structure was created.")
        print('Path: ' + output_path)
