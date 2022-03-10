!alias aether2 embed <drac2>
aether_name = "Aether";
loaded_name = "Loaded Aether";
recovery_name = "Aether Recovery";
base = "";
ch = character();
if not ch:
	return f'''-f "Error|Character not valid.''';
fLevel = ch.levels.get("Fighter");
if not fLevel or fLevel < 3:
	return f'''-f "Error|Fighter level is not valid.''';
aether = fLevel;
loaded = min(6, aether);
ch.create_cc(aether_name, 0, aether, 'short', 'bubble', aether - loaded, None,  aether_name, "Beginning at 3rd level, you've learned how to create Aether phials which draw in magical energy from your body to charge themselves. you have a number of Aether phials equal to your level. While holding a Savageclaw you can spend these shells to fuel various Lionhart features.\n\nWhen you spend a Aether phial it is unavailable until you finish a short or long rest, at the end of which your empty phials draw the necessary magic from you.");
ch.create_cc(loaded_name, 0, loaded, 'short', 'bubble', loaded, None, loaded_name, "Your Savageclaw can only hold six Aether at a time. Once they are spent you must reload with an action before spending anymore. if you reload while you still have Aether in your cylinder you lose those Aether.");
base += f''' -title "{name} Counters Updated" -f "{aether_name} Counter Updated|{ch.cc_str(aether_name)}" -f "{loaded_name} Counter Updated|{ch.cc_str(loaded_name)}"''';
if fLevel >= 10:
	ch.create_cc(recovery_name, 0, 1, 'long', 'bubble');
	base += f''' -f "{recovery_name} Counter Updated|{ch.cc_str(recovery_name)}" ''';
return base;
</drac2>
-thumb {image} 
-color {color}