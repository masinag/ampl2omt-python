import os

from ampl2omt.problem.objective import Objective

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_file_path(file_name):
    return os.path.join(BASE_DIR, file_name)


def test_parse_hs001(mgr, parser):
    # var x {j in 1..2};
    #
    # minimize obj:
    #   100*(x[2] - x[1]^2)^2 + (1-x[1])^2;
    #   ;
    #
    # subject to constr: -1.5 <= x[2];
    problem = parser.parse_file(get_file_path("hs001.nl"))
    assert problem.variables == [
        mgr.VarReal("x0"),
        mgr.VarReal("x1"),
    ]
    x0, x1 = problem.variables
    assert problem.objectives == [
        Objective(Objective.MINIMIZE,
                  mgr.Plus(
                      mgr.Mult(mgr.Real(100),
                               mgr.Pow(mgr.Minus(x1, mgr.Pow(x0, mgr.Real(2))), mgr.Real(2))),
                      mgr.Pow(mgr.Minus(mgr.Real(1), x0), mgr.Real(2))
                  ))
    ]
    assert problem.constraints == [
        mgr.Ge(x1, mgr.Real(-1.5))
    ]


def test_parse_hs073(mgr, parser):
    # var x {1..4} >= 0;
    #
    # minimize obj:
    #   24.55*x[1] + 26.75*x[2] + 39*x[3] + 40.50*x[4]
    #   ;
    #
    # subject to constr1: 2.3*x[1] + 5.6*x[2] + 11.1*x[3] + 1.3*x[4] >= 5;
    # subject to constr2: 12*x[1] + 11.9*x[2] + 41.8*x[3] + 52.1*x[4]
    #     >= 21 +
    #        1.645*sqrt(0.28*x[1]^2 + 0.19*x[2]^2 + 20.5*x[3]^2 + 0.62*x[4]^2);
    # subject to constr3: sum {j in 1..4} x[j] = 1;
    #
    # let x[1] := 1;
    # let x[2] := 1;
    # let x[3] := 1;
    # let x[4] := 1;
    problem = parser.parse_file(get_file_path("hs073.nl"))
    assert problem.variables == [
        mgr.VarReal("x0"),
        mgr.VarReal("x1"),
        mgr.VarReal("x2"),
        mgr.VarReal("x3"),
    ]


