from optparse import OptionParser
import sys,os
from dqmlayouts import *

genLists = {
    'shift': ('shift_ecal_layout', 'shift_ecal_T0_layout', 'shift_ecal_relval_layout'),
    'ecal': ('ecal-layouts', 'ecal_T0_layouts'),
    'overview': ('ecal_overview_layouts'),
    'online': ('ecal-layouts', 'shift_ecal_layout', 'ecal_overview_layouts'),
    'offline': ('ecal_T0_layouts', 'shift_ecal_T0_layout', 'ecal_overview_layouts'),
    'relval': ('ecal_relval-layouts', 'ecalmc_relval-layouts', 'shift_ecal_relval_layout'),
    'all': ('shift_ecal_layout', 'shift_ecal_T0_layout', 'shift_ecal_relval_layout',
        'ecal-layouts', 'ecal_T0_layouts', 'ecal_overview_layouts',
        'ecal_relval-layouts', 'ecalmc_relval-layouts', 'shift_ecal_relval_layout'),
    'priv': ('ecalpriv-layouts', 'ecal_overview_layouts')
}

optparser = OptionParser()
optparser.add_option('-l', '--list', dest = 'list', help = 'LIST=(shift|ecal|overview|online|offline|relval|all)', metavar = 'LIST', default = 'all')
optparser.add_option('-t', '--target-dir', dest = 'targetDir', help = '', metavar = '', default = '.')

(options, args) = optparser.parse_args()

if 'CMSSW_BASE' not in os.environ:
    print "CMSSW environment not set"
    sys.exit()

if options.list not in genLists:
    optparser.print_usage()
    sys.exit()

if not options.targetDir:
    optparser.print_usage()
    sys.exit()

genList = genLists[options.list]
targetDir = options.targetDir

#### BEGIN path definitions / utility functions ####

from DQM.EcalMonitorTasks.ClusterTask_cfi import ecalClusterTask
from DQM.EcalMonitorTasks.EnergyTask_cfi import ecalEnergyTask
from DQM.EcalMonitorTasks.IntegrityTask_cfi import ecalIntegrityTask
from DQM.EcalMonitorTasks.LaserTask_cfi import ecalLaserTask
from DQM.EcalMonitorTasks.LedTask_cfi import ecalLedTask
from DQM.EcalMonitorTasks.OccupancyTask_cfi import ecalOccupancyTask
from DQM.EcalMonitorTasks.PedestalTask_cfi import ecalPedestalTask
from DQM.EcalMonitorTasks.PNDiodeTask_cfi import ecalPNDiodeTask
from DQM.EcalMonitorTasks.PresampleTask_cfi import ecalPresampleTask
from DQM.EcalMonitorTasks.RawDataTask_cfi import ecalRawDataTask
from DQM.EcalMonitorTasks.SelectiveReadoutTask_cfi import ecalSelectiveReadoutTask
from DQM.EcalMonitorTasks.TestPulseTask_cfi import ecalTestPulseTask
from DQM.EcalMonitorTasks.TimingTask_cfi import ecalTimingTask
from DQM.EcalMonitorTasks.TrigPrimTask_cfi import ecalTrigPrimTask

from DQM.EcalMonitorClient.IntegrityClient_cfi import ecalIntegrityClient
from DQM.EcalMonitorClient.LaserClient_cfi import ecalLaserClient
from DQM.EcalMonitorClient.LedClient_cfi import ecalLedClient
from DQM.EcalMonitorClient.OccupancyClient_cfi import ecalOccupancyClient
from DQM.EcalMonitorClient.PedestalClient_cfi import ecalPedestalClient
from DQM.EcalMonitorClient.PNIntegrityClient_cfi import ecalPNIntegrityClient
from DQM.EcalMonitorClient.PresampleClient_cfi import ecalPresampleClient
from DQM.EcalMonitorClient.RawDataClient_cfi import ecalRawDataClient
from DQM.EcalMonitorClient.SelectiveReadoutClient_cfi import ecalSelectiveReadoutClient
from DQM.EcalMonitorClient.SummaryClient_cfi import ecalSummaryClient
from DQM.EcalMonitorClient.TestPulseClient_cfi import ecalTestPulseClient
from DQM.EcalMonitorClient.TimingClient_cfi import ecalTimingClient
from DQM.EcalMonitorClient.TrigPrimClient_cfi import ecalTrigPrimClient
from DQM.EcalMonitorClient.CalibrationSummaryClient_cfi import ecalCalibrationSummaryClient

clusterTask = ecalClusterTask.MEs
energyTask = ecalEnergyTask.MEs
integrityTask = ecalIntegrityTask.MEs
laserTask = ecalLaserTask.MEs
ledTask = ecalLedTask.MEs
occupancyTask = ecalOccupancyTask.MEs
pedestalTask = ecalPedestalTask.MEs
pnDiodeTask = ecalPNDiodeTask.MEs
presampleTask = ecalPresampleTask.MEs
rawDataTask = ecalRawDataTask.MEs
selectiveReadoutTask = ecalSelectiveReadoutTask.MEs
testPulseTask = ecalTestPulseTask.MEs
timingTask = ecalTimingTask.MEs
trigPrimTask = ecalTrigPrimTask.MEs
integrityClient = ecalIntegrityClient.MEs
laserClient = ecalLaserClient.MEs
ledClient = ecalLedClient.MEs
occupancyClient = ecalOccupancyClient.MEs
pedestalClient = ecalPedestalClient.MEs
pnIntegrityClient = ecalPNIntegrityClient.MEs
presampleClient = ecalPresampleClient.MEs
rawDataClient = ecalRawDataClient.MEs
selectiveReadoutClient = ecalSelectiveReadoutClient.MEs
summaryClient = ecalSummaryClient.MEs
testPulseClient = ecalTestPulseClient.MEs
timingClient = ecalTimingClient.MEs
trigPrimClient = ecalTrigPrimClient.MEs
calibrationSummaryClient = ecalCalibrationSummaryClient.MEs

smNamesEE = [
    "EE-01", "EE-02", "EE-03", "EE-04", "EE-05", "EE-06", "EE-07", "EE-08", "EE-09",
    "EE+01", "EE+02", "EE+03", "EE+04", "EE+05", "EE+06", "EE+07", "EE+08", "EE+09"]

smNamesEB = [
    "EB-01", "EB-02", "EB-03", "EB-04", "EB-05", "EB-06", "EB-07", "EB-08", "EB-09",
    "EB-10", "EB-11", "EB-12", "EB-13", "EB-14", "EB-15", "EB-16", "EB-17", "EB-18",
    "EB+01", "EB+02", "EB+03", "EB+04", "EB+05", "EB+06", "EB+07", "EB+08", "EB+09",
    "EB+10", "EB+11", "EB+12", "EB+13", "EB+14", "EB+15", "EB+16", "EB+17", "EB+18"]

smMEMNamesEE = ["EE-02", "EE-03", "EE-07", "EE-08", "EE+02", "EE+03", "EE+07", "EE+08"]

laserWavelengths = ['1', '2', '3', '4']

laserNames = ['(Quantronics)', '(Green)', '(Photonics)', '(IR)']

ledWavelengths = ['1', '2']

mgpaGainsFull = ['01', '06', '12']
mgpaGains = ['12']

pnMGPAGainsFull = ['01', '16']
pnMGPAGains = ['16']

