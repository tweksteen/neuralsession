#-*- encoding: utf8 -*- 

from pybrain.datasets import ClassificationDataSet
        
def generate_data( hour_to_use_app = 10):
    """
        Generate sample data to verify a classification learning NN. 
    """
    dataset = ClassificationDataSet(4, 1, nb_classes=2)
    for month in xrange(1,12):  # month 12 reserved for tests
        for day in xrange(1,8):
            for hour in xrange(0,24):
                for minute in xrange(1,7):
                    if hour == hour_to_use_app :
                        c = 1
                    else :
                        c = 0
                    input = [month,day,hour,minute]
                    dataset.addSample(input, [c])
    dataset.assignClasses()
    return dataset
