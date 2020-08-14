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
    subplot(4,1,1), plot(T(:,1), T(:,2)/1000);
    grid;
    subplot(4,1,2), plot(T_2(:,1), T_2(:,2)/1000);
    grid;
    subplot(4,1,3), plot(consecutive(T, samples));
    grid;
    axis([0 samples 0 samples/500]);
    axis 'auto y';
    subplot(4,1,4), plot(consecutive(T_2, samples));
    grid;
    axis([0 samples 0 samples/500]);
    axis 'auto y';
    saveas(gcf,strcat(strcat(file_name, file_name_2),'.png'));
end

function[cc] = consecutive(t, samples)
    if t(1)~= 0
        t = [0 t];
    end
    % iterator = 1;
    cc = [];
    d = diff(t);
    for i = 1:length(d)
        cc = [cc d(i)*ones(1,d(i))];
    end
end