ebRep = {'subdet': 'EcalBarrel', 'prefix': 'EB', 'suffix': ''}
eeRep = {'subdet': 'EcalEndcap', 'prefix': 'EE'}
eemRep = {'subdet': 'EcalEndcap', 'prefix': 'EE', 'suffix': ' EE -'}
eepRep = {'subdet': 'EcalEndcap', 'prefix': 'EE', 'suffix': ' EE +'}

def formRep(rep, setRep):
    for key, value in setRep.items():
        if type(value) is ListType:
            rep.update({key: '%(' + key + ')s'})

def prepareRepAndME(m, rep):
    me = {}
    if type(m) is TupleType:
        rep.update(m[1])
        me = m[0]
    else:
        me = m

    for ph in findall(r'\%\(([^\)]+)\)s', me.path.value()):
        if ph not in rep:
            rep.update({ph: '%(' + ph + ')s'})

    return me
            
def single(name, *mes, **keywords) :
    rows = []
    returnSet = False
    rep = {}
    setRep = {}
    
    if 'rep' in keywords:
        setRep = keywords['rep']
        formRep(rep, setRep)
    
    for m in mes :
        me = prepareRepAndME(m, rep)
        
        rows.append([(me.path.value() % rep, me.description.value() % rep)])

    if len(setRep) > 0:
        return LayoutElemSet(name, rows, setRep)
    else:
        return LayoutElem(name, rows)

def eb(name, *mes, **keywords) :
    rows = []
    rep = {}
    setRep = {}
    
    if 'rep' in keywords:
        setRep = keywords['rep']
        formRep(rep, setRep)
    
    for m in mes:
        me = prepareRepAndME(m, rep)
        
        rep.update(ebRep)
        rows.append([(me.path.value() % rep, me.description.value() % rep)])

    if len(setRep) > 0:
        return LayoutElemSet(name, rows, setRep)
    else:
        return LayoutElem(name, rows)

def ee(name, *mes, **keywords) :
    rows = []
    rep = {}
    setRep = {}
    
    if 'rep' in keywords:
        setRep = keywords['rep']
        formRep(rep, setRep)
    
    for m in mes :
        me = prepareRepAndME(m, rep)
        
        rep.update(eeRep)
        rows.append([(me.path.value() % rep, me.description.value() % rep)])

    if len(setRep) > 0:
        return LayoutElemSet(name, rows, setRep)
    else:
        return LayoutElem(name, rows)

def ecal2P(name, *mes, **keywords) :
    rows = [list(), list()]
    rep = {}
    setRep = {}
    
    if 'rep' in keywords:
        setRep = keywords['rep']
        formRep(rep, setRep)

    for m in mes :
        me = prepareRepAndME(m, rep)
        
        rep.update(ebRep)
        rows[0].append((me.path.value() % rep, me.description.value() % rep))
        rep.update(eeRep)
        rows[1].append((me.path.value() % rep, me.description.value() % rep))

    if len(setRep) > 0:
        return LayoutElemSet(name, rows, setRep)
    else:
        return LayoutElem(name, rows)

def ecal3P(name, *mes, **keywords) :
    rep = {}    
    setRep = {}

    if 'rep' in keywords:
        setRep = keywords['rep']
        formRep(rep, setRep)

    ebrows = []
    eerows = []
    for m in mes :
        me = prepareRepAndME(m, rep)
        
        rep.update(ebRep)
        ebrows.append([(me.path.value() % rep, me.description.value() % rep)])
        cols = []
        rep.update(eemRep)
        cols.append((me.path.value() % rep, me.description.value() % rep))
        rep.update(eepRep)
        cols.append((me.path.value() % rep, me.description.value() % rep))
        eerows.append(cols)

    rows = ebrows + eerows

    if len(setRep) > 0:
        return LayoutElemSet(name, rows, setRep)
    else:
        return LayoutElem(name, rows)

def ee2P(name, *mes, **keywords) :
    rows = []
    rep = {}
    setRep = {}
    
    if 'rep' in keywords:
        setRep = keywords['rep']
        formRep(rep, setRep)

    for m in mes :
        me = prepareRepAndME(m, rep)
            
        rep.update(ebRep)
        cols = []
        rep.update(eemRep)
        cols.append((me.path.value() % rep, me.description.value() % rep))
        rep.update(eepRep)
        cols.append((me.path.value() % rep, me.description.value() % rep))
        rows.append(cols)

    if len(setRep) > 0:
        return LayoutElemSet(name, rows, setRep)
    else:
        return LayoutElem(name, rows)
    
def subdetSet_produce(subdet, mes) :
    rep = {'subdet': subdet[0], 'prefix': subdet[1]}
    tmpList = []
    for m in mes:
        me = prepareRepAndME(m, rep)

        for ph in findall(r'\%\(([^\)]+)\)s', me.path.value()):
            if ph not in rep:
                rep.update({ph: '%(' + ph + ')s'})
                        
        tmpList.append((me.path.value() % rep, me.description.value() % rep))

    if len(tmpList) == 1:
        return [[tmpList[0]]]
    elif len(tmpList) == 2:
        return [[tmpList[0]], [tmpList[1]]]
    else:
        rows = []
        cols = []
        for i in range(0, len(tmpList)):
            cols.append(tmpList[i])
            if len(cols) == 2:
                rows.append(cols)
                cols = []

    return rows

def eeSMSet(name, *mes) :
    rows = subdetSet_produce(('EcalEndcap', 'EE'), mes)
    return [LayoutElemSet(name + ' %(sm)s', rows, {'sm': smNamesEE}, addSerial = False)]

def eeSMMEMSet(name, *mes) :
    rows = subdetSet_produce(('EcalEndcap', 'EE'), mes)
    return [LayoutElemSet(name + ' %(sm)s', rows, {'sm': smMEMNamesEE}, addSerial = False)]

def ebSMSet(name, *mes) :
    rows = subdetSet_produce(('EcalBarrel', 'EB'), mes)
    return [LayoutElemSet(name + ' %(sm)s', rows, {'sm': smNamesEB}, addSerial = False)]

def smSet(name, *mes) :
    return eeSMSet(name, *mes) + ebSMSet(name, *mes)

def smMEMSet(name, *mes) :
    return eeSMMEMSet(name, *mes) + ebSMSet(name, *mes)

def subdetEtaPhi(name, me, meEta, mePhi) :
    elems = [
        LayoutElem(name + " EB", [[(me.path.value() % ebRep, me.description.value() % ebRep)], [(meEta.path.value() % ebRep, meEta.description.value() % ebRep), (mePhi.path.value() % ebRep, mePhi.description.value() % ebRep)]]),
        LayoutElem(name + " EE -", [[(me.path.value() % eemRep, me.description.value() % eemRep)], [(meEta.path.value() % eemRep, meEta.description.value() % eemRep), (mePhi.path.value() % eemRep, mePhi.description.value() % eemRep)]]),
        LayoutElem(name + " EE +", [[(me.path.value() % eepRep, me.description.value() % eepRep)], [(meEta.path.value() % eepRep, meEta.description.value() % eepRep), (mePhi.path.value() % eepRep, mePhi.description.value() % eepRep)]])
    ]

    return elems

#### END path definitions / utility functions ####

layouts = {}

#### BEGIN shift_ecal_layout / shift_ecal_T0_layout ####

