embed <drac2>
args = argparse(&ARGS&); #parsed arguments
_args = &ARGS&; #raw arguments
ch = character(); #save character to a variable 
_argsJoined = " ".join(_args).lower(); #used for single coins mode
if not ch: #character not found, so we can't do anything
	err("You do not have a valid character");
#save variables to save resources
purse = ch.coinpurse; 
startCoins = purse.get_coins();
compactMode = get("coinscompact", "0"); #try to get cvar, default to 0
autoMode = get("coinsauto", "0"); #try to get cvar, default to 0
imported = get("coinsimported", "0"); #try to get cvar, default to 0
mode = get("coinsmode", "0"); #try to get cvar, default to 0
electrum = get("coinselectrum", "1"); #try to get cvar, default to 1
_coins = ["pp", "gp", "ep", "sp", "cp"]; #used for indexing and checking if suffix is valid
delta = [0, 0, 0, 0, 0]; #delta = change, instead of multiple addition and subtractions we add to delta, and do 1 big shift later
base = f' -thumb "https://i.imgur.com/auM9MBe.png" -color "#d4af37" -title "{name}\\\'s Coinpurse" '; trailStr = ""; #base and trail string that we will add onto
if (imported == "0" and purse.total == 0) or ("import" in args): #if not imported and value is 0, import automatically. also can force import with command
	_forceImport = f'import {name.lower()}' in _argsJoined; #we need to check if they are SURE they want to import again
	if "import" in args and imported == "1" and (not _forceImport): #do not import the coins, until they force it
		trailStr += f' -f "Coins Not Imported|Your coins were already imported previously from the bags alias. If you want to import again, type `!coins import {name.lower()}`." ';
	else: #import the coins now
		ch.set_cvar("coinsimported", "1"); #set import cvar to 1 to prevent future imports
		bags = load_json(get('bags', '[]')) 
		bagsDict = {bag: items for bag, items in bags}
		coins = bagsDict.get('Coin Pouch');
		if coins:
			#coins from bag alias are valid, add them to the delta
			delta[0] = coins.pp; delta[1] = coins.gp; delta[2] = coins.ep; delta[3] = coins.sp; delta[4] = coins.cp;
			trailStr += f' -f "Coins Imported|Your coins were imported from the bags alias." '; #trail string is just info to add at the end
if "compact" in args: #compact mode toggled:
	ch.set_cvar("coinscompact", "1" if compactMode == "0" else "0") ;
	trailStr += f' -f "Compact Mode:|{"On" if get("coinscompact") == "1" else "Off"}" '
	compactMode = get("coinscompact", "0");
if "auto" in args: #auto mode toggled
	ch.set_cvar("coinsauto", "1" if autoMode == "0" else "0") ;
	trailStr += f' -f "Automatic Conversion:|{"On" if get("coinsauto") == "1" else "Off"}" '
	autoMode = get("coinsauto", "0");
if "mode" in args: #coins mode toggled between single and multi
	ch.set_cvar("coinsmode", "1" if mode == "0" else "0") ;
	trailStr += f' -f "Coin Mode:|{"Multi" if get("coinsmode") == "1" else "Single"}" '
	autoMode = get("coinsmode", "0");
if "electrum" in args: #electrum mode toggled
	ch.set_cvar("coinselectrum", "1" if electrum == "0" else "0") ;
	trailStr += f' -f "Electrum:|{"Shown" if get("coinselectrum") == "1" else "Hidden"}" '
	electrum = get("coinselectrum", "0");
if f'wipe {name.lower()}' in _argsJoined: #wipe mode (forced)
	trailStr += f' -f "Wipe:|Coins wiped." '
	purse.set_coins(0, 0, 0, 0, 0);
elif "wipe" in args: #wipe (not forced) found
	trailStr += f' -f "Wipe:|Are you sure you want to wipe your coins? If you are sure, type `!coins wipe {name.lower()}` to empty your coins." '
#help instructions
if "help" in args:
	base += f' -title "!coins help" -desc "**Usage of coins alias**:\n`!coins [args]`\n\n**Supported Arguments**:\n`help` help command\n`compact` enable compact mode, showing only the total gp value of your wallet\n`auto` enable automatic conversion to the highest level coins\n`mode` change mode of parsing, from multiple coins per line, to one line, which allows spaces\n`import` import coins from the old coins alias (this is automatically done if you have an empty coin purse)\n`wipe` empty your coin purse\n`electrum` hide electrum coins because nobody likes them\n\n**Examples**:\n`!coins +5gp`\n`!coins 50`\n`!coins -5sp +10gp` (in multi mode)\n`!coins + 20 sp` (in single mode)\n\n[(shitty) source code](https://github.com/superderpicus/avrae/blob/main/coins.py)" ';
	base += trailStr;
	return base;
#multi coin mode
if mode == "1":
	for a in _args: #iterate each argument (presumably each a coin)
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
		if (electrum == "0" and x != "ep") or electrum == "1":
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