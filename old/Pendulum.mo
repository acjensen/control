package Pendulum

    connector Flange "Two-dimensional flange"
        Modelica.SIunits.Position x1;
        Modelica.SIunits.Position y1;
        flow Modelica.SIunits.Force f;
    end Flange;

  model Pendulum "A double pendulum system"
      type Coordinate=Real(unit="m");
      parameter Coordinate x1=0;
      parameter Coordinate y1=0;
      parameter Modelica.SIunits.Length len1=1;
      parameter Modelica.SIunits.Length len2=0.5;
      parameter Modelica.SIunits.Length halflen1=len1/2;
      parameter Modelica.SIunits.Length halflen2=len2/2;
      parameter Modelica.SIunits.Inertia i1=0.5;
      parameter Modelica.SIunits.Inertia i2=0.3;
      Modelica.SIunits.Force f12 "Force of link 1 on link 2";
      Modelica.SIunits.Force f21 "Force of link 2 on link 1";
      Modelica.SIunits.Force fg1 "Force of ground on link 1";
      Modelica.SIunits.Force f1g "Force of link 1 on ground";
      Modelica.SIunits.Torque t1;
      Modelica.SIunits.Torque t2; 
      Coordinate p1x;
      Coordinate p1y;
      Coordinate p2x;
      Coordinate p2y;
      Modelica.SIunits.Angle phi1 "Angle of link 1";
      Modelica.SIunits.Angle phi2 "Angle of link 2";
      Modelica.SIunits.AngularVelocity omega1 "Angular velocity of link 1";
      Modelica.SIunits.AngularVelocity omega2 "Angular velocity of link 2";
  
      initial equation
          phi1 = 0;
          phi2 = 0;
          omega1 = 0;
          omega2 = 0;
      equation
          omega1 = der(phi1);
          omega2 = der(phi2);
          t1 = i1*omega1;
          t2 = i2*omega2;
          f12 = t1*halflen1;
          fg1 = t2*halflen2;
          fg1 = -f1g;
          f12 = -f21;
          p1x = len1*Modelica.Math.sin(phi1);
          p1y = len1*Modelica.Math.cos(phi1);
          p2x = len2*Modelica.Math.sin(phi2);
          p2y = len2*Modelica.Math.cos(phi2);
  
  end Pendulum;

end Pendulum;
