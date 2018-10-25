close all
X11 = X1*10^-9;
X22 = X2*10^-9;
Y2 = position_z(2167)-0.23;

deltaX = (X22 - (X11) );
deltaY = Y2 - Y1;
K = ((deltaY/deltaX)/0.1);

G = tf(K,[1, 0])
s = tf('s')
% G = G*exp(-s)
cv_linear_z_tmp = mergeData(cv_linear_z); % dobra daados
cv_linear_z1 = cv_linear_z_tmp(1:length(time))';
position_z1 = position_z;

time_ns = time * 10^-9;
t = linspace(0,time_ns(end)-time_ns(1),length(cv_linear_z1));
y1 = lsim(G, cv_linear_z1, t);
plot(t, position_z1, t, y1 + Y1);

legend('Sistema Real', 'Modelo Estimado');
title('Dados Capturas vs Modelo Estimado');


%syms x;
%syms y;
%y = sym(m*(x - X11) + Y1);
% xs = [1:10]
% ys = subs(y,x,xs)
% plot(xs, ys)

% dataz1 = iddata(ys, xs);
% sys_z1 = tfest(dataz1,1,0);

% s = tf('s');
