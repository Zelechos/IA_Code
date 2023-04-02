#2. Identificar los códigos ASCCI manuscritos utilizando una red neuronal convolucional (la arquitectura y la capacidad de la red deberá ser definida por usted, buscando lograr al menos un 95% con un dataset de prueba).
# Imports
import torch
import torchvision # torch package for vision related things
import torch.nn.functional as F  # Parameterless functions, like (some) activation functions
import torchvision.datasets as datasets  # Standard datasets
import torchvision.transforms as transforms  # Transformations we can perform on our dataset for augmentation
from torch import optim  # For optimizers like SGD, Adam, etc.
from torch import nn  # All neural network modules
from torch.utils.data import DataLoader  # Gives easier dataset managment by creating mini batches etc.
from tqdm import tqdm  # For nice progress bar!
from torch.utils.data import (Dataset,DataLoader,) 
import pandas as pd
import os
from skimage import io

# Simple CNN
class CNN(nn.Module):
    def __init__(self, in_channels=1, num_classes=1):
        super(CNN, self).__init__()
        
        #First CNN
        self.conv1 = nn.Conv2d(
            in_channels = in_channels,
            out_channels= 6,
            kernel_size=(3, 3),
            stride=(1, 1),
            padding=(1, 1),
        )
    
        
        self.pool = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))
        
        #Second CNN
        self.conv2 = nn.Conv2d(
            in_channels= 6,
            out_channels=12,
            kernel_size=(3, 3),
            stride=(1, 1),
            padding=(1, 1),
        )
        
        self.fc1 = nn.Linear(12 * 50 * 45, num_classes)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        #print("conv 1")
#         print(x.shape)
        x = self.pool(x)
#         print("pool 1")
#         print(x.shape)
        x = F.relu(self.conv2(x))
#         print("conv 2")
#         print(x.shape)
        x = self.pool(x)
#         print("pool 2")
#         print(x.shape)
#         print("Shape 1")
#         print(x.shape)
#         print(x.shape[0])
#         print(x.shape[1])
        x = x.reshape(x.shape[0], -1)
#         print("Shape 2")
#         print(x.shape)
#         print(x.shape[0])
#         print(x.shape[1])
        x = self.fc1(x)
#         print("esta es la x del fc1 : ",x)
        return x

# model = CNN()
# x = torch.rand(64, 1, 28, 28)
# print(x)
# print(model(x).shape)
# # Set device
class Dataset_treatment(Dataset):
    def __init__(self,csv_file , root_dir, transform=None):
        self.annotations = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        img_path = os.path.join(self.root_dir, self.annotations.iloc[index, 0])
        image = io.imread(img_path)
        y_label = torch.tensor(int(self.annotations.iloc[index, 1]))

        if self.transform:
            image = self.transform(image)

        return (image, y_label)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Hyperparameters
in_channels = 4
num_classes = 5
learning_rate = 0.001
batch_size = 250
num_epochs = 500


# Load Data
dataset = Dataset_treatment(    
    csv_file="ASCCI.csv",
    root_dir="dataset",
    transform = transforms.ToTensor(),
)

# Dataset is actually a lot larger ~25k images, just took out 10 pictures
# to upload to Github. It's enough to understand the structure and scale
# if you got more images.
# Load Data
train_set, test_set = torch.utils.data.random_split(dataset, [128,128])
train_loader = DataLoader(dataset=train_set, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(dataset=test_set, batch_size=batch_size, shuffle=True)

# Initialize network
model = CNN(in_channels=in_channels, num_classes=num_classes).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Train Network
for epoch in range(num_epochs):
    for batch_idx, (data, targets) in enumerate(tqdm(train_loader)):
        # Get data to cuda if possible
        data = data.to(device=device)
        targets = targets.to(device=device)

        # forward
        scores = model(data)
        loss = criterion(scores, targets)

        # backward
        optimizer.zero_grad()
        loss.backward()

        # gradient descent or adam step
        optimizer.step()

# Check accuracy on training & test to see how good our model
def check_accuracy(loader, model):
    num_correct = 0
    num_samples = 0
    model.eval()

    with torch.no_grad():
        for x, y in loader:
            x = x.to(device=device)
            y = y.to(device=device)

            scores = model(x)
            _, predictions = scores.max(1)
            num_correct += (predictions == y).sum()
            num_samples += predictions.size(0)


    model.train()
    return num_correct/num_samples


print(f"Accuracy on training set: {check_accuracy(train_loader, model)*100:.2f}")
print(f"Accuracy on test set: {check_accuracy(test_loader, model)*100:.2f}")