import ROOT
from ROOT import * 


def main():

    f = TFile("../output/demo/data.root")
    tree = f.Get('citibike_train')
    
    
    ROOT.TMVA.Tools.Instance()
     
    fout = ROOT.TFile("TMVA.root","RECREATE")
     
    factory = ROOT.TMVA.Factory("TMVAClassification", fout, ":".join(["!V","!Silent","Color","DrawProgressBar","Transformations=I;D;P;G,D","AnalysisType=Classification"]))
    
    factory.AddVariable("TripDuration", "F")
    factory.AddVariable('StartWhichDay', 'I')
    factory.AddVariable('StartHour', 'I')
    
    factory.AddVariable('MeanTemp', 'F')
    factory.AddVariable('MeanWindSpeed', 'F')
    factory.AddVariable('MeanHumidity', 'F') 
    
    #factory.AddVariable('StartStationLat', 'F')
    #factory.AddVariable('StartStationLon', 'F')
    #factory.AddVariable('EndStationLat', 'F')
    #factory.AddVariable('EndStationLon', 'F')
    
    factory.AddSignalTree(tree)
    factory.AddBackgroundTree(tree)
     
    # apply event weight if needed
    #factory.SetSignalWeightExpression("EventWeight");
    #factory.SetBackgroundWeightExpression("EventWeight");
    
    # cuts defining the signal and background sample
    sigCut = ROOT.TCut("UserType==1")
    bgCut = ROOT.TCut("UserType==0")
     
    factory.PrepareTrainingAndTestTree(sigCut,   # signal events
                                       bgCut,    # background events
                                       ":".join([
                                            "nTrain_Signal=0",
                                            "nTest_Signal=0",
                                            "SplitMode=Random",
                                            "NormMode=NumEvents",
                                            "!V"
                                           ]))
    
    
    method = factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT",
                       ":".join([
                           "!H",
                           "!V",
                           "NTrees=850",
                           #"nEventsMin=150",
                           "MaxDepth=3",
                           "BoostType=AdaBoost",
                           "AdaBoostBeta=0.5",
                           "SeparationType=GiniIndex",
                           "nCuts=20",
                           "PruneMethod=NoPruning",
                           ]))
     
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()


if __name__ == '__main__':
    main()
