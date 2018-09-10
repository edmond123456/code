%x = -pi:0.01:pi;
%plot(x,sin(x)), grid on
clc
clear all
f=0.03;
p=2;
x = 0:0.001:150;
y=1/4*1800*(sin(2*pi*f*x)+sin(2*pi*f*p*x)/p+sin(2*pi*f*p^2*x)/p^2+sin(2*pi*f*p^3*x)/p^3+sin(2*pi*f*p^4*x)/p^4)+1998;
y1=2000-y;
plot(x,y), grid on