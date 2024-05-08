#include "TMath.h"
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <math.h>
#include <time.h>
#include "TFile.h"
#include "TChain.h"
#include "TTree.h"
#include "TBranch.h"
#include "TH1.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TF1.h"
#include "TAxis.h"
#include "TLorentzVector.h"
#include "RooGlobalFunc.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include <vector>
#include <assert.h>
#include <TMVA/Reader.h>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <cassert>
#include <sstream>
#include <string>
#include "TFileCollection.h"
#include "THashList.h"
#include "TBenchmark.h"
#include "TLegend.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TColor.h"
#include "TLine.h"
#include "TLatex.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TGraphAsymmErrors.h"
#include "TKey.h"
#include "THStack.h"
#include "TPaveLabel.h"


void computeChi2(string biasList, string dataHisto, string runPeriod = "", bool inclusive = false, string region = "", FILE* fOut = NULL){
    
  gStyle->SetOptStat("e");
  gStyle->SetStatX(0.899514);
  gStyle->SetStatY(0.901);
  gStyle->SetStatW(0.3); 
  gStyle->SetStatH(0.25);

  TFileCollection fc("FileCollection", "FileCollection", biasList.c_str());
  int nBias = fc.GetNFiles();

  double chi2[nBias];
  double bias[nBias];
  double minBias = -0.8, maxBias = 0.8, stepBias = 0.01;
  int kBias = 0;

  for(int i = 0; i < nBias; i++){
    chi2[i] = 0;
    bias[i] = minBias + stepBias*i;
  }
  //Rebinning
  int rebinning;
  float prefitRange = 0.2;
  int idx;
  if(!inclusive){
    //int rebinning_array[18] = {5,5,4,4,4,4,4,4,4,4,4,4,4,4,4,7,4,5}; // For UL18
    //int rebinning_array[18] = {4,4,6,3,2,2,4,4,4,4,4,4,2,3,3,5,4,4}; // For UL17
    //int rebinning_array[18] = {6,4,4,3,3,3,3,3,3,3,3,4,3,3,3,5,6,4}; // For UL16 preVFP
    //int rebinning_array[18] = {4,6,5,4,4,4,4,4,4,4,4,4,3,3,3,5,6,5}; // For UL16 postVFP
    /* Run 3 */
    //int rebinning_array[18] = {6,6,6, 6,7,8, 4,5,4, 6,4,4, 4,6,5, 6,6,5}; // For 2022preEE
    //int rebinning_array[18] = {6,6,6, 4,8,4, 4,4,4, 4,4,4, 5,5,4, 6,6,6}; // For 2022postEE
    int rebinning_array[18] = {5,8,5, 4,6,10, 4,4,5, 4,5,4, 4,6,4, 10,6,5}; // For 2022E
    //int rebinning_array[18] = {6,4,6, 4,4,4, 3,6,4, 4,3,4, 5,4,4, 6,5,5}; // For 2023preBPix
    //int rebinning_array[18] = {10,10,10, 5,5,10, 4,4,4, 4,4,4, 8,4,8, 8,6,5}; // For 2023postBPix

    idx = std::stoi(region);
    rebinning = rebinning_array[idx];

    //float prefitting_array[18] = {0.2,0.2,0.2, 0.2,0.2,0.3, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2}; // For 2022preEE
    float prefitting_array[18] = {0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2}; // For 2022postEE
    //float prefitting_array[18] = {0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.15,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2}; // For 2023preBPix
    //float prefitting_array[18] = {0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.2,0.2,0.2, 0.1,0.2,0.2, 0.2,0.2,0.2}; // For 2023postBPix
    prefitRange = prefitting_array[idx];
  }

  // Open Data Histogram
  TFile *dataF = TFile::Open(dataHisto.c_str());
  /* Run 2 */
  //TH1D* Data = (TH1D*) dataF->Get("histograms/DataUL18"); // For UL18 Corrected
  //TH1D* Data = (TH1D*) dataF->Get("histograms/DataUL18_BAD"); // For UL18 BAD
  //TH1D* Data = (TH1D*) dataF->Get("histograms/DataUL17"); // For UL17
  //TH1D* Data = (TH1D*) dataF->Get(("histograms/DataUL16" + runPeriod).c_str()); // For UL16
  /* Run 3 */
  TH1D* Data = (TH1D*) dataF->Get("histograms/Data2022"); // For 2022
  //TH1D* Data = (TH1D*) dataF->Get("histograms/Data2023"); // For 2023

  //Rebinning
  if(!inclusive)
    Data = (TH1D*) Data->Rebin(rebinning);
  else
    Data = (TH1D*) Data->Rebin(3);
  /* //To avoid error=0 for manual Chi2?
  int ndBins = Data->GetNbinsX();
  double nData[ndBins];
  double errData[ndBins];

  for(int iBin = 0; iBin < ndBins; iBin++){
    nData[iBin] = Data->GetBinContent(iBin+1);
    if(Data->GetBinError(iBin+1) != 0)
      errData[iBin] = Data->GetBinError(iBin+1);
    else
      errData[iBin] = 1;
    cout << errData[iBin] << endl;
  }
  */

  string biasH;
  ifstream biasHistoList(biasList.c_str());
  if (!biasHistoList.is_open()) {
    cout << "File with bias histograms is incorrect!" <<endl;
    return 0;
  }
  while ( getline(biasHistoList, biasH) ){
    
    TFile *f = TFile::Open(biasH.c_str());
    TH1D* bkg = (TH1D*) f->Get("histograms/background");
    //Rebinning
    if(!inclusive)
      bkg = (TH1D*) bkg->Rebin(rebinning);
    else
      bkg = (TH1D*) bkg->Rebin(3);
    
    int nBins = bkg->GetNbinsX();

    /*** For Manual Likelihood - Chi2 ***/ /*
    double nBckg[nBins];
    double errBckg[nBins];

    //Pruebas:
    const Double_t* bkg_binning = (bkg->GetXaxis()->GetXbins())->GetArray();
    TH1D* bkg_smooth = new TH1D("","",bkg->GetNbinsX(),bkg_binning);
    double errThresh = 3.0; // 3
    
    for(int iBin = 0; iBin < nBins; iBin++){

      nBckg[iBin] = bkg->GetBinContent(iBin+1);
      errBckg[iBin] = bkg->GetBinError(iBin+1);

      //if(bkg->GetBinError(iBin+1) != 0) // For MC errors
        //chi2[kBias] += (nData[iBin] - nBckg[iBin])*(nData[iBin] - nBckg[iBin])/(errBckg[iBin] * errBckg[iBin]); // For MC errors
      //else
        //chi2[kBias] += (nData[iBin] - nBckg[iBin])*(nData[iBin] - nBckg[iBin]);
      //chi2[kBias] += (nData[iBin] - nBckg[iBin])*(nData[iBin] - nBckg[iBin])/(errData[iBin] * errData[iBin]); // For Data errors


      /// Background Smooth ///
      if(nBckg[iBin]/errBckg[iBin] < errThresh){
					   
	if(iBin == 0){
	  if(bkg->GetBinContent(iBin+2)/bkg->GetBinError(iBin+2) < errThresh){
	    if(bkg->GetBinContent(iBin+3)/bkg->GetBinError(iBin+3) < errThresh){
	      if(bkg->GetBinContent(iBin+4)/bkg->GetBinError(iBin+4) < errThresh){
		if(bkg->GetBinContent(iBin+5)/bkg->GetBinError(iBin+5) < errThresh){
		  if(bkg->GetBinContent(iBin+6)/bkg->GetBinError(iBin+6) < errThresh){
		    continue;
		  } else {
		    nBckg[iBin] = bkg->GetBinContent(iBin+6);
		    errBckg[iBin] = bkg->GetBinError(iBin+6);
		  }
		} else {
		  nBckg[iBin] = bkg->GetBinContent(iBin+5);
		  errBckg[iBin] = bkg->GetBinError(iBin+5);
		}
	      } else {
		nBckg[iBin] = bkg->GetBinContent(iBin+4);
		errBckg[iBin] = bkg->GetBinError(iBin+4);
	      }
	    } else {
	      nBckg[iBin] = bkg->GetBinContent(iBin+3);
	      errBckg[iBin] = bkg->GetBinError(iBin+3);
	    }
	  } else {
	    nBckg[iBin] = bkg->GetBinContent(iBin+2);
	    errBckg[iBin] = bkg->GetBinError(iBin+2);
	  }
	}
	   			     
	else if(iBin == nBins-1){
	  nBckg[iBin] = nBckg[iBin-1];
	  errBckg[iBin] = errBckg[iBin-1];
	} else{
	  if(nBckg[iBin-1]/errBckg[iBin-1] > errThresh && bkg->GetBinContent(iBin+2)/bkg->GetBinError(iBin+2) > errThresh){
	    nBckg[iBin] = (nBckg[iBin-1] + bkg->GetBinContent(iBin+2))/errThresh;
	    errBckg[iBin] = (errBckg[iBin-1] + bkg->GetBinError(iBin+2))/errThresh;
	  } else if(nBckg[iBin-1]/errBckg[iBin-1] > errThresh && bkg->GetBinContent(iBin+2)/bkg->GetBinError(iBin+2) < errThresh){
	    nBckg[iBin] = nBckg[iBin-1];
	    errBckg[iBin] = errBckg[iBin-1];
	  } else if(nBckg[iBin-1]/errBckg[iBin-1] < errThresh && bkg->GetBinContent(iBin+2)/bkg->GetBinError(iBin+2) > errThresh){
	    nBckg[iBin] = bkg->GetBinContent(iBin+2);
	    errBckg[iBin] = bkg->GetBinError(iBin+2);
	  } else continue;
	}
      }
      if(kBias == 80) cout <<"Data: "<<nBckg[iBin]<<"  Error: "<<errBckg[iBin]<<"  Ratio: "<<nBckg[iBin]/errBckg[iBin]<< endl;

      //chi2[kBias] += nBckg[iBin] - nData[iBin]*log(nBckg[iBin]); // Poisson
      //chi2[kBias] += (nData[iBin] - nBckg[iBin])*(nData[iBin] - nBckg[iBin])/(errBckg[iBin] * errBckg[iBin]);
      //chi2[kBias] += (nData[iBin] - nBckg[iBin])*(nData[iBin] - nBckg[iBin])/(errData[iBin] * errData[iBin]);

      //Prueba:
      bkg_smooth->SetBinContent(iBin+1, nBckg[iBin]);
      bkg_smooth->SetBinError(iBin+1, errBckg[iBin]);

    } // Loop over Histogram bins to compute Chi2

    //Prueba:
    chi2[kBias] = Data->Chi2Test(bkg_smooth, "UW,CHI2");
					       
					   */
    /*** For Chi2 Using ROOT Function ***/ 
    Double_t residuals[nBins];
    chi2[kBias] = Data->Chi2Test(bkg, "UW,CHI2", residuals);
				   	  					   
    kBias++;
    f->Close();

    //cout<<"File #: "<<kBias<<endl;

  } // Loop over Bias Histograms

  biasHistoList.close();
  dataF->Close();
  
  for(int b=0; b<nBias; b++){
    cout << "Bias: "<< bias[b] << "  Chi2: "<< chi2[b] << endl;
    //Prueba 2: smoothing chi2 distribution ==> No funciona
    /*
    if(b == 0 || b == nBias-1) continue;
    else {
      if (fabs(chi2[b] - chi2[b-1]) > 2.5) {
        chi2[b] = (chi2[b-1] + chi2[b+1])/2.0;
      }
    }
    */
  }

  //// Draw Chi2 Plot ////
  TCanvas* c2 = new TCanvas();                                                                                                                       
  TGraph* gr = new TGraph(nBias,bias,chi2);


  //// Pre-Fit to Pol6 ////
  double chi2Min = 999999;
  double biasAtMin = 0;
  for(int i = 0; i < nBias; i++){
    if(chi2[i] < chi2Min){
      chi2Min = chi2[i];
      biasAtMin = bias[i];
    }
  }
  cout <<"Minimum chi2: "<< chi2Min<<" at bias = "<<biasAtMin << endl;
  TF1 *myprefit = new TF1("myprefit","pol6", biasAtMin-prefitRange, biasAtMin+prefitRange); // preEE +-0.3, postEE +-0.1
  gr->Fit("myprefit", "R");
  myprefit->SetLineColor(4);

  float getPreBias = myprefit->GetMinimumX();
  float getPreBiasChi2 = myprefit->Eval(myprefit->GetMinimumX());
  cout <<"Pre-Bias: "<< getPreBias << " // Chi2:" << getPreBiasChi2<< endl;
  float preErrorThresh = getPreBiasChi2 + 1;
  float getBiasErrorLow = 0.;
  float getBiasErrorUp = 0.;
  //Lower Error
  for (float band=biasAtMin-prefitRange; band < biasAtMin+prefitRange; band = band+0.0001){   
    if (myprefit->Eval(band) - preErrorThresh < 0.){   
      getBiasErrorLow = band;
      break;
    }
  }
  //Upper Error
  for (float band=biasAtMin+prefitRange; band > biasAtMin-prefitRange; band = band-0.0001){
    if (myprefit->Eval(band) - preErrorThresh < 0.){
      getBiasErrorUp = band;
      break;
    }
  }
  float preBias = getPreBias;
  float preBiasErrorLow = fabs(getBiasErrorLow - getPreBias);
  float preBiasErrorUp = fabs(getBiasErrorUp - getPreBias);
  cout <<"Pre-Error Low: "<< preBiasErrorLow << " // Pre-Error Up:" << preBiasErrorUp << endl;

  //// Final Fit to Pol2 ////
  TF1 *myfit = new TF1("myfit","pol2", preBias - 3*preBiasErrorLow, preBias + 3*preBiasErrorUp);
  gr->Fit("myfit", "R");
  myfit->SetLineColor(2);

  getPreBias = myfit->GetMinimumX();
  getPreBiasChi2 = myfit->Eval(myfit->GetMinimumX());
  preErrorThresh = getPreBiasChi2 + 1.;
  //Lower
  for (float band=preBias-3*preBiasErrorLow; band < preBias+3*preBiasErrorUp; band = band+0.0001){
    if (myfit->Eval(band) - preErrorThresh < 0.){
      getBiasErrorLow= band;
      break;
    }
  }
  //Upper
  for (float band=preBias+3*preBiasErrorUp; band > preBias-3*preBiasErrorLow; band = band-0.0001){
    if (myfit->Eval(band) - preErrorThresh < 0.){
      getBiasErrorUp = band;
      break;
    }
  }
  float Bias = getPreBias;
  float biasChi2 = myfit->Eval(myfit->GetMinimumX());
  float BiasErrorLow = fabs(getBiasErrorLow - getPreBias);
  float BiasErrorUp = fabs(getBiasErrorUp - getPreBias);

  cout <<"chi2 at minimum: "<< biasChi2 << endl;
  cout <<"Final Bias: "<< Bias <<" ==> Error Low: "<< BiasErrorLow << " // Error Up:" << BiasErrorUp << endl;

  //// Draw Graph ////

  int upperRange = (int) myfit->Eval(myfit->GetMinimumX())*5;
  TH2F * thegrh = new TH2F("", "", nBias,  minBias, maxBias, 1, 0, upperRange);
  thegrh->SetStats(kFALSE);
  thegrh->GetXaxis()->SetTitle("#kappa_{bias}  [TeV^{-1}]");
  thegrh->GetYaxis()->SetTitle("#chi^{2}");
  thegrh->GetYaxis()->SetTitleSize(0.05);
  thegrh->GetYaxis()->SetTitleOffset(1);
  thegrh->Draw(); 

  //gr->SetMaximum(chi2[50]); //60
  //gr->SetTitle("");
  //gr->GetXaxis()->SetTitle("#kappa_{bias}  (TeV^{-1})");
  //gr->GetYaxis()->SetTitle("#chi^{2}");
  gr->SetMarkerStyle(20);
  gr->SetMarkerSize(0.75);
  gr->Draw("P");
  myprefit->SetLineColor(4);
  myprefit->Draw("same");
  myfit->Draw("same");

  TLegend * leg = new TLegend(0.58, 0.66, 0.92, 0.89); // La que uso
  //leg->SetBorderSize(0);
  //leg->SetFillStyle(0);
  leg->SetTextSize(0.03);
  leg->AddEntry(gr, "#chi^{2}" , "p");
  leg->AddEntry(myprefit, "pol6 fit", "l");
  leg->AddEntry((TObject*)0,Form("PreFit: #kappa_{b} = %.3f^{-%.3f}_{+%.3f} TeV^{-1} ", preBias, preBiasErrorLow, preBiasErrorUp), ""); 
  leg->AddEntry(myfit, "pol2 fit", "l");
  leg->AddEntry((TObject*)0,Form("#kappa_{b} = %.3f^{-%.3f}_{+%.3f} TeV^{-1} ", Bias, BiasErrorLow, BiasErrorUp), ""); 
  leg->Draw();

  TString title;
  /* Run 2 */
  //title = "#bf{CMS}                                                   2018, 59.7 fb^{-1} (13 TeV)"; // v1
  //title = "#bf{CMS} #it{Work in progress}                         2018, 59.7 fb^{-1} (13 TeV)"; // UL18
  //title = "#bf{CMS} #it{Work in progress}                         2017, 41.5 fb^{-1} (13 TeV)"; // UL17
  //title = "#bf{CMS} #it{Work in progress}                  2016 preVFP, 19.5 fb^{-1} (13 TeV)"; // UL16 preVFP
  //title = "#bf{CMS} #it{Work in progress}                 2016 postVFP, 16.8 fb^{-1} (13 TeV)"; // UL16 postVFP
  /* Run 3 */
  //title = "#bf{CMS} #it{Work in progress}                  2022 preEE, 8.0 fb^{-1} (13.6 TeV)"; // 2022preEE
  //title = "#bf{CMS} #it{Work in progress}                2022 postEE, 26.7 fb^{-1} (13.6 TeV)"; // 2022postEE
  title = "#bf{CMS} #it{Work in progress}                      2022 E, 5.8 fb^{-1} (13.6 TeV)"; // 2022E
  //title = "#bf{CMS} #it{Work in progress}               2023 preBPix, 17.7 fb^{-1} (13.6 TeV)"; // 2023preBPix
  //title = "#bf{CMS} #it{Work in progress}               2023 postBPix, 9.5 fb^{-1} (13.6 TeV)"; // 2023postBPix

  TLatex* preliminary = new TLatex(0.11,0.92, title);
  preliminary->SetNDC();
  preliminary->SetTextFont(42);
  preliminary->SetTextSize(0.045);
  preliminary->Draw();

  if(inclusive){
    TPaveLabel *label = new TPaveLabel(0.12,0.75,0.32,0.84,"p_{T} > 200 GeV","NDC");
    label->SetBorderSize(0);
    label->SetFillColor(0);
    label->SetFillStyle(0);
    label->SetTextSize(0.37);
    label->Draw();
  }
  else {
    TString subtitle1[18] = {"p_{T} > 110 GeV","p_{T} > 110 GeV","p_{T} > 110 GeV","p_{T} > 200 GeV","p_{T} > 200 GeV","p_{T} > 200 GeV","p_{T} > 200 GeV","p_{T} > 200 GeV","p_{T} > 200 GeV","p_{T} > 200 GeV","p_{T} > 200 GeV","p_{T} > 200 GeV","p_{T} > 200 GeV","p_{T} > 200 GeV","p_{T} > 200 GeV","p_{T} > 110 GeV","p_{T} > 110 GeV","p_{T} > 110 GeV"};
    TString subtitle2[18] = {"-2.4 < #eta < -2.1","-2.4 < #eta < -2.1","-2.4 < #eta < -2.1","-2.1 < #eta < -1.2","-2.1 < #eta < -1.2","-2.1 < #eta < -1.2","-1.2 < #eta < 0","-1.2 < #eta < 0","-1.2 < #eta < 0","0 < #eta < 1.2","0 < #eta < 1.2","0 < #eta < 1.2","1.2 < #eta < 2.1","1.2 < #eta < 2.1","1.2 < #eta < 2.1","2.1 < #eta < 2.4","2.1 < #eta < 2.4","2.1 < #eta < 2.4"};
    TString subtitle3[18] = {"-180#circ < #phi < -60#circ","-60#circ < #phi < 60#circ","60#circ < #phi < 180#circ","-180#circ < #phi < -60#circ","-60#circ < #phi < 60#circ","60#circ < #phi < 180#circ","-180#circ < #phi < -60#circ","-60#circ < #phi < 60#circ","60#circ < #phi < 180#circ","-180#circ < #phi < -60#circ","-60#circ < #phi < 60#circ","60#circ < #phi < 180#circ","-180#circ < #phi < -60#circ","-60#circ < #phi < 60#circ","60#circ < #phi < 180#circ","-180#circ < #phi < -60#circ","-60#circ < #phi < 60#circ","60#circ < #phi < 180#circ"};

    TPaveLabel *label1 = new TPaveLabel(0.12,0.75,0.32,0.84,subtitle1[idx],"NDC");
    label1->SetBorderSize(0);
    label1->SetFillColor(0);
    label1->SetFillStyle(0);
    label1->SetTextSize(0.37);
    label1->Draw();

    TPaveLabel *label2 = new TPaveLabel(0.12,0.69,0.32,0.78,subtitle2[idx],"NDC");
    label2->SetBorderSize(0);
    label2->SetFillColor(0);
    label2->SetFillStyle(0);
    label2->SetTextSize(0.37);
    label2->Draw();

    TPaveLabel *label3 = new TPaveLabel(0.12,0.63,0.32,0.72,subtitle3[idx],"NDC");
    label3->SetBorderSize(0);
    label3->SetFillColor(0);
    label3->SetFillStyle(0);
    label3->SetTextSize(0.37);
    label3->Draw();
  }

  /// Save inclusive plots
  if(inclusive){
    /* Run 2 */
    //c2->SaveAs("png/chi2/chi2_UL18_ptZbinned.png"); // UL18
    //c2->SaveAs("png/chi2/chi2_UL18_ptZbinned.root");
    //c2->SaveAs("png/chi2/chi2_UL18_ptZbinned.pdf");
    //c2->SaveAs("png/chi2/chi2_UL17_ptZbinned.png"); // UL17
    //c2->SaveAs("png/chi2/chi2_UL17_ptZbinned.root");
    //c2->SaveAs("png/chi2/chi2_UL17_ptZbinned.pdf");
    //c2->SaveAs(("png/chi2/chi2_UL16" + runPeriod + "_ptZreweight.png").c_str()); // UL16
    //c2->SaveAs(("png/chi2/chi2_UL16" + runPeriod + "_ptZreweight.root").c_str());
    //c2->SaveAs(("png/chi2/chi2_UL16" + runPeriod + "_ptZreweight.pdf").c_str());
    /* Run 3 */
    //c2->SaveAs(("png/chi2/chi2_2022" + runPeriod + "_inclusive.png").c_str()); // 2022
    //c2->SaveAs(("png/chi2/chi2_2022" + runPeriod + "_inclusive.root").c_str());
    //c2->SaveAs(("png/chi2/chi2_2022" + runPeriod + "_inclusive.pdf").c_str());
    c2->SaveAs(("png/chi2/chi2_2023" + runPeriod + "_inclusive.png").c_str()); // 2023
    c2->SaveAs(("png/chi2/chi2_2023" + runPeriod + "_inclusive.root").c_str());
    c2->SaveAs(("png/chi2/chi2_2023" + runPeriod + "_inclusive.pdf").c_str());
  }
  /// Save bias map plots
  else {
    /* Run 2 */
    //c2->SaveAs(("png/chi2/UL18/chi2_"+ region +"_UL18.png").c_str()); // UL18
    //c2->SaveAs(("png/chi2/UL18/chi2_"+ region +"_UL18.root").c_str());
    //c2->SaveAs(("png/chi2/UL18/chi2_"+ region +"_UL18.pdf").c_str());
    //c2->SaveAs(("png/chi2/UL17/chi2_"+ region +"_UL17.png").c_str()); // UL17
    //c2->SaveAs(("png/chi2/UL17/chi2_"+ region +"_UL17.root").c_str());
    //c2->SaveAs(("png/chi2/UL17/chi2_"+ region +"_UL17.pdf").c_str());
    //c2->SaveAs(("png/chi2/UL16postVFP/chi2_"+ region +"_UL16"+ runPeriod +".png").c_str()); // UL16
    //c2->SaveAs(("png/chi2/UL16postVFP/chi2_"+ region +"_UL16"+ runPeriod +".root").c_str());
    //c2->SaveAs(("png/chi2/UL16postVFP/chi2_"+ region +"_UL16"+ runPeriod +".pdf").c_str());
    /* Run 3 */
    c2->SaveAs(("png/chi2/2022"+ runPeriod +"/chi2_"+ region +"_2022"+ runPeriod +".png").c_str()); // 2022
    c2->SaveAs(("png/chi2/2022"+ runPeriod +"/chi2_"+ region +"_2022"+ runPeriod +".root").c_str());
    c2->SaveAs(("png/chi2/2022"+ runPeriod +"/chi2_"+ region +"_2022"+ runPeriod +".pdf").c_str());
    //c2->SaveAs(("png/chi2/2023"+ runPeriod +"/chi2_"+ region +"_2023"+ runPeriod +".png").c_str()); // 2023
    //c2->SaveAs(("png/chi2/2023"+ runPeriod +"/chi2_"+ region +"_2023"+ runPeriod +".root").c_str());
    //c2->SaveAs(("png/chi2/2023"+ runPeriod +"/chi2_"+ region +"_2023"+ runPeriod +".pdf").c_str());
  
    /// Save bias map results in a txt file
    fprintf(fOut, "%s %f %f \n", region.c_str(), Bias, BiasErrorLow);
  }

}

