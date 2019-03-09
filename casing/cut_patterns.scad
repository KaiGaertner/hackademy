use <part01.scad>;
use <part02.scad>;
use <part03.scad>;
use <part04.scad>;
use <part05.scad>;
use <part06.scad>;
use <part07.scad>;
use <part08.scad>;

projection (cut=true) translate ([0,0,0])
part01();

projection (cut=true) translate ([200,0,0])
rotate([-90,0,0])part02();

projection (cut=true) translate ([500,100,0])
rotate([0,90,90])part03();

projection (cut=false)
translate([500,200,0])rotate([0,0,0]) part04();

projection (cut=false)
translate([500,0,-100])rotate([90,0,90]) part05();

projection (cut=false)
translate([750,350,0])rotate([90,0,90]) part06();

projection (cut=false)
translate([250,500,0])rotate([0,0,0]) part07();


projection (cut=false)
translate([500,100,0])rotate([-90,0,0]) part08();