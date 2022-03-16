!alias coins2 embed <drac2>
args = argparse(&ARGS&); #args passed to alias (compact, +xgp, -xsp)
_args = &ARGS&; #raw args to get money changes
ch = character(); #character var
if not ch:
	err("You do not have a valid character");
purse = ch.coinpurse; #coinpurse
startCoins = purse.get_coins(); # save the coins we have now, to use later
compactMode = get("coinscompact", "0");
autoMode = get("coinsauto", "0");

_coins = ["pp", "gp", "ep", "sp", "cp"];
delta = [0, 0, 0, 0, 0];
base = f' -thumb "https://i.imgur.com/auM9MBe.png" -color "#d4af37" -title "{name}\'s Coinpurse" '; #set the picture and colour
trailStr = ""; #string that will be appended at the end
nLine = '\n';

#check if compact was passed in args
if "compact" in args:
	# compact mode toggled
	if (not compactMode) or (compactMode == "0"):
		# compact mode should be toggled ON
		ch.set_cvar("coinscompact", "1") ;
		trailStr = f' -f "Compact Mode:|On" '
	else:
		# compact mode should be toggled OFF
		ch.set_cvar("coinscompact", "0");
		trailStr = f' -f "Compact Mode:|Off" '
	compactMode = get("coinscompact", "0"); # update compact variable if it was changed

#check if auto was passed in args
if "auto" in args:
	# auto mode toggled
	if (not autoMode) or (autoMode == "0"):
		# auto mode should be toggled ON
		ch.set_cvar("coinsauto", "1") ;
		trailStr = f' -f "Automatic Conversion:|On" '
	else:
		# auto mode should be toggled OFF
		ch.set_cvar("coinsauto", "0");
		trailStr = f' -f "Automatic Conversion:|Off" '
	autoMode = get("coinsauto", "0"); # update auto variable if it was changed

# check the raw args for money commands
for a in _args:
	if a != "":
		size = len(a); #size of the string for subbing later
		if a.isnumeric() or a[1:].isnumeric():
			#if arg is all a number, add the coins
			delta[1] += int(a); #default to GP
		elif a != "" and any(char.isdigit() for char in a):
			# has a number in it, try to parse it
			#first letter of string is + or a number, meaning we add coins
			amt = a[0:size-2];suf = a[size-2:size];index = 0;
			if suf in _coins:
				index = _coins.index(suf);
			else:
				err(f'Invalid coin type: `{suf}` passed in arguments.');
			delta[index] += int(amt);

#modify coins with the delta we got
for x in range(5):
	if ((startCoins[_coins[x]]) + delta[x] < 0):
		err(f'You do not have enough `{_coins[x]} to do that.')
#use built in function
purse.modify_coins(delta[0],delta[1],delta[2],delta[3],delta[4],autoMode);
totalGained = purse.total - startCoins.total;

#if automode is enabled, then automatically convert the coins
if autoMode == "1":
	purse.autoconvert();

#if compact mode is enabled, the coin string should be compact
if compactMode == "1":
	_delta = totalGained;
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
	_delta = totalGained;
	if _delta != 0:
		if _delta < 0:
			_delta = f'({_delta})';
		else:				
			_delta = f'(+{_delta})';
	else:
		_delta = "";
	base += f' -desc "{desc}" -f "Total Value|:DDBGold: {purse.total} {_delta} gp" '

return base + trailStr;
</drac2>