from datetime import datetime
from process import Process
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import TanhLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

apps = { "itunes" : "/Applications/iTunes.app/Contents/MacOS/iTunes",
         "things" : "/Applications/Things.app/Contents/MacOS/Things",
         "firefox" : "/Applications/Firefox.app/Contents/MacOS/firefox-bin"}

input_args = ("dayofmonth", "dayofweek", "hour", "minute")

class ProcessLearning():
    
    def __init__(self):
        self.net = buildNetwork(len(input_args), 3, len(apps), bias=True, hiddenclass=TanhLayer)
        self.ds = SupervisedDataSet(len(input_args), len(apps))
        self.trainer = BackpropTrainer(self.net, self.ds, verbose = True)
        
    def _get_apps_tuple(self, ps):
        apps_tuple = [0 for i in range(len(apps))]
        for p in ps:
            for i, app in enumerate(apps):
                if p.command == apps[app]:
                    apps_tuple[i] = 1
        return apps_tuple
        
    def train(self):
        now = datetime.now()
        self.ds.addSample((now.day, now.isoweekday(), now.hour, now.minute), self._get_apps_tuple(Process.latest()))
        self.net.reset()
        self.trainer.trainUntilConvergence()

    def test_train_net():
        self.net = buildNetwork(len(input_args), 3, len(apps), bias=True, hiddenclass=TanhLayer)

        self.ds = SupervisedDataSet(len(input_args), len(apps))

        self.ds.addSample((10, 1, 10, 6), (1,0,0)) # I start Itunes every day at 10 a.m.
        self.ds.addSample((12, 2, 10, 3), (1,0,0))
        self.ds.addSample((10, 3, 10, 4), (1,0,0))
        self.ds.addSample((7, 4, 10, 2), (1,0,0))
        self.ds.addSample((9, 7, 10, 1), (1,0,0))
        self.ds.addSample((2, 6, 10, 4), (1,0,0))
    
        self.ds.addSample((2, 1, 6, 0), (0,1,0)) # I start things every Monday
        self.ds.addSample((17, 1, 8, 52), (0,1,0))
        self.ds.addSample((21, 1, 11, 23), (0,1,0))
        self.ds.addSample((24, 1, 7, 12), (0,1,0))
    
        self.ds.addSample((6, 1, 20, 0), (0,0,1)) # I start firefox every evening around 8 p.m.
        self.ds.addSample((3, 5, 20, 1), (0,0,1))
        self.ds.addSample((30, 3, 20, 4), (0,0,1))
        self.ds.addSample((17, 2, 19, 58), (0,0,1))

        self.trainer = BackpropTrainer(self.net, self.ds, verbose = True)
        self.trainer.trainUntilConvergence()
    
if __name__ == '__main__':
    l = ProcessLearning()
    l.train()
    print l.net.activate((10, 6, 10, 6)) # What do I do every day at 10 a.m.
    print l.net.activate((4, 1, 7, 22)) # What do I do every monday
    print l.net.activate((24, 3, 20, 1)) # What do I do every evening at 8 p.m.