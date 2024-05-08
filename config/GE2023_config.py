from analysis_tools import ObjectCollection, Category, Process, Dataset, Feature, Systematic
from analysis_tools.utils import DotDict
from analysis_tools.utils import join_root_selection as jrs
from plotting_tools import Label
from collections import OrderedDict
import ROOT
import math
from cmt.config.base_config import Config as base_config

class Config(base_config):
    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)

        # Define the lumi dict
        preBPix = {
            "C" : 17650*0.878,
        }
        postBPix = {
            "D" : 9451*0.962,
        }
        lumi_pb = {
            "preBPix"  : preBPix,
            "postBPix" : postBPix,
        }

        #### PATCH FOR NORMALIZATION ISSUES:  ####
        #### commented some lines and created ####
        #### manually lumi_fb dict unscaled   ####
#        if lumi_pb and not type(lumi_pb) == dict:
#            self.lumi_fb = lumi_pb / 1000.
#            self.lumi_pb = lumi_pb 
#
#        else:
#            lumi_fb = {}
#            for period, period_dict in lumi_pb.items():
#                period_dict_fb = {}
#                for era, lum in period_dict.items():
#                    period_dict_fb[era] = lum / 1000
#                lumi_fb[period] = period_dict_fb
#            self.lumi_fb = lumi_fb
#            self.lumi_pb = lumi_pb

        preBPix_fb = {
            "C" : 17.650,
        }
        postBPix_fb = {
            "D" : 9.451,
        }
        lumi_fb = {
            "preBPix"  : preBPix_fb,
            "postBPix" : postBPix_fb,
        }
        self.lumi_fb = lumi_fb
        self.lumi_pb = lumi_pb
        ############################################

        self.x = kwargs

        self.channels = self.add_channels()
        self.regions = self.add_regions()
        self.categories = self.add_categories()
        self.processes, self.process_group_names, _ = self.add_processes()
        self.datasets = self.add_datasets()
        if 'xrd_redir' in kwargs:
            self.prefix_datasets(self.datasets, kwargs['xrd_redir'])
        self.features = self.add_features()
        self.versions = self.add_versions()
        self.weights = self.add_weights()
        self.systematics = self.add_systematics()
        self.default_module_files = self.add_default_module_files()

        self.upper_left_text = "Private work"
        self.label_size = 1.2

    def join_selection_channels(self, selection):
        return jrs([jrs(jrs(selection[ch.name], op="and"), ch.selection, op="and")
            for ch in self.channels], op="or")

    def combine_selections_per_channel(self, selection1, selection2):
        selection = DotDict()
        for channel in selection1:
            selection[channel] = jrs(selection1[channel], selection2[channel], op="or")
        return selection

    def get_aux(self, name, default=None):
        return self.x.get(name, default)

    def add_regions(self):
        pass

    def add_channels(self):
        pass

    def add_categories(self):

        categories = [
            Category("base", "base category", selection = ""),
            Category("preselection_2023", "GEMethod Preselection for Run3 2023", selection = "nMuon > 1"),
        ]
        return ObjectCollection(categories)

    def add_processes(self):

        processes = [
            ## Drell-Yan ##
            Process("DrellYan", Label("DY"), color=ROOT.kAzure+1),
            Process("DY_preBPix", Label("DY"), color=ROOT.kAzure+1, parent_process="DrellYan"),
            Process("DY_postBPix", Label("DY"), color=ROOT.kAzure+1, parent_process="DrellYan"),
            # Z mumu #
            Process("Zmumu_onshell", Label("Z/#gamma #rightarrow #mu#mu M_{#mu#mu} 50to120"), color=ROOT.kAzure+10, isZonshell=True, parent_process="DY_preBPix"),
            Process("Zmumu", Label("off-shell Z/#gamma #rightarrow #mu#mu"), color=ROOT.kAzure+1, parent_process="DY_preBPix"),
            Process("Zmumu2", Label("Z/#gamma #rightarrow #mu#mu M_{#mu#mu} 120to200"), color=(255, 140, 0), parent_process="Zmumu"),
            Process("Zmumu3", Label("Z/#gamma #rightarrow #mu#mu M_{#mu#mu} 200to400"), color=(232, 17, 35), parent_process="Zmumu"),
            Process("Zmumu4", Label("Z/#gamma #rightarrow #mu#mu M_{#mu#mu} 400to800"), color=(236, 0, 140), parent_process="Zmumu"),
            Process("Zmumu5", Label("Z/#gamma #rightarrow #mu#mu M_{#mu#mu} 800to1500"), color=(104, 33, 122), parent_process="Zmumu"),
            Process("Zmumu6", Label("Z/#gamma #rightarrow #mu#mu M_{#mu#mu} 1500to2500"), color=(0, 24, 143), parent_process="Zmumu"),
            Process("Zmumu7", Label("Z/#gamma #rightarrow #mu#mu M_{#mu#mu} 2500to4000"), color=(0, 188, 242), parent_process="Zmumu"),
            Process("Zmumu8", Label("Z/#gamma #rightarrow #mu#mu M_{#mu#mu} 4000to6000"), color=(0, 178, 148), parent_process="Zmumu"),
            Process("Zmumu9", Label("Z/#gamma #rightarrow #mu#mu M_{#mu#mu} 6000"), color=(0, 158, 73), parent_process="Zmumu"),
            Process("Zmumu_onshell_postBPix", Label("Z/#gamma #rightarrow #mu#mu M_{#mu#mu} 50to120"), color=ROOT.kAzure+10, isZonshell=True, parent_process="DY_postBPix"),
            Process("Zmumu_postBPix", Label("off-shell Z/#gamma #rightarrow #mu#mu"), color=ROOT.kAzure+1, parent_process="DY_postBPix"),
            # Z tautau #
            Process("Ztaus_preBPix", Label("Z/#gamma #rightarrow #tau#tau"), color=ROOT.kAzure+3, parent_process="DY_preBPix"),
            Process("Ztaus_postBPix", Label("Z/#gamma #rightarrow #tau#tau"), color=ROOT.kAzure+3, parent_process="DY_postBPix"),
            Process("Ztautau_onshell", Label("Z/#gamma #rightarrow #tau#tau M_{#mu#mu} 50to120"), color=(255, 241, 0), isZonshell=True, parent_process="Ztaus_preBPix"),
            Process("Ztautau", Label("off-shell Z/#gamma #rightarrow #tau#tau"), color=(206, 30, 30), parent_process="Ztaus_preBPix"),
            Process("Ztautau_onshell_postBPix", Label("Z/#gamma #rightarrow #mu#mu M_{#mu#mu} 50to120"), color=(255, 241, 0), isZonshell=True, parent_process="Ztaus_postBPix"),
            Process("Ztautau_postBPix", Label("off-shell Z/#gamma #rightarrow #mu#mu"), color=(206, 30, 30), parent_process="Ztaus_postBPix"),
            # Z boosted #
            Process("DY_ptZ", Label("boosted Z/#gamma #rightarrow ll"), color=(206, 30, 30), parent_process="DY_preBPix"),
            Process("DY_ptZ1", Label("Z/#gamma #rightarrow ll p_{T}^{#mu#mu} 40to100"), color=(255, 140, 0), isZboost=True, parent_process="DY_ptZ"),
            Process("DY_ptZ2", Label("Z/#gamma #rightarrow ll p_{T}^{#mu#mu} 100to200"), color=(232, 17, 35), isZboost=True, parent_process="DY_ptZ"),
            Process("DY_ptZ3", Label("Z/#gamma #rightarrow ll p_{T}^{#mu#mu} 200to400"), color=(236, 0, 140), isZboost=True, parent_process="DY_ptZ"),
            Process("DY_ptZ4", Label("Z/#gamma #rightarrow ll p_{T}^{#mu#mu} 400to600"), color=(104, 33, 122), isZboost=True, parent_process="DY_ptZ"),
            Process("DY_ptZ5", Label("Z/#gamma #rightarrow ll p_{T}^{#mu#mu} 600"), color=(0, 24, 143), isZboost=True, parent_process="DY_ptZ"),
            Process("DY_ptZ_postBPix", Label("boosted Z/#gamma #rightarrow ll"), color=(206, 30, 30), isZboost=True, parent_process="DY_postBPix"),

            ## Top ##
            Process("Top", Label("Top"), color=(36, 147, 25)),
            Process("Top_preBPix", Label("Top"), color=(36, 147, 25), parent_process="Top"),
            Process("Top_postBPix", Label("Top"), color=(36, 147, 25), parent_process="Top"),
            Process("TTbar", Label("t#bar{t}"), color=(36, 147, 25), parent_process="Top_preBPix"),
            Process("TTbar_postBPix", Label("t#bar{t}"), color=(36, 147, 25), parent_process="Top_postBPix"),
            Process("ST", Label("single t"), color=(36, 147, 25), parent_process="Top_preBPix"),
            Process("ST_postBPix", Label("single t"), color=(36, 147, 25), parent_process="Top_postBPix"),

            # Di-Boson
            Process("DiBoson", Label("DiBoson"), color=(206, 30, 30)),
            Process("DiBoson_preBPix", Label("DiBoson"), color=(206, 30, 30), parent_process="DiBoson"),
            Process("DiBoson_postBPix", Label("DiBoson"), color=(206, 30, 30), parent_process="DiBoson"),
            Process("WW", Label("WW"), color=(206, 30, 30), parent_process="DiBoson_preBPix"),
            Process("WW_postBPix", Label("WW"), color=(206, 30, 30), parent_process="DiBoson_postBPix"),
            Process("WZ", Label("WZ"), color=(206, 30, 30), parent_process="DiBoson_preBPix"),
            Process("WZ_postBPix", Label("WZ"), color=(206, 30, 30), parent_process="DiBoson_postBPix"),
            Process("ZZ", Label("ZZ"), color=(206, 30, 30), parent_process="DiBoson_preBPix"),
            Process("ZZ_postBPix", Label("ZZ"), color=(206, 30, 30), parent_process="DiBoson_postBPix"),

            ### DATA ###
            Process("Data2023", Label("Data"), color=(0, 0, 0), isData=True),
            Process("Data2023_preBPix", Label("Data"), color=(0, 0, 0), isData=True, parent_process="Data2023"),
            Process("Data2023_postBPix", Label("Data"), color=(0, 0, 0), isData=True, parent_process="Data2023"),

        ]

        process_group_names = {
            "Zmumu_mass-binned": [
                "Zmumu_onshell",
                "Zmumu2",
                "Zmumu3",
                "Zmumu4",
                "Zmumu5",
                "Zmumu6",
                "Zmumu7",
                "Zmumu8",
                "Zmumu9",
            ],

            "ptZ_binned": [
                "DY_ptZ1",
                "DY_ptZ2",
                "DY_ptZ3",
                "DY_ptZ4",
                "DY_ptZ5",
            ],

            "DY_stitching": [
                "Zmumu_onshell",
                "Zmumu",
                "Ztaus_preBPix",
                "DY_ptZ",
            ],

            "2023_preBPix": [
                "DY_preBPix",
                "Top_preBPix",
                "DiBoson_preBPix",
                "Data2023_preBPix",
            ],

            "2023_postBPix": [
                "DY_postBPix",
                "Top_postBPix",
                "DiBoson_postBPix",
                "Data2023_postBPix",
            ],

            "2023_full": [
                "DrellYan",
                "Top",
                "DiBoson",
                "Data2023",
            ],

        }

        return ObjectCollection(processes), process_group_names, []


    def prefix_datasets(self, datasets, prefix):

        for dataset in datasets:
            dataset.prefix = prefix + '//'


    def add_datasets(self):
        datasets = [

            ### Drell-Yan ###

            # ZtoMuMu

            Dataset("Zmumu_M-50to120",
                dataset="/DYto2Mu_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_onshell"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=2219.0,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-50to120_postBPix",
                dataset="/DYto2Mu_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_onshell_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=2219.0,
                tags=["postBPix"]),

            Dataset("Zmumu_M-120to200",
                dataset="/DYto2Mu_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu2"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=21.65,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-120to200_postBPix",
                dataset="/DYto2Mu_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=21.65,
                tags=["postBPix"]),

            Dataset("Zmumu_M-200to400",
                dataset="/DYto2Mu_MLL-200to400_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu3"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=3.058,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-200to400_postBPix",
                dataset="/DYto2Mu_MLL-200to400_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=3.058,
                tags=["postBPix"]),

            Dataset("Zmumu_M-400to800",
                dataset="/DYto2Mu_MLL-400to800_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu4"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.2691,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-400to800_postBPix",
                dataset="/DYto2Mu_MLL-400to800_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.2691,
                tags=["postBPix"]),

            Dataset("Zmumu_M-800to1500",
                dataset="/DYto2Mu_MLL-800to1500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu5"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.01915,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-800to1500_postBPix",
                dataset="/DYto2Mu_MLL-800to1500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.01915,
                tags=["postBPix"]),

            Dataset("Zmumu_M-1500to2500",
                dataset="/DYto2Mu_MLL-1500to2500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu6"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.001111,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-1500to2500_postBPix",
                dataset="/DYto2Mu_MLL-1500to2500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v4/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.001111,
                tags=["postBPix"]),

            Dataset("Zmumu_M-2500to4000",
                dataset="/DYto2Mu_MLL-2500to4000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu7"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.00005949,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-2500to4000_postBPix",
                dataset="/DYto2Mu_MLL-2500to4000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.00005949,
                tags=["postBPix"]),

            Dataset("Zmumu_M-4000to6000",
                dataset="/DYto2Mu_MLL-4000to6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu8"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.000001558,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-4000to6000_postBPix",
                dataset="/DYto2Mu_MLL-4000to6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.000001558,
                tags=["postBPix"]),

            Dataset("Zmumu_M-6000",
                dataset="/DYto2Mu_MLL-6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu9"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.00000003519,), # From GenXSecAnalyzer (NLO)

            Dataset("Zmumu_M-6000_postBPix",
                dataset="/DYto2Mu_MLL-6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Zmumu_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.00000003519,
                tags=["postBPix"]),

            # ZtoTauTau

            Dataset("Ztautau_M-50to120",
                dataset="/DYto2Tau_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_onshell"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=2219.0,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-50to120_postBPix",
                dataset="/DYto2Tau_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_onshell_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=2219.0,
                tags=["postBPix"]),

            Dataset("Ztautau_M-120to200",
                dataset="/DYto2Tau_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=21.65,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-120to200_postBPix",
                dataset="/DYto2Tau_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=21.65,
                tags=["postBPix"]),

            Dataset("Ztautau_M-200to400",
                dataset="/DYto2Tau_MLL-200to400_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=3.058,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-200to400_postBPix",
                dataset="/DYto2Tau_MLL-200to400_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=3.058,
                tags=["postBPix"]),

            Dataset("Ztautau_M-400to800",
                dataset="/DYto2Tau_MLL-400to800_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.2691,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-400to800_postBPix",
                dataset="/DYto2Tau_MLL-400to800_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.2691,
                tags=["postBPix"]),

            Dataset("Ztautau_M-800to1500",
                dataset="/DYto2Tau_MLL-800to1500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.01915,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-800to1500_postBPix",
                dataset="/DYto2Tau_MLL-800to1500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.01915,
                tags=["postBPix"]),

            Dataset("Ztautau_M-1500to2500",
                dataset="/DYto2Tau_MLL-1500to2500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.001111,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-1500to2500_postBPix",
                dataset="/DYto2Tau_MLL-1500to2500_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.001111,
                tags=["postBPix"]),

            Dataset("Ztautau_M-2500to4000",
                dataset="/DYto2Tau_MLL-2500to4000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.00005949,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-2500to4000_postBPix",
                dataset="/DYto2Tau_MLL-2500to4000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.00005949,
                tags=["postBPix"]),

            Dataset("Ztautau_M-4000to6000",
                dataset="/DYto2Tau_MLL-4000to6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.000001558,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-4000to6000_postBPix",
                dataset="/DYto2Tau_MLL-4000to6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.000001558,
                tags=["postBPix"]),

            Dataset("Ztautau_M-6000",
                dataset="/DYto2Tau_MLL-6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.00000003519,), # From GenXSecAnalyzer (NLO)

            Dataset("Ztautau_M-6000_postBPix",
                dataset="/DYto2Tau_MLL-6000_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("Ztautau_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.00000003519,
                tags=["postBPix"]),

            # DY_ptZ-binned

            Dataset("DY_ptZ-40to100_1J",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-40to100_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ1"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=477.2,), # From GenXSecAnalyzer (NLO)

            Dataset("DY_ptZ-40to100_1J_postBPix",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-40to100_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=477.2,
                tags=["postBPix"]),

            Dataset("DY_ptZ-40to100_2J",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-40to100_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ1"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=177.7,), # From GenXSecAnalyzer (NLO)

            Dataset("DY_ptZ-40to100_2J_postBPix",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-40to100_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=177.7,
                tags=["postBPix"]),

            Dataset("DY_ptZ-100to200_1J",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-100to200_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ2"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=45.50,), # From GenXSecAnalyzer (NLO)

            Dataset("DY_ptZ-100to200_1J_postBPix",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-100to200_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=45.50,
                tags=["postBPix"]),

            Dataset("DY_ptZ-100to200_2J",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-100to200_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ2"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=52.23,), # From GenXSecAnalyzer (NLO)

            Dataset("DY_ptZ-100to200_2J_postBPix",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-100to200_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=52.23,
                tags=["postBPix"]),

            Dataset("DY_ptZ-200to400_1J",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-200to400_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ3"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=3.370,), # From GenXSecAnalyzer (NLO)

            Dataset("DY_ptZ-200to400_1J_postBPix",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-200to400_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=3.370,
                tags=["postBPix"]),

            Dataset("DY_ptZ-200to400_2J",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-200to400_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ3"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=7.216,), # From GenXSecAnalyzer (NLO)

            Dataset("DY_ptZ-200to400_2J_postBPix",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-200to400_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=7.216,
                tags=["postBPix"]),

            Dataset("DY_ptZ-400to600_1J",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-400to600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ4"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.1167,), # From GenXSecAnalyzer (NLO)

            Dataset("DY_ptZ-400to600_1J_postBPix",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-400to600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.1167,
                tags=["postBPix"]),

            Dataset("DY_ptZ-400to600_2J",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-400to600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ4"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.4203,), # From GenXSecAnalyzer (NLO)

            Dataset("DY_ptZ-400to600_2J_postBPix",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-400to600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.4203,
                tags=["postBPix"]),

            Dataset("DY_ptZ-600_1J",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ5"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.01394,), # From GenXSecAnalyzer (NLO)

            Dataset("DY_ptZ-600_1J_postBPix",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.01394,
                tags=["postBPix"]),

            Dataset("DY_ptZ-600_2J",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ5"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=0.07020,), # From GenXSecAnalyzer (NLO)

            Dataset("DY_ptZ-600_2J_postBPix",
                dataset="/DYto2L-2Jets_MLL-50_PTLL-600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v1/"
                    "NANOAODSIM",
                process=self.processes.get("DY_ptZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=0.07020,
                tags=["postBPix"]),

            ### Top ###

            # TTbar

            Dataset("TT_2l2nu",
                dataset="/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=96.9,), # From TOP-22-012

            Dataset("TT_2l2nu_postBPix",
                dataset="/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=96.9,
                tags=["postBPix"]),

            Dataset("TT_lnu2q",
                dataset="/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=404.0,), # From TOP-22-012

            Dataset("TT_lnu2q_postBPix",
                dataset="/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("TTbar_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=404.0,
                tags=["postBPix"]),

            # Single Top

            Dataset("ST_tW-lnu2q",
                dataset="/TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=19.31,), # From https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopNNLORef x BR

            Dataset("ST_tW-lnu2q_postBPix",
                dataset="/TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=19.31,
                tags=["postBPix"]),

            Dataset("ST_tW-2l2nu",
                dataset="/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=4.663,),

            Dataset("ST_tW-2l2nu_postBPix",
                dataset="/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=4.663,
                tags=["postBPix"]),

            ## NOT YET ##
            #Dataset("ST_tbarW-lnu2q",
            #    dataset="/TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
            #        ""
            #        "NANOAODSIM",
            #    process=self.processes.get("ST"),
            #    prefix="xrootd-es-cie.ciemat.es:1096//",
            #    runPeriod="preBPix",
            #    xs=19.31,), 

            Dataset("ST_tbarW-lnu2q_postBPix",
                dataset="/TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=19.31,
                tags=["postBPix"]),

            Dataset("ST_tbarW-2l2nu",
                dataset="/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v15-v4/"
                    "NANOAODSIM",
                process=self.processes.get("ST"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=4.663,), 

            Dataset("ST_tbarW-2l2nu_postBPix",
                dataset="/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v6-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ST_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=4.663,
                tags=["postBPix"]),

            ## NOT YET ##
#            Dataset("ST_s-top",
#                dataset="/TBbartoLplusNuBbar-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/"
#                    ""
#                    "NANOAODSIM",
#                process=self.processes.get("ST"),
#                prefix="xrootd-es-cie.ciemat.es:1096//",
#                runPeriod="preBPix",
#                xs=3.623,),

#            Dataset("ST_s-top_postBPix",
#                dataset="/TBbartoLplusNuBbar-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/"
#                    ""
#                    "NANOAODSIM",
#                process=self.processes.get("ST_postBPix"),
#                prefix="xrootd-es-cie.ciemat.es:1096//",
#                runPeriod="postBPix",
#                xs=3.623,
#                tags=["postBPix"]),

#            Dataset("ST_s-tbar",
#                dataset="/TbarBtoLminusNuB-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/"
#                    ""
#                    "NANOAODSIM",
#                process=self.processes.get("ST"),
#                prefix="xrootd-es-cie.ciemat.es:1096//",
#                runPeriod="preBPix",
#                xs=3.623,),

#            Dataset("ST_s-tbar_postBPix",
#                dataset="/TbarBtoLminusNuB-s-channel-4FS_TuneCP5_13p6TeV_amcatnlo-pythia8/"
#                    ""
#                    "NANOAODSIM",
#                process=self.processes.get("ST_postBPix"),
#                prefix="xrootd-es-cie.ciemat.es:1096//",
#                runPeriod="postBPix",
#                xs=3.623,
#                tags=["postBPix"]),

#            Dataset("ST_t-top",
#                dataset="/TBbarQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/"
#                    ""
#                    "NANOAODSIM",
#                process=self.processes.get("ST"),
 #               prefix="xrootd-es-cie.ciemat.es:1096//",
#                runPeriod="preBPix",
#                xs=145.0,),

#            Dataset("ST_t-top_postBPix",
#                dataset="/TBbarQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/"
#                    ""
#                    "NANOAODSIM",
#                process=self.processes.get("ST_postBPix"),
#                prefix="xrootd-es-cie.ciemat.es:1096//",
#                runPeriod="postBPix",
#                xs=145.0,
#                tags=["postBPix"]),

#            Dataset("ST_t-tbar",
#                dataset="/TbarBQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/"
#                    ""
#                    "NANOAODSIM",
#                process=self.processes.get("ST"),
#                prefix="xrootd-es-cie.ciemat.es:1096//",
#                runPeriod="preBPix",
#                xs=87.2,),

#            Dataset("ST_t-tbar_postBPix",
#                dataset="/TbarBQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/"
#                    ""
#                    "NANOAODSIM",
#                process=self.processes.get("ST_postBPix"),
#                prefix="xrootd-es-cie.ciemat.es:1096//",
#                runPeriod="postBPix",
#                xs=87.2,
#                tags=["postBPix"]),


            ### DiBoson ###

            Dataset("WW_2l2nu",
                dataset="/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v4/"
                    "NANOAODSIM",
                process=self.processes.get("WW"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=12.98,), # From 13 TeV value with 4% expected increase with MCFM x BR

            Dataset("WW_2l2nu_postBPix",
                dataset="/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("WW_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=12.98,
                tags=["postBPix"]),

            Dataset("WW_lnu2q",
                dataset="/WWtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("WW"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=53.73,),

            Dataset("WW_lnu2q_postBPix",
                dataset="/WWtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v3/"
                    "NANOAODSIM",
                process=self.processes.get("WW_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=53.73,
                tags=["postBPix"]),

            Dataset("WZ_2l2q",
                dataset="/WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v3/"
                    "NANOAODSIM",
                process=self.processes.get("WZ"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=3.661,), # From MATRIX (SMP-22-017 at NNLO) x BR

            Dataset("WZ_2l2q_postBPix",
                dataset="/WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=3.661,
                tags=["postBPix"]),

            Dataset("WZ_3lnu",
                dataset="/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=1.769,),  

            Dataset("WZ_3lnu_postBPix",
                dataset="/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=1.769,
                tags=["postBPix"]),

            Dataset("WZ_lnu2q",
                dataset="/WZtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=12.39,),  

            Dataset("WZ_lnu2q_postBPix",
                dataset="/WZtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("WZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=12.39,
                tags=["postBPix"]),

            Dataset("ZZ",
                dataset="/ZZ_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ZZ"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                xs=16.7,), # From MATRIX (SMP-22-017 at NNLO)

            Dataset("ZZ_postBPix",
                dataset="/ZZ_TuneCP5_13p6TeV_pythia8/"
                    "Run3Summer23BPixNanoAODv12-130X_mcRun3_2023_realistic_postBPix_v2-v2/"
                    "NANOAODSIM",
                process=self.processes.get("ZZ_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                xs=16.7,
                tags=["postBPix"]),


            # DATA: ReMini + ReNano CD

            Dataset("Data0_2023C_v1",
                dataset="/Muon0/Run2023C-22Sep2023_v1-v1/NANOAOD",
                process=self.processes.get("Data2023_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                runEra="C",),

            Dataset("Data0_2023C_v2",
                dataset="/Muon0/Run2023C-22Sep2023_v2-v1/NANOAOD",
                process=self.processes.get("Data2023_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                runEra="C",),

            Dataset("Data0_2023C_v3",
                dataset="/Muon0/Run2023C-22Sep2023_v3-v1/NANOAOD",
                process=self.processes.get("Data2023_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                runEra="C",),

            Dataset("Data0_2023C_v4",
                dataset="/Muon0/Run2023C-22Sep2023_v4-v1/NANOAOD",
                process=self.processes.get("Data2023_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                runEra="C",),

            Dataset("Data1_2023C_v1",
                dataset="/Muon1/Run2023C-22Sep2023_v1-v1/NANOAOD",
                process=self.processes.get("Data2023_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                runEra="C",),

            Dataset("Data1_2023C_v2",
                dataset="/Muon1/Run2023C-22Sep2023_v2-v1/NANOAOD",
                process=self.processes.get("Data2023_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                runEra="C",),

            Dataset("Data1_2023C_v3",
                dataset="/Muon1/Run2023C-22Sep2023_v3-v1/NANOAOD",
                process=self.processes.get("Data2023_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="preBPix",
                runEra="C",),

            Dataset("Data1_2023C_v4",
                dataset="/Muon1/Run2023C-22Sep2023_v4-v1/NANOAOD",
                process=self.processes.get("Data2023_preBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//", # NOTE: Not fully completed, 98.28%
                runPeriod="preBPix",
                runEra="C",),

            Dataset("Data0_2023D_v1",
                dataset="/Muon0/Run2023D-22Sep2023_v1-v1/NANOAOD",
                process=self.processes.get("Data2023_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                runEra="D",
                tags=["postBPix"]),

            Dataset("Data0_2023D_v2",
                dataset="/Muon0/Run2023D-22Sep2023_v2-v1/NANOAOD",
                process=self.processes.get("Data2023_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                runEra="D",
                tags=["postBPix"]),

            Dataset("Data1_2023D_v1",
                dataset="/Muon1/Run2023D-22Sep2023_v1-v1/NANOAOD",
                process=self.processes.get("Data2023_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                runEra="D",
                tags=["postBPix"]),

            Dataset("Data1_2023D_v2",
                dataset="/Muon1/Run2023D-22Sep2023_v2-v1/NANOAOD",
                process=self.processes.get("Data2023_postBPix"),
                prefix="xrootd-es-cie.ciemat.es:1096//",
                runPeriod="postBPix",
                runEra="D",
                tags=["postBPix"]),

        ]
        return ObjectCollection(datasets)

    def add_features(self):
        
        ### Feature selections ###
        barrel_dimu   = "fabs(Muon_eta.at(mu1_index)) <= 1.2 || fabs(Muon_eta.at(mu2_index)) <= 1.2"
        endcap_dimu   = "(fabs(Muon_eta.at(mu1_index)) > 1.2 && fabs(Muon_eta.at(mu1_index)) <= 2.1) || (fabs(Muon_eta.at(mu2_index)) > 1.2 && fabs(Muon_eta.at(mu2_index)) <= 2.1)"
        forwardE_dimu = "fabs(Muon_eta.at(mu1_index)) > 2.1 || fabs(Muon_eta.at(mu2_index)) > 2.1"

        ### Labels for Selections ###
        axis_barrel   = " |#eta| < 1.2"
        axis_endcap   = " 1.2 < |#eta| < 2.1"
        axis_forwardE = " |#eta| > 2.1"
 
        features = [
            # Curvature
            Feature("kappa_mu1", "1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))", binning=(50, -5., 5.),
                x_title=Label("#mu_{1} #kappa"),
                units="TeV^{-1}"),
            Feature("kappa_mu2", "1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))", binning=(50, -5., 5.),
                x_title=Label("#mu_{2} #kappa"),
                units="TeV^{-1}"),
            Feature("kappa", "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)), 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))})", binning=(50, -5., 5.),
                x_title=Label("#kappa"),
                units="TeV^{-1}"),

            Feature("kappa_barrel", "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(fabs(Muon_eta.at(mu1_index)) <= 1.2)), 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(fabs(Muon_eta.at(mu2_index)) <= 1.2))})", binning=(50, -5., 5.),
                selection=barrel_dimu,
                x_title=Label("#kappa"+axis_barrel),
                units="TeV^{-1}"),
            Feature("kappa_endcap", "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(fabs(Muon_eta.at(mu1_index)) > 1.2 && fabs(Muon_eta.at(mu1_index)) <= 2.1) ), 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(fabs(Muon_eta.at(mu2_index)) > 1.2 && fabs(Muon_eta.at(mu2_index)) <= 2.1) )})", binning=(50, -5., 5.),
                selection=endcap_dimu,
                x_title=Label("#kappa"+axis_endcap),
                units="TeV^{-1}"),
            Feature("kappa_forwardE", "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(fabs(Muon_eta.at(mu1_index)) > 2.1)), 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(fabs(Muon_eta.at(mu2_index)) > 2.1))})", binning=(50, -5., 5.),
                selection=forwardE_dimu,
                x_title=Label("#kappa"+axis_forwardE),
                units="TeV^{-1}"),
            
            # pT single muons
            Feature("pt_mu1", "Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)", binning=(50, 0, 2200),
                x_title=Label("#mu_{1} p_{T}"),
                units="GeV"),
            Feature("pt_mu2", "Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)", binning=(50, 0, 2200),
                x_title=Label("#mu_{2} p_{T}"),
                units="GeV"),
            Feature("pt_muPlus", "(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == 1)) + (Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == 1))",
                binning=(50, 0, 2200),
                x_title=Label("#mu^{+} p_{T}"),
                units="GeV"),
            Feature("pt_muMinus", "(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == -1)) + (Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == -1))",
                binning=(50, 0, 2200),
                x_title=Label("#mu^{-} p_{T}"),
                units="GeV"),

            Feature("pt_muPlus_barrel", "(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == 1)) + (Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == 1))", 
                binning=(50, 0, 2200),
                selection=barrel_dimu,
                x_title=Label("#mu^{+} p_{T}"+axis_barrel),
                units="GeV"),
            Feature("pt_muMinus_barrel", "(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == -1)) + (Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == -1))", 
                binning=(50, 0, 2200),
                selection=barrel_dimu,
                x_title=Label("#mu^{-} p_{T}"+axis_barrel),
                units="GeV"),
            Feature("pt_muPlus_endcap", "(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == 1)) + (Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == 1))", 
                binning=(50, 0, 2200),
                selection=endcap_dimu,
                x_title=Label("#mu^{+} p_{T}"+axis_endcap),
                units="GeV"),
            Feature("pt_muMinus_endcap", "(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == -1)) + (Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == -1))", 
                binning=(50, 0, 2200),
                selection=endcap_dimu,
                x_title=Label("#mu^{-} p_{T}"+axis_endcap),
                units="GeV"),
            Feature("pt_muPlus_forwardE", "(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == 1)) + (Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == 1))", 
                binning=(50, 0, 2200),
                selection=forwardE_dimu,
                x_title=Label("#mu^{+} p_{T}"+axis_forwardE),
                units="GeV"),
            Feature("pt_muMinus_forwardE", "(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(Muon_charge.at(mu1_index) == -1)) + (Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(Muon_charge.at(mu2_index) == -1))", 
                binning=(50, 0, 2200),
                selection=forwardE_dimu,
                x_title=Label("#mu^{-} p_{T}"+axis_forwardE),
                units="GeV"),
            
            # pT Z
            Feature("pt_Z_peak", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 400),
                x_title=Label("p_{T_{#mu#mu}}"),
                units="GeV"),
            Feature("pt_Z_tail", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 2200),
                x_title=Label("p_{T_{#mu#mu}}"),
                units="GeV"),

            Feature("pt_Z_peak_barrel", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 400),
                selection=barrel_dimu,
                x_title=Label("p_{T_{#mu#mu}}"+axis_barrel),
                units="GeV"),
            Feature("pt_Z_peak_endcap", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 400),
                selection=endcap_dimu,
                x_title=Label("p_{T_{#mu#mu}}"+axis_endcap),
                units="GeV"),
            Feature("pt_Z_peak_forwardE", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 400),
                selection=forwardE_dimu,
                x_title=Label("p_{T_{#mu#mu}}"+axis_forwardE),
                units="GeV"),
            Feature("pt_Z_tail_barrel", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 2200),
                selection=barrel_dimu,
                x_title=Label("p_{T_{#mu#mu}}"+axis_barrel),
                units="GeV"),
            Feature("pt_Z_tail_endcap", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 2200),
                selection=endcap_dimu,
                x_title=Label("p_{T_{#mu#mu}}"+axis_endcap),
                units="GeV"),
            Feature("pt_Z_tail_forwardE", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", binning=(50, 0, 2200),
                selection=forwardE_dimu,
                x_title=Label("p_{T_{#mu#mu}}"+axis_forwardE),
                units="GeV"),
            
            # Mass Z
            Feature("Z_mass_peak", "DiMuon_invM", binning=(50, 60, 120),
                x_title=Label("M_{#mu#mu}"),
                units="GeV"),
            Feature("Z_mass_tail", "DiMuon_invM", binning=(50, 0, 5000),
                x_title=Label("M_{#mu#mu}"),
                units="GeV"),

            Feature("Z_mass_peak_barrel", "DiMuon_invM", binning=(50, 60, 120),
                selection=barrel_dimu,
                x_title=Label("M_{#mu#mu}"+axis_barrel),
                units="GeV"),
            Feature("Z_mass_peak_endcap", "DiMuon_invM", binning=(50, 60, 120),
                selection=endcap_dimu,
                x_title=Label("M_{#mu#mu}"+axis_endcap),
                units="GeV"),
            Feature("Z_mass_peak_forwardE", "DiMuon_invM", binning=(50, 60, 120),
                selection=forwardE_dimu,
                x_title=Label("M_{#mu#mu}"+axis_forwardE),
                units="GeV"),
            Feature("Z_mass_tail_barrel", "DiMuon_invM", binning=(50, 0, 5000),
                selection=barrel_dimu,
                x_title=Label("M_{#mu#mu}"+axis_barrel),
                units="GeV"),
            Feature("Z_mass_tail_endcap", "DiMuon_invM", binning=(50, 0, 5000),
                selection=endcap_dimu,
                x_title=Label("M_{#mu#mu}"+axis_endcap),
                units="GeV"),
            Feature("Z_mass_tail_forwardE", "DiMuon_invM", binning=(50, 0, 5000),
                selection=forwardE_dimu,
                x_title=Label("M_{#mu#mu}"+axis_forwardE),
                units="GeV"),
            
            # Eta and Phi
            Feature("eta", "std::vector<float>({Muon_eta.at(mu1_index), Muon_eta.at(mu2_index)})", binning=(50, -2.5, 2.5),
                x_title=Label("#eta")),
            Feature("phi", "std::vector<float>({Muon_phi.at(mu1_index), Muon_phi.at(mu2_index)})", binning=(50, -3.2, 3.2),
                x_title=Label("#phi"),
                units="rad"),

            # PileUp plot                                                                    
            Feature("nVertices", "PV_npvsGood", binning=(80, 0, 80),
                x_title=Label("# of vertices")),

            # WEIGHTS
#            Feature("L1PreFiringWeight", "L1PreFiringWeight", binning=(20, 0, 2),
#                x_title=Label("L1PreFiringWeight"),
#                central="prefiring_nom"),
#                #systematics=["prefiring_syst"]),
        ]

        ### GEN LEVEL PLOTS ###

        gen_features = [

            Feature("lhe_Zpt_peak", "LHE_Vpt", binning=(200, 0, 400),
                x_title=Label("LHE p_{T}^{#mu#mu}"),
                units="GeV"),
            Feature("lhe_Zpt_tail", "LHE_Vpt", binning=(200, 0, 2200),
                x_title=Label("LHE p_{T}^{#mu#mu}"),
                units="GeV"),

            Feature("genZ_mass_peak", "sqrt(2*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(cosh(GenPart_eta.at(Muon_genPartIdx.at(mu1_index))-GenPart_eta.at(Muon_genPartIdx.at(mu2_index)))-cos(GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))))", binning=(200, 0, 300),
                selection="(Muon_genPartIdx.at(mu1_index)>-1 && Muon_genPartIdx.at(mu2_index)>-1)",
                x_title=Label("gen m_{#mu#mu}"),
                units="GeV"),
            Feature("genZ_mass_tail", "sqrt(2*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(cosh(GenPart_eta.at(Muon_genPartIdx.at(mu1_index))-GenPart_eta.at(Muon_genPartIdx.at(mu2_index)))-cos(GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))))", binning=(200, 0, 7000),
                selection="(Muon_genPartIdx.at(mu1_index)>-1 && Muon_genPartIdx.at(mu2_index)>-1)",
                x_title=Label("gen m_{#mu#mu}"),
                units="GeV"),

            Feature("mu1_genPt", "GenPart_pt.at(Muon_genPartIdx.at(mu1_index))", binning=(100, 0, 2500),
                x_title=Label("gen #mu_{1} p_{T}"),
                selection="Muon_genPartIdx.at(mu1_index)>-1",
                units="GeV"),
            Feature("mu2_genPt", "GenPart_pt.at(Muon_genPartIdx.at(mu2_index))", binning=(100, 0, 2500),
                x_title=Label("gen #mu_{2} p_{T}"),
                selection="Muon_genPartIdx.at(mu2_index)>-1",
                units="GeV"),

            Feature("Z_pt_peak", "DiMuon_pt", binning=(200, 0, 400),
                x_title=Label("p_{T}^{#mu#mu}"),
                units="GeV"),
            Feature("Z_pt_tail", "DiMuon_pt", binning=(200, 0, 2200),
                x_title=Label("p_{T}^{#mu#mu}"),
                units="GeV"),

            Feature("mZ_peak", "DiMuon_invM", binning=(200, 0, 300),
                x_title=Label("m_{#mu#mu}"),
                units="GeV"),
            Feature("mZ_tail", "DiMuon_invM", binning=(200, 0, 7000),
                x_title=Label("m_{#mu#mu}"),
                units="GeV"),


#UNCOMMENT
#            Feature("Z_genPt_tail", "sqrt((GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))+(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))+2*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(cos(GenPart_phi.at(Muon_genPartIdx.at(mu1_index)))*cos(GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))+sin(GenPart_phi.at(Muon_genPartIdx.at(mu1_index)))*sin(GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))))", binning=(200, 0, 2200),
#                x_title=Label("gen p_{T_{#mu#mu}}"),
#                selection="Muon_genPartIdx.at(mu1_index)>-1 && Muon_genPartIdx.at(mu2_index)>-1",
#                units="GeV"),
#            Feature("Z_genPt_peak", "sqrt((GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))+(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))+2*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(cos(GenPart_phi.at(Muon_genPartIdx.at(mu1_index)))*cos(GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))+sin(GenPart_phi.at(Muon_genPartIdx.at(mu1_index)))*sin(GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))))", binning=(200, 0, 500),
#                x_title=Label("gen p_{T_{#mu#mu}}"),
#                selection="Muon_genPartIdx.at(mu1_index)>-1 && Muon_genPartIdx.at(mu2_index)>-1",
#                units="GeV"),

#UNCOMMENT
#            Feature("Z_genM_tail_1", "sqrt(2*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(cosh(GenPart_eta.at(Muon_genPartIdx.at(mu1_index))-GenPart_eta.at(Muon_genPartIdx.at(mu2_index)))-cos(GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index))-2*3.1416)))", binning=(200, 0, 4000),
#                selection="(Muon_genPartIdx.at(mu1_index)>-1 && Muon_genPartIdx.at(mu2_index)>-1) && (GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))>3.1416",
#                x_title=Label("gen M_{#mu#mu}"),
#                units="GeV"),
            #Feature("Z_genM_tail_2", "sqrt(2*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(cosh(GenPart_eta.at(Muon_genPartIdx.at(mu1_index))-GenPart_eta.at(Muon_genPartIdx.at(mu2_index)))-cos(GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index))+2*3.1416)))", binning=(50, 0, 5000),
            #    selection="(Muon_genPartIdx.at(mu1_index)>-1 && Muon_genPartIdx.at(mu2_index)>-1) && (GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))<-3.1416",
            #    x_title=Label("gen M_{#mu#mu}"),
            #    units="GeV"),
#UNCOMMENT
#            Feature("Z_genM_peak_1", "sqrt(2*(GenPart_pt.at(Muon_genPartIdx.at(mu1_index)))*(GenPart_pt.at(Muon_genPartIdx.at(mu2_index)))*(cosh(GenPart_eta.at(Muon_genPartIdx.at(mu1_index))-GenPart_eta.at(Muon_genPartIdx.at(mu2_index)))-cos(GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index))-2*3.1416)))", binning=(200, 0, 300),
#                selection="(Muon_genPartIdx.at(mu1_index)>-1 && Muon_genPartIdx.at(mu2_index)>-1) && (GenPart_phi.at(Muon_genPartIdx.at(mu1_index))-GenPart_phi.at(Muon_genPartIdx.at(mu2_index)))>3.1416",
#                x_title=Label("gen M_{#mu#mu}"),
#                units="GeV"),
#UNCOMMENT
            
        ]

        ### ptZ Reweight Histo ###
        ptZ_feature = [
            Feature("ptZ", "sqrt((Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))+(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))+2*(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index))*(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index))*(cos(Muon_phi.at(mu1_index))*cos(Muon_phi.at(mu2_index))+sin(Muon_phi.at(mu1_index))*sin(Muon_phi.at(mu2_index))))", 
                binning=(100, 0, 1500),
                x_title=Label("p_{T_{#mu#mu}}"),
                units="GeV"),

            # WEIGHTS
            Feature("L1PreFiringWeight", "L1PreFiringWeight", binning=(20, 0, 2),
                x_title=Label("L1PreFiringWeight"),
                central="prefiring_nom"),
                #systematics=["prefiring_syst"]),

        ]
        
        ### Curvature with Bias ###
        biases = []

        # Curvature regions
        etas = [-2.4, -2.1, -1.2, 0, 1.2, 2.1, 2.4]
        phis_deg = [-180, -60, 60, 180]
        phis = [-math.pi, -math.pi/3.0, math.pi/3.0, math.pi]
        axis = []
        selections = []

        for i in range(len(etas)-1):
            for j in range(len(phis)-1):
                axis.append(str(etas[i])+" < #eta < "+str(etas[i+1]) + " , " + str(phis_deg[j])+" < #phi < "+str(phis_deg[j+1]))

                selections.append( "(Muon_eta.at(mu1_index) > " + str(etas[i]) + " && Muon_eta.at(mu1_index) <= " + str(etas[i+1]) + " && Muon_phi.at(mu1_index) > " + str(phis[j]) + " && Muon_phi.at(mu1_index) <= " + str(phis[j+1]) + ") || (Muon_eta.at(mu2_index) > " + str(etas[i]) + " && Muon_eta.at(mu2_index) <= " + str(etas[i+1]) + " && Muon_phi.at(mu2_index) > " + str(phis[j]) + " && Muon_phi.at(mu2_index) <= " + str(phis[j+1]) + ")" )

        #bin_sel = [(20, -5., 5.) if i==0 or i==1 or i==2 or i==15 or i==16 or i==17 else (50, -5., 5.) for i in range(len(selections))] # Actual -> cte.

        #var_bin = [-7,-6.5,-6,-5.5,-5,-4.5,-4,-3.5,-3,-2,0,2,3,3.5,4,4.5,5,5.5,6,6.5,7]
        #var_bin = [-9,-8.5,-8,-7.5,-7,-6.5,-6,-5.5,-5,-4.5,-4,-3.5,-3,-2,0,2,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9]
        #bin_sel = [var_bin if i==0 or i==1 or i==2 or i==15 or i==16 or i==17 else (50, -5., 5.) for i in range(len(selections))] # Nuevo -> Variable
        bin_sel = [(60, -9., 9.) if i==0 or i==1 or i==2 or i==15 or i==16 or i==17 else (60, -5., 5.) for i in range(len(selections))] # General for rebin

        feature_bias = [
#            # WEIGHTS                                                                                                                                    
#            Feature("L1PreFiringWeight", "L1PreFiringWeight", binning=(20, 0, 2),
#                x_title=Label("L1PreFiringWeight"),
#                central="prefiring_nom"),                                                                                                       
	]

        for i in range (161):
            biases.append(round(-0.8 + 0.01*i, 2))
        for bias in biases:
            ### For Inclusive Bias ###
            feature_bias.append( Feature("kappa_%s" %bias, "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)) + (float)%s, 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)) + (float)%s})" %(bias, bias), 
                binning=(50, -5., 5.),
                x_title=Label("#kappa"),
                units="TeV^{-1}"), )
            ### For Bias Map ###
#            for x,sel in enumerate(selections):
#                feature_bias.append( Feature("kappa_%s_%s" %(x,bias), "std::vector<float>({1000*Muon_charge.at(mu1_index)/(Muon_tunepRelPt.at(mu1_index)*Muon_pt.at(mu1_index)*(mu1_region == %s)) + (float)%s, 1000*Muon_charge.at(mu2_index)/(Muon_tunepRelPt.at(mu2_index)*Muon_pt.at(mu2_index)*(mu2_region == %s)) + (float)%s})" %(x, bias, x, bias), 
#                    binning=bin_sel[x],
#                    selection=sel,
#                    x_title=Label("#kappa  " + axis[x]),
#                    units="TeV^{-1}"), )


        return ObjectCollection(feature_bias)

    def add_versions(self):
        versions = {}
        return versions

    def add_weights(self):
        weights = DotDict()
        weights.default = "1"

        weights.total_events_weights = ["genWeight", "puWeight"]

        weights.preselection_2023 = ["genWeight", "puWeight", "mu_idSF_weight", "mu_isoSF_weight", "mu_hltSF_weight", "mu_recoSF_weight"]

        return weights

    def add_systematics(self):
        systematics = [
            Systematic("prefiring_nom", "_Nom"),
            #Systematic("perfiring_syst", "", up="_Up", down="_Dn")
            ]

        return ObjectCollection(systematics)

    def add_default_module_files(self):
        defaults = {}
        return defaults

    # feature methods

    def get_central_value(self, feature):
        """
        Return the expression from the central value of a feature
        """
        if feature.central == "":
            return self.central
        return self.systematics.get(feature.central).expression

    def get_object_expression(self, feature, isMC=False,
            syst_name="central", systematic_direction=""):
        """
        Returns a feature or category's expression including the systematic considered
        """

        def get_expression(obj):
            if isinstance(obj, Feature):
                return obj.expression
            elif isinstance(obj, Category):
                return obj.selection
            elif isinstance(obj, str):
                return obj
            else:
                raise ValueError("Object %s cannot be used in method get_feature_expression" % obj)

        def add_systematic_tag(feat_expression, tag):
            """
            Includes systematic tag in the feature expression.
                - Directly if it does not come from a vector
                - Before ".at" if it comes from a vector
            """
            if ".at" in feat_expression:
                index = feat_expression.find(".at")
                return feat_expression[:index] + tag + feat_expression[index:]
            else:
                return feat_expression + tag

        feature_expression = get_expression(feature)
        if "{{" in feature_expression:  # derived expression
            while "{{" in feature_expression:
                initial = feature_expression.find("{{")
                final = feature_expression.find("}}")
                feature_name_to_look = feature_expression[initial + 2: final]
                feature_to_look = self.features.get(feature_name_to_look)
                feature_to_look_expression = feature_to_look.expression
                if not isMC:
                    tag = ""
                elif syst_name in feature_to_look.systematics:
                    syst = self.systematics.get(syst_name)
                    if type(syst.expression) == tuple:
                        feature_to_look_expression = feature_to_look_expression.replace(
                            syst.expression[0], syst.expression[1])
                        tag = ""
                    else:
                        tag = syst.expression
                    tag += eval("syst.%s" % systematic_direction)
                else:
                    if feature_to_look.central == "":
                        tag = ""
                    else:
                        central = self.systematics.get(feature_to_look.central)
                        if type(central.expression) == tuple:
                            feature_to_look_expression = feature_to_look_expression.replace(
                                central.expression[0], central.expression[1])
                            tag = ""
                        else:
                            tag = central.expression

                feature_to_look_expression = add_systematic_tag(feature_to_look_expression, tag)
                feature_expression = feature_expression.replace(feature_expression[initial: final + 2],
                    feature_to_look_expression)
            return feature_expression

        elif isinstance(feature, Feature):  # not derived expression and not a category
            if not isMC:
                return add_systematic_tag(feature.expression, "")
            feature_expression = feature.expression
            tag = ""
            if syst_name in feature.systematics:
                syst = self.systematics.get(syst_name)
                if type(syst.expression) == tuple:
                    feature_expression = feature_expression.replace(syst.expression[0],
                        syst.expression[1])
                    tag = ""
                else:
                    tag = syst.expression
                tag += eval("syst.%s" % systematic_direction)
            else:
                if feature.central != "":
                    central = self.systematics.get(feature.central)
                    if type(central.expression) == tuple:
                        feature_expression = feature_expression.replace(central.expression[0],
                            central.expression[1])
                        tag = ""
                    else:
                        tag = central.expression
            return add_systematic_tag(feature_expression, tag)
        else:
            return get_expression(feature)

    def get_systematics_from_expression(self, expression):
        systs = []
        while "{{" in expression:
            initial = expression.find("{{")
            final = expression.find("}}")
            feature_name_to_look = expression[initial + 2: final]
            feature_to_look = self.features.get(feature_name_to_look)
            feature_to_look_expression = feature_to_look.expression
            expression = expression.replace(expression[initial: final + 2], "")
            systs += (feature_to_look.systematics + self.get_systematics_from_expression(
                feature_to_look_expression))
        return systs

    def get_weights_systematics(self, list_of_weights, isMC=False):
        systematics = []
        config_systematics = self.systematics.names()
        if isMC:
            for weight in list_of_weights:
                try:
                    feature = self.features.get(weight)
                    for syst in feature.systematics:
                        if syst not in systematics and syst in config_systematics:
                            systematics.append(syst)
                except ValueError:
                    continue
        return systematics

    def get_norm_systematics(self, process_datasets, region):
        return []

    def get_weights_expression(self, list_of_weights, syst_name="central", systematic_direction=""):
        weights = []
        for weight in list_of_weights:
            try:
                feature = self.features.get(weight)
                weights.append(self.get_object_expression(
                    feature, True, syst_name, systematic_direction))
            except ValueError:
                weights.append(weight)
        return "*".join(weights)

    def is_process_from_dataset(self, process_name, dataset_name=None, dataset=None):
        assert dataset_name or dataset
        assert not (dataset_name and dataset)

        if not dataset:
            dataset = self.datasets.get(dataset_name)

        process = dataset.process
        while True:
            if process.name == process_name:
                return True
            elif process.parent_process:
                process = self.processes.get(process.parent_process)
            else:
                return False

    def get_inner_text_for_plotting(self, category, region):
        inner_text = ""
        #inner_text=[category.label + " category"]
        if region:
            if isinstance(region.label, list):
                inner_text += region.label
            else:
                inner_text.append(region.label)
        return inner_text


config = Config("base", year=2023, ecm=13.6, lumi_pb=27101)
