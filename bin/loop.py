from analysis_tools.utils import import_root

ROOT = import_root()

f = "root://xrootd-cms.infn.it:///store/data/Run2016B/SingleMuon/NANOAOD/ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v2/2520000/184135A0-03E0-D042-8323-1E2648EB869F.root"

df = ROOT.RDataFrame("Events", f)


ROOT.gInterpreter.Declare(f"""

        struct MyFunctor {{
             void operator()(ULong64_t e) {{
                if (e % 100000 == 0)
                    cout << e << endl;
                return;
            }}
        }};
""")

 

f = ROOT.MyFunctor()

df.Foreach(f, ["rdfentry_"])

print(df.Count().GetValue())
