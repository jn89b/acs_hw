clear;
clc
close all;

% Load octave directory

% Load csv data
mic_725pm = read_csv('Mic1_725rpm.csv');
save_as_mat('mic_725rpm.mat', mic_725pm);

%save mic_725pm.mat mic_725pm
mic_2 = read_csv('Mic1_1000rpm.csv');
save_as_mat('mic_1000rpm.mat', mic_2);

mic_3 = read_csv('Mic1_1300rpm.csv');
save_as_mat('mic_1300rpm.mat', mic_3);
 
mic_4 = read_csv('Mic1_1650rpm.csv');
save_as_mat('mic_1650rpm.mat', mic_4);

mic_5 = read_csv('Mic1_1900rpm.csv');
save_as_mat('mic_1900rpm.mat', mic_5);


function [data] = read_csv(filename)
    % Read csv file
    data = readtable(filename);
end 

function save_as_mat(mat_file_name, data)
    % Save data as mat file
    save(mat_file_name, 'data');

end
