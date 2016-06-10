// Inputs
boxdim = 1;
gridsize = boxdim/30;
Z = 0; 

// Points
Point(1) = {0,0,Z,gridsize};
Point(2) = {boxdim,0,Z,gridsize};
Point(3) = {boxdim,boxdim,Z,gridsize};
Point(4) = {0,boxdim,Z,gridsize};
Point(5) = {0.5*boxdim, 0.5*boxdim, 0, gridsize};
Point(6) = {0.6*boxdim, 0.5*boxdim, 0, gridsize};
Point(7) = {0.4*boxdim, 0.5*boxdim, 0, gridsize};

// Lines
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Circle(5) = {6, 5, 7};
Circle(6) = {7, 5, 6};

// Line Loop
Line Loop(5) = {3, 4, 1, 2};
Line Loop(6) = {5, 6};

// Surface
Plane Surface(1) = {5};
Plane Surface(2) = {6,5};

// Create physical entities
Physical Surface("Surface") 	= {2};
Physical Line("Left Side") 		= {4};
Physical Line("Right Side") 	= {2};
Physical Line("Top and Bottom") = {3, 1};
Physical Line("Circle")			= {5, 6};