layouts['shift_ecal_layout'] = LayoutDir("00 Shift/Ecal", [
    ecal3P('Summary', summaryClient.QualitySummary),
    ecal3P('FE Status', rawDataClient.QualitySummary),
    ecal3P('Integrity', integrityClient.QualitySummary),
    ecal3P('Occupancy', occupancyTask.DigiAll),
    ecal3P('Noise', presampleClient.QualitySummary),
    ecal3P('RecHit Energy', energyTask.HitMapAll),
    ecal3P('Timing', timingClient.QualitySummary),
    ecal3P('TriggerPrimitives', trigPrimClient.EmulQualitySummary),
    ecal3P('Hot Cells', occupancyClient.QualitySummary),
    ecal3P('Laser 3 (Photonics)', (laserClient.QualitySummary, {'wl': '3'})), #online
    ecal2P('Laser 3 PN', (laserClient.PNQualitySummary, {'wl': '3'})), #online
    ecal3P('Test Pulse', (testPulseClient.QualitySummary, {'gain': '12'})), #online
    ecal2P('Test Pulse PN', (testPulseClient.PNQualitySummary, {'pngain': '16'})), #online
    ecal2P('Pedestal', (pedestalClient.QualitySummary, {'gain': '12'})), #online - not used in 2012
    ecal2P('Pedestal PN', (pedestalClient.PNQualitySummary, {'pngain': '16'})), #online - not used in 2012
    ee2P('Led 1', (ledClient.QualitySummary, {'wl': '1'})), #online
    ee('Led 1 PN', (ledClient.PNQualitySummary, {'wl': '1'})) #online
])

layouts['shift_ecal_layout'].remove('Pedestal')
layouts['shift_ecal_layout'].remove('Pedestal PN')

layouts['shift_ecal_T0_layout'] = layouts['shift_ecal_layout'].clone()
layouts['shift_ecal_T0_layout'].remove("Laser 3 (Photonics)")
layouts['shift_ecal_T0_layout'].remove("Laser 3 PN")
layouts['shift_ecal_T0_layout'].remove("Test Pulse")
layouts['shift_ecal_T0_layout'].remove("Test Pulse PN")
layouts['shift_ecal_T0_layout'].remove("Pedestal")
layouts['shift_ecal_T0_layout'].remove("Pedestal PN")
layouts['shift_ecal_T0_layout'].remove("Led 1")
layouts['shift_ecal_T0_layout'].remove("Led 1 PN")

#### END shift_ecal_layout / shift_ecal_T0_layout ####

#### BEGIN ecal-layouts.py / ecal_T0_layouts.py / ecalpriv-layouts.py ####

layouts['ecal-layouts'] = LayoutDir("Ecal/Layouts", [
    ecal3P('Summary', summaryClient.QualitySummary),
    ecal3P('Occupancy Summary', occupancyTask.DigiAll),
    ecal3P('Calibration Summary', calibrationSummaryClient.QualitySummary),
    LayoutDir("Overview", [], addSerial = True),
    LayoutDir("Raw Data", [], addSerial = True),
    LayoutDir("Occupancy", [], addSerial = True),
    LayoutDir("Noise", [], addSerial = True),
    LayoutDir("Energy", [], addSerial = True),
    LayoutDir("Timing", [], addSerial = True),
    LayoutDir("Trigger Primitives", [], addSerial = True),
    LayoutDir("Selective Readout", [], addSerial = True),
    LayoutDir("Laser", [], addSerial = True), #online
    LayoutDir("Led", [], addSerial = True), #online
    LayoutDir('Test Pulse', [], addSerial = True), #online
    LayoutDir('Pedestal', [], addSerial = True), #online - not used in 2012
    LayoutDir('Trend', [], addSerial = True), #online
    LayoutDir("By SuperModule", [], addSerial = True)
])

layouts['ecal-layouts'].get('Overview').append([
    ecal3P('Summary', summaryClient.QualitySummary),
    ecal3P('FE Status', rawDataClient.QualitySummary),
    ecal3P('Integrity', integrityClient.QualitySummary),
    ecal3P('Occupancy', occupancyTask.DigiAll),
    ecal3P('Noise', presampleClient.QualitySummary),
    ecal3P('RecHit Energy', energyTask.HitMapAll),
    ecal3P('Timing', timingClient.QualitySummary),
    ecal3P('Trigger Primitives', trigPrimClient.EmulQualitySummary),
    ecal3P('Hot Cells', occupancyClient.QualitySummary),
    ecal3P('Laser %(wl)s %(lname)s', laserClient.QualitySummary, rep = {'wl': laserWavelengths, 'lname': laserNames}), #online
    ecal2P('Laser %(wl)s PN', laserClient.PNQualitySummary, rep = {'wl': laserWavelengths}), #online
    ecal3P('Test Pulse G%(gain)s', testPulseClient.QualitySummary, rep = {'gain': mgpaGains}), #online
    ecal2P('Test Pulse PN G%(pngain)s', testPulseClient.PNQualitySummary, rep = {'pngain': pnMGPAGains}), #online
    ecal3P('Pedestal G%(gain)s', pedestalClient.QualitySummary, rep = {'gain': mgpaGains}), #online - not used in 2012
    ecal3P('Pedestal PN G%(pngain)s', pedestalClient.PNQualitySummary, rep = {'pngain': pnMGPAGains}), #online - not used in 2012
    ee2P('Led %(wl)s', ledClient.QualitySummary, rep = {'wl': ledWavelengths}), #online
    ee('Led %(wl)s PN', ledClient.PNQualitySummary, rep = {'wl': ledWavelengths}), #online
    single('Error Trends', rawDataTask.TrendNSyncErrors, integrityTask.TrendNErrors) #online
])

layouts['ecal-layouts'].get("Raw Data").append([
    ecal3P('FEStatus Summary', rawDataClient.QualitySummary),
    ecal2P('Total FE Sync Errors', rawDataTask.DesyncTotal),
    ecal2P('FE Errors in this LS', rawDataTask.DesyncByLumi, rawDataTask.FEByLumi),
    ecal3P('Integrity Summary', integrityClient.QualitySummary),
    ecal2P('Total Integrity Errors', integrityTask.Total),
    ecal2P('Integrity Errors in this LS', integrityTask.ByLumi), #online
    single('Error Trends', rawDataTask.TrendNSyncErrors, integrityTask.TrendNErrors), #online
    ecal2P('Event Type', rawDataTask.EventTypePreCalib, rawDataTask.EventTypeCalib, rawDataTask.EventTypePostCalib),
    ecal2P('FED Entries', occupancyTask.DCC),
    LayoutDir('Desync Errors', [
        ecal2P('CRC', rawDataTask.CRC),
        ecal2P('DCC-GT Mismatch', rawDataTask.RunNumber, rawDataTask.Orbit),
        ecal2P('DCC-GT Mismatch', rawDataTask.BXDCC, rawDataTask.L1ADCC, rawDataTask.TriggerType),
        ecal2P('DCC-TCC Mismatch', rawDataTask.BXTCC, rawDataTask.L1ATCC),
        ecal2P('DCC-SRP Mismatch', rawDataTask.BXSRP, rawDataTask.L1ASRP),
        ecal2P('DCC-FE Mismatch', rawDataTask.BXFE, rawDataTask.L1AFE)
    ]),
    LayoutDir('By SuperModule', [
        LayoutDir('Integrity Quality', smSet('Integrity', integrityClient.Quality)),
        LayoutDir('FEStatus', smSet('FE Status Flags', rawDataTask.FEStatus))
    ])
])

