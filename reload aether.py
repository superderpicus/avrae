!alias reload embed <drac2>
aether_name = "Aether";
loaded_name = "Loaded Aether";
ch = character();
if not ch:
	return f'''-f "Error|Character not valid.''';
fLevel = ch.levels.get("Fighter");
if not fLevel or fLevel < 3:
	return f'''-f "Error|Fighter level is not valid.''';
if not ch.cc_exists(aether_name) or not ch.cc_exists(loaded_name):
	return f'''-f "Error|Custom counters not found. Use !Aether to create them and update them on level up."'''
loaded = ch.get_cc(loaded_name);
current = ch.get_cc(aether_name);
if (current <= 0):
	return f'''-f "Cannot Reload Aether|Not enough Aether remaining to reload."'''
diff = min(6, current);
ch.mod_cc(loaded_name, -loaded); # set loaded to 0, removing all the aether
lost_aether = loaded;
msg = "";
if lost_aether > 0:
	msg = f'''Wasted {lost_aether} Aether.''';
ch.mod_cc(loaded_name, diff);
ch.mod_cc(aether_name, -diff);
return f'''-f "{name} reloads their Aether!|Your Savageclaw can only hold six Aether at a time. Once they are spent you must reload with an action before spending anymore. if you reload while you still have Aether in your cylinder you lose those Aether." -f "Aether|Aether: {ch.cc_str(aether_name)} (-{diff})\nLoaded Aether: {ch.cc_str(loaded_name)} (+{diff}) {msg}"'''
</drac2>
-thumb {image} 
-color {color}