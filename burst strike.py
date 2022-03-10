!alias burst2 embed <drac2>
ch = character(); c = combat(); cc = "Loaded Aether"; i = '-i' in &ARGS&; args = argparse(&ARGS&);
rr = int(args.last('rr') or 1); ele = args.last('e'); targets = args.get('t'); fLevel = ch.levels.get("Fighter");
crit = [False,True][args.adv(custom={'adv':'crit'})]; _ele = ele or get("burst", "fire"); _elist = ['fire', 'cold', 'lightning']; critText = " (CRIT!)";
if not _ele in _elist:
    _ele = 'fire';
targets = [target for targ in targets if c and (target := c.get_combatant(targ))];
desc = "*Starting at 3rd Level, when you hit a creature with a melee weapon attack you can expend one Aether charge to pull your weapon\'s trigger and to deal additional damage to the target. When you gain this feature you can decide if its damage is fire, cold or lightning. You cannot change this damage once you pick a damage type. The creature takes 2d4 of the type you choose. This damage increases to 3d4 at 7th level, 4d4 at 15th level.*\n\n";\
footer = ""; tCount = 0;
damstr = fLevel >= 15 and "4d4" or (fLevel >= 7 and "3d4" or (fLevel >= 3 and "2d4"));
for t in targets:
    tCount += 1;
hasTarget = tCount > 0; tCount = tCount > 0 and tCount or 1;
base = f''' -thumb {image} -color {color} '''; ccstr = "";
if not fLevel or fLevel < 3:
    return base + f'''-title "Fighter level too low!" -desc "This character does not have enough fighter levels to use this."''';
totalHits = rr * tCount; totalDamage = 0;
count = ch.cc_exists(cc) and ch.get_cc(cc) or 0;
if not i:
  if (not count) or (count < (totalHits)):
    return base + f''' -title "Not enough {cc} left!" -desc "You don't have enough {cc} left to spend {totalHits} Aether." -f "{cc}|{cc_str(cc)}" '''
  else:
    ch.mod_cc(cc,(totalHits) * -1);
    ccstr += f''' -f "{cc}|{ch.cc_str(cc)} (-{(totalHits)})" '''    
else:   
  if ch.cc_exists(cc):
    ccstr += f''' -f "{cc}|{ch.cc_str(cc)}" '''
base += f''' -title "{name} uses Burst Strike!" '''
if hasTarget:
    for target in targets:
        tDam = 0;

        t = f'''{target.name}''';
        b = "";
        for i in range(0, rr):
            if rr > 1:
                b += f'''__**Attack {i+1}**__\n''';
            res = target.damage(f'''{damstr}[{_ele}]''', crit);
            tDam += res.total; totalDamage += res.total;
            b += f'''{res.damage}\n\n'''
            footer += f'''{target.name}: {target.hp_str()}\n'''
        if rr > 1:
            b += f'''__**Total Damage:**__ {tDam}\n\n''';
        base += f''' -f "{t}|{b} "'''
else:
    t = "";
    b = "";
    for i in range(0, rr):
        r = vroll(f'''{damstr}[{_ele}]''', crit and 2 or 1);
        rText = f'''**Damage:{crit and critText or ""}** {r}''';
        if rr > 1:          
            base += f''' -f "Attack {i+1}|{rText}" ''';
        else:
            base += f''' -f "Meta|{rText}" ''';
    totalDamage += r.total;
    base += f''' -f "Total Damage|{totalDamage} "''';
base += f''' -desc "{desc}" -footer "{footer}" '''; base += ccstr; return base;
</drac2>