embed <drac2>
args = argparse(&ARGS&);_args = &ARGS&;ch = character(); _argsJoined = " ".join(_args).lower();
if not ch:
	err("You do not have a valid character");
purse = ch.coinpurse;startCoins = purse.get_coins();compactMode = get("coinscompact", "0");autoMode = get("coinsauto", "0");imported = get("coinsimported", "0");mode = get("coinsmode", "0");_coins = ["pp", "gp", "ep", "sp", "cp"];delta = [0, 0, 0, 0, 0];
base = f' -thumb "https://i.imgur.com/auM9MBe.png" -color "#d4af37" -title "{name}\\\'s Coinpurse" '; trailStr = "";
if (imported == "0" and purse.total == 0) or ("import" in args):
	_forceImport = f'import {name.lower()}' in _argsJoined;
	if "import" in args and imported == "1" and (not _forceImport):
		trailStr += f' -f "Coins Not Imported|Your coins were already imported previously from the bags alias. If you want to import again, type `!coins import {name.lower()}`." ';
	else:
		ch.set_cvar("coinsimported", "1");
		bags = load_json(get('bags', '[]'))
		bagsDict = {bag: items for bag, items in bags}
		coins = bagsDict.get('Coin Pouch');
		if coins:
			#purse.modify_coins(coins.pp, coins.gp, coins.ep, coins.sp, coins.cp)
			delta[0] = coins.pp; delta[1] = coins.gp; delta[2] = coins.ep; delta[3] = coins.sp; delta[4] = coins.cp;
			trailStr += f' -f "Coins Imported|Your coins were imported from the bags alias." ';
if "compact" in args:
	if (not compactMode) or (compactMode == "0"):
		ch.set_cvar("coinscompact", "1") ;
		trailStr += f' -f "Compact Mode:|On" '
	else:
		ch.set_cvar("coinscompact", "0");
		trailStr += f' -f "Compact Mode:|Off" '
	compactMode = get("coinscompact", "0");
if "auto" in args:
	if (not autoMode) or (autoMode == "0"):
		ch.set_cvar("coinsauto", "1") ;
		trailStr += f' -f "Automatic Conversion:|On" '
	else:
		ch.set_cvar("coinsauto", "0");
		trailStr += f' -f "Automatic Conversion:|Off" '
	autoMode = get("coinsauto", "0");
if "mode" in args:
	if (not mode) or (mode == "0"):
		ch.set_cvar("coinsmode", "1");
		trailStr += f' -f "Coin Mode:|Multi" ';
	else:
		ch.set_cvar("coinsmode", "0");
		trailStr += f' -f "Coin Mode:|Single" ';
if f'wipe {name.lower()}' in _argsJoined:
	trailStr += f' -f "Wipe:|Coins wiped." '
	purse.set_coins(0, 0, 0, 0, 0);
elif "wipe" in args:
	trailStr += f' -f "Wipe:|Are you sure you want to wipe your coins? If you are sure, type `!coins wipe {name.lower()}` to empty your coins." '
if mode == "1":
	for a in _args:
		if a != "":
			size = len(a);
			if a.isnumeric() or a[1:].isnumeric():
				delta[1] += int(a);
			elif a != "" and any(char.isdigit() for char in a):
				amt = a[0:size-2];suf = a[size-2:size];index = 0;
				if suf in _coins:
					index = _coins.index(suf);
				else:
					err(f'Invalid coin type: `{suf}` passed in arguments.');
				delta[index] += int(amt);
else:
	a ="".join(_args).lower().replace(" ","");
	if a != "":
		size = len(a);
		if a.isnumeric() or a[1:].isnumeric():
			delta[1] += int(a);
		elif a != "" and any(char.isdigit() for char in a):
			amt = a[0:size-2];suf = a[size-2:size]; index = 0;
			if suf in _coins:
				index = _coins.index(suf);
			else:
				err(f'Invalid coin type: `{suf}` passed in arguments.');
			delta[index] += int(amt);
for x in range(5):
	if ((startCoins[_coins[x]]) + delta[x] < 0):
		err(f'You do not have enough `{_coins[x]}` to do that.')
purse.modify_coins(delta[0],delta[1],delta[2],delta[3],delta[4],autoMode);
totalGained = purse.total - startCoins.total;
if autoMode == "1":
	purse.autoconvert();
if compactMode == "1":
	_delta = round(totalGained, 3);
	if _delta != 0:
		if _delta < 0:
			_delta = f'({_delta})';
		else:				
			_delta = f'(+{_delta})';
	else:
		_delta = "";
	base += f' -desc "{purse.compact_str()} {_delta}" '
else:
	desc = "";
	for x in _coins:
		index = _coins.index(x);
		_delta = delta[index];
		if _delta != 0:
			if _delta < 0:
				_delta = f'({_delta})';
			else:					
				_delta = f'(+{_delta})';
		else:
			_delta = "";
		desc += f'''{purse.coin_str(x)} {_delta}\n''';
	totalStr = "";
	_delta = round(totalGained, 3);
	if _delta != 0:
		if _delta < 0:
			_delta = f'({_delta})';
		else:				
			_delta = f'(+{_delta})';
	else:
		_delta = "";
	base += f' -desc "{desc}" -f "Total Value|{purse.compact_str()} {_delta}" '
return base + trailStr;
</drac2>