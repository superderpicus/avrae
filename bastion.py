!alias bastion embed <drac2>
ch = character(); 
c = combat(); 
cc = "Sorcery Points";
i = '-i' in &ARGS&; 
args = argparse(&ARGS&);
target = args.last('t') or None;
amount = int(args.last('n') or 1);
ccstr = "";
base = "";
desc = "You can tap into the grand equation of existence to imbue a creature with a shimmering shield of order. As an action, you can expend 1 to 5 sorcery points to create a magical ward around yourself or another creature you can see within 30 feet of you.\n\nThe ward lasts until you finish a long rest or until you use this feature again. The ward is represented by a number of d8s equal to the number of sorcery points spent to create it. When the warded creature takes damage, it can expend a number of those dice, roll them, and reduce the damage taken by the total rolled on those dice."
n = "Bastion of Law";
lvl = ch.levels.get("Sorcerer");
if not lvl or lvl < 6:
  return base + f'''-title "Sorcerer level too low!" -desc "This character does not have enough sorcerer levels to use this."''';
count = ch.cc_exists(cc) and ch.get_cc(cc) or 0;
if not i:
  if (not count) or (count < amount):
    return base + f''' -title "Not enough {cc} left!" -desc "You don't have enough {cc} left to spend {amount} {cc}." -f "{cc}|{cc_str(cc)}" '''
  else:
    ch.mod_cc(cc, -amount);
    ccstr += f''' -f "{cc}|{ch.cc_str(cc)} (-{amount})" '''    
else:   
  if ch.cc_exists(cc):
    ccstr += f''' -f "{cc}|{ch.cc_str(cc)}" '''
base += f''' -title "{name} uses {n}!" '''
if target and c:
  com = c.get_combatant(target);
  com.add_effect(f'Bastion of Law ({amount}d8)', f' -attack "|-{amount}d8|Bastion Healing" ', -1, False, None, False, "The ward is represented by a number of d8s equal to the number of sorcery points spent to create it. When the warded creature takes damage, it can expend a number of those dice, roll them, and reduce the damage taken by the total rolled on those dice.") if com else "";
  base += f''' -f "{com.name}|**Effect**: Bastion of Law ({amount}d8)\n`{amount}d8` damage can be prevented." ''';
else:
  base += f''' -f "Ward|`{amount}d8` damage can be prevented." {ccstr} ''';
base += f''' -f "Bastion of Law|{desc}" ''';
return base;
</drac2>
-thumb {image}
-color {color}