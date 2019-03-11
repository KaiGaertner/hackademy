module part01 (){
//base part
translate([3,3,0]) color("yellow") cube([150,300,3]);
// front handles
translate([23,0,0])cube([30,3,3]);
translate([103,0,0])cube([30,3,3]);
// back handles
translate([23,303,0])color ("yellow")cube([30,3,3]);
translate([103,303,0])cube([30,3,3]);
// left handles
translate([0,33,0]) cube([3,30,3]);
translate([0,133,0]) cube([3,30,3]);
translate([0,233,0]) color("yellow") cube([3,30,3]);
// right handles
translate([153,33,0]) cube([3,30,3]);
translate([153,133,0]) cube([3,30,3]);
translate([153,233,0]) color("yellow") cube([3,30,3]);
};
part01();

