%% *DSH Data Visualizer*
% _By: Joshua Cohen_
%start on a fresh template, init variables
clc
close all
clear all
fName = 'dshData.csv';
delim = ',';
startRow = 2;
temps = [];
tTime = [];
humids = [];
hTime = [];
WIDTH = 1300;
HEIGHT = 700;
%gets the size of the screen being used
screenSize = get(0,'ScreenSize');
%sets figure in center of screen
figureCoords = [(screenSize(3)-WIDTH)/2,(screenSize(4)-HEIGHT)/2,WIDTH,HEIGHT];
%create figure and set it's properties
mainFig = figure('Position',figureCoords);

%   column1: text (%s)
%	column2: double (%f)
%   column3: double (%f)
%	column4: text (%s)
%   column5: double (%f)
format = '%s%f%f%s%f%[^\n\r]';
fileID = fopen(fName,'r');
dataArray = textscan(fileID, format, ...
    'Delimiter', delim,...
    'EmptyValue' ,NaN,...
    'HeaderLines' ,startRow-1, ...
    'ReturnOnError', false, ...
    'EndOfLine', '\r\n');
fclose(fileID);

Time = strtok(dataArray{:, 1},'.');
Time = string(Time);
NetworkID = dataArray{:, 2};
NodeID = dataArray{:, 3};
SensorType = dataArray{:, 4};
SensorValue = dataArray{:, 5};
for i = 1:length(SensorType)
if(strcmp(SensorType{i},'TEMPC'))
    temps = [temps, SensorValue(i)];
    tTime = [tTime, Time(i)];
elseif(strcmp(SensorType{i},'HUM'))
    humids = [humids, SensorValue(i)];
    hTime = [hTime, Time(i)];
end
end
tTime = char(tTime);
tTime = squeeze(tTime(1,:,:))';
hTime = char(hTime);
hTime = squeeze(hTime(1,:,:))';

plot(datenum(tTime,31),temps)
datetick('x', 31);
hold on;
plot(datenum(hTime,31),humids)

axis manual;
axisTitle = title('Humidity and Temperature Values');
set(axisTitle,'FontSize', 25);
set(axisTitle, 'Color', 'k');
legend('Temperatures (C^o)','Humidities', 'Location','southwest')
xlabel('Date') % x-axis label
ylabel('Value') % y-axis label

clearvars fName delimiter startRow formatSpec fileID dataArray ans Time SensorType SensorValue NetworkID NodeID;