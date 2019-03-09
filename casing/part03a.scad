module part03a (){
    
    // base form
    translate([0,3,3] )color ("orange") cube([3,97,47]);
    
    // pin unten vorne
    translate([0,3,0]) color ("orange") cube([3,30,3]);
    
    // pin vorderseite
    translate([0,0,15]) color ("orange") cube([3,3,15]);
   
    
    // pin oben vorne
    translate([0,13,50]) color ("orange") cube([3,20,3]);
    
    //pin unten hinten
    translate([0,63,0] )color ("orange") cube([3,37,3]);
    
    
    // pin oben hinten
    translate([0,60,50])color ("orange") cube([3,20,3]);
    
    // connector part03 unten
    translate([0,100,0]) color ("orange") cube([3,3,20]);
    
    // connector part03 oben
    translate([0,100,40]) color ("orange") cube([3,3,10]);
}

part03a();