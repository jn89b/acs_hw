clear, clc, close all
% white noise generation
fs = 96000;
T = 0.1;
N = round(T*fs);
x = randn(1, N);
t = (0:N-1)/fs;
% filtering
xA = filterA(x, fs);
% plot the original signal
figure(1)
plot(t, x)
grid on
hold on
% plot the filtered signal
plot(t, xA, 'r')
set(gca, 'FontName', 'Times New Roman', 'FontSize', 14)
axis([0 T -5 5])
xlabel('Time, s')
ylabel('Amplitude')
title('Original and A-weighted signal in the time domain')
legend('Original signal', 'A-weighted signal')