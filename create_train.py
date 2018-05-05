import argparse
import sys
import os

import tf_scripts.retrain as tf_retrain

from scripts.StructureFileCreator import StructureFileCreator
from contextlib import redirect_stdout

IMAGE_DIR = 'jpg_image/product'
LEARNING_RATE = 0.001
BATCH_SIZE = 10
STEPS_NUMBER = 4000
MODEL_NAME = "mobilenet"
MODEL_SIZE = 1.0
IMAGE_SIZE = 224
ARCHITECTURE = MODEL_NAME + "_" + \
    str(float(MODEL_SIZE)) + "_" + str(IMAGE_SIZE)

if __name__ == "__main__":

    path_to_data = './data/decor'
    output_directory = './jpg_image'
    csv_data = './data/decor.csv'

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--path', help='path to images from which will be create structure, defaul = ./data/decor', type=str)
    parser.add_argument(
        '--output', help='direcory where structure should be create, default=./jpg_image', type=str)
    parser.add_argument(
        '--csv', help='path to csv file with data, dafault = ./data/decor.csv', type=str)

    args, unparsed = parser.parse_known_args()

    if args.path:
        path_to_data = args.path
    if args.output:
        output_directory = args.output
    if args.csv:
        csv_data = args.csv

    # Creating structure
    my_creator = StructureFileCreator(
        path_to_data, output_directory, csv_data, True)
    my_creator.run()

    # Removing label which contain less than 31 images
    my_creator.remove_directory_contain_not_enough_images()

    # Setting flags tu retrain.py script
    tf_retrain.FLAGS = argparse.Namespace()
    tf_retrain.FLAGS.architecture = ARCHITECTURE  # 'mobilenet_0.50_224'
    tf_retrain.FLAGS.bottleneck_dir = 'tf_files/bottlenecks'
    tf_retrain.FLAGS.eval_step_interval = 100
    tf_retrain.FLAGS.final_tensor_name = 'final_result'
    tf_retrain.FLAGS.flip_left_right = False
    tf_retrain.FLAGS.how_many_training_steps = STEPS_NUMBER
    tf_retrain.FLAGS.image_dir = IMAGE_DIR
    tf_retrain.FLAGS.intermediate_output_graphs_dir = '/tmp/intermediate_graph/'
    tf_retrain.FLAGS.intermediate_store_frequency = 0
    tf_retrain.FLAGS.learning_rate = LEARNING_RATE
    tf_retrain.FLAGS.model_dir = 'tf_files/models/'
    tf_retrain.FLAGS.output_graph = 'tf_files/retrained_graph.pb'
    tf_retrain.FLAGS.output_labels = 'tf_files/retrained_labels.txt'
    tf_retrain.FLAGS.print_misclassified_test_images = False
    tf_retrain.FLAGS.random_brightness = 0
    tf_retrain.FLAGS.random_crop = 0
    tf_retrain.FLAGS.random_scale = 0
    tf_retrain.FLAGS.summaries_dir = 'tf_files/training_summaries/' + ARCHITECTURE
    tf_retrain.FLAGS.test_batch_size = -1
    tf_retrain.FLAGS.testing_percentage = 10
    tf_retrain.FLAGS.train_batch_size = BATCH_SIZE
    tf_retrain.FLAGS.validation_batch_size = 100
    tf_retrain.FLAGS.validation_percentage = 10

    unparsed = []

    # Train model

    tf_retrain.tf.app.run(main=tf_retrain.main, argv=[sys.argv[0]] + unparsed)

    # bad solution to avoid error with to less number of image
    # edit line 192 in retrain.py as above:
    #   if len(validation_images) == 0:
    #         validation_images.append(base_name)
    #       elif percentage_hash < validation_percentage:
