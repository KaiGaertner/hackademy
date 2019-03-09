module part08(){
    translate([-20,193,350])color("green")cube([196,3,50]);
    translate([-20,193,300])color("green")cube([20,3,50]);
    translate([156,193,300])color("green")cube([20,3,50]);
    translate([3,193,300])color("green")cube([150,3,50]);

}


//use <part01.scad>;
//use <part02.scad>;
//use <part03.scad>;
//use <part04.scad>;
//use <part05.scad>;
//use <part06.scad>;
//use <part07.scad>;
//
//part01();
//part02();
//part03();
//// zweites Seitenteil
//translate([15.3,0,0]) part03();
//part04();
//part05();
//part06();
//part07();
part08();
//
//projection (cut=false)
//translate([0,0,0])rotate([-90,0,0]) part08();