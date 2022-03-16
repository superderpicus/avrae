{{a="".join(args).lower().replace(" ","") or "!"}}
{{onOff,commands,compactToggle,automaticToggle,convertCommand,help,openToggle=["Off","On"],["?","!","+","-"],a in "compact",a in "automatic",a in "convert",a in "help",1 if args and args[0] in "open" else 0}}
{{openModes=["None","One","All"]}}
{{settings=load_json(get("bagSettings",dump_json({"weightlessBags":["bag of holding","handy haversack","heward's handy haversack"],"customWeights":{},"weightTracking":"Off","openMode":"All","autoCoins":False,"compactCoins":False})))}}
{{coinsMaker=settings.update({"autoCoins":get("autocoins","0")=="1","compactCoins":get("compactcoins","0")=="1"}) if not "autoCoins" in settings else ''}}
{{viewMaker=settings.update({"openMode":"All"}) if not "openMode" in settings or not settings.openMode in openModes else ''}}
{{viewToggle=settings.update({"openMode":args[1].title() if openToggle and len(args)>1 and args[1].title() in openModes else "All"}) if openToggle else ''}}
{{openMode=openModes.index(settings.openMode)}}
{{automaticToggle and (settings.update({"autoCoins":settings.autoCoins==False}) or delete_cvar("autocoins")) or compactToggle and (settings.update({"compactCoins":settings.compactCoins==False}) or delete_cvar("compactcoins"))}}
{{set_cvar("bagSettings",dump_json(settings)) if compactToggle or automaticToggle or openToggle else ''}}
{{newPouch=[[coinPouchName,{x:0 for x in coinTypes}]]}}
{{set_cvar_nx("bags",dump_json(newPouch))}}
{{bagsLoaded=load_json(bags)}}
{{cvars=get_raw().get("cvars",{})}}
{{oldBags=[load_json(cvars[x])for x in cvars if x.strip("bag").isdigit()]}}
{{oldBagsConverted=[[x[0],{x[z].i:x[z].q for z in range(1,len(x))}]for x in oldBags]}}
{{deleter=[delete_cvar(f"bag{i}") for i in range(len(oldBags))]}}
{{bagsLoaded=bagsLoaded+oldBagsConverted}}
{{throwaway=bagsLoaded.pop(0) if oldBags and bagsLoaded[0][1]=={} else ""}}
{{pouch=([x for x in bagsLoaded if x[0]==coinPouchName] or newPouch)[0]}}
{{pouch in bagsLoaded or bagsLoaded.append(pouch)}}
{{a="?" if help else "!" if compactToggle or convertCommand or automaticToggle or openToggle else a+defaultCoin if a[-1].isdigit() else a}}

{{mode=commands.index(a[0])if a[0]in commands else 2 if a[0].isdigit()else 0}}
{{amount=int(''.join([x for x in a if x in "0123456789-"])or 0)}}
{{coinType=''.join([x for x in a[1:] if not x.isdigit()])}}
{{error=not coinType in coinTypes}}
{{error or pouch[1].update({coinType:pouch[1][coinType]+amount})}}
<drac2>
if not error:
 for coin in coinTypes[:-1]:
  larger = coinTypes[coinTypes.index(coin)+1]
  rate = int(coinRates[coin]/coinRates[larger])
  p = pouch[1][coin]//rate
  if pouch[1][coin] < 0:
   pouch[1].update({larger:pouch[1][larger]+p,coin:pouch[1][coin]-p*rate})
if settings.autoCoins or convertCommand:
 for coin in coinTypes[1:]:
  smaller = coinTypes[coinTypes.index(coin)-1]
  rate = int(coinRates[smaller]/coinRates[coin])
  p = pouch[1][smaller]//rate
  if pouch[1][smaller] >= rate:
   pouch[1].update({smaller:pouch[1][smaller]-p*rate,coin:pouch[1][coin]+p})
</drac2>
{{error=[x for x in pouch[1]if pouch[1][x]<0]}}
{{error or set_cvar("bags",dump_json(bagsLoaded))}}
{{titlePre=[" failed to take "," needs help managing ","'s "," adds "," takes out "]}}
{{titleSuf=[" from ","",""," to "," from "]}}
-title "<name>{{titlePre[0 if error else mode+1]+(f'{amount:,} '.strip('-')+coinType+titleSuf[mode+1] if amount else '')+('their ' if mode!=1 else '')+pouch[0]+'!'}}"
-desc "{{'''You lack sufficient funds to complete your request. Be glad I'm not Wells Fargo or I'd charge you money for not having money!''' if error else ((f'{sum([float(pouch[1][x]/coinRates[x]*coinRates[defaultCoin]) for x in coinTypes])} {defaultCoin}' if settings.compactCoins else '\n'.join([f'{pouch[1][x]:,} '+x for x in pouch[1]])) if openMode or mode==1 else '')if mode else '''Bag's little sister.\" -f \"Commands|`+/- # [cp/sp/ep/gp/pp]` \n adds/removes # coins. If no type is provided, the alias assumes gp. If you want to use a different standard, alter the alias to reflect that, setting `defaultCoin` to whatever you want to use. Spacing doesn't matter, `!coins +5gp` is the same as `!coins + 5 gp`.\" -f \"Additional Commands|**convert** \n Converts your lower denomination coinage to higher.\n• `!coins convert`\n\n**auto** \n Toggles automatic conversion on and off. (Disclaimer: Automatic Conversion might be faulty when using custom currencies)\n• `!coins auto`\n\n**compact** \n Toggles Compact Mode on and off. Compact Mode makes `!coins` display your wealth as one lumped value or as individual denominations.\n• `!coins compact`\n\n**open** \n Sets which bags will be opened when adding/removing items, shared setting with `!bag`.\n• `!coins open none|one|all`\" -f \"Alternative Coin Names|If your server uses alternate coinage, then modify the `coinTypes`, `coinRates`, `defaultCoin`, and `coinPouchName` in the **base** alias as appropriate for your server. Whichever denomination you set as the `defaultCoin` should also have its conversion rate set to `1` in the `coinRates`.'''}}"
{{f"-footer 'For help managing your {coinPouchName}, see !coins ?'"*(mode>0)}}
-thumb https://i.imgur.com/auM9MBe.png -color d4af37 
{{f'-f "Automatic Conversion|{onOff[settings.autoCoins]}"'*automaticToggle}}
{{f'-f "Compact Mode:|{onOff[settings.compactCoins]}"'*compactToggle}}
{{f'-f "Open Mode:|{openModes[openMode]}"'*openToggle}}