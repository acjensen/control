package Pendulum

    SI = import Modelica.Units.SI;

    connector Flange "Two-dimensional flange"
        parameter Coordinate x1=0;
        parameter Coordinate y1=0;
        flow SI.Force

    SI.Position s "Absolute position of flange";
    flow SI.Force f "Cut force directed into flange";

    model Pendulum "A double pendulum system"
        type Angle=Real(unit="rad");
        type AngularVelocity=Real(unit="rad/s");
        type Inertia=Real(unit="kg.m2");
        type Length=Real(unit="m");
        type Coordinate=Real(unit="m");
        parameter Coordinate x1=0;
        parameter Coordinate y1=0;
        parameter Inertia L1=.5;
        parameter Inertia L2=.3;
        parameter Length len1=1;
        parameter Length len2=.5;
        Angle phi1 "Angle for link 1";
        Angle phi2 "Angle for link 2";
        AngularVelocity omega1 "Angular velocity for link 1";
        AngularVelocity omega2 "Angular velocity for link 2";

        initial equation
            phi1 = 0;
            phi2 = 0;
            omega1 = 0;
            omega2 = 0;
        equation
            omega1 = der(phi1);
            omega2 = der(phi2);

    end Pendulum

end Pendulum