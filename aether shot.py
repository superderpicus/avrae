!alias aethershot embed <drac2>
ch = character(); c = combat(); cc = "Loaded Aether"; i = '-i' in &ARGS&; args = argparse(&ARGS&);
rr = int(args.last('rr') or 1); ele = args.last('e'); targets = args.get('t'); fLevel = ch.levels.get("Fighter");
crit = [False,True][args.adv(custom={'adv':'crit'})]; _ele = ele or get("shot", "fire"); _elist = ['fire', 'cold', 'lightning']; critText = " (CRIT!)";
dex = dexterityMod; prof = proficiencyBonus; hitBonus = dex + prof;
if not _ele in _elist:
    _ele = 'fire';
targets = [target for targ in targets if c and (target := c.get_combatant(targ))];
desc = "*By 7th level, your Savageclaw design has become more intricate, allowing you to include a functional ranged weapon into it. While wielding a Savageclaw you gain a new attack option that you can use with the Attack action. This special attack is a ranged weapon attack with a range of 60 feet. You are proficient with it, and you add your Dexterity modifier to its attack and damage rolls. When you gain this feature you can decide if It's damage is fire, cold or lightning. You cannot change this damage once you pick a damage type. its damage die is 1d8. You expend one Aether charge when you use this attack option.\n\tWhen you gain the Extra Attack feature, this special attack can be used for any of the attacks you make as part of the Attack action.*\n\n";\
footer = ""; tCount = 0;
damstr = "1d8";
for t in targets:
    tCount += 1;
hasTarget = tCount > 0; tCount = tCount > 0 and tCount or 1;
base = f''' -thumb {image} -color {color} '''; ccstr = "";
if not fLevel or fLevel < 7:
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
base += f''' -title "{name} uses Aether Shot!" '''
if hasTarget:
    for target in targets:
        tDam = 0;

        t = f'''{target.name}''';
        b = "";
        for i in range(0, rr):
            hit = vroll(f'''1d20+{hitBonus}''');
            if rr > 1:
                b += f'''__**Attack {i+1}**__\n''';
            if hit.result > target.ac:
                res = target.damage(f'''{damstr}[{_ele}]''', crit);
                tDam += res.total; totalDamage += res.total;
                b += f'''{res.damage}\n\n'''
                footer += f'''{target.name}: {target.hp_str()}\n'''
            else:
                b += f'''**Miss!**''';
        if rr > 1 and tDam > 0:
            b += f'''__**Total Damage:**__ {tDam}\n\n''';
        base += f''' -f "{t}|{b} "'''
else:
    t = "";
    b = "";
    for i in range(0, rr):
        hit = vroll(f'''1d20+{prof}+{dex}''');
        r = vroll(f'''{damstr}[{_ele}]''', crit and 2 or 1);
        rText = f'''**To Hit:** {hit}\n**Damage:{crit and critText or ""}** {r}''';
        if rr > 1:          
            base += f''' -f "Attack {i+1}|{rText}" ''';
        else:
            base += f''' -f "Meta|{rText}" ''';
    totalDamage += r.total;
    if totalDamage > 0:
        base += f''' -f "Total Damage|{totalDamage} "''';
base += f''' -desc "{desc}" -footer "{footer}" '''; base += ccstr; return base;
</drac2>