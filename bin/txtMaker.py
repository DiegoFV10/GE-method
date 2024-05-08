biases = []
for i in range (161):
    biases.append(-0.8 + 0.01*i)

### For Inclusive Bias ###
"""
with open("/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/inclusiveBias_2023postBPix.txt","w") as f:
    for bias in biases:
        f.write("/eos/user/d/diegof/cmt/FeaturePlot/GE2023_config/cat_preselection_2023/inclusiveBias_postBPix/root/kappa_%s__pg_2023_full.root" %bias)
        f.write("\n")
f.close()
"""
### For Bias Maps ###

for i in range(18):
    with open("/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/2022checks/2022E/chi2Map_%s_2022E.txt" %i,"w") as f:
        for bias in biases:
            f.write("/eos/user/d/diegof/cmt/FeaturePlot/GE2022_config/cat_preselection_2022/biasMap_2022E/root/kappa_%s_%s__pg_2022_full.root" %(i,bias))
            f.write("\n")
    f.close()

