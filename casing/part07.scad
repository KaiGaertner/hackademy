module part07(){
    
    // stripe right
    translate([100,100,400]) color("green") cube([53,206,3]);
    
    //hole in the middle 
    translate([50,103,400]) color("green") cube([50,70,3]);
    translate([50,233,400]) color("green") cube([50,70,3]);
    
    // column left stripe
    translate([3,100,400]) color("green") cube([47,206,3]);
    
    
    // connectors
    
    // mitte hinten
    translate([0,263,400]) color("green") cube([3,43,3]);
    // mitte mitte
    translate([0,163,400]) color("green") cube([3,70,3]);
    translate([0,100,400]) color("green") cube([3,33,3]);
    
    // rechts vorne
    translate([153,100,400]) color("green") cube([3,33,3]);
    
    // rechts mitte
    translate([153,163,400]) color("green") cube([3,70,3]);
    
    // rechts hinten
    translate([153,263,400]) color("green") cube([3,43,3]);
    
    
    // arm right stripe
    translate([-50,100,400]) color("green") cube([50,206,3]);
    
    translate([-220,125,400]) color("green") cube([50,50,3]);
    translate([-120,100,400]) color("green") cube([70,206,3]);
    
    // ueberhang vorne
    translate([-220,20,400]) color("green") cube([100,105,3]);
    // hinten links
    translate([-220,175,400]) color("green") cube([100,131,3]);
}

//use <part01.scad>;
//use <part02.scad>;
//use <part03.scad>;
//use <part04.scad>;
//use <part05.scad>;
//use <part06.scad>;
//part01();
//part02();
//part03();
//// zweites Seitenteil
//translate([15.3,0,0]) part03();
//part04();
//part05();
//part06();
part07();