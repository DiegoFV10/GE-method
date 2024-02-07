biases = []
for i in range (161):
    biases.append(-0.8 + 0.01*i)

### For Inclusive Bias ###
"""
with open("/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/inclusiveBias_2022postEE.txt","w") as f:
    for bias in biases:
        f.write("/eos/user/d/diegof/cmt/FeaturePlot/GE2022_config/cat_preselection_2022/biasHistos_2022postEE/root/kappa_%s__pg_2022_postEE.root" %bias)
        f.write("\n")
f.close()
"""
### For Bias Maps ###

for i in range(18):
    with open("/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/2022postEE/chi2Map_%s_2022postEE_incomplete.txt" %i,"w") as f:
        for bias in biases:
            #f.write("/eos/user/d/diegof/cmt/FeaturePlot/GEMethod_config/cat_preselection_UL18/biasMap_UL18_GOOD/root/kappa_%s_%s__pg_UL18_corrected.root" %(i,bias))
            #f.write("/eos/user/d/diegof/cmt/FeaturePlot/UL17_config/cat_preselection_UL17/biasMap_UL17_GOOD/root/kappa_%s_%s__pg_UL17.root" %(i,bias))
            f.write("/eos/user/d/diegof/cmt/FeaturePlot/GE2022_config/cat_preselection_2022/biasMap_2022postEE_partial/root/kappa_%s_%s__pg_2022_postEE.root" %(i,bias))
            f.write("\n")
    f.close()

