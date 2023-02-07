clear;
clc;
close all;


%{
    Get data 
    format into long array 
    use A filtering 
    Convert pascales to sound intensity (dBA)
    Plot results (How far can you hear the sound?)
    Create detection range
%}


rpm_names = {'1000', '1300', '1650', '1900', '725'};
fs = 25E3;
pressure_ref = 1e-12; %dBA


%Number 2 parameters
measured_distance = 1; %measured distance of sound
env_spl = 55; %sound pressure level of background noise dBA - the threshold for detection 
distance_from_sound = 1:10:1000; %distance from sound


%% Format data
%load all mat files
overall_data = {};
mat_files = dir('*.mat');

for i = 1:length(rpm_names)
    
    current_data = load(mat_files(i).name);
    current_data.data = table2array(current_data.data);
    current_data.data = current_data.data(:); 

    %add time to vector
    time_vector = [];
    time_vector(1) = 0.0;
    for j = 1:length(current_data.data)-1
        time_vector(j+1) = time_vector(j) + (1/fs);
    end
        
    %filter out data 
    [b,a] = adsgn(fs); %Create A-weighting filter coefficients
    filtered_data = filter(b,a, current_data.data); %filter out mic data with A-weights
        
    %compute pressure and frequencies
    [pressure,frequency] = oct3bank(filtered_data, fs, pressure_ref);
    
    %compute sound distance
    max_spl = max(pressure(:)); %get maximum frequency 
    
    sound_pressure_level = compute_sound_pressure_level(measured_distance, ...
        distance_from_sound, max_spl);

    %pack up data into struct file
    current_data.time_vector = time_vector';
    current_data.name = rpm_names{i};
    current_data.filtered_data = filtered_data;
    current_data.pressure = pressure;
    current_data.frequency = frequency;
    current_data.max_spl = max_spl;
    current_data.sound_pressure_level = sound_pressure_level;

    overall_data{i} = current_data;

end


%% Number 2 Plot frequency vs dBA 
figure(1)
line_color = ['b' 'g' 'k' 'c' 'm' 'r'];
labels = {}
for i = 1:length(overall_data)
    
    pressure = overall_data{i}.pressure;
    frequency = overall_data{i}.frequency;
    rpm_name = overall_data{i}.name;
    labels{i} = append('RPM ' + string(rpm_name));

    plot(frequency, pressure, line_color(i), 'LineWidth',1)
    hold on
end
legend(labels, 'Location', 'southeast')
xlabel('Frequency (hz)')
ylabel('Sound Pressure Intensity(dBA)')

%% Number 3 Plots 
figure(2)

for i = 1:length(overall_data)
    
    pressure = overall_data{i}.pressure;
    frequency = overall_data{i}.frequency;
    rpm_name = overall_data{i}.name;
    labels{i} = append('RPM ' + string(rpm_name));
    sound_pressure_level = overall_data{i}.sound_pressure_level;
    
    plot(distance_from_sound, sound_pressure_level, line_color(i));
    hold on
end

hold on 
plot([distance_from_sound(1), distance_from_sound(end)],...
        [env_spl, env_spl], 'r--' )

adjusted_labels = labels;
adjusted_labels{end+1} = 'Background' 

legend(adjusted_labels, 'Location', 'northeast')
xlabel('Frequency (hz)')
ylabel('Pressure (dBA)')
ylabel('Sound Pressure Intensity(dBA)')


%-----------------PRACTICE --------------------------------------------%
% %% Toy data
% idx_number = 2;
% toy_data = overall_data{idx_number}.data;
% time_vector = overall_data{idx_number}.time_vector;
% 
% %filter out data 
% [b,a] = adsgn(fs); %Create A-weighting filter coefficients
% filtered_data = filter(b,a, toy_data); %filter out mic data with A-weights
% 
% [P,F] = filtbank(filtered_data, fs, 100e-3);
% waterfall(P)
% zlabel('Level (dB)');
% ylabel('Frame #');
% xlabel('Frequency Band');
% 
% %%
% [P,F] = oct3bank(filtered_data, fs, 1e-12);
% 
% %% 
% max_spl = max(P(:)); %get maximum frequency 
% measured_distance = 1; %measured distance of sound
% env_spl = 30; %sound pressure level of background noise dBA - the threshold for detection 
% distance_from_sound = 1:10:1000; %distance from sound
% 
% sound_pressure_level = compute_sound_pressure_level(measured_distance, ...
%     distance_from_sound, max_spl);
% 
% figure()
% plot(distance_from_sound, sound_pressure_level, ...
%     [distance_from_sound(1), distance_from_sound(end)],...
%     [env_spl, env_spl], 'r--');


%% Functions used

function [sound_pressure_level] = compute_sound_pressure_level(measured_distance, ...
    distance_from_sound, max_spl);
    
    sound_pressure_level = max_spl - 20*log10(distance_from_sound./ ...
        measured_distance);

end

function [pressure, frequency] = compute_pressure_freq(fs, data, pressure_ref_db)
    [b,a] = adsgn(fs); %Create A-weighting filter coefficients
    filtered_data = filter(b,a, data); %filter out mic data with A-weights
    [pressure,frequency] = oct3bank(x, fs, pressure_ref_db)
    

end






