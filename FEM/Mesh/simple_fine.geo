// Inputs
boxdim = 1;
gridsize = boxdim/10;
Z = 0; 

// Points
Point(1) = {0,0,Z,gridsize};
Point(2) = {boxdim,0,Z,gridsize};
Point(3) = {boxdim,boxdim,Z,gridsize};
Point(4) = {0,boxdim,Z,gridsize};

// Lines
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

// Line Loop
Line Loop(5) = {3, 4, 1, 2};

// Surface
Plane Surface(6) = {5};

// Create physical entities
Physical Surface("Surface") = {6};
Physical Line("Left Side") = {4};
Physical Line("Right Side") = {2};
Physical Line("Top and Bottom") = {3, 1};
Coherence;
