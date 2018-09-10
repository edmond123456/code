%x = -pi:0.01:pi;
%plot(x,sin(x)), grid on
%plot of pseudorandom numbers
clc
clear all
f=0.03;
p=2;
MaxVelXY=0.55;
x = 0:0.01:30;

d=1*(sin(2*pi*f*x+(rand(1,3001)-1)*pi)+sin(2*pi*f*p*x+(rand(1,3001)-1)*pi)/p+sin(2*pi*f*p^2*x+(rand(1,3001)-1)*pi)/p^2+sin(2*pi*f*p^3*x+(rand(1,3001)-1)*pi)/p^3+sin(2*pi*f*p^4*x+(rand(1,3001)-1)*pi)/p^4);

%d=1/4*(sin(2*pi*f*x+(rand(2)-1)*pi)+sin(2*pi*f*p*x+(rand(2)-1)*pi)/p+sin(2*pi*f*p^2*x+(rand(2)-1)*pi)/p^2+sin(2*pi*f*p^3*x+(rand(2)-1)*pi)/p^3+sin(2*pi*f*p^4*x+(rand(2)-1)*pi)/p^4);
%vp0=1/4*(sin(2*pi*f)+sin(2*pi*f*p)/p+sin(2*pi*f*p^2)/p^2+sin(2*pi*f*p^3)/p^3+sin(2*pi*f*p^4)/p^4);
%d=vp0.*MaxVelXY.*x;


%plot(x,d)
y=1998-cumsum(d);
plot(x,y), grid on