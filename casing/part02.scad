module part02 (){
    //links
    color("green") cube([23,3,15]);
    translate([3,0,15])color("green")  cube([20,3,15]);
    translate([0,0,30]) color("green") cube([23,3,20]);
    // high links
    translate([23,0,3]) color("green") cube([30,3,50]);
    // mitte
    translate([53,0,0]) color("green") cube([50,3,50]);
    // high rechts
    translate([103,0,3])color("green")  cube([30,3,50]);
    // rechts
    translate([133,0,0])
    color("green") cube([23,3,15]);
    translate([133,0,15]) color("green") cube([20,3,15]);
    translate([133,0,30]) color("green") cube([23,3,20]);
}
part02();

