module part06(){
translate([3,303,3]) color("pink") cube([150,3,397]);
translate([0,303,0]) color("pink") cube([23,3,60]);
translate([133,303,0]) color("pink") cube([23,3,60]);
translate([53,303,0]) color("pink") cube([50,3,3]);
    translate([0,303,120]) color("pink") cube([3,3,120]);
    translate([153,303,120]) color("pink") cube([3,3,120]);
    translate([0,303,300]) color("pink") cube([3,3,100]);
    
    // connector top
    translate([50,303,400]) color("pink") cube([50,3,3]);
    // corresponding element on part05
    //translate([5,10,40]) color("pink") cube([5,0.3,0.3]);
    
    
    // stabilisation
    translate([-100,303,0]) color("pink") cube([100,3,20]);
    
    // connectors right
    translate([153,303,300]) color("pink") cube([3,3,100]);
}

part06();

