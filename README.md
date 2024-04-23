# genomstromning
Analysera hur det går för våra studenter


## Data

Läs data från Ladok. Du behöver två utdrag från fliken "Utdata".

1. Studenter på program. Gå till "Deltagande kurspaketering".
2. Kursresultat för studenter. Gå till "Resultat" och välj tid (helst: läsår). Viktigt: 
   * Välj "Visa moduler", annars presenteras endast fullständiga kursresultat, inte partiella. 
   * Välj vilka kurser som ska visas. 
     - År 1:
         - NMDVK: MM2001, MM5012, MM5013, DA2004, och DA3018/DA4006.
	 - NMATK: MM2001, MM5012, MM5013, MM5016, DA2004.
	 - NMESK: MM2001, MM5012, MM5016, DA2004, MT3004.
	 - NMMLK: MM2001, MM5012, MM5013, DA2004, DA4004.
	 - För alla:
	    + MM2001, MM5012, MM5013, MM5016
	    + DA2004, DA3018/DA4006, DA4004
	    + MT3004
     - År 2, obligatoriskt:
         - NMATK: MM5010, MT3001, MM5011, MT4001, MM5015, MT4002
	 - NMDVK: MM5010, MT3001, MT4001, MT4007, MM5015, MM5016
	 - NMESK: MM5010, MT3001, MT4001, MT3005, MM5015, MT4002, MT5018, MT5009, MT5011
	 - NMMLK: MM5010, MT3001, MT4001, MT4007, MM5015, MT4002, MT5018, DA4006
	 - För alla:
	    + MM5010, MM5011, MM5015, 
	    + MT3001, MT4001, MT4002, MT3005, MT4007, MT5009, MT5011, MT5018
	    + DA4004, DA4006
3. Exportera som CSV


## Användning

Se `genomstromning -h`.



## Produktion

Från Ladoks entresida, välj _Utdata_ i övre menyn och klick _Resultat_. 
Välj kurser att studera i väljaren _Utbildningskod_, välj resultatperiod, samt
se till att klicka i "visa moduler" (eller liknande).

Exportera slutligen till Excel.
