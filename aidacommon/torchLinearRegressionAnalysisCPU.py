from aida.aida import *;
host = 'tfServer2608'; dbname = 'bixi'; user = 'bixi'; passwd = 'bixi'; jobName = 'torchLinear'; port = 55660;
dw = AIDA.connect(host,dbname,user,passwd,jobName,port);
def trainingLoop(dw,input_size, output_size,nn,torch,datasets,F,np):
    learningrate = 0.01
    epoch_size = 1000
    model = nn.Linear(input_size,output_size)
    criterion = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=learningrate)
    X, y = datasets.make_regression(n_samples=600000,n_features=1,noise=20,random_state=1)
    X = torch.from_numpy(X.astype(np.float32))
    y = torch.from_numpy(y.astype(np.float32))
    y = y.view(y.shape[0],1)
    for epoch in range(epoch_size):
        y_predicted = model(X)
        loss = criterion(y_predicted, y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    return(model.weight)

weight = dw._X(trainingLoop,1,1)
print(weight)
