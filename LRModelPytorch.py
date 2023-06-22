from aida.aida import *
import time
import torch

class LRModel:
    class LinearRegression(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = torch.nn.Linear(5, 1)

        def forward(self, data):
            return self.linear(data)
    def __init__(self):
        import torch
        self.weights = None
        self.optimizer = None
        self.model = self.LinearRegression

    @staticmethod
    def iterate(db, data, weights):
        import torch

        model = weights
        try:
            batch, target = next(db.iterator)
        except StopIteration:
            db.iterator = iter(data.getLoader())
            batch, target = next(db.iterator)

        preds = model(torch.squeeze(batch).float())
        loss = db.loss(torch.squeeze(preds), target)
        loss.backward()
        grads = []
        for param in model.parameters():
            grads.append(param.grad)
        return grads

    @staticmethod
    def preprocess(db, data):
        import torch
        data.makeLoader([('x1', 'x2', 'x3', 'x4', 'x5'), 'y'], 1000)
        db.iterator = iter(data.getLoader())
        db.loss = torch.nn.MSELoss()
        return data

    def initialize(self, data):
        import torch
        self.weights = self.model()
        self.optimizer = torch.optim.SGD(self.weights.parameters(), lr=1e-3)

    def aggregate(self, results):
        self.optimizer.zero_grad()
        for grad, param in zip(results, self.weights.parameters()):
            param.grad = grad
        self.optimizer.step()


dw = AIDA.connect('nwhe_middleware', 'bixi', 'bixi', 'bixi')
print('Registering model')
service = dw._RegisterModel(LRModel)
print('Fitting model')
start = time.perf_counter()
service.fit(dw.lr_data, 50000, sync=False)
stop = time.perf_counter()
print(f'Central Model finished in {stop-start}')
dw._close()
