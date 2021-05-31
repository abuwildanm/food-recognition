# Indonesian Food Recognition

## Introduction

In this project, we try to build a model to recognize Indonesian foods such as rice, omelette, tempeh, and tofu. For now, our model can only recognize that four types of food. Our hope is that in the future we can improve the performance of the model so that the model can recognize more types of Indonesian food

## Getting Started

1. Follow this [notebook](https://github.com/abuwildanm/food-recognition/blob/master/Create_Custom_Dataset_From_Google_Images.ipynb) to create custom dataset from Google Images
2. Annotate the image dataset using [labelImg](https://github.com/tzutalin/labelImg) tool
3. Follow this [notebook](https://github.com/abuwildanm/food-recognition/blob/master/Food_Recognition_ML_Model.ipynb) to train the model
4. If you want to create custom dataset for model training in Vertex AI, you can follow this [notebook](https://github.com/abuwildanm/food-recognition/blob/master/Create_Dataset_For_Vertex_AI.ipynb)
5. Follow this [instruction](https://github.com/abuwildanm/food-recognition/tree/master/flask-vm-server) to deploy the model
6. If you want to convert your model to Tensorflow model or Tensorflow Lite model, you can follow this [notebook](https://github.com/abuwildanm/food-recognition/blob/master/Create_Tensorflow_Model_from_YOLO.ipynb)
