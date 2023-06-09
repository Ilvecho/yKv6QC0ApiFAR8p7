import pandas as pd
import torch
from torch import nn

# Some Global parameters
N_ATTRIBUTES = 6        # This could be extracted from the data shape, but for simplicity I just declare it here
N_OUTPUTS = 1
learning_rate = 0.1    # Standard value for a learning rate
N_EPOCHS = 10000

# Auxiliary class to manipluate the dataset. Once again, it's not necessary in this case, but makes the code easily scalable
def DataLoader(file_name, split: float):

    data = pd.read_csv(file_name)

    attributes = torch.tensor(data.drop('Y', axis=1).values).float()
    labels = torch.tensor(data['Y'].values).unsqueeze_(1)

    # split the dataset in training and validation
    train_attributes = attributes[:int(attributes.shape[0]*split)].float()
    val_attributes = attributes[int(attributes.shape[0]*split):].float()

    train_labels = labels[:int(attributes.shape[0]*split)].float()
    val_labels = labels[int(attributes.shape[0]*split):].float()
    
    return train_attributes, val_attributes, train_labels, val_labels


# Class that defines the Neural Network: in this particular case it's not necessary, given the simple structure of the network
# However, this solution is easily scalable
class SingleLayerPerceptron(nn.Module):
  def __init__(self):
    super().__init__()
    self.stack = nn.Sequential(
        nn.Linear(N_ATTRIBUTES, N_OUTPUTS),
        nn.Sigmoid()
    )
  
  def forward(self, x):
    logits = self.stack(x)
    return logits



train_attributes, val_attributes, train_labels, val_labels = DataLoader('ACME-HappinessSurvey2020.csv', 0.85)

model = SingleLayerPerceptron()
loss_fn = nn.CrossEntropyLoss()
# loss_fn = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

# train loop - we use the full dataset every time, and repeat for few epochs
# Need to change it to batches
N_EPOCHS = 10000

for e in range(N_EPOCHS):
  pred = model(train_attributes)
  loss = loss_fn(pred, train_labels)
  if e % 500 == 0:
    print(f'Epoch {e} shows a loss of {loss}')

  loss.backward()
  optimizer.step()
  optimizer.zero_grad()


# Validation
pred = model(val_attributes)
print(pred)
print(val_labels)
print(loss_fn(pred, val_labels))