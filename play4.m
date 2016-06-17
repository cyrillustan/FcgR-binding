clear;clc;

%Load best fit from normalizing the data by CHO line and not treating
%receptor expression as equal
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

%%%Note carefully that start is a row vector that must be transposed to be
%%%put into Error
start = best';
nsamples = 100;
proppdf = @(x,y) PROPPDF(x,y);
proprnd = @(x) PROPRND(x);
pdf = @(x) PDF(x, kdBruhns, mfiAdjMean4, mfiAdjMean26, v, biCoefMat, tnpbsa);

[sample,accept] = mhsample(start,nsamples,'logpdf',pdf,'logproppdf',proppdf,'proprnd',proprnd);

%Collect the errors for each element in the chain
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

save('mcmc2.mat','sample','accept','errors','dispFromBest','distFromBest','rdispFromBest','rdistFromBest')