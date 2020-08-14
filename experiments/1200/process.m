function[c, T3] = process(file_name, file_name_2, samples)
    T = csvread(file_name, 1, 0);
    T_2 = csvread(file_name_2, 1, 0);
    [m,n] = size(T);
    [m_2,n_2] = size(T_2);
    T2 =  T(:,1);
    T3 = T2';
    T_22 =  T_2(:,1);
    T_23 = T_22';
    c = setdiff(0:(samples-1), T3);
    c_2 = setdiff(0:(samples-1), T_23);
    [m1,n1] = size(c);
    subplot(3,1,1), plot(T(:,1), T(:,2)/1000);
    hold;
    subplot(3,1,1), plot(T_2(:,1), T_2(:,2)/1000);
    grid;
    subplot(3,1,2), histogram(c, samples/50);
    grid;
    axis([0 samples 0 samples/500]);
    axis 'auto y'
    subplot(3,1,3), histogram(c_2, samples/50);
    grid;
    axis([0 samples 0 samples/500]);
    axis 'auto y'
    saveas(gcf,strcat(file_name,'.png'));
end