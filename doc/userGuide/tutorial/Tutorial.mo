within ;
package Tutorial "Contains models for the mpcpy tutorial"

  model RC "A simple RC network for example purposes"

    Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature preTemp
      annotation (Placement(transformation(extent={{-40,0},{-20,20}})));
    Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor senTemp
      annotation (Placement(transformation(extent={{70,0},{90,20}})));
    Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preHeat
      annotation (Placement(transformation(extent={{-18,-40},{2,-20}})));
    Modelica.Blocks.Interfaces.RealOutput Tzone(unit="K") "Zone temperature"
      annotation (Placement(transformation(extent={{100,0},{120,20}})));
    Modelica.Blocks.Interfaces.RealInput Qflow(unit="W") "Heat input"
      annotation (Placement(transformation(extent={{-140,-50},{-100,-10}})));
    Modelica.Thermal.HeatTransfer.Components.HeatCapacitor heatCapacitor(C=1e5) "Thermal capacitance of zone"
      annotation (Placement(transformation(extent={{20,10},{40,30}})));
    Modelica.Thermal.HeatTransfer.Components.ThermalResistor thermalResistor(R=
          0.01) "Thermal resistance of zone" annotation (Placement(transformation(extent={{-10,0},{10,20}})));
    Modelica.Blocks.Interfaces.RealInput weaTDryBul(unit="K") "Ambient temperature"
      annotation (Placement(transformation(extent={{-140,-10},{-100,30}})));
  equation
    connect(senTemp.T, Tzone)
      annotation (Line(points={{90,10},{110,10}}, color={0,0,127}));
    connect(preHeat.Q_flow, Qflow)
      annotation (Line(points={{-18,-30},{-120,-30}}, color={0,0,127}));
    connect(heatCapacitor.port, senTemp.port)
      annotation (Line(points={{30,10},{50,10},{70,10}}, color={191,0,0}));
    connect(heatCapacitor.port, preHeat.port)
      annotation (Line(points={{30,10},{30,-30},{2,-30}}, color={191,0,0}));
    connect(preTemp.port, thermalResistor.port_a)
      annotation (Line(points={{-20,10},{-16,10},{-10,10}}, color={191,0,0}));
    connect(thermalResistor.port_b, heatCapacitor.port)
      annotation (Line(points={{10,10},{20,10},{30,10}}, color={191,0,0}));
    connect(preTemp.T, weaTDryBul)
      annotation (Line(points={{-42,10},{-120,10}}, color={0,0,127}));
  end RC;
  annotation (uses(Modelica(version="3.2.2")));
end Tutorial;
