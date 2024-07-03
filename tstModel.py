from model.model import Model

mymodel = Model()

mymodel.buildGraph(120)
mymodel.printGraphDetails()
v0 = mymodel.getNodes()[1]
mymodel.getComponenteConnessa(v0)