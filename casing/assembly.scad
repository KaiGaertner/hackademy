use <part01.scad>;
use <part02.scad>;
use <part03.scad>;
use <part03a.scad>;
use <part04.scad>;
use <part05.scad>;
use <part06.scad>;
use <part07.scad>;
use <part08.scad>;

part01();
part02();
part03();
// zweites Seitenteil
translate([153,0,0]) part03();

part03a();
// zweites Seitenteil
translate([153,0,0]) part03a();
part04();
part05();
part06();
part07();
part08();