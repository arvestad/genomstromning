# genomstromning
Analysera hur det går för våra studenter


## Data

Läs data från Ladok. Du behöver två utdrag från fliken "Utdata".

1. Studenter på program. Gå till "Deltagande kurspaketering".
2. Kursresultat för studenter. Gå till "Resultat" och välj tid (helst: läsår). Viktigt: 
   * Välj "Visa moduler", annars presenteras endast fullständiga kursresultat, inte partiella. 
   * Välj vilka kurser som ska visas. 
     - För NMDVK år 1 är det MM2001, MM5012, MM5013, DA2004, och DA3018.
	 - NMATK: MM2001, MM5012, MM5013, MM5016, DA2004.
	 - NMASK: MM2001, MM5012, MM5016, DA2004, MT3004.
	 - NMMLK: MM2001, MM5012, MM5013, DA2004, DA4004.
	 - För alla: MM2001, MM5012, MM5013, MM5016, DA2004, DA3018, MT3004
3. Exportera som CSV


## Användning

Se `genomstromning -h`.



## Produktion

För indata till översikt över HÅP-produktion, hämta hem en rapport (från menyn _Uppföljning_)
över _Helårsprestationer_. Välj "(403) Matematiska institutionen" i rutan _Organisationsenhet_,
"Grund och avancerad nivå" i _Utbildningstypsgrupp_, och gruppera (längst ner) efter "Kurstillfälle".
Exportera resultatet, inte underlaget.