layouts['ecal-layouts'].get("Occupancy").append([
    ecal3P('Hot Cells', occupancyClient.QualitySummary)
])
layouts['ecal-layouts'].get("Occupancy").append(
    subdetEtaPhi("Digi", occupancyTask.DigiAll, occupancyTask.DigiProjEta, occupancyTask.DigiProjPhi) +
    subdetEtaPhi("RecHit", occupancyTask.RecHitAll, occupancyTask.RecHitProjEta, occupancyTask.RecHitProjPhi) +
    subdetEtaPhi("RecHit (Filtered)", occupancyTask.RecHitThrAll, occupancyTask.RecHitThrProjEta, occupancyTask.RecHitThrProjPhi) +
    subdetEtaPhi("Trigger Primitive (Filtered)", occupancyTask.TPDigiThrAll, occupancyTask.TPDigiThrProjEta, occupancyTask.TPDigiThrProjPhi) +
    subdetEtaPhi("Basic Cluster", clusterTask.BCOccupancy, clusterTask.BCOccupancyProjEta, clusterTask.BCOccupancyProjPhi)
)
layouts['ecal-layouts'].get("Occupancy").append([
    ecal2P('Hit Multiplicity', occupancyTask.Digi1D, occupancyTask.RecHitThr1D),
    ecal2P('Multiplicity Trend', occupancyTask.TrendNDigi, occupancyTask.TrendNRecHitThr, occupancyTask.TrendNTPDigi), #online
    ecal2P('FED Total', occupancyTask.DigiDCC),
    ecal2P('Basic Cluster Multiplicity', clusterTask.BCNum),
    ecal3P('Super Cluster Seed', clusterTask.SCSeedOccupancy),
    ecal2P('Super Cluster Multiplicity', clusterTask.SCNum),
    ecal3P('Single Crystal Cluster', clusterTask.SingleCrystalCluster),
    ecal2P('Cluster Multiplicity Trends', clusterTask.TrendNBC, clusterTask.TrendNSC), #online
    ecal3P('Laser', laserTask.Occupancy), #online
    ee2P('Led', ledTask.Occupancy), #online
    ecal3P('Test Pulse', testPulseTask.Occupancy), #online
    ecal3P('Pedestal', pedestalTask.Occupancy), #online - not used in 2012
    ecal2P('PN Digi', pnDiodeTask.OccupancySummary), #online
    LayoutDir('SR and TT Flags', [
        ecal3P('Zero Suppression', selectiveReadoutTask.ZS1Map, selectiveReadoutTask.ZSMap),
        ecal3P('Full Readout', selectiveReadoutTask.FullReadoutMap),
        ecal3P('Forced Readout', selectiveReadoutTask.RUForcedMap),
        ecal3P('All SR Flags', selectiveReadoutTask.FlagCounterMap),
        ecal3P('TT High Interest', trigPrimTask.HighIntMap),
        ecal3P('TT Medium Interest', trigPrimTask.MedIntMap),
        ecal3P('TT Low Interest', trigPrimTask.LowIntMap)
    ]),
    LayoutDir('By SuperModule', [
        LayoutDir('Digi', smSet('Digi Occupancy', occupancyTask.Digi)),
        LayoutDir('PN Digi', smMEMSet('PN Digi Occupancy', pnDiodeTask.Occupancy)) #online
    ])
])

layouts['ecal-layouts'].get("Noise").append([
    ecal3P('Presample Quality', presampleClient.QualitySummary),
    ecal3P('RMS Map', presampleClient.RMSMapAll),
    ecal3P('Reconstructed', occupancyTask.RecHitAll, clusterTask.SingleCrystalCluster),
    ecal2P('Trend', presampleClient.TrendMean, presampleClient.TrendRMS), #online
    LayoutDir('By SuperModule', [
        LayoutDir('Quality', smSet('Quality', presampleClient.Quality)),        
        LayoutDir('Mean', smSet('Mean', presampleTask.Pedestal, presampleClient.Mean)),
        LayoutDir('RMS', smSet('RMS', presampleClient.RMSMap, presampleClient.RMS)),
        LayoutDir('PN', smMEMSet('PN Presample', pnDiodeTask.Pedestal)) #online
    ])
])

layouts['ecal-layouts'].get("Energy").append([
    ecal3P('RecHit Energy', energyTask.HitMapAll),
    ecal3P('RecHit Energy Spectrum', energyTask.HitAll)
])
layouts['ecal-layouts'].get("Energy").append(
    subdetEtaPhi("Basic Cluster Energy", clusterTask.BCEMap, clusterTask.BCEMapProjEta, clusterTask.BCEMapProjPhi) +
    subdetEtaPhi("Basic Cluster Size", clusterTask.BCSizeMap, clusterTask.BCSizeMapProjEta, clusterTask.BCSizeMapProjPhi)
)
layouts['ecal-layouts'].get("Energy").append([
    ecal2P('Basic Cluster Energy', clusterTask.BCE),
    ecal2P('Basic Cluster Size', clusterTask.BCSize),
    ecal2P('Basic Cluster Size Trend', clusterTask.TrendBCSize), #online
    ecal2P('Super Cluster Energy', clusterTask.SCE),
    ecal2P('Super Cluster Energy Low', clusterTask.SCELow),
    ecal2P('Super Cluster Seed Energy', clusterTask.SCSeedEnergy),
    ecal2P('Super Cluster R9', clusterTask.SCR9),
    ecal2P('Super Cluster Size', clusterTask.SCNBCs, clusterTask.SCNcrystals),
    ecal2P('Cluster Energy vs Seed Energy', clusterTask.SCClusterVsSeed),
    LayoutDir('By SuperModule', 
        smSet('RecHit', energyTask.HitMap, energyTask.Hit)
    )
##     LayoutDir('DiClusterMass', [
##         single('Pi0', clusterTask.Pi0),
##         single('JPsi', clusterTask.JPsi),
##         single('Z', clusterTask.Z),
##         single('High Mass', clusterTask.HighMass)
##     ])
])

layouts['ecal-layouts'].get("Timing").append([
    ecal3P('Quality Summary', timingClient.QualitySummary),
    ecal3P('Mean', timingClient.MeanAll),
    ecal3P('RMS', timingClient.RMSAll)
])
layouts['ecal-layouts'].get("Timing").append(
    subdetEtaPhi("Map", timingTask.TimeAllMap, timingClient.ProjEta, timingClient.ProjPhi)
)
layouts['ecal-layouts'].get("Timing").append([
    ecal2P("Forward-Backward", timingClient.FwdBkwdDiff, timingClient.FwdvBkwd),
    ecal3P('Distribution', timingTask.TimeAll),
    ecal3P('Vs Amptlitude', timingTask.TimeAmpAll),
    LayoutDir('By SuperModule', [
        LayoutDir('Quality', smSet('Quality', timingClient.Quality)),
        LayoutDir('Distribution', smSet('Distribution', timingTask.Time1D)),
        LayoutDir('Mean', smSet('Mean', timingTask.TimeMap, timingClient.MeanSM)),
        LayoutDir('RMS', smSet('RMS', timingClient.RMSMap)),
        LayoutDir('Vs Amplitude', smSet('Time vs Amplitude', timingTask.TimeAmp)),
        LayoutDir('Laser', smSet('Photonics Laser', (laserTask.Timing, {'wl': '3'}))), #online
        LayoutDir('Led', eeSMSet('Led 1', (ledTask.Timing, {'wl': '1'}))) #online
    ])
])