void chi2Plot(){
  /*** For Inclusive Bias Plots ***/
  //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/nanoaod_base_analysis/bin/txt/chi2Histos_UL17_Mz200.txt", "/eos/user/d/diegof/cmt/FeaturePlot/UL17_config/cat_preselection_UL17/biasHistos_Mz200/root/kappa_0.0__pg_UL17.root", "", ""); // For UL17 Mz>200

  //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/nanoaod_base_analysis/bin/txt/UL18/chi2Map_0_UL18.txt", "/eos/user/d/diegof/cmt/FeaturePlot/GEMethod_config/cat_preselection_UL18/biasMap_UL18/root/kappa_0_0.0__pg_UL18_corrected.root", "", "");
  //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/nanoaod_base_analysis/bin/txt/prueba_kappa9.txt", "/eos/user/d/diegof/cmt/FeaturePlot/GEMethod_config/cat_preselection_UL18/biasScan_0_kappa9_data/root/kappa_0_0.0__pg_UL18_corrected.root", "", "");

  /* Run 2 */
  //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/nanoaod_base_analysis/bin/txt/chi2Histos_UL18_ptZreweight.txt", "/eos/user/d/diegof/cmt/FeaturePlot/GEMethod_config/cat_preselection_UL18/UL18corr_ptZreweight/root/kappa__pg_UL18_corrected.root", "", ""); // For UL18 Corrected
  //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/nanoaod_base_analysis/bin/txt/chi2Histos_UL17_ptZreweight.txt", "/eos/user/d/diegof/cmt/FeaturePlot/UL17_config/cat_preselection_UL17/UL17_ptZreweight/root/kappa__pg_UL17.root", "", ""); // For UL17
  //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/nanoaod_base_analysis/bin/txt/chi2Histos_UL16preVFP_ptZreweight.txt", "/eos/user/d/diegof/cmt/FeaturePlot/UL16_config/cat_preselection_UL16/preVFP_FINAL/root/kappa__pg_UL16_preVFP.root", "_preVFP", ""); // For UL16 preVFP
  //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/nanoaod_base_analysis/bin/txt/chi2Histos_UL16postVFP_ptZreweight.txt", "/eos/user/d/diegof/cmt/FeaturePlot/UL16_config/cat_preselection_UL16/postVFP_FINAL/root/kappa__pg_UL16_postVFP.root", "_postVFP", ""); // For UL16 postVFP

  /* Run 3 */
  //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/inclusiveBias_2022preEE.txt", "/eos/user/d/diegof/cmt/FeaturePlot/GE2022_config/cat_preselection_2022/biasHistos_2022preEE/root/kappa_0.0__pg_2022_preEE.root", "_preEE", true); // For 2022preEE
  //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/inclusiveBias_2022postEE.txt", "/eos/user/d/diegof/cmt/FeaturePlot/GE2022_config/cat_preselection_2022/biasHistos_2022postEE/root/kappa_0.0__pg_2022_postEE.root", "_postEE", true); // For 2022postEE

  //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/inclusiveBias_2023preBPix.txt", "/eos/user/d/diegof/cmt/FeaturePlot/GE2023_config/cat_preselection_2023/inclusiveBias_preBPix/root/kappa_0.0__pg_2023_full.root", "_preBPix", true); // For 2023preBPix
  //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/inclusiveBias_2023postBPix.txt", "/eos/user/d/diegof/cmt/FeaturePlot/GE2023_config/cat_preselection_2023/inclusiveBias_postBPix/root/kappa_0.0__pg_2023_full.root", "_postBPix", true); // For 2023preBPix

  /* For Scale Maps */
  
  // Write output to txt
  FILE* fOut;
  //fOut = fopen("outBias/UL18/ScaleMap_results_UL18.txt","w+");
  //fOut = fopen("outBias/UL17/ScaleMap_results_UL17.txt","w+");
  //fOut = fopen("outBias/UL16preVFP/ScaleMap_results_UL16preVFP.txt","w+");
  //fOut = fopen("outBias/UL16postVFP/ScaleMap_results_UL16postVFP.txt","w+");
  /// Run 3 ///
  //fOut = fopen("outBias/2022preEE/ScaleMap_results_2022preEE.txt","w+"); // 2022preEE
  //fOut = fopen("outBias/2022postEE/ScaleMap_results_2022postEE.txt","w+"); // 2022postEE
  fOut = fopen("outBias/2022postEE/ScaleMap_results_2022E.txt","w+"); // 2022E
  //fOut = fopen("outBias/2023preBPix/ScaleMap_results_2023preBPix.txt","w+"); // 2023preBPix
  //fOut = fopen("outBias/2023postBPix/ScaleMap_results_2023postBPix.txt","w+"); // 2023postBPix

  for (int i=0; i<18; i++){ 
    std::string region = std::to_string(i);
    //cout << "/afs/cern.ch/user/d/diegof/Wprime/nanoaod_base_analysis/bin/txt/UL18/chi2Map_"+ region +"_UL18.txt" << endl;
    //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/nanoaod_base_analysis/bin/txt/UL18/chi2Map_"+ region +"_UL18.txt", "/eos/user/d/diegof/cmt/FeaturePlot/GEMethod_config/cat_preselection_UL18/biasMap_UL18_GOOD/root/kappa_"+ region +"_0.0__pg_UL18_corrected.root", "", region, fOut); // UL18
    //cout << "/afs/cern.ch/user/d/diegof/Wprime/nanoaod_base_analysis/bin/txt/UL17/chi2Map_"+ region +"_UL17.txt" << endl;
    //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/nanoaod_base_analysis/bin/txt/UL17/chi2Map_"+ region +"_UL17.txt", "/eos/user/d/diegof/cmt/FeaturePlot/UL17_config/cat_preselection_UL17/biasMap_UL17_GOOD/root/kappa_"+ region +"_0.0__pg_UL17.root", "", region, fOut); // UL17
    //cout << "/afs/cern.ch/user/d/diegof/Wprime/nanoaod_base_analysis/bin/txt/UL16preVFP/chi2Map_"+ region +"_UL16preVFP.txt" << endl;
    //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/nanoaod_base_analysis/bin/txt/UL16preVFP/chi2Map_"+ region +"_UL16preVFP.txt", "/eos/user/d/diegof/cmt/FeaturePlot/UL16_config/cat_preselection_UL16/biasMap_UL16preVFP_GOOD/root/kappa_"+ region +"_0.0__pg_UL16_preVFP.root", "_preVFP", region, fOut); // UL16 preVFP
    //cout << "/afs/cern.ch/user/d/diegof/Wprime/nanoaod_base_analysis/bin/txt/UL16postVFP/chi2Map_"+ region +"_UL16postVFP.txt" << endl;
    //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/nanoaod_base_analysis/bin/txt/UL16postVFP/chi2Map_"+ region +"_UL16postVFP.txt", "/eos/user/d/diegof/cmt/FeaturePlot/UL16_config/cat_preselection_UL16/biasMap_UL16postVFP_GOOD/root/kappa_"+ region +"_0.0__pg_UL16_postVFP.root", "_postVFP", region, fOut); // UL16 postVFP
    /// Run 3 ///
    //cout << "/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/2022preEE/chi2Map_"+ region +"_2022preEE.txt" << endl;
    //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/2022preEE/chi2Map_"+ region +"_2022preEE.txt", "/eos/user/d/diegof/cmt/FeaturePlot/GE2022_config/cat_preselection_2022/biasMap_preEE_ciemat/root/kappa_"+ region +"_0.0__pg_2022_full.root", "_preEE", false, region, fOut); // 2022preEE
    //cout << "/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/2022postEE/chi2Map_"+ region +"_2022postEE.txt" << endl;
    //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/2022postEE/chi2Map_"+ region +"_2022postEE.txt", "/eos/user/d/diegof/cmt/FeaturePlot/GE2022_config/cat_preselection_2022/biasMap_postEE_ciemat/root/kappa_"+ region +"_0.0__pg_2022_full.root", "_postEE", false, region, fOut); // 2022postEE
    // Checks 2022 //
    cout << "/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/2022checks/2022E/chi2Map_"+ region +"_2022E.txt" << endl;
    computeChi2("/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/2022checks/2022E/chi2Map_"+ region +"_2022E.txt", "/eos/user/d/diegof/cmt/FeaturePlot/GE2022_config/cat_preselection_2022/biasMap_2022E/root/kappa_"+ region +"_0.0__pg_2022_full.root", "E", false, region, fOut); // 2022E

    //cout << "/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/2023preBPix/chi2Map_"+ region +"_2023preBPix.txt" << endl;
    //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/2023preBPix/chi2Map_"+ region +"_2023preBPix.txt", "/eos/user/d/diegof/cmt/FeaturePlot/GE2023_config/cat_preselection_2023/biasMap_preBPix/root/kappa_"+ region +"_0.0__pg_2023_full.root", "_preBPix", false, region, fOut); // 2023preBPix
    //cout << "/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/2023postBPix/chi2Map_"+ region +"_2023postBPix.txt" << endl;
    //computeChi2("/afs/cern.ch/user/d/diegof/Wprime/GE-method/bin/txt/2023postBPix/chi2Map_"+ region +"_2023postBPix.txt", "/eos/user/d/diegof/cmt/FeaturePlot/GE2023_config/cat_preselection_2023/biasMap_postBPix/root/kappa_"+ region +"_0.0__pg_2023_full.root", "_postBPix", false, region, fOut); // 2023postBPix
  }

  fclose(fOut);

}
