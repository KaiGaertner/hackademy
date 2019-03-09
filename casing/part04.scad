module part04 (){
    translate([3,3,50])color("blue") cube([150,100,3]);
    translate([0,0,50])color("blue") cube([23,13,3]);
    translate([133,0,50])color("blue") cube([23,13,3]);
    translate([53,0,50])color("blue") cube([50,3,3]);
    translate([0,33,50])color("blue") cube([3,27,3]);
    translate([153,33,50])color("blue") cube([3,27,3]);
    translate([0,80,50])color("blue") cube([3,23,3]);
    translate([153,80,50])color("blue") cube([3,23,3]);
}

//use <part01.scad>;
//use <part02.scad>;
//use <part03.scad>;
//
//part01();
//part02();
//part03();
//// zweites Seitenteil
//translate([15.3,0,0]) part03();

part04();