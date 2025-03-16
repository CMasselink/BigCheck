# BigCheck
Checkt of iemand in het BIG register staat, of iemand eventueel geschrapt is of dat er beperkingen zijn opgelegd.
Indien er bevindingen zijn, worden de namen en BIG nummers van deze personen weggeschreven in checklist.csv. 
Voor iedere persoon in checklist.csv is er dus een bevinding gedaan. Mogeijke bevindingen:
- Persoon komt niet voor in BIG register
- Persoon is definitief geschrapt uit het BIG register of heeft inschrijving niet verlengd
- Persoon is voorwaardelijk geschorst of heeft beperkingen opgelegd gekregen

# Werking
Zet een csv bestand genaamd test.csv in dezelfde directory als het python script.
Alternatief: geef de naam van het csv bestand met de te checken personen mee als commandline parameter. Indien er geen parameter meegegeven wordt, gaat het script uit van een bestand met de naam test.csv.  
Vul het CSV bestand met te controleren medewerkers met het volgende formaat: achternaam;bigregistratienummer.
Gebruik geen kolomkoppen.

# Afhankelijkheden
Het script maakt gebruik van het externe package zeep voor het aanroepen van de SOAP service. 
Zie https://docs.python-zeep.org/en/master/index.html voor documentatie. zeep kan via PIP geïnstalleerd worden.
