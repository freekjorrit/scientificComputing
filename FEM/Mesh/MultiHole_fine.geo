// Inputs
boxdim = 10;
gridsize = boxdim/60;
Z = 0; 

// Points
Point(1) = {0,0,Z,gridsize};
Point(2) = {boxdim,0,Z,gridsize};
Point(3) = {boxdim,boxdim,Z,gridsize};
Point(4) = {0,boxdim,Z,gridsize};

// Circles
C1x = 0.3*boxdim;
C1y = 0.3*boxdim;
R1 = 0.1*boxdim;
Point(5) = {C1x, C1y, 0, gridsize};
Point(6) = {C1x + R1, C1y, 0, gridsize};
Point(7) = {C1x - R1, C1y, 0, gridsize};

C2x = 0.3*boxdim;
C2y = 0.7*boxdim;
R2 = R1;
Point(8) = {C2x, C2y, 0, gridsize};
Point(9) = {C2x + R2, C2y, 0, gridsize};
Point(10) = {C2x - R2, C2y, 0, gridsize};

C3x = 0.7*boxdim;
C3y = 0.3*boxdim;
R3 = R1;
Point(11) = {C3x, C3y, 0, gridsize};
Point(12) = {C3x + R3, C3y, 0, gridsize};
Point(13) = {C3x - R3, C3y, 0, gridsize};

C4x = 0.7*boxdim;
C4y = 0.7*boxdim;
R4 = R1;
Point(14) = {C4x, C4y, 0, gridsize};
Point(15) = {C4x + R4, C4y, 0, gridsize};
Point(16) = {C4x - R4, C4y, 0, gridsize};

// Lines
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

Circle(5) = {6, 5, 7};
Circle(6) = {7, 5, 6};

Circle(7) = {9, 8, 10};
Circle(8) = {10, 8, 9};

Circle(9) = {13, 11, 12};
Line(10) = {12, 15};
Circle(11) = {15, 14, 16};
Line(12) = {16, 13};

// Line Loop
Line Loop(1) = {3, 4, 1, 2};
Line Loop(2) = {5, 6};
Line Loop(3) = {7, 8};
Line Loop(4) = {9, 10, 11, 12}; 

// Surface
Plane Surface(1) = {1};
Plane Surface(2) = {4,3,2,1};

// Create physical entities
Physical Surface("Surface") 	= {2};
Physical Line("Left Side") 		= {4};
Physical Line("Right Side") 	= {2};
Physical Line("Top and Bottom") = {3, 1};
Physical Line("Circle1")		= {5, 6};
Physical Line("Circle2")		= {7, 8};
Physical Line("Hole")			= {9, 10, 11, 12}; 

