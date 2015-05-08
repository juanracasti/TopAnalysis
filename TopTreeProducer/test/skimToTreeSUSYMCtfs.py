import FWCore.ParameterSet.Config as cms

process = cms.Process("Tree")

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load("RecoMET/METProducers.METSignificance_cfi")
process.load("RecoMET/METProducers.METSignificanceParams_cfi")


######### Skim Filter

# Select isolated collections
process.selectedMuons = cms.EDFilter("CandPtrSelector",
                                     src = cms.InputTag("slimmedMuons"),
                                     cut = cms.string("pt>8"))

process.selectedElectrons = cms.EDFilter("CandPtrSelector",
                                         src = cms.InputTag("slimmedElectrons"),
                                         cut = cms.string("pt>8"))

process.allLeps = cms.EDProducer("CandViewMerger",
                                 src = cms.VInputTag(cms.InputTag("selectedElectrons"),
                                                     cms.InputTag("selectedMuons")))

process.allDiLep = cms.EDProducer("CandViewShallowCloneCombiner",
                                  decay = cms.string('allLeps allLeps'),
                                  cut = cms.string('deltaR(daughter(0).eta,daughter(0).phi,daughter(1).eta,daughter(1).phi) > 0.05 && min(daughter(0).pt,daughter(1).pt) > 8 && max(daughter(0).pt,daughter(1).pt) > 17'),
                                  checkCharge = cms.bool(False))

process.countDiLeps = cms.EDFilter("CandViewCountFilter",
                                   src = cms.InputTag("allDiLep"),
                                   minNumber = cms.uint32(1))

process.preYieldFilter = cms.Sequence(process.selectedMuons+process.selectedElectrons+process.allLeps+process.allDiLep+process.countDiLeps)

process.demo = cms.EDAnalyzer('SUSYSkimToTreeTFS',
                              readGen        = cms.untracked.bool(True),
                              readLHE        = cms.untracked.bool(False),
                              trigTag        = cms.untracked.InputTag('TriggerResults'),
                              muonTag        = cms.untracked.InputTag('slimmedMuons'),
                              jetPFTag       = cms.untracked.InputTag('slimmedJets'),
                              metTag         = cms.untracked.InputTag('slimmedMETs'),
                              PVTag          = cms.untracked.InputTag('offlineSlimmedPrimaryVertices'),
                              electronTag    = cms.untracked.InputTag('slimmedElectrons'),
                              tauTag         = cms.untracked.InputTag('slimmedTaus'),
                              pfTag          = cms.untracked.InputTag('packedPFCandidates'))

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("Tree_13TeV.root"),
                                   closeFileFast = cms.untracked.bool(True))

# Skim
process.p = cms.Path(process.preYieldFilter*process.METSignificance*process.demo)
# No skim
#process.p = cms.Path(process.METSignificance*process.demo)

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring("#inputfiles#"))

process.source.fileNames = cms.untracked.vstring('file:/afs/cern.ch/user/p/piedra/work/store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/00C90EFC-3074-E411-A845-002590DB9262.root')
#process.source.fileNames = cms.untracked.vstring('root://xrootd.unl.edu//store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/00C90EFC-3074-E411-A845-002590DB9262.root')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.options = cms.untracked.PSet(reportEvery = cms.untracked.int32(10000))

# MessageLogger stuff
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

# GlobalTag stuff
process.GlobalTag.globaltag = 'GR_R_52_V7::All'

# Debug
#process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck", ignoreTotal = cms.untracked.int32(1))

