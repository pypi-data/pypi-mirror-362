def get_code():
    return '''
import numpy as np

X= np.array(([2,9],[1,5],[3,6]),dtype=float)
y= np.array(([92],[86],[89]), dtype=float)
X=X/np.amax(X,axis=0)
y=y/100

def sigmoid(x):
    return (1/(1+np.exp(-x)))

def derivatives_sigmoid(x):
    return x*(1-x)

epoch=5000
lr=0.1
input_neurons=2
hidden_neurons=3
output_neurons=1

wh=np.random.uniform(size=(input_neurons,hidden_neurons))
bh=np.random.uniform(size=(1,hidden_neurons))
wout=np.random.uniform(size=(hidden_neurons,output_neurons))
bout=np.random.uniform(size=(1,output_neurons))

for i in range(epoch):
    hinp1=np.dot(X,wh)
    hinp=hinp1+bh
    hlayer_act=sigmoid(hinp)
    outinp1=np.dot(hlayer_act,wout)
    outinp=outinp1+bout
    output=sigmoid(outinp)

    eo=y-output
    outgrad=derivatives_sigmoid(output)
    d_output=eo*outgrad
    eh=d_output.dot(wout.T)

    hiddengrad=derivatives_sigmoid(hlayer_act)
    d_hiddenlayer= eh*hiddengrad

    wout+=hlayer_act.T.dot(d_output)*lr
    wh+=X.T.dot(d_hiddenlayer)*lr

print("input:\n"+str(X))
print("Actual output:\n"+str(y))
print("Predicted op:\n", output)
'''