layouts['ecal-layouts'].get("Trigger Primitives").append([
    ecal3P('Emulation Quality', trigPrimClient.EmulQualitySummary),
    ecal3P('Occupancy (Filtered)', occupancyTask.TPDigiThrAll),
    ecal3P('Et Spectrum', trigPrimTask.EtReal),
    ecal3P('Emulation Et Spectrum', trigPrimTask.EtMaxEmul),
    ecal3P('Et Map', trigPrimTask.EtSummary),
    ecal3P('Timing', trigPrimClient.TimingSummary),
    ecal3P('Non Single Timing', trigPrimClient.NonSingleSummary),
    ecal3P("Occupancy vs BX", trigPrimTask.OccVsBx),
    ecal3P("Et vs BX", trigPrimTask.EtVsBx),
    ecal3P('Emululation Timing', trigPrimTask.EmulMaxIndex),
    LayoutDir('By SuperModule', [
        LayoutDir('EmulMatching', smSet('Match', trigPrimTask.MatchedIndex)),
        LayoutDir('Et', smSet('TP Et', trigPrimTask.EtRealMap))
    ])
])

layouts['ecal-layouts'].get("Selective Readout").append([
    ecal2P('DCC Data Size', selectiveReadoutTask.DCCSize),
    ecal2P('DCC Data Size', selectiveReadoutTask.DCCSizeProf),
    ecal3P('DCC Data Size', selectiveReadoutTask.EventSize),
    ecal3P('Tower Data Size', selectiveReadoutTask.TowerSize),
    ecal3P('Payload High Interest', selectiveReadoutTask.HighIntPayload),
    ecal3P('Payload Low Interest', selectiveReadoutTask.LowIntPayload),
    ecal3P("ZS Filter Output (High Int.)", selectiveReadoutTask.HighIntOutput),
    ecal3P("ZS Filter Output (Low Int.)", selectiveReadoutTask.LowIntOutput),
    ecal3P('High Interest Rate', selectiveReadoutClient.HighInterest),
    ecal3P('Medium Interest Rate', selectiveReadoutClient.MedInterest),
    ecal3P('Low Interest Rate', selectiveReadoutClient.LowInterest),
    ecal3P('TT Flags', trigPrimTask.TTFlags),
    ecal3P('Full Readout Flags', selectiveReadoutClient.FR),
    ecal3P('Zero Suppression Flags', selectiveReadoutClient.ZS1),
    ecal3P('Forced Readout Flags', selectiveReadoutClient.RUForced),
    ecal3P('Full Readout Flag Dropped', selectiveReadoutClient.FRDropped),
    ecal3P('ZS Flag Readout', selectiveReadoutClient.ZSReadout)
])

layouts['ecal-layouts'].get("Laser").append([
    ecal3P("Quality Summary L%(wl)s %(lname)s", laserClient.QualitySummary, rep = {'wl': laserWavelengths, 'lname': laserNames}),
    ecal3P('Amplitude L%(wl)s %(lname)s', laserTask.AmplitudeSummary, rep = {'wl': laserWavelengths, 'lname': laserNames}),
    ecal2P('Amplitude RMS L%(wl)s %(lname)s', laserClient.AmplitudeRMS, rep = {'wl': laserWavelengths, 'lname': laserNames}),
    ecal3P('Occupancy', laserTask.Occupancy),
    ecal2P('Signal Rate L%(wl)s %(lname)s', laserTask.SignalRate, rep = {'wl': laserWavelengths, 'lname': laserNames}),
    ecal2P('Timing Spread L%(wl)s %(lname)s', laserClient.TimingRMSMap, rep = {'wl': laserWavelengths, 'lname': laserNames}),
    ecal2P('PN Quality Summary L%(wl)s %(lname)s', laserClient.PNQualitySummary, rep = {'wl': laserWavelengths, 'lname': laserNames}),
    LayoutDirSet('Laser%(wl)s %(lname)s', [
        LayoutDir('Quality', smSet('Quality', laserClient.Quality)),
        LayoutDir('Amplitude', smSet('Amplitude', laserTask.Amplitude, laserClient.AmplitudeMean)),
        LayoutDir('Timing', smSet('Timing', laserTask.Timing, laserClient.TimingMean, laserClient.TimingRMS)),
        LayoutDir('APD Over PN', smSet('APD Over PN', laserTask.AOverP)),
        LayoutDir('Shape', smSet('Shape', laserTask.Shape)),
        LayoutDir('PN Amplitude', smMEMSet('Amplitude', laserTask.PNAmplitude))
    ], {'wl': laserWavelengths, 'lname': laserNames})
])

layouts['ecal-layouts'].get("Led").append([
    ee2P("Quality Summary L%(wl)s", ledClient.QualitySummary, rep = {'wl': ledWavelengths}),
    ee2P('Amplitude L%(wl)s', ledTask.AmplitudeSummary, rep = {'wl': ledWavelengths}),    
    single('Amplitude RMS L%(wl)s', ledClient.AmplitudeRMS, rep = {'wl': ledWavelengths}),
    ee2P('Occupancy', ledTask.Occupancy),
    single('Signal Rate L%(wl)s', ledTask.SignalRate, rep = {'wl': ledWavelengths}),
    single('Timing Spread L%(wl)s', ledClient.TimingRMSMap, rep = {'wl': ledWavelengths}),
    single('PN Quality Summary L%(wl)s', ledClient.PNQualitySummary, rep = {'wl': ledWavelengths}),
    LayoutDirSet('Led%(wl)s', [
        LayoutDir('Quality', eeSMSet('Quality', ledClient.Quality)),
        LayoutDir('Amplitude', eeSMSet('Amplitude', ledTask.Amplitude, ledClient.AmplitudeMean)),
        LayoutDir('Timing',  eeSMSet('Timing', ledTask.Timing, ledClient.TimingMean)),
        LayoutDir('APD Over PN', eeSMSet('APD Over PN', ledTask.AOverP)),
        LayoutDir('Shape', eeSMSet('Shape', ledTask.Shape)),
        LayoutDir('PN Amplitude', eeSMMEMSet('Amplitude', ledTask.PNAmplitude))
    ], {'wl': ledWavelengths})
])

layouts['ecal-layouts'].get("Test Pulse").append([
    ecal3P('Quality Summary G%(gain)s', testPulseClient.QualitySummary, rep = {'gain': mgpaGains}),
    ecal3P('Occupancy', testPulseTask.Occupancy),
    ecal2P('PN Quality Summary G%(pngain)s', testPulseClient.PNQualitySummary, rep = {'pngain': pnMGPAGains}),
    LayoutDirSet('Gain%(gain)s', [
        LayoutDir('Quality', smSet('Quality', testPulseClient.Quality)),
        LayoutDir('Amplitude', smSet('Amplitude', testPulseTask.Amplitude)),
        LayoutDir('Amplitude RMS', smSet('RMS', testPulseClient.AmplitudeRMS)),
        LayoutDir('Shape', smSet('Shape', testPulseTask.Shape))
    ], {'gain': mgpaGains}),
    LayoutDirSet('PNGain%(pngain)s',
        smMEMSet('Amplitude', testPulseTask.PNAmplitude),
        {'pngain': pnMGPAGains})
])

