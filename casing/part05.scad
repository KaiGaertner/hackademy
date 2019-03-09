module part05(){
    translate([3,100,53])color("grey") cube([150,3,347]);
    translate([0,100,53])color("grey") cube([3,3,67]);
    translate([153,100,53])color("gray") cube([3,3,67]);
    translate([0,100,180])color("grey") cube([3,3,80]);
    translate([153,100,180])color("grey") cube([3,3,80]);
    
    // connector top
    translate([50,100,400]) color("grey") cube([50,3,3]);
    // corresponding element on part06
    //translate([5,30.3,40]) color("red") cube([5,0.3,0.3]);
    
    // connectors left
    translate([0,100,320])color("grey") cube([3,3,80]);
    
    // connectors right
    translate([153,100,320])color("grey") cube([3,3,80]);
}

//use <part01.scad>;
//use <part02.scad>;
//use <part03.scad>;
//use <part04.scad>;

//part01();
//part02();
//part03();
//// zweites Seitenteil
//translate([15.3,0,0]) part03();
//part04();
part05();
