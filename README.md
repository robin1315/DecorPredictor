## Table of contents
1. [Repository description](#decor_predictor)
2. [How to use](#how_to_use)
3. [Architecture](#architecture)
4. [Result](#result)

## Decor Predictor

Simple example of using [TensorFlow](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/#0) 
script to create classifier for pruducts from this dataset:
[Decor](https://www.kaggle.com/olgabelitskaya/traditional-decor-patterns/data)

The solution was written in [Python 3.6.5](https://www.python.org/downloads/release/python-365/).

Used libraries:
- [tensorflow](https://www.tensorflow.org/)
- [pandas](https://pandas.pydata.org/)
- [pillow](https://pillow.readthedocs.io/en/5.1.x/)

## How to use

Local machine:
1. Clone repository 
  ``` 
  git clone https://gitlab.com/robert-kowalski/DecorPredictor.git 
  ```
2. Install the required libraries using e.g. 
  ```
  pip install -r .\requirements.txt 
  ```
3. Enter to main directory and run create_train.py in terminal 
   (script prepare files and train model) 
  ``` 
  python create_train.py
  ```  

4. To get prediction run 
  ```
  python .\tf_scripts\label_image.py --image=path_to_image
  ```
  
  e.g 
    
  ```
  python .\tf_scripts\label_image.py --image=test_data\wz_low.jpg
  ```


Docker:
1. Install [Docker](https://www.docker.com/)
2. Clone repository 
  ``` 
  git clone https://gitlab.com/robert-kowalski/DecorPredictor.git 
  ```
3. Enter to main folder and run 
  ``` 
  docker-compose up -d --build 
  ```
4. Check name of created container by run 
  ```
  docker ps 
  ```

   Should be somethink like ```decorpredictor_decor_container_1```

5. To enter into container type:
  ```
  docker exec -t -i decorpredictor_decor_container_1 bash
  ``` 

6. Run create_train.py (script prepare files and train model): 
  ```
  python create_train.py
  ```
7. To get prediction run 
  ```
  python ./tf_scripts/label_image.py --image=path_to_image
  ```
    
  e.g. 
    
  ```
  python ./tf_scripts/label_image.py --image=./test_data/wz_low.jpg
  ```


##### Protip

Tensorflow required python x64 and jpg image only.

## Architecture

- ***best_accuracy*** - folder contains model and screens with 
  best achieved accuracy. 
- ***data*** - inside are dataset and csv file from decor database
- ***jpg_image*** - created after run script, stores converted 
  image in structured form
- ***scripts*** - contains python files
- ***test_data*** - inside are some example of test images
- ***tf_files*** - all structure of files create by tesorflow
  scripts
- ***tf_scripts*** - all tensorflow scripts

Main folder contains two important files:
- ***create_train.py*** - create right structure for learning 
  script and run this script, use predefined parameters
- ***only_train.py*** - only train model if structure was created 
  before. 


## Result
Best result which was achieved:

96% final accuracy

for the following parameters:
```python
LEARNING_RATE = 0.001
BATCH_SIZE = 10
STEPS_NUMBER = 4000
MODEL_NAME = "mobilenet"
MODEL_SIZE = 1.0
IMAGE_SIZE = 224
``` 

All parameters are defined in ***create_train.py*** and ***only_train.py***.