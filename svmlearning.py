from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import TanhLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.utilities import percentError
from pybrain.structure.modules.svmunit import SVMUnit
from pybrain.supervised.trainers.svmtrainer import SVMTrainer
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.supervised.trainers import RPropMinusTrainer
from pybrain.structure.modules import SoftmaxLayer

#neural session specific modules
from generatedata import *

input_args = ("month", "day", "hour", "minute")

def train_net():
    fnn = buildNetwork(len(input_args), 3, 2)
    ds = ClassificationDataSet(len(input_args),2,nb_classes=2)

    ds = generate_data(ds , hour_to_use_app = 10)
    
    trainer = RPropMinusTrainer( fnn, dataset= ds, verbose=True)

    trainer.train()
    trainer.trainEpochs(15)
    
    test = ClassificationDataSet(4,2)
    test.addSample((12,6,10,6),[1,0])
    test.addSample((12,1,7,2),[0,1])
    test.addSample((12,3,11,1),[0,1])
    
    fnn.activateOnDataset(test)
    
    return fnn,trainer,ds,test
    
def train_svm():
    svm = SVMUnit()
    ds = ClassificationDataSet(len(input_args),1,nb_classes=2)

    ds = generate_data(ds , hour_to_use_app = 10)
    
    trainer = SVMTrainer( svm , ds )

    trainer.train()
    
    test = ClassificationDataSet(4,1)
    test.addSample((12,6,10,6),[0])
    test.addSample((12,1,7,22),[1])
    test.addSample((12,3,20,1),[1])
    
    svm.activateOnDataset(test)
    
    return svm,trainer,ds,test
    
