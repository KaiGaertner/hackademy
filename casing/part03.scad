module part03 (){
    // high part
    translate([0,103,0]) color ("red") cube([3,30,400]);
    translate([0,133,3]) color ("red") cube([3,30,400]);
    // middle part
    translate([0,163,0])color("red") cube([3,30,400]);
    //einkerbung
    translate([0,193,0])color("red") cube([3,3,350]);
    translate([0,196,0])color("red") cube([3,37,400]);
    translate([0,233,3])color("green") cube([3,30,400]);
    translate([0,263,0]) color("blue") cube([3,40,400]);
    
    // pin rueckwand unten
    translate([0,303,60])color("red")cube([3,3,60]);
    // pin rueckwand oben
    translate([0,303,240])color("red")cube([3,3,60]);
    
    // pin vorne mitte
    translate([0,100,120])color("red")cube([3,3,60]);
    // pin vorne oben
    translate([0,100,260])color("red")cube([3,3,60]);
    
    // pin part03a
    translate([0,100,20]) color ("red") cube([3,3,20]);
}

// to long for printer
part03();