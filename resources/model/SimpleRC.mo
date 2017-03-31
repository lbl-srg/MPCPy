within ;
model SimpleRC "A simple RC network for example purposes"
  Modelica.Thermal.HeatTransfer.Components.HeatCapacitor heatCapacitor
    annotation (Placement(transformation(extent={{-10,0},{10,20}})));
  Modelica.Thermal.HeatTransfer.Components.ThermalResistor thermalResistor
    annotation (Placement(transformation(extent={{-40,-10},{-20,10}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature
    prescribedTemperature
    annotation (Placement(transformation(extent={{-80,-10},{-60,10}})));
  Modelica.Blocks.Interfaces.RealInput Tamb
    annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
  Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor temperatureSensor
    annotation (Placement(transformation(extent={{40,-10},{60,10}})));
  Modelica.Blocks.Interfaces.RealOutput T
    "Absolute temperature as output signal"
    annotation (Placement(transformation(extent={{100,-10},{120,10}})));
equation
  connect(thermalResistor.port_b, heatCapacitor.port)
    annotation (Line(points={{-20,0},{-10,0},{0,0}}, color={191,0,0}));
  connect(thermalResistor.port_a, prescribedTemperature.port)
    annotation (Line(points={{-40,0},{-60,0}}, color={191,0,0}));
  connect(prescribedTemperature.T, Tamb)
    annotation (Line(points={{-82,0},{-120,0}}, color={0,0,127}));
  connect(temperatureSensor.port, heatCapacitor.port)
    annotation (Line(points={{40,0},{20,0},{0,0}}, color={191,0,0}));
  connect(temperatureSensor.T, T)
    annotation (Line(points={{60,0},{110,0}}, color={0,0,127}));
  annotation (uses(Modelica(version="3.2.2")));
end SimpleRC;
