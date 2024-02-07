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


void DrawMap(string biasMap, string year, string VFP=""){
  
  /// Create TH2 with the Map ///

  Double_t etaBins[7] = {-2.4, -2.1, -1.2, 0, 1.2, 2.1, 2.4};
  Double_t phiBins[4] = {-180, -60, 60, 180};

  TH2D* ScaleMap = new TH2D("", "", 6, etaBins, 3, phiBins);

  std::ifstream outBias(biasMap.c_str());
  if (!outBias.is_open()){
    cout << "File with output bias map is incorrect!" << endl;
    return 0;
  }
  double bias, error;
  int region;

  for(int iEta = 1; iEta <= 6; iEta ++){
    for(int iPhi = 1; iPhi <= 3; iPhi ++){
      outBias >> region >> bias >> error;
      ScaleMap->SetBinContent(iEta, iPhi, bias);
      ScaleMap->SetBinError(iEta, iPhi, error);
    }
  }

  /// Draw Scale Map ///
  
  TCanvas *Map = new TCanvas("ScaleMap","",600,500);
  Map->SetRightMargin(0.2);
  Map->SetFillColor(0);
  Map->SetFillStyle(4000);
  gStyle->SetOptTitle(0);
  gStyle->SetOptStat(0);
  gStyle->SetPaintTextFormat("1.2g");
  Map->cd();

  Int_t colors[11] =  {
    //Positive Overflow.
    TColor::GetColor("#FF0000"), //Reds
    TColor::GetColor("#FE2E2E"), 
    TColor::GetColor("#FA5858"), 
    TColor::GetColor("#F78181"), 
    TColor::GetColor("#F5A9A9"), 
    0, //This is the cero
    TColor::GetColor("#A9E2F3"), //Blues
    TColor::GetColor("#81DAF5"), 
    TColor::GetColor("#58D3F7"),     
    TColor::GetColor("#2ECCFA"), 
    TColor::GetColor("#00BFFF"), 
  };

  Double_t levels[] = {
    -0.81, -0.30, -0.2, -0.15, -0.1, 
    0.1, 0.15, 0.2, 0.30, 0.81
  };
  //Double_t levels[] = {
  //  -0.31, -0.15, -0.1, -0.05, 
  //   0.05, 0.1, 0.15, 0.31
  //};
  gStyle->SetPalette((sizeof(colors)/sizeof(Int_t)), colors);

  ScaleMap->SetContour((sizeof(levels)/sizeof(Double_t)), levels);
  ScaleMap->GetYaxis()->SetTitleOffset(1.1);
  ScaleMap->GetYaxis()->SetTitle("#phi");
  ScaleMap->GetXaxis()->SetTitle("#eta");
  ScaleMap->GetZaxis()->SetRangeUser(-0.81, 0.81); 
  //ScaleMap->GetZaxis()->SetRangeUser(-0.31, 0.31); 
  ScaleMap->SetMarkerSize(1.5);
  ScaleMap->Draw("COLZ");
  ScaleMap->Draw("texte same");

  TString title;
  if (year == "UL18")
    title = "#bf{CMS} #it{Work in progress}                     2018, 59.7 fb^{-1} (13 TeV)";
  else if (year == "UL17")
    title = "#bf{CMS} #it{Work in progress}                     2017, 41.5 fb^{-1} (13 TeV)";
  else if (year == "UL16" && VFP == "preVFP")
    title = "#bf{CMS} #it{Work in progress}              2016 preVFP, 19.5 fb^{-1} (13 TeV)";
  else if (year == "UL16" && VFP == "postVFP")
    title = "#bf{CMS} #it{Work in progress}             2016 postVFP, 16.8 fb^{-1} (13 TeV)";

  else if (year == "2022" && VFP == "preEE")
    title = "#bf{CMS} #it{Work in progress}              2022 preEE, 8.1 fb^{-1} (13.6 TeV)";
  else
    title = "#bf{CMS} #it{Work in progress}            2022 postEE, 27.0 fb^{-1} (13.6 TeV)";


  TLatex* preliminary = new TLatex(0.12,0.92, title);
  preliminary->SetNDC();
  preliminary->SetTextFont(42);
  preliminary->SetTextSize(0.035);
  preliminary->Draw();

  Map->SaveAs(("png/ScaleMap/"+ year + VFP +"/ScaleMap_"+ year + VFP +".png").c_str());
  Map->SaveAs(("png/ScaleMap/"+ year + VFP +"/ScaleMap_"+ year + VFP +".pdf").c_str());
  Map->SaveAs(("png/ScaleMap/"+ year + VFP +"/ScaleMap_"+ year + VFP +".root").c_str());
  
}

