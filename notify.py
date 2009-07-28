import Growl

a = Growl.GrowlNotifier(applicationName="pouet", notifications=['info'], applicationIcon=Growl.Image.imageFromPath("logo.png"))
a.register()
a.notify('info', "NeuralSession", "Demarrage de firefox ...")