layouts['ecal-layouts'].get('Pedestal').append([
    ecal3P('Quality Summary G%(gain)s', pedestalClient.QualitySummary, rep = {'gain': mgpaGains}),
    ecal3P('Occupancy', pedestalTask.Occupancy),
    ecal2P('PN Quality Summary G%(pngain)s', pedestalClient.PNQualitySummary, rep = {'pngain': pnMGPAGains}),
    LayoutDirSet('Gain%(gain)s', [
        LayoutDir('Quality', smSet('Quality', pedestalClient.Quality)),
        LayoutDir('Mean', smSet('Mean', pedestalTask.Pedestal, pedestalClient.Mean)),
        LayoutDir('RMS', smSet('RMS', pedestalClient.RMS))
    ], {'gain': mgpaGains}),
    LayoutDirSet('PNGain%(pngain)s', [
        LayoutDir('Mean', smMEMSet('Mean', pedestalTask.PNPedestal)),
        LayoutDir('RMS', smMEMSet('RMS', pedestalClient.PNRMS))
    ], {'pngain': pnMGPAGains})
])

layouts['ecal-layouts'].get("Trend").append([
    single('Errors', rawDataTask.TrendNSyncErrors, integrityTask.TrendNErrors),
    ecal2P('Number of Digis', occupancyTask.TrendNDigi),
    ecal2P('Number of RecHits', occupancyTask.TrendNRecHitThr),
    ecal2P('Number of TPs', occupancyTask.TrendNTPDigi),
    ecal2P('Presample Mean', presampleClient.TrendMean),
    ecal2P('Presample RMS', presampleClient.TrendRMS),
    ecal2P('Basic Clusters', clusterTask.TrendNBC, clusterTask.TrendBCSize),
    ecal2P('Super Clusters', clusterTask.TrendNSC, clusterTask.TrendSCSize)
])

ebSMRep = {'sm': smNamesEB}
ebSMRep.update(ebRep)
ebSMSet = LayoutDirSet("%(sm)s", [
    single("Integrity", integrityClient.Quality),
    single("FEStatus", rawDataTask.FEStatus),
    single("Digi Occupancy", occupancyTask.Digi),
    single("Presample Quality", presampleClient.Quality),
    single("Presample Mean", presampleTask.Pedestal, presampleClient.Mean),
    single("Presample RMS", presampleClient.RMS),
    single("Energy", energyTask.HitMap, energyTask.Hit),
    single("Timing Quality", timingClient.Quality),
    single("Timing All", timingTask.Time1D),
    single("Timing Mean", timingTask.TimeMap, timingClient.MeanSM),
    single("Timing RMS", timingClient.RMSMap),
    single("Timing Vs Amplitude", timingTask.TimeAmp),
    single("Trigger Primitives", trigPrimTask.EtRealMap, trigPrimTask.MatchedIndex),
    LayoutDir('Laser', [
        single('Quality L%(wl)s %(lname)s', laserClient.Quality, rep = {'wl': laserWavelengths, 'lname': laserNames}),
        single('Amplitude L%(wl)s %(lname)s', laserTask.Amplitude, laserClient.AmplitudeMean, rep = {'wl': laserWavelengths, 'lname': laserNames}),
        single('Timing L%(wl)s %(lname)s', laserTask.Timing, laserClient.TimingMean, laserClient.TimingRMS, rep = {'wl': laserWavelengths, 'lname': laserNames}),
        single('APD Over PN L%(wl)s %(lname)s', laserTask.AOverP, rep = {'wl': laserWavelengths, 'lname': laserNames}),
        single('Shape L%(wl)s %(lname)s', laserTask.Shape, rep = {'wl': laserWavelengths, 'lname': laserNames})
    ]), #online
    LayoutDir('Test Pulse', [
        single('Quality G%(gain)s', testPulseClient.Quality, rep = {'gain': mgpaGains}),
        single('Amplitude G%(gain)s', testPulseTask.Amplitude, testPulseClient.AmplitudeRMS, rep = {'gain': mgpaGains}),
        single('Shape G%(gain)s', testPulseTask.Shape, rep = {'gain': mgpaGains})
    ]), #online
    LayoutDir('Pedestal', [
        single('Quality G%(gain)s', pedestalClient.Quality, rep = {'gain': mgpaGains}),
        single('Mean G%(gain)s', pedestalTask.Pedestal, pedestalClient.Mean, rep = {'gain': mgpaGains}),
        single('RMS G%(gain)s', pedestalClient.RMS, rep = {'gain': mgpaGains})
    ]) #online
], ebSMRep)
eeSMRep = {'sm': smNamesEE}
eeSMRep.update(eeRep)
eeSMSet = ebSMSet.clone()
eeSMSet.setReplacement(eeSMRep)
eeSMSet.append(
    LayoutDir('Led', [
        single('Quality L%(wl)s', ledClient.Quality, rep = {'wl': ledWavelengths}),
        single('Amplitude L%(wl)s', ledTask.Amplitude, ledClient.AmplitudeMean, rep = {'wl': ledWavelengths}),
        single('Timing L%(wl)s', ledTask.Timing, ledClient.TimingMean, rep = {'wl': ledWavelengths}),
        single('APD Over PN L%(wl)s', ledTask.AOverP, rep = {'wl': ledWavelengths}),
        single('Shape L%(wl)s', ledTask.Shape, rep = {'wl': ledWavelengths})
    ]) #online
)
ebSMMEMRep = {'sm': smNamesEB}
ebSMMEMRep.update(ebRep)
ebSMMEMSet = LayoutDirSet("%(sm)s", [
    single('PN Digi Occupancy', pnDiodeTask.Occupancy), #online
    single('PN Presample', pnDiodeTask.Pedestal), #online
    LayoutDir('Laser', [single('PN Amplitude L%(wl)s', laserTask.PNAmplitude, rep = {'wl': laserWavelengths})]), #online
    LayoutDir('Test Pulse', [single('PN Amplitude G%(pngain)s', testPulseTask.PNAmplitude, rep = {'pngain': pnMGPAGains})]), #online
    LayoutDir('Pedestal', [single('PN Pedestal G%(pngain)s', pedestalTask.PNPedestal, pedestalClient.PNRMS, rep = {'pngain': pnMGPAGains})]) #online
], ebSMMEMRep)
eeSMMEMRep = {'sm': smMEMNamesEE}
eeSMMEMRep.update(eeRep)
eeSMMEMSet = ebSMMEMSet.clone()
eeSMMEMSet.setReplacement(eeSMMEMRep)
eeSMMEMSet.append(
    LayoutDir('Led', [
        single('PN Amplitude L%(wl)s', ledTask.PNAmplitude, rep = {'wl': ledWavelengths})
    ])
)

layouts['ecal-layouts'].get("By SuperModule").append([
    ebSMSet,
    eeSMSet,
    ebSMMEMSet,
    eeSMMEMSet
])