void DrawProfile(string biasMap, string year, string VFP=""){

  /// Read the map and set profile ///

  Double_t etaBins[7] = {-2.4, -2.1, -1.2, 0, 1.2, 2.1, 2.4};

  std::ifstream outBias(biasMap.c_str());
  if (!outBias.is_open()){
    cout << "File with output bias map is incorrect!" << endl;
    return 0;
  }
  double bias, error;
  int region;
  int idx = 0;

  TGraphErrors* ProfileMapPhi1 = new TGraphErrors(6);
  TGraphErrors* ProfileMapPhi2 = new TGraphErrors(6);
  TGraphErrors* ProfileMapPhi3 = new TGraphErrors(6);

  while(outBias >> region >> bias >> error){
    if(region % 3 == 0){
      ProfileMapPhi1->SetPoint(idx, (etaBins[idx+1] + etaBins[idx])/2.0, bias);
      ProfileMapPhi1->SetPointError(idx, (etaBins[idx+1] - etaBins[idx])/2.0, error);
    }
    else if((region-1) % 3 == 0){
      ProfileMapPhi2->SetPoint(idx, (etaBins[idx+1] + etaBins[idx])/2.0, bias);
      ProfileMapPhi2->SetPointError(idx, (etaBins[idx+1] - etaBins[idx])/2.0, error);
    }
    else if((region-2) % 3 == 0){
      ProfileMapPhi3->SetPoint(idx, (etaBins[idx+1] + etaBins[idx])/2.0, bias);
      ProfileMapPhi3->SetPointError(idx, (etaBins[idx+1] - etaBins[idx])/2.0, error);
      idx ++;
    }
  }

  /// Draw the profile map ///

  TCanvas *Map = new TCanvas("ProfileMap","",600,500);
  gStyle->SetPadRightMargin(1.5);
  gStyle->SetOptTitle(0);
  gStyle->SetOptStat(0);
  Map->SetFillColor(0);
  Map->SetFillStyle(4000);
  Map->cd();

  ProfileMapPhi1->GetXaxis()->SetRangeUser(-2.4,2.4);
  ProfileMapPhi1->SetMaximum(0.8);
  ProfileMapPhi1->SetMinimum(-0.8);
  ProfileMapPhi1->GetXaxis()->SetLabelSize(0.045);
  ProfileMapPhi1->GetYaxis()->SetLabelSize(0.045);
  ProfileMapPhi1->GetXaxis()->SetTitleSize(0.045);
  ProfileMapPhi1->GetYaxis()->SetTitleSize(0.045);
  ProfileMapPhi1->GetYaxis()->SetTitleOffset(1.1);
  ProfileMapPhi1->GetYaxis()->SetTitle("#kappa_{bias}  [TeV^{-1}]");
  ProfileMapPhi1->GetXaxis()->SetTitle("#eta");

  ProfileMapPhi1->SetLineWidth(2);
  ProfileMapPhi1->SetLineColor(1);
  ProfileMapPhi1->SetMarkerStyle(20);
  ProfileMapPhi1->SetMarkerSize(1);
  ProfileMapPhi1->Draw("ap");

  ProfileMapPhi2->SetLineWidth(2);
  ProfileMapPhi2->SetLineColor(2);
  ProfileMapPhi2->SetMarkerColor(2);
  ProfileMapPhi2->SetMarkerStyle(20);
  ProfileMapPhi2->SetMarkerSize(1);
  ProfileMapPhi2->Draw("p same");

  ProfileMapPhi3->SetLineWidth(2);
  ProfileMapPhi3->SetLineColor(4);
  ProfileMapPhi3->SetMarkerColor(4);
  ProfileMapPhi3->SetMarkerStyle(20);
  ProfileMapPhi3->SetMarkerSize(1);
  ProfileMapPhi3->Draw("p same");

  TLegend * leg = new TLegend(0.3, 0.65, 0.7, 0.9);
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetTextSize(0.04);
  leg->AddEntry(ProfileMapPhi1, "-180#circ < #phi < -60#circ"  , "apel");
  leg->AddEntry(ProfileMapPhi2, "-60#circ < #phi < 60#circ"  , "apel");
  leg->AddEntry(ProfileMapPhi3, "60#circ < #phi < 180#circ"  , "apel");
  leg->Draw();

  TString title;
  if (year == "UL18")
    title = "#bf{CMS} #it{Work in progress}                     2018, 59.7 fb^{-1} (13 TeV)";
  else if (year == "UL17")
    title = "#bf{CMS} #it{Work in progress}                     2017, 41.5 fb^{-1} (13 TeV)";
  else if (year == "UL16" && VFP == "preVFP")
    title = "#bf{CMS} #it{Work in progress}              2016 preVFP, 19.5 fb^{-1} (13 TeV)";
  else if (year == "UL16" && VFP == "postVFP")
    title = "#bf{CMS} #it{Work in progress}             2016 postVFP, 16.8 fb^{-1} (13 TeV)";

  else if (year == "2022" && VFP == "preEE")
    title = "#bf{CMS} #it{Work in progress}              2022 preEE, 8.1 fb^{-1} (13.6 TeV)";
  else
    title = "#bf{CMS} #it{Work in progress}            2022 postEE, 27.0 fb^{-1} (13.6 TeV)";

  TLatex* preliminary = new TLatex(0.12,0.92, title);
  preliminary->SetNDC();
  preliminary->SetTextFont(42);
  preliminary->SetTextSize(0.04);
  preliminary->Draw();

  Map->SaveAs(("png/ScaleMap/"+ year + VFP +"/ProfileMap_"+ year + VFP +".png").c_str());
  Map->SaveAs(("png/ScaleMap/"+ year + VFP +"/ProfileMap_"+ year + VFP +".pdf").c_str());
  Map->SaveAs(("png/ScaleMap/"+ year + VFP +"/ProfileMap_"+ year + VFP +".root").c_str());

}

