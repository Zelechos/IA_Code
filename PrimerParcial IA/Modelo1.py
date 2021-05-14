#1. Predecir el tipo de cambio del dólar para los meses de mayo a diciembre del 2021
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms  # Transformations we can perform on our dataset for augmentation
from tqdm import tqdm
import pandas as pd
import os

class Dataset_treatment(Dataset):
    def __init__(self, csv_file , root_dir, transform=None):
        self.annotations = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        Mes = self.annotations.iloc[index, 0]
        PrecioDolar = self.annotations.iloc[index, 1]
        return (Mes, PrecioDolar)
    

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

dataset = Dataset_treatment(
    csv_file= "dolar.csv",
    root_dir= "DataSet",
    transform = transforms.ToTensor(),
    )     

print(len(dataset))
print(dataset.__getitem__(23))
print("++++++++++++++++++++++")

dataloader = DataLoader(dataset, batch_size=23 , shuffle=True)

x , y = next(iter(dataloader))
print(x)
print("--------------------------")
print(y.shape)


class SimpleRNN(torch.nn.Module):
    def __init__(self):
        super.__init__()
        #Instancion nuestra Red Neuronal Recurrente
        self.rnn = torch.nn.RNN(
        input_size = 1, #El Tamaño de la entrada
        hidden_size = 1, #La Cantidad de Neuronas en la Capa Oculta
        num_layers =  1, #La Cantidad de Capaz Ocultas que tendra
        batch_first = True #    
        )
        
    def Forward(self, x):
        y , _ = self.rnn(x)
        # Obtenemos la Ultima salida
        return y[: , -1]

rnn = SimpleRNN()


def fit(model, dataloader, epochs=10):
    model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = torch.nn.MSELoss()
    bar = tqdm(range(1, epochs+1))
    for epoch in bar:
        model.train()
        train_loss = []
        for batch in dataloader:
            X, y = batch
            X, y = X.to(device), y.to(device)
            optimizer.zero_grad()
            y_hat = model(X)
            loss = criterion(y_hat, y)
            loss.backward()
            optimizer.step()
            train_loss.append(loss.item())
        model.eval()
        eval_loss = []
        with torch.no_grad():
            for batch in dataloader:
                X, y = batch
                X, y = X.to(device), y.to(device)
                y_hat = model(X)
                loss = criterion(y_hat, y)
                eval_loss.append(loss.item())
        bar.set_description(f"loss {np.mean(train_loss):.5f} val_loss {np.mean(eval_loss):.5f}")
        
def predict(model, dataloader):
    model.eval()
    with torch.no_grad():
        preds = torch.tensor([]).to(device)
        for batch in dataloader:
            X = batch
            X = X.to(device)
            pred = model(X)
            preds = torch.cat([preds, pred])
        return preds
    
fit(rnn , dataloader)