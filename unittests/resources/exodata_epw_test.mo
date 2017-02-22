within ;
model exodata_epw_test

  Buildings.BoundaryConditions.WeatherData.ReaderTMY3 weaDat1(
    calTSky=Buildings.BoundaryConditions.Types.SkyTemperatureCalculation.TemperaturesAndSkyCover,
    HSou=Buildings.BoundaryConditions.Types.RadiationDataSource.File,
    filNam=
        "modelica://Buildings/Resources/weatherdata/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.mos")
    annotation (Placement(transformation(extent={{-22,12},{-2,32}})));

  Buildings.BoundaryConditions.WeatherData.Bus weaBus2
             "Weather data bus"
    annotation (Placement(transformation(extent={{18,12},{38,32}})));
  Modelica.Blocks.Interfaces.RealOutput weaPAtm
    annotation (Placement(transformation(extent={{100,90},{120,110}})));
  Modelica.Blocks.Interfaces.RealOutput weaTDewPoi
    annotation (Placement(transformation(extent={{100,70},{120,90}})));
  Modelica.Blocks.Interfaces.RealOutput weaTDryBul
    annotation (Placement(transformation(extent={{100,50},{120,70}})));
  Modelica.Blocks.Interfaces.RealOutput weaRelHum
    annotation (Placement(transformation(extent={{100,30},{120,50}})));
  Modelica.Blocks.Interfaces.RealOutput weaNOpa
    annotation (Placement(transformation(extent={{100,-30},{120,-10}})));
  Modelica.Blocks.Interfaces.RealOutput weaCelHei
    annotation (Placement(transformation(extent={{100,-10},{120,10}})));
  Modelica.Blocks.Interfaces.RealOutput weaNTot
    annotation (Placement(transformation(extent={{100,10},{120,30}})));
  Modelica.Blocks.Interfaces.RealOutput weaWinSpe
    annotation (Placement(transformation(extent={{100,-50},{120,-30}})));
  Modelica.Blocks.Interfaces.RealOutput weaWinDir
    annotation (Placement(transformation(extent={{100,-70},{120,-50}})));
  Modelica.Blocks.Interfaces.RealOutput weaHHorIR
    annotation (Placement(transformation(extent={{100,-90},{120,-70}})));
  Modelica.Blocks.Interfaces.RealOutput weaHDirNor
    annotation (Placement(transformation(extent={{100,-110},{120,-90}})));
  Modelica.Blocks.Interfaces.RealOutput weaHGloHor
    annotation (Placement(transformation(extent={{100,-130},{120,-110}})));
  Modelica.Blocks.Interfaces.RealOutput weaHDifHor
    annotation (Placement(transformation(extent={{100,-150},{120,-130}})));
  Modelica.Blocks.Interfaces.RealOutput weaSolZen
    annotation (Placement(transformation(extent={{100,-210},{120,-190}})));
  Modelica.Blocks.Interfaces.RealOutput weaTBlaSky
    annotation (Placement(transformation(extent={{100,-190},{120,-170}})));
  Modelica.Blocks.Interfaces.RealOutput weaTWetBul
    annotation (Placement(transformation(extent={{100,-170},{120,-150}})));
  Modelica.Blocks.Interfaces.RealOutput weaSolTim
    annotation (Placement(transformation(extent={{100,-230},{120,-210}})));
  Modelica.Blocks.Interfaces.RealOutput weaCloTim
    annotation (Placement(transformation(extent={{100,-250},{120,-230}})));
  Modelica.Blocks.Interfaces.RealOutput lat
    annotation (Placement(transformation(extent={{100,-270},{120,-250}})));
  Modelica.Blocks.Interfaces.RealOutput lon
    annotation (Placement(transformation(extent={{100,-290},{120,-270}})));
equation
  connect(weaDat1.weaBus, weaBus2) annotation (Line(
      points={{-2,22},{14,22},{28,22}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaTDryBul, weaBus2.TDryBul) annotation (Line(points={{110,60},{68,60},
          {28,60},{28,22}},  color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaPAtm, weaBus2.pAtm) annotation (Line(points={{110,100},{68,100},{
          28,100},{28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaTDewPoi, weaBus2.TDewPoi) annotation (Line(points={{110,80},{70,80},
          {28,80},{28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaRelHum, weaBus2.relHum) annotation (Line(points={{110,40},{28,40},
          {28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaNTot, weaBus2.nTot) annotation (Line(points={{110,20},{28,20},{28,
          22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaCelHei, weaBus2.celHei) annotation (Line(points={{110,0},{28,0},{
          28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaNOpa, weaBus2.nOpa) annotation (Line(points={{110,-20},{28,-20},{
          28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaWinSpe, weaBus2.winSpe) annotation (Line(points={{110,-40},{28,-40},
          {28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaWinDir, weaBus2.winDir) annotation (Line(points={{110,-60},{28,-60},
          {28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaHHorIR, weaBus2.HHorIR) annotation (Line(points={{110,-80},{28,-80},
          {28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaHDirNor, weaBus2.HDirNor) annotation (Line(points={{110,-100},{74,
          -100},{28,-100},{28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaHGloHor, weaBus2.HGloHor) annotation (Line(points={{110,-120},{28,
          -120},{28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaHDifHor, weaBus2.HDifHor) annotation (Line(points={{110,-140},{70,
          -140},{28,-140},{28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaTWetBul, weaBus2.TWetBul) annotation (Line(points={{110,-160},{70,
          -160},{28,-160},{28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaTBlaSky, weaBus2.TBlaSky) annotation (Line(points={{110,-180},{68,
          -180},{28,-180},{28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaSolZen, weaBus2.solZen) annotation (Line(points={{110,-200},{86,
          -200},{28,-200},{28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaSolTim, weaBus2.solTim) annotation (Line(points={{110,-220},{28,
          -220},{28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(weaCloTim, weaBus2.cloTim) annotation (Line(points={{110,-240},{28,
          -240},{28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(lat, weaBus2.lat) annotation (Line(points={{110,-260},{70,-260},{28,
          -260},{28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(lon, weaBus2.lon) annotation (Line(points={{110,-280},{70,-280},{28,
          -280},{28,22}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  annotation (uses(Buildings(version="3.0.1"), Modelica(version="3.2.2")),
      experiment(StopTime=3.1536e+07, Interval=3600));
end exodata_epw_test;
