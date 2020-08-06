within ;
package TestModels
  package Detailed
    model Case600FF
      "Basic test with light-weight construction and free floating temperature"
      package MediumA = Buildings.Media.Air "Medium model";
      parameter Modelica.SIunits.Area Aflo = 48 "Floor area of zone";
      parameter Modelica.SIunits.Angle lat "Building latitude";
      parameter Modelica.SIunits.Angle S_=
        Buildings.Types.Azimuth.S "Azimuth for south walls";
      parameter Modelica.SIunits.Angle E_=
        Buildings.Types.Azimuth.E "Azimuth for east walls";
      parameter Modelica.SIunits.Angle W_=
        Buildings.Types.Azimuth.W "Azimuth for west walls";
      parameter Modelica.SIunits.Angle N_=
        Buildings.Types.Azimuth.N "Azimuth for north walls";
      parameter Modelica.SIunits.Angle C_=
        Buildings.Types.Tilt.Ceiling "Tilt for ceiling";
      parameter Modelica.SIunits.Angle F_=
        Buildings.Types.Tilt.Floor "Tilt for floor";
      parameter Modelica.SIunits.Angle Z_=
        Buildings.Types.Tilt.Wall "Tilt for wall";
      parameter Integer nConExtWin = 1 "Number of constructions with a window";
      parameter Integer nConBou = 1
        "Number of surface that are connected to constructions that are modeled inside the room";
      parameter Buildings.HeatTransfer.Data.OpaqueConstructions.Generic matExtWal(
        nLay=3,
        absIR_a=0.9,
        absIR_b=0.9,
        absSol_a=0.6,
        absSol_b=0.6,
        material={Buildings.HeatTransfer.Data.Solids.Generic(
            x=0.009,
            k=0.140,
            c=900,
            d=530,
            nStaRef=Buildings.ThermalZones.Detailed.Validation.BESTEST.nStaRef),
                             Buildings.HeatTransfer.Data.Solids.Generic(
            x=0.066,
            k=0.040,
            c=840,
            d=12,
            nStaRef=Buildings.ThermalZones.Detailed.Validation.BESTEST.nStaRef),
                             Buildings.HeatTransfer.Data.Solids.Generic(
            x=0.012,
            k=0.160,
            c=840,
            d=950,
            nStaRef=Buildings.ThermalZones.Detailed.Validation.BESTEST.nStaRef)})
                               "Exterior wall"
        annotation (Placement(transformation(extent={{20,84},{34,98}})));
      parameter Buildings.HeatTransfer.Data.OpaqueConstructions.Generic
                                                              matFlo(final nLay=
               2,
        absIR_a=0.9,
        absIR_b=0.9,
        absSol_a=0.6,
        absSol_b=0.6,
        material={Buildings.HeatTransfer.Data.Solids.Generic(
            x=1.003,
            k=0.040,
            c=0,
            d=0,
            nStaRef=Buildings.ThermalZones.Detailed.Validation.BESTEST.nStaRef),
                             Buildings.HeatTransfer.Data.Solids.Generic(
            x=0.025,
            k=0.140,
            c=1200,
            d=650,
            nStaRef=Buildings.ThermalZones.Detailed.Validation.BESTEST.nStaRef)})
                               "Floor"
        annotation (Placement(transformation(extent={{80,84},{94,98}})));
       parameter Buildings.HeatTransfer.Data.Solids.Generic soil(
        x=2,
        k=1.3,
        c=800,
        d=1500) "Soil properties"
        annotation (Placement(transformation(extent={{40,40},{60,60}})));

      Buildings.ThermalZones.Detailed.MixedAir roo(
        redeclare package Medium = MediumA,
        hRoo=2.7,
        nConExtWin=nConExtWin,
        nConBou=1,
        nPorts=3,
        AFlo=48,
        datConBou(
          layers={matFlo},
          each A=48,
          each til=F_),
        nConExt=4,
        nConPar=0,
        nSurBou=0,
        lat=lat,
        intConMod=Buildings.HeatTransfer.Types.InteriorConvection.Temperature,
        steadyStateWindow=false,
        datConExt(
          layers={roof,matExtWal,matExtWal,matExtWal},
          A={48,6*2.7,6*2.7,8*2.7},
          til={C_,Z_,Z_,Z_},
          azi={S_,W_,E_,N_}),
        datConExtWin(
          layers={matExtWal},
          A={8*2.7},
          glaSys={window600},
          wWin={2*3},
          hWin={2},
          fFra={0.001},
          til={Z_},
          azi={S_}),
        massDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial,
        energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial,
        extConMod=Buildings.HeatTransfer.Types.ExteriorConvection.TemperatureWind)
        "Room model for Case 600"
        annotation (Placement(transformation(extent={{12,-30},{42,0}})));
      Modelica.Blocks.Routing.Multiplex3 multiplex3_1
        annotation (Placement(transformation(extent={{-32,-6},{-24,2}})));
      Modelica.Blocks.Sources.Constant uSha(k=0)
        "Control signal for the shading device"
        annotation (Placement(transformation(extent={{-44,14},{-36,22}})));
      Modelica.Blocks.Routing.Replicator replicator(nout=max(1,nConExtWin))
        annotation (Placement(transformation(extent={{-28,14},{-20,22}})));
      Modelica.Thermal.HeatTransfer.Sources.FixedTemperature TSoi[nConBou](each T=
            283.15) "Boundary condition for construction"
                                              annotation (Placement(transformation(
            extent={{0,0},{-8,8}},
            origin={48,-52})));
      parameter Buildings.HeatTransfer.Data.OpaqueConstructions.Generic roof(nLay=3,
        absIR_a=0.9,
        absIR_b=0.9,
        absSol_a=0.6,
        absSol_b=0.6,
        material={Buildings.HeatTransfer.Data.Solids.Generic(
            x=0.019,
            k=0.140,
            c=900,
            d=530,
            nStaRef=Buildings.ThermalZones.Detailed.Validation.BESTEST.nStaRef),
                             Buildings.HeatTransfer.Data.Solids.Generic(
            x=0.1118,
            k=0.040,
            c=840,
            d=12,
            nStaRef=Buildings.ThermalZones.Detailed.Validation.BESTEST.nStaRef),
                             Buildings.HeatTransfer.Data.Solids.Generic(
            x=0.010,
            k=0.160,
            c=840,
            d=950,
            nStaRef=Buildings.ThermalZones.Detailed.Validation.BESTEST.nStaRef)})
                               "Roof"
        annotation (Placement(transformation(extent={{60,84},{74,98}})));
      Buildings.ThermalZones.Detailed.Validation.BESTEST.Data.Win600
             window600(
        UFra=3,
        haveExteriorShade=false,
        haveInteriorShade=false) "Window"
        annotation (Placement(transformation(extent={{40,84},{54,98}})));
      Buildings.HeatTransfer.Conduction.SingleLayer soi(
        A=48,
        material=soil,
        steadyStateInitial=true,
        stateAtSurface_a=false,
        stateAtSurface_b=true,
        T_a_start=283.15,
        T_b_start=283.75) "2m deep soil (per definition on p.4 of ASHRAE 140-2007)"
        annotation (Placement(transformation(
            extent={{5,-5},{-3,3}},
            rotation=-90,
            origin={33,-35})));
      Buildings.Fluid.Sources.Outside sinInf(redeclare package Medium = MediumA,
          nPorts=1) "Sink model for air infiltration"
               annotation (Placement(transformation(extent={{-82,-28},{-70,-16}})));
      Modelica.Blocks.Sources.Constant InfiltrationRate(k=48*2.7*0.5/3600)
        "0.41 ACH adjusted for the altitude (0.5 at sea level)"
        annotation (Placement(transformation(extent={{-96,-78},{-88,-70}})));
      Modelica.Blocks.Math.Product product
        annotation (Placement(transformation(extent={{-50,-60},{-40,-50}})));
      Buildings.Fluid.Sensors.Density density(redeclare package Medium = MediumA)
        "Air density inside the building"
        annotation (Placement(transformation(extent={{-40,-76},{-50,-66}})));
      Buildings.BoundaryConditions.WeatherData.Bus weaBus
        annotation (Placement(transformation(extent={{-98,96},{-82,112}})));
      Modelica.Blocks.Math.MultiSum multiSum(nu=1)
        annotation (Placement(transformation(extent={{-78,-80},{-66,-68}})));

      Modelica.Blocks.Interfaces.RealOutput Tzone(unit="K")
        "Zone mean air drybulb temperature"
        annotation (Placement(transformation(extent={{100,-10},{120,10}})));
      Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor thermostat
        annotation (Placement(transformation(extent={{50,-26},{70,-6}})));
      Buildings.Fluid.Sources.Outside souInf(redeclare package Medium = MediumA,
          nPorts=1) "Source model for air infiltration"
        annotation (Placement(transformation(extent={{-64,-40},{-52,-28}})));
      Buildings.Fluid.Movers.BaseClasses.IdealSource infMover(
        control_m_flow=true,
        allowFlowReversal=false,
        redeclare package Medium = MediumA,
        m_flow_small=1e-4)
        annotation (Placement(transformation(extent={{-38,-38},{-30,-30}})));
      Buildings.Fluid.Movers.BaseClasses.IdealSource infMover1(
        control_m_flow=true,
        allowFlowReversal=false,
        redeclare package Medium = MediumA,
        m_flow_small=1e-4)
        annotation (Placement(transformation(extent={{-20,-26},{-28,-18}})));
      Modelica.Blocks.Interfaces.RealInput intRad
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,60},{-100,100}})));
      Modelica.Blocks.Interfaces.RealInput intCon
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,30},{-100,70}})));
      Modelica.Blocks.Interfaces.RealInput intLat
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,0},{-100,40}})));
    equation
      connect(multiplex3_1.y, roo.qGai_flow) annotation (Line(
          points={{-23.6,-2},{-22,-2},{-22,-9},{10.8,-9}},
          color={0,0,127},
          smooth=Smooth.None));
      connect(roo.uSha, replicator.y) annotation (Line(
          points={{10.8,-1.5},{-18,-1.5},{-18,18},{-19.6,18}},
          color={0,0,127},
          smooth=Smooth.None));
      connect(uSha.y, replicator.u) annotation (Line(
          points={{-35.6,18},{-34,18},{-34,18},{-30,18},{-30,18},{-28.8,18}},
          color={0,0,127},
          smooth=Smooth.None));
      connect(density.port, roo.ports[1])  annotation (Line(
          points={{-45,-76},{2,-76},{2,-24.5},{15.75,-24.5}},
          color={0,127,255},
          smooth=Smooth.None));
      connect(density.d, product.u2) annotation (Line(
          points={{-50.5,-71},{-56,-71},{-56,-58},{-51,-58}},
          color={0,0,127},
          smooth=Smooth.None));
      connect(TSoi[1].port, soi.port_a) annotation (Line(
          points={{40,-48},{32,-48},{32,-40}},
          color={191,0,0},
          smooth=Smooth.None));
      connect(soi.port_b, roo.surf_conBou[1]) annotation (Line(
          points={{32,-32},{32,-27},{31.5,-27}},
          color={191,0,0},
          smooth=Smooth.None));
      connect(multiSum.y, product.u1) annotation (Line(
          points={{-64.98,-74},{-54,-74},{-54,-52},{-51,-52}},
          color={0,0,127},
          smooth=Smooth.None));
      connect(InfiltrationRate.y, multiSum.u[1]) annotation (Line(
          points={{-87.6,-74},{-78,-74}},
          color={0,0,127},
          smooth=Smooth.None));

      connect(weaBus,sinInf. weaBus) annotation (Line(
          points={{-90,104},{-90,104},{-90,-20},{-82,-20},{-82,-21.88}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus, roo.weaBus) annotation (Line(
          points={{-90,104},{-90,104},{-90,24},{40,24},{40,2},{40.425,2},{
              40.425,-1.575}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));

      connect(thermostat.T, Tzone) annotation (Line(points={{70,-16},{88,-16},{
              88,0},{110,0}}, color={0,0,127}));
      connect(thermostat.port, roo.heaPorAir) annotation (Line(points={{50,-16},{26.25,
              -16},{26.25,-15}}, color={191,0,0}));
      connect(souInf.weaBus, sinInf.weaBus) annotation (Line(
          points={{-64,-33.88},{-76,-33.88},{-76,-34},{-90,-34},{-90,-20},{-82,
              -20},{-82,-21.88}},
          color={255,204,51},
          thickness=0.5));
      connect(souInf.ports[1], infMover.port_a)
        annotation (Line(points={{-52,-34},{-38,-34}}, color={0,127,255}));
      connect(infMover.port_b, roo.ports[2]) annotation (Line(points={{-30,-34},
              {-6,-34},{-6,-32},{-6,-20.5},{15.75,-20.5},{15.75,-22.5}},
                                                           color={0,127,255}));
      connect(product.y, infMover.m_flow_in) annotation (Line(points={{-39.5,
              -55},{-34,-55},{-34,-44},{-44,-44},{-44,-26},{-36.4,-26},{-36.4,
              -30.8}}, color={0,0,127}));
      connect(sinInf.ports[1], infMover1.port_b)
        annotation (Line(points={{-70,-22},{-28,-22}}, color={0,127,255}));
      connect(infMover1.port_a, roo.ports[3]) annotation (Line(points={{-20,-22},
              {14,-22},{14,-20.5},{15.75,-20.5}}, color={0,127,255}));
      connect(infMover1.m_flow_in, infMover.m_flow_in) annotation (Line(points={{-21.6,
              -18.8},{-21.6,-14},{-32,-14},{-32,-26},{-36.4,-26},{-36.4,-30.8}},
                       color={0,0,127}));
      connect(intRad, multiplex3_1.u1[1]) annotation (Line(points={{-120,80},{
              -76,80},{-76,80},{-76,0.8},{-32.8,0.8}},
                                               color={0,0,127}));
      connect(intCon, multiplex3_1.u2[1]) annotation (Line(points={{-120,50},{
              -78,50},{-78,50},{-78,-2},{-32.8,-2}},
                                             color={0,0,127}));
      connect(intLat, multiplex3_1.u3[1]) annotation (Line(points={{-120,20},{
              -80,20},{-80,-4.8},{-32.8,-4.8}},
                                        color={0,0,127}));
      annotation (
    experiment(
          StopTime=3.1536e+07,
          Interval=3600,
          __Dymola_Algorithm="Radau"),
    __Dymola_Commands(file="modelica://Buildings/Resources/Scripts/Dymola/ThermalZones/Detailed/Validation/BESTEST/Case600FF.mos"
            "Simulate and plot"), Documentation(info="<html>
<p>
This model is used for the test case 600FF of the BESTEST validation suite.
Case 600FF is a light-weight building.
The room temperature is free floating.
</p>
</html>",     revisions="<html>
<ul>
<li>
October 29, 2016, by Michael Wetter:<br/>
Placed a capacity at the room-facing surface
to reduce the dimension of the nonlinear system of equations,
which generally decreases computing time.<br/>
Removed the pressure drop element which is not needed.<br/>
Linearized the radiative heat transfer, which is the default in
the library, and avoids a large nonlinear system of equations.<br/>
This is for
<a href=\"https://github.com/lbl-srg/modelica-buildings/issues/565\">issue 565</a>.
</li>
<li>
December 22, 2014 by Michael Wetter:<br/>
Removed <code>Modelica.Fluid.System</code>
to address issue
<a href=\"https://github.com/lbl-srg/modelica-buildings/issues/311\">#311</a>.
</li>
<li>
October 9, 2013, by Michael Wetter:<br/>
Implemented soil properties using a record so that <code>TSol</code> and
<code>TLiq</code> are assigned.
This avoids an error when the model is checked in the pedantic mode.
</li>
<li>
July 15, 2012, by Michael Wetter:<br/>
Added reference results.
Changed implementation to make this model the base class
for all BESTEST cases.
Added computation of hourly and annual averaged room air temperature.
<li>
October 6, 2011, by Michael Wetter:<br/>
First implementation.
</li>
</ul>
</html>"),
        Icon(graphics={
            Rectangle(
              extent={{-92,92},{92,-92}},
              pattern=LinePattern.None,
              lineColor={117,148,176},
              fillColor={170,213,255},
              fillPattern=FillPattern.Sphere),
            Rectangle(
              extent={{-100,-100},{100,100}},
              lineColor={95,95,95},
              fillColor={95,95,95},
              fillPattern=FillPattern.Solid),
            Rectangle(
              extent={{-92,92},{92,-92}},
              pattern=LinePattern.None,
              lineColor={117,148,176},
              fillColor={170,213,255},
              fillPattern=FillPattern.Sphere),
            Rectangle(
              extent={{-46,42},{52,-46}},
              lineColor={0,0,0},
              fillColor={255,255,255},
              fillPattern=FillPattern.Solid),
            Text(
              extent={{-150,144},{150,104}},
              textString="%name",
              lineColor={0,0,255})}),
        __Dymola_experimentSetupOutput(events=false));
    end Case600FF;

    model Case600HeatCool
      import TestModels;
      extends Case600FF;
      Modelica.Blocks.Interfaces.RealInput qHeat
        annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
      Modelica.Blocks.Interfaces.RealInput qCool
        annotation (Placement(transformation(extent={{-140,-100},{-100,-60}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preHeat
        annotation (Placement(transformation(extent={{10,-70},{22,-58}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preCool
        annotation (Placement(transformation(extent={{10,-80},{22,-68}})));
    equation
      connect(preCool.port, roo.heaPorAir) annotation (Line(points={{22,-74},{
              26.25,-74},{26.25,-15}}, color={191,0,0}));
      connect(preHeat.port, roo.heaPorAir) annotation (Line(points={{22,-64},{
              26.25,-64},{26.25,-15}}, color={191,0,0}));
      connect(qHeat, preHeat.Q_flow) annotation (Line(points={{-120,-40},{-80,
              -40},{-80,-88},{-12,-88},{-12,-64},{10,-64}}, color={0,0,127}));
      connect(qCool, preCool.Q_flow) annotation (Line(points={{-120,-80},{-84,
              -80},{-84,-94},{-4,-94},{-4,-74},{10,-74}}, color={0,0,127}));
    end Case600HeatCool;

    model Case900FF "Case 600FF, but with high thermal mass"
      extends TestModels.Detailed.Case600FF(
        matExtWal=extWalCase900,
        matFlo=floorCase900);

      parameter Buildings.ThermalZones.Detailed.Validation.BESTEST.Data.ExteriorWallCase900
         extWalCase900 "Exterior wall"
        annotation (Placement(transformation(extent={{60,60},{74,74}})));

      parameter Buildings.ThermalZones.Detailed.Validation.BESTEST.Data.FloorCase900
        floorCase900 "Floor"
        annotation (Placement(transformation(extent={{80,60},{94,74}})));

      annotation (
    experiment(StopTime=3.1536e+07),
    __Dymola_Commands(file="modelica://Buildings/Resources/Scripts/Dymola/ThermalZones/Detailed/Validation/BESTEST/Case900FF.mos"
            "Simulate and plot"), Documentation(info="<html>
<p>
This model is used for the test case 900FF of the BESTEST validation suite.
Case 900FF is a heavy-weight building.
The room temperature is free floating.
</p>
</html>",     revisions="<html>
<ul>
<li>
July 29, 2016, by Michael Wetter:<br/>
Added missing parameter declarations.
This is for
<a href=\"https://github.com/lbl-srg/modelica-buildings/issues/543\">issue 543</a>.
</li>
<li>
October 6, 2011, by Michael Wetter:<br/>
First implementation.
</li>
</ul>
</html>"));
    end Case900FF;

    model Case900HeatCool
      extends Case900FF;
      Modelica.Blocks.Interfaces.RealInput qHeat
        annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
      Modelica.Blocks.Interfaces.RealInput qCool
        annotation (Placement(transformation(extent={{-140,-100},{-100,-60}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preHeat
        annotation (Placement(transformation(extent={{10,-70},{22,-58}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preCool
        annotation (Placement(transformation(extent={{10,-80},{22,-68}})));
    equation
      connect(preHeat.port, roo.heaPorAir) annotation (Line(points={{22,-64},{
              26.25,-64},{26.25,-15}}, color={191,0,0}));
      connect(preCool.port, roo.heaPorAir) annotation (Line(points={{22,-74},{
              26.25,-74},{26.25,-15}}, color={191,0,0}));
      connect(qHeat, preHeat.Q_flow) annotation (Line(points={{-120,-40},{-70,
              -40},{-70,-92},{-10,-92},{-10,-64},{10,-64}}, color={0,0,127}));
      connect(qCool, preCool.Q_flow) annotation (Line(points={{-120,-80},{-80,
              -80},{-80,-98},{6,-98},{6,-74},{10,-74}}, color={0,0,127}));
    end Case900HeatCool;

    package Examples
      extends Modelica.Icons.ExamplesPackage;
      model Case600FF "Model of Case600FF to be used with MPCPy"
        import TestModels;
        extends Icons.MPCPy;
        extends TestModels.Detailed.Examples.BaseClasses.FreeFloat;
        TestModels.Detailed.Case600FF zone(lat=0.69394291059295)
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
      equation
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,70},{
                18,70},{18,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,40},{
                16,40},{16,2},{38,2}}, color={0,0,127}));
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(weaBus, zone.weaBus) annotation (Line(
            points={{-100,0},{-80,0},{-80,10.4},{41,10.4}},
            color={255,204,51},
            thickness=0.5), Text(
            string="%first",
            index=-1,
            extent={{-6,3},{-6,3}}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,100}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end Case600FF;

      model Case600SimpleHVAC_OpenLoop
        "Model of Case600 with a simple HVAC system and open loop control to be used with MPCPy"
        import TestModels;
        extends Icons.MPCPy;
        extends TestModels.Detailed.Examples.BaseClasses.SimpleHVAC_OpenLoop;
        TestModels.Detailed.Case600HeatCool zone(lat=0.69394291059295)
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
      equation
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,70},{
                18,70},{18,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,40},{
                16,40},{16,2},{38,2}}, color={0,0,127}));
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(weaBus, zone.weaBus) annotation (Line(
            points={{-100,0},{-4,0},{-4,10.4},{41,10.4}},
            color={255,204,51},
            thickness=0.5), Text(
            string="%first",
            index=-1,
            extent={{-6,3},{-6,3}}));
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{1,-44},{
                20,-44},{20,-4},{38,-4}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{1,-54},{
                24,-54},{24,-8},{38,-8}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,100}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end Case600SimpleHVAC_OpenLoop;

      model Case600SimpleHVAC_ClosedLoop
        "Model of Case600 with a simple HVAC system and closed loop control to be used with MPCPy"
        import TestModels;
        extends Icons.MPCPy;
        extends TestModels.Detailed.Examples.BaseClasses.SimpleHVAC_ClosedLoop;
        TestModels.Detailed.Case600HeatCool zone(lat=0.69394291059295)
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
        Modelica.Blocks.Interfaces.RealOutput uHeat
          "Heating heatflow output" annotation (Placement(transformation(extent=
                 {{100,-70},{120,-50}}), iconTransformation(extent={{100,-10},{
                  120,10}})));
        Modelica.Blocks.Interfaces.RealOutput uCool
          "Cooling heatflow output" annotation (Placement(transformation(extent=
                 {{100,-90},{120,-70}}), iconTransformation(extent={{100,-10},{
                  120,10}})));
      equation
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{1,-44},{
                20,-44},{20,-4},{38,-4}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{1,-54},{
                22,-54},{22,-8},{38,-8}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,70},{
                18,70},{18,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,40},{
                16,40},{16,2},{38,2}}, color={0,0,127}));
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(weaBus, zone.weaBus) annotation (Line(
            points={{-100,0},{-80,0},{-80,10.4},{41,10.4}},
            color={255,204,51},
            thickness=0.5), Text(
            string="%first",
            index=-1,
            extent={{-6,3},{-6,3}}));
        connect(zone.Tzone, controller.Tzone) annotation (Line(points={{61,0},{
                70,0},{70,-72},{-70,-72},{-70,-50},{-62,-50}}, color={0,0,127}));
        connect(uHeat, equipment.uHeat) annotation (Line(points={{110,-60},{96,
                -60},{96,-68},{-32,-68},{-32,-42},{-22,-42}}, color={0,0,127}));
        connect(uCool, equipment.uCool) annotation (Line(points={{110,-80},{-36,
                -80},{-36,-46},{-30,-46},{-30,-58},{-22,-58}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,100}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end Case600SimpleHVAC_ClosedLoop;

      model Case900FF "Model of Case900FF to be used with MPCPy"
        import TestModels;
        extends Icons.MPCPy;
        extends TestModels.Detailed.Examples.BaseClasses.FreeFloat;
        TestModels.Detailed.Case900FF zone(lat=0.69394291059295)
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
      equation
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,70},{
                18,70},{18,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,40},{
                16,40},{16,2},{38,2}}, color={0,0,127}));
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(weaBus, zone.weaBus) annotation (Line(
            points={{-100,0},{-80,0},{-80,10.4},{41,10.4}},
            color={255,204,51},
            thickness=0.5), Text(
            string="%first",
            index=-1,
            extent={{-6,3},{-6,3}}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,100}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end Case900FF;

      model Case900SimpleHVAC_OpenLoop
        "Model of Case900 with a simple HVAC system and open loop control to be used with MPCPy"
        import TestModels;
        extends Icons.MPCPy;
        extends TestModels.Detailed.Examples.BaseClasses.SimpleHVAC_OpenLoop;
        TestModels.Detailed.Case900HeatCool zone(lat=0.69394291059295)
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
      equation
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,70},{
                18,70},{18,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,40},{
                16,40},{16,2},{38,2}}, color={0,0,127}));
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(weaBus, zone.weaBus) annotation (Line(
            points={{-100,0},{-4,0},{-4,10.4},{41,10.4}},
            color={255,204,51},
            thickness=0.5), Text(
            string="%first",
            index=-1,
            extent={{-6,3},{-6,3}}));
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{1,-44},{
                20,-44},{20,-4},{38,-4}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{1,-54},{
                24,-54},{24,-8},{38,-8}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,100}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end Case900SimpleHVAC_OpenLoop;

      model Case900SimpleHVAC_ClosedLoop
        "Model of Case900 with a simple HVAC system and closed loop control to be used with MPCPy"
        import TestModels;
        extends Icons.MPCPy;
        extends TestModels.Detailed.Examples.BaseClasses.SimpleHVAC_ClosedLoop;
        TestModels.Detailed.Case900HeatCool zone(lat=0.69394291059295)
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
        Modelica.Blocks.Interfaces.RealOutput uHeat
          "Heating heatflow output" annotation (Placement(transformation(extent=
                 {{100,-70},{120,-50}}), iconTransformation(extent={{100,-10},{
                  120,10}})));
        Modelica.Blocks.Interfaces.RealOutput uCool
          "Cooling heatflow output" annotation (Placement(transformation(extent=
                 {{100,-90},{120,-70}}), iconTransformation(extent={{100,-10},{
                  120,10}})));
      equation
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{1,-44},{
                20,-44},{20,-4},{38,-4}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{1,-54},{
                22,-54},{22,-8},{38,-8}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,70},{
                18,70},{18,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,40},{
                16,40},{16,2},{38,2}}, color={0,0,127}));
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(weaBus, zone.weaBus) annotation (Line(
            points={{-100,0},{-80,0},{-80,10.4},{41,10.4}},
            color={255,204,51},
            thickness=0.5), Text(
            string="%first",
            index=-1,
            extent={{-6,3},{-6,3}}));
        connect(zone.Tzone, controller.Tzone) annotation (Line(points={{61,0},{
                70,0},{70,-72},{-70,-72},{-70,-50},{-62,-50}}, color={0,0,127}));
        connect(uHeat, equipment.uHeat) annotation (Line(points={{110,-60},{80,
                -60},{80,-68},{-34,-68},{-34,-42},{-22,-42}}, color={0,0,127}));
        connect(uCool, equipment.uCool) annotation (Line(points={{110,-80},{-36,
                -80},{-36,-46},{-30,-46},{-30,-58},{-22,-58}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,100}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end Case900SimpleHVAC_ClosedLoop;

      model simCase600FF "Test for running the Case600FF detailed model"
        extends Modelica.Icons.Example;
        import TestModels;
        parameter Modelica.SIunits.Angle lat=0.693943 "Latitude of building";
        TestModels.Detailed.Case600FF zone(lat=lat)
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
        Buildings.BoundaryConditions.WeatherData.ReaderTMY3 weaDat(filNam=
              "modelica://Buildings/Resources/weatherdata/DRYCOLD.mos",
            computeWetBulbTemperature=false)
          annotation (Placement(transformation(extent={{-40,20},{-28,32}})));
        Modelica.Blocks.Sources.Constant intLoads(k=0)
          annotation (Placement(transformation(extent={{-80,0},{-60,20}})));
        Modelica.Blocks.Interfaces.RealOutput Tzone
          "Zone mean air drybulb temperature"
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
      equation
        connect(weaDat.weaBus, zone.weaBus) annotation (Line(
            points={{-28,26},{41,26},{41,10.4}},
            color={255,204,51},
            thickness=0.5));
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(intLoads.y, zone.intRad) annotation (Line(points={{-59,10},{-36,
                10},{-36,8},{38,8}}, color={0,0,127}));
        connect(intLoads.y, zone.intCon) annotation (Line(points={{-59,10},{-36,
                10},{-36,5},{38,5}}, color={0,0,127}));
        connect(intLoads.y, zone.intLat) annotation (Line(points={{-59,10},{-36,
                10},{-36,2},{38,2}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)),
          experiment(
            StopTime=864000,
            Interval=300,
            Tolerance=1e-06,
            __Dymola_Algorithm="Radau"));
      end simCase600FF;

      model simCase600SimpleHVAC
        "Test for running the Case600SimpleHVAC detailed model"
        extends Modelica.Icons.Example;
        import TestModels;
        parameter Modelica.SIunits.Angle lat=0.693943 "Latitude of building";
        TestModels.Detailed.Case600HeatCool zone(lat=lat)
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
        Buildings.BoundaryConditions.WeatherData.ReaderTMY3 weaDat(filNam=
              "modelica://Buildings/Resources/weatherdata/DRYCOLD.mos",
            computeWetBulbTemperature=false)
          annotation (Placement(transformation(extent={{-40,20},{-28,32}})));
        Modelica.Blocks.Interfaces.RealOutput Tzone
          "Zone mean air drybulb temperature"
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
        TestModels.HVAC.Controllers.DualSetpoint controller
          annotation (Placement(transformation(extent={{-40,-40},{-20,-20}})));
        Modelica.Blocks.Sources.Constant heatSet(k=273.15 + 5)
          annotation (Placement(transformation(extent={{-80,-60},{-60,-40}})));
        Modelica.Blocks.Sources.Constant coolSet(k=273.15 + 100)
          annotation (Placement(transformation(extent={{-80,-30},{-60,-10}})));
        TestModels.HVAC.Equipment.SimpleHeaterCooler equipment
          annotation (Placement(transformation(extent={{0,-40},{20,-20}})));
        Modelica.Blocks.Math.Add add
          annotation (Placement(transformation(extent={{40,-40},{60,-20}})));
        Modelica.Blocks.Interfaces.RealOutput Phvac(unit="W")
          "Total electrical power consumed by HVAC system" annotation (Placement(
              transformation(extent={{100,-30},{120,-10}}), iconTransformation(extent=
                 {{100,-10},{120,10}})));
        Modelica.Blocks.Sources.Constant qRadGai_flow(k=120/48) "Radiative heat gain"
          annotation (Placement(transformation(extent={{-76,28},{-68,36}})));
        Modelica.Blocks.Sources.Constant qLatGai_flow(k=0) "Latent heat gain"
          annotation (Placement(transformation(extent={{-76,12},{-68,20}})));
        Modelica.Blocks.Sources.Constant qConGai_flow(k=80/48) "Convective heat gain"
          annotation (Placement(transformation(extent={{-88,20},{-80,28}})));
      equation
        connect(weaDat.weaBus, zone.weaBus) annotation (Line(
            points={{-28,26},{41,26},{41,10.4}},
            color={255,204,51},
            thickness=0.5));
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(zone.Tzone, controller.Tzone) annotation (Line(points={{61,0},{
                80,0},{80,-52},{-46,-52},{-46,-30},{-42,-30}}, color={0,0,127}));
        connect(heatSet.y, controller.HeatSet) annotation (Line(points={{-59,
                -50},{-56,-50},{-56,-36},{-42,-36}}, color={0,0,127}));
        connect(coolSet.y, controller.CoolSet) annotation (Line(points={{-59,
                -20},{-56,-20},{-56,-24},{-42,-24}}, color={0,0,127}));
        connect(controller.yHeat, equipment.uHeat)
          annotation (Line(points={{-19,-22},{-2,-22}}, color={0,0,127}));
        connect(controller.yCool, equipment.uCool) annotation (Line(points={{
                -19,-26},{-10,-26},{-10,-38},{-2,-38}}, color={0,0,127}));
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{21,-24},
                {26,-24},{26,-4},{38,-4}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{21,-34},
                {30,-34},{30,-8},{38,-8}}, color={0,0,127}));
        connect(equipment.PHeat, add.u1) annotation (Line(points={{21,-28},{32,-28},{32,
                -24},{38,-24}}, color={0,0,127}));
        connect(equipment.PCool, add.u2) annotation (Line(points={{21,-38},{32,-38},{32,
                -36},{38,-36}}, color={0,0,127}));
        connect(add.y, Phvac) annotation (Line(points={{61,-30},{90,-30},{90,-20},{110,
                -20}}, color={0,0,127}));
        connect(qRadGai_flow.y, zone.intRad) annotation (Line(points={{-67.6,32},
                {-54,32},{-54,8},{38,8}}, color={0,0,127}));
        connect(qConGai_flow.y, zone.intCon) annotation (Line(points={{-79.6,24},
                {-60,24},{-60,5},{38,5}}, color={0,0,127}));
        connect(qLatGai_flow.y, zone.intLat) annotation (Line(points={{-67.6,16},
                {-62,16},{-62,2},{38,2}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)),
          experiment(
            StopTime=864000,
            Interval=300,
            Tolerance=1e-06,
            __Dymola_Algorithm="Radau"));
      end simCase600SimpleHVAC;

      model simCase900FF "Test for running the Case900FF detailed model"
        extends Modelica.Icons.Example;
        parameter Modelica.SIunits.Angle lat=0.693943 "Latitude of building";
        TestModels.Detailed.Case900FF zone(lat=lat)
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
        Buildings.BoundaryConditions.WeatherData.ReaderTMY3 weaDat(filNam=
              "modelica://Buildings/Resources/weatherdata/DRYCOLD.mos",
            computeWetBulbTemperature=false)
          annotation (Placement(transformation(extent={{-40,20},{-28,32}})));
        Modelica.Blocks.Sources.Constant intLoads(k=0)
          annotation (Placement(transformation(extent={{-80,0},{-60,20}})));
        Modelica.Blocks.Interfaces.RealOutput Tzone
          "Zone mean air drybulb temperature"
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
      equation
        connect(weaDat.weaBus, zone.weaBus) annotation (Line(
            points={{-28,26},{41,26},{41,10.4}},
            color={255,204,51},
            thickness=0.5));
        connect(intLoads.y, zone.intRad) annotation (Line(points={{-59,10},{-20,
                10},{-20,8},{38,8}}, color={0,0,127}));
        connect(zone.intCon, zone.intRad) annotation (Line(points={{38,5},{-20,
                5},{-20,8},{38,8}}, color={0,0,127}));
        connect(zone.intLat, zone.intRad) annotation (Line(points={{38,2},{-20,
                2},{-20,8},{38,8}}, color={0,0,127}));
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end simCase900FF;

      model simCase900SimpleHVAC
        "Test for running the Case900FF detailed model"
        import TestModels;
        extends Modelica.Icons.Example;
        parameter Modelica.SIunits.Angle lat=0.693943 "Latitude of building";
        Case900HeatCool zone(lat=lat)
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
        Buildings.BoundaryConditions.WeatherData.ReaderTMY3 weaDat(filNam=
              "modelica://Buildings/Resources/weatherdata/DRYCOLD.mos",
            computeWetBulbTemperature=false)
          annotation (Placement(transformation(extent={{-40,20},{-28,32}})));
        Modelica.Blocks.Sources.Constant intLoads(k=0)
          annotation (Placement(transformation(extent={{-80,0},{-60,20}})));
        Modelica.Blocks.Interfaces.RealOutput Tzone
          "Zone mean air drybulb temperature"
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
        TestModels.HVAC.Controllers.DualSetpoint controller
          annotation (Placement(transformation(extent={{-40,-40},{-20,-20}})));
        Modelica.Blocks.Sources.Constant heatSet(k=273.15 + 21)
          annotation (Placement(transformation(extent={{-80,-60},{-60,-40}})));
        Modelica.Blocks.Sources.Constant coolSet(k=273.15 + 24)
          annotation (Placement(transformation(extent={{-80,-30},{-60,-10}})));
        TestModels.HVAC.Equipment.SimpleHeaterCooler equipment
          annotation (Placement(transformation(extent={{0,-40},{20,-20}})));
        Modelica.Blocks.Math.Add add
          annotation (Placement(transformation(extent={{40,-40},{60,-20}})));
        Modelica.Blocks.Interfaces.RealOutput Phvac(unit="W")
          "Total electrical power consumed by HVAC system" annotation (Placement(
              transformation(extent={{100,-30},{120,-10}}), iconTransformation(extent=
                 {{100,-10},{120,10}})));
      equation
        connect(weaDat.weaBus, zone.weaBus) annotation (Line(
            points={{-28,26},{41,26},{41,10.4}},
            color={255,204,51},
            thickness=0.5));
        connect(intLoads.y, zone.intRad) annotation (Line(points={{-59,10},{30,
                10},{30,8},{38,8}}, color={0,0,127}));
        connect(zone.intCon, zone.intRad) annotation (Line(points={{38,5},{30,5},
                {30,8},{38,8}}, color={0,0,127}));
        connect(zone.intLat, zone.intRad) annotation (Line(points={{38,2},{30,2},
                {30,8},{38,8}}, color={0,0,127}));
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(heatSet.y, controller.HeatSet) annotation (Line(points={{-59,
                -50},{-56,-50},{-56,-36},{-42,-36}}, color={0,0,127}));
        connect(coolSet.y, controller.CoolSet) annotation (Line(points={{-59,
                -20},{-56,-20},{-56,-24},{-42,-24}}, color={0,0,127}));
        connect(zone.Tzone, controller.Tzone) annotation (Line(points={{61,0},{
                80,0},{80,-52},{-46,-52},{-46,-30},{-42,-30}}, color={0,0,127}));
        connect(controller.yHeat, equipment.uHeat)
          annotation (Line(points={{-19,-22},{-2,-22}}, color={0,0,127}));
        connect(controller.yCool, equipment.uCool) annotation (Line(points={{
                -19,-26},{-10,-26},{-10,-38},{-2,-38}}, color={0,0,127}));
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{21,-24},
                {26,-24},{26,-4},{38,-4}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{21,-34},
                {30,-34},{30,-8},{38,-8}}, color={0,0,127}));
        connect(add.y, Phvac) annotation (Line(points={{61,-30},{90,-30},{90,-20},{110,
                -20}}, color={0,0,127}));
        connect(equipment.PHeat, add.u1) annotation (Line(points={{21,-28},{32,-28},{32,
                -24},{38,-24}}, color={0,0,127}));
        connect(equipment.PCool, add.u2) annotation (Line(points={{21,-38},{32,-38},{32,
                -36},{38,-36}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)),
          experiment(
            StopTime=864000,
            Interval=300,
            Tolerance=1e-06,
            __Dymola_Algorithm="Radau"));
      end simCase900SimpleHVAC;

      package BaseClasses
        extends Modelica.Icons.BasesPackage;
        partial model FreeFloat
          import TestModels;
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
          annotation (Placement(transformation(extent={{-110,-10},{-90,10}})));
          Modelica.Blocks.Interfaces.RealInput intRad_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,80},{-100,120}})));
          Modelica.Blocks.Interfaces.RealInput intLat_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,20},{-100,60}})));
          Modelica.Blocks.Interfaces.RealInput intCon_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,50},{-100,90}})));
          Modelica.Blocks.Interfaces.RealOutput Tzone(unit="K")
            "Zone mean air drybulb temperature"
            annotation (Placement(transformation(extent={{100,-10},{120,10}}),
                iconTransformation(extent={{100,-10},{120,10}})));
        equation
        connect(weaPAtm,weaBus. pAtm) annotation (Line(points={{-240,500},{-194,500},{-194,
                  0},{-100,0}},               color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaTDewPoi,weaBus. TDewPoi) annotation (Line(points={{-240,440},{-198,440},
                  {-198,0},{-100,0}},        color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaTDryBul,weaBus. TDryBul) annotation (Line(points={{-240,380},{-202,380},
                  {-202,0},{-100,0}},        color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaRelHum,weaBus. relHum) annotation (Line(points={{-240,320},{-190,320},
                  {-190,0},{-100,0}},   color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaNOpa,weaBus. nOpa) annotation (Line(points={{-240,260},{-188,260},{-188,
                  0},{-100,0}},    color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaCelHei,weaBus. celHei) annotation (Line(points={{-240,200},{-184,200},
                  {-184,0},{-100,0}},   color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaNTot,weaBus. nTot) annotation (Line(points={{-240,140},{-180,140},{-180,
                  0},{-100,0}},    color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaWinSpe,weaBus. winSpe) annotation (Line(points={{-240,80},{-176,80},{
                  -176,0},{-100,0}},   color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaWinDir,weaBus. winDir) annotation (Line(points={{-240,20},{-240,22},{
                  -172,22},{-172,0},{-100,0}},   color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaHHorIR,weaBus. HHorIR) annotation (Line(points={{-240,-40},{-168,-40},
                  {-168,0},{-100,0}},   color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaHDirNor,weaBus. HDirNor) annotation (Line(points={{-240,-100},{-164,-100},
                  {-164,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaHGloHor,weaBus. HGloHor) annotation (Line(points={{-240,-160},{-160,-160},
                  {-160,0},{-100,0}},                     color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaHDifHor,weaBus. HDifHor) annotation (Line(points={{-240,-220},{-156,-220},
                  {-156,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaTBlaSky,weaBus. TBlaSky) annotation (Line(points={{-240,-278},{-152,-278},
                  {-152,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaTWetBul,weaBus. TWetBul) annotation (Line(points={{-240,-340},{-148,-340},
                  {-148,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaSolZen,weaBus. solZen) annotation (Line(points={{-240,-402},{-144,-402},
                  {-144,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaCloTim,weaBus. cloTim) annotation (Line(points={{-240,-460},{-138,-460},
                  {-138,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaSolTim,weaBus. solTim) annotation (Line(points={{-240,-520},{-134,-520},
                  {-134,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
          annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
                coordinateSystem(preserveAspectRatio=false)));
        end FreeFloat;

        partial model SimpleHVAC_OpenLoop
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
          annotation (Placement(transformation(extent={{-110,-10},{-90,10}})));
          Modelica.Blocks.Interfaces.RealInput intRad_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,80},{-100,120}})));
          Modelica.Blocks.Interfaces.RealInput intLat_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,20},{-100,60}})));
          Modelica.Blocks.Interfaces.RealInput intCon_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,50},{-100,90}})));
          Modelica.Blocks.Interfaces.RealOutput Tzone(unit="K")
            "Zone mean air drybulb temperature"
            annotation (Placement(transformation(extent={{100,-10},{120,10}}),
                iconTransformation(extent={{100,-10},{120,10}})));
          HVAC.Equipment.SimpleHeaterCooler            equipment
            annotation (Placement(transformation(extent={{-20,-60},{0,-40}})));
          Modelica.Blocks.Interfaces.RealOutput Phvac(unit="W")
            "Total electrical power consumed by HVAC system" annotation (Placement(
                transformation(extent={{100,-50},{120,-30}}), iconTransformation(extent=
                   {{100,-10},{120,10}})));
          Modelica.Blocks.Math.Add add
            annotation (Placement(transformation(extent={{40,-60},{60,-40}})));
          Modelica.Blocks.Interfaces.RealInput uHeat "Heating signal input"
            annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
          Modelica.Blocks.Interfaces.RealInput uCool "Cooling signal input"
            annotation (Placement(transformation(extent={{-140,-100},{-100,-60}})));
        equation
        connect(weaPAtm,weaBus. pAtm) annotation (Line(points={{-240,500},{-194,500},{-194,
                  0},{-100,0}},               color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaTDewPoi,weaBus. TDewPoi) annotation (Line(points={{-240,440},{-198,440},
                  {-198,0},{-100,0}},        color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaTDryBul,weaBus. TDryBul) annotation (Line(points={{-240,380},{-202,380},
                  {-202,0},{-100,0}},        color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaRelHum,weaBus. relHum) annotation (Line(points={{-240,320},{-190,320},
                  {-190,0},{-100,0}},   color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaNOpa,weaBus. nOpa) annotation (Line(points={{-240,260},{-188,260},{-188,
                  0},{-100,0}},    color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaCelHei,weaBus. celHei) annotation (Line(points={{-240,200},{-184,200},
                  {-184,0},{-100,0}},   color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaNTot,weaBus. nTot) annotation (Line(points={{-240,140},{-180,140},{-180,
                  0},{-100,0}},    color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaWinSpe,weaBus. winSpe) annotation (Line(points={{-240,80},{-176,80},{
                  -176,0},{-100,0}},   color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaWinDir,weaBus. winDir) annotation (Line(points={{-240,20},{-240,22},{
                  -172,22},{-172,0},{-100,0}},   color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaHHorIR,weaBus. HHorIR) annotation (Line(points={{-240,-40},{-168,-40},
                  {-168,0},{-100,0}},   color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaHDirNor,weaBus. HDirNor) annotation (Line(points={{-240,-100},{-164,-100},
                  {-164,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaHGloHor,weaBus. HGloHor) annotation (Line(points={{-240,-160},{-160,-160},
                  {-160,0},{-100,0}},                     color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaHDifHor,weaBus. HDifHor) annotation (Line(points={{-240,-220},{-156,-220},
                  {-156,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaTBlaSky,weaBus. TBlaSky) annotation (Line(points={{-240,-278},{-152,-278},
                  {-152,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaTWetBul,weaBus. TWetBul) annotation (Line(points={{-240,-340},{-148,-340},
                  {-148,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaSolZen,weaBus. solZen) annotation (Line(points={{-240,-402},{-144,-402},
                  {-144,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaCloTim,weaBus. cloTim) annotation (Line(points={{-240,-460},{-138,-460},
                  {-138,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaSolTim,weaBus. solTim) annotation (Line(points={{-240,-520},{-134,-520},
                  {-134,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
          connect(equipment.PHeat,add. u1) annotation (Line(points={{1,-48},{30,-48},{30,
                  -44},{38,-44}}, color={0,0,127}));
          connect(equipment.PCool,add. u2) annotation (Line(points={{1,-58},{30,-58},{30,
                  -56},{38,-56}}, color={0,0,127}));
          connect(add.y,Phvac)  annotation (Line(points={{61,-50},{80,-50},{80,-40},{110,
                  -40}}, color={0,0,127}));
          connect(equipment.uHeat,uHeat)  annotation (Line(points={{-22,-42},{-80,
                  -42},{-80,-40},{-120,-40}}, color={0,0,127}));
          connect(equipment.uCool,uCool)  annotation (Line(points={{-22,-58},{-80,
                  -58},{-80,-80},{-120,-80}}, color={0,0,127}));
          annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
                coordinateSystem(preserveAspectRatio=false)));
        end SimpleHVAC_OpenLoop;

        partial model SimpleHVAC_ClosedLoop
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
          annotation (Placement(transformation(extent={{-110,-10},{-90,10}})));
          Modelica.Blocks.Interfaces.RealInput intRad_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,80},{-100,120}})));
          Modelica.Blocks.Interfaces.RealInput intLat_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,20},{-100,60}})));
          Modelica.Blocks.Interfaces.RealInput intCon_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,50},{-100,90}})));
          Modelica.Blocks.Interfaces.RealOutput Tzone(unit="K")
            "Zone mean air drybulb temperature"
            annotation (Placement(transformation(extent={{100,-10},{120,10}}),
                iconTransformation(extent={{100,-10},{120,10}})));
          HVAC.Equipment.SimpleHeaterCooler            equipment
            annotation (Placement(transformation(extent={{-20,-60},{0,-40}})));
          HVAC.Controllers.DualSetpoint            controller
            annotation (Placement(transformation(extent={{-60,-60},{-40,-40}})));
          Modelica.Blocks.Interfaces.RealOutput Phvac(unit="W")
            "Total electrical power consumed by HVAC system" annotation (Placement(
                transformation(extent={{100,-50},{120,-30}}), iconTransformation(extent=
                   {{100,-10},{120,10}})));
          Modelica.Blocks.Math.Add add
            annotation (Placement(transformation(extent={{40,-60},{60,-40}})));
          Modelica.Blocks.Interfaces.RealInput coolSet annotation (Placement(
                transformation(extent={{-140,-60},{-100,-20}})));
          Modelica.Blocks.Interfaces.RealInput heatSet annotation (Placement(
                transformation(extent={{-140,-100},{-100,-60}})));
        equation
        connect(weaPAtm,weaBus. pAtm) annotation (Line(points={{-240,500},{-194,500},{-194,
                  0},{-100,0}},               color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaTDewPoi,weaBus. TDewPoi) annotation (Line(points={{-240,440},{-198,440},
                  {-198,0},{-100,0}},        color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaTDryBul,weaBus. TDryBul) annotation (Line(points={{-240,380},{-202,380},
                  {-202,0},{-100,0}},        color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaRelHum,weaBus. relHum) annotation (Line(points={{-240,320},{-190,320},
                  {-190,0},{-100,0}},   color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaNOpa,weaBus. nOpa) annotation (Line(points={{-240,260},{-188,260},{-188,
                  0},{-100,0}},    color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaCelHei,weaBus. celHei) annotation (Line(points={{-240,200},{-184,200},
                  {-184,0},{-100,0}},   color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaNTot,weaBus. nTot) annotation (Line(points={{-240,140},{-180,140},{-180,
                  0},{-100,0}},    color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaWinSpe,weaBus. winSpe) annotation (Line(points={{-240,80},{-176,80},{
                  -176,0},{-100,0}},   color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaWinDir,weaBus. winDir) annotation (Line(points={{-240,20},{-240,22},{
                  -172,22},{-172,0},{-100,0}},   color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaHHorIR,weaBus. HHorIR) annotation (Line(points={{-240,-40},{-168,-40},
                  {-168,0},{-100,0}},   color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaHDirNor,weaBus. HDirNor) annotation (Line(points={{-240,-100},{-164,-100},
                  {-164,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaHGloHor,weaBus. HGloHor) annotation (Line(points={{-240,-160},{-160,-160},
                  {-160,0},{-100,0}},                     color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaHDifHor,weaBus. HDifHor) annotation (Line(points={{-240,-220},{-156,-220},
                  {-156,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaTBlaSky,weaBus. TBlaSky) annotation (Line(points={{-240,-278},{-152,-278},
                  {-152,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaTWetBul,weaBus. TWetBul) annotation (Line(points={{-240,-340},{-148,-340},
                  {-148,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaSolZen,weaBus. solZen) annotation (Line(points={{-240,-402},{-144,-402},
                  {-144,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaCloTim,weaBus. cloTim) annotation (Line(points={{-240,-460},{-138,-460},
                  {-138,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(weaSolTim,weaBus. solTim) annotation (Line(points={{-240,-520},{-134,-520},
                  {-134,0},{-100,0}},         color={0,0,127}), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
          connect(controller.yHeat,equipment. uHeat)
            annotation (Line(points={{-39,-42},{-22,-42}}, color={0,0,127}));
          connect(controller.yCool,equipment. uCool) annotation (Line(points={{-39,-46},
                  {-30,-46},{-30,-58},{-22,-58}}, color={0,0,127}));
          connect(equipment.PHeat,add. u1) annotation (Line(points={{1,-48},{30,-48},{30,
                  -44},{38,-44}}, color={0,0,127}));
          connect(equipment.PCool,add. u2) annotation (Line(points={{1,-58},{30,-58},{30,
                  -56},{38,-56}}, color={0,0,127}));
          connect(add.y,Phvac)  annotation (Line(points={{61,-50},{80,-50},{80,-40},{110,
                  -40}}, color={0,0,127}));
          connect(controller.CoolSet,coolSet)  annotation (Line(points={{-62,-44},
                  {-80,-44},{-80,-40},{-120,-40}}, color={0,0,127}));
          connect(controller.HeatSet,heatSet)  annotation (Line(points={{-62,-56},
                  {-80,-56},{-80,-80},{-120,-80}}, color={0,0,127}));
          annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
                coordinateSystem(preserveAspectRatio=false)));
        end SimpleHVAC_ClosedLoop;
      end BaseClasses;
    end Examples;
  end Detailed;

  package MPC

    model R1C1 "Reduced order zone model with no heating and cooling inputs"
      parameter Modelica.SIunits.Area Aflo = 48 "Floor area of zone";
      parameter Modelica.SIunits.Area Awall = 48 + 2 * 2.7 * (6 + 8) "Wall and ceiling area";
      parameter Modelica.SIunits.Volume V = 48 * 2.7 "Zone volume";
      parameter Units.ThermalResistancePerArea R = 0.01 "Resistance of zone";
      parameter Modelica.SIunits.HeatCapacity C = 1e5 "Capacitance of zone";
      parameter Real shgc = 0.8 "Solar heat gain coefficient of window";
      parameter Modelica.SIunits.Temperature T0_C = 20+273.15 "Initial temperature of C";

      Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor thermostat
        annotation (Placement(transformation(extent={{60,-30},{80,-10}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor air(C=C, T(fixed=true,
            start=T0_C))
        annotation (Placement(transformation(extent={{38,-20},{58,0}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tR(R=R/Awall)
        annotation (Placement(transformation(extent={{10,-50},{30,-30}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature
        prescribedTemperature
        annotation (Placement(transformation(extent={{-20,-50},{0,-30}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf2
        annotation (Placement(transformation(extent={{8,-10},{28,10}})));
      Modelica.Blocks.Math.Sum sum1(nin=2)
        annotation (Placement(transformation(extent={{-20,-10},{0,10}})));
      Modelica.Blocks.Math.Gain gain(k=shgc)
        annotation (Placement(transformation(extent={{-22,50},{-2,70}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf1
        annotation (Placement(transformation(extent={{8,50},{28,70}})));
      Modelica.Blocks.Interfaces.RealOutput Tzone(unit="K")
        "Zone mean air drybulb temperature"
        annotation (Placement(transformation(extent={{100,-10},{120,10}}),
            iconTransformation(extent={{100,-10},{120,10}})));
      Modelica.Blocks.Interfaces.RealInput intRad
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,60},{-100,100}})));
      Modelica.Blocks.Interfaces.RealInput intCon
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,30},{-100,70}})));
      Modelica.Blocks.Interfaces.RealInput intLat
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,0},{-100,40}})));
      Modelica.Blocks.Math.Gain gain1(k=Aflo)
        annotation (Placement(transformation(extent={{-80,70},{-60,90}})));
      Modelica.Blocks.Math.Gain gain2(k=Aflo)
        annotation (Placement(transformation(extent={{-80,40},{-60,60}})));
      Modelica.Blocks.Math.Gain gain3(k=Aflo)
        annotation (Placement(transformation(extent={{-80,10},{-60,30}})));
      Modelica.Blocks.Interfaces.RealInput weaTDryBul
        annotation (Placement(transformation(extent={{-140,-40},{-100,0}})));
      Modelica.Blocks.Interfaces.RealInput weaHGloHor
        annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
    equation

      connect(thermostat.T,Tzone)  annotation (Line(points={{80,-20},{90,-20},{
              90,0},{110,0}},
                        color={0,0,127}));
      connect(tR.port_b, air.port) annotation (Line(points={{30,-40},{30,-40},{34,-40},
              {34,-20},{48,-20}}, color={191,0,0}));
      connect(thermostat.port, air.port)
        annotation (Line(points={{60,-20},{48,-20}}, color={191,0,0}));
      connect(prescribedTemperature.port, tR.port_a)
        annotation (Line(points={{0,-40},{0,-40},{10,-40}}, color={191,0,0}));
      connect(sum1.y, phf2.Q_flow)
        annotation (Line(points={{1,0},{4.5,0},{8,0}}, color={0,0,127}));
      connect(phf2.port, air.port) annotation (Line(points={{28,0},{28,0},{34,0},{34,
              -20},{48,-20}}, color={191,0,0}));
      connect(gain.y, phf1.Q_flow)
        annotation (Line(points={{-1,60},{8,60}}, color={0,0,127}));
      connect(phf1.port, air.port) annotation (Line(points={{28,60},{34,60},{34,-20},
              {48,-20}}, color={191,0,0}));
      connect(intRad, gain1.u)
        annotation (Line(points={{-120,80},{-101,80},{-82,80}}, color={0,0,127}));
      connect(intCon, gain2.u)
        annotation (Line(points={{-120,50},{-101,50},{-82,50}}, color={0,0,127}));
      connect(intLat, gain3.u)
        annotation (Line(points={{-120,20},{-82,20},{-82,20}}, color={0,0,127}));
      connect(gain1.y, sum1.u[1]) annotation (Line(points={{-59,80},{-40,80},{-40,-1},
              {-22,-1}}, color={0,0,127}));
      connect(gain2.y, sum1.u[2]) annotation (Line(points={{-59,50},{-44,50},{-44,1},
              {-22,1}}, color={0,0,127}));
      connect(prescribedTemperature.T, weaTDryBul)
        annotation (Line(points={{-22,-40},{-34,-40},{-34,-20},{-46,-20},{-46,
              -20},{-72,-20},{-72,-20},{-120,-20}},     color={0,0,127}));
      connect(weaHGloHor, gain.u) annotation (Line(points={{-120,-40},{-80,-40},
              {-80,-40},{-38,-40},{-38,60},{-24,60}},
                                       color={0,0,127}));
      annotation (
    experiment(
          StopTime=3.1536e+07,
          Interval=3600,
          __Dymola_Algorithm="Radau"),
    __Dymola_Commands(file="modelica://Buildings/Resources/Scripts/Dymola/ThermalZones/Detailed/Validation/BESTEST/Case600FF.mos"
            "Simulate and plot"), Documentation(info="<html>
<p>
This model is used for the test case 600FF of the BESTEST validation suite.
Case 600FF is a light-weight building.
The room temperature is free floating.
</p>
</html>",     revisions="<html>
<ul>
<li>
October 29, 2016, by Michael Wetter:<br/>
Placed a capacity at the room-facing surface
to reduce the dimension of the nonlinear system of equations,
which generally decreases computing time.<br/>
Removed the pressure drop element which is not needed.<br/>
Linearized the radiative heat transfer, which is the default in
the library, and avoids a large nonlinear system of equations.<br/>
This is for
<a href=\"https://github.com/lbl-srg/modelica-buildings/issues/565\">issue 565</a>.
</li>
<li>
December 22, 2014 by Michael Wetter:<br/>
Removed <code>Modelica.Fluid.System</code>
to address issue
<a href=\"https://github.com/lbl-srg/modelica-buildings/issues/311\">#311</a>.
</li>
<li>
October 9, 2013, by Michael Wetter:<br/>
Implemented soil properties using a record so that <code>TSol</code> and
<code>TLiq</code> are assigned.
This avoids an error when the model is checked in the pedantic mode.
</li>
<li>
July 15, 2012, by Michael Wetter:<br/>
Added reference results.
Changed implementation to make this model the base class
for all BESTEST cases.
Added computation of hourly and annual averaged room air temperature.
<li>
October 6, 2011, by Michael Wetter:<br/>
First implementation.
</li>
</ul>
</html>"),
        Icon(graphics={
            Rectangle(
              extent={{-92,92},{92,-92}},
              pattern=LinePattern.None,
              lineColor={117,148,176},
              fillColor={170,213,255},
              fillPattern=FillPattern.Sphere),
            Rectangle(
              extent={{-100,-100},{100,100}},
              lineColor={95,95,95},
              fillColor={95,95,95},
              fillPattern=FillPattern.Solid),
            Rectangle(
              extent={{-92,92},{92,-92}},
              pattern=LinePattern.None,
              lineColor={117,148,176},
              fillColor={170,213,255},
              fillPattern=FillPattern.Sphere),
            Rectangle(
              extent={{-44,42},{54,-46}},
              lineColor={0,0,0},
              fillColor={135,135,135},
              fillPattern=FillPattern.Solid),
            Text(
              extent={{-150,144},{150,104}},
              textString="%name",
              lineColor={0,0,255})}),
        __Dymola_experimentSetupOutput(events=false));
    end R1C1;

    model R1C1HeatCool
      "Reduced order zone model with heating and cooling inputs"
      extends R1C1;
      Modelica.Blocks.Interfaces.RealInput qHeat
        annotation (Placement(transformation(extent={{-140,-100},{-100,-60}})));
      Modelica.Blocks.Interfaces.RealInput qCool
        annotation (Placement(transformation(extent={{-140,-120},{-100,-80}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preHeat
        annotation (Placement(transformation(extent={{8,-82},{28,-62}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preCool
        annotation (Placement(transformation(extent={{8,-100},{28,-80}})));
    equation
      connect(qHeat, preHeat.Q_flow) annotation (Line(points={{-120,-80},{-40,
              -80},{-40,-72},{8,-72}}, color={0,0,127}));
      connect(qCool, preCool.Q_flow) annotation (Line(points={{-120,-100},{-40,
              -100},{-40,-90},{8,-90}}, color={0,0,127}));
      connect(preHeat.port, air.port) annotation (Line(points={{28,-72},{48,-72},
              {48,-20}}, color={191,0,0}));
      connect(preCool.port, air.port) annotation (Line(points={{28,-90},{48,-90},
              {48,-20}}, color={191,0,0}));
    end R1C1HeatCool;

    model R2C2 "Reduced order zone model with no heating and cooling inputs"
      parameter Modelica.SIunits.Area Aflo = 48 "Floor area of zone";
      parameter Modelica.SIunits.Area Awall = 48 + 2 * 2.7 * (6 + 8) "Wall and ceiling area";
      parameter Modelica.SIunits.Volume V = 48 * 2.7 "Zone volume";
      parameter Units.ThermalResistancePerArea R = 0.01 "Resistance of zone";
      parameter Units.ThermalResistancePerArea Ri = 0.01 "Resistance of internal thermal mass";
      parameter Modelica.SIunits.HeatCapacity C = 1e5 "Capacitance of zone";
      parameter Units.HeatCapacityPerArea Ci = 1e5 "Capacitance of internal thermal mass";
      parameter Real shgc = 0.8 "Solar heat gain coefficient of window";
      parameter Modelica.SIunits.Temperature T0_C = 20+273.15 "Initial temperature of C";
      parameter Modelica.SIunits.Temperature T0_Ci = 20+273.15 "Initial temperature of Ci";

      Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor thermostat
        annotation (Placement(transformation(extent={{60,-30},{80,-10}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor air(C=C, T(fixed=true,
            start=T0_C))
        annotation (Placement(transformation(extent={{40,-20},{60,0}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tR(R=R/Awall)
        annotation (Placement(transformation(extent={{10,-50},{30,-30}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature
        prescribedTemperature
        annotation (Placement(transformation(extent={{-20,-50},{0,-30}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf2
        annotation (Placement(transformation(extent={{8,-10},{28,10}})));
      Modelica.Blocks.Math.Gain gain(k=shgc)
        annotation (Placement(transformation(extent={{-22,50},{-2,70}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf1
        annotation (Placement(transformation(extent={{8,50},{28,70}})));
      Modelica.Blocks.Interfaces.RealOutput Tzone(unit="K")
        "Zone mean air drybulb temperature"
        annotation (Placement(transformation(extent={{100,-10},{120,10}}),
            iconTransformation(extent={{100,-10},{120,10}})));
      Modelica.Blocks.Interfaces.RealInput intRad
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,60},{-100,100}})));
      Modelica.Blocks.Interfaces.RealInput intCon
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,30},{-100,70}})));
      Modelica.Blocks.Interfaces.RealInput intLat
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,0},{-100,40}})));
      Modelica.Blocks.Math.Gain gain1(k=Aflo)
        annotation (Placement(transformation(extent={{-80,70},{-60,90}})));
      Modelica.Blocks.Math.Gain gain2(k=Aflo)
        annotation (Placement(transformation(extent={{-80,40},{-60,60}})));
      Modelica.Blocks.Math.Gain gain3(k=Aflo)
        annotation (Placement(transformation(extent={{-80,10},{-60,30}})));
      Modelica.Blocks.Interfaces.RealInput weaTDryBul
        annotation (Placement(transformation(extent={{-140,-40},{-100,0}})));
      Modelica.Blocks.Interfaces.RealInput weaHGloHor
        annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor intMass(C=Ci*Aflo, T(fixed=
              true, start=T0_Ci))
        annotation (Placement(transformation(extent={{32,60},{52,80}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tRi(R=Ri/Aflo)
        annotation (Placement(transformation(
            extent={{-10,-10},{10,10}},
            rotation=0,
            origin={20,30})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf3
        annotation (Placement(transformation(extent={{-24,20},{-4,40}})));
    equation

      connect(thermostat.T,Tzone)  annotation (Line(points={{80,-20},{90,-20},{
              90,0},{110,0}},
                        color={0,0,127}));
      connect(tR.port_b, air.port) annotation (Line(points={{30,-40},{30,-40},{34,-40},
              {34,-20},{50,-20}}, color={191,0,0}));
      connect(thermostat.port, air.port)
        annotation (Line(points={{60,-20},{50,-20}}, color={191,0,0}));
      connect(prescribedTemperature.port, tR.port_a)
        annotation (Line(points={{0,-40},{0,-40},{10,-40}}, color={191,0,0}));
      connect(phf2.port, air.port) annotation (Line(points={{28,0},{28,0},{34,0},{34,
              -20},{50,-20}}, color={191,0,0}));
      connect(gain.y, phf1.Q_flow)
        annotation (Line(points={{-1,60},{8,60}}, color={0,0,127}));
      connect(intRad, gain1.u)
        annotation (Line(points={{-120,80},{-101,80},{-82,80}}, color={0,0,127}));
      connect(intCon, gain2.u)
        annotation (Line(points={{-120,50},{-101,50},{-82,50}}, color={0,0,127}));
      connect(intLat, gain3.u)
        annotation (Line(points={{-120,20},{-82,20},{-82,20}}, color={0,0,127}));
      connect(prescribedTemperature.T, weaTDryBul)
        annotation (Line(points={{-22,-40},{-34,-40},{-34,-20},{-60,-20},{-60,
              -20},{-60,-20},{-60,-20},{-120,-20}},     color={0,0,127}));
      connect(weaHGloHor, gain.u) annotation (Line(points={{-120,-40},{-36,-40},
              {-36,60},{-24,60}},      color={0,0,127}));
      connect(phf1.port, intMass.port)
        annotation (Line(points={{28,60},{42,60}}, color={191,0,0}));
      connect(intMass.port, tRi.port_a) annotation (Line(points={{42,60},{42,50},{2,
              50},{2,30},{10,30}}, color={191,0,0}));
      connect(tRi.port_b, air.port) annotation (Line(points={{30,30},{34,30},{34,-20},
              {50,-20}}, color={191,0,0}));
      connect(gain1.y, phf3.Q_flow) annotation (Line(points={{-59,80},{-40,80},{-40,
              30},{-24,30}}, color={0,0,127}));
      connect(phf3.port, tRi.port_a)
        annotation (Line(points={{-4,30},{-2,30},{10,30}}, color={191,0,0}));
      connect(gain2.y, phf2.Q_flow) annotation (Line(points={{-59,50},{-50,50},{-50,
              0},{8,0}}, color={0,0,127}));
      annotation (
    experiment(
          StopTime=3.1536e+07,
          Interval=3600,
          __Dymola_Algorithm="Radau"),
    __Dymola_Commands(file="modelica://Buildings/Resources/Scripts/Dymola/ThermalZones/Detailed/Validation/BESTEST/Case600FF.mos"
            "Simulate and plot"), Documentation(info="<html>
<p>
This model is used for the test case 600FF of the BESTEST validation suite.
Case 600FF is a light-weight building.
The room temperature is free floating.
</p>
</html>",     revisions="<html>
<ul>
<li>
October 29, 2016, by Michael Wetter:<br/>
Placed a capacity at the room-facing surface
to reduce the dimension of the nonlinear system of equations,
which generally decreases computing time.<br/>
Removed the pressure drop element which is not needed.<br/>
Linearized the radiative heat transfer, which is the default in
the library, and avoids a large nonlinear system of equations.<br/>
This is for
<a href=\"https://github.com/lbl-srg/modelica-buildings/issues/565\">issue 565</a>.
</li>
<li>
December 22, 2014 by Michael Wetter:<br/>
Removed <code>Modelica.Fluid.System</code>
to address issue
<a href=\"https://github.com/lbl-srg/modelica-buildings/issues/311\">#311</a>.
</li>
<li>
October 9, 2013, by Michael Wetter:<br/>
Implemented soil properties using a record so that <code>TSol</code> and
<code>TLiq</code> are assigned.
This avoids an error when the model is checked in the pedantic mode.
</li>
<li>
July 15, 2012, by Michael Wetter:<br/>
Added reference results.
Changed implementation to make this model the base class
for all BESTEST cases.
Added computation of hourly and annual averaged room air temperature.
<li>
October 6, 2011, by Michael Wetter:<br/>
First implementation.
</li>
</ul>
</html>"),
        Icon(graphics={
            Rectangle(
              extent={{-92,92},{92,-92}},
              pattern=LinePattern.None,
              lineColor={117,148,176},
              fillColor={170,213,255},
              fillPattern=FillPattern.Sphere),
            Rectangle(
              extent={{-100,-100},{100,100}},
              lineColor={95,95,95},
              fillColor={95,95,95},
              fillPattern=FillPattern.Solid),
            Rectangle(
              extent={{-92,92},{92,-92}},
              pattern=LinePattern.None,
              lineColor={117,148,176},
              fillColor={170,213,255},
              fillPattern=FillPattern.Sphere),
            Rectangle(
              extent={{-44,42},{54,-46}},
              lineColor={0,0,0},
              fillColor={135,135,135},
              fillPattern=FillPattern.Solid),
            Text(
              extent={{-150,144},{150,104}},
              textString="%name",
              lineColor={0,0,255})}),
        __Dymola_experimentSetupOutput(events=false));
    end R2C2;

    model R2C2HeatCool
      "Reduced order zone model with heating and cooling inputs"
      extends R2C2;
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preHeat
        annotation (Placement(transformation(extent={{8,-82},{28,-62}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preCool
        annotation (Placement(transformation(extent={{8,-100},{28,-80}})));
      Modelica.Blocks.Interfaces.RealInput qHeat
        annotation (Placement(transformation(extent={{-140,-100},{-100,-60}})));
      Modelica.Blocks.Interfaces.RealInput qCool
        annotation (Placement(transformation(extent={{-140,-120},{-100,-80}})));
    equation
      connect(qHeat, preHeat.Q_flow) annotation (Line(points={{-120,-80},{-56,
              -80},{-56,-72},{8,-72}}, color={0,0,127}));
      connect(qCool, preCool.Q_flow) annotation (Line(points={{-120,-100},{-56,
              -100},{-56,-90},{8,-90}}, color={0,0,127}));
      connect(preHeat.port, air.port) annotation (Line(points={{28,-72},{50,-72},
              {50,-20}}, color={191,0,0}));
      connect(preCool.port, air.port) annotation (Line(points={{28,-90},{50,-90},
              {50,-20}}, color={191,0,0}));
    end R2C2HeatCool;

    model R3C3 "Reduced order zone model with no heating and cooling inputs"
      parameter Modelica.SIunits.Area Aflo = 48 "Floor area of zone";
      parameter Modelica.SIunits.Area Awall = 48 + 2 * 2.7 * (6 + 8) "Wall and ceiling area";
      parameter Modelica.SIunits.Volume V = 48 * 2.7 "Zone volume";
      parameter Units.ThermalResistancePerArea R = 0.01 "Resistance of zone";
      parameter Units.ThermalResistancePerArea Ri = 0.01 "Resistance of internal thermal mass";
      parameter Units.ThermalResistancePerArea Re = 0.01 "Resistance of external thermal mass";
      parameter Modelica.SIunits.HeatCapacity C = 1e5 "Capacitance of zone";
      parameter Units.HeatCapacityPerArea Ci = 1e5 "Capacitance of internal thermal mass";
      parameter Units.HeatCapacityPerArea Ce = 1e5 "Capacitance of external thermal mass";
      parameter Real shgc = 0.8 "Solar heat gain coefficient of window";
      parameter Real shgce = 0.8 "Solar heat gain coefficient of ext. walls";
      parameter Modelica.SIunits.Temperature T0_C = 20+273.15 "Initial temperature of C";
      parameter Modelica.SIunits.Temperature T0_Ci = 20+273.15 "Initial temperature of Ci";
      parameter Modelica.SIunits.Temperature T0_Ce = 20+273.15 "Initial temperature of Ce";

      Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor thermostat
        annotation (Placement(transformation(extent={{60,-30},{80,-10}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor air(C=C, T(start=T0_C,
            fixed=true))
        annotation (Placement(transformation(extent={{40,-20},{60,0}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tRe(R=Re/Awall)
        annotation (Placement(transformation(extent={{-60,-50},{-40,-30}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature
        prescribedTemperature
        annotation (Placement(transformation(extent={{-88,-50},{-68,-30}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf2
        annotation (Placement(transformation(extent={{13.5,3.5},{26.5,16.5}})));
      Modelica.Blocks.Math.Gain gain(k=shgc)
        annotation (Placement(transformation(extent={{-15,53},{-1,67}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf1
        annotation (Placement(transformation(extent={{14,54},{26,66}})));
      Modelica.Blocks.Interfaces.RealOutput Tzone(unit="K")
        "Zone mean air drybulb temperature"
        annotation (Placement(transformation(extent={{100,-10},{120,10}}),
            iconTransformation(extent={{100,-10},{120,10}})));
      Modelica.Blocks.Interfaces.RealInput intRad
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,60},{-100,100}})));
      Modelica.Blocks.Interfaces.RealInput intCon
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,30},{-100,70}})));
      Modelica.Blocks.Interfaces.RealInput intLat
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,0},{-100,40}})));
      Modelica.Blocks.Math.Gain gain1(k=Aflo)
        annotation (Placement(transformation(extent={{-77,73},{-63,87}})));
      Modelica.Blocks.Math.Gain gain2(k=Aflo)
        annotation (Placement(transformation(extent={{-77,43},{-63,57}})));
      Modelica.Blocks.Math.Gain gain3(k=Aflo)
        annotation (Placement(transformation(extent={{-77,13},{-63,27}})));
      Modelica.Blocks.Interfaces.RealInput weaTDryBul
        annotation (Placement(transformation(extent={{-140,-40},{-100,0}})));
      Modelica.Blocks.Interfaces.RealInput weaHGloHor
        annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor intMass(C=Ci*Aflo, T(fixed=
              true, start=T0_Ci))
        annotation (Placement(transformation(extent={{32,60},{52,80}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tRi(R=Ri/Aflo)
        annotation (Placement(transformation(
            extent={{-10,-10},{10,10}},
            rotation=0,
            origin={20,30})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tR(R=R/Awall)
        annotation (Placement(transformation(extent={{10,-50},{30,-30}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor extMass(C=Ce*Awall, T(fixed=
              true, start=T0_Ce))
        annotation (Placement(transformation(extent={{-20,-40},{0,-20}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf3
        annotation (Placement(transformation(extent={{-16,24},{-4,36}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf4 annotation (
          Placement(transformation(
            extent={{-6,-6},{6,6}},
            rotation=-90,
            origin={-34,-26})));
      Modelica.Blocks.Math.Gain gain4(k=Awall/(Aflo + Awall))
        annotation (Placement(transformation(extent={{-7,-7},{7,7}},
            rotation=-90,
            origin={-34,-8})));
      Modelica.Blocks.Math.Gain gain5(k=Aflo/(Aflo + Awall))
        annotation (Placement(transformation(extent={{-7,-7},{7,7}},
            rotation=0,
            origin={-40,80})));
      Modelica.Blocks.Math.Gain gain6(k=shgce)
        annotation (Placement(transformation(extent={{-89,-73},{-75,-59}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf5
        annotation (Placement(transformation(extent={{-6,-6},{6,6}},
            rotation=90,
            origin={-10,-54})));
    equation

      connect(thermostat.T,Tzone)  annotation (Line(points={{80,-20},{90,-20},{
              90,0},{110,0}},
                        color={0,0,127}));
      connect(thermostat.port, air.port)
        annotation (Line(points={{60,-20},{50,-20}}, color={191,0,0}));
      connect(prescribedTemperature.port, tRe.port_a)
        annotation (Line(points={{-68,-40},{-60,-40}},           color={191,0,0}));
      connect(phf2.port, air.port) annotation (Line(points={{26.5,10},{26.5,10},{34,
              10},{34,-20},{50,-20}}, color={191,0,0}));
      connect(gain.y, phf1.Q_flow)
        annotation (Line(points={{-0.3,60},{-0.3,60},{14,60}},
                                                 color={0,0,127}));
      connect(intRad, gain1.u)
        annotation (Line(points={{-120,80},{-78.4,80}},         color={0,0,127}));
      connect(intCon, gain2.u)
        annotation (Line(points={{-120,50},{-78.4,50}},         color={0,0,127}));
      connect(intLat, gain3.u)
        annotation (Line(points={{-120,20},{-100,20},{-78.4,20}},
                                                               color={0,0,127}));
      connect(prescribedTemperature.T, weaTDryBul)
        annotation (Line(points={{-90,-40},{-94,-40},{-94,-20},{-120,-20}},
                                                        color={0,0,127}));
      connect(weaHGloHor, gain.u) annotation (Line(points={{-120,-40},{-120,-40},
              {-96,-40},{-96,-54},{-24,-54},{-24,60},{-16.4,60}},
                                       color={0,0,127}));
      connect(phf1.port, intMass.port)
        annotation (Line(points={{26,60},{26,60},{42,60}},
                                                   color={191,0,0}));
      connect(intMass.port, tRi.port_a) annotation (Line(points={{42,60},{42,50},{2,
              50},{2,30},{10,30}}, color={191,0,0}));
      connect(tRi.port_b, air.port) annotation (Line(points={{30,30},{34,30},{34,-20},
              {50,-20}}, color={191,0,0}));
      connect(air.port, tR.port_b) annotation (Line(points={{50,-20},{34,-20},{34,-40},
              {30,-40}}, color={191,0,0}));
      connect(tRe.port_b, extMass.port)
        annotation (Line(points={{-40,-40},{-10,-40}}, color={191,0,0}));
      connect(tR.port_a, extMass.port)
        annotation (Line(points={{10,-40},{-10,-40}}, color={191,0,0}));
      connect(gain2.y, phf2.Q_flow) annotation (Line(points={{-62.3,50},{-50,50},{-50,
              10},{13.5,10}},
                         color={0,0,127}));
      connect(phf3.port, tRi.port_a)
        annotation (Line(points={{-4,30},{-4,30},{10,30}}, color={191,0,0}));
      connect(phf4.Q_flow, gain4.y) annotation (Line(points={{-34,-20},{-34,-20},{-34,
              -18},{-34,-15.7}}, color={0,0,127}));
      connect(gain1.y, gain4.u) annotation (Line(points={{-62.3,80},{-54,80},{-54,60},
              {-34,60},{-34,0.4}}, color={0,0,127}));
      connect(gain1.y, gain5.u)
        annotation (Line(points={{-62.3,80},{-48.4,80}}, color={0,0,127}));
      connect(gain5.y, phf3.Q_flow) annotation (Line(points={{-32.3,80},{-28,80},{-28,
              30},{-16,30}}, color={0,0,127}));
      connect(phf4.port, extMass.port) annotation (Line(points={{-34,-32},{-34,
              -32},{-34,-40},{-10,-40}}, color={191,0,0}));
      connect(gain6.y, phf5.Q_flow) annotation (Line(points={{-74.3,-66},{-74.3,
              -66},{-10,-66},{-10,-60}},
                                    color={0,0,127}));
      connect(gain6.u, weaHGloHor) annotation (Line(points={{-90.4,-66},{-96,
              -66},{-96,-40},{-120,-40}},
                                color={0,0,127}));
      connect(phf5.port, extMass.port) annotation (Line(points={{-10,-48},{-10,
              -44},{-10,-40}}, color={191,0,0}));
      annotation (
    experiment(
          StopTime=3.1536e+07,
          Interval=3600,
          __Dymola_Algorithm="Radau"),
    __Dymola_Commands(file="modelica://Buildings/Resources/Scripts/Dymola/ThermalZones/Detailed/Validation/BESTEST/Case600FF.mos"
            "Simulate and plot"), Documentation(info="<html>
<p>
This model is used for the test case 600FF of the BESTEST validation suite.
Case 600FF is a light-weight building.
The room temperature is free floating.
</p>
</html>",     revisions="<html>
<ul>
<li>
October 29, 2016, by Michael Wetter:<br/>
Placed a capacity at the room-facing surface
to reduce the dimension of the nonlinear system of equations,
which generally decreases computing time.<br/>
Removed the pressure drop element which is not needed.<br/>
Linearized the radiative heat transfer, which is the default in
the library, and avoids a large nonlinear system of equations.<br/>
This is for
<a href=\"https://github.com/lbl-srg/modelica-buildings/issues/565\">issue 565</a>.
</li>
<li>
December 22, 2014 by Michael Wetter:<br/>
Removed <code>Modelica.Fluid.System</code>
to address issue
<a href=\"https://github.com/lbl-srg/modelica-buildings/issues/311\">#311</a>.
</li>
<li>
October 9, 2013, by Michael Wetter:<br/>
Implemented soil properties using a record so that <code>TSol</code> and
<code>TLiq</code> are assigned.
This avoids an error when the model is checked in the pedantic mode.
</li>
<li>
July 15, 2012, by Michael Wetter:<br/>
Added reference results.
Changed implementation to make this model the base class
for all BESTEST cases.
Added computation of hourly and annual averaged room air temperature.
<li>
October 6, 2011, by Michael Wetter:<br/>
First implementation.
</li>
</ul>
</html>"),
        Icon(graphics={
            Rectangle(
              extent={{-92,92},{92,-92}},
              pattern=LinePattern.None,
              lineColor={117,148,176},
              fillColor={170,213,255},
              fillPattern=FillPattern.Sphere),
            Rectangle(
              extent={{-100,-100},{100,100}},
              lineColor={95,95,95},
              fillColor={95,95,95},
              fillPattern=FillPattern.Solid),
            Rectangle(
              extent={{-92,92},{92,-92}},
              pattern=LinePattern.None,
              lineColor={117,148,176},
              fillColor={170,213,255},
              fillPattern=FillPattern.Sphere),
            Rectangle(
              extent={{-44,42},{54,-46}},
              lineColor={0,0,0},
              fillColor={135,135,135},
              fillPattern=FillPattern.Solid),
            Text(
              extent={{-150,144},{150,104}},
              textString="%name",
              lineColor={0,0,255})}),
        __Dymola_experimentSetupOutput(events=false));
    end R3C3;

    model R3C3HeatCool
      "Reduced order zone model with heating and cooling inputs"
      extends R3C3;
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preHeat
        annotation (Placement(transformation(extent={{8,-82},{28,-62}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preCool
        annotation (Placement(transformation(extent={{8,-100},{28,-80}})));
      Modelica.Blocks.Interfaces.RealInput qHeat
        annotation (Placement(transformation(extent={{-140,-100},{-100,-60}})));
      Modelica.Blocks.Interfaces.RealInput qCool
        annotation (Placement(transformation(extent={{-140,-120},{-100,-80}})));
    equation
      connect(qHeat, preHeat.Q_flow) annotation (Line(points={{-120,-80},{-20,
              -80},{-20,-72},{8,-72}}, color={0,0,127}));
      connect(qCool, preCool.Q_flow) annotation (Line(points={{-120,-100},{0,
              -100},{0,-90},{8,-90}}, color={0,0,127}));
      connect(preHeat.port, air.port) annotation (Line(points={{28,-72},{50,-72},
              {50,-20}}, color={191,0,0}));
      connect(preCool.port, air.port) annotation (Line(points={{28,-90},{50,-90},
              {50,-20}}, color={191,0,0}));
    end R3C3HeatCool;

    model R4C3 "Reduced order zone model with no heating and cooling inputs"
      parameter Modelica.SIunits.Area Aflo = 48 "Floor area of zone";
      parameter Modelica.SIunits.Area Awall = 48 + 2 * 2.7 * (6 + 8) "Wall and ceiling area";
      parameter Modelica.SIunits.Volume V = 48 * 2.7 "Zone volume";
      parameter Units.ThermalResistancePerArea R = 0.01 "Resistance of zone";
      parameter Units.ThermalResistancePerArea Ri = 0.01 "Resistance of internal thermal mass";
      parameter Units.ThermalResistancePerArea Re = 0.01 "Resistance of external thermal mass";
      parameter Units.ThermalResistancePerArea Rinf = 0.01 "Resistance of infiltration";
      parameter Modelica.SIunits.HeatCapacity C = 1e5 "Capacitance of zone";
      parameter Units.HeatCapacityPerArea Ci = 1e5 "Capacitance of internal thermal mass";
      parameter Units.HeatCapacityPerArea Ce = 1e5 "Capacitance of external thermal mass";
      parameter Real shgc = 0.8 "Solar heat gain coefficient of window";
      parameter Real shgce = 0.8 "Solar heat gain coefficient of ext. walls";
      parameter Modelica.SIunits.Temperature T0_C = 20+273.15 "Initial temperature of C";
      parameter Modelica.SIunits.Temperature T0_Ci = 20+273.15 "Initial temperature of Ci";
      parameter Modelica.SIunits.Temperature T0_Ce = 20+273.15 "Initial temperature of Ce";

      Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor thermostat
        annotation (Placement(transformation(extent={{60,-30},{80,-10}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor air(C=C, T(fixed=
              true, start=T0_C))
        annotation (Placement(transformation(extent={{40,-20},{60,0}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tRe(R=Re/Awall)
        annotation (Placement(transformation(extent={{-60,-50},{-40,-30}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature
        prescribedTemperature
        annotation (Placement(transformation(extent={{-88,-50},{-68,-30}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf2
        annotation (Placement(transformation(extent={{13.5,3.5},{26.5,16.5}})));
      Modelica.Blocks.Math.Gain gain(k=shgc)
        annotation (Placement(transformation(extent={{-15,53},{-1,67}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf1
        annotation (Placement(transformation(extent={{14,54},{26,66}})));
      Modelica.Blocks.Interfaces.RealOutput Tzone(unit="K")
        "Zone mean air drybulb temperature"
        annotation (Placement(transformation(extent={{100,-10},{120,10}}),
            iconTransformation(extent={{100,-10},{120,10}})));
      Modelica.Blocks.Interfaces.RealInput intRad
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,60},{-100,100}})));
      Modelica.Blocks.Interfaces.RealInput intCon
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,30},{-100,70}})));
      Modelica.Blocks.Interfaces.RealInput intLat
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,0},{-100,40}})));
      Modelica.Blocks.Math.Gain gain1(k=Aflo)
        annotation (Placement(transformation(extent={{-77,73},{-63,87}})));
      Modelica.Blocks.Math.Gain gain2(k=Aflo)
        annotation (Placement(transformation(extent={{-77,43},{-63,57}})));
      Modelica.Blocks.Math.Gain gain3(k=Aflo)
        annotation (Placement(transformation(extent={{-77,13},{-63,27}})));
      Modelica.Blocks.Interfaces.RealInput weaTDryBul
        annotation (Placement(transformation(extent={{-140,-40},{-100,0}})));
      Modelica.Blocks.Interfaces.RealInput weaHGloHor
        annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor intMass(C=Ci*Aflo, T(fixed=
              true, start=T0_Ci))
        annotation (Placement(transformation(extent={{32,60},{52,80}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tRi(R=Ri/Aflo)
        annotation (Placement(transformation(
            extent={{-10,-10},{10,10}},
            rotation=0,
            origin={20,30})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tR(R=R/Awall)
        annotation (Placement(transformation(extent={{10,-50},{30,-30}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor extMass(C=Ce*Awall, T(fixed=
              true, start=T0_Ce))
        annotation (Placement(transformation(extent={{-20,-40},{0,-20}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf3
        annotation (Placement(transformation(extent={{-16,24},{-4,36}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf4 annotation (
          Placement(transformation(
            extent={{-6,-6},{6,6}},
            rotation=-90,
            origin={-34,-26})));
      Modelica.Blocks.Math.Gain gain4(k=Awall/(Aflo + Awall))
        annotation (Placement(transformation(extent={{-7,-7},{7,7}},
            rotation=-90,
            origin={-34,-8})));
      Modelica.Blocks.Math.Gain gain5(k=Aflo/(Aflo + Awall))
        annotation (Placement(transformation(extent={{-7,-7},{7,7}},
            rotation=0,
            origin={-40,80})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tRinf(R=Rinf/Awall)
        annotation (Placement(transformation(extent={{-2,-74},{18,-54}})));
      Modelica.Blocks.Math.Gain gain6(k=shgce)
        annotation (Placement(transformation(extent={{-93,-75},{-79,-61}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf5
        annotation (Placement(transformation(extent={{-6,-6},{6,6}},
            rotation=90,
            origin={-10,-52})));
    equation

      connect(thermostat.T,Tzone)  annotation (Line(points={{80,-20},{90,-20},{
              90,0},{110,0}},
                        color={0,0,127}));
      connect(thermostat.port, air.port)
        annotation (Line(points={{60,-20},{50,-20}}, color={191,0,0}));
      connect(prescribedTemperature.port, tRe.port_a)
        annotation (Line(points={{-68,-40},{-60,-40}},           color={191,0,0}));
      connect(phf2.port, air.port) annotation (Line(points={{26.5,10},{26.5,10},{34,
              10},{34,-20},{50,-20}}, color={191,0,0}));
      connect(gain.y, phf1.Q_flow)
        annotation (Line(points={{-0.3,60},{-0.3,60},{14,60}},
                                                 color={0,0,127}));
      connect(intRad, gain1.u)
        annotation (Line(points={{-120,80},{-78.4,80}},         color={0,0,127}));
      connect(intCon, gain2.u)
        annotation (Line(points={{-120,50},{-78.4,50}},         color={0,0,127}));
      connect(intLat, gain3.u)
        annotation (Line(points={{-120,20},{-100,20},{-78.4,20}},
                                                               color={0,0,127}));
      connect(prescribedTemperature.T, weaTDryBul)
        annotation (Line(points={{-90,-40},{-94,-40},{-94,-20},{-120,-20}},
                                                        color={0,0,127}));
      connect(weaHGloHor, gain.u) annotation (Line(points={{-120,-40},{-120,-40},
              {-98,-40},{-98,-58},{-22,-58},{-22,60},{-16.4,60}},
                                       color={0,0,127}));
      connect(phf1.port, intMass.port)
        annotation (Line(points={{26,60},{26,60},{42,60}},
                                                   color={191,0,0}));
      connect(intMass.port, tRi.port_a) annotation (Line(points={{42,60},{42,50},{2,
              50},{2,30},{10,30}}, color={191,0,0}));
      connect(tRi.port_b, air.port) annotation (Line(points={{30,30},{34,30},{34,-20},
              {50,-20}}, color={191,0,0}));
      connect(air.port, tR.port_b) annotation (Line(points={{50,-20},{34,-20},{34,-40},
              {30,-40}}, color={191,0,0}));
      connect(tRe.port_b, extMass.port)
        annotation (Line(points={{-40,-40},{-10,-40}}, color={191,0,0}));
      connect(tR.port_a, extMass.port)
        annotation (Line(points={{10,-40},{-10,-40}}, color={191,0,0}));
      connect(gain2.y, phf2.Q_flow) annotation (Line(points={{-62.3,50},{-50,50},{-50,
              10},{13.5,10}},
                         color={0,0,127}));
      connect(phf3.port, tRi.port_a)
        annotation (Line(points={{-4,30},{-4,30},{10,30}}, color={191,0,0}));
      connect(extMass.port, phf4.port)
        annotation (Line(points={{-10,-40},{-34,-40},{-34,-32}}, color={191,0,0}));
      connect(phf4.Q_flow, gain4.y) annotation (Line(points={{-34,-20},{-34,-20},{-34,
              -18},{-34,-15.7}}, color={0,0,127}));
      connect(gain1.y, gain4.u) annotation (Line(points={{-62.3,80},{-54,80},{-54,60},
              {-34,60},{-34,0.4}}, color={0,0,127}));
      connect(gain1.y, gain5.u)
        annotation (Line(points={{-62.3,80},{-48.4,80}}, color={0,0,127}));
      connect(gain5.y, phf3.Q_flow) annotation (Line(points={{-32.3,80},{-28,80},{-28,
              30},{-16,30}}, color={0,0,127}));
      connect(prescribedTemperature.port, tRinf.port_a) annotation (Line(points={{-68,-40},
              {-64,-40},{-64,-64},{-2,-64}},       color={191,0,0}));
      connect(air.port, tRinf.port_b) annotation (Line(points={{50,-20},{34,-20},
              {34,-64},{18,-64}},
                             color={191,0,0}));
      connect(weaHGloHor, gain6.u) annotation (Line(points={{-120,-40},{-98,-40},
              {-98,-68},{-94.4,-68}},
                                 color={0,0,127}));
      connect(gain6.y, phf5.Q_flow) annotation (Line(points={{-78.3,-68},{-10,
              -68},{-10,-58}},
                         color={0,0,127}));
      connect(phf5.port, extMass.port) annotation (Line(points={{-10,-46},{-10,
              -46},{-10,-40}}, color={191,0,0}));
      annotation (
    experiment(
          StopTime=3.1536e+07,
          Interval=3600,
          __Dymola_Algorithm="Radau"),
    __Dymola_Commands(file="modelica://Buildings/Resources/Scripts/Dymola/ThermalZones/Detailed/Validation/BESTEST/Case600FF.mos"
            "Simulate and plot"), Documentation(info="<html>
<p>
This model is used for the test case 600FF of the BESTEST validation suite.
Case 600FF is a light-weight building.
The room temperature is free floating.
</p>
</html>",     revisions="<html>
<ul>
<li>
October 29, 2016, by Michael Wetter:<br/>
Placed a capacity at the room-facing surface
to reduce the dimension of the nonlinear system of equations,
which generally decreases computing time.<br/>
Removed the pressure drop element which is not needed.<br/>
Linearized the radiative heat transfer, which is the default in
the library, and avoids a large nonlinear system of equations.<br/>
This is for
<a href=\"https://github.com/lbl-srg/modelica-buildings/issues/565\">issue 565</a>.
</li>
<li>
December 22, 2014 by Michael Wetter:<br/>
Removed <code>Modelica.Fluid.System</code>
to address issue
<a href=\"https://github.com/lbl-srg/modelica-buildings/issues/311\">#311</a>.
</li>
<li>
October 9, 2013, by Michael Wetter:<br/>
Implemented soil properties using a record so that <code>TSol</code> and
<code>TLiq</code> are assigned.
This avoids an error when the model is checked in the pedantic mode.
</li>
<li>
July 15, 2012, by Michael Wetter:<br/>
Added reference results.
Changed implementation to make this model the base class
for all BESTEST cases.
Added computation of hourly and annual averaged room air temperature.
<li>
October 6, 2011, by Michael Wetter:<br/>
First implementation.
</li>
</ul>
</html>"),
        Icon(graphics={
            Rectangle(
              extent={{-92,92},{92,-92}},
              pattern=LinePattern.None,
              lineColor={117,148,176},
              fillColor={170,213,255},
              fillPattern=FillPattern.Sphere),
            Rectangle(
              extent={{-100,-100},{100,100}},
              lineColor={95,95,95},
              fillColor={95,95,95},
              fillPattern=FillPattern.Solid),
            Rectangle(
              extent={{-92,92},{92,-92}},
              pattern=LinePattern.None,
              lineColor={117,148,176},
              fillColor={170,213,255},
              fillPattern=FillPattern.Sphere),
            Rectangle(
              extent={{-44,42},{54,-46}},
              lineColor={0,0,0},
              fillColor={135,135,135},
              fillPattern=FillPattern.Solid),
            Text(
              extent={{-150,144},{150,104}},
              textString="%name",
              lineColor={0,0,255})}),
        __Dymola_experimentSetupOutput(events=false));
    end R4C3;

    model R4C3HeatCool
      "Reduced order zone model with heating and cooling inputs"
      extends R4C3;
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preHeat
        annotation (Placement(transformation(extent={{8,-90},{28,-70}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preCool
        annotation (Placement(transformation(extent={{8,-108},{28,-88}})));
      Modelica.Blocks.Interfaces.RealInput qHeat
        annotation (Placement(transformation(extent={{-140,-100},{-100,-60}})));
      Modelica.Blocks.Interfaces.RealInput qCool
        annotation (Placement(transformation(extent={{-140,-120},{-100,-80}})));
    equation
      connect(qCool, preCool.Q_flow) annotation (Line(points={{-120,-100},{-56,
              -100},{-56,-98},{8,-98}}, color={0,0,127}));
      connect(qHeat, preHeat.Q_flow)
        annotation (Line(points={{-120,-80},{8,-80}}, color={0,0,127}));
      connect(preHeat.port, air.port) annotation (Line(points={{28,-80},{50,-80},
              {50,-20}}, color={191,0,0}));
      connect(preCool.port, air.port) annotation (Line(points={{28,-98},{50,-98},
              {50,-20}}, color={191,0,0}));
    end R4C3HeatCool;

    model R4C4 "Reduced order zone model with no heating and cooling inputs"
      parameter Modelica.SIunits.Area Aflo = 48 "Floor area of zone";
      parameter Modelica.SIunits.Area Awall = 48 + 2 * 2.7 * (6 + 8) "Wall and ceiling area";
      parameter Modelica.SIunits.Volume V = 48 * 2.7 "Zone volume";
      parameter Units.ThermalResistancePerArea R = 0.01 "Resistance of zone";
      parameter Units.ThermalResistancePerArea Ri = 0.01 "Resistance of internal thermal mass";
      parameter Units.ThermalResistancePerArea Re = 0.01 "Resistance of external thermal mass";
      parameter Units.ThermalResistancePerArea Rem = 0.01 "Resistance of external thermal mass (middle layer)";
      parameter Modelica.SIunits.HeatCapacity C = 1e5 "Capacitance of zone";
      parameter Units.HeatCapacityPerArea Ci = 1e5 "Capacitance of internal thermal mass";
      parameter Units.HeatCapacityPerArea Ce = 1e5 "Capacitance of external thermal mass";
      parameter Units.HeatCapacityPerArea Cem = 1e5 "Capacitance of external thermal mass (middle layer)";
      parameter Real shgc = 0.8 "Solar heat gain coefficient of window";
      parameter Real shgce = 0.8 "Solar heat gain coefficient of ext. walls";
      parameter Modelica.SIunits.Temperature T0_C = 20+273.15 "Initial temperature of C";
      parameter Modelica.SIunits.Temperature T0_Ci = 20+273.15 "Initial temperature of Ci";
      parameter Modelica.SIunits.Temperature T0_Ce = 20+273.15 "Initial temperature of Ce";
      parameter Modelica.SIunits.Temperature T0_Cem = 20+273.15 "Initial temperature of Cem";
      Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor thermostat
        annotation (Placement(transformation(extent={{60,-30},{80,-10}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor air(C=C, T(fixed=
              true, start=T0_C))
        annotation (Placement(transformation(extent={{42,-20},{62,0}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tRe(R=Re/Awall)
        annotation (Placement(transformation(extent={{-62,-48},{-46,-32}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature
        prescribedTemperature
        annotation (Placement(transformation(extent={{-90,-50},{-70,-30}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf2
        annotation (Placement(transformation(extent={{13.5,3.5},{26.5,16.5}})));
      Modelica.Blocks.Math.Gain gain(k=shgc)
        annotation (Placement(transformation(extent={{-15,53},{-1,67}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf1
        annotation (Placement(transformation(extent={{14,54},{26,66}})));
      Modelica.Blocks.Interfaces.RealOutput Tzone(unit="K")
        "Zone mean air drybulb temperature"
        annotation (Placement(transformation(extent={{100,-10},{120,10}}),
            iconTransformation(extent={{100,-10},{120,10}})));
      Modelica.Blocks.Interfaces.RealInput intRad
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,60},{-100,100}})));
      Modelica.Blocks.Interfaces.RealInput intCon
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,30},{-100,70}})));
      Modelica.Blocks.Interfaces.RealInput intLat
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,0},{-100,40}})));
      Modelica.Blocks.Math.Gain gain1(k=Aflo)
        annotation (Placement(transformation(extent={{-77,73},{-63,87}})));
      Modelica.Blocks.Math.Gain gain2(k=Aflo)
        annotation (Placement(transformation(extent={{-77,43},{-63,57}})));
      Modelica.Blocks.Math.Gain gain3(k=Aflo)
        annotation (Placement(transformation(extent={{-77,13},{-63,27}})));
      Modelica.Blocks.Interfaces.RealInput weaTDryBul
        annotation (Placement(transformation(extent={{-140,-40},{-100,0}})));
      Modelica.Blocks.Interfaces.RealInput weaHGloHor
        annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor intMass(C=Ci*Aflo, T(fixed=
              true, start=T0_Ci))
        annotation (Placement(transformation(extent={{32,60},{52,80}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tRi(R=Ri/Aflo)
        annotation (Placement(transformation(
            extent={{-10,-10},{10,10}},
            rotation=0,
            origin={20,30})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tR(R=R/Awall)
        annotation (Placement(transformation(extent={{24,-48},{40,-32}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor extMass(C=Ce*Awall, T(fixed=
              true, start=T0_Ce))
        annotation (Placement(transformation(extent={{-46,-40},{-26,-20}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf3
        annotation (Placement(transformation(extent={{-16,24},{-4,36}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf4 annotation (
          Placement(transformation(
            extent={{-6,-6},{6,6}},
            rotation=-90,
            origin={18,-28})));
      Modelica.Blocks.Math.Gain gain4(k=Awall/(Aflo + Awall))
        annotation (Placement(transformation(extent={{-7,-7},{7,7}},
            rotation=0,
            origin={-2,-4})));
      Modelica.Blocks.Math.Gain gain5(k=Aflo/(Aflo + Awall))
        annotation (Placement(transformation(extent={{-7,-7},{7,7}},
            rotation=0,
            origin={-40,80})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tRem(R=Rem/Awall)
        annotation (Placement(transformation(extent={{-22,-48},{-6,-32}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor extMass1(C=Cem*Awall, T(fixed=
              true, start=T0_Cem))
        annotation (Placement(transformation(extent={{-6,-40},{14,-20}})));
      Modelica.Blocks.Math.Gain gain6(k=shgce)
        annotation (Placement(transformation(extent={{-91,-75},{-77,-61}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf5
        annotation (Placement(transformation(extent={{-6,-6},{6,6}},
            rotation=90,
            origin={-36,-58})));
    equation

      connect(thermostat.T,Tzone)  annotation (Line(points={{80,-20},{90,-20},{
              90,0},{110,0}},
                        color={0,0,127}));
      connect(thermostat.port, air.port)
        annotation (Line(points={{60,-20},{52,-20}}, color={191,0,0}));
      connect(prescribedTemperature.port, tRe.port_a)
        annotation (Line(points={{-70,-40},{-62,-40}},           color={191,0,0}));
      connect(phf2.port, air.port) annotation (Line(points={{26.5,10},{26.5,10},{42,
              10},{42,-20},{52,-20}}, color={191,0,0}));
      connect(gain.y, phf1.Q_flow)
        annotation (Line(points={{-0.3,60},{-0.3,60},{14,60}},
                                                 color={0,0,127}));
      connect(intRad, gain1.u)
        annotation (Line(points={{-120,80},{-78.4,80}},         color={0,0,127}));
      connect(intCon, gain2.u)
        annotation (Line(points={{-120,50},{-78.4,50}},         color={0,0,127}));
      connect(intLat, gain3.u)
        annotation (Line(points={{-120,20},{-100,20},{-78.4,20}},
                                                               color={0,0,127}));
      connect(prescribedTemperature.T, weaTDryBul)
        annotation (Line(points={{-92,-40},{-96,-40},{-96,-20},{-120,-20}},
                                                        color={0,0,127}));
      connect(weaHGloHor, gain.u) annotation (Line(points={{-120,-40},{-98,-40},
              {-98,-54},{-24,-54},{-24,60},{-16.4,60}},
                                       color={0,0,127}));
      connect(phf1.port, intMass.port)
        annotation (Line(points={{26,60},{26,60},{42,60}},
                                                   color={191,0,0}));
      connect(intMass.port, tRi.port_a) annotation (Line(points={{42,60},{42,50},{2,
              50},{2,30},{10,30}}, color={191,0,0}));
      connect(tRi.port_b, air.port) annotation (Line(points={{30,30},{42,30},{42,-20},
              {52,-20}}, color={191,0,0}));
      connect(air.port, tR.port_b) annotation (Line(points={{52,-20},{42,-20},{42,-40},
              {40,-40}}, color={191,0,0}));
      connect(tRe.port_b, extMass.port)
        annotation (Line(points={{-46,-40},{-36,-40}}, color={191,0,0}));
      connect(gain2.y, phf2.Q_flow) annotation (Line(points={{-62.3,50},{-50,50},{-50,
              10},{13.5,10}},
                         color={0,0,127}));
      connect(phf3.port, tRi.port_a)
        annotation (Line(points={{-4,30},{-4,30},{10,30}}, color={191,0,0}));
      connect(phf4.Q_flow, gain4.y) annotation (Line(points={{18,-22},{18,-22},{18,-4},
              {5.7,-4}},         color={0,0,127}));
      connect(gain1.y, gain4.u) annotation (Line(points={{-62.3,80},{-56,80},{-56,60},
              {-40,60},{-40,-4},{-10.4,-4}},
                                   color={0,0,127}));
      connect(gain1.y, gain5.u)
        annotation (Line(points={{-62.3,80},{-48.4,80}}, color={0,0,127}));
      connect(gain5.y, phf3.Q_flow) annotation (Line(points={{-32.3,80},{-28,80},{-28,
              30},{-16,30}}, color={0,0,127}));
      connect(extMass.port, tRem.port_a)
        annotation (Line(points={{-36,-40},{-36,-40},{-22,-40}}, color={191,0,0}));
      connect(tRem.port_b, extMass1.port)
        annotation (Line(points={{-6,-40},{4,-40}}, color={191,0,0}));
      connect(tR.port_a, extMass1.port)
        annotation (Line(points={{24,-40},{24,-40},{4,-40}},  color={191,0,0}));
      connect(extMass1.port, phf4.port)
        annotation (Line(points={{4,-40},{18,-40},{18,-34}}, color={191,0,0}));
      connect(gain6.u, weaHGloHor) annotation (Line(points={{-92.4,-68},{-98,
              -68},{-98,-40},{-120,-40}},
                                color={0,0,127}));
      connect(gain6.y, phf5.Q_flow) annotation (Line(points={{-76.3,-68},{-36,
              -68},{-36,-64}},
                         color={0,0,127}));
      connect(phf5.port, extMass.port) annotation (Line(points={{-36,-52},{-36,
              -46},{-36,-40}}, color={191,0,0}));
      annotation (
    experiment(
          StopTime=3.1536e+07,
          Interval=3600,
          __Dymola_Algorithm="Radau"),
    __Dymola_Commands(file="modelica://Buildings/Resources/Scripts/Dymola/ThermalZones/Detailed/Validation/BESTEST/Case600FF.mos"
            "Simulate and plot"), Documentation(info="<html>
<p>
This model is used for the test case 600FF of the BESTEST validation suite.
Case 600FF is a light-weight building.
The room temperature is free floating.
</p>
</html>",     revisions="<html>
<ul>
<li>
October 29, 2016, by Michael Wetter:<br/>
Placed a capacity at the room-facing surface
to reduce the dimension of the nonlinear system of equations,
which generally decreases computing time.<br/>
Removed the pressure drop element which is not needed.<br/>
Linearized the radiative heat transfer, which is the default in
the library, and avoids a large nonlinear system of equations.<br/>
This is for
<a href=\"https://github.com/lbl-srg/modelica-buildings/issues/565\">issue 565</a>.
</li>
<li>
December 22, 2014 by Michael Wetter:<br/>
Removed <code>Modelica.Fluid.System</code>
to address issue
<a href=\"https://github.com/lbl-srg/modelica-buildings/issues/311\">#311</a>.
</li>
<li>
October 9, 2013, by Michael Wetter:<br/>
Implemented soil properties using a record so that <code>TSol</code> and
<code>TLiq</code> are assigned.
This avoids an error when the model is checked in the pedantic mode.
</li>
<li>
July 15, 2012, by Michael Wetter:<br/>
Added reference results.
Changed implementation to make this model the base class
for all BESTEST cases.
Added computation of hourly and annual averaged room air temperature.
<li>
October 6, 2011, by Michael Wetter:<br/>
First implementation.
</li>
</ul>
</html>"),
        Icon(graphics={
            Rectangle(
              extent={{-92,92},{92,-92}},
              pattern=LinePattern.None,
              lineColor={117,148,176},
              fillColor={170,213,255},
              fillPattern=FillPattern.Sphere),
            Rectangle(
              extent={{-100,-100},{100,100}},
              lineColor={95,95,95},
              fillColor={95,95,95},
              fillPattern=FillPattern.Solid),
            Rectangle(
              extent={{-92,92},{92,-92}},
              pattern=LinePattern.None,
              lineColor={117,148,176},
              fillColor={170,213,255},
              fillPattern=FillPattern.Sphere),
            Rectangle(
              extent={{-44,42},{54,-46}},
              lineColor={0,0,0},
              fillColor={135,135,135},
              fillPattern=FillPattern.Solid),
            Text(
              extent={{-150,144},{150,104}},
              textString="%name",
              lineColor={0,0,255})}),
        __Dymola_experimentSetupOutput(events=false));
    end R4C4;

    model R4C4HeatCool
      "Reduced order zone model with heating and cooling inputs"
      extends R4C4;
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preHeat
        annotation (Placement(transformation(extent={{8,-90},{28,-70}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preCool
        annotation (Placement(transformation(extent={{8,-108},{28,-88}})));
      Modelica.Blocks.Interfaces.RealInput qHeat
        annotation (Placement(transformation(extent={{-140,-100},{-100,-60}})));
      Modelica.Blocks.Interfaces.RealInput qCool
        annotation (Placement(transformation(extent={{-140,-120},{-100,-80}})));
    equation
      connect(qHeat, preHeat.Q_flow)
        annotation (Line(points={{-120,-80},{8,-80}}, color={0,0,127}));
      connect(qCool, preCool.Q_flow) annotation (Line(points={{-120,-100},{-56,
              -100},{-56,-98},{8,-98}}, color={0,0,127}));
      connect(preHeat.port, air.port) annotation (Line(points={{28,-80},{52,-80},
              {52,-20}}, color={191,0,0}));
      connect(preCool.port, air.port) annotation (Line(points={{28,-98},{52,-98},
              {52,-20}}, color={191,0,0}));
    end R4C4HeatCool;

    model R5C4 "Reduced order zone model with no heating and cooling inputs"
      parameter Modelica.SIunits.Area Aflo = 48 "Floor area of zone";
      parameter Modelica.SIunits.Area Awall = 48 + 2 * 2.7 * (6 + 8) "Wall and ceiling area";
      parameter Modelica.SIunits.Volume V = 48 * 2.7 "Zone volume";
      parameter Units.ThermalResistancePerArea R = 0.01 "Resistance of zone";
      parameter Units.ThermalResistancePerArea Ri = 0.01 "Resistance of internal thermal mass";
      parameter Units.ThermalResistancePerArea Re = 0.01 "Resistance of external thermal mass";
      parameter Units.ThermalResistancePerArea Rem = 0.01 "Resistance of external thermal mass (middle layer)";
      parameter Units.ThermalResistancePerArea Rinf = 0.01 "Resistance of infiltration";
      parameter Modelica.SIunits.HeatCapacity C = 1e5 "Capacitance of zone";
      parameter Units.HeatCapacityPerArea Ci = 1e5 "Capacitance of internal thermal mass";
      parameter Units.HeatCapacityPerArea Ce = 1e5 "Capacitance of external thermal mass";
      parameter Units.HeatCapacityPerArea Cem = 1e5 "Capacitance of external thermal mass (middle layer)";
      parameter Real shgc = 0.8 "Solar heat gain coefficient of window";
      parameter Real shgce = 0.8 "Solar heat gain coefficient of ext. walls";
      parameter Modelica.SIunits.Temperature T0_C = 20+273.15 "Initial temperature of C";
      parameter Modelica.SIunits.Temperature T0_Ci = 20+273.15 "Initial temperature of Ci";
      parameter Modelica.SIunits.Temperature T0_Ce = 20+273.15 "Initial temperature of Ce";
      parameter Modelica.SIunits.Temperature T0_Cem = 20+273.15 "Initial temperature of Cem";
      Modelica.Thermal.HeatTransfer.Sensors.TemperatureSensor thermostat
        annotation (Placement(transformation(extent={{64,-30},{84,-10}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor air(C=C, T(fixed=
              true, start=T0_C))
        annotation (Placement(transformation(extent={{42,-20},{62,0}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tRe(R=Re/Awall)
        annotation (Placement(transformation(extent={{-60,-48},{-44,-32}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature
        prescribedTemperature
        annotation (Placement(transformation(extent={{-88,-50},{-68,-30}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf2
        annotation (Placement(transformation(extent={{13.5,3.5},{26.5,16.5}})));
      Modelica.Blocks.Math.Gain gain(k=shgc)
        annotation (Placement(transformation(extent={{-15,53},{-1,67}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf1
        annotation (Placement(transformation(extent={{14,54},{26,66}})));
      Modelica.Blocks.Interfaces.RealOutput Tzone(unit="K")
        "Zone mean air drybulb temperature"
        annotation (Placement(transformation(extent={{100,-10},{120,10}}),
            iconTransformation(extent={{100,-10},{120,10}})));
      Modelica.Blocks.Interfaces.RealInput intRad
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,60},{-100,100}})));
      Modelica.Blocks.Interfaces.RealInput intCon
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,30},{-100,70}})));
      Modelica.Blocks.Interfaces.RealInput intLat
        "Connector of Real input signals 1"
        annotation (Placement(transformation(extent={{-140,0},{-100,40}})));
      Modelica.Blocks.Math.Gain gain1(k=Aflo)
        annotation (Placement(transformation(extent={{-77,73},{-63,87}})));
      Modelica.Blocks.Math.Gain gain2(k=Aflo)
        annotation (Placement(transformation(extent={{-77,43},{-63,57}})));
      Modelica.Blocks.Math.Gain gain3(k=Aflo)
        annotation (Placement(transformation(extent={{-77,13},{-63,27}})));
      Modelica.Blocks.Interfaces.RealInput weaTDryBul
        annotation (Placement(transformation(extent={{-140,-40},{-100,0}})));
      Modelica.Blocks.Interfaces.RealInput weaHGloHor
        annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor intMass(C=Ci*Aflo, T(fixed=
              true, start=T0_Ci))
        annotation (Placement(transformation(extent={{32,60},{52,80}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tRi(R=Ri/Aflo)
        annotation (Placement(transformation(
            extent={{-10,-10},{10,10}},
            rotation=0,
            origin={20,30})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tR(R=R/Awall)
        annotation (Placement(transformation(extent={{24,-48},{40,-32}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor extMass(C=Ce*Awall, T(fixed=
              true, start=T0_Ce))
        annotation (Placement(transformation(extent={{-44,-40},{-24,-20}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf3
        annotation (Placement(transformation(extent={{-16,24},{-4,36}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf4 annotation (
          Placement(transformation(
            extent={{-6,-6},{6,6}},
            rotation=-90,
            origin={18,-28})));
      Modelica.Blocks.Math.Gain gain4(k=Awall/(Aflo + Awall))
        annotation (Placement(transformation(extent={{-7,-7},{7,7}},
            rotation=0,
            origin={-2,-4})));
      Modelica.Blocks.Math.Gain gain5(k=Aflo/(Aflo + Awall))
        annotation (Placement(transformation(extent={{-7,-7},{7,7}},
            rotation=0,
            origin={-40,80})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tRem(R=Rem/Awall)
        annotation (Placement(transformation(extent={{-22,-48},{-6,-32}})));
      Modelica.Thermal.HeatTransfer.Components.HeatCapacitor extMass1(C=Cem*Awall, T(fixed=
              true, start=T0_Cem))
        annotation (Placement(transformation(extent={{-6,-40},{14,-20}})));
      Modelica.Thermal.HeatTransfer.Components.ThermalResistor tRinf(R=Rinf/Awall)
        annotation (Placement(transformation(extent={{-14,-70},{2,-54}})));
      Modelica.Blocks.Math.Gain gain6(k=shgce)
        annotation (Placement(transformation(extent={{-93,-75},{-79,-61}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow phf5
        annotation (Placement(transformation(extent={{-6,-6},{6,6}},
            rotation=90,
            origin={-34,-52})));
    equation

      connect(thermostat.T,Tzone)  annotation (Line(points={{84,-20},{90,-20},{90,0},
              {110,0}}, color={0,0,127}));
      connect(thermostat.port, air.port)
        annotation (Line(points={{64,-20},{52,-20}}, color={191,0,0}));
      connect(prescribedTemperature.port, tRe.port_a)
        annotation (Line(points={{-68,-40},{-60,-40}},           color={191,0,0}));
      connect(phf2.port, air.port) annotation (Line(points={{26.5,10},{26.5,10},{42,
              10},{42,-20},{52,-20}}, color={191,0,0}));
      connect(gain.y, phf1.Q_flow)
        annotation (Line(points={{-0.3,60},{-0.3,60},{14,60}},
                                                 color={0,0,127}));
      connect(intRad, gain1.u)
        annotation (Line(points={{-120,80},{-78.4,80}},         color={0,0,127}));
      connect(intCon, gain2.u)
        annotation (Line(points={{-120,50},{-78.4,50}},         color={0,0,127}));
      connect(intLat, gain3.u)
        annotation (Line(points={{-120,20},{-100,20},{-78.4,20}},
                                                               color={0,0,127}));
      connect(prescribedTemperature.T, weaTDryBul)
        annotation (Line(points={{-90,-40},{-94,-40},{-94,-20},{-120,-20}},
                                                        color={0,0,127}));
      connect(weaHGloHor, gain.u) annotation (Line(points={{-120,-40},{-98,-40},
              {-98,-54},{-24,-54},{-24,60},{-16.4,60}},
                                       color={0,0,127}));
      connect(phf1.port, intMass.port)
        annotation (Line(points={{26,60},{26,60},{42,60}},
                                                   color={191,0,0}));
      connect(intMass.port, tRi.port_a) annotation (Line(points={{42,60},{42,50},{2,
              50},{2,30},{10,30}}, color={191,0,0}));
      connect(tRi.port_b, air.port) annotation (Line(points={{30,30},{42,30},{42,-20},
              {52,-20}}, color={191,0,0}));
      connect(air.port, tR.port_b) annotation (Line(points={{52,-20},{42,-20},{42,-40},
              {40,-40}}, color={191,0,0}));
      connect(tRe.port_b, extMass.port)
        annotation (Line(points={{-44,-40},{-34,-40}}, color={191,0,0}));
      connect(gain2.y, phf2.Q_flow) annotation (Line(points={{-62.3,50},{-50,50},{-50,
              10},{13.5,10}},
                         color={0,0,127}));
      connect(phf3.port, tRi.port_a)
        annotation (Line(points={{-4,30},{-4,30},{10,30}}, color={191,0,0}));
      connect(phf4.Q_flow, gain4.y) annotation (Line(points={{18,-22},{18,-22},{18,-4},
              {5.7,-4}},         color={0,0,127}));
      connect(gain1.y, gain4.u) annotation (Line(points={{-62.3,80},{-56,80},{-56,60},
              {-40,60},{-40,-4},{-10.4,-4}},
                                   color={0,0,127}));
      connect(gain1.y, gain5.u)
        annotation (Line(points={{-62.3,80},{-48.4,80}}, color={0,0,127}));
      connect(gain5.y, phf3.Q_flow) annotation (Line(points={{-32.3,80},{-28,80},{-28,
              30},{-16,30}}, color={0,0,127}));
      connect(extMass.port, tRem.port_a)
        annotation (Line(points={{-34,-40},{-34,-40},{-22,-40}}, color={191,0,0}));
      connect(tRem.port_b, extMass1.port)
        annotation (Line(points={{-6,-40},{4,-40}}, color={191,0,0}));
      connect(tR.port_a, extMass1.port)
        annotation (Line(points={{24,-40},{24,-40},{4,-40}},  color={191,0,0}));
      connect(extMass1.port, phf4.port)
        annotation (Line(points={{4,-40},{18,-40},{18,-34}}, color={191,0,0}));
      connect(prescribedTemperature.port, tRinf.port_a) annotation (Line(points={{-68,-40},
              {-62,-40},{-62,-62},{-14,-62}},      color={191,0,0}));
      connect(tRinf.port_b, air.port) annotation (Line(points={{2,-62},{42,-62},{42,
              -20},{52,-20}}, color={191,0,0}));
      connect(weaHGloHor, gain6.u) annotation (Line(points={{-120,-40},{-98,-40},
              {-98,-68},{-94.4,-68}},
                                 color={0,0,127}));
      connect(gain6.y, phf5.Q_flow) annotation (Line(points={{-78.3,-68},{-34,
              -68},{-34,-58}},
                         color={0,0,127}));
      connect(phf5.port, extMass.port) annotation (Line(points={{-34,-46},{-34,
              -46},{-34,-40}}, color={191,0,0}));
      annotation (
    experiment(
          StopTime=3.1536e+07,
          Interval=3600,
          __Dymola_Algorithm="Radau"),
    __Dymola_Commands(file="modelica://Buildings/Resources/Scripts/Dymola/ThermalZones/Detailed/Validation/BESTEST/Case600FF.mos"
            "Simulate and plot"), Documentation(info="<html>
<p>
This model is used for the test case 600FF of the BESTEST validation suite.
Case 600FF is a light-weight building.
The room temperature is free floating.
</p>
</html>",     revisions="<html>
<ul>
<li>
October 29, 2016, by Michael Wetter:<br/>
Placed a capacity at the room-facing surface
to reduce the dimension of the nonlinear system of equations,
which generally decreases computing time.<br/>
Removed the pressure drop element which is not needed.<br/>
Linearized the radiative heat transfer, which is the default in
the library, and avoids a large nonlinear system of equations.<br/>
This is for
<a href=\"https://github.com/lbl-srg/modelica-buildings/issues/565\">issue 565</a>.
</li>
<li>
December 22, 2014 by Michael Wetter:<br/>
Removed <code>Modelica.Fluid.System</code>
to address issue
<a href=\"https://github.com/lbl-srg/modelica-buildings/issues/311\">#311</a>.
</li>
<li>
October 9, 2013, by Michael Wetter:<br/>
Implemented soil properties using a record so that <code>TSol</code> and
<code>TLiq</code> are assigned.
This avoids an error when the model is checked in the pedantic mode.
</li>
<li>
July 15, 2012, by Michael Wetter:<br/>
Added reference results.
Changed implementation to make this model the base class
for all BESTEST cases.
Added computation of hourly and annual averaged room air temperature.
<li>
October 6, 2011, by Michael Wetter:<br/>
First implementation.
</li>
</ul>
</html>"),
        Icon(graphics={
            Rectangle(
              extent={{-92,92},{92,-92}},
              pattern=LinePattern.None,
              lineColor={117,148,176},
              fillColor={170,213,255},
              fillPattern=FillPattern.Sphere),
            Rectangle(
              extent={{-100,-100},{100,100}},
              lineColor={95,95,95},
              fillColor={95,95,95},
              fillPattern=FillPattern.Solid),
            Rectangle(
              extent={{-92,92},{92,-92}},
              pattern=LinePattern.None,
              lineColor={117,148,176},
              fillColor={170,213,255},
              fillPattern=FillPattern.Sphere),
            Rectangle(
              extent={{-44,42},{54,-46}},
              lineColor={0,0,0},
              fillColor={135,135,135},
              fillPattern=FillPattern.Solid),
            Text(
              extent={{-150,144},{150,104}},
              textString="%name",
              lineColor={0,0,255})}),
        __Dymola_experimentSetupOutput(events=false));
    end R5C4;

    model R5C4HeatCool
      "Reduced order zone model with heating and cooling inputs"
      extends R5C4;
      Modelica.Blocks.Interfaces.RealInput qHeat
        annotation (Placement(transformation(extent={{-140,-100},{-100,-60}})));
      Modelica.Blocks.Interfaces.RealInput qCool
        annotation (Placement(transformation(extent={{-140,-120},{-100,-80}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preHeat
        annotation (Placement(transformation(extent={{8,-90},{28,-70}})));
      Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow preCool
        annotation (Placement(transformation(extent={{8,-108},{28,-88}})));
    equation
      connect(qHeat, preHeat.Q_flow)
        annotation (Line(points={{-120,-80},{8,-80}}, color={0,0,127}));
      connect(qCool, preCool.Q_flow) annotation (Line(points={{-120,-100},{-56,
              -100},{-56,-98},{8,-98}}, color={0,0,127}));
      connect(preHeat.port, air.port) annotation (Line(points={{28,-80},{52,-80},
              {52,-20}}, color={191,0,0}));
      connect(preCool.port, air.port) annotation (Line(points={{28,-98},{52,-98},
              {52,-20}}, color={191,0,0}));
    end R5C4HeatCool;

    package Examples
      extends Modelica.Icons.ExamplesPackage;
      model R1C1
        "Reduced order zone model with no HVAC system to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.FreeFloat;
        import TestModels;

        TestModels.MPC.R1C1 zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                18,80},{18,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                16,60},{16,2},{38,2}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {0,20},{0,-2},{38,-2}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {-8,0},{-8,-4},{38,-4}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {120,100}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R1C1;

      model R1C1SimpleHVAC_OpenLoop
        "Reduced order zone model with HVAC system and open loop contol to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.SimpleHVAC_OpenLoop;

        R1C1HeatCool zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
        Modelica.Blocks.Math.Product product
          annotation (Placement(transformation(extent={{24,-76},{34,-66}})));
        Modelica.Blocks.Math.Product product1
          annotation (Placement(transformation(extent={{24,-94},{34,-84}})));
        Modelica.Blocks.Math.MultiSum multiSum(nu=3, k={1,1,1})
          annotation (Placement(transformation(extent={{74,-86},{86,-74}})));
        Modelica.Blocks.Math.Gain uHeatGain(k=500)
          annotation (Placement(transformation(extent={{42,-74},{48,-68}})));
        Modelica.Blocks.Math.Gain uCoolGain(k=500)
          annotation (Placement(transformation(extent={{42,-92},{48,-86}})));
        Modelica.Blocks.Interfaces.RealOutput J(unit="W")
          "Total electrical power consumed by HVAC system" annotation (
            Placement(transformation(extent={{100,-90},{120,-70}}),
              iconTransformation(extent={{100,-10},{120,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                16,80},{16,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                12,60},{12,2},{38,2}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {0,20},{0,-2},{38,-2}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {-4,0},{-4,-4},{38,-4}}, color={0,0,127}));
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{-39,-44},
                {0,-44},{0,-8},{38,-8}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{-39,-54},
                {2,-54},{2,-10},{38,-10}}, color={0,0,127}));
        connect(product.y, uHeatGain.u) annotation (Line(points={{34.5,-71},{
                38.25,-71},{38.25,-71},{41.4,-71}}, color={0,0,127}));
        connect(product1.y, uCoolGain.u) annotation (Line(points={{34.5,-89},{
                38.25,-89},{38.25,-89},{41.4,-89}}, color={0,0,127}));
        connect(uHeatGain.y, multiSum.u[1]) annotation (Line(points={{48.3,-71},
                {52,-71},{52,-77.2},{74,-77.2}}, color={0,0,127}));
        connect(uCoolGain.y, multiSum.u[2]) annotation (Line(points={{48.3,-89},
                {52,-89},{52,-80},{74,-80}}, color={0,0,127}));
        connect(uHeat, product.u1) annotation (Line(points={{-120,-40},{-86,-40},
                {-86,-68},{23,-68}}, color={0,0,127}));
        connect(product.u2, product.u1) annotation (Line(points={{23,-74},{10,
                -74},{10,-68},{23,-68}}, color={0,0,127}));
        connect(uCool, product1.u1) annotation (Line(points={{-120,-60},{-90,
                -60},{-90,-86},{23,-86}}, color={0,0,127}));
        connect(product1.u2, product1.u1) annotation (Line(points={{23,-92},{10,
                -92},{10,-86},{23,-86}}, color={0,0,127}));
        connect(add.y, Phvac) annotation (Line(points={{61,-50},{80,-50},{80,
                -40},{110,-40}}, color={0,0,127}));
        connect(multiSum.u[3], Phvac) annotation (Line(points={{74,-82.8},{70,
                -82.8},{70,-50},{80,-50},{80,-40},{110,-40}}, color={0,0,127}));
        connect(multiSum.y, J)
          annotation (Line(points={{87.02,-80},{110,-80}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,120}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R1C1SimpleHVAC_OpenLoop;

      model R1C1SimpleHVAC_ClosedLoop
        "Reduced order zone model with HVAC system and closed loop contol to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.SimpleHVAC_ClosedLoop;

        R1C1HeatCool zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(zone.Tzone, controller.Tzone) annotation (Line(points={{61,0},{
                70,0},{70,-72},{-90,-72},{-90,-50},{-82,-50}}, color={0,0,127}));
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{-19,-44},
                {0,-44},{0,-8},{38,-8}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{-19,-54},
                {2,-54},{2,-10},{38,-10}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {0,0},{0,-4},{38,-4}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {2,20},{2,-2},{38,-2}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                16,60},{16,2},{38,2}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                18,80},{18,5},{38,5}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,120}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R1C1SimpleHVAC_ClosedLoop;

      model R2C2
        "Reduced order zone model with no HVAC system to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.FreeFloat;
        import TestModels;

        TestModels.MPC.R2C2 zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                18,80},{18,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                16,60},{16,2},{38,2}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {0,20},{0,-2},{38,-2}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {-8,0},{-8,-4},{38,-4}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {120,100}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R2C2;

      model R2C2SimpleHVAC_OpenLoop
        "Reduced order zone model with HVAC system and open loop contol to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.SimpleHVAC_OpenLoop;

        R2C2HeatCool zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
        Modelica.Blocks.Math.Product product
          annotation (Placement(transformation(extent={{24,-76},{34,-66}})));
        Modelica.Blocks.Math.Product product1
          annotation (Placement(transformation(extent={{24,-94},{34,-84}})));
        Modelica.Blocks.Math.MultiSum multiSum(nu=3, k={1,1,1})
          annotation (Placement(transformation(extent={{74,-86},{86,-74}})));
        Modelica.Blocks.Math.Gain uHeatGain
          annotation (Placement(transformation(extent={{42,-74},{48,-68}})));
        Modelica.Blocks.Math.Gain uCoolGain
          annotation (Placement(transformation(extent={{42,-92},{48,-86}})));
        Modelica.Blocks.Interfaces.RealOutput J(unit="W")
          "Total electrical power consumed by HVAC system" annotation (
            Placement(transformation(extent={{100,-90},{120,-70}}),
              iconTransformation(extent={{100,-10},{120,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                16,80},{16,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                12,60},{12,2},{38,2}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {0,20},{0,-2},{38,-2}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {-4,0},{-4,-4},{38,-4}}, color={0,0,127}));
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{-39,-44},
                {0,-44},{0,-8},{38,-8}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{-39,-54},
                {2,-54},{2,-10},{38,-10}}, color={0,0,127}));
        connect(product.y, uHeatGain.u) annotation (Line(points={{34.5,-71},{
                38.25,-71},{38.25,-71},{41.4,-71}}, color={0,0,127}));
        connect(product1.y, uCoolGain.u) annotation (Line(points={{34.5,-89},{
                38.25,-89},{38.25,-89},{41.4,-89}}, color={0,0,127}));
        connect(uHeatGain.y, multiSum.u[1]) annotation (Line(points={{48.3,-71},
                {52,-71},{52,-77.2},{74,-77.2}}, color={0,0,127}));
        connect(uCoolGain.y, multiSum.u[2]) annotation (Line(points={{48.3,-89},
                {52,-89},{52,-80},{74,-80}}, color={0,0,127}));
        connect(uHeat, product.u1) annotation (Line(points={{-120,-40},{-86,-40},
                {-86,-68},{23,-68}}, color={0,0,127}));
        connect(product.u2, product.u1) annotation (Line(points={{23,-74},{10,
                -74},{10,-68},{23,-68}}, color={0,0,127}));
        connect(uCool, product1.u1) annotation (Line(points={{-120,-60},{-90,
                -60},{-90,-86},{23,-86}}, color={0,0,127}));
        connect(product1.u2, product1.u1) annotation (Line(points={{23,-92},{10,
                -92},{10,-86},{23,-86}}, color={0,0,127}));
        connect(multiSum.y, J)
          annotation (Line(points={{87.02,-80},{110,-80}}, color={0,0,127}));
        connect(add.y, multiSum.u[3]) annotation (Line(points={{61,-50},{66,-50},
                {66,-82.8},{74,-82.8}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,120}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R2C2SimpleHVAC_OpenLoop;

      model R2C2SimpleHVAC_ClosedLoop
        "Reduced order zone model with HVAC system and closed loop contol to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.SimpleHVAC_ClosedLoop;

        R2C2HeatCool zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(zone.Tzone, controller.Tzone) annotation (Line(points={{61,0},{
                70,0},{70,-72},{-90,-72},{-90,-50},{-82,-50}}, color={0,0,127}));
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{-19,-44},
                {0,-44},{0,-8},{38,-8}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{-19,-54},
                {2,-54},{2,-10},{38,-10}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {0,0},{0,-4},{38,-4}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {2,20},{2,-2},{38,-2}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                16,60},{16,2},{38,2}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                18,80},{18,5},{38,5}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,120}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R2C2SimpleHVAC_ClosedLoop;

      model R3C3
        "Reduced order zone model with no HVAC system to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.FreeFloat;
        import TestModels;

        TestModels.MPC.R3C3 zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                18,80},{18,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                16,60},{16,2},{38,2}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {0,20},{0,-2},{38,-2}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {-8,0},{-8,-4},{38,-4}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {120,100}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R3C3;

      model R3C3SimpleHVAC_OpenLoop
        "Reduced order zone model with HVAC system and open loop contol to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.SimpleHVAC_OpenLoop;

        R3C3HeatCool zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
        Modelica.Blocks.Math.Product product
          annotation (Placement(transformation(extent={{24,-76},{34,-66}})));
        Modelica.Blocks.Math.Product product1
          annotation (Placement(transformation(extent={{24,-94},{34,-84}})));
        Modelica.Blocks.Math.MultiSum multiSum(nu=3, k={1,1,1})
          annotation (Placement(transformation(extent={{74,-86},{86,-74}})));
        Modelica.Blocks.Math.Gain uHeatGain(k=500)
          annotation (Placement(transformation(extent={{42,-74},{48,-68}})));
        Modelica.Blocks.Math.Gain uCoolGain(k=500)
          annotation (Placement(transformation(extent={{42,-92},{48,-86}})));
        Modelica.Blocks.Interfaces.RealOutput J(unit="W")
          "Total electrical power consumed by HVAC system" annotation (
            Placement(transformation(extent={{100,-90},{120,-70}}),
              iconTransformation(extent={{100,-10},{120,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                16,80},{16,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                12,60},{12,2},{38,2}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {0,20},{0,-2},{38,-2}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {-4,0},{-4,-4},{38,-4}}, color={0,0,127}));
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{-39,-44},
                {0,-44},{0,-8},{38,-8}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{-39,-54},
                {2,-54},{2,-10},{38,-10}}, color={0,0,127}));
        connect(product.y, uHeatGain.u) annotation (Line(points={{34.5,-71},{
                38.25,-71},{38.25,-71},{41.4,-71}}, color={0,0,127}));
        connect(product1.y, uCoolGain.u) annotation (Line(points={{34.5,-89},{
                38.25,-89},{38.25,-89},{41.4,-89}}, color={0,0,127}));
        connect(uHeatGain.y, multiSum.u[1]) annotation (Line(points={{48.3,-71},
                {52,-71},{52,-77.2},{74,-77.2}}, color={0,0,127}));
        connect(uCoolGain.y, multiSum.u[2]) annotation (Line(points={{48.3,-89},
                {52,-89},{52,-80},{74,-80}}, color={0,0,127}));
        connect(uHeat, product.u1) annotation (Line(points={{-120,-40},{-86,-40},
                {-86,-68},{23,-68}}, color={0,0,127}));
        connect(product.u2, product.u1) annotation (Line(points={{23,-74},{10,
                -74},{10,-68},{23,-68}}, color={0,0,127}));
        connect(uCool, product1.u1) annotation (Line(points={{-120,-60},{-90,
                -60},{-90,-86},{23,-86}}, color={0,0,127}));
        connect(product1.u2, product1.u1) annotation (Line(points={{23,-92},{10,
                -92},{10,-86},{23,-86}}, color={0,0,127}));
        connect(multiSum.y, J)
          annotation (Line(points={{87.02,-80},{110,-80}}, color={0,0,127}));
        connect(add.y, multiSum.u[3]) annotation (Line(points={{61,-50},{66,-50},
                {66,-82.8},{74,-82.8}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,120}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R3C3SimpleHVAC_OpenLoop;

      model R3C3SimpleHVAC_ClosedLoop
        "Reduced order zone model with HVAC system and closed loop contol to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.SimpleHVAC_ClosedLoop;

        R3C3HeatCool zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(zone.Tzone, controller.Tzone) annotation (Line(points={{61,0},{
                70,0},{70,-72},{-90,-72},{-90,-50},{-82,-50}}, color={0,0,127}));
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{-19,-44},
                {0,-44},{0,-8},{38,-8}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{-19,-54},
                {2,-54},{2,-10},{38,-10}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {0,0},{0,-4},{38,-4}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {2,20},{2,-2},{38,-2}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                16,60},{16,2},{38,2}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                18,80},{18,5},{38,5}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,120}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R3C3SimpleHVAC_ClosedLoop;

      model R4C3
        "Reduced order zone model with no HVAC system to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.FreeFloat;
        import TestModels;

        TestModels.MPC.R4C3 zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                18,80},{18,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                16,60},{16,2},{38,2}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {0,20},{0,-2},{38,-2}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {-8,0},{-8,-4},{38,-4}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {120,100}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R4C3;

      model R4C3SimpleHVAC_OpenLoop
        "Reduced order zone model with HVAC system and open loop contol to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.SimpleHVAC_OpenLoop;

        R4C3HeatCool zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
        Modelica.Blocks.Math.Product product
          annotation (Placement(transformation(extent={{24,-76},{34,-66}})));
        Modelica.Blocks.Math.Product product1
          annotation (Placement(transformation(extent={{24,-94},{34,-84}})));
        Modelica.Blocks.Math.MultiSum multiSum(nu=3, k={1,1,1})
          annotation (Placement(transformation(extent={{74,-86},{86,-74}})));
        Modelica.Blocks.Math.Gain uHeatGain
          annotation (Placement(transformation(extent={{42,-74},{48,-68}})));
        Modelica.Blocks.Math.Gain uCoolGain
          annotation (Placement(transformation(extent={{42,-92},{48,-86}})));
        Modelica.Blocks.Interfaces.RealOutput J(unit="W")
          "Total electrical power consumed by HVAC system" annotation (
            Placement(transformation(extent={{100,-90},{120,-70}}),
              iconTransformation(extent={{100,-10},{120,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                16,80},{16,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                12,60},{12,2},{38,2}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {0,20},{0,-2},{38,-2}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {-4,0},{-4,-4},{38,-4}}, color={0,0,127}));
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{-39,-44},
                {0,-44},{0,-8},{38,-8}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{-39,-54},
                {2,-54},{2,-10},{38,-10}}, color={0,0,127}));
        connect(product.y, uHeatGain.u) annotation (Line(points={{34.5,-71},{
                38.25,-71},{38.25,-71},{41.4,-71}}, color={0,0,127}));
        connect(product1.y, uCoolGain.u) annotation (Line(points={{34.5,-89},{
                38.25,-89},{38.25,-89},{41.4,-89}}, color={0,0,127}));
        connect(uHeatGain.y, multiSum.u[1]) annotation (Line(points={{48.3,-71},
                {52,-71},{52,-77.2},{74,-77.2}}, color={0,0,127}));
        connect(uCoolGain.y, multiSum.u[2]) annotation (Line(points={{48.3,-89},
                {52,-89},{52,-80},{74,-80}}, color={0,0,127}));
        connect(uHeat, product.u1) annotation (Line(points={{-120,-40},{-86,-40},
                {-86,-68},{23,-68}}, color={0,0,127}));
        connect(product.u2, product.u1) annotation (Line(points={{23,-74},{10,
                -74},{10,-68},{23,-68}}, color={0,0,127}));
        connect(uCool, product1.u1) annotation (Line(points={{-120,-60},{-90,
                -60},{-90,-86},{23,-86}}, color={0,0,127}));
        connect(product1.u2, product1.u1) annotation (Line(points={{23,-92},{10,
                -92},{10,-86},{23,-86}}, color={0,0,127}));
        connect(multiSum.y, J)
          annotation (Line(points={{87.02,-80},{110,-80}}, color={0,0,127}));
        connect(add.y, multiSum.u[3]) annotation (Line(points={{61,-50},{66,-50},
                {66,-82.8},{74,-82.8}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,120}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R4C3SimpleHVAC_OpenLoop;

      model R4C3SimpleHVAC_ClosedLoop
        "Reduced order zone model with HVAC system and closed loop contol to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.SimpleHVAC_ClosedLoop;

        R4C3HeatCool zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(zone.Tzone, controller.Tzone) annotation (Line(points={{61,0},{
                70,0},{70,-72},{-90,-72},{-90,-50},{-82,-50}}, color={0,0,127}));
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{-19,-44},
                {0,-44},{0,-8},{38,-8}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{-19,-54},
                {2,-54},{2,-10},{38,-10}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {0,0},{0,-4},{38,-4}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {2,20},{2,-2},{38,-2}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                16,60},{16,2},{38,2}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                18,80},{18,5},{38,5}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,120}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R4C3SimpleHVAC_ClosedLoop;

      model R4C4
        "Reduced order zone model with no HVAC system to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.FreeFloat;
        import TestModels;

        TestModels.MPC.R4C4 zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                18,80},{18,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                16,60},{16,2},{38,2}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {0,20},{0,-2},{38,-2}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {-8,0},{-8,-4},{38,-4}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {120,100}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R4C4;

      model R4C4SimpleHVAC_OpenLoop
        "Reduced order zone model with HVAC system and open loop contol to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.SimpleHVAC_OpenLoop;

        R4C4HeatCool zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
        Modelica.Blocks.Math.Product product
          annotation (Placement(transformation(extent={{24,-76},{34,-66}})));
        Modelica.Blocks.Math.Product product1
          annotation (Placement(transformation(extent={{24,-94},{34,-84}})));
        Modelica.Blocks.Math.MultiSum multiSum(nu=3, k={1,1,1})
          annotation (Placement(transformation(extent={{74,-86},{86,-74}})));
        Modelica.Blocks.Math.Gain uHeatGain
          annotation (Placement(transformation(extent={{42,-74},{48,-68}})));
        Modelica.Blocks.Math.Gain uCoolGain
          annotation (Placement(transformation(extent={{42,-92},{48,-86}})));
        Modelica.Blocks.Interfaces.RealOutput J(unit="W")
          "Total electrical power consumed by HVAC system" annotation (
            Placement(transformation(extent={{100,-90},{120,-70}}),
              iconTransformation(extent={{100,-10},{120,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                16,80},{16,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                12,60},{12,2},{38,2}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {0,20},{0,-2},{38,-2}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {-4,0},{-4,-4},{38,-4}}, color={0,0,127}));
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{-39,-44},
                {0,-44},{0,-8},{38,-8}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{-39,-54},
                {2,-54},{2,-10},{38,-10}}, color={0,0,127}));
        connect(product.y, uHeatGain.u) annotation (Line(points={{34.5,-71},{
                38.25,-71},{38.25,-71},{41.4,-71}}, color={0,0,127}));
        connect(product1.y, uCoolGain.u) annotation (Line(points={{34.5,-89},{
                38.25,-89},{38.25,-89},{41.4,-89}}, color={0,0,127}));
        connect(uHeatGain.y, multiSum.u[1]) annotation (Line(points={{48.3,-71},
                {52,-71},{52,-77.2},{74,-77.2}}, color={0,0,127}));
        connect(uCoolGain.y, multiSum.u[2]) annotation (Line(points={{48.3,-89},
                {52,-89},{52,-80},{74,-80}}, color={0,0,127}));
        connect(uHeat, product.u1) annotation (Line(points={{-120,-40},{-86,-40},
                {-86,-68},{23,-68}}, color={0,0,127}));
        connect(product.u2, product.u1) annotation (Line(points={{23,-74},{10,
                -74},{10,-68},{23,-68}}, color={0,0,127}));
        connect(uCool, product1.u1) annotation (Line(points={{-120,-60},{-90,
                -60},{-90,-86},{23,-86}}, color={0,0,127}));
        connect(product1.u2, product1.u1) annotation (Line(points={{23,-92},{10,
                -92},{10,-86},{23,-86}}, color={0,0,127}));
        connect(multiSum.y, J)
          annotation (Line(points={{87.02,-80},{110,-80}}, color={0,0,127}));
        connect(add.y, multiSum.u[3]) annotation (Line(points={{61,-50},{66,-50},
                {66,-82.8},{74,-82.8}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,120}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R4C4SimpleHVAC_OpenLoop;

      model R4C4SimpleHVAC_ClosedLoop
        "Reduced order zone model with HVAC system and closed loop contol to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.SimpleHVAC_ClosedLoop;

        R4C4HeatCool zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(zone.Tzone, controller.Tzone) annotation (Line(points={{61,0},{
                70,0},{70,-72},{-90,-72},{-90,-50},{-82,-50}}, color={0,0,127}));
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{-19,-44},
                {0,-44},{0,-8},{38,-8}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{-19,-54},
                {2,-54},{2,-10},{38,-10}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {0,0},{0,-4},{38,-4}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {2,20},{2,-2},{38,-2}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                16,60},{16,2},{38,2}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                18,80},{18,5},{38,5}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,120}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R4C4SimpleHVAC_ClosedLoop;

      model R5C4
        "Reduced order zone model with no HVAC system to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.FreeFloat;
        import TestModels;

        TestModels.MPC.R5C4 zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                18,80},{18,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                16,60},{16,2},{38,2}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {0,20},{0,-2},{38,-2}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {-8,0},{-8,-4},{38,-4}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {120,100}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R5C4;

      model R5C4SimpleHVAC_OpenLoop
        "Reduced order zone model with HVAC system and open loop contol to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.SimpleHVAC_OpenLoop;

        R5C4HeatCool zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
        Modelica.Blocks.Math.Product product
          annotation (Placement(transformation(extent={{24,-76},{34,-66}})));
        Modelica.Blocks.Math.Product product1
          annotation (Placement(transformation(extent={{24,-94},{34,-84}})));
        Modelica.Blocks.Math.MultiSum multiSum(nu=3, k={1,1,1})
          annotation (Placement(transformation(extent={{74,-86},{86,-74}})));
        Modelica.Blocks.Math.Gain uHeatGain(k=500)
          annotation (Placement(transformation(extent={{42,-74},{48,-68}})));
        Modelica.Blocks.Math.Gain uCoolGain(k=500)
          annotation (Placement(transformation(extent={{42,-92},{48,-86}})));
        Modelica.Blocks.Interfaces.RealOutput J(unit="W")
          "Total electrical power consumed by HVAC system" annotation (
            Placement(transformation(extent={{100,-90},{120,-70}}),
              iconTransformation(extent={{100,-10},{120,10}})));
      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                16,80},{16,5},{38,5}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                12,60},{12,2},{38,2}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {0,20},{0,-2},{38,-2}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {-4,0},{-4,-4},{38,-4}}, color={0,0,127}));
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{-39,-44},
                {0,-44},{0,-8},{38,-8}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{-39,-54},
                {2,-54},{2,-10},{38,-10}}, color={0,0,127}));
        connect(product.y, uHeatGain.u) annotation (Line(points={{34.5,-71},{
                38.25,-71},{38.25,-71},{41.4,-71}}, color={0,0,127}));
        connect(product1.y, uCoolGain.u) annotation (Line(points={{34.5,-89},{
                38.25,-89},{38.25,-89},{41.4,-89}}, color={0,0,127}));
        connect(uHeatGain.y, multiSum.u[1]) annotation (Line(points={{48.3,-71},
                {52,-71},{52,-77.2},{74,-77.2}}, color={0,0,127}));
        connect(uCoolGain.y, multiSum.u[2]) annotation (Line(points={{48.3,-89},
                {52,-89},{52,-80},{74,-80}}, color={0,0,127}));
        connect(uHeat, product.u1) annotation (Line(points={{-120,-40},{-86,-40},
                {-86,-68},{23,-68}}, color={0,0,127}));
        connect(product.u2, product.u1) annotation (Line(points={{23,-74},{10,
                -74},{10,-68},{23,-68}}, color={0,0,127}));
        connect(uCool, product1.u1) annotation (Line(points={{-120,-60},{-90,
                -60},{-90,-86},{23,-86}}, color={0,0,127}));
        connect(product1.u2, product1.u1) annotation (Line(points={{23,-92},{10,
                -92},{10,-86},{23,-86}}, color={0,0,127}));
        connect(multiSum.y, J)
          annotation (Line(points={{87.02,-80},{110,-80}}, color={0,0,127}));
        connect(add.y, multiSum.u[3]) annotation (Line(points={{61,-50},{66,-50},
                {66,-82.8},{74,-82.8}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,120}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R5C4SimpleHVAC_OpenLoop;

      model R5C4SimpleHVAC_ClosedLoop
        "Reduced order zone model with HVAC system and closed loop contol to be used with MPCPy"
        extends Icons.MPCPy;
        extends BaseClasses.SimpleHVAC_ClosedLoop;
        R5C4HeatCool zone
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));

      equation
        connect(zone.Tzone, Tzone)
          annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(zone.Tzone, controller.Tzone) annotation (Line(points={{61,0},{
                70,0},{70,-72},{-90,-72},{-90,-50},{-82,-50}}, color={0,0,127}));
        connect(equipment.qHeat, zone.qHeat) annotation (Line(points={{-19,-44},
                {0,-44},{0,-8},{38,-8}}, color={0,0,127}));
        connect(equipment.qCool, zone.qCool) annotation (Line(points={{-19,-54},
                {2,-54},{2,-10},{38,-10}}, color={0,0,127}));
        connect(weaHGloHor, zone.weaHGloHor) annotation (Line(points={{-120,0},
                {0,0},{0,-4},{38,-4}}, color={0,0,127}));
        connect(weaTDryBul, zone.weaTDryBul) annotation (Line(points={{-120,20},
                {2,20},{2,-2},{38,-2}}, color={0,0,127}));
        connect(intLat_zone, zone.intLat) annotation (Line(points={{-120,60},{
                16,60},{16,2},{38,2}}, color={0,0,127}));
        connect(intCon_zone, zone.intCon) annotation (Line(points={{-120,80},{
                18,80},{18,5},{38,5}}, color={0,0,127}));
        connect(intRad_zone, zone.intRad) annotation (Line(points={{-120,100},{
                20,100},{20,8},{38,8}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,-100},
                  {100,120}})), Diagram(coordinateSystem(preserveAspectRatio=
                false, extent={{-100,-100},{100,100}})));
      end R5C4SimpleHVAC_ClosedLoop;

      package BaseClasses
        extends Modelica.Icons.BasesPackage;
        model FreeFloat
          import TestModels;
          Modelica.Blocks.Interfaces.RealInput weaTDryBul
          "Input dry bulb temperature"
          annotation (Placement(transformation(extent={{-140,0},{-100,40}})));
          Modelica.Blocks.Interfaces.RealInput weaHGloHor
          "Input direct normal radiation"
          annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
          Modelica.Blocks.Interfaces.RealInput intRad_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,80},{-100,120}})));
          Modelica.Blocks.Interfaces.RealInput intCon_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,60},{-100,100}})));
          Modelica.Blocks.Interfaces.RealInput intLat_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,40},{-100,80}})));
          Modelica.Blocks.Interfaces.RealOutput Tzone(unit="K")
            "Zone mean air drybulb temperature"
            annotation (Placement(transformation(extent={{100,-10},{120,10}})));
          annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
                coordinateSystem(preserveAspectRatio=false)));
        end FreeFloat;

        partial model SimpleHVAC_OpenLoop
          HVAC.Equipment.SimpleHeaterCooler equipment
            annotation (Placement(transformation(extent={{-60,-60},{-40,-40}})));
          Modelica.Blocks.Math.Add add
            annotation (Placement(transformation(extent={{40,-60},{60,-40}})));
          Modelica.Blocks.Interfaces.RealInput weaTDryBul
          "Input dry bulb temperature"
          annotation (Placement(transformation(extent={{-140,0},{-100,40}})));
          Modelica.Blocks.Interfaces.RealInput weaHGloHor
          "Input direct normal radiation"
          annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
          Modelica.Blocks.Interfaces.RealInput intRad_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,80},{-100,120}})));
          Modelica.Blocks.Interfaces.RealInput intCon_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,60},{-100,100}})));
          Modelica.Blocks.Interfaces.RealInput intLat_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,40},{-100,80}})));
          Modelica.Blocks.Interfaces.RealOutput Tzone(unit="K")
            "Zone mean air drybulb temperature"
            annotation (Placement(transformation(extent={{100,-10},{120,10}})));
          Modelica.Blocks.Interfaces.RealInput uHeat "Heating signal input"
            annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
          Modelica.Blocks.Interfaces.RealInput uCool "Cooling signal input"
            annotation (Placement(transformation(extent={{-140,-80},{-100,-40}})));
          Modelica.Blocks.Interfaces.RealOutput Phvac(unit="W")
            "Total electrical power consumed by HVAC system" annotation (
              Placement(transformation(extent={{100,-50},{120,-30}}),
                iconTransformation(extent={{100,-10},{120,10}})));
        equation
          connect(equipment.uHeat,uHeat)  annotation (Line(points={{-62,-42},{-80,-42},{
                  -80,-40},{-120,-40}}, color={0,0,127}));
          connect(equipment.uCool,uCool)  annotation (Line(points={{-62,-58},{-80,-58},{
                  -80,-60},{-120,-60}}, color={0,0,127}));
          connect(equipment.PHeat,add. u1) annotation (Line(points={{-39,-48},{20,
                  -48},{20,-44},{38,-44}}, color={0,0,127}));
          connect(equipment.PCool,add. u2) annotation (Line(points={{-39,-58},{20,
                  -58},{20,-56},{38,-56}}, color={0,0,127}));
          connect(add.y,Phvac)  annotation (Line(points={{61,-50},{80,-50},{80,
                  -40},{110,-40}}, color={0,0,127}));
          annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
                coordinateSystem(preserveAspectRatio=false)));
        end SimpleHVAC_OpenLoop;

        partial model SimpleHVAC_ClosedLoop
          Modelica.Blocks.Interfaces.RealInput weaTDryBul
          "Input dry bulb temperature"
          annotation (Placement(transformation(extent={{-140,0},{-100,40}})));
          Modelica.Blocks.Interfaces.RealInput weaHGloHor
          "Input direct normal radiation"
          annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
          Modelica.Blocks.Interfaces.RealInput intRad_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,80},{-100,120}})));
          Modelica.Blocks.Interfaces.RealInput intCon_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,60},{-100,100}})));
          Modelica.Blocks.Interfaces.RealInput intLat_zone
            "Connector of Real input signals 1"
            annotation (Placement(transformation(extent={{-140,40},{-100,80}})));
          Modelica.Blocks.Interfaces.RealOutput Tzone(unit="K")
            "Zone mean air drybulb temperature"
            annotation (Placement(transformation(extent={{100,-10},{120,10}})));
          HVAC.Equipment.SimpleHeaterCooler equipment
            annotation (Placement(transformation(extent={{-40,-60},{-20,-40}})));
          Modelica.Blocks.Math.Add add
            annotation (Placement(transformation(extent={{40,-60},{60,-40}})));
          Modelica.Blocks.Interfaces.RealOutput Phvac(unit="W")
            "Total electrical power consumed by HVAC system" annotation (
              Placement(transformation(extent={{100,-50},{120,-30}}),
                iconTransformation(extent={{100,-10},{120,10}})));
          HVAC.Controllers.DualSetpoint            controller
            annotation (Placement(transformation(extent={{-80,-60},{-60,-40}})));
          Modelica.Blocks.Interfaces.RealInput coolSet annotation (Placement(
                transformation(extent={{-140,-60},{-100,-20}})));
          Modelica.Blocks.Interfaces.RealInput heatSet annotation (Placement(
                transformation(extent={{-140,-100},{-100,-60}})));
        equation
          connect(equipment.PHeat,add. u1) annotation (Line(points={{-19,-48},{20,
                  -48},{20,-44},{38,-44}}, color={0,0,127}));
          connect(equipment.PCool,add. u2) annotation (Line(points={{-19,-58},{20,
                  -58},{20,-56},{38,-56}}, color={0,0,127}));
          connect(add.y,Phvac)  annotation (Line(points={{61,-50},{80,-50},{80,
                  -40},{110,-40}}, color={0,0,127}));
          connect(controller.yHeat,equipment. uHeat)
            annotation (Line(points={{-59,-42},{-42,-42}}, color={0,0,127}));
          connect(controller.yCool,equipment. uCool) annotation (Line(points={{
                  -59,-46},{-50,-46},{-50,-58},{-42,-58}}, color={0,0,127}));
          connect(controller.CoolSet,coolSet)  annotation (Line(points={{-82,-44},
                  {-96,-44},{-96,-40},{-120,-40}}, color={0,0,127}));
          connect(controller.HeatSet,heatSet)  annotation (Line(points={{-82,-56},
                  {-96,-56},{-96,-80},{-120,-80}}, color={0,0,127}));
          annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
                coordinateSystem(preserveAspectRatio=false)));
        end SimpleHVAC_ClosedLoop;
      end BaseClasses;
    end Examples;
  end MPC;

  package HVAC "Package containing detailed component models for HVAC"
    package Equipment
      model SimpleHeaterCooler
        "A simple heater and cooler with constant efficiency and COP"
        parameter Modelica.SIunits.Power heatingCap = 10000 "Capacity of heater";
        parameter Modelica.SIunits.DimensionlessRatio heatingEff = 0.99 "Efficiency of heater";
        parameter Modelica.SIunits.Power coolingCap = 10000 "Capacity of cooler";
        parameter Modelica.SIunits.DimensionlessRatio coolingCOP = 3 "COP of cooler";
        Modelica.Blocks.Math.Gain heatingCapGain(k=heatingCap)
          annotation (Placement(transformation(extent={{-20,70},{0,90}})));
        Modelica.Blocks.Math.Gain coolingCapGain(k=coolingCap)
          annotation (Placement(transformation(extent={{-20,-90},{0,-70}})));
        Modelica.Blocks.Math.Gain heatingPowerGain(k=1/heatingEff)
          annotation (Placement(transformation(extent={{60,10},{80,30}})));
        Modelica.Blocks.Math.Gain coolingPowerGain(k=-1/coolingCOP)
          annotation (Placement(transformation(extent={{60,-90},{80,-70}})));
        Modelica.Blocks.Interfaces.RealOutput PCool(unit="W") "Cooling electrical power output"
          annotation (Placement(transformation(extent={{100,-90},{120,-70}})));
        Modelica.Blocks.Interfaces.RealOutput PHeat(unit="W") "Heating electrical power output"
          annotation (Placement(transformation(extent={{100,10},{120,30}}),
              iconTransformation(extent={{100,10},{120,30}})));
        Modelica.Blocks.Interfaces.RealInput uHeat "Heating signal input"
          annotation (Placement(transformation(extent={{-140,60},{-100,100}})));
        Modelica.Blocks.Interfaces.RealInput uCool "Cooling signal input"
          annotation (Placement(transformation(extent={{-140,-100},{-100,-60}}),
              iconTransformation(extent={{-140,-100},{-100,-60}})));
        Modelica.Blocks.Interfaces.RealOutput qHeat(unit="W") "Heating heatflow output"
          annotation (Placement(transformation(extent={{100,50},{120,70}})));
        Modelica.Blocks.Interfaces.RealOutput qCool(unit="W") "Cooling heatflow output"
          annotation (Placement(transformation(extent={{100,-50},{120,-30}}),
              iconTransformation(extent={{100,-50},{120,-30}})));
      equation
        connect(heatingCapGain.y, heatingPowerGain.u) annotation (Line(points={{1,80},{
                20,80},{20,20},{58,20}},                color={0,0,127}));
        connect(coolingCapGain.y, coolingPowerGain.u) annotation (Line(points={{1,-80},
                {58,-80}},                 color={0,0,127}));
        connect(coolingPowerGain.y, PCool)
          annotation (Line(points={{81,-80},{110,-80}}, color={0,0,127}));
        connect(heatingPowerGain.y, PHeat)
          annotation (Line(points={{81,20},{110,20}}, color={0,0,127}));
        connect(heatingCapGain.u, uHeat) annotation (Line(points={{-22,80},{-120,80}},
                                color={0,0,127}));
        connect(uCool, coolingCapGain.u) annotation (Line(points={{-120,-80},{-22,-80}},
                                     color={0,0,127}));
        connect(heatingCapGain.y, qHeat) annotation (Line(points={{1,80},{60,80},{60,60},
                {110,60}},         color={0,0,127}));
        connect(coolingPowerGain.u, qCool) annotation (Line(points={{58,-80},{20,-80},
                {20,-40},{110,-40}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={
                Rectangle(
                extent={{-100,100},{100,-100}},
                lineColor={0,0,0},
                fillColor={255,255,255},
                fillPattern=FillPattern.Solid),
              Rectangle(
                extent={{-100,100},{100,0}},
                lineColor={0,0,0},
                fillColor={238,46,47},
                fillPattern=FillPattern.Solid),
              Rectangle(
                extent={{-100,0},{100,-100}},
                lineColor={0,0,0},
                fillColor={28,108,200},
                fillPattern=FillPattern.Solid),
              Text(
                extent={{-150,140},{150,100}},
                textString="%name",
                lineColor={0,0,255})}),                                Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end SimpleHeaterCooler;
    end Equipment;

    package Controllers
      model DualSetpoint
        "A controller that outputs a heating and cooling signal according to respective setpoints with a deadband."
        Modelica.Blocks.Interfaces.RealInput Tzone
          annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
        Modelica.Blocks.Interfaces.RealInput CoolSet
          annotation (Placement(transformation(extent={{-140,40},{-100,80}})));
        Modelica.Blocks.Interfaces.RealInput HeatSet
          annotation (Placement(transformation(extent={{-140,-80},{-100,-40}}),
              iconTransformation(extent={{-140,-80},{-100,-40}})));
        Buildings.Controls.Continuous.LimPID conPID(controllerType=Modelica.Blocks.Types.SimpleController.P, k=2)
          annotation (Placement(transformation(extent={{-70,-70},{-50,-50}})));
        Buildings.Controls.Continuous.LimPID conPID1(
          controllerType=Modelica.Blocks.Types.SimpleController.P,
          yMax=0,
          yMin=-1,
          k=2)
          annotation (Placement(transformation(extent={{-90,50},{-70,70}})));
        Modelica.Blocks.Interfaces.RealOutput yHeat "Heating output signal"
          annotation (Placement(transformation(extent={{100,70},{120,90}})));
        Modelica.Blocks.Interfaces.RealOutput yCool "Cooling output signal"
          annotation (Placement(transformation(extent={{100,30},{120,50}})));
      equation
        connect(HeatSet, conPID.u_s) annotation (Line(points={{-120,-60},{-72,
                -60}},                   color={0,0,127}));
        connect(CoolSet, conPID1.u_s) annotation (Line(points={{-120,60},{-92,
                60}},                   color={0,0,127}));
        connect(Tzone, conPID1.u_m) annotation (Line(points={{-120,0},{-80,0},{
                -80,48}}, color={0,0,127}));
        connect(conPID.y, yHeat)
          annotation (Line(points={{-49,-60},{30,-60},{30,80},{110,80}},
                                                       color={0,0,127}));
        connect(conPID1.y, yCool) annotation (Line(points={{-69,60},{20,60},{20,
                40},{110,40}}, color={0,0,127}));
        connect(Tzone, conPID.u_m) annotation (Line(points={{-120,0},{-80,0},{
                -80,-80},{-60,-80},{-60,-72}},
                          color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={
              Rectangle(
                extent={{-100,98},{100,-100}},
                fillColor={255,255,255},
                fillPattern=FillPattern.Solid,
                lineColor={0,0,0}),
              Rectangle(
                extent={{60,100},{100,60}},
                fillColor={215,215,215},
                fillPattern=FillPattern.Solid,
                pattern=LinePattern.None),
              Rectangle(
                extent={{-100,100},{-60,60}},
                fillColor={215,215,215},
                fillPattern=FillPattern.Solid,
                pattern=LinePattern.None),
              Rectangle(
                extent={{-60,100},{60,60}},
                fillColor={215,215,215},
                fillPattern=FillPattern.Solid,
                pattern=LinePattern.None),
              Polygon(
                points={{-60,60},{60,60},{40,40},{-40,40},{-60,60}},
                fillColor={215,215,215},
                fillPattern=FillPattern.Solid,
                pattern=LinePattern.None),
              Line(
                points={{-100,60},{-60,60},{-40,40},{40,40},{60,60},{100,60}},
                color={0,0,0},
                pattern=LinePattern.Dash),
              Rectangle(
                extent={{-60,-60},{60,-100}},
                fillColor={215,215,215},
                fillPattern=FillPattern.Solid,
                pattern=LinePattern.None),
              Rectangle(
                extent={{-100,-60},{-60,-100}},
                fillColor={215,215,215},
                fillPattern=FillPattern.Solid,
                pattern=LinePattern.None),
              Rectangle(
                extent={{60,-60},{100,-100}},
                fillColor={215,215,215},
                fillPattern=FillPattern.Solid,
                pattern=LinePattern.None),
              Polygon(
                points={{-60,-60},{60,-60},{40,-40},{-40,-40},{-60,-60}},
                fillColor={215,215,215},
                fillPattern=FillPattern.Solid,
                pattern=LinePattern.None),
              Line(
                points={{-100,-60},{-60,-60},{-40,-40},{40,-40},{60,-60},{100,
                    -60}},
                color={0,0,0},
                pattern=LinePattern.Dash),
              Rectangle(extent={{-100,100},{100,-100}}, lineColor={0,0,0}),
              Text(
                extent={{-150,140},{150,100}},
                textString="%name",
                lineColor={0,0,255})}),           Diagram(coordinateSystem(
                preserveAspectRatio=false)));
      end DualSetpoint;
    end Controllers;
  end HVAC;

  package Components

    model SHGC_lin
      "
  Time-dependent solar heat gain coefficient modeled
  as a linear function of time of day (0-86400 s).
  "
      parameter Real a=1 "Parameter controlling the slope of shgc function";
      parameter Real b=0 "Parameter controlling the offset of shgc function";
      Modelica.Blocks.Interfaces.RealOutput shgc
        "Time-dependent solar heat gain coefficient"
        annotation (Placement(transformation(extent={{96,-10},{116,10}})));
      Modelica.Blocks.Interfaces.RealInput tday "Time of day in seconds"
        annotation (Placement(transformation(extent={{-128,-20},{-88,20}})));
      Modelica.Blocks.Sources.Constant A(k=a)
        annotation (Placement(transformation(extent={{-94,-30},{-74,-10}})));
      Modelica.Blocks.Sources.Constant B(k=b)
        annotation (Placement(transformation(extent={{-18,20},{2,40}})));
      Modelica.Blocks.Sources.Constant tend(k=86400)
        annotation (Placement(transformation(extent={{-94,-62},{-74,-42}})));
      Modelica.Blocks.Math.Division division
        annotation (Placement(transformation(extent={{-52,-36},{-32,-16}})));
      Modelica.Blocks.Math.Product product
        annotation (Placement(transformation(extent={{-18,-16},{2,4}})));
      Modelica.Blocks.Math.Add3 add3(k3=-1)
        annotation (Placement(transformation(extent={{58,-10},{78,10}})));
      Modelica.Blocks.Math.Min min
        annotation (Placement(transformation(extent={{16,-64},{36,-44}})));
      Modelica.Blocks.Sources.Constant Zero(k=0)
        annotation (Placement(transformation(extent={{-18,-46},{2,-26}})));
    equation

      connect(division.u2, tend.y) annotation (Line(points={{-54,-32},{-60,-32},{-60,
              -52},{-73,-52}}, color={0,0,127}));
      connect(A.y, division.u1)
        annotation (Line(points={{-73,-20},{-73,-20},{-54,-20}}, color={0,0,127}));
      connect(tday, product.u1)
        annotation (Line(points={{-108,0},{-20,0}}, color={0,0,127}));
      connect(division.y, product.u2) annotation (Line(points={{-31,-26},{-26,-26},{
              -26,-12},{-20,-12}}, color={0,0,127}));
      connect(Zero.y, min.u1) annotation (Line(points={{3,-36},{8,-36},{8,-48},{14,-48}},
            color={0,0,127}));
      connect(min.y, add3.u3) annotation (Line(points={{37,-54},{46,-54},{46,-8},
              {56,-8}}, color={0,0,127}));
      connect(B.y, add3.u1) annotation (Line(points={{3,30},{34,30},{34,8},{56,
              8}}, color={0,0,127}));
      connect(product.y, add3.u2) annotation (Line(points={{3,-6},{34,-6},{34,0},
              {56,0}}, color={0,0,127}));
      connect(add3.y, shgc)
        annotation (Line(points={{79,0},{90,0},{106,0}}, color={0,0,127}));
      connect(A.y, min.u2) annotation (Line(points={{-73,-20},{-66,-20},{-66,
              -60},{14,-60}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={
            Rectangle(extent={{-100,100},{100,-100}}, lineColor={28,108,200}),
            Line(
              points={{-100,-40},{-80,-20},{-60,-10},{-40,-6},{0,-4},{40,-6},{60,-10},
                  {80,-20},{100,-40}},
              color={28,108,200},
              pattern=LinePattern.Dash,
              thickness=0.5),
            Ellipse(
              extent={{-40,40},{40,-40}},
              lineColor={28,108,200},
              fillColor={255,255,0},
              fillPattern=FillPattern.Solid)}),                      Diagram(
            coordinateSystem(preserveAspectRatio=false)));
    end SHGC_lin;

    model test
      Modelica.Blocks.Sources.Clock clock
        annotation (Placement(transformation(extent={{-50,-12},{-30,8}})));
      SHGC_lin sHGC_lin
        annotation (Placement(transformation(extent={{-14,-12},{6,8}})));
    equation
      connect(clock.y, sHGC_lin.tday) annotation (Line(points={{-29,-2},{-22,-2},
              {-14.8,-2}}, color={0,0,127}));
      annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
            coordinateSystem(preserveAspectRatio=false)));
    end test;
  end Components;

  package Units
    extends Modelica.Icons.Package;
    type ThermalResistancePerArea = Real(unit="(m2.K)/W");
    type HeatCapacityPerArea = Real(unit="J/(m2.K)");
    annotation (Icon(graphics={
          Rectangle(
            extent={{-68,74},{-60,-44}},
            lineColor={64,64,64},
            fillColor={175,175,175},
            fillPattern=FillPattern.Solid),
          Polygon(
            points={{-60,-8},{-60,2},{-10,52},{-10,42},{-60,-8}},
            lineColor={64,64,64},
            fillColor={175,175,175},
            fillPattern=FillPattern.Solid),
          Polygon(
            points={{-40,12},{-34,18},{4,-44},{-4,-44},{-40,12}},
            lineColor={64,64,64},
            fillColor={175,175,175},
            fillPattern=FillPattern.Solid),
          Ellipse(
            extent={{18,32},{74,-42}},
            lineColor={64,64,64},
            fillColor={175,175,175},
            fillPattern=FillPattern.Solid),
          Polygon(
            points={{74,-2},{74,-50},{70,-64},{64,-72},{54,-76},{24,-76},{24,-68},
                {52,-68},{60,-64},{64,-58},{66,-50},{66,-30},{70,-24},{74,-10},{74,
                -2}},
            lineColor={64,64,64},
            smooth=Smooth.Bezier,
            fillColor={175,175,175},
            fillPattern=FillPattern.Solid),
          Ellipse(
            extent={{28,22},{64,-32}},
            lineColor={64,64,64},
            fillColor={255,255,255},
            fillPattern=FillPattern.Solid)}));
  end Units;

  package Icons
    extends Modelica.Icons.IconsPackage;
    model MPCPy
      annotation (Icon(coordinateSystem(preserveAspectRatio=false), graphics={
              Bitmap(extent={{-100,-88},{100,92}}, fileName=
                  "modelica://TestModels/../../../mpcpy/MPCPy/doc/userGuide/source/images/logo.png")}),
          Diagram(coordinateSystem(preserveAspectRatio=false)));
    end MPCPy;
  end Icons;

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
  annotation (uses(
      Modelica(version="3.2.2"),
      SOEPDemo(version="1"),
      RapidMPC(version="1"),
      Buildings(version="4.0.0")));
end TestModels;