layouts['ecalpriv-layouts'] = layouts['ecal-layouts'].clone()
layouts['ecalpriv-layouts'].get('Test Pulse/Quality Summary G%(gain)s').setReplacement({'gain': mgpaGainsFull})
layouts['ecalpriv-layouts'].get('Test Pulse/PN Quality Summary G%(pngain)s').setReplacement({'pngain': pnMGPAGainsFull})
layouts['ecalpriv-layouts'].get('Test Pulse/Gain%(gain)s').setReplacement({'gain': mgpaGainsFull})
layouts['ecalpriv-layouts'].get('Test Pulse/PNGain%(pngain)s').setReplacement({'pngain': pnMGPAGainsFull})
layouts['ecalpriv-layouts'].get('Pedestal/Quality Summary G%(gain)s').setReplacement({'gain': mgpaGainsFull})
layouts['ecalpriv-layouts'].get('Pedestal/PN Quality Summary G%(pngain)s').setReplacement({'pngain': pnMGPAGainsFull})
layouts['ecalpriv-layouts'].get('Pedestal/Gain%(gain)s').setReplacement({'gain': mgpaGainsFull})
layouts['ecalpriv-layouts'].get('Pedestal/PNGain%(pngain)s').setReplacement({'pngain': pnMGPAGainsFull})
layouts['ecalpriv-layouts'].remove('By SuperModule')
ebSMSet.get("Test Pulse/Quality G%(gain)s").setReplacement({'gain': mgpaGainsFull})
ebSMSet.get("Test Pulse/Amplitude G%(gain)s").setReplacement({'gain': mgpaGainsFull})
ebSMSet.get("Test Pulse/Shape G%(gain)s").setReplacement({'gain': mgpaGainsFull})
ebSMSet.get("Pedestal/Quality G%(gain)s").setReplacement({'gain': mgpaGainsFull})
ebSMSet.get("Pedestal/Mean G%(gain)s").setReplacement({'gain': mgpaGainsFull})
ebSMSet.get("Pedestal/RMS G%(gain)s").setReplacement({'gain': mgpaGainsFull})
ebSMMEMSet.get("Test Pulse/PN Amplitude G%(pngain)s").setReplacement({'pngain': pnMGPAGainsFull})
ebSMMEMSet.get("Pedestal/PN Pedestal G%(pngain)s").setReplacement({'pngain': pnMGPAGainsFull})
eeSMSet.get("Test Pulse/Quality G%(gain)s").setReplacement({'gain': mgpaGainsFull})
eeSMSet.get("Test Pulse/Amplitude G%(gain)s").setReplacement({'gain': mgpaGainsFull})
eeSMSet.get("Test Pulse/Shape G%(gain)s").setReplacement({'gain': mgpaGainsFull})
eeSMSet.get("Pedestal/Quality G%(gain)s").setReplacement({'gain': mgpaGainsFull})
eeSMSet.get("Pedestal/Mean G%(gain)s").setReplacement({'gain': mgpaGainsFull})
eeSMSet.get("Pedestal/RMS G%(gain)s").setReplacement({'gain': mgpaGainsFull})
eeSMMEMSet.get("Test Pulse/PN Amplitude G%(pngain)s").setReplacement({'pngain': pnMGPAGainsFull})
eeSMMEMSet.get("Pedestal/PN Pedestal G%(pngain)s").setReplacement({'pngain': pnMGPAGainsFull})
layouts['ecalpriv-layouts'].append(
    LayoutDir("By SuperModule", [
        ebSMSet,
        eeSMSet,
        ebSMMEMSet,
        eeSMMEMSet
    ])
)

#removing pedestal from central DQM layouts (2012)
layouts['ecal-layouts'].remove('Pedestal')
layouts['ecal-layouts'].remove('Overview/Pedestal G%(gain)s')
layouts['ecal-layouts'].remove('Overview/Pedestal PN G%(pngain)s')
layouts['ecal-layouts'].remove('Occupancy/Pedestal')
layouts['ecal-layouts'].remove('By SuperModule/Pedestal')

layouts['ecal_T0_layouts'] = layouts['ecal-layouts'].clone()
layouts['ecal_T0_layouts'].remove('Calibration Summary')
layouts['ecal_T0_layouts'].remove('Selective Readout')
layouts['ecal_T0_layouts'].remove('Laser')
layouts['ecal_T0_layouts'].remove('Led')
layouts['ecal_T0_layouts'].remove('Test Pulse')
layouts['ecal_T0_layouts'].remove('Pedestal')
layouts['ecal_T0_layouts'].remove('Trend')
layouts['ecal_T0_layouts'].remove('Overview/Laser %(wl)s %(lname)s')
layouts['ecal_T0_layouts'].remove('Overview/Laser %(wl)s PN')
layouts['ecal_T0_layouts'].remove('Overview/Test Pulse G%(gain)s')
layouts['ecal_T0_layouts'].remove('Overview/Test Pulse PN G%(pngain)s')
layouts['ecal_T0_layouts'].remove('Overview/Pedestal G%(gain)s')
layouts['ecal_T0_layouts'].remove('Overview/Pedestal PN G%(pngain)s')
layouts['ecal_T0_layouts'].remove('Overview/Led %(wl)s')
layouts['ecal_T0_layouts'].remove('Overview/Led %(wl)s PN')
layouts['ecal_T0_layouts'].remove('Overview/Error Trends')
layouts['ecal_T0_layouts'].remove('Raw Data/Integrity Errors in this LS')
layouts['ecal_T0_layouts'].remove('Raw Data/Error Trends')
layouts['ecal_T0_layouts'].remove('Occupancy/Cluster Multiplicity Trends')
layouts['ecal_T0_layouts'].remove('Occupancy/Laser')
layouts['ecal_T0_layouts'].remove('Occupancy/Led')
layouts['ecal_T0_layouts'].remove('Occupancy/Test Pulse')
layouts['ecal_T0_layouts'].remove('Occupancy/Pedestal')
layouts['ecal_T0_layouts'].remove('Occupancy/PN Digi')
layouts['ecal_T0_layouts'].remove('Occupancy/By SuperModule/PN Digi')
layouts['ecal_T0_layouts'].remove('Noise/Trend')
layouts['ecal_T0_layouts'].remove('Noise/By SuperModule/PN')
layouts['ecal_T0_layouts'].remove('Energy/Basic Cluster Size Trend')
layouts['ecal_T0_layouts'].remove('Timing/Laser')
layouts['ecal_T0_layouts'].remove('Timing/Led')
layouts['ecal_T0_layouts'].remove('By SuperModule/%(sm)s/Laser')
layouts['ecal_T0_layouts'].remove('By SuperModule/%(sm)s/Test Pulse')
layouts['ecal_T0_layouts'].remove('By SuperModule/%(sm)s/Pedestal')
layouts['ecal_T0_layouts'].remove('By SuperModule/%(sm)s/Led')

#### END ecal-layouts.py / ecal_T0_layouts.py / ecalpriv-layouts.py ####

#### BEGIN ecal_overview_layouts ####

