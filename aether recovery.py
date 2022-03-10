!alias aetherrecovery embed <drac2>
ch = character(); cc = "Aether Recovery"; cc2 = "Aether"; ccstr = "";
fLevel = ch.levels.get("Fighter"); base = ""; prof = proficiencyBonus;
if not fLevel or fLevel < 10:    
    return base + f'''-title "Fighter level too low!" -desc "This character does not have enough fighter levels to use this."''';
count = ch.cc_exists(cc) and ch.get_cc(cc) or 0;
if not ch.cc_exists(cc):    
    return base + f'''-title "Counter not found!" -desc "This character does not a counter called: {cc}."''';
if count == 0:    
    return base + f'''-title "No remaining uses of {cc} left!" -desc "You cannot use this feature until your next long rest."''';
if not ch.cc_exists(cc2):
    return base + f'''-title "Counter not found!" -desc "This character does not a counter called: {cc2}."''';
aether = ch.get_cc(cc2);
ch.mod_cc(cc, -1);
ccstr += f''' -f "{cc}|{ch.cc_str(cc)} (-1)" '''
ch.mod_cc(cc2, prof);
ccstr += f''' -f "{cc2}|{ch.cc_str(cc2)} (+{ch.get_cc(cc2) - aether }) "''';
desc = "*At the 10th Level, when you use Second Wind you recover Aether equal to your proficiency bonus. You may do so once per long rest.*\n\n";\
base += f''' -desc "{desc}" '''; 
base += ccstr;
return base;
</drac2>