clear;clc;

%Load best fit from normalizing the data by CHO line, not assuming
%receptor expression is equal
load('paramCompare.mat')

%Loading basic parameters
[kd, tnpbsa4, tnpbsa26, mfiAdjMean4, mfiAdjMean26, kdBruhns] = loadData;

%Set valencies
v = [4;26];
%Create vector of TNP-BSA molarities
tnpbsa = [tnpbsa4;tnpbsa26];
%Create a matrix of binomial coefficients of the form v!/((v-i)!*i!) for
%all i from 1 to v for all v from 1 to 26
biCoefMat = zeros(26,26);
for j = 1:26
    for k = 1:j
        biCoefMat(k,j) = nchoosek(j,k);
    end
end

%From mfiAdjMean, create matrices which hold the adjusted expression
%level mean and expression level standard deviation for each condition
%(i.e. FcgR with IgG1, valency 4)
mfiAdjMean = [mfiAdjMean4 mfiAdjMean26];
meanPerCond = zeros(24,2);
stdPerCond = zeros(24,2);
for j = 1:24
    for k = 1:2
        meanPerCond(j,k) = nanmean(mfiAdjMean(j,4*(k-1)+1:4*k));
        stdPerCond(j,k) = std(mfiAdjMean(j,4*(k-1)+1:4*k),0,2,'omitnan');
    end
end

%%%Note carefully that start is a row vector that must be transposed to be
%%%put into Error
start = best';
%Number of samples for MCMC
nsamples = 1000000;
%Log probability proposal distribution
proppdf = @(x,y) 0;
%Pseudo-random generator of new points to test
proprnd = @(x) x+normrnd(0,0.1,1,7);
%Probability distribution of interest
pdf = @(x) PDF(x,kdBruhns,mfiAdjMean4,mfiAdjMean26,v,biCoefMat,tnpbsa,meanPerCond,stdPerCond);

%Run Metropolis-Hastings algorithm
[sample,accept] = mhsample(start,nsamples,'logpdf',pdf,'logproppdf',proppdf,'proprnd',proprnd,'symmetric',0);

%Collect the errors for each element in the chain. Also, collect the list
%of all displacements in log space and "standard" space from the best fit
%point. From these displacements, find the distances in log space and in
%standard space.
errors = zeros(nsamples,1);
dispFromBest = zeros(size(sample));
distFromBest = zeros(nsamples,1);
rdispFromBest = zeros(size(sample));
rdistFromBest = zeros(nsamples,1);
for j = 1:nsamples
    errors(j) = Error(sample(j,:)', kdBruhns, mfiAdjMean4, mfiAdjMean26, v, biCoefMat, tnpbsa);
    dispFromBest(j,:) = best' - sample(j,:);
    distFromBest(j) = sqrt(nansum(dispFromBest(j,:).^2));
    rdispFromBest(j,:) = 10.^best' - 10.^sample(j,:);
    rdistFromBest(j) = sqrt(nansum(rdispFromBest(j,:).^2));
end