void ScaleMap(){
 
  //DrawMap("outBias/UL18/ScaleMap_results_UL18.txt", "UL18");
  //DrawMap("outBias/UL17/ScaleMap_results_UL17.txt", "UL17");
  //DrawMap("outBias/UL16preVFP/ScaleMap_results_UL16preVFP.txt", "UL16", "preVFP");
  //DrawMap("outBias/UL16postVFP/ScaleMap_results_UL16postVFP.txt", "UL16", "postVFP");

  //DrawMap("outBias/2022preEE/ScaleMap_results_2022preEE.txt", "2022", "preEE");
  DrawMap("outBias/2022postEE/ScaleMap_results_2022postEE.txt", "2022", "postEE");


  //DrawProfile("outBias/UL18/ScaleMap_results_UL18.txt", "UL18");
  //DrawProfile("outBias/UL17/ScaleMap_results_UL17.txt", "UL17");
  //DrawProfile("outBias/UL16preVFP/ScaleMap_results_UL16preVFP.txt", "UL16", "preVFP");
  //DrawProfile("outBias/UL16postVFP/ScaleMap_results_UL16postVFP.txt", "UL16", "postVFP");

  //DrawProfile("outBias/2022preEE/ScaleMap_results_2022preEE.txt", "2022", "preEE");
  DrawProfile("outBias/2022postEE/ScaleMap_results_2022postEE.txt", "2022", "postEE");

}