def test_parse_hs085(mgr, parser):
    # param a {2..17};
    # param b {2..17};
    # param c10 := 12.3/752.3;
    #
    # var x {1..5};
    # var y1  = x[2]+x[3]+41.6;
    # var c1  = .024*x[4]-4.62;
    # var y2  = 12.5/c1+12;
    # var c2  = .0003535*x[1]^2+.5311*x[1]+.08705*y2*x[1];
    # var c3  = .052*x[1]+78+.002377*y2*x[1];
    # var y3  = c2/c3;
    # var y4  = 19*y3;
    # var c4  = .04782*(x[1]-y3)+.1956*(x[1]-y3)^2/x[2]+.6376*y4+1.594*y3;
    # var c5  = 100*x[2];
    # var c6  = x[1]-y3-y4;
    # var c7  = .95-c4/c5;
    # var y5  = c6*c7;
    # var y6  = x[1]-y5-y4-y3;
    # var c8  = (y5+y4)*.995;
    # var y7  = c8/y1;
    # var y8  = c8/3798;
    # var c9  = y7-.0663*y7/y8-.3153;
    # var y9  = 96.82/c9+.321*y1;
    # var y10 = 1.29*y5+1.258*y4+2.29*y3+1.71*y6;
    # var y11 = 1.71*x[1]-.452*y4+.58*y3;
    # var c11 = 1.75*y2*.995*x[1];
    # var c12 = .995*y10+1998;
    # var y12 = c10*x[1]+c11/c12;
    # var y13 = c12-1.75*y2;
    # var y14 = 3623+64.4*x[2]+58.4*x[3]+146312/(y9+x[5]);
    # var c13 = .995*y10+60.8*x[2]+48*x[4]-.1121*y14-5095;
    # var y15 = y13/c13;
    # var y16 = 148000-331000*y15+40*y13-61*y15*y13;
    # var c14 = 2324*y10-28740000*y2;
    # var y17 = 14130000-1328*y10-531*y11+c14/c12;
    # var c15 = y13/y15-y13/.52;
    # var c16 = 1.104-.72*y15;
    # var c17 = y9+x[5];
    #
    # minimize obj:
    #    -5.843e-7*y17+1.17e-4*y14+2.358e-5*y13+1.502e-6*y16
    #    +.0321*y12+.004324*y5+1e-4*c15/c16+37.48*y2/c12+.1365;
    #
    # s.t. con1:  1.5*x[2]-x[3]>=0;
    # s.t. con2:  y1-213.1>=0;
    # s.t. con3:  405.23-y1>=0;
    # s.t. con4:  x[1]>=704.4148;
    # s.t. con5:  x[1]<=906.3855;
    # s.t. con6:  x[2]>=68.6;
    # s.t. con7:  x[2]<=288.88;
    # s.t. con8:  x[3]>=0;
    # s.t. con9:  x[3]<=134.75;
    # s.t. con10: x[4]>=193;
    # s.t. con11: x[4]<=287.0966;
    # s.t. con12: x[5]>=25;
    # s.t. con13: x[5]<=84.1988;
    # s.t. con14: y2-a[2]>=0;
    # s.t. con15: y3-a[3]>=0;
    # s.t. con16: y4-a[4]>=0;
    # s.t. con17: y5-a[5]>=0;
    # s.t. con18: y6-a[6]>=0;
    # s.t. con19: y7-a[7]>=0;
    # s.t. con20: y8-a[8]>=0;
    # s.t. con21: y9-a[9]>=0;
    # s.t. con22: y10-a[10]>=0;
    # s.t. con23: y11-a[11]>=0;
    # s.t. con24: y12-a[12]>=0;
    # s.t. con25: y13-a[13]>=0;
    # s.t. con26: y14-a[14]>=0;
    # s.t. con27: y15-a[15]>=0;
    # s.t. con28: y16-a[16]>=0;
    # s.t. con29: y17-a[17]>=0;
    # s.t. con30: b[2]-y2>=0;
    # s.t. con31: b[3]-y3>=0;
    # s.t. con32: b[4]-y4>=0;
    # s.t. con33: b[5]-y5>=0;
    # s.t. con34: b[6]-y6>=0;
    # s.t. con35: b[7]-y7>=0;
    # s.t. con36: b[8]-y8>=0;
    # s.t. con37: b[9]-y9>=0;
    # s.t. con38: b[10]-y10>=0;
    # s.t. con39: b[11]-y11>=0;
    # s.t. con40: b[12]-y12>=0;
    # s.t. con41: b[13]-y13>=0;
    # s.t. con42: b[14]-y14>=0;
    # s.t. con43: b[15]-y15>=0;
    # s.t. con44: b[16]-y16>=0;
    # s.t. con45: b[17]-y17>=0;
    # s.t. con46: y4-.28/.72*y5>=0;
    # s.t. con47: 21-3496*y2/c12>=0;
    # s.t. con48: 62212/c17-110.6-y1>=0;
    #
    # data;
    #
    # param a:=
    #  2       17.505
    #  3       11.275
    #  4      214.228
    #  5        7.458
    #  6         .961
    #  7        1.612
    #  8         .146
    #  9      107.99
    # 10      922.693
    # 11      926.832
    # 12       18.766
    # 13     1072.163
    # 14     8961.448
    # 15         .063
    # 16    71084.33
    # 17  2802713
    #  ;
    #
    # param b:=
    #  2     1053.6667
    #  3       35.03
    #  4      665.585
    #  5      584.463
    #  6      265.916
    #  7        7.046
    #  8         .222
    #  9      273.366
    # 10     1286.105
    # 11     1444.046
    # 12      537.141
    # 13     3247.039
    # 14    26844.086
    # 15         .386
    # 16   140000
    # 17 12146108
    problem = parser.parse_file(get_file_path("hs085.nl"))
    assert problem.variables == [mgr.VarReal(f"x{i}") for i in range(5)]