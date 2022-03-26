#  var s  = (+document.form_calc.s.value);
# var n = 1;
# var dArray = [];

# for (n=1; n<25; n++){
# dArray[n] = s - (s / Math.pow(2, (n / 12)));
# dArray[n] = Math.round(dArray[n] * 1000) / 1000;
# }

frets=[]
n=1
scale=640
fret =0
frets.append(fret)
while n<25 :
    fret=scale - (scale / pow(2,(n/12)) )
    frets.append(fret)
    n=n+1

for fret in frets :
    print(fret)
