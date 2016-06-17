clc;clear;

%%%Get point which procures the best fit
load('paramCompare.mat')

%%%Establish constants
%Load data
[kd, tnpbsa4, tnpbsa26, mfiAdjMean4, mfiAdjMean26, kdBruhns, ~, ~, best] = loadData;
%Valencies and TNP-X-BSA molarities
v = [4;26];
tnpbsa = [tnpbsa4;tnpbsa26];
%Create matrix of binomial coefficients
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

%%%Do MHC
start = best;
%See hmc.m documentation to see why options vector was chosen in these
%ways.
options = [1,0,0,0,0,0,20,0,1,0,0,0,0,100,0,0,1,1/20];
[samples,energies,diag] = hmc(@(x) 191*log(Error(x,kdBruhns,mfiAdjMean4, ...
    mfiAdjMean26, v, biCoefMat, tnpbsa)/191)*2*(9*(9+1))/(191-9-1), ... 
    start,options,@(x) gradest(@(y)Error(y,kdBruhns,mfiAdjMean4,mfiAdjMean26,v,biCoefMat,tnpbsa),x));
