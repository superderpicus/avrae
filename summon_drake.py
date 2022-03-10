embed <drac2>

# Variables
ch = character()
c = combat()
com = combat() and combat().me
cc = "Summon Drake"
i = '-i' in &ARGS&
args = argparse(&ARGS&)
ele = args.last('e') or "fire";
ele = ele.capitalize()
lvl = args.last('l');
their = get('their','their')

index = ['Fire', 'Lightning', 'Poison', 'Acid', 'Cold']
elements = ['Fire 🔥', 'Lightning ⚡', 'Poison ☠️', 'Acid ☣️', 'Cold ❄️']
if not ele in index:
  ele = "Fire";

var = 0;
count = 0;
for x in index:
  if x == ele:
    var = count;
  count += 1;

ele = elements[var];
ch.set_cvar("drake_element", index[var].lower());

base = f'''!i madd "Fatalis ({ele})" -name "Fatalis" -h ''';
base += f''' -thumb {image} -color {color} '''

# Checking if there are uses left.
if not i:
  if not ch.get_cc(cc) and not lvl:
    return base + f''' -title "{name} has no uses of {cc} left!" -f "To use this without a use of {cc}, use [-l level] to expend a spell slot." '''

  elif lvl:
    has = ch.spellbook.get_slots(lvl);
    if has > 0:
      ch.spellbook.use_slot(lvl);
      return base + f'''-title "{name} uses {their} {cc}!" -desc "At 3rd level, as an action, you can magically summon the drake that is bound to you. It appears in an unoccupied space of your choice within 30 feet of you.\n\nOnce you summon the drake, you can’t do so again until you finish a long rest, unless you expend a spell slot of 1st level or higher to summon it.\n\nSummoned Drake Element: {ele}\n\n{ch.spellbook.slots_str(lvl)} (-1)"'''
  
    else:
      base += ""
      return base + f'''-title "{name} uses {their} {cc}!" -desc "You do not have enough spell slots remaining to use this spell!\n\n{ch.spellbook.slots_str(lvl)}"'''
  else:
    ch.mod_cc(cc,-1);
    base += f''' -footer "{cc}: {ch.cc_str(cc)} (-1)" '''
else:   
  if ch.cc_exists(cc):
    base += f''' -footer "{cc}: {ch.cc_str(cc)}" '''

# Adding the description and title. 
base += f''' -title "{name} uses {their} {cc}!" '''
# Adding the effect if there is combat and a target.
base += f''' -desc "At 3rd level, as an action, you can magically summon the drake that is bound to you. It appears in an unoccupied space of your choice within 30 feet of you.\n\nOnce you summon the drake, you can’t do so again until you finish a long rest, unless you expend a spell slot of 1st level or higher to summon it.\n\nSummoned Drake Element: {ele}"''';

return base
</drac2>
