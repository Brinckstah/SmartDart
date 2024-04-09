import torch
import torchvision
import torchvision.transforms as transform

# https://stackoverflow.com/questions/20554074/sklearn-omp-error-15-initializing-libiomp5md-dll-but-found-mk2iomp5md-dll-a
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# Tensor transform needs a list
tensor_transform = transform.Compose([transform.ToTensor()])
train_data = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=tensor_transform)
val_data = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=tensor_transform)

train_data, val_data

import numpy as np
import pandas as pd

#dict with classes - labeled
classes = {0: 'plane', 1:'car', 2: 'bird', 3:'cat', 4:'deer', 5:'dog', 6:'frog', 7:'horse', 8:'ship', 9:'truck'}
np.asarray(train_data[0][0]).shape

train_dataloader = torch.utils.data.DataLoader(train_data, batch_size=4, shuffle=True)
val_dataloader = torch.utils.data.DataLoader(val_data, batch_size=4, shuffle=False)

train_iter = iter(train_dataloader)
images, labels = next(train_iter)

import torch.nn as nn
import torch.nn.functional as F


#https://www.youtube.com/watch?v=Egz4bXMlmDM
#https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html
#https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.1039645/full
#https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html
#https://github.com/WillKoehrsen/deep-learning-v2-pytorch/blob/master/convolutional-neural-networks/cifar-cnn/cifar10_cnn_exercise.ipynb
#https://aoakintibu.medium.com/multilabel-classification-with-cnn-278702d98c5b


class ImageClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        #define layers, 3 input RGB space, transform into 6 channel feature maps, kernel size 5
        # 01: picture 32x32 aka 32 - kernel size 5 + 0 (padding)/ 1 (stride + 1,
        # 02: pool layer halving the resolution == 01 / 2
        # 03: (02 -5 +0)/ 1 + 1
        # 04: 03 / 2
        self.convl = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120) #  = pixel 400. 16 channels(16 kernels), 5 kommer fra 04
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10) #10 fordi vi har 10 klasser

    def forward(self, x):
        #activation function
        x = self.pool(F.relu(self.convl(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) #flatten everything but batch size
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)


# MODEL TRAINING
import torch.optim as optim
def hello():
    classifier_model = ImageClassifier()
    loss_function = nn.CrossEntropyLoss()
    optimiser = optim.SGD(classifier_model.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(10):
        running_loss = 0.0
        for i, batch in enumerate(train_dataloader, 0):
            images, labels = batch
            
            #zero gradient for optimiser
            optimiser.zero_grad()
            logits = classifier_model(images)
            loss = loss_function(logits, labels)
            loss.backward()
            optimiser.step()

            running_loss +=loss.item()
            if i % 2000 == 1999:
                print(f' [{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
                running_loss = 0.0

    print('finished training')
    torch.save(classifier_model.state_dict(), 'cifar10_classifier.pth')


def validation():
    model = ImageClassifier()
    model.load_state_dict(torch.load('cifar10_classifier.pth'))
    model.eval()
    
    correct = 0
    total = 0

    with torch.no_grad():
        for batch in val_dataloader:
            images, labels = batch
            logits = model(images)
            _, predicted = torch.max(logits.data, 1) # first dimension
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f'Accuracy over 10000 validations images: {100 * correct // total}%')

validation()


def load_trained_model(model_path):
    model = ImageClassifier()
    model.load_state_dict(torch.load(model_path))
    model.eval()  # Set to evaluation mode
    return model


def vizualize_model(result):
    train_loss = result.history['loss']
    train_acc = result.history['accuracy']
    val_loss = result.history['val_loss']
    val_acc = result.history['val_accuracy']

    pd.DataFrame({"Training Loss" : train_loss,
             "Validation Loss": val_loss,
             "Train Accuracy" : train_acc,
             "Validation Accuracy" : val_acc}).style.bar(color='#ff781c') 