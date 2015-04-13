from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.transferLogs = True
config.General.requestName  = 'WZJetsTo3LNu_PU20bx25_PHYS14'

config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName    = 'skimToTreeSUSYMCtfs.py'
config.JobType.outputFiles = ['Tree_13TeV.root']
config.JobType.inputFiles  = ['Winter14_V5_DATA_UncertaintySources_AK5PFchs.txt','PHYS14_V2_MC_L3Absolute_AK4PFchs.txt','PHYS14_V2_MC_L2Relative_AK4PFchs.txt','PHYS14_V2_MC_L1FastJet_AK4PFchs.txt']

config.section_("Data")
config.Data.inputDataset    = '/WZJetsTo3LNu_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
config.Data.splitting       = 'FileBased'
config.Data.unitsPerJob     = 1
config.Data.publishDataName = 'Skim_2L_Pt17_8'
config.Data.ignoreLocality  = True

config.section_("Site")
config.Site.storageSite = 'T2_ES_IFCA'

config.section_("User")

