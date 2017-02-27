within ;
package LBNL71T_MPC

  model RunMPC

    parameter Modelica.SIunits.Angle lon= -87.6298*Modelica.Constants.pi/180;
    parameter Modelica.SIunits.Angle lat= 41.8781*Modelica.Constants.pi/180;
    parameter Modelica.SIunits.Time timZon= -6*3600;
    parameter Modelica.SIunits.Time modTimOffset = 0;

    Buildings.BoundaryConditions.WeatherData.ReaderTMY3 epw(filNam=
        "modelica://Buildings/Resources/weatherdata/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.mos")
    "Weather data"
    annotation (Placement(transformation(extent={{-540,20},{-430,120}})));
  MPC mpc(
    timZon=timZon,
    modTimOffset=0,
    lon=lon,
    lat=lat)
    annotation (Placement(transformation(extent={{-108,-102},{146,138}})));
    Modelica.Blocks.Sources.CombiTimeTable intGaiFra(
         extrapolation=Modelica.Blocks.Types.Extrapolation.Periodic, table=[0,
        0.05; 3600*8,0.05; 3600*8,0.9; 3600*12,0.9; 3600*12,0.8; 3600*13,
        0.8; 3600*13,1; 3600*17,1; 3600*17,0.1; 3600*20,0.1; 3600*20,0.05;
        3600*24,0.05])
    "Fraction of internal heat gain"
      annotation (Placement(transformation(extent={{-320,200},{-300,220}})));
    Modelica.Blocks.Math.MatrixGain gai(K=20*[0.4; 0.4; 0.2])
    "Matrix gain to split up heat gain in radiant, convective and latent gain"
      annotation (Placement(transformation(extent={{-280,200},{-260,220}})));
  Modelica.Blocks.Routing.DeMultiplex3 deMultiplex3_1
    annotation (Placement(transformation(extent={{222,118},{202,138}})));
    Modelica.Blocks.Sources.CombiTimeTable intGaiFra1(
         extrapolation=Modelica.Blocks.Types.Extrapolation.Periodic, table=[0,
        0.05; 3600*7,0.05; 3600*7,0.1; 3600*19,0.1; 3600*19,0.05; 3600*24,
        0.05]) "Fraction of internal heat gain"
      annotation (Placement(transformation(extent={{-320,160},{-300,180}})));
    Modelica.Blocks.Math.MatrixGain gai1(
                                        K=20*[0.4; 0.4; 0.2])
    "Matrix gain to split up heat gain in radiant, convective and latent gain"
      annotation (Placement(transformation(extent={{-280,160},{-260,180}})));
  Modelica.Blocks.Routing.DeMultiplex3 deMultiplex3_2
    annotation (Placement(transformation(extent={{220,48},{200,68}})));
  Buildings.BoundaryConditions.WeatherData.Bus weaBus "Weather data bus"
    annotation (Placement(transformation(extent={{-412,60},{-392,80}})));
  BoundaryConditions.WeatherProcessor          weatherProcessor(
      modTimOffset=0,
      lon=-1.5344934783534,
      lat=0.73268921998722,
      timZon=-21600)
      annotation (Placement(transformation(extent={{-316,36},{-248,104}})));
  Controllers.DualSetpoint                   DualSetpoint(
      OnStatus=true,
      Setpoint=20 + 273,
      Setback=5)
      annotation (Placement(transformation(extent={{-82,-172},{-62,-152}})));
  equation

  connect(deMultiplex3_1.y1[1], mpc.intRad_wes) annotation (Line(points={{201,135},
            {176.5,135},{176.5,109.2},{156.583,109.2}},            color={0,
          0,127}));
  connect(deMultiplex3_1.y2[1], mpc.intCon_wes) annotation (Line(points={{201,128},
            {176,128},{176,94.8},{156.583,94.8}},    color={0,0,127}));
  connect(deMultiplex3_1.y3[1], mpc.intLat_wes) annotation (Line(points={{201,121},
            {174.5,121},{174.5,80.4},{156.583,80.4}},              color={0,
          0,127}));
  connect(deMultiplex3_1.y1[1], mpc.intRad_eas) annotation (Line(points={{201,135},
            {184,135},{184,13.2},{156.583,13.2}},              color={0,0,
          127}));
  connect(deMultiplex3_1.y2[1], mpc.intCon_eas) annotation (Line(points={{201,128},
            {188,128},{188,-1.2},{156.583,-1.2}},              color={0,0,
          127}));
  connect(deMultiplex3_1.y3[1], mpc.intLat_eas) annotation (Line(points={{201,121},
            {194,121},{194,-15.6},{156.583,-15.6}},              color={0,0,
          127}));
  connect(deMultiplex3_2.y1[1], mpc.intRad_hal) annotation (Line(points={{199,65},
            {178,65},{178,61.2},{156.583,61.2}},             color={0,0,127}));
  connect(deMultiplex3_2.y2[1], mpc.intCon_hal) annotation (Line(points={{199,58},
            {170,58},{170,46.8},{156.583,46.8}},             color={0,0,127}));
  connect(deMultiplex3_2.y3[1], mpc.intLat_hal) annotation (Line(points={{199,51},
            {170,51},{170,32.4},{156.583,32.4}},             color={0,0,127}));
  connect(epw.weaBus, weaBus) annotation (Line(
      points={{-430,70},{-402,70}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaBus.pAtm, weatherProcessor.weaPAtm) annotation (Line(
      points={{-402,70},{-396,70},{-388,70},{-388,102},{-318,102}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(weaBus.TDewPoi, weatherProcessor.weaTDewPoi) annotation (Line(
      points={{-402,70},{-388,70},{-388,96},{-318,96}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(weaBus.TDryBul, weatherProcessor.weaTDryBul) annotation (Line(
      points={{-402,70},{-388,70},{-388,89.8},{-318,89.8}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(weaBus.relHum, weatherProcessor.weaRelHum) annotation (Line(
      points={{-402,70},{-388,70},{-388,83.8},{-318,83.8}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(weaBus.nOpa, weatherProcessor.weaNOpa) annotation (Line(
      points={{-402,70},{-388,70},{-388,77.8},{-318,77.8}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(weaBus.celHei, weatherProcessor.weaCelHei) annotation (Line(
      points={{-402,70},{-396,70},{-386,70},{-386,71.8},{-318,71.8}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(weaBus.nTot, weatherProcessor.weaNTot) annotation (Line(
      points={{-402,70},{-388,70},{-388,66},{-318,66}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(weaBus.winSpe, weatherProcessor.weaWinSpe) annotation (Line(
      points={{-402,70},{-396,70},{-388,70},{-388,60},{-318,60}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(weaBus.winDir, weatherProcessor.weaWinDir) annotation (Line(
      points={{-402,70},{-388,70},{-388,53.6},{-318,53.6}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(weaBus.HHorIR, weatherProcessor.weaHHorIR) annotation (Line(
      points={{-402,70},{-388,70},{-388,47.8},{-318,47.8}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(weaBus.HDirNor, weatherProcessor.weaHDirNor) annotation (Line(
      points={{-402,70},{-396,70},{-388,70},{-388,41.8},{-318,41.8}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(weaBus.HGloHor, weatherProcessor.weaHGloHor) annotation (Line(
      points={{-402,70},{-388,70},{-388,36},{-318,36}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(mpc.weaPAtm, weatherProcessor.weaPAtm) annotation (Line(points={{
            -118.583,128.4},{-376,128.4},{-376,102},{-318,102}},
                                                               color={0,0,
          127}));
  connect(mpc.weaTDewPoi, weatherProcessor.weaTDewPoi) annotation (Line(
        points={{-118.583,114},{-136,114},{-136,146},{-378,146},{-378,96},{-318,
            96}},    color={0,0,127}));
  connect(mpc.weaTDryBul, weatherProcessor.weaTDryBul) annotation (Line(
        points={{-118.583,99.6},{-138,99.6},{-138,144},{-376,144},{-376,89.8},{
            -318,89.8}},      color={0,0,127}));
  connect(mpc.weaRelHum, weatherProcessor.weaRelHum) annotation (Line(
        points={{-118.583,85.2},{-140,85.2},{-140,142},{-374,142},{-374,83.8},{
            -318,83.8}},      color={0,0,127}));
  connect(mpc.weaNOpa, weatherProcessor.weaNOpa) annotation (Line(points={{
            -118.583,70.8},{-142,70.8},{-142,140},{-372,140},{-372,77.8},{-318,
            77.8}},
                  color={0,0,127}));
  connect(mpc.weaCelHei, weatherProcessor.weaCelHei) annotation (Line(
        points={{-118.583,56.4},{-144,56.4},{-144,138},{-370,138},{-370,71.8},{
            -318,71.8}},      color={0,0,127}));
  connect(mpc.weaNTot, weatherProcessor.weaNTot) annotation (Line(points={{
            -118.583,42},{-146,42},{-146,136},{-368,136},{-368,66},{-318,66}},
        color={0,0,127}));
  connect(mpc.weaWinSpe, weatherProcessor.weaWinSpe) annotation (Line(
        points={{-118.583,27.6},{-134,27.6},{-134,34},{-148,34},{-148,134},{
            -366,134},{-366,60},{-318,60}},color={0,0,127}));
  connect(mpc.weaWinDir, weatherProcessor.weaWinDir) annotation (Line(
        points={{-118.583,13.2},{-150,13.2},{-150,132},{-364,132},{-364,53.6},{
            -318,53.6}},      color={0,0,127}));
  connect(mpc.weaHHorIR, weatherProcessor.weaHHorIR) annotation (Line(
        points={{-118.583,-1.2},{-152,-1.2},{-152,130},{-362,130},{-362,47.8},{
            -318,47.8}},      color={0,0,127}));
  connect(mpc.weaHDirNor, weatherProcessor.weaHDirNor) annotation (Line(
        points={{-118.583,-15.6},{-154,-15.6},{-154,128},{-360,128},{-360,41.8},
            {-318,41.8}},     color={0,0,127}));
  connect(mpc.weaHGloHor, weatherProcessor.weaHGloHor) annotation (Line(
        points={{-118.583,-30},{-156,-30},{-156,126},{-358,126},{-358,36},{-318,
            36}},    color={0,0,127}));
  connect(weatherProcessor.weaHDifHor, mpc.weaHDifHor) annotation (Line(
        points={{-247,102},{-182,102},{-182,-44.4},{-118.583,-44.4}}, color=
         {0,0,127}));
  connect(weatherProcessor.weaTBlaSky, mpc.weaTBlaSky) annotation (Line(
        points={{-247,96},{-186,96},{-186,-58.8},{-118.583,-58.8}}, color={
          0,0,127}));
  connect(weatherProcessor.weaTWetBul, mpc.weaTWetBul) annotation (Line(
        points={{-247,90},{-247,90},{-190,90},{-190,-73.2},{-118.583,-73.2}},
        color={0,0,127}));
  connect(weatherProcessor.weaCloTim, mpc.weaCloTim) annotation (Line(
        points={{-247,77.8},{-198,77.8},{-198,-102},{-118.583,-102}}, color=
         {0,0,127}));
  connect(weatherProcessor.weaSolTim, mpc.weaSolTim) annotation (Line(
        points={{-247,71.8},{-202,71.8},{-202,-116.4},{-118.583,-116.4}},
        color={0,0,127}));
  connect(weatherProcessor.weaSolZen, mpc.weaSolZen) annotation (Line(
        points={{-247,84},{-194,84},{-194,-87.6},{-118.583,-87.6}}, color={
          0,0,127}));
  connect(intGaiFra.y, gai.u)
    annotation (Line(points={{-299,210},{-282,210}}, color={0,0,127}));
  connect(intGaiFra1.y, gai1.u) annotation (Line(points={{-299,170},{-290.5,
          170},{-282,170}}, color={0,0,127}));
  connect(gai.y, deMultiplex3_1.u) annotation (Line(points={{-259,210},{-34,
          210},{242,210},{242,142},{242,128},{224,128}}, color={0,0,127}));
  connect(gai1.y, deMultiplex3_2.u) annotation (Line(points={{-259,170},{
          -259,170},{250,170},{250,58},{222,58}}, color={0,0,127}));
  connect(mpc.wesTdb, DualSetpoint.meaTDryBul_wes) annotation (Line(points={{151.292,
            -34.8},{240,-34.8},{240,-222},{-140,-222},{-140,-156},{-84,-156}},
                  color={0,0,127}));
  connect(mpc.halTdb, DualSetpoint.meaTDryBul_hal) annotation (Line(points={{151.292,
            -44.4},{232,-44.4},{232,-216},{-132,-216},{-132,-162},{-84,-162}},
                             color={0,0,127}));
  connect(mpc.easTdb, DualSetpoint.meaTDryBul_eas) annotation (Line(points={{151.292,
            -54},{226,-54},{226,-204},{-120,-204},{-120,-168},{-84,-168}},
                             color={0,0,127}));
  connect(DualSetpoint.y_wes, mpc.conHeat_wes) annotation (Line(points={{-61,
            -158},{-2.16667,-158},{-2.16667,-111.6}},     color={0,0,127}));
  connect(DualSetpoint.y_hal, mpc.conHeat_hal) annotation (Line(points={{-61,
          -162},{-61,-162},{19,-162},{19,-111.6}},       color={0,0,127}));
  connect(DualSetpoint.y_eas, mpc.conHeat_eas) annotation (Line(points={{-61,
            -166},{-61,-166},{40.1667,-166},{40.1667,-111.6}},     color={0,
          0,127}));

    annotation (Diagram(coordinateSystem(extent={{-600,-240},{280,240}})), Icon(
          coordinateSystem(extent={{-600,-240},{280,240}})),
    experiment(StopTime=604800, Interval=300),
    __Dymola_experimentSetupOutput);
  end RunMPC;

  model MPC "Open loop MPC model of the three zones"
    extends Modelica.Blocks.Icons.Block;

    replaceable package Medium = Buildings.Media.Air "Medium model";

    parameter Modelica.SIunits.Angle lon=-122*Modelica.Constants.pi/180;
    parameter Modelica.SIunits.Angle lat=38*Modelica.Constants.pi/180;
    parameter Modelica.SIunits.Time timZon=-8*3600;
    parameter Modelica.SIunits.Time modTimOffset=0;
    Modelica.Blocks.Interfaces.RealInput intRad_wes
    "Radiant, convective and latent heat input into room (positive if heat gain)"
      annotation (Placement(transformation(extent={{280,180},{240,220}})));
    Modelica.Blocks.Interfaces.RealInput intCon_wes
    "Radiant, convective and latent heat input into room (positive if heat gain)"
      annotation (Placement(transformation(extent={{280,150},{240,190}})));
    Modelica.Blocks.Interfaces.RealInput intLat_wes
    "Radiant, convective and latent heat input into room (positive if heat gain)"
      annotation (Placement(transformation(extent={{280,120},{240,160}})));
    Modelica.Blocks.Interfaces.RealInput intRad_hal
    "Radiant, convective and latent heat input into room (positive if heat gain)"
      annotation (Placement(transformation(extent={{280,80},{240,120}})));
    Modelica.Blocks.Interfaces.RealInput intCon_hal
    "Radiant, convective and latent heat input into room (positive if heat gain)"
      annotation (Placement(transformation(extent={{280,50},{240,90}})));
    Modelica.Blocks.Interfaces.RealInput intLat_hal
    "Radiant, convective and latent heat input into room (positive if heat gain)"
      annotation (Placement(transformation(extent={{280,20},{240,60}})));
    Modelica.Blocks.Interfaces.RealInput intRad_eas
    "Radiant, convective and latent heat input into room (positive if heat gain)"
      annotation (Placement(transformation(extent={{280,-20},{240,20}})));
    Modelica.Blocks.Interfaces.RealInput intCon_eas
    "Radiant, convective and latent heat input into room (positive if heat gain)"
      annotation (Placement(transformation(extent={{280,-50},{240,-10}})));
    Modelica.Blocks.Interfaces.RealInput intLat_eas
    "Radiant, convective and latent heat input into room (positive if heat gain)"
      annotation (Placement(transformation(extent={{280,-80},{240,-40}})));
    Modules.modExt          exteas(
      lat=lat,
      A_ext=1.51,
      til=1.5707963267949,
      azi=-1.5707963267949)
      annotation (Placement(transformation(extent={{64,20},{84,40}})));
    Modules.modZon          eas(A_zon=13.7954)
      annotation (Placement(transformation(extent={{68,-10},{88,10}})));
    Modules.modAdj          adjeas(A_adj=10.22)
      annotation (Placement(transformation(extent={{34,-10},{54,10}})));
    Modules.modZon          hal(A_zon=9.09792)
      annotation (Placement(transformation(extent={{-2,-10},{18,10}})));
    Modules.modAdj          adjwes(A_adj=10.22)
      annotation (Placement(transformation(extent={{-38,-10},{-18,10}})));
    Modules.modZon          wes(A_zon=13.7954)
      annotation (Placement(transformation(extent={{-76,-10},{-56,10}})));
    Modules.modExt          extwes(
      lat=lat,
      A_ext=1.51,
      til=1.5707963267949,
      azi=1.5707963267949)
      annotation (Placement(transformation(extent={{-76,20},{-56,40}})));
    Modules.modWin          winwes(
      lat=lat,
      A_win=8.71,
      til=1.5707963267949,
      azi=1.5707963267949)
      annotation (Placement(transformation(extent={{-76,-40},{-56,-20}})));
    Modules.modWin          wineas(
      lat=lat,
      A_win=8.71,
      azi(displayUnit="deg") = -1.5707963267949,
      til=1.5707963267949)
      annotation (Placement(transformation(extent={{64,-40},{84,-20}})));
  protected
    Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor temSen
    "Room air temperature sensor"
      annotation (Placement(transformation(extent={{-2,-64},{18,-44}})));
    Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor temSen1
    "Room air temperature sensor"
      annotation (Placement(transformation(extent={{24,-88},{44,-68}})));
    Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor temSen2
    "Room air temperature sensor"
      annotation (Placement(transformation(extent={{66,-106},{86,-86}})));
  public
    Modelica.Blocks.Interfaces.RealOutput easTdb(unit = "K")
    annotation (Placement(transformation(extent={{240,-150},{260,-130}})));
  Modelica.Blocks.Interfaces.RealOutput halTdb(unit = "K")
    annotation (Placement(transformation(extent={{240,-130},{260,-110}})));
  Modelica.Blocks.Interfaces.RealOutput wesTdb(unit = "K")
    annotation (Placement(transformation(extent={{240,-110},{260,-90}})));
    Modelica.Blocks.Interfaces.RealInput weaPAtm "Input pressure"
      annotation (Placement(transformation(extent={{-280,220},{-240,260}})));
    Modelica.Blocks.Interfaces.RealInput weaTDewPoi
    "Input dew point temperature"
    annotation (Placement(transformation(extent={{-280,190},{-240,230}})));
    Modelica.Blocks.Interfaces.RealInput weaTDryBul
    "Input dry bulb temperature"
    annotation (Placement(transformation(extent={{-280,160},{-240,200}})));
    Modelica.Blocks.Interfaces.RealInput weaRelHum
    "Input relative humidity"
    annotation (Placement(transformation(extent={{-280,130},{-240,170}})));
    Modelica.Blocks.Interfaces.RealInput weaNOpa "Input opaque sky cover"
    annotation (Placement(transformation(extent={{-280,100},{-240,140}})));
    Modelica.Blocks.Interfaces.RealInput weaCelHei "Input ceiling height"
    annotation (Placement(transformation(extent={{-280,70},{-240,110}})));
    Modelica.Blocks.Interfaces.RealInput weaNTot "Input total sky cover"
    annotation (Placement(transformation(extent={{-280,40},{-240,80}})));
    Modelica.Blocks.Interfaces.RealInput weaWinSpe "Input wind speed"
    annotation (Placement(transformation(extent={{-280,10},{-240,50}})));
    Modelica.Blocks.Interfaces.RealInput weaWinDir "Input wind direction"
    annotation (Placement(transformation(extent={{-280,-20},{-240,20}})));
    Modelica.Blocks.Interfaces.RealInput weaHHorIR
    "Input diffuse horizontal radiation"
    annotation (Placement(transformation(extent={{-280,-50},{-240,-10}})));
    Modelica.Blocks.Interfaces.RealInput weaHDirNor
    "Input infrared horizontal radiation"
    annotation (Placement(transformation(extent={{-280,-80},{-240,-40}})));
    Modelica.Blocks.Interfaces.RealInput weaHGloHor
    "Input direct normal radiation"
    annotation (Placement(transformation(extent={{-280,-110},{-240,-70}})));
    Modelica.Blocks.Interfaces.RealInput weaHDifHor
    "Input global horizontal radiation" annotation (Placement(
        transformation(extent={{-280,-140},{-240,-100}})));
    Modelica.Blocks.Interfaces.RealInput weaTBlaSky
    "Input global horizontal radiation" annotation (Placement(
        transformation(extent={{-280,-170},{-240,-130}})));
    Modelica.Blocks.Interfaces.RealInput weaTWetBul
    "Input global horizontal radiation" annotation (Placement(
        transformation(extent={{-280,-200},{-240,-160}})));
    Modelica.Blocks.Interfaces.RealInput weaCloTim
    "Input global horizontal radiation" annotation (Placement(
        transformation(extent={{-280,-260},{-240,-220}})));
    Modelica.Blocks.Interfaces.RealInput weaSolTim
    "Input global horizontal radiation" annotation (Placement(
        transformation(extent={{-280,-290},{-240,-250}})));
    Modelica.Blocks.Interfaces.RealInput weaSolZen
    "Input global horizontal radiation" annotation (Placement(
        transformation(extent={{-280,-230},{-240,-190}})));
  BoundaryConditions.Wea2Bus          wea2Bus
      annotation (Placement(transformation(extent={{-164,138},{-120,242}})));
    Modelica.Blocks.Interfaces.RealInput conHeat_eas(unit = "1")
    "HVAC Heating Input for eas Zone" annotation (Placement(transformation(
        extent={{-20,-20},{20,20}},
        rotation=90,
        origin={40,-260})));
    Modelica.Blocks.Interfaces.RealInput conHeat_hal(unit = "1")
    "HVAC Heating Input for hal Zone" annotation (Placement(transformation(
        extent={{-20,-20},{20,20}},
        rotation=90,
        origin={0,-260})));
    Modelica.Blocks.Interfaces.RealInput conHeat_wes(unit = "1")
    "HVAC Heating Input for wes Zone" annotation (Placement(transformation(
        extent={{-20,-20},{20,20}},
        rotation=90,
        origin={-40,-260})));
    HVAC.ConvectiveHeater                   convectiveHeater_wes(eff=0.99,
        q_max=1034.655)
      annotation (Placement(transformation(extent={{-60,-76},{-40,-56}})));
    HVAC.ConvectiveHeater                   convectiveHeater_eas(eff=0.99,
        q_max=827.724)
      annotation (Placement(transformation(extent={{-60,-116},{-40,-96}})));
    Modelica.Blocks.Interfaces.RealOutput wesPhvac(unit = "W")
      annotation (Placement(transformation(extent={{240,-170},{260,-150}})));
    Modelica.Blocks.Interfaces.RealOutput easPhvac(unit = "W")
      annotation (Placement(transformation(extent={{240,-210},{260,-190}})));
    Modelica.Blocks.Math.Add3 add
    annotation (Placement(transformation(extent={{210,-250},{230,-230}})));
    Modelica.Blocks.Interfaces.RealOutput Ptot(unit = "W")
      annotation (Placement(transformation(extent={{240,-250},{260,-230}})));
    HVAC.ConvectiveHeater                   convectiveHeater_hal(eff=0.99,
        q_max=350)
      annotation (Placement(transformation(extent={{-60,-96},{-40,-76}})));
  Modelica.Blocks.Interfaces.RealOutput halPhvac(unit = "W")
    annotation (Placement(transformation(extent={{240,-190},{260,-170}})));
  equation

    // Fluid connections
    connect(extwes.porZon, wes.porZon) annotation (Line(points={{-55,30},{
          -46,30},{-46,5},{-55,5}},
                              color={191,0,0}));
    connect(wes.porZon, adjwes.porAdj) annotation (Line(points={{-55,5},{
          -42,5},{-42,0},{-39,0}},
                         color={191,0,0}));
    connect(adjwes.porZon, hal.porZon)
      annotation (Line(points={{-17,0},{19,0},{19,5}}, color={191,0,0}));
    connect(adjeas.porZon, eas.porZon)
      annotation (Line(points={{55,0},{89,0},{89,5}}, color={191,0,0}));
    connect(exteas.porZon, eas.porZon)
      annotation (Line(points={{85,30},{96,30},{96,5},{89,5}}, color={191,0,0}));

  connect(intRad_wes, wes.intRad) annotation (Line(points={{260,200},{260,
          200},{210,200},{210,174},{-44,174},{-44,62},{-88,62},{-88,-7},{
          -78,-7}}, color={0,0,127}));
  connect(intCon_wes, wes.intCon) annotation (Line(points={{260,170},{-40,
          170},{-40,58},{-84,58},{-84,7},{-78,7}}, color={0,0,127}));
  connect(intRad_hal, hal.intRad) annotation (Line(points={{260,100},{-12,
          100},{-12,-7},{-4,-7}}, color={0,0,127}));
  connect(intCon_hal, hal.intCon) annotation (Line(points={{260,70},{210,70},
          {210,104},{-8,104},{-8,7},{-4,7}}, color={0,0,127}));
  connect(intRad_eas, eas.intRad) annotation (Line(points={{260,0},{210,0},
          {210,28},{116,28},{116,16},{60,16},{60,-6},{66,-6},{66,-7}},
                                                               color={0,0,
          127}));
  connect(intCon_eas, eas.intCon) annotation (Line(points={{260,-30},{206,
          -30},{206,22},{120,22},{120,12},{62,12},{62,6},{66,6},{66,7}},
                                                                  color={0,
          0,127}));
    connect(hal.porZon, adjeas.porAdj)
      annotation (Line(points={{19,5},{19,0},{33,0}}, color={191,0,0}));
  connect(temSen.port, wes.porZon) annotation (Line(points={{-2,-54},{-2,-44},{-46,
            -44},{-46,5},{-55,5}},         color={191,0,0}));
  connect(temSen1.port, adjeas.porAdj)
    annotation (Line(points={{24,-78},{24,0},{33,0}}, color={191,0,0}));
  connect(temSen.T, wesTdb) annotation (Line(points={{18,-54},{18,-54},{96,-54},{96,
            -78},{216,-78},{216,-100},{250,-100}},           color={0,0,127}));
  connect(temSen1.T, halTdb) annotation (Line(points={{44,-78},{44,-80},{212,-80},
            {212,-120},{250,-120}},        color={0,0,127}));
  connect(eas.porZon, temSen2.port) annotation (Line(points={{89,5},{120,5},{120,-48},
            {54,-48},{54,-96},{66,-96}},         color={191,0,0}));
  connect(temSen2.T, easTdb) annotation (Line(points={{86,-96},{86,-96},{96,-96},{
            96,-82},{208,-82},{208,-140},{250,-140}},          color={0,0,
          127}));
  connect(winwes.porZon, wes.porZon) annotation (Line(points={{-55,-30},{
          -46,-30},{-46,5},{-55,5}}, color={191,0,0}));
  connect(wineas.porZon, eas.porZon) annotation (Line(points={{85,-30},{96,
          -30},{96,5},{89,5}}, color={191,0,0}));
  connect(weaPAtm, wea2Bus.weaPAtm)
    annotation (Line(points={{-260,240},{-166,240}}, color={0,0,127}));
  connect(weaTDewPoi, wea2Bus.weaTDewPoi) annotation (Line(points={{-260,
          210},{-236,210},{-236,234},{-166,234}}, color={0,0,127}));
  connect(weaTDryBul, wea2Bus.weaTDryBul) annotation (Line(points={{-260,
          180},{-234,180},{-234,228},{-166,228}}, color={0,0,127}));
  connect(weaRelHum, wea2Bus.weaRelHum) annotation (Line(points={{-260,150},
          {-232,150},{-232,222},{-166,222}}, color={0,0,127}));
  connect(weaNOpa, wea2Bus.weaNOpa) annotation (Line(points={{-260,120},{
          -230,120},{-230,216},{-166,216}}, color={0,0,127}));
  connect(weaCelHei, wea2Bus.weaCelHei) annotation (Line(points={{-260,90},
          {-228,90},{-228,210},{-166,210}}, color={0,0,127}));
  connect(weaNTot, wea2Bus.weaNTot) annotation (Line(points={{-260,60},{
          -226,60},{-226,204},{-166,204}}, color={0,0,127}));
  connect(weaWinSpe, wea2Bus.weaWinSpe) annotation (Line(points={{-260,30},
          {-224,30},{-224,198},{-166,198}}, color={0,0,127}));
  connect(weaWinDir, wea2Bus.weaWinDir) annotation (Line(points={{-260,0},{
          -222,0},{-222,192},{-166,192}}, color={0,0,127}));
  connect(weaHHorIR, wea2Bus.weaHHorIR) annotation (Line(points={{-260,-30},
          {-220,-30},{-220,186},{-166,186}}, color={0,0,127}));
  connect(weaHDirNor, wea2Bus.weaHDirNor) annotation (Line(points={{-260,
          -60},{-218,-60},{-218,180},{-166,180}}, color={0,0,127}));
  connect(weaHGloHor, wea2Bus.weaHGloHor) annotation (Line(points={{-260,
          -90},{-216,-90},{-216,174},{-166,174}}, color={0,0,127}));
  connect(weaHDifHor, wea2Bus.weaHDifHor) annotation (Line(points={{-260,
          -120},{-214,-120},{-214,168},{-166,168}}, color={0,0,127}));
  connect(weaTBlaSky, wea2Bus.weaTBlaSky) annotation (Line(points={{-260,
          -150},{-212,-150},{-212,162.2},{-166,162.2}}, color={0,0,127}));
  connect(weaTWetBul, wea2Bus.weaTWetBul) annotation (Line(points={{-260,
          -180},{-210,-180},{-210,156},{-166,156}}, color={0,0,127}));
  connect(weaSolZen, wea2Bus.weaSolZen) annotation (Line(points={{-260,-210},
          {-208,-210},{-208,149.8},{-166,149.8}}, color={0,0,127}));
  connect(weaCloTim, wea2Bus.weaCloTim) annotation (Line(points={{-260,-240},
          {-206,-240},{-206,144},{-166,144}}, color={0,0,127}));
  connect(weaSolTim, wea2Bus.weaSolTim) annotation (Line(points={{-260,-270},
          {-204,-270},{-204,138},{-166,138}}, color={0,0,127}));
  connect(wea2Bus.weaBus, extwes.weaBus) annotation (Line(
      points={{-120,190},{-114,190},{-110,190},{-110,30},{-77,30}},
      color={255,204,51},
      thickness=0.5));
  connect(wea2Bus.weaBus, winwes.weaBus) annotation (Line(
      points={{-120,190},{-110,190},{-110,-30},{-77,-30}},
      color={255,204,51},
      thickness=0.5));
  connect(wea2Bus.weaBus, wineas.weaBus) annotation (Line(
      points={{-120,190},{-110,190},{-110,40},{28,40},{28,-30},{63,-30}},
      color={255,204,51},
      thickness=0.5));
  connect(wea2Bus.weaBus, exteas.weaBus) annotation (Line(
      points={{-120,190},{-110,190},{-110,40},{28,40},{28,30},{63,30}},
      color={255,204,51},
      thickness=0.5));
    connect(convectiveHeater_wes.HeatOutput, wes.porZon) annotation (Line(points={
            {-39.6,-66},{-24,-66},{-24,-16},{-46,-16},{-46,5},{-55,5}}, color={191,
            0,0}));
    connect(convectiveHeater_eas.HeatOutput, eas.porZon) annotation (Line(points={
            {-39.6,-106},{-24,-106},{-12,-106},{-12,-16},{46,-16},{96,-16},{96,5},
            {89,5}}, color={191,0,0}));
    connect(conHeat_wes, convectiveHeater_wes.u) annotation (Line(points={{-40,
          -260},{-40,-260},{-40,-180},{-40,-176},{-102,-176},{-102,-66},{
          -62,-66}},
          color={0,0,127}));
    connect(conHeat_eas, convectiveHeater_eas.u) annotation (Line(points={{40,-260},
          {40,-260},{40,-160},{40,-154},{-94,-154},{-94,-106},{-62,-106}},
          color={0,0,127}));
    connect(convectiveHeater_wes.P_e, wesPhvac) annotation (Line(points={{-39,-72},
            {-2,-72},{-2,-110},{110,-110},{110,-86},{184,-86},{184,-160},{250,-160}},
          color={0,0,127}));
    connect(convectiveHeater_eas.P_e, easPhvac) annotation (Line(points={{-39,-112},
            {-39,-112},{-10,-112},{-10,-118},{114,-118},{114,-90},{176,-90},{176,-200},
            {250,-200}}, color={0,0,127}));
  connect(add.y,Ptot)
    annotation (Line(points={{231,-240},{250,-240}}, color={0,0,127}));
  connect(add.u1, wesPhvac) annotation (Line(points={{208,-232},{184,-232},
          {184,-160},{250,-160}}, color={0,0,127}));
  connect(conHeat_hal, convectiveHeater_hal.u) annotation (Line(points={{0,-260},
          {0,-260},{0,-166},{0,-164},{-98,-164},{-98,-86},{-62,-86}},
        color={0,0,127}));
  connect(convectiveHeater_hal.P_e, halPhvac) annotation (Line(points={{-39,
          -92},{-6,-92},{-6,-114},{112,-114},{112,-88},{180,-88},{180,-180},
          {250,-180}}, color={0,0,127}));
  connect(add.u2, halPhvac) annotation (Line(points={{208,-240},{180,-240},
          {180,-180},{250,-180}}, color={0,0,127}));
  connect(add.u3, easPhvac) annotation (Line(points={{208,-248},{176,-248},
          {176,-200},{250,-200}}, color={0,0,127}));
  connect(convectiveHeater_hal.HeatOutput, adjeas.porAdj) annotation (Line(
        points={{-39.6,-86},{-18,-86},{-18,-14},{24,-14},{24,0},{33,0}},
        color={191,0,0}));
    annotation (Diagram(coordinateSystem(preserveAspectRatio=false, extent={{-240,
            -240},{240,260}}),   graphics={
          Rectangle(
            extent={{-130,124},{138,-122}},
            lineColor={0,0,0},
            lineThickness=1,
            fillPattern=FillPattern.Solid,
            fillColor={255,255,255}),
          Text(
            extent={{64,-122},{136,-138}},
            lineColor={0,0,0},
            lineThickness=1,
            fillColor={255,255,255},
            fillPattern=FillPattern.Solid,
          textString="Reduced Order Model"),
          Text(
            extent={{-164,134},{-120,122}},
            lineColor={0,0,0},
            lineThickness=1,
            fillColor={255,255,255},
            fillPattern=FillPattern.Solid,
            textString="Weather Input",
            fontSize=12),
          Rectangle(
            extent={{-118,132},{-102,114}},
            lineColor={255,255,255},
            fillColor={0,0,0},
            fillPattern=FillPattern.Solid),
          Rectangle(
            extent={{-50,132},{-34,114}},
            lineColor={255,255,255},
            fillColor={0,0,0},
            fillPattern=FillPattern.Solid),
          Text(
            extent={{-32,136},{46,122}},
            lineColor={0,0,0},
            lineThickness=1,
            fillColor={255,255,255},
            fillPattern=FillPattern.Solid,
            fontSize=12,
            textString="Internal Load West Input"),
          Rectangle(
            extent={{-8,9},{8,-9}},
            lineColor={255,255,255},
            fillColor={0,0,0},
            fillPattern=FillPattern.Solid,
            origin={138,103},
            rotation=90),
          Text(
            extent={{138,122},{216,108}},
            lineColor={0,0,0},
            lineThickness=1,
            fillColor={255,255,255},
            fillPattern=FillPattern.Solid,
            fontSize=12,
            textString="Internal Load Hall Input"),
          Text(
            extent={{138,44},{216,30}},
            lineColor={0,0,0},
            lineThickness=1,
            fillColor={255,255,255},
            fillPattern=FillPattern.Solid,
            fontSize=12,
            textString="Internal Load East Input"),
          Rectangle(
            extent={{-8,9},{8,-9}},
            lineColor={255,255,255},
            fillColor={0,0,0},
            fillPattern=FillPattern.Solid,
            origin={138,25},
            rotation=90),
          Rectangle(
            extent={{-11.5,9.5},{11.5,-9.5}},
            lineColor={255,255,255},
            fillColor={0,0,0},
            fillPattern=FillPattern.Solid,
            origin={137.5,-84.5},
            rotation=90),
          Text(
            extent={{138,-62},{216,-76}},
            lineColor={0,0,0},
            lineThickness=1,
            fillColor={255,255,255},
            fillPattern=FillPattern.Solid,
            fontSize=12,
          textString="Measurement Outputs"),
          Rectangle(
            extent={{-8,9},{8,-9}},
            lineColor={255,255,255},
            fillColor={0,0,0},
            fillPattern=FillPattern.Solid,
            origin={-98,-123},
            rotation=180),
          Text(
            extent={{-96,-124},{-20,-136}},
            lineColor={0,0,0},
            lineThickness=1,
            fillColor={255,255,255},
            fillPattern=FillPattern.Solid,
            fontSize=12,
            textString="Control Signals")}),
                                  Icon(coordinateSystem(preserveAspectRatio=false,
            extent={{-240,-240},{240,260}}),
                                       graphics={
        Rectangle(
          extent={{-240,260},{240,-280}},
          lineColor={0,0,0},
          fillColor={255,255,255},
          fillPattern=FillPattern.Solid),
          Rectangle(
            extent={{-80,-30},{80,26}},
            lineColor={95,95,95},
            fillColor={95,95,95},
            fillPattern=FillPattern.Solid),
          Rectangle(
            extent={{-74,18},{-24,-20}},
            pattern=LinePattern.None,
            lineColor={117,148,176},
            fillColor={170,213,255},
            fillPattern=FillPattern.Sphere),
          Rectangle(
            extent={{-80,16},{-74,-18}},
            lineColor={95,95,95},
            fillColor={255,255,255},
            fillPattern=FillPattern.Solid),
          Rectangle(
            extent={{-78,16},{-76,-18}},
            lineColor={95,95,95},
            fillColor={170,213,255},
            fillPattern=FillPattern.Solid),
          Rectangle(
            extent={{24,18},{74,-20}},
            pattern=LinePattern.None,
            lineColor={117,148,176},
            fillColor={170,213,255},
            fillPattern=FillPattern.Sphere),
          Rectangle(
            extent={{-16,18},{16,-20}},
            pattern=LinePattern.None,
            lineColor={117,148,176},
            fillColor={170,213,255},
            fillPattern=FillPattern.Sphere),
          Rectangle(
            extent={{74,16},{80,-18}},
            lineColor={95,95,95},
            fillColor={255,255,255},
            fillPattern=FillPattern.Solid),
          Rectangle(
            extent={{76,16},{78,-18}},
            lineColor={95,95,95},
            fillColor={170,213,255},
            fillPattern=FillPattern.Solid),
          Text(
            extent={{20,100},{96,68}},
            lineColor={0,0,127},
            textString="TRoo"),
          Text(
            extent={{20,74},{96,42}},
            lineColor={0,0,127},
            textString="Xi"),
          Text(
            extent={{22,-44},{98,-76}},
            lineColor={0,0,127},
            textString="HDirWin")}));
  end MPC;

  package Modules "RC modules for multi-zone building"
    model modZon
      parameter Modelica.SIunits.Area A_zon = 1;
      parameter RapidMPC.Units.HeatCapacityCoefficient c_zon=2500
        annotation (Fixed=false);
      parameter RapidMPC.Units.HeatCapacityCoefficient c_int=150000
        annotation (Fixed=false);
      parameter RapidMPC.Units.HeatResistanceCoefficient r_int=0.2
        annotation (Fixed=false);
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor capZon(C = c_zon*A_zon)
        annotation (Placement(transformation(extent={{-24,-14},{-4,-34}})));

      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor capInt(C = c_int*A_zon)
        annotation (Placement(transformation(extent={{8,-14},{28,-34}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor resInt(R=r_int/
            A_zon)
        annotation (Placement(transformation(extent={{-8,6},{12,26}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preCon
        annotation (Placement(transformation(extent={{-60,60},{-40,80}})));
      Modelica.Blocks.Interfaces.RealInput intCon
        annotation (Placement(transformation(extent={{-140,50},{-100,90}})));
      Modelica.Blocks.Interfaces.RealInput intRad
        annotation (Placement(transformation(extent={{-140,-90},{-100,-50}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preRad
        annotation (Placement(transformation(extent={{-60,-80},{-40,-60}})));
      Modelica.Thermal.HeatTransfer.Interfaces.HeatPort_b porZon
        annotation (Placement(transformation(extent={{100,40},{120,60}}),
            iconTransformation(extent={{100,40},{120,60}})));
      Modelica.Thermal.HeatTransfer.Interfaces.HeatPort_b porInt annotation (
          Placement(transformation(extent={{100,-60},{120,-40}}),
            iconTransformation(extent={{100,-60},{120,-40}})));
    Modelica.Blocks.Math.Gain areCon(k=A_zon)
      annotation (Placement(transformation(extent={{-90,60},{-70,80}})));
    Modelica.Blocks.Math.Gain areRad(k=A_zon)
      annotation (Placement(transformation(extent={{-90,-80},{-70,-60}})));
    equation
      connect(resInt.port_b, capInt.port)
        annotation (Line(points={{12,16},{18,16},{18,-14}}, color={191,0,0}));
      connect(preCon.port, capZon.port) annotation (Line(points={{-40,70},{-30,
            70},{-30,-14},{-14,-14}},  color={191,0,0}));
      connect(preRad.port, capInt.port) annotation (Line(points={{-40,-70},{2,
            -70},{2,-14},{18,-14}},    color={191,0,0}));
      connect(capZon.port, resInt.port_a)
        annotation (Line(points={{-14,-14},{-14,16},{-8,16}},
                                                            color={191,0,0}));
      connect(capZon.port, porZon)
        annotation (Line(points={{-14,-14},{-14,50},{110,50}},color={191,0,0}));
      connect(capInt.port, porInt) annotation (Line(points={{18,-14},{32,-14},{
            48,-14},{48,-50},{110,-50}},
                                       color={191,0,0}));
    connect(intCon, areCon.u)
      annotation (Line(points={{-120,70},{-92,70}}, color={0,0,127}));
    connect(areCon.y, preCon.Q_flow)
      annotation (Line(points={{-69,70},{-60,70}}, color={0,0,127}));
    connect(intRad, areRad.u)
      annotation (Line(points={{-120,-70},{-92,-70}}, color={0,0,127}));
    connect(areRad.y, preRad.Q_flow)
      annotation (Line(points={{-69,-70},{-60,-70}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={
            Rectangle(
              extent={{-100,100},{100,-100}},
              lineColor={0,0,0},
              fillColor={255,255,255},
              fillPattern=FillPattern.Solid),
            Text(
              extent={{-44,36},{42,-34}},
              lineColor={0,0,0},
              textStyle={TextStyle.Bold},
              textString="modZon")}),                                Diagram(
          coordinateSystem(preserveAspectRatio=false)));
    end modZon;

    model modExt
      parameter Modelica.SIunits.Area A_ext = 1;
      parameter RapidMPC.Units.HeatResistanceCoefficient r_out=0.1
        annotation (Fixed=false);
      parameter RapidMPC.Units.HeatResistanceCoefficient r_zon=2
        annotation (Fixed=false);
      parameter RapidMPC.Units.HeatCapacityCoefficient c_bou=15000
        annotation (Fixed=false);
      parameter Modelica.SIunits.DimensionlessRatio abs = 0.6 annotation(Fixed=false);
      parameter Modelica.SIunits.Angle til = Modelica.Constants.pi/2;
      parameter Modelica.SIunits.Angle azi = 0;
      parameter Modelica.SIunits.Angle lat = 38*Modelica.Constants.pi/180;
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor capExt(C = c_bou*A_ext)
        annotation (Placement(transformation(extent={{40,-50},{60,-70}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor resExtZon(R = r_zon/A_ext)
        annotation (Placement(transformation(extent={{60,60},{80,80}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor resExtOut(R = r_out/A_ext)
        annotation (Placement(transformation(extent={{20,60},{40,80}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature preTdb
        annotation (Placement(transformation(extent={{-20,60},{0,80}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preIto
        annotation (Placement(transformation(extent={{22,-60},{42,-40}})));

      Modelica.Thermal.HeatTransfer.Interfaces.HeatPort_b porZon
        annotation (Placement(transformation(extent={{100,-10},{120,10}}),
            iconTransformation(extent={{100,-10},{120,10}})));
      Modelica.Blocks.Math.Gain absIto(k = abs*A_ext)
        annotation (Placement(transformation(extent={{-4,-60},{16,-40}})));
      Buildings.BoundaryConditions.WeatherData.Bus weaBus annotation (Placement(
            transformation(extent={{-120,-20},{-80,20}}), iconTransformation(
              extent={{-120,-10},{-100,10}})));
      Buildings.BoundaryConditions.SolarIrradiation.DiffuseIsotropic HDifTilIso(til=til)
        annotation (Placement(transformation(extent={{-60,-40},{-40,-20}})));
      Buildings.BoundaryConditions.SolarIrradiation.DirectTiltedSurface HDirTil(
        til=til,
        lat=lat,
        azi=azi)
        annotation (Placement(transformation(extent={{-60,-80},{-40,-60}})));
      Modelica.Blocks.Math.Add add
        annotation (Placement(transformation(extent={{-28,-58},{-12,-42}})));
    equation
      connect(preTdb.port, resExtOut.port_a)
        annotation (Line(points={{0,70},{0,70},{20,70}},      color={191,0,0}));
      connect(resExtZon.port_b, porZon)
        annotation (Line(points={{80,70},{110,70},{110,0}},color={191,0,0}));
      connect(absIto.y, preIto.Q_flow) annotation (Line(points={{17,-50},{17,
              -50},{22,-50}},  color={0,0,127}));
      connect(preIto.port, capExt.port)
        annotation (Line(points={{42,-50},{42,-50},{50,-50}}, color={191,0,0}));
      connect(weaBus.TDryBul, preTdb.T) annotation (Line(
          points={{-100,0},{-62,0},{-62,70},{-22,70}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus, HDifTilIso.weaBus) annotation (Line(
          points={{-100,0},{-80,0},{-80,-30},{-60,-30}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus, HDirTil.weaBus) annotation (Line(
          points={{-100,0},{-80,0},{-80,-70},{-60,-70}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(absIto.u, add.y)
        annotation (Line(points={{-6,-50},{-11.2,-50}}, color={0,0,127}));
      connect(HDifTilIso.H, add.u1) annotation (Line(points={{-39,-30},{-34,-30},
              {-34,-45.2},{-29.6,-45.2}}, color={0,0,127}));
      connect(HDirTil.H, add.u2) annotation (Line(points={{-39,-70},{-34,-70},{
              -34,-54.8},{-29.6,-54.8}}, color={0,0,127}));
      connect(resExtOut.port_b, capExt.port)
        annotation (Line(points={{40,70},{50,70},{50,-50}}, color={191,0,0}));
      connect(resExtZon.port_a, capExt.port)
        annotation (Line(points={{60,70},{50,70},{50,-50}}, color={191,0,0}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={
            Rectangle(
              extent={{-100,100},{100,-100}},
              lineColor={0,0,0},
              fillColor={255,255,255},
              fillPattern=FillPattern.Solid),
            Text(
              extent={{-38,38},{48,-32}},
              lineColor={0,0,0},
              textStyle={TextStyle.Bold},
              textString="modExt"),
            Rectangle(extent={{-100,100},{100,-100}}, lineColor={0,0,0})}),
                                                                     Diagram(
          coordinateSystem(preserveAspectRatio=false)));
    end modExt;

    model modWin
      parameter Modelica.SIunits.Area A_win = 1;
      parameter RapidMPC.Units.HeatResistanceCoefficient r_win=0.3
        annotation (Fixed=false);
      parameter Modelica.SIunits.DimensionlessRatio g = 0.75 annotation(Fixed=false);
      parameter Modelica.SIunits.Angle til = Modelica.Constants.pi/2;
      parameter Modelica.SIunits.Angle azi = 0;
      parameter Modelica.SIunits.Angle lat = 38*Modelica.Constants.pi/180;
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preSol
        annotation (Placement(transformation(extent={{36,-40},{56,-20}})));
      Modelica.Blocks.Math.Gain solWin(k=g*A_win)
        annotation (Placement(transformation(extent={{0,-40},{20,-20}})));
      Buildings.BoundaryConditions.SolarIrradiation.DiffuseIsotropic HDifTilIso(til=til)
        annotation (Placement(transformation(extent={{-70,-20},{-50,0}})));
      Buildings.BoundaryConditions.SolarIrradiation.DirectTiltedSurface HDirTil(
        til=til,
        lat=lat,
        azi=azi)
        annotation (Placement(transformation(extent={{-70,-60},{-50,-40}})));
      Modelica.Blocks.Math.Add add
        annotation (Placement(transformation(extent={{-38,-38},{-22,-22}})));
      Buildings.BoundaryConditions.WeatherData.Bus weaBus annotation (Placement(
            transformation(extent={{-120,-20},{-80,20}}), iconTransformation(
              extent={{-120,-10},{-100,10}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor resWin(R=r_win/A_win)
        annotation (Placement(transformation(extent={{30,20},{50,40}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature preTdb
        annotation (Placement(transformation(extent={{-10,20},{10,40}})));
      Modelica.Thermal.HeatTransfer.Interfaces.HeatPort_b porZon annotation (
          Placement(transformation(extent={{80,20},{100,40}}), iconTransformation(
              extent={{100,-10},{120,10}})));
    equation
      connect(solWin.y,preSol. Q_flow)
        annotation (Line(points={{21,-30},{36,-30}},   color={0,0,127}));
      connect(weaBus, HDifTilIso.weaBus) annotation (Line(
          points={{-100,0},{-78,0},{-78,-10},{-70,-10}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus, HDirTil.weaBus) annotation (Line(
          points={{-100,0},{-78,0},{-78,-50},{-70,-50}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(HDifTilIso.H, add.u1) annotation (Line(points={{-49,-10},{-44,-10},{-44,
              -25.2},{-39.6,-25.2}},  color={0,0,127}));
      connect(HDirTil.H, add.u2) annotation (Line(points={{-49,-50},{-44,-50},{-44,-34.8},
              {-39.6,-34.8}},          color={0,0,127}));
      connect(add.y,solWin. u)
        annotation (Line(points={{-21.2,-30},{-2,-30}},
                                                    color={0,0,127}));
      connect(preTdb.port, resWin.port_a)
        annotation (Line(points={{10,30},{10,30},{30,30}}, color={191,0,0}));
      connect(weaBus.TDryBul, preTdb.T) annotation (Line(
          points={{-100,0},{-78,0},{-78,30},{-12,30}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(resWin.port_b, porZon) annotation (Line(points={{50,30},{56,30},{60,30},
              {90,30}}, color={191,0,0}));
      connect(preSol.port, porZon)
        annotation (Line(points={{56,-30},{90,-30},{90,30}}, color={191,0,0}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={
            Rectangle(
              extent={{-100,100},{100,-100}},
              lineColor={0,0,0},
              fillColor={255,255,255},
              fillPattern=FillPattern.Solid),
            Text(
              extent={{-42,38},{44,-32}},
              lineColor={0,0,0},
              textStyle={TextStyle.Bold},
              textString="modWin"),
            Rectangle(extent={{-100,100},{100,-100}}, lineColor={0,0,0})}),
                                                                     Diagram(
          coordinateSystem(preserveAspectRatio=false)));
    end modWin;

    model modAdj
      parameter Modelica.SIunits.Area A_adj = 1;
      parameter RapidMPC.Units.HeatResistanceCoefficient r_adj=0.3
        annotation (Fixed=false);
      parameter RapidMPC.Units.HeatResistanceCoefficient r_zon=0.3
        annotation (Fixed=false);
      parameter RapidMPC.Units.HeatCapacityCoefficient c_bou=15000
        annotation (Fixed=false);
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor capBou(C = c_bou*A_adj)
        annotation (Placement(transformation(extent={{-10,-12},{10,-32}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor resBouAdj(R = r_adj/A_adj)
        annotation (Placement(transformation(extent={{-28,-10},{-8,10}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor resBouZon(R = r_zon/A_adj)
        annotation (Placement(transformation(extent={{6,-10},{26,10}})));
      Modelica.Thermal.HeatTransfer.Interfaces.HeatPort_a porAdj
        annotation (Placement(transformation(extent={{-120,-10},{-100,10}}),
            iconTransformation(extent={{-120,-10},{-100,10}})));
      Modelica.Thermal.HeatTransfer.Interfaces.HeatPort_b porZon
        annotation (Placement(transformation(extent={{100,-10},{120,10}}),
            iconTransformation(extent={{100,-10},{120,10}})));
    equation
      connect(resBouAdj.port_b, resBouZon.port_a)
        annotation (Line(points={{-8,0},{6,0}},   color={191,0,0}));
      connect(capBou.port, resBouZon.port_a)
        annotation (Line(points={{0,-12},{0,0},{6,0}},  color={191,0,0}));
      connect(resBouAdj.port_a, porAdj)
        annotation (Line(points={{-28,0},{-110,0}},  color={191,0,0}));
      connect(resBouZon.port_b, porZon)
        annotation (Line(points={{26,0},{110,0}},          color={191,0,0}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={
            Rectangle(
              extent={{-100,100},{100,-100}},
              lineColor={0,0,0},
              fillColor={255,255,255},
              fillPattern=FillPattern.Solid),
            Text(
              extent={{-40,38},{46,-32}},
              lineColor={0,0,0},
              textStyle={TextStyle.Bold},
              textString="modAdj"),
            Rectangle(extent={{-100,100},{100,-100}}, lineColor={0,0,0})}),
                                                                     Diagram(
          coordinateSystem(preserveAspectRatio=false)));
    end modAdj;

    model modGnd
      parameter Modelica.SIunits.Area A_gnd = 1;
      parameter RapidMPC.Units.HeatResistanceCoefficient r_out=0.3
        annotation (Fixed=false);
      parameter RapidMPC.Units.HeatResistanceCoefficient r_zon=0.3
        annotation (Fixed=false);
      parameter RapidMPC.Units.HeatCapacityCoefficient c_sla=200000
        annotation (Fixed=false);
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor capSla(C = c_sla*A_gnd)
        annotation (Placement(transformation(extent={{-10,-12},{10,-32}})));
      Modelica.Blocks.Interfaces.RealInput weaGnd
        annotation (Placement(transformation(extent={{-140,-20},{-100,20}}),
          iconTransformation(extent={{-140,-20},{-100,20}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature preGnd
        annotation (Placement(transformation(extent={{-68,-10},{-48,10}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor resGndOut(R = r_out/A_gnd)
        annotation (Placement(transformation(extent={{-28,-10},{-8,10}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor resGndZon(R = r_zon/A_gnd)
        annotation (Placement(transformation(extent={{6,-10},{26,10}})));
      Modelica.Thermal.HeatTransfer.Interfaces.HeatPort_b porZon
        annotation (Placement(transformation(extent={{100,-10},{120,10}}),
            iconTransformation(extent={{100,-10},{120,10}})));
    equation
      connect(preGnd.T, weaGnd)
        annotation (Line(points={{-70,0},{-70,0},{-120,0}},    color={0,0,127}));
      connect(preGnd.port, resGndOut.port_a)
        annotation (Line(points={{-48,0},{-48,0},{-28,0}},    color={191,0,0}));
      connect(resGndOut.port_b, resGndZon.port_a)
        annotation (Line(points={{-8,0},{6,0}},   color={191,0,0}));
      connect(capSla.port, resGndZon.port_a)
        annotation (Line(points={{0,-12},{0,0},{6,0}},  color={191,0,0}));
      connect(resGndZon.port_b, porZon)
        annotation (Line(points={{26,0},{110,0},{110,0}},  color={191,0,0}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={
            Rectangle(
              extent={{-100,100},{100,-100}},
              lineColor={0,0,0},
              fillColor={255,255,255},
              fillPattern=FillPattern.Solid),
            Text(
              extent={{-46,38},{40,-32}},
              lineColor={0,0,0},
              textStyle={TextStyle.Bold},
              textString="modGnd"),
            Rectangle(extent={{-100,100},{100,-100}}, lineColor={0,0,0})}),
                                                                     Diagram(
          coordinateSystem(preserveAspectRatio=false)));
    end modGnd;

    annotation ();
  end Modules;

  package BoundaryConditions
    "Package containing models for defining boundary conditions."

    block WeatherCalculator
    "Reader for TMY3 weather data or user input data.  Modification of Buildings.BoundaryConditions.WeatherData.ReaderTMY3."

      parameter Boolean computeWetBulbTemperature = true
      "If true, then this model computes the wet bulb temperature"
        annotation(Evaluate=true);

      parameter Boolean computeBlackSkyTemperature = true
      "If true, then this model computes the black sky temperature"
        annotation(Evaluate=true);
      //--------------------------------------------------------------
      // Atmospheric pressure
      Modelica.Blocks.Interfaces.RealInput pAtm_in(
        final quantity="Pressure",
        final unit="Pa",
        displayUnit="Pa") "Input pressure"
        annotation (Placement(transformation(extent={{-340,280},{-300,320}}),
            iconTransformation(extent={{-340,280},{-300,320}})));
      //--------------------------------------------------------------
      // Ceiling height
      Modelica.Blocks.Interfaces.RealInput ceiHei_in(
        final quantity="Height",
        final unit="m",
        displayUnit="m") "Input ceiling height"
        annotation (Placement(transformation(extent={{-340,-20},{-300,20}}),
            iconTransformation(extent={{-340,-20},{-300,20}})));
      //--------------------------------------------------------------
      // Total sky cover
      Modelica.Blocks.Interfaces.RealInput totSkyCov_in(
        min=0,
        max=1,
        unit="1") "Input total sky cover"
        annotation (Placement(transformation(extent={{-340,-80},{-300,-40}}),
            iconTransformation(extent={{-340,-80},{-300,-40}})));
      //--------------------------------------------------------------
      // Opaque sky cover
      Modelica.Blocks.Interfaces.RealInput opaSkyCov_in(
        min=0,
        max=1,
        unit="1") "Input opaque sky cover"
        annotation (Placement(transformation(extent={{-340,40},{-300,80}}),
            iconTransformation(extent={{-340,40},{-300,80}})));
      //--------------------------------------------------------------
      // Dry bulb temperature
      Modelica.Blocks.Interfaces.RealInput TDryBul_in(
        final quantity="ThermodynamicTemperature",
        final unit="K",
        displayUnit="degC") "Input dry bulb temperature"
        annotation (Placement(transformation(extent={{-340,160},{-300,200}}),
            iconTransformation(extent={{-340,160},{-300,200}})));

      //--------------------------------------------------------------
      // Dew point temperature
      Modelica.Blocks.Interfaces.RealInput TDewPoi_in(
        final quantity="ThermodynamicTemperature",
        final unit="K",
        displayUnit="degC") "Input dew point temperature"
        annotation (Placement(transformation(extent={{-340,220},{-300,260}}),
            iconTransformation(extent={{-340,220},{-300,260}})));

      //--------------------------------------------------------------
      // Relative humidity
      Modelica.Blocks.Interfaces.RealInput relHum_in(
        min=0,
        max=1,
        unit="1") "Input relative humidity"
        annotation (Placement(transformation(extent={{-340,100},{-300,140}}),
            iconTransformation(extent={{-340,100},{-300,140}})));
      //--------------------------------------------------------------
      // Wind speed
      Modelica.Blocks.Interfaces.RealInput winSpe_in(
        final quantity="Velocity",
        final unit="m/s",
        min=0) "Input wind speed"
        annotation (Placement(transformation(extent={{-340,-140},{-300,-100}}),
            iconTransformation(extent={{-340,-140},{-300,-100}})));
      //--------------------------------------------------------------
      // Wind direction
      Modelica.Blocks.Interfaces.RealInput winDir_in(
        final quantity="Angle",
        final unit="rad",
        displayUnit="deg") "Input wind direction"
        annotation (Placement(transformation(extent={{-340,-198},{-300,-158}}),
            iconTransformation(extent={{-340,-198},{-300,-158}})));
      //--------------------------------------------------------------
      // Infrared horizontal radiation
      Modelica.Blocks.Interfaces.RealInput HInfHor_in(
        final quantity="RadiantEnergyFluenceRate",
        final unit="W/m2") "Input infrared horizontal radiation"
        annotation (Placement(transformation(extent={{-340,-260},{-300,-220}}),
            iconTransformation(extent={{-340,-260},{-300,-220}})));
      //--------------------------------------------------------------
       parameter Buildings.BoundaryConditions.Types.RadiationDataSource HSou = Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HDirNor_HGloHor
      "Global, diffuse, and direct normal radiation"
         annotation (Evaluate=true, Dialog(group="Data source"));
      //--------------------------------------------------------------
      // Global horizontal radiation
      Modelica.Blocks.Interfaces.RealInput HGloHor_in(
        final quantity="RadiantEnergyFluenceRate",
        final unit="W/m2") if (HSou == Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HGloHor_HDifHor or HSou == Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HDirNor_HGloHor)
      "Input global horizontal radiation"
        annotation (Placement(transformation(extent={{-340,-380},{-300,-340}}),
            iconTransformation(extent={{-340,-380},{-300,-340}})));
      //--------------------------------------------------------------
      // Diffuse horizontal radiation
      Modelica.Blocks.Interfaces.RealInput HDifHor_in(
        final quantity="RadiantEnergyFluenceRate",
        final unit="W/m2") if (HSou == Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HGloHor_HDifHor or HSou == Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HDirNor_HDifHor)
      "Input diffuse horizontal radiation"
        annotation (Placement(transformation(extent={{-342,-440},{-302,-400}}),
            iconTransformation(extent={{-238,-200},{-198,-160}})));
      //--------------------------------------------------------------
      // Direct normal radiation
      Modelica.Blocks.Interfaces.RealInput HDirNor_in(final quantity="RadiantEnergyFluenceRate",
          final unit="W/m2") if
                              (HSou == Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HDirNor_HDifHor or HSou == Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HDirNor_HGloHor)
      "Input direct normal radiation"
        annotation (Placement(transformation(extent={{-340,-320},{-300,-280}}),
            iconTransformation(extent={{-340,-320},{-300,-280}})));

      //--------------------------------------------------------------

      parameter Modelica.SIunits.Angle lon(displayUnit="deg")= -122*3.14159/180
      "Longitude";
      parameter Modelica.SIunits.Angle lat(displayUnit="deg")= 38*3.14159/180
      "Latitude";
      parameter Modelica.SIunits.Time timZon(displayUnit="h")= -6*3600
      "Time zone";
      parameter Modelica.SIunits.Time modTimOffset(displayUnit="s") = 0
      "Local time at t = 0";
      Buildings.BoundaryConditions.WeatherData.Bus weaBus "Weather data bus"
        annotation (Placement(transformation(extent={{258,-18},{278,2}}),
            iconTransformation(extent={{190,-10},{210,10}})));

      parameter Buildings.BoundaryConditions.Types.SkyTemperatureCalculation
        calTSky=Buildings.BoundaryConditions.Types.SkyTemperatureCalculation.TemperaturesAndSkyCover
      "Computation of black-body sky temperature if enabled"
                                                    annotation (
        choicesAllMatching=true,
        Evaluate=true,
        Dialog(group="Sky temperature"));

      constant Real epsCos = 1e-6 "Small value to avoid division by 0";

    protected
      Buildings.BoundaryConditions.WeatherData.BaseClasses.CheckTemperature
        cheTemDryBul "Check dry bulb temperature "
        annotation (Placement(transformation(extent={{128,-208},{148,-188}})));
      Buildings.BoundaryConditions.WeatherData.BaseClasses.CheckTemperature
        cheTemDewPoi "Check dew point temperature"
        annotation (Placement(transformation(extent={{128,-248},{148,-228}})));
      Buildings.BoundaryConditions.WeatherData.BaseClasses.CheckPressure chePre
      "Check the air pressure"
        annotation (Placement(transformation(extent={{128,52},{148,72}})));
      Buildings.BoundaryConditions.WeatherData.BaseClasses.CheckSkyCover cheTotSkyCov
      "Check the total sky cover"
        annotation (Placement(transformation(extent={{128,-48},{148,-28}})));
      Buildings.BoundaryConditions.WeatherData.BaseClasses.CheckSkyCover cheOpaSkyCov
      "Check the opaque sky cover"
        annotation (Placement(transformation(extent={{128,-168},{148,-148}})));
      Buildings.BoundaryConditions.WeatherData.BaseClasses.CheckRadiation cheGloHorRad
      "Check the global horizontal radiation"
        annotation (Placement(transformation(extent={{128,152},{148,172}})));
      Buildings.BoundaryConditions.WeatherData.BaseClasses.CheckRadiation cheDifHorRad
      "Check the diffuse horizontal radiation"
        annotation (Placement(transformation(extent={{128,112},{148,132}})));
      Buildings.BoundaryConditions.WeatherData.BaseClasses.CheckRadiation cheDirNorRad
      "Check the direct normal radiation"
        annotation (Placement(transformation(extent={{128,192},{148,212}})));
      Buildings.BoundaryConditions.WeatherData.BaseClasses.CheckCeilingHeight cheCeiHei
      "Check the ceiling height"
        annotation (Placement(transformation(extent={{128,-128},{148,-108}})));
      Buildings.BoundaryConditions.WeatherData.BaseClasses.CheckWindSpeed cheWinSpe
      "Check the wind speed"
        annotation (Placement(transformation(extent={{128,-88},{148,-68}})));
      Buildings.BoundaryConditions.WeatherData.BaseClasses.CheckIRRadiation cheHorRad
      "Check the horizontal infrared irradiation"
        annotation (Placement(transformation(extent={{128,232},{148,252}})));
      Buildings.BoundaryConditions.WeatherData.BaseClasses.CheckWindDirection cheWinDir
      "Check the wind direction"
        annotation (Placement(transformation(extent={{128,-288},{148,-268}})));
      Buildings.BoundaryConditions.SkyTemperature.BlackBody TBlaSkyCom(final
          calTSky=calTSky) if computeBlackSkyTemperature
      "Computation of the black-body sky temperature"
            annotation (Placement(transformation(extent={{208,-228},{228,-208}})));
      DateRefTime modTim(refTime=modTimOffset) "Model time"
        annotation (Placement(transformation(extent={{-222,12},{-202,32}})));
      Buildings.BoundaryConditions.WeatherData.BaseClasses.LocalCivilTime locTim(
          final lon=lon, final timZon=timZon) "Local civil time"
        annotation (Placement(transformation(extent={{-152,-168},{-132,-148}})));
      Buildings.BoundaryConditions.WeatherData.BaseClasses.EquationOfTime eqnTim
      "Equation of time"
        annotation (Placement(transformation(extent={{-152,-128},{-132,-108}})));
      Buildings.BoundaryConditions.WeatherData.BaseClasses.SolarTime solTim
      "Solar time"
        annotation (Placement(transformation(extent={{-112,-148},{-92,-128}})));
      // Conditional connectors
      Modelica.Blocks.Interfaces.RealInput pAtm_in_internal(
        final quantity="Pressure",
        final unit="Pa",
        displayUnit="bar") "Needed to connect to conditional connector";
      Modelica.Blocks.Interfaces.RealInput ceiHei_in_internal(
        final quantity="Height",
        final unit="m",
        displayUnit="m") "Needed to connect to conditional connector";
      Modelica.Blocks.Interfaces.RealInput totSkyCov_in_internal(
        final quantity="1",
        min=0,
        max=1) "Needed to connect to conditional connector";
      Modelica.Blocks.Interfaces.RealInput opaSkyCov_in_internal(
        final quantity="1",
        min=0,
        max=1) "Needed to connect to conditional connector";
      Modelica.Blocks.Interfaces.RealInput TDryBul_in_internal(
        final quantity="ThermodynamicTemperature",
        final unit="K",
        displayUnit="degC") "Needed to connect to conditional connector";
      Modelica.Blocks.Interfaces.RealInput TDewPoi_in_internal(
        final quantity="ThermodynamicTemperature",
        final unit="K",
        displayUnit="degC") "Needed to connect to conditional connector";
      Modelica.Blocks.Interfaces.RealInput relHum_in_internal(
        final quantity="1",
        min=0,
        max=1) "Needed to connect to conditional connector";
      Modelica.Blocks.Interfaces.RealInput winSpe_in_internal(
        final quantity="Velocity",
        final unit="m/s") "Needed to connect to conditional connector";
      Modelica.Blocks.Interfaces.RealInput winDir_in_internal(
        final quantity="Angle",
        final unit="rad",
        displayUnit="deg") "Needed to connect to conditional connector";
      Modelica.Blocks.Interfaces.RealInput HGloHor_in_internal(
        final quantity="RadiantEnergyFluenceRate",
        final unit="W/m2") "Needed to connect to conditional connector";
      Modelica.Blocks.Interfaces.RealInput HDifHor_in_internal(
        final quantity="RadiantEnergyFluenceRate",
        final unit="W/m2") "Needed to connect to conditional connector";
      Modelica.Blocks.Interfaces.RealInput HDirNor_in_internal(
        final quantity="RadiantEnergyFluenceRate",
        final unit="W/m2") "Needed to connect to conditional connector";
      Modelica.Blocks.Interfaces.RealInput HInfHor_in_internal(
        final quantity="RadiantEnergyFluenceRate",
        final unit="W/m2") "Needed to connect to conditional connector";

      Buildings.BoundaryConditions.WeatherData.BaseClasses.CheckRelativeHumidity cheRelHum
        annotation (Placement(transformation(extent={{128,12},{148,32}})));
      Buildings.BoundaryConditions.SolarGeometry.BaseClasses.AltitudeAngle altAng
      "Solar altitude angle"
        annotation (Placement(transformation(extent={{-58,-266},{-38,-246}})));
       Buildings.BoundaryConditions.SolarGeometry.BaseClasses.ZenithAngle zenAng(final lat=
           lat) "Zenith angle"
        annotation (Placement(transformation(extent={{-94,-238},{-74,-218}})));
       Buildings.BoundaryConditions.SolarGeometry.BaseClasses.Declination decAng
      "Declination angle"
        annotation (Placement(transformation(extent={{-172,-228},{-152,-208}})));
       Buildings.BoundaryConditions.SolarGeometry.BaseClasses.SolarHourAngle solHouAng
        annotation (Placement(transformation(extent={{-172,-258},{-152,-238}})));
      Latitude latitude(final latitude=lat) "Latitude"
        annotation (Placement(transformation(extent={{-210,-318},{-190,-298}})));
      Longitude longitude(final longitude=lon) "Longitude"
        annotation (Placement(transformation(extent={{-172,-288},{-152,-268}})));

      //---------------------------------------------------------------------------
      // Optional instanciation of a block that computes the wet bulb temperature.
      // This block may be needed for evaporative cooling towers.
      // By default, it is enabled. This introduces a nonlinear equation, but
      // we have not observed an increase in computing time because of this equation.
    Buildings.Utilities.Psychrometrics.TWetBul_TDryBulPhi tWetBul_TDryBulXi(
        redeclare package Medium = Buildings.Media.Air, TDryBul(displayUnit=
            "degC")) if                   computeWetBulbTemperature
      annotation (Placement(transformation(extent={{212,-74},{232,-54}})));

      //---------------------------------------------------------------------------
      // Conversion blocks for sky cover
      Buildings.BoundaryConditions.WeatherData.BaseClasses.CheckBlackBodySkyTemperature
                                                                                      cheTemBlaSky(TMin=0) if
           computeBlackSkyTemperature "Check black body sky temperature"
        annotation (Placement(transformation(extent={{208,-268},{228,-248}})));

      // Blocks that are added in order to set the name of the output signal,
      // which then is displayed in the GUI of the weather data connector.
      block Latitude "Generate constant signal of type Real"
        extends Modelica.Blocks.Icons.Block;

        parameter Modelica.SIunits.Angle latitude "Latitude";

        Modelica.Blocks.Interfaces.RealOutput y(
          unit="rad",
          displayUnit="deg") "Latitude of the location"
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
      equation
        y = latitude;
        annotation (
        Icon(coordinateSystem(
            preserveAspectRatio=true,
            extent={{-100,-100},{100,100}}), graphics={
            Text(
              extent={{-81,32},{84,-24}},
              lineColor={0,0,0},
                textString="Latitude")}),
        Diagram(coordinateSystem(
            preserveAspectRatio=false,
            extent={{-100,-100},{100,100}})),
        Documentation(info="<html>
<p>
Block to output the latitude of the location.
This block is added so that the latitude is displayed
with a comment in the GUI of the weather bus connector.
</p>
<h4>Implementation</h4>
<p>
If
<a href=\"modelica://Modelica.Blocks.Sources.Constant\">
Modelica.Blocks.Sources.Constant</a> where used, then
the comment for the latitude would be \"Connector of Real output signal\".
As this documentation string cannot be overwritten, a new block
was implemented.
</p>
</html>",     revisions="<html>
<ul>
<li>
January 4, 2016, by Michael Wetter:<br/>
First implementation.
</li>
</ul>
</html>"));
      end Latitude;

      block Longitude "Generate constant signal of type Real"
        extends Modelica.Blocks.Icons.Block;

        parameter Modelica.SIunits.Angle longitude "Longitude";

        Modelica.Blocks.Interfaces.RealOutput y(
          unit="rad",
          displayUnit="deg") "Longitude of the location"
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
      equation
        y = longitude;
        annotation (
        Icon(coordinateSystem(
            preserveAspectRatio=true,
            extent={{-100,-100},{100,100}}), graphics={
            Text(
              extent={{-81,32},{84,-24}},
              lineColor={0,0,0},
                textString="Longitude")}),
        Diagram(coordinateSystem(
            preserveAspectRatio=false,
            extent={{-100,-100},{100,100}})),
        Documentation(info="<html>
<p>
Block to output the longitude of the location.
This block is added so that the longitude is displayed
with a comment in the GUI of the weather bus connector.
</p>
<h4>Implementation</h4>
<p>
If
<a href=\"modelica://Modelica.Blocks.Sources.Constant\">
Modelica.Blocks.Sources.Constant</a> where used, then
the comment for the longitude would be \"Connector of Real output signal\".
As this documentation string cannot be overwritten, a new block
was implemented.
</p>
</html>",     revisions="<html>
<ul>
<li>
January 4, 2016, by Michael Wetter:<br/>
First implementation.
</li>
</ul>
</html>"));
      end Longitude;

    public
      Modelica.Blocks.Interfaces.RealOutput HDifHor
        annotation (Placement(transformation(extent={{300,350},{320,370}})));
    equation
      //---------------------------------------------------------------------------
      // Select atmospheric pressure connector
      connect(pAtm_in, pAtm_in_internal);
      connect(pAtm_in_internal, chePre.PIn);
      //---------------------------------------------------------------------------
      // Select ceiling height connector
      connect(ceiHei_in, ceiHei_in_internal);
      connect(ceiHei_in_internal, cheCeiHei.ceiHeiIn);

      //---------------------------------------------------------------------------
      // Select total sky cover connector
      connect(totSkyCov_in, totSkyCov_in_internal);
      connect(totSkyCov_in_internal, cheTotSkyCov.nIn);
      //---------------------------------------------------------------------------
      // Select opaque sky cover connector
      connect(opaSkyCov_in, opaSkyCov_in_internal);
      connect(opaSkyCov_in_internal, cheOpaSkyCov.nIn);

      //---------------------------------------------------------------------------
      // Select dew point temperature connector
      connect(TDewPoi_in, TDewPoi_in_internal);
      connect(TDewPoi_in_internal, cheTemDewPoi.TIn);
      //---------------------------------------------------------------------------
      // Select dry bulb temperature connector
      connect(TDryBul_in, TDryBul_in_internal);
      connect(TDryBul_in_internal, cheTemDryBul.TIn);
      //---------------------------------------------------------------------------
      // Select relative humidity connector
      connect(relHum_in, relHum_in_internal);
      connect(relHum_in_internal, cheRelHum.relHumIn);
      //---------------------------------------------------------------------------
      // Select wind speed connector
      connect(winSpe_in, winSpe_in_internal);
      connect(winSpe_in_internal, cheWinSpe.winSpeIn);
      //---------------------------------------------------------------------------
      // Select wind direction connector
      connect(winDir_in, winDir_in_internal);
      connect(winDir_in_internal, cheWinDir.nIn);
      //---------------------------------------------------------------------------
      // Select global horizontal radiation connector
      if HSou ==  Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HGloHor_HDifHor or HSou == Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HDirNor_HGloHor then
        connect(HGloHor_in, HGloHor_in_internal)
        "Get HGloHor using user input file";
      elseif HSou == Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HDirNor_HDifHor then
         HDirNor_in_internal*cos(zenAng.zen)+HDifHor_in_internal = HGloHor_in_internal
        "Calculate the HGloHor using HDirNor and HDifHor according to (A.4.14) and (A.4.15)";
      end if;
      connect(HGloHor_in_internal, cheGloHorRad.HIn);
      //---------------------------------------------------------------------------
      // Select diffuse horizontal radiation connector
      if HSou == Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HGloHor_HDifHor or HSou == Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HDirNor_HDifHor then
         connect(HDifHor_in, HDifHor_in_internal)
        "Get HDifHor using user input file";
      elseif  HSou == Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HDirNor_HGloHor then
          HGloHor_in_internal - HDirNor_in_internal*cos(zenAng.zen) = HDifHor_in_internal
        "Calculate the HGloHor using HDirNor and HDifHor according to (A.4.14) and (A.4.15)";
      end if;
      connect(HDifHor_in_internal, cheDifHorRad.HIn);
      //---------------------------------------------------------------------------
      // Select direct normal radiation connector
      if HSou == Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HDirNor_HGloHor or HSou == Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HDirNor_HDifHor then
         connect(HDirNor_in, HDirNor_in_internal)
        "Get HDirNor using user input file";
      elseif  HSou == Buildings.BoundaryConditions.Types.RadiationDataSource.Input_HGloHor_HDifHor then
          (HGloHor_in_internal -HDifHor_in_internal)/Buildings.Utilities.Math.Functions.smoothMax(x1=cos(zenAng.zen), x2=epsCos, deltaX=0.1*epsCos)
           = HDirNor_in_internal
        "Calculate the HDirNor using HGloHor and HDifHor according to (A.4.14) and (A.4.15)";
      end if;
      connect(HDirNor_in_internal, cheDirNorRad.HIn);

      //---------------------------------------------------------------------------
      // Select infrared radiation connector
      connect(HInfHor_in, HInfHor_in_internal);
      connect(HInfHor_in_internal, cheHorRad.HIn);
      //---------------------------------------------------------------------------
      connect(chePre.POut, weaBus.pAtm) annotation (Line(
          points={{149,62},{188,62},{188,-8},{268,-8}},
          color={0,0,127}), Text(
          string="%second",
          index=1,
          extent={{6,3},{6,3}}));
      connect(cheTotSkyCov.nOut, weaBus.nTot) annotation (Line(
          points={{149,-38},{188,-38},{188,-8},{268,-8}},
          color={0,0,127}), Text(
          string="%second",
          index=1,
          extent={{6,3},{6,3}}));
      connect(cheOpaSkyCov.nOut, weaBus.nOpa) annotation (Line(
          points={{149,-158},{188,-158},{188,-8},{268,-8}},
          color={0,0,127}), Text(
          string="%second",
          index=1,
          extent={{6,3},{6,3}}));
      connect(cheGloHorRad.HOut, weaBus.HGloHor) annotation (Line(
          points={{149,162},{188,162},{188,-8},{268,-8}},
          color={0,0,127}), Text(
          string="%second",
          index=1,
          extent={{6,3},{6,3}}));
      connect(cheDifHorRad.HOut, weaBus.HDifHor) annotation (Line(
          points={{149,122},{188,122},{188,-8},{268,-8}},
          color={0,0,127}), Text(
          string="%second",
          index=1,
          extent={{6,3},{6,3}}));
      connect(cheDirNorRad.HOut, weaBus.HDirNor) annotation (Line(
          points={{149,202},{188,202},{188,-8},{268,-8}},
          color={0,0,127}), Text(
          string="%second",
          index=1,
          extent={{6,3},{6,3}}));
      connect(cheCeiHei.ceiHeiOut, weaBus.celHei) annotation (Line(
          points={{149,-118},{188,-118},{188,-8},{268,-8}},
          color={0,0,127}), Text(
          string="%second",
          index=1,
          extent={{6,3},{6,3}}));
      connect(cheWinSpe.winSpeOut, weaBus.winSpe) annotation (Line(
          points={{149,-78},{188,-78},{188,-8},{268,-8}},
          color={0,0,127}), Text(
          string="%second",
          index=1,
          extent={{6,3},{6,3}}));
      connect(cheHorRad.HOut, weaBus.HHorIR) annotation (Line(
          points={{149,242},{188,242},{188,-8},{268,-8}},
          color={0,0,127}), Text(
          string="%second",
          index=1,
          extent={{6,3},{6,3}}));
      connect(cheWinDir.nOut, weaBus.winDir) annotation (Line(
          points={{149,-278},{248,-278},{248,-8},{268,-8}},
          color={0,0,127}), Text(
          string="%second",
          index=1,
          extent={{6,3},{6,3}}));

      connect(eqnTim.eqnTim, solTim.equTim) annotation (Line(
          points={{-131,-118},{-120,-118},{-120,-132},{-114,-132}},
          color={0,0,127}));
      connect(locTim.locTim, solTim.locTim) annotation (Line(
          points={{-131,-158},{-120,-158},{-120,-143.4},{-114,-143.4}},
          color={0,0,127}));

      connect(cheTemDewPoi.TOut, weaBus.TDewPoi) annotation (Line(
          points={{149,-238},{248,-238},{248,-8},{268,-8}},
          color={0,0,127}), Text(
          string="%second",
          index=1,
          extent={{6,3},{6,3}}));

      connect(cheRelHum.relHumOut, weaBus.relHum) annotation (Line(
          points={{149,22},{248,22},{248,-8},{268,-8}},
          color={0,0,127}), Text(
          string="%second",
          index=1,
          extent={{6,3},{6,3}}));
      connect(cheTemDryBul.TOut, weaBus.TDryBul) annotation (Line(
          points={{149,-198},{248,-198},{248,-8},{268,-8}},
          color={0,0,127}), Text(
          string="%second",
          index=1,
          extent={{6,3},{6,3}}));
      connect(decAng.decAng, zenAng.decAng)
                                      annotation (Line(
          points={{-151,-218},{-96,-218},{-96,-222.6}},
          color={0,0,127}));
      connect(solHouAng.solHouAng, zenAng.solHouAng)  annotation (Line(
          points={{-151,-248},{-142,-248},{-142,-232.8},{-96,-232.8}},
          color={0,0,127}));
      connect(solHouAng.solTim, solTim.solTim) annotation (Line(
          points={{-174,-248},{-186,-248},{-186,-180},{-52,-180},{-52,-138},{
            -91,-138}},
          color={0,0,127}));
      connect(zenAng.zen, altAng.zen) annotation (Line(
          points={{-73,-228},{-72,-228},{-72,-256},{-60,-256}},
          color={0,0,127}));

      // Connectors for wet bulb temperature.
      // These are removed if computeWetBulbTemperature = false
      connect(chePre.POut, tWetBul_TDryBulXi.p) annotation (Line(
          points={{149,62},{188,62},{188,-72},{211,-72}},
          color={0,0,127}));
      connect(tWetBul_TDryBulXi.TWetBul, weaBus.TWetBul) annotation (Line(
          points={{233,-64},{248,-64},{248,-8},{260,-8},{268,-8}},
          color={0,0,127}), Text(
          string="%second",
          index=1,
          extent={{6,3},{6,3}}));
      connect(cheTemDryBul.TOut, tWetBul_TDryBulXi.TDryBul) annotation (Line(
          points={{149,-198},{188,-198},{188,-56},{211,-56}},
          color={0,0,127}));
      connect(cheRelHum.relHumOut, tWetBul_TDryBulXi.phi) annotation (Line(
          points={{149,22},{176,22},{176,-64},{211,-64}},
          color={0,0,127}));

      // Connectors for black sky temperature.
      // These are removed if computeBlackSkyTemperature = false
      connect(cheOpaSkyCov.nOut, TBlaSkyCom.nOpa) annotation (Line(
          points={{149,-158},{188,-158},{188,-221},{206,-221}},
          color={0,0,127}));
      connect(cheHorRad.HOut, TBlaSkyCom.HHorIR) annotation (Line(
          points={{149,242},{188,242},{188,-226},{206,-226}},
          color={0,0,127}));
      connect(cheTemDryBul.TOut, TBlaSkyCom.TDryBul) annotation (Line(
          points={{149,-198},{188,-198},{188,-210},{206,-210}},
          color={0,0,127}));
      connect(TBlaSkyCom.TDewPoi, cheTemDewPoi.TOut) annotation (Line(
          points={{206,-215},{188,-215},{188,-238},{149,-238}},
          color={0,0,127}));
      connect(TBlaSkyCom.TBlaSky, cheTemBlaSky.TIn);
      connect(cheTemBlaSky.TOut, weaBus.TBlaSky) annotation (Line(points={{229,
            -258},{229,-258},{248,-258},{248,-8},{268,-8}},
                                                      color={0,0,127}));

      connect(altAng.alt, weaBus.solAlt) annotation (Line(
          points={{-37,-256},{-24,-256},{-24,-296},{274,-296},{274,-8},{268,-8}},
          color={0,0,127}));
      connect(zenAng.zen, weaBus.solZen) annotation (Line(
          points={{-73,-228},{-72,-228},{-72,-298},{276,-298},{276,-8},{268,-8}},
          color={0,0,127}));
      connect(decAng.decAng, weaBus.solDec) annotation (Line(
          points={{-151,-218},{-151,-224},{-108,-224},{-108,-300},{278,-300},{
            278,-8},{268,-8}},
          color={0,0,127}));
      connect(solHouAng.solHouAng, weaBus.solHouAng) annotation (Line(
          points={{-151,-248},{-151,-248},{-124,-248},{-124,-302},{280,-302},{
            280,-144},{280,-8},{268,-8}},
          color={0,0,127}));
      connect(longitude.y, weaBus.lon) annotation (Line(
          points={{-151,-278},{-138,-278},{-138,-304},{282,-304},{282,-8},{268,
            -8}},
          color={0,0,127}));
      connect(latitude.y, weaBus.lat) annotation (Line(
          points={{-189,-308},{-184,-308},{-184,-306},{284,-306},{284,-8},{268,
            -8}},
          color={0,0,127}));
    connect(modTim.y, eqnTim.nDay) annotation (Line(points={{-201,22},{-192,22},
            {-178,22},{-178,-118},{-154,-118}}, color={0,0,127}));
    connect(modTim.y, locTim.cloTim) annotation (Line(points={{-201,22},{-190,
            22},{-178,22},{-178,-158},{-154,-158}}, color={0,0,127}));
    connect(modTim.y, decAng.nDay) annotation (Line(points={{-201,22},{-116,22},
            {-34,22},{-34,-194},{-182,-194},{-182,-218},{-174,-218}},
                                                                    color={0,0,
            127}));
    connect(modTim.y, weaBus.cloTim) annotation (Line(points={{-201,22},{-116,
            22},{-14,22},{-14,-8},{268,-8}},
                                     color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(solTim.solTim, weaBus.solTim) annotation (Line(points={{-91,-138},{
            -14,-138},{-14,-8},{268,-8}},
                                      color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
      annotation (
        defaultComponentName="weaDat",
        Icon(coordinateSystem(
            preserveAspectRatio=false,
            extent={{-200,-200},{200,200}},
            initialScale=0.05), graphics={
            Rectangle(
              extent={{-200,200},{200,-200}},
              lineColor={124,142,255},
              fillColor={39,45,81},
              fillPattern=FillPattern.Solid),
            Text(
              extent={{-162,270},{138,230}},
              textString="%name",
              lineColor={0,0,255}),
            Ellipse(
              extent={{-146,154},{28,-20}},
              lineColor={255,220,220},
              lineThickness=1,
              fillPattern=FillPattern.Sphere,
              fillColor={215,215,215}),
            Ellipse(
              extent={{-62,-74},{-58,-78}},
              lineColor={255,220,220},
              lineThickness=1,
              fillPattern=FillPattern.Sphere,
              fillColor={255,255,170}),
            Ellipse(
              extent={{-66,184},{-62,180}},
              lineColor={255,220,220},
              lineThickness=1,
              fillPattern=FillPattern.Sphere,
              fillColor={255,255,170}),
            Ellipse(
              extent={{62,182},{66,178}},
              lineColor={255,220,220},
              lineThickness=1,
              fillPattern=FillPattern.Sphere,
              fillColor={255,255,170}),
            Ellipse(
              extent={{156,190},{160,186}},
              lineColor={255,220,220},
              lineThickness=1,
              fillPattern=FillPattern.Sphere,
              fillColor={255,255,170}),
            Ellipse(
              extent={{56,-56},{60,-60}},
              lineColor={255,220,220},
              lineThickness=1,
              fillPattern=FillPattern.Sphere,
              fillColor={255,255,170}),
            Ellipse(
              extent={{118,-184},{122,-188}},
              lineColor={255,220,220},
              lineThickness=1,
              fillPattern=FillPattern.Sphere,
              fillColor={255,255,170}),
            Ellipse(
              extent={{154,-116},{158,-120}},
              lineColor={255,220,220},
              lineThickness=1,
              fillPattern=FillPattern.Sphere,
              fillColor={255,255,170}),
            Ellipse(
              extent={{-156,-28},{-152,-32}},
              lineColor={255,220,220},
              lineThickness=1,
              fillPattern=FillPattern.Sphere,
              fillColor={255,255,170}),
            Ellipse(
              extent={{148,-20},{152,-24}},
              lineColor={255,220,220},
              lineThickness=1,
              fillPattern=FillPattern.Sphere,
              fillColor={255,255,170}),
            Ellipse(
              extent={{148,116},{152,112}},
              lineColor={255,220,220},
              lineThickness=1,
              fillPattern=FillPattern.Sphere,
              fillColor={255,255,170}),
            Ellipse(
              extent={{-168,136},{-164,132}},
              lineColor={255,220,220},
              lineThickness=1,
              fillPattern=FillPattern.Sphere,
              fillColor={255,255,170}),
            Ellipse(
              extent={{8,-160},{12,-164}},
              lineColor={255,220,220},
              lineThickness=1,
              fillPattern=FillPattern.Sphere,
              fillColor={255,255,170}),
            Ellipse(
              extent={{-146,-152},{-142,-156}},
              lineColor={255,220,220},
              lineThickness=1,
              fillPattern=FillPattern.Sphere,
              fillColor={255,255,170}),
            Ellipse(
              extent={{86,56},{90,52}},
              lineColor={255,220,220},
              lineThickness=1,
              fillPattern=FillPattern.Sphere,
              fillColor={255,255,170})}),
        Documentation(info="<html>
<p>
This component reads TMY3 weather data (Wilcox and Marion, 2008) or user specified weather data.
The weather data format is the Typical Meteorological Year (TMY3)
as obtained from the EnergyPlus web site at
<a href=\"http://energyplus.net/weather\">
http://energyplus.net/weather</a>. These
data, which are in the EnergyPlus format, need to be converted as described
in the next paragraph.
</p>
<!-- ============================================== -->
<h4>Output to weaBus</h4>
<p>
The following variables serve as output and are accessible via <code>weaBus</code>:
</p>
<table summary=\"summary\" border=\"1\" cellspacing=\"0\" cellpadding=\"2\" style=\"border-collapse:collapse;\">
<!-- ============================================== -->
<tr>
  <th>Name
  </th>
  <th>Unit
  </th>
  <th>Description
  </th>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>HDifHor</code>
  </td>
  <td>
    W/m2
  </td>
  <td>
    Horizontal diffuse solar radiation.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>HDifNor</code>
  </td>
  <td>
    W/m2
  </td>
  <td>
    Direct normal radiation.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>HGloHor</code>
  </td>
  <td>
    W/m2
  </td>
  <td>
    Horizontal global radiation.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>HHorIR</code>
  </td>
  <td>
    W/m2
  </td>
  <td>
    Horizontal infrared irradiation.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>TBlaSky</code>
  </td>
  <td>
    K
  </td>
  <td>
    Output temperature.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>TDewPoi</code>
  </td>
  <td>
    K
  </td>
  <td>
    Dew point temperature.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>TDryBul</code>
  </td>
  <td>
    K
  </td>
  <td>
    Dry bulb temperature at ground level.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>TWetBul</code>
  </td>
  <td>
    K
  </td>
  <td>
    Wet bulb temperature.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>celHei</code>
  </td>
  <td>
    m
  </td>
  <td>
    Ceiling height.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>cloTim</code>
  </td>
  <td>
    s
  </td>
  <td>
    One-based day number in seconds.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>lat</code>
  </td>
  <td>
    rad
  </td>
  <td>
  Latitude of the location.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>lon</code>
  </td>
  <td>
    rad
  </td>
  <td>
  Longitude of the location.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>nOpa</code>
  </td>
  <td>
    1
  </td>
  <td>
  Opaque sky cover [0, 1].
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>nTot</code>
  </td>
  <td>
    1
  </td>
  <td>
   Total sky Cover [0, 1].
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>pAtm</code>
  </td>
  <td>
    Pa
  </td>
  <td>
    Atmospheric pressure.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>relHum</code>
  </td>
  <td>
    1
  </td>
  <td>
    Relative humidity.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>solAlt</code>
  </td>
  <td>
    rad
  </td>
  <td>
    Altitude angle.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>solDec</code>
  </td>
  <td>
    rad
  </td>
  <td>
    Declination angle.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>solHouAng</code>
  </td>
  <td>
    rad
  </td>
  <td>
    Solar hour angle.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>solTim</code>
  </td>
  <td>
    s
  </td>
  <td>
    Solar time.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>solZen</code>
  </td>
  <td>
    rad
  </td>
  <td>
    Zenith angle.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>winDir</code>
  </td>
  <td>
    rad
  </td>
  <td>
    Wind direction.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    <code>winSpe</code>
  </td>
  <td>
    m/s
  </td>
  <td>
    Wind speed.
  </td>
</tr>
</table>
<!-- ============================================== -->
<h4>Adding new weather data</h4>
<p>
To add new weather data, proceed as follows:
</p>
<ol>
<li>
Download the weather data file with the <code>epw</code> extension from
<a href=\"http://energyplus.net/weather\">
http://energyplus.net/weather</a>.
</li>
<li>
Add the file to <code>Buildings/Resources/weatherdata</code> (or to any directory
for which you have write permission).
</li>
<li>
On a console window, type<pre>
  cd Buildings/Resources/weatherdata
  java -jar ../bin/ConvertWeatherData.jar inputFile.epw
</pre>
This will generate the weather data file <code>inputFile.mos</code>, which can be read
by the model
<a href=\"modelica://Buildings.BoundaryConditions.WeatherData.ReaderTMY3\">
Buildings.BoundaryConditions.WeatherData.ReaderTMY3</a>.
</li>
</ol>
<!-- ============================================== -->
<h4>Location data that are read automatically from the weather data file</h4>
<p>
The following location data are automatically read from the weather file:
</p>
<ul>
<li>
The latitude of the weather station, <code>lat</code>,
</li>
<li>
the longitude of the weather station, <code>lon</code>, and
</li>
<li>
the time zone relative to Greenwich Mean Time, <code>timZone</code>.
</li>
</ul>
<!-- ============================================== -->
<h4>Wet bulb temperature</h4>
<p>
By default, the data bus contains the wet bulb temperature.
This introduces a nonlinear equation.
However, we have not observed an increase in computing time because
of this equation.
To disable the computation of the wet bulb temperature, set
<code>computeWetBulbTemperature=false</code>.
</p>
<!-- ============================================== -->
<h4>Using constant or user-defined input signals for weather data</h4>
<p>
This model has the option of using a constant value, using the data from the weather file,
or using data from an input connector for the following variables:
</p>
<ul>
<li>
The atmospheric pressure,
</li>
<li>
the ceiling height,
</li>
<li>
the total sky cover pressure,
</li>
<li>
the opaque sky cover pressure,
</li>
<li>
the dry bulb temperature,
</li>
<li>
the dew point temperature,
</li>
<li>
the sky black body temperature,
</li>
<li>
the relative humidity,
</li>
<li>
the wind direction,
</li>
<li>
the wind speed,
</li>
<li>
the global horizontal radiation, direct normal and diffuse horizontal radiation,
and
</li>
<li>
the infrared horizontal radiation.
</li>
</ul>
<p>
By default, all data are obtained from the weather data file,
except for the atmospheric pressure, which is set to the
parameter <code>pAtm=101325</code> Pascals.
</p>
<p>
The parameter <code>*Sou</code> configures the source of the data.
For the atmospheric pressure, temperatures, relative humidity, wind speed and wind direction,
the enumeration
<a href=\"modelica://Buildings.BoundaryConditions.Types.DataSource\">
Buildings.BoundaryConditions.Types.DataSource</a>
is used as follows:
</p>
<table summary=\"summary\" border=\"1\" cellspacing=\"0\" cellpadding=\"2\" style=\"border-collapse:collapse;\">
<!-- ============================================== -->
<tr>
  <th>Parameter <code>*Sou</code>
  </th>
  <th>Data used to compute weather data.
  </th>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    File
  </td>
  <td>
    Use data from file.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    Parameter
  </td>
  <td>
    Use value specified by the parameter.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    Input
  </td>
  <td>
    Use value from the input connector.
  </td>
</tr>
</table>
<p>
Because global, diffuse and direct radiation are related to each other, the parameter
<code>HSou</code> is treated differently.
It is set to a value of the enumeration
<a href=\"modelica://Buildings.BoundaryConditions.Types.RadiationDataSource\">
Buildings.BoundaryConditions.Types.RadiationDataSource</a>,
and allows the following configurations:
</p>
<table summary=\"summary\" border=\"1\" cellspacing=\"0\" cellpadding=\"2\" style=\"border-collapse:collapse;\">
<!-- ============================================== -->
<tr>
  <th>Parameter <code>HSou</code>
  </th>
  <th>Data used to compute weather data.
  </th>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    File
  </td>
  <td>
    Use data from file.
  </td>
</tr>
<!-- ============================================== -->
<tr>
  <td>
    Input_HGloHor_HDifHor
  </td>
  <td>
    Use global horizontal and diffuse horizontal radiation from input connector.
  </td>
</tr>
<tr>
  <td>
    Input_HDirNor_HDifHor
  </td>
  <td>
    Use direct normal and diffuse horizontal radiation from input connector.
  </td>
</tr>
<tr>
  <td>
    Input_HDirNor_HGloHor
  </td>
  <td>
    Use direct normal and global horizontal radiation from input connector.
  </td>
</tr>
</table>
<p>
<b>Notes</b>
</p>
<ol>
<li>
<p>
In HVAC systems, when the fan is off, changes in atmospheric pressure can cause small air flow rates
in the duct system due to change in pressure and hence in the mass of air that is stored
in air volumes (such as in fluid junctions or in the room model).
This may increase computing time. Therefore, the default value for the atmospheric pressure is set to a constant.
Furthermore, if the initial pressure of air volumes are different
from the atmospheric pressure, then fast pressure transients can happen in the first few seconds of the simulation.
This can cause numerical problems for the solver. To avoid this problem, set the atmospheric pressure to the
same value as the medium default pressure, which is typically set to the parameter <code>Medium.p_default</code>.
For medium models for moist air and dry air, the default is
<code>Medium.p_default=101325</code> Pascals.
</p>
</li>
<li>
<p>
Different units apply depending on whether data are obtained from a file, or
from a parameter or an input connector:
</p>
<ul>
<li>
When using TMY3 data from a file (e.g. <code>USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.mos</code>), the units must be the same as the original TMY3 file used by EnergyPlus (e.g.
<code>USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw</code>).
The TMY3 data used by EnergyPlus are in both SI units and non-SI units.
If <code>Resources/bin/ConvertWeatherData.jar</code> is used to convert the <code>.epw</code> file to an <code>.mos</code> file, the units of the TMY3 data are preserved and the file can be directly
used by this data reader.
The data reader will automatically convert units to the SI units used by Modelica.
For example, the dry bulb temperature <code>TDryBul</code> in TMY3 is in degree Celsius.
The data reader will automatically convert the data to Kelvin.
The wind direction <code>winDir</code> in TMY3 is degrees and will be automatically converted to radians.
</li>
<li>
When using data from a parameter or from an input connector,
the data must be in the SI units used by Modelica.
For instance, the unit must be
<code>Pa</code> for pressure,
<code>K</code> for temperature,
<code>W/m2</code> for solar radiations and
<code>rad</code> for wind direction.
</li>
</ul>
</li>
<li>
The ReaderTMY3 should only be used with TMY3 data. It contains a time shift for solar radiation data
that is explained below. This time shift needs to be removed if the user may want to
use the ReaderTMY3 for other weather data types.
</li>
</ol>
<h4>Implementation</h4>
<h5>Start and end data for annual weather data files</h5>
<p>
The TMY3 weather data, as well as the EnergyPlus weather data, start at 1:00 AM
on January 1, and provide hourly data until midnight on December 31.
Thus, the first entry for temperatures, humidity, wind speed etc. are values
at 1:00 AM and not at midnight. Furthermore, the TMY3 weather data files can have
values at midnight of December 31 that may be significantly different from the values
at 1:00 AM on January 1.
Since annual simulations require weather data that start at 0:00 on January 1,
data need to be provided for this hour. Due to the possibly large change in
weatherdata between 1:00 AM on January 1 and midnight at December 31,
the weather data files in the Buildings library do not use the data entry from
midnight at December 31 as the value for <i>t=0</i>. Rather, the
value from 1:00 AM on January 1 is duplicated and used for 0:00 on January 1.
To maintain a data record with <i>8760</i> hours, the weather data record from
midnight at December 31 is deleted.
These changes in the weather data file are done in the Java program that converts
EnergyPlus weather data file to Modelica weather data files, and which is described
below.
</p>
<h5>Time shift for solar radiation data</h5>
<p>
To read weather data from the TMY3 weather data file, there are
two data readers in this model. One data reader obtains all data
except solar radiation, and the other data reader reads only the
solar radiation data, shifted by <i>30</i> minutes.
The reason for this time shift is as follows:
The TMY3 weather data file contains for solar radiation the
\"...radiation received
on a horizontal surface during
the 60-minute period ending at
the timestamp.\"

Thus, as the figure below shows, a more accurate interpolation is obtained if
time is shifted by <i>30</i> minutes prior to reading the weather data.
</p>
<p align=\"center\">
<img alt=\"image\" src=\"modelica://Buildings/Resources/Images/BoundaryConditions/WeatherData/RadiationTimeShift.png\"
border=\"1\" />
</p>
<h4>References</h4>
<ul>
<li>
Wilcox S. and W. Marion. <i>Users Manual for TMY3 Data Sets</i>.
Technical Report, NREL/TP-581-43156, revised May 2008.
</li>
</ul>
</html>",     revisions="<html>
<ul>
<li>
April 21, 2016, by Michael Wetter:<br/>
Introduced <code>absFilNam</code> to avoid multiple calls to
<a href=\"modelica://Buildings.BoundaryConditions.WeatherData.BaseClasses.getAbsolutePath\">
Buildings.BoundaryConditions.WeatherData.BaseClasses.getAbsolutePath</a>.
This is for
<a href=\"https://github.com/lbl-srg/modelica-buildings/issues/506\">Buildings, #506</a>.
</li>
<li>
January 6, 2016, by Moritz Lauster:<br/>
Changed output <code>radHorIR</code> to <code>HHorIR</code>.
This is for
<a href=\"https://github.com/iea-annex60/modelica-annex60/issues/376\">#376</a>.
</li>
<li>
January 4, 2016, by Moritz Lauster:<br/>
Added a table in documentation with output variables accessible via <code>weaBus</code>.
This is for
<a href=\"https://github.com/iea-annex60/modelica-annex60/issues/376\">#376</a>.
</li>
<li>
December 15, 2015, by Michael Wetter:<br/>
Added the block <code>cheTemBlaSky</code>. This also allows to graphically
connect the black body sky temperature to the weather bus, which is required
in Dymola 2016 for the variable <code>weaBus.TBlaSky</code> to appear
in the graphical editor.
This is for
<a href=\"https://github.com/iea-annex60/modelica-annex60/issues/377\">#377</a>.
</li>
<li>
September 24, 2015, by Marcus Fuchs:<br/>
Replace annotation <code>__Dymola_loadSelector</code> by <code>loadSelector</code>
for MSL compliancy as reported by @tbeu at
<a href=\"https://github.com/RWTH-EBC/AixLib/pull/107\">RWTH-EBC/AixLib#107</a>
</li>
<li>
June 6, 2015, by Michael Wetter:<br/>
Removed redundant but consistent
<code>connect(TBlaSkyCom.TBlaSky, weaBus.TBlaSky)</code>
statement.
This avoids a warning if
<a href=\"modelica://Buildings.BoundaryConditions.SolarIrradiation.BaseClasses.Examples.SkyClearness\">
Buildings.BoundaryConditions.SolarIrradiation.BaseClasses.Examples.SkyClearness</a>
is translated in pedantic mode in Dymola 2016.
This is for
<a href=\"https://github.com/iea-annex60/modelica-annex60/issues/266\">#266</a>.
</li>
<li>
March 26, 2015, by Michael Wetter:<br/>
Added option to obtain the black body sky temperature
from a parameter or an input signal.
This is required for
<a href=\"modelica://Buildings.Rooms.Validation.MixedAirInitialization\">
Buildings.Rooms.Validation.MixedAirInitialization</a>.
</li>
<li>
October 17, 2014, by Michael Wetter:<br/>
Corrected error that led the total and opaque sky cover to be ten times
too low if its value was obtained from the parameter or the input connector.
For the standard configuration in which the sky cover is obtained from
the weather data file, the model was correct. This error only affected
the other two possible configurations.
</li>
<li>
September 12, 2014, by Michael Wetter:<br/>
Removed redundant connection <code>connect(conHorRad.HOut, cheHorRad.HIn);</code>.
</li>
<li>
May 30, 2014, by Michael Wetter:<br/>
Removed undesirable annotation <code>Evaluate=true</code>.
</li>
<li>
May 5, 2013, by Thierry S. Nouidui:<br/>
Added the option to use a constant, an input signal or the weather file as the source
for the ceiling height, the total sky cover, the opaque sky cover, the dew point temperature,
and the infrared horizontal radiation <code>HInfHor</code>.
</li>
<li>
October 8, 2013, by Michael Wetter:<br/>
Improved the algorithm that determines the absolute path of the file.
Now weather files are searched in the path specified, and if not found, the urls
<code>file://</code>, <code>modelica://</code> and <code>modelica://Buildings</code>
are added in this order to search for the weather file.
This allows using the data reader without having to specify an absolute path,
as long as the <code>Buildings</code> library
is on the <code>MODELICAPATH</code>.
This change was implemented in
<a href=\"modelica://Buildings.BoundaryConditions.WeatherData.BaseClasses.getAbsolutePath\">
Buildings.BoundaryConditions.WeatherData.BaseClasses.getAbsolutePath</a>
and improves this weather data reader.
</li>
<li>
May 2, 2013, by Michael Wetter:<br/>
Added function call to <code>getAbsolutePath</code>.
</li>
<li>
October 16, 2012, by Michael Wetter:<br/>
Added computation of the wet bulb temperature.
Computing the wet bulb temperature introduces a nonlinear
equation. As we have not observed an increase in computing time
because of computing the wet bulb temperature, it is computed
by default. By setting the parameter
<code>computeWetBulbTemperature=false</code>, the computation of the
wet bulb temperature can be removed.
Revised documentation.
</li>
<li>
August 11, 2012, by Wangda Zuo:<br/>
Renamed <code>radHor</code> to <code>radHorIR</code> and
improved the optional inputs for radiation data.
</li>
<li>
July 24, 2012, by Wangda Zuo:<br/>
Corrected the notes of SI unit requirements for input files.
</li>
<li>
July 13, 2012, by Michael Wetter:<br/>
Removed assignment of <code>HGloHor_in</code> in its declaration,
because this gives an overdetermined system if the input connector
is used.
Removed non-required assignments of attribute <code>displayUnit</code>.
</li>
<li>
February 25, 2012, by Michael Wetter:<br/>
Added subbus for solar position, which is needed by irradition and
shading model.
</li>
<li>
November 29, 2011, by Michael Wetter:<br/>
Fixed wrong display unit for <code>pAtm_in_internal</code> and
made propagation of parameter final.
</li>
<li>
October 27, 2011, by Wangda Zuo:<br/>
<ol>
<li>
Added optional connectors for dry bulb temperature, relative humidity, wind speed, wind direction, global horizontal radiation, diffuse horizontal radiation.<br/>
</li>
<li>
Separate the unit conversion for TMY3 data and data validity check.
</li>
</ol>
</li>
<li>
October 3, 2011, by Michael Wetter:<br/>
Propagated value for sky temperature calculation to make it accessible as a parameter.
</li>
<li>
July 20, 2011, by Michael Wetter:<br/>
Added the option to use a constant, an input signal or the weather file as the source
for the atmospheric pressure.
</li><li>
March 15, 2011, by Wangda Zuo:<br/>
Delete the wet bulb temperature since it may cause numerical problem.
</li>
<li>
March 7, 2011, by Wangda Zuo:<br/>
Added wet bulb temperature. Changed reader to read only needed columns.
Added explanation for 30 minutes shift for radiation data.
</li>
<li>
March 5, 2011, by Michael Wetter:<br/>
Changed implementation to obtain longitude and time zone directly
from weather file.
</li>
<li>
June 25, 2010, by Wangda Zuo:<br/>
First implementation.
</li>
</ul>
</html>"),
        Diagram(coordinateSystem(preserveAspectRatio=false,
         extent={{-300,-440},{300,300}})));
    end WeatherCalculator;

    block DateRefTime
    "Calculates the time of year with reference to a start time of the year for t = 0 in simulation time."
      extends Modelica.Blocks.Interfaces.SO;
      parameter Modelica.SIunits.Time refTime = 0;

    equation
      y = time + refTime;
      annotation (Icon(graphics={   Rectangle(
            extent={{-100,-100},{100,100}},
            lineColor={0,0,127},
            fillColor={255,255,255},
            fillPattern=FillPattern.Solid),
            Ellipse(extent={{-80,80},{80,-80}}, lineColor={160,160,164},
              fillColor={215,215,215},
              fillPattern=FillPattern.Solid),
            Line(points={{0,80},{0,60}}, color={160,160,164}),
            Line(points={{80,0},{60,0}}, color={160,160,164}),
            Line(points={{0,-80},{0,-60}}, color={160,160,164}),
            Line(points={{-80,0},{-60,0}}, color={160,160,164}),
            Line(points={{37,70},{26,50}}, color={160,160,164}),
            Line(points={{70,38},{49,26}}, color={160,160,164}),
            Line(points={{71,-37},{52,-27}}, color={160,160,164}),
            Line(points={{39,-70},{29,-51}}, color={160,160,164}),
            Line(points={{-39,-70},{-29,-52}}, color={160,160,164}),
            Line(points={{-71,-37},{-50,-26}}, color={160,160,164}),
            Line(points={{-71,37},{-54,28}}, color={160,160,164}),
            Line(points={{-38,70},{-28,51}}, color={160,160,164}),
            Line(
              points={{0,0},{-50,50}},
              thickness=0.5),
            Line(
              points={{0,0},{40,0}},
              thickness=0.5),
            Text(
              extent={{-34,-10},{42,-38}},
              lineColor={0,0,0},
              textString="mm/dd")}));
    end DateRefTime;

    model WeatherProcessor
      parameter Modelica.SIunits.Angle lon(displayUnit="deg")= -122*3.14159/180
      "Longitude";
      parameter Modelica.SIunits.Angle lat(displayUnit="deg")= 38*3.14159/180
      "Latitude";
      parameter Modelica.SIunits.Time timZon(displayUnit="h")= -6*3600
      "Time zone";
      parameter Modelica.SIunits.Time modTimOffset(displayUnit="s") = 0
      "Local time at t = 0";
    WeatherCalculator weaCal(
      lon=lon,
      lat=lat,
      timZon=timZon,
      modTimOffset=modTimOffset)
      annotation (Placement(transformation(extent={{-10,-8},{10,12}})));
      Modelica.Blocks.Interfaces.RealInput weaPAtm "Input pressure"
      annotation (Placement(transformation(extent={{-380,300},{-340,340}})));
      Modelica.Blocks.Interfaces.RealInput weaTDewPoi
      "Input dew point temperature"
      annotation (Placement(transformation(extent={{-380,240},{-340,280}})));
      Modelica.Blocks.Interfaces.RealInput weaTDryBul
      "Input dry bulb temperature"
      annotation (Placement(transformation(extent={{-380,178},{-340,218}})));
      Modelica.Blocks.Interfaces.RealInput weaRelHum "Input relative humidity"
      annotation (Placement(transformation(extent={{-380,118},{-340,158}})));
      Modelica.Blocks.Interfaces.RealInput weaNOpa "Input opaque sky cover"
      annotation (Placement(transformation(extent={{-380,58},{-340,98}})));
      Modelica.Blocks.Interfaces.RealInput weaCelHei "Input ceiling height"
      annotation (Placement(transformation(extent={{-380,-2},{-340,38}})));
      Modelica.Blocks.Interfaces.RealInput weaNTot "Input total sky cover"
      annotation (Placement(transformation(extent={{-380,-60},{-340,-20}})));
      Modelica.Blocks.Interfaces.RealInput weaWinSpe "Input wind speed"
      annotation (Placement(transformation(extent={{-380,-120},{-340,-80}})));
      Modelica.Blocks.Interfaces.RealInput weaWinDir "Input wind direction"
      annotation (Placement(transformation(extent={{-380,-184},{-340,-144}})));
      Modelica.Blocks.Interfaces.RealInput weaHHorIR
      "Input infrared horizontal radiation"
      annotation (Placement(transformation(extent={{-380,-242},{-340,-202}})));
      Modelica.Blocks.Interfaces.RealInput weaHDirNor
      "Input direct normal radiation"
      annotation (Placement(transformation(extent={{-380,-302},{-340,-262}})));
      Modelica.Blocks.Interfaces.RealInput weaHGloHor
      "Input global horizontal radiation"
      annotation (Placement(transformation(extent={{-380,-360},{-340,-320}})));
      Modelica.Blocks.Interfaces.RealOutput weaHDifHor
      annotation (Placement(transformation(extent={{340,310},{360,330}})));
      Modelica.Blocks.Interfaces.RealOutput weaCloTim
      annotation (Placement(transformation(extent={{340,68},{360,88}})));
      Modelica.Blocks.Interfaces.RealOutput weaSolTim
      annotation (Placement(transformation(extent={{340,8},{360,28}})));
      Buildings.BoundaryConditions.WeatherData.Bus weaBus "Weather data bus"
        annotation (Placement(transformation(extent={{36,-8},{56,12}})));
      Modelica.Blocks.Interfaces.RealOutput weaTBlaSky
      annotation (Placement(transformation(extent={{340,250},{360,270}})));
      Modelica.Blocks.Interfaces.RealOutput weaTWetBul
      annotation (Placement(transformation(extent={{340,190},{360,210}})));
      Modelica.Blocks.Interfaces.RealOutput weaSolZen
      annotation (Placement(transformation(extent={{340,130},{360,150}})));
    equation
    connect(weaCal.pAtm_in, weaPAtm) annotation (Line(points={{-16,17},{-60,17},
            {-60,320},{-360,320}}, color={0,0,127}));
    connect(weaCal.TDewPoi_in, weaTDewPoi) annotation (Line(points={{-16,14},{-62,
            14},{-62,260},{-360,260}}, color={0,0,127}));
    connect(weaCal.TDryBul_in, weaTDryBul) annotation (Line(points={{-16,11},{-64,
            11},{-64,198},{-360,198}}, color={0,0,127}));
    connect(weaCal.relHum_in, weaRelHum) annotation (Line(points={{-16,8},{-66,
            8},{-66,138},{-360,138}}, color={0,0,127}));
    connect(weaCal.opaSkyCov_in, weaNOpa) annotation (Line(points={{-16,5},{-68,
            5},{-68,78},{-360,78}}, color={0,0,127}));
    connect(weaCal.ceiHei_in, weaCelHei) annotation (Line(points={{-16,2},{-70,
            2},{-70,18},{-360,18}}, color={0,0,127}));
    connect(weaCal.totSkyCov_in, weaNTot) annotation (Line(points={{-16,-1},{-70,
            -1},{-70,-40},{-360,-40}}, color={0,0,127}));
    connect(weaCal.winSpe_in, weaWinSpe) annotation (Line(points={{-16,-4},{-68,
            -4},{-68,-100},{-360,-100}}, color={0,0,127}));
    connect(weaCal.winDir_in, weaWinDir) annotation (Line(points={{-16,-6.9},{-66,
            -6.9},{-66,-164},{-360,-164}}, color={0,0,127}));
    connect(weaCal.HInfHor_in, weaHHorIR) annotation (Line(points={{-16,-10},{-64,
            -10},{-64,-222},{-360,-222}}, color={0,0,127}));
    connect(weaCal.HDirNor_in, weaHDirNor) annotation (Line(points={{-16,-13},{
            -36,-13},{-62,-13},{-62,-282},{-360,-282}}, color={0,0,127}));
    connect(weaCal.HGloHor_in, weaHGloHor) annotation (Line(points={{-16,-16},{
            -60,-16},{-60,-340},{-360,-340}}, color={0,0,127}));
      connect(weaCal.weaBus, weaBus) annotation (Line(
          points={{10,2},{46,2}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%second",
          index=1,
          extent={{6,3},{6,3}}));
    connect(weaBus.HDifHor, weaHDifHor) annotation (Line(
        points={{46,2},{46,2},{46,320},{350,320}},
        color={255,204,51},
        thickness=0.5), Text(
        string="%first",
        index=-1,
        extent={{-6,3},{-6,3}}));
    connect(weaBus.cloTim, weaCloTim) annotation (Line(
        points={{46,2},{46,2},{46,78},{350,78}},
        color={255,204,51},
        thickness=0.5), Text(
        string="%first",
        index=-1,
        extent={{-6,3},{-6,3}}));
    connect(weaBus.solTim, weaSolTim) annotation (Line(
        points={{46,2},{46,2},{46,68},{46,18},{350,18}},
        color={255,204,51},
        thickness=0.5), Text(
        string="%first",
        index=-1,
        extent={{-6,3},{-6,3}}));
    connect(weaBus.TBlaSky, weaTBlaSky) annotation (Line(
        points={{46,2},{46,2},{46,146},{46,260},{350,260}},
        color={255,204,51},
        thickness=0.5), Text(
        string="%first",
        index=-1,
        extent={{-6,3},{-6,3}}));
    connect(weaBus.TWetBul, weaTWetBul) annotation (Line(
        points={{46,2},{46,2},{46,126},{46,200},{350,200}},
        color={255,204,51},
        thickness=0.5), Text(
        string="%first",
        index=-1,
        extent={{-6,3},{-6,3}}));
    connect(weaBus.solZen, weaSolZen) annotation (Line(
        points={{46,2},{46,2},{46,140},{350,140}},
        color={255,204,51},
        thickness=0.5), Text(
        string="%first",
        index=-1,
        extent={{-6,3},{-6,3}}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-340,
              -340},{340,340}})),
                              Diagram(coordinateSystem(preserveAspectRatio=false,
              extent={{-340,-340},{340,340}})));
    end WeatherProcessor;

    model Wea2Bus
      Modelica.Blocks.Interfaces.RealInput weaPAtm "Input pressure"
        annotation (Placement(transformation(extent={{-260,480},{-220,520}})));
      Modelica.Blocks.Interfaces.RealInput weaTDewPoi
      "Input dew point temperature"
      annotation (Placement(transformation(extent={{-260,420},{-220,460}})));
      Modelica.Blocks.Interfaces.RealInput weaTDryBul
      "Input dry bulb temperature"
      annotation (Placement(transformation(extent={{-260,360},{-220,400}})));
      Modelica.Blocks.Interfaces.RealInput weaRelHum "Input relative humidity"
      annotation (Placement(transformation(extent={{-260,300},{-220,340}})));
      Modelica.Blocks.Interfaces.RealInput weaNOpa "Input opaque sky cover"
      annotation (Placement(transformation(extent={{-260,240},{-220,280}})));
      Modelica.Blocks.Interfaces.RealInput weaCelHei "Input ceiling height"
      annotation (Placement(transformation(extent={{-260,180},{-220,220}})));
      Modelica.Blocks.Interfaces.RealInput weaNTot "Input total sky cover"
      annotation (Placement(transformation(extent={{-260,120},{-220,160}})));
      Modelica.Blocks.Interfaces.RealInput weaWinSpe "Input wind speed"
      annotation (Placement(transformation(extent={{-260,60},{-220,100}})));
      Modelica.Blocks.Interfaces.RealInput weaWinDir "Input wind direction"
      annotation (Placement(transformation(extent={{-260,0},{-220,40}})));
      Modelica.Blocks.Interfaces.RealInput weaHHorIR
      "Input diffuse horizontal radiation"
      annotation (Placement(transformation(extent={{-260,-60},{-220,-20}})));
      Modelica.Blocks.Interfaces.RealInput weaHDirNor
      "Input infrared horizontal radiation"
      annotation (Placement(transformation(extent={{-260,-120},{-220,-80}})));
      Modelica.Blocks.Interfaces.RealInput weaHGloHor
      "Input direct normal radiation"
      annotation (Placement(transformation(extent={{-260,-180},{-220,-140}})));
      Modelica.Blocks.Interfaces.RealInput weaHDifHor
      "Input global horizontal radiation"
      annotation (Placement(transformation(extent={{-260,-240},{-220,-200}})));
      Modelica.Blocks.Interfaces.RealInput weaTBlaSky
      "Input global horizontal radiation"
      annotation (Placement(transformation(extent={{-260,-298},{-220,-258}})));
      Modelica.Blocks.Interfaces.RealInput weaTWetBul
      "Input global horizontal radiation"
      annotation (Placement(transformation(extent={{-260,-360},{-220,-320}})));
      Modelica.Blocks.Interfaces.RealInput weaCloTim
      "Input global horizontal radiation"
      annotation (Placement(transformation(extent={{-260,-480},{-220,-440}})));
      Modelica.Blocks.Interfaces.RealInput weaSolTim
      "Input global horizontal radiation"
      annotation (Placement(transformation(extent={{-260,-540},{-220,-500}})));
      Modelica.Blocks.Interfaces.RealInput weaSolZen
      "Input global horizontal radiation"
      annotation (Placement(transformation(extent={{-260,-422},{-220,-382}})));
    Buildings.BoundaryConditions.WeatherData.Bus weaBus "Weather data bus"
      annotation (Placement(transformation(extent={{210,-10},{230,10}})));
    equation
    connect(weaPAtm, weaBus.pAtm) annotation (Line(points={{-240,500},{-240,500},
            {-194,500},{-194,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaTDewPoi, weaBus.TDewPoi) annotation (Line(points={{-240,440},{
            -198,440},{-198,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaTDryBul, weaBus.TDryBul) annotation (Line(points={{-240,380},{
            -202,380},{-202,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaRelHum, weaBus.relHum) annotation (Line(points={{-240,320},{-190,
            320},{-190,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaNOpa, weaBus.nOpa) annotation (Line(points={{-240,260},{-188,260},
            {-188,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaCelHei, weaBus.celHei) annotation (Line(points={{-240,200},{-184,
            200},{-184,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaNTot, weaBus.nTot) annotation (Line(points={{-240,140},{-180,140},
            {-180,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaWinSpe, weaBus.winSpe) annotation (Line(points={{-240,80},{-176,
            80},{-176,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaWinDir, weaBus.winDir) annotation (Line(points={{-240,20},{-240,
            22},{-172,22},{-172,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaHHorIR, weaBus.HHorIR) annotation (Line(points={{-240,-40},{-168,
            -40},{-168,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaHDirNor, weaBus.HDirNor) annotation (Line(points={{-240,-100},{
            -164,-100},{-164,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaHGloHor, weaBus.HGloHor) annotation (Line(points={{-240,-160},{
            -202,-160},{-160,-160},{-160,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaHDifHor, weaBus.HDifHor) annotation (Line(points={{-240,-220},{
            -156,-220},{-156,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaTBlaSky, weaBus.TBlaSky) annotation (Line(points={{-240,-278},{
            -152,-278},{-152,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaTWetBul, weaBus.TWetBul) annotation (Line(points={{-240,-340},{
            -148,-340},{-148,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaSolZen, weaBus.solZen) annotation (Line(points={{-240,-402},{
            -144,-402},{-144,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaCloTim, weaBus.cloTim) annotation (Line(points={{-240,-460},{
            -138,-460},{-138,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    connect(weaSolTim, weaBus.solTim) annotation (Line(points={{-240,-520},{
            -134,-520},{-134,0},{220,0}}, color={0,0,127}), Text(
        string="%second",
        index=1,
        extent={{6,3},{6,3}}));
    annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-220,
              -520},{220,520}}), graphics={
          Rectangle(
            extent={{-220,520},{220,-520}},
            lineColor={0,0,0},
            fillColor={255,255,255},
            fillPattern=FillPattern.Solid),
          Line(
            points={{-198,-2},{2,-2}},
            color={0,0,126},
            thickness=0.5),
          Line(
            points={{0,-2},{200,-2}},
            color={255,204,0},
            thickness=0.5)}), Diagram(coordinateSystem(preserveAspectRatio=
              false, extent={{-220,-520},{220,520}})));
    end Wea2Bus;

    package Examples

      model WeatherProcessor
      import RapidMPC;
      RapidMPC.BoundaryConditions.WeatherProcessor weatherProcessor(
        lon(displayUnit="deg") = -1.5344934783534,
        modTimOffset=0,
        lat=0.73268921998722,
        timZon=-21600)
        annotation (Placement(transformation(extent={{-10,-20},{10,18}})));
        Buildings.BoundaryConditions.WeatherData.ReaderTMY3 EPW(
        filNam=
            "modelica://Buildings/Resources/weatherdata/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.mos",
        pAtmSou=Buildings.BoundaryConditions.Types.DataSource.File,
        ceiHeiSou=Buildings.BoundaryConditions.Types.DataSource.File,
        TDryBulSou=Buildings.BoundaryConditions.Types.DataSource.File,
        HSou=Buildings.BoundaryConditions.Types.RadiationDataSource.File)
        "Weather data"
        annotation (Placement(transformation(extent={{-98,0},{-62,34}})));

      Buildings.BoundaryConditions.WeatherData.Bus weaBus "Weather data bus"
        annotation (Placement(transformation(extent={{-48,8},{-28,28}})));
      equation
      connect(EPW.weaBus, weaBus) annotation (Line(
          points={{-62,17},{-54,17},{-54,18},{-38,18}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%second",
          index=1,
          extent={{6,3},{6,3}}));
      connect(weaBus.pAtm, weatherProcessor.weaPAtm) annotation (Line(
          points={{-38,18},{-10.5882,18},{-10.5882,16.8824}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus.TDewPoi, weatherProcessor.weaTDewPoi) annotation (Line(
          points={{-38,18},{-28,18},{-28,13.5294},{-10.5882,13.5294}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus.TDryBul, weatherProcessor.weaTDryBul) annotation (Line(
          points={{-38,18},{-28,18},{-28,10.0647},{-10.5882,10.0647}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus.relHum, weatherProcessor.weaRelHum) annotation (Line(
          points={{-38,18},{-28,18},{-28,6.71176},{-10.5882,6.71176}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus.nOpa, weatherProcessor.weaNOpa) annotation (Line(
          points={{-38,18},{-28,18},{-28,3.35882},{-10.5882,3.35882}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus.celHei, weatherProcessor.weaCelHei) annotation (Line(
          points={{-38,18},{-28,18},{-28,0.00588235},{-10.5882,0.00588235}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus.nTot, weatherProcessor.weaNTot) annotation (Line(
          points={{-38,18},{-28,18},{-28,-3.23529},{-10.5882,-3.23529}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus.winSpe, weatherProcessor.weaWinSpe) annotation (Line(
          points={{-38,18},{-34,18},{-28,18},{-28,-6.58824},{-10.5882,-6.58824}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));

      connect(weaBus.winDir, weatherProcessor.weaWinDir) annotation (Line(
          points={{-38,18},{-28,18},{-28,-10.1647},{-10.5882,-10.1647}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus.HHorIR, weatherProcessor.weaHHorIR) annotation (Line(
          points={{-38,18},{-28,18},{-28,-13.4059},{-10.5882,-13.4059}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus.HDirNor, weatherProcessor.weaHDirNor) annotation (Line(
          points={{-38,18},{-28,18},{-28,-16.7588},{-10.5882,-16.7588}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus.HGloHor, weatherProcessor.weaHGloHor) annotation (Line(
          points={{-38,18},{-28,18},{-28,-20},{-10.5882,-20}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
            coordinateSystem(preserveAspectRatio=false)));
      end WeatherProcessor;
    annotation (Icon(graphics={
            Rectangle(
              lineColor={200,200,200},
              fillColor={248,248,248},
              fillPattern=FillPattern.HorizontalCylinder,
              extent={{-100,-100},{100,100}},
              radius=25.0),
            Rectangle(
              lineColor={128,128,128},
              fillPattern=FillPattern.None,
              extent={{-100,-100},{100,100}},
              radius=25.0),
            Polygon(
              origin={8,14},
              lineColor={78,138,73},
              fillColor={78,138,73},
              pattern=LinePattern.None,
              fillPattern=FillPattern.Solid,
              points={{-58.0,46.0},{42.0,-14.0},{-58.0,-74.0},{-58.0,46.0}})}));
    end Examples;

  end BoundaryConditions;

  package HVAC "HVAC components"
    model ConvectiveHeater
      parameter Real q_max(unit = "W") "Max heater output";
      parameter Real eff(unit = "1") "Efficiency of heater";
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow prescribedHeatFlow
        annotation (Placement(transformation(extent={{22,-10},{42,10}})));
      Modelica.Blocks.Math.Gain gain1(k=q_max)
      annotation (Placement(transformation(extent={{-38,-10},{-18,10}})));
      Modelica.Blocks.Interfaces.RealInput u "Input signal connector"
        annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
      Modelica.Thermal.HeatTransfer.Interfaces.HeatPort_b HeatOutput
        annotation (Placement(transformation(extent={{94,-10},{114,10}})));
    Modelica.Blocks.Interfaces.RealOutput P_e(unit="W")
      annotation (Placement(transformation(extent={{100,-70},{120,-50}})));
      Modelica.Blocks.Math.Gain gain2(k=eff)
        annotation (Placement(transformation(extent={{20,-70},{40,-50}})));
    equation
    connect(gain1.y, prescribedHeatFlow.Q_flow)
      annotation (Line(points={{-17,0},{2.5,0},{22,0}}, color={0,0,127}));
    connect(gain1.u, u)
      annotation (Line(points={{-40,0},{-120,0}}, color={0,0,127}));
      connect(prescribedHeatFlow.port, HeatOutput)
        annotation (Line(points={{42,0},{104,0}}, color={191,0,0}));
    connect(gain1.y, gain2.u) annotation (Line(points={{-17,0},{0,0},{0,-60},
            {18,-60}}, color={0,0,127}));
    connect(gain2.y, P_e)
      annotation (Line(points={{41,-60},{110,-60}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={
              Rectangle(
              extent={{-100,100},{100,-100}},
              lineColor={0,0,0},
              fillColor={255,255,255},
              fillPattern=FillPattern.Solid), Text(
              extent={{-58,24},{68,-14}},
              lineColor={0,0,0},
              fillColor={255,255,255},
              fillPattern=FillPattern.Solid,
              textString="ConvectiveHeater")}),                      Diagram(
            coordinateSystem(preserveAspectRatio=false)));
    end ConvectiveHeater;
  end HVAC;

  package Controllers "Controller components"
    package HeaterPI

      model PI
      Modelica.Blocks.Interfaces.RealInput Setpoint
        annotation (Placement(transformation(extent={{-140,30},{-100,70}})));
      Modelica.Blocks.Interfaces.RealInput Measurement annotation (Placement(
            transformation(extent={{-140,-70},{-100,-30}})));
      Buildings.Controls.Continuous.LimPID conPID(
        Td=0,
        k=0.0001,
        Ti=0.1)
        annotation (Placement(transformation(extent={{-16,6},{4,26}})));
      Modelica.Blocks.Interfaces.RealOutput y
        "Connector of actuator output signal"
        annotation (Placement(transformation(extent={{100,-10},{120,10}})));
      equation
      connect(Setpoint, conPID.u_s) annotation (Line(points={{-120,50},{-52,
              50},{-52,16},{-18,16}}, color={0,0,127}));
      connect(Measurement, conPID.u_m) annotation (Line(points={{-120,-50},{
              -6,-50},{-6,4}}, color={0,0,127}));
      connect(conPID.y, y) annotation (Line(points={{5,16},{40,16},{40,0},{74,
              0},{110,0}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
            coordinateSystem(preserveAspectRatio=false)));
      end PI;
    end HeaterPI;

    model SingleSetpoint
      parameter Real Setpoint "Temperature setpoint for HVAC";
      parameter Boolean OnStatus "On-Off Status for HVAC";
      Modelica.Blocks.Sources.Constant const(k=Setpoint)
        annotation (Placement(transformation(extent={{-100,80},{-80,100}})));
      HeaterPI.PI wes
        annotation (Placement(transformation(extent={{0,30},{20,50}})));
      HeaterPI.PI hal
        annotation (Placement(transformation(extent={{0,-10},{20,10}})));
      HeaterPI.PI eas
        annotation (Placement(transformation(extent={{0,-50},{20,-30}})));
    Modelica.Blocks.Interfaces.RealOutput y_wes
      "Connector of actuator output signal"
      annotation (Placement(transformation(extent={{100,30},{120,50}})));
    Modelica.Blocks.Interfaces.RealOutput y_hal
      "Connector of actuator output signal"
      annotation (Placement(transformation(extent={{100,-10},{120,10}})));
    Modelica.Blocks.Interfaces.RealOutput y_eas
      "Connector of actuator output signal"
      annotation (Placement(transformation(extent={{100,-50},{120,-30}})));
    Modelica.Blocks.Interfaces.RealInput meaTDryBul_wes
      annotation (Placement(transformation(extent={{-140,40},{-100,80}})));
    Modelica.Blocks.Interfaces.RealInput meaTDryBul_hal
      annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
    Modelica.Blocks.Interfaces.RealInput meaTDryBul_eas
      annotation (Placement(transformation(extent={{-140,-80},{-100,-40}})));
      Modelica.Blocks.Logical.Switch switch1
        annotation (Placement(transformation(extent={{-60,66},{-40,86}})));
      Modelica.Blocks.Sources.BooleanConstant OnOffStatus(k=OnStatus)
        annotation (Placement(transformation(extent={{-100,20},{-80,40}})));
      Modelica.Blocks.Logical.Switch switch2
        annotation (Placement(transformation(extent={{-60,20},{-40,40}})));
      Modelica.Blocks.Logical.Switch switch3
        annotation (Placement(transformation(extent={{-60,-40},{-40,-20}})));
      Modelica.Blocks.Logical.Switch switch4
        annotation (Placement(transformation(extent={{40,50},{60,70}})));
      Modelica.Blocks.Logical.Switch switch5
        annotation (Placement(transformation(extent={{40,10},{60,30}})));
      Modelica.Blocks.Logical.Switch switch6
        annotation (Placement(transformation(extent={{40,-30},{60,-10}})));
      Modelica.Blocks.Sources.Constant const1(k=0)
        annotation (Placement(transformation(extent={{0,80},{20,100}})));
    equation
    connect(wes.Measurement, meaTDryBul_wes) annotation (Line(points={{-2,35},{-10,35},
              {-10,34},{-18,34},{-18,60},{-120,60}},      color={0,0,127}));
    connect(hal.Measurement, meaTDryBul_hal) annotation (Line(points={{-2,-5},
            {-52,-5},{-52,0},{-120,0}}, color={0,0,127}));
    connect(eas.Measurement, meaTDryBul_eas) annotation (Line(points={{-2,-45},
            {-50,-45},{-50,-60},{-120,-60}}, color={0,0,127}));
      connect(const.y, switch1.u1) annotation (Line(points={{-79,90},{-66,90},{-66,84},
              {-62,84}}, color={0,0,127}));
      connect(meaTDryBul_wes, switch1.u3) annotation (Line(points={{-120,60},{-120,60},
              {-66,60},{-66,68},{-62,68}}, color={0,0,127}));
      connect(const.y, switch2.u1) annotation (Line(points={{-79,90},{-74,90},{-74,38},
              {-62,38}}, color={0,0,127}));
      connect(OnOffStatus.y, switch2.u2)
        annotation (Line(points={{-79,30},{-62,30}}, color={255,0,255}));
      connect(OnOffStatus.y, switch1.u2) annotation (Line(points={{-79,30},{-70,30},
              {-70,76},{-62,76}}, color={255,0,255}));
      connect(const.y, switch3.u1) annotation (Line(points={{-79,90},{-74,90},{-74,-22},
              {-62,-22}}, color={0,0,127}));
      connect(OnOffStatus.y, switch3.u2) annotation (Line(points={{-79,30},{-70,30},
              {-70,-30},{-62,-30}}, color={255,0,255}));
      connect(meaTDryBul_hal, switch2.u3) annotation (Line(points={{-120,0},{-66,0},
              {-66,22},{-62,22}}, color={0,0,127}));
      connect(meaTDryBul_eas, switch3.u3) annotation (Line(points={{-120,-60},{-96,-60},
              {-66,-60},{-66,-38},{-62,-38}}, color={0,0,127}));
      connect(switch1.y, wes.Setpoint) annotation (Line(points={{-39,76},{-22,76},{-22,
              45},{-2,45}}, color={0,0,127}));
      connect(switch2.y, hal.Setpoint) annotation (Line(points={{-39,30},{-22,30},{-22,
              5},{-2,5}}, color={0,0,127}));
      connect(switch3.y, eas.Setpoint) annotation (Line(points={{-39,-30},{-22,-30},
              {-22,-35},{-2,-35}}, color={0,0,127}));
      connect(const1.y, switch4.u3) annotation (Line(points={{21,90},{30,90},{30,52},
              {38,52}}, color={0,0,127}));
      connect(const1.y, switch5.u3) annotation (Line(points={{21,90},{30,90},{30,12},
              {38,12}}, color={0,0,127}));
      connect(const1.y, switch6.u3) annotation (Line(points={{21,90},{30,90},{30,-28},
              {38,-28}}, color={0,0,127}));
      connect(OnOffStatus.y, switch5.u2) annotation (Line(points={{-79,30},{-70,30},
              {-70,16},{16,16},{16,20},{38,20}}, color={255,0,255}));
      connect(OnOffStatus.y, switch4.u2) annotation (Line(points={{-79,30},{-70,30},
              {-70,16},{16,16},{16,20},{26,20},{26,60},{38,60}}, color={255,0,255}));
      connect(OnOffStatus.y, switch6.u2) annotation (Line(points={{-79,30},{-70,30},
              {-70,16},{16,16},{16,20},{26,20},{26,-20},{38,-20}}, color={255,0,255}));
      connect(wes.y, switch4.u1) annotation (Line(points={{21,40},{24,40},{24,68},{38,
              68}}, color={0,0,127}));
      connect(hal.y, switch5.u1)
        annotation (Line(points={{21,0},{24,0},{24,28},{38,28}}, color={0,0,127}));
      connect(eas.y, switch6.u1) annotation (Line(points={{21,-40},{24,-40},{24,-12},
              {38,-12}}, color={0,0,127}));
      connect(switch4.y, y_wes) annotation (Line(points={{61,60},{80,60},{80,40},{110,
              40}}, color={0,0,127}));
      connect(switch5.y, y_hal) annotation (Line(points={{61,20},{80,20},{80,0},{110,
              0}}, color={0,0,127}));
      connect(switch6.y, y_eas) annotation (Line(points={{61,-20},{80,-20},{80,-40},
              {110,-40}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={
            Rectangle(
            extent={{-100,100},{100,-100}},
            lineColor={0,0,0},
            fillColor={255,255,255},
            fillPattern=FillPattern.Solid), Text(
            extent={{-54,54},{66,-32}},
            lineColor={0,0,0},
            fillColor={255,255,255},
            fillPattern=FillPattern.Solid,
            textString="Single Setpoint")}),                         Diagram(
            coordinateSystem(preserveAspectRatio=false)));
    end SingleSetpoint;

    model DualSetpoint
      parameter Real Setpoint "Temperature setpoint for HVAC";
      parameter Real Setback "Temperature setback for HVAC";
      parameter Boolean OnStatus "On-Off Status for HVAC";
      Modelica.Blocks.Sources.Pulse    const(
        amplitude=Setback,
        period=24*3600,
        offset=Setpoint - Setback,
      width=11/24*100,
      startTime=6*3600)
        annotation (Placement(transformation(extent={{-100,80},{-80,100}})));
      HeaterPI.PI wes
        annotation (Placement(transformation(extent={{0,30},{20,50}})));
      HeaterPI.PI hal
        annotation (Placement(transformation(extent={{0,-10},{20,10}})));
      HeaterPI.PI eas
        annotation (Placement(transformation(extent={{0,-50},{20,-30}})));
    Modelica.Blocks.Interfaces.RealOutput y_wes
      "Connector of actuator output signal"
      annotation (Placement(transformation(extent={{100,30},{120,50}})));
    Modelica.Blocks.Interfaces.RealOutput y_hal
      "Connector of actuator output signal"
      annotation (Placement(transformation(extent={{100,-10},{120,10}})));
    Modelica.Blocks.Interfaces.RealOutput y_eas
      "Connector of actuator output signal"
      annotation (Placement(transformation(extent={{100,-50},{120,-30}})));
    Modelica.Blocks.Interfaces.RealInput meaTDryBul_wes
      annotation (Placement(transformation(extent={{-140,40},{-100,80}})));
    Modelica.Blocks.Interfaces.RealInput meaTDryBul_hal
      annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
    Modelica.Blocks.Interfaces.RealInput meaTDryBul_eas
      annotation (Placement(transformation(extent={{-140,-80},{-100,-40}})));
      Modelica.Blocks.Logical.Switch switch1
        annotation (Placement(transformation(extent={{-60,66},{-40,86}})));
      Modelica.Blocks.Sources.BooleanConstant OnOffStatus(k=OnStatus)
        annotation (Placement(transformation(extent={{-100,20},{-80,40}})));
      Modelica.Blocks.Logical.Switch switch2
        annotation (Placement(transformation(extent={{-60,20},{-40,40}})));
      Modelica.Blocks.Logical.Switch switch3
        annotation (Placement(transformation(extent={{-60,-40},{-40,-20}})));
      Modelica.Blocks.Logical.Switch switch4
        annotation (Placement(transformation(extent={{40,50},{60,70}})));
      Modelica.Blocks.Logical.Switch switch5
        annotation (Placement(transformation(extent={{40,10},{60,30}})));
      Modelica.Blocks.Logical.Switch switch6
        annotation (Placement(transformation(extent={{40,-30},{60,-10}})));
      Modelica.Blocks.Sources.Constant const1(k=0)
        annotation (Placement(transformation(extent={{0,80},{20,100}})));
    equation
    connect(wes.Measurement, meaTDryBul_wes) annotation (Line(points={{-2,35},{-10,35},
              {-10,34},{-18,34},{-18,60},{-120,60}},      color={0,0,127}));
    connect(hal.Measurement, meaTDryBul_hal) annotation (Line(points={{-2,-5},
            {-52,-5},{-52,0},{-120,0}}, color={0,0,127}));
    connect(eas.Measurement, meaTDryBul_eas) annotation (Line(points={{-2,-45},
            {-50,-45},{-50,-60},{-120,-60}}, color={0,0,127}));
      connect(const.y, switch1.u1) annotation (Line(points={{-79,90},{-66,90},{-66,84},
              {-62,84}}, color={0,0,127}));
      connect(meaTDryBul_wes, switch1.u3) annotation (Line(points={{-120,60},{-120,60},
              {-66,60},{-66,68},{-62,68}}, color={0,0,127}));
      connect(const.y, switch2.u1) annotation (Line(points={{-79,90},{-74,90},{-74,38},
              {-62,38}}, color={0,0,127}));
      connect(OnOffStatus.y, switch2.u2)
        annotation (Line(points={{-79,30},{-62,30}}, color={255,0,255}));
      connect(OnOffStatus.y, switch1.u2) annotation (Line(points={{-79,30},{-70,30},
              {-70,76},{-62,76}}, color={255,0,255}));
      connect(const.y, switch3.u1) annotation (Line(points={{-79,90},{-74,90},{-74,-22},
              {-62,-22}}, color={0,0,127}));
      connect(OnOffStatus.y, switch3.u2) annotation (Line(points={{-79,30},{-70,30},
              {-70,-30},{-62,-30}}, color={255,0,255}));
      connect(meaTDryBul_hal, switch2.u3) annotation (Line(points={{-120,0},{-66,0},
              {-66,22},{-62,22}}, color={0,0,127}));
      connect(meaTDryBul_eas, switch3.u3) annotation (Line(points={{-120,-60},{-96,-60},
              {-66,-60},{-66,-38},{-62,-38}}, color={0,0,127}));
      connect(switch1.y, wes.Setpoint) annotation (Line(points={{-39,76},{-22,76},{-22,
              45},{-2,45}}, color={0,0,127}));
      connect(switch2.y, hal.Setpoint) annotation (Line(points={{-39,30},{-22,30},{-22,
              5},{-2,5}}, color={0,0,127}));
      connect(switch3.y, eas.Setpoint) annotation (Line(points={{-39,-30},{-22,-30},
              {-22,-35},{-2,-35}}, color={0,0,127}));
      connect(const1.y, switch4.u3) annotation (Line(points={{21,90},{30,90},{30,52},
              {38,52}}, color={0,0,127}));
      connect(const1.y, switch5.u3) annotation (Line(points={{21,90},{30,90},{30,12},
              {38,12}}, color={0,0,127}));
      connect(const1.y, switch6.u3) annotation (Line(points={{21,90},{30,90},{30,-28},
              {38,-28}}, color={0,0,127}));
      connect(OnOffStatus.y, switch5.u2) annotation (Line(points={{-79,30},{-70,30},
              {-70,16},{16,16},{16,20},{38,20}}, color={255,0,255}));
      connect(OnOffStatus.y, switch4.u2) annotation (Line(points={{-79,30},{-70,30},
              {-70,16},{16,16},{16,20},{26,20},{26,60},{38,60}}, color={255,0,255}));
      connect(OnOffStatus.y, switch6.u2) annotation (Line(points={{-79,30},{-70,30},
              {-70,16},{16,16},{16,20},{26,20},{26,-20},{38,-20}}, color={255,0,255}));
      connect(wes.y, switch4.u1) annotation (Line(points={{21,40},{24,40},{24,68},{38,
              68}}, color={0,0,127}));
      connect(hal.y, switch5.u1)
        annotation (Line(points={{21,0},{24,0},{24,28},{38,28}}, color={0,0,127}));
      connect(eas.y, switch6.u1) annotation (Line(points={{21,-40},{24,-40},{24,-12},
              {38,-12}}, color={0,0,127}));
      connect(switch4.y, y_wes) annotation (Line(points={{61,60},{80,60},{80,40},{110,
              40}}, color={0,0,127}));
      connect(switch5.y, y_hal) annotation (Line(points={{61,20},{80,20},{80,0},{110,
              0}}, color={0,0,127}));
      connect(switch6.y, y_eas) annotation (Line(points={{61,-20},{80,-20},{80,-40},
              {110,-40}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={
            Rectangle(
            extent={{-100,100},{100,-100}},
            lineColor={0,0,0},
            fillColor={255,255,255},
            fillPattern=FillPattern.Solid), Text(
            extent={{-54,54},{66,-32}},
            lineColor={0,0,0},
            fillColor={255,255,255},
            fillPattern=FillPattern.Solid,
            textString="Dual Setpoint")}),                           Diagram(
            coordinateSystem(preserveAspectRatio=false)));
    end DualSetpoint;
  end Controllers;
  annotation (uses(Modelica(version="3.2.2"), Buildings(version="3.0.1")));
end LBNL71T_MPC;
