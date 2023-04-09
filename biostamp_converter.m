clear 
close all
clc
frmt = 'png';
Fts = 16; %Label font size
Lw = 1.5; %Line weight
folder = '/Users/katierohrer/Desktop/MOCA/GitHub/All-Lab-Data2.0/Data/ChestAA/CH2M/R1Fast';
path_to_save = folder;
saveplot = 0;
saveCSV = 1;
arm_len = 0.640;


muscles = {'Forearm', 'Brachio', 'Bicep'};
for trialnum = 1:length(muscles) 
    muscle = muscles{trialnum};

    %% arm lens
        % cg1f 0.560
        % gsp1m 0.570
        % ch2m 0.640
        % ya3m 0.660
        % es3f 0.550
        % ssi2f 0.608
    
    %% Finding correct files
    files = dir(folder);
    accel_file = "";
    gyro_file = "";
    for k=1:length(files)
       file = files(k).name;
       if contains(file, muscle) && contains(file, "Linear")
           accel_file = file;
       end
    
       if contains(file, muscle) && contains(file, "Angular")
           gyro_file = file;
       end
    
    end
    
    %% Extracting trial info from file
    file_info = split(accel_file, ".");
    
    export_file_name = join(file_info(1:7), ".");
    save_name = strcat(path_to_save, "/", ...
                       export_file_name, ".");
    X = strcat(folder, filesep, accel_file);
    A = importdata(strcat(folder, filesep, accel_file));
    B = importdata(strcat(folder, filesep, gyro_file));
    diff = length(A.data) - length(B.data) + 1;
    
    %% Getting equal lengths for time
    if diff < 0
        acc = A.data(1:end,:);
        time_dt_acc = acc(:,1);
    
        gyro = B.data(diff:end,:);
    else
        acc = A.data(diff:end,:);
        time_dt_acc = acc(diff:end,1);
    
        gyro = B.data(1:end,:);
    end
    
    %% sampling frequency and time vector
    fs = 62.5; %Hz
    dt = 1/fs;
    time_real = acc(:,1);
    nn = length(time_real);
    time = (0:1/fs:(nn-1)/fs)';
    
    %% remove any offset
    gyro(:,2) = gyro(:,2) - mean(gyro(1:200,2));
    gyro(:,3) = gyro(:,3) - mean(gyro(1:200,3));
    gyro(:,4) = gyro(:,4) - mean(gyro(1:200,4));
    
    clear b a
    [b,a] = butter(4,20/(fs/2),'low');
    gyro(:,2) = filtfilt(b,a,gyro(:,2));
    gyro(:,3) = filtfilt(b,a,gyro(:,3));
    gyro(:,4) = filtfilt(b,a,gyro(:,4));
    
    %% Gyro angle velocity
    if saveCSV == 1 
        save = strcat(folder, "/", gyro_file);
        
        B.colheaders = [B.colheaders, "gyro vel x (dps)", "gyro vel y (dps)", "gyro vel z (dps)"];
        B.data = [B.data, gyro(:,2), gyro(:,3), gyro(:,4)];

        newfile = [B.colheaders; B.data];

        writematrix(newfile, save)
    end
    
    %% Integration
    
    % Numerical integration gyro_x
    ang_x = zeros(1,nn);
    ang_x(1) = 0;
    for i = 2:1:nn
      ang_x(i) = ang_x(i-1)+1/2*(gyro(i-1,2)+gyro(i,2))/fs;
    end
    
    % Numerical integration gyro_y
    ang_y = zeros(1,nn);
    ang_y(1) = 0;
    for i = 2:1:nn
      ang_y(i) = ang_y(i-1)+1/2*(gyro(i-1,3)+gyro(i,3))/fs;
    end
    
    % Numerical integration gyro_z
    ang_z = zeros(1,nn);
    ang_z(1)= 0;
    for i = 2:1:nn
      ang_z(i) = ang_z(i-1)+1/2*(gyro(i-1,4)+gyro(i,4))/fs;
    end
    
    %% Gyro angle displacement
    if saveCSV == 1
        save = strcat(folder, "/", gyro_file);

        B.colheaders = [B.colheaders, "gyro disp x (deg)", "gyro disp y (deg)", "gyro disp z (deg)"];
        B.data = [B.data, ang_x', ang_y', ang_z'];

        newfile = [B.colheaders; B.data];

        writematrix(newfile, save);
    end
    
    %% acceleration removing off set
    clear b a
    [b,a] = butter(4, 5/(fs/2),'low');
    acc(:,2) = filtfilt(b,a,acc(:,2));
    acc(:,3) = filtfilt(b,a,acc(:,3));
    acc(:,4) = filtfilt(b,a,acc(:,4));
    
    %% accelaration converted in initial config
    % acc_p = zeros(nn,4);
    % for i = 1:1:nn
    %     T = [cosd(ang_z(i)) -sind(ang_z(i)) 0; sind(ang_z(i)) cosd(ang_z(i)) 0; 0 0 1]; %trnasformation matrix
    %     acc_p(i,2:4) = T*acc(i,2:4)';
    % end
    
    % Method 2-----------------------------------------------------------------
    % dt = (gyro(2,1)-gyro(1,1))/1000;
    T1 = eye(3);
    for i = 2:1:nn
          ang = -[gyro(i-1,2)+gyro(i,2) gyro(i-1,3)+gyro(i,3) gyro(i-1,4)+gyro(i,4)]*dt/2; 
          theta = norm(ang);
    %      ang = [ang_x_corr(i-1)-ang_x_corr(i) ang_y_corr(i-1)-ang_y_corr(i) ang_z_corr(i-1)-ang_z_corr(i)];
    %      theta =norm(ang);
        if theta <= 0.001   % incase change in angle very small
            theta = 0;
            u = [1 1 1];
        else
            u = ang/theta;
        end
        e_0 = cosd(theta/2);
        e = u*sind(theta/2);
        T = quat2dcm([e_0 e]);
        T2 = T1*T;
        T1 = T2;
        acc_p(i,2:4) = T2*acc(i,2:4)';
    end
    acc_p(1,2:4) = acc(1,2:4);
    
    for i =1:1:nn     % gravity correction
      acc_p(i,2:4) = acc_p(i,2:4)-acc(1,2:4);
    end
    
    % Taking signal to local coordinate
    mAccL = zeros(nn,4);  % movement accl in local
    T1 = eye(3);
    for i = 2:1:nn
          ang = -[gyro(i-1,2)+gyro(i,2) gyro(i-1,3)+gyro(i,3) gyro(i-1,4)+gyro(i,4)]*dt/2; 
          theta = norm(ang);
        if theta <= 0.001   % incase change in angle very small
            theta = 0;
            u = [1 1 1];
        else
            u = ang/theta;
        end
        e_0 = cosd(theta/2);
        e = u*sind(theta/2);
        T = quat2dcm([e_0 e]);
        T2 = T1*T;
        T1 = T2;
        mAccL(i,2:4) = T2'*acc_p(i,2:4)';
    end
    
    gravL = acc(:,2:4)-mAccL(:,2:4);
    checkN = zeros(nn,1);
    for i = 1:1:nn
        checkN(i) = norm([gravL(i,1) gravL(i,2) gravL(i,3)]);
    end
    
    ang = atan2(-gravL(:,3),gravL(:,1));
    ang = (ang-ang(1))*180/pi;
    
    ang = smooth(ang,62);
    
    % Tilt compensation
    v = -acc(1,2:4);
    v = v/norm(v);
    u = [0 v(3) -v(2)];
    u = u/norm(u);
    theta = acosd(v(1));
    e_0 = cosd(theta/2);
    e = u*sind(theta/2);
    T = quat2dcm([e_0 e]);
    T = T';
    %v_p = T*v'  %check
    
    acc_p_tc = zeros('like',acc_p); %Global acceleration with tilt correction
    for i = 1:1:nn
        acc_p_tc(i,2:4) = T*acc_p(i,2:4)';
    end
    
    %% double-integration for displacement
    [b,a] = ellip(5,0.03,50,0.1/(fs/2),'high');
    acc_p_tc(:,2) = filtfilt(b,a,acc_p_tc(:,2));
    acc_p_tc(:,3) = filtfilt(b,a,acc_p_tc(:,3));
    acc_p_tc(:,4) = filtfilt(b,a,acc_p_tc(:,4));
    
    accx = acc_p_tc(:,2)*9.81;
    accy = acc_p_tc(:,3)*9.81;
    accz = acc_p_tc(:,4)*9.81;
    
    %% Numerical integration to velocity
    velx = zeros(1,nn);
    vely = zeros(1,nn);
    velz = zeros(1,nn);
    velx(1) = 0;
    vely(1) = 0;
    velz(1) = 0;
    for i = 2:1:nn
      velx(i) = velx(i-1)+1/2*(accx(i-1)+ accx(i))/fs;
      vely(i) = vely(i-1)+1/2*(accy(i-1)+ accy(i))/fs;
      velz(i) = velz(i-1)+1/2*(accz(i-1)+ accz(i))/fs;
    end
    
    clear b a
    [b,a] = ellip(5,0.03,50,0.2/(fs/2),'high');
    velx_f = filtfilt(b,a,velx);
    vely_f = filtfilt(b,a,vely);
    velz_f = filtfilt(b,a,velz);
    
    
    %% raw velocity in m/s
    if saveCSV == 1
        save = strcat(folder, "/", accel_file);

        A.colheaders = [A.colheaders, "vel x (m/s)", "vel y (m/s)", "vel z (m/s)"];
        A.data = [A.data, velx', vely', velz'];

        newfile = [A.colheaders; A.data];

        writematrix(newfile, save)
    end
    
    % Numerical integration to disp
    disx = zeros(1,nn);
    disy = zeros(1,nn);
    disz = zeros(1,nn);
    disx(1) = 0;
    disy(1) = 0;
    disz(1) = 0;
    for i = 2:1:nn
      disx(i) = disx(i-1)+1/2*(velx_f(i-1)+ velx_f(i))/fs;
      disy(i) = disy(i-1)+1/2*(vely_f(i-1)+ vely_f(i))/fs;
      disz(i) = disz(i-1)+1/2*(velz_f(i-1)+ velz_f(i))/fs;
    end
    
    
    disx = filtfilt(b,a,disx);
    disy = filtfilt(b,a,disy);
    disz = filtfilt(b,a,disz);
    
    % Transformation to inclined plane (rotation about z-axis)
    degree = -90;
    T_rot_z = [cosd(degree)    -sind(degree)     0;...
               sind(degree)     cosd(degree)     0; ...
                    0               0            1];
    
    for i=1:1:nn
      dis_in(i,1:3) = T_rot_z*[disx(i);disy(i);disz(i)];
    end
    
    % Transformation to inclined plane (rotation about x-axis)
    degree = -90;
    T_rot_x = [1          0               0; ...
               0     cosd(degree)   -sind(degree); ...
               0     sind(degree)    cosd(degree)];
    
    for i=1:1:nn
      dis_in(i,1:3) = T_rot_x*dis_in(i,1:3)';
    end
    
    % Transformation to inclined plane (rotation about z-axis) correction for
    % initial angle
    degree = 30;
    T_rot_z = [cosd(degree)    -sind(degree)     0; ...
               sind(degree)     cosd(degree)     0; ...
                    0               0            1];
    for i=1:1:nn
      dis_in(i,1:3) = T_rot_z*dis_in(i,1:3)';
    end
    
    offset_z = zeros(length(time),1);
    offset_y = zeros(length(time),1);
    for i = 1:1:nn
       offset_z(i) = arm_len*cosd(ang(i));
       offset_y(i) = -arm_len*sind(ang(i));
    end
    
    dis_in(:,3) = dis_in(:,3)-offset_z;
    dis_in(:,2) = dis_in(:,2)-offset_y;
    
    
    %% displacement over time in m
    if saveCSV == 1
        save = strcat(folder, "/", accel_file);

        A.colheaders = [A.colheaders, "disp x (m)", "disp y (m)", "disp z (m)"];
        A.data = [A.data, dis_in(1:i,1), dis_in(1:i,2), dis_in(1:i,3)];
        
        newfile = [A.colheaders; A.data];

        writematrix(newfile, save)
    end

    clearvars -except muscle muscles folder trialnum path_to_save ...
        arm_len Fts Lw savePlot saveCSV frmt
    close all
    clc
end