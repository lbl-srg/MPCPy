within ;
model BuildingsEPWReader

  Buildings.BoundaryConditions.WeatherData.ReaderTMY3 epw(filNam=
      "modelica://Buildings/Resources/weatherdata/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.mos")
  "Weather data"
  annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
  annotation (uses(Buildings(version="3.0.1")));
end BuildingsEPWReader;
