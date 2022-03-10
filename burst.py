embed <drac2>
ch = character()
c = combat()
cc = "Aether"
i = '-i' in &ARGS&
args = argparse(&ARGS&)
rr = int(args.last('rr') or 1);
ele = args.last('e');
targets = args.get('t');
_ele = ele or get("burst", "fire");
_elist = ['fire', 'cold', 'lightning'];
if not _ele in _elist:
	_ele = 'fire';
targets = [target for targ in targets if c and (target := c.get_combatant(targ))]
desc = "*Starting at 3rd Level, when you hit a creature with a melee weapon attack you can expend one Aether charge to pull your weapon\'s trigger and to deal additional damage to the target. When you gain this feature you can decide if its damage is fire, cold or lightning. You cannot change this damage once you pick a damage type. The creature takes 2d4 of the type you choose. This damage increases to 3d4 at 7th level, 4d4 at 15th level.*\n\n";
footer = "";
tCount = 0;
for t in targets:
	tCount += 1;
hasTarget = tCount > 0;
tCount = tCount > 0 and tCount or 1;
base = f''' -thumb {image} -color {color} '''
totalHits = rr * tCount;
totalDamage = 0;
count = ch.cc_exists(cc) and ch.get_cc(cc) or 0;
if not i:
  if (not count) or (count < (totalHits)):
    return base + f''' -title "Not enough {cc} left!" -desc "You don't have enough {cc} left to use this." -f "{cc}|{cc_str(cc)}" '''
  else:
    ch.mod_cc(cc,(totalHits) * -1);
    base += f''' -f "{cc}|{ch.cc_str(cc)} (-{(totalHits)})" '''    
else:   
  if ch.cc_exists(cc):
    base += f''' -f "{cc}|{ch.cc_str(cc)}" '''
base += f''' -title "{name} uses Burst Strike!" '''
if hasTarget:
	for target in targets:
		for i in range(0, rr):
			res = target.damage(f'''{(level >= 15 and 4) or (level >= 7 and 3) or 2}d4[{_ele}]''');
			totalDamage += res.total;
			desc += f'''**{target.name}**\n{res.damage}\n\n'''
			footer += f'''{target.name}: {target.hp_str()}\n'''
else:
	r = vroll(f'''{(level >= 15 and 4) or (level >= 7 and 3) or 2}d4[{_ele}]''');
	desc += f'''**Damage:** {r}\n\n'''
	base += f''' -title "{name} uses Burst Strike!"'''
	totalDamage += r.total;
if totalDamage > 0:
	desc += f'''**Total Damage:** {totalDamage}\n''';
base += f''' -desc "{desc}" -footer "{footer}" ''';
return base
</drac2>