layouts['ecal_overview_layouts'] = LayoutDir("Collisions/EcalFeedBack", [
    ecal3P("Single Event Timing", timingTask.TimeAll),
    eb("Forward-Backward EB", timingClient.FwdBkwdDiff, timingClient.FwdvBkwd),
    ee("Forward-Backward EE", timingClient.FwdBkwdDiff, timingClient.FwdvBkwd),
])
layouts['ecal_overview_layouts'].append(
    subdetEtaPhi("Timing Map", timingTask.TimeAllMap, timingClient.ProjEta, timingClient.ProjPhi)
)
layouts['ecal_overview_layouts'].append(
    LayoutElem("Timing ES", [
        [["EcalPreshower/ESTimingTask/ES Timing Z 1 P 1"], ["EcalPreshower/ESTimingTask/ES Timing Z -1 P 1"]],
        [["EcalPreshower/ESTimingTask/ES Timing Z 1 P 2"], ["EcalPreshower/ESTimingTask/ES Timing Z -1 P 2"]]
    ])
)
layouts['ecal_overview_layouts'].append(
    subdetEtaPhi("Occupancy", occupancyTask.RecHitThrAll, occupancyTask.RecHitThrProjEta, occupancyTask.RecHitThrProjPhi)
)
layouts['ecal_overview_layouts'].append([
    LayoutElem("Occupancy ES", [
        [["EcalPreshower/ESOccupancyTask/ES Occupancy with selected hits Z 1 P 1"], ["EcalPreshower/ESOccupancyTask/ES Occupancy with selected hits Z -1 P 1"]],
        [["EcalPreshower/ESOccupancyTask/ES Occupancy with selected hits Z 1 P 2"], ["EcalPreshower/ESOccupancyTask/ES Occupancy with selected hits Z -1 P 2"]]
    ]),
    eb("RecHit Energy EB", energyTask.HitMapAll, energyTask.HitAll),
    ee2P("RecHit Energy EE", energyTask.HitMapAll, energyTask.HitMapAll),
    LayoutElem("RecHit Energy ES", [
        [["EcalPreshower/ESOccupancyTask/ES Energy Density with selected hits Z 1 P 1"], ["EcalPreshower/ESOccupancyTask/ES Energy Density with selected hits Z -1 P 1"]],
        [["EcalPreshower/ESOccupancyTask/ES Energy Density with selected hits Z 1 P 2"], ["EcalPreshower/ESOccupancyTask/ES Energy Density with selected hits Z -1 P 2"]]
    ])
])

#### END ecal_overview_layouts ####

#### BEGIN ecal_relval-layouts / ecalmc_relval-layouts ####

layouts['ecal_relval-layouts'] = LayoutDir("DataLayouts/Ecal", [
    ecal2P("Number of Ecal RecHits", occupancyTask.RecHitThr1D),
    LayoutElem("Number of ES RecHits", [
        [["EcalPreshower/ESOccupancyTask/ES Num of RecHits Z 1 P 1"], ["EcalPreshower/ESOccupancyTask/ES Num of RecHits Z -1 P 1"]],
        [["EcalPreshower/ESOccupancyTask/ES Num of RecHits Z 1 P 2"], ["EcalPreshower/ESOccupancyTask/ES Num of RecHits Z -1 P 2"]]
    ])
] + subdetEtaPhi("Ecal RecHit Occupancy", occupancyTask.RecHitThrAll, occupancyTask.RecHitThrProjEta, occupancyTask.RecHitThrProjPhi) + [
    ecal3P("Ecal Spectrum", energyTask.HitAll),
    LayoutElem("ES Spectrum", [
        [["EcalPreshower/ESOccupancyTask/ES RecHit Energy Z 1 P 1"], ["EcalPreshower/ESOccupancyTask/ES RecHit Energy Z -1 P 1"]],
        [["EcalPreshower/ESOccupancyTask/ES RecHit Energy Z 1 P 2"], ["EcalPreshower/ESOccupancyTask/ES RecHit Energy Z -1 P 2"]]
    ]),
    LayoutElem("Ecal Max Energy", [
        [["EcalBarrel/EBRecoSummary/recHits_EB_energyMax"]],
        [["EcalEndcap/EERecoSummary/recHits_EEP_energyMax"], ["EcalEndcap/EERecoSummary/recHits_EEM_energyMax"]]
    ]),
    LayoutElem("ES Max Energy", [
        [["EcalPreshower/ESRecoSummary/recHits_ES_energyMax"]]
    ]),
    LayoutElem("Ecal Timing", [
        [["EcalBarrel/EBRecoSummary/recHits_EB_time"]],
        [["EcalEndcap/EERecoSummary/recHits_EEP_time"], ["EcalEndcap/EERecoSummary/recHits_EEM_time"]]
    ]),
    LayoutElem("ES Timing", [
        [["EcalPreshower/ESRecoSummary/recHits_ES_time"]]
    ]),
    LayoutElem("Ecal Chi2", [
        [["EcalBarrel/EBRecoSummary/recHits_EB_Chi2"]],
        [["EcalEndcap/EERecoSummary/recHits_EEP_Chi2"], ["EcalEndcap/EERecoSummary/recHits_EEM_Chi2"]]
    ]),
    LayoutElem("EB SwissCross", [
        [["EcalBarrel/EBRecoSummary/recHits_EB_E1oE4"]]
    ]),
    LayoutElem("RecHit Flags", [
        [["EcalBarrel/EBRecoSummary/recHits_EB_recoFlag"]],
        [["EcalEndcap/EERecoSummary/recHits_EE_recoFlag"]]
    ]),
    LayoutElem("ReducedRecHit Flags", [
        [["EcalBarrel/EBRecoSummary/redRecHits_EB_recoFlag"]],
        [["EcalEndcap/EERecoSummary/redRecHits_EE_recoFlag"]]
    ]),
    LayoutElem("Basic Cluster RecHit Flags", [
        [["EcalBarrel/EBRecoSummary/basicClusters_recHits_EB_recoFlag"]],
        [["EcalEndcap/EERecoSummary/basicClusters_recHits_EE_recoFlag"]]
    ]),
    ecal2P("Number of Basic Clusters", clusterTask.BCNum),
    ecal2P("Number of Super Clusters", clusterTask.SCNum),
    ecal2P("Super Cluster Energy", clusterTask.SCE),
    LayoutElem("Super Cluster Occupancy Eta", [
        [["EcalBarrel/EBRecoSummary/superClusters_EB_eta"]],
        [["EcalEndcap/EERecoSummary/superClusters_EE_eta"]]
    ]),
    LayoutElem("Super Cluster Occupancy Phi", [
        [["EcalBarrel/EBRecoSummary/superClusters_EB_phi"]],
        [["EcalEndcap/EERecoSummary/superClusters_EE_phi"]]
    ]),
    ecal2P("Super Cluster Size (Crystals)", clusterTask.SCNcrystals),
    ecal2P("Super Cluster Size (Basic Clusters)", clusterTask.SCNBCs),
    LayoutElem("Super Cluster Seed SwissCross", [
        [["EcalBarrel/EBRecoSummary/superClusters_EB_E1oE4"]]
    ]),
    LayoutElem("Preshower Planes Energy", [
        [["EcalPreshower/ESRecoSummary/esClusters_energy_plane1"], ["EcalPreshower/ESRecoSummary/esClusters_energy_plane2"]],
        [["EcalPreshower/ESRecoSummary/esClusters_energy_ratio"]]
    ])
])

layouts['ecalmc_relval-layouts'] = layouts['ecal_relval-layouts'].clone('MCLayouts/Ecal')

#### END ecal_relval-layouts / ecalmc_relval-layouts ####

#### BEGIN shift_ecal_relval_layout ####

layouts['shift_ecal_relval_layout'] = LayoutDir("00 Shift/Ecal", [
    ecal3P("RecHit Spectra", energyTask.HitAll),
    ecal2P("Number of RecHits", occupancyTask.RecHitThr1D),
    ecal3P("Mean Timing", timingClient.MeanAll)
])

#### END shift_ecal_relval_layout ####

for lo in genList:
    filename = lo
    if lo == 'ecalpriv-layouts' :
        filename = 'ecal-layouts'

    output = file(targetDir + '/' + filename + '.py', 'w')
    layouts[lo].expand(output)
    output.close()


