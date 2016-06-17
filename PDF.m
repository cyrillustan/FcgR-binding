function [prob] = pdf(x, kd, mfiAdjMean4, mfiAdjMean26, v, biCoefMat, tnpbsa)
    %Find residuals for the model granted current parameters
    sse = Error(x',kd,mfiAdjMean4,mfiAdjMean26,v,biCoefMat,tnpbsa);
    %Estimate AICc for the model granted current parameters (see
    %http://theses.ulaval.ca/archimede/fichiers/21842/apa.html
    
    AICc = 191*log(log(sse/191))+180/181;
%     AICc = 191*log(sse/191)+180/181;
    prob = exp(-AICc/2);
end