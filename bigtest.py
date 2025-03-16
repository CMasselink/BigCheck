import zeep
import time
from pathlib import Path

def performBigCheck(naam, bignummer):
    """Haalt de BIG data op en checkt of er sprake is van een schorsing of andere beperkingen."""
    bignummer = str(bignummer).replace("\n", "")
    wsdl = 'https://api.bigregister.nl/zksrv/soap/4?wsdl'
    client = zeep.Client(wsdl=wsdl)
    data = client.service.ListHcpApprox4('Name', naam, RegistrationNumber=bignummer)
    if data is not None:
        achternaam = data[0]['BirthSurname']
        mailingname = data[0]['MailingName']
        einddatum = str(data[0]['ArticleRegistration']['ArticleRegistrationExtApp'][0]['ArticleRegistrationEndDate'])
        maatregel = data[0]['JudgmentProvision']
        fouteDatum = '0002-01-01 00:00:00' # indien iemand permanent geschrapt is, wordt de de einddatum op deze waarde gezet
        
        if einddatum == fouteDatum: # als deze conditie waar is, betekent dit dat de medewerker definitief geschorst is en dus zijn/haar beroep niet meer mag uitoefenen 
            print(mailingname, 'met bignummer:', bignummer,'is geschrapt!')
            naughtylist.append(achternaam + ";" + str(bignummer))
        if (maatregel is not None) and (einddatum != fouteDatum): # als aan deze condities wordt voldaan, betekent dit dat de medewerker voorlopig geschorst is of beperkingen opgelegd heeft gekregen
            maatregelEindatum = maatregel['JudgmentProvisionExtApp'][0]['EndDate']
            maatregelToelichting = maatregel['JudgmentProvisionExtApp'][0]['PublicDescription']
            print(mailingname, 'met bignummer:', bignummer, 'is  voorlopig geschorst of er is een beperking opgelegd')
            print('De schorsing loopt tot:', maatregelEindatum)
            print('De volgende maatregelen, voorwaarden en redenen voor schorsing zijn benoemd:','\n' ,maatregelToelichting)
            naughtylist.append(achternaam + ';' + bignummer + ';' + str(maatregelEindatum))
        if(maatregel is None) and (einddatum != fouteDatum): # geen bijzonderheden gevonden, niks aan de hand.
            print(mailingname, 'met bignummer:', str(bignummer), 'is niks mee aan de hand!')
        print('\n')
    else: # De combinatie van naam & BIG nummer horen niet bij elkaar. Persoon staat niet in het BIG register met opgegeven gegevens.
        print(naam, 'staat niet in het BIG register met het opgegeven nummer!') 
        naughtylist.append(naam + ';' + str(bignummer))

def procesCSV(file):
    """Leest een CSV bestand uit waar de naam en BIG nummer van de te controleren personen in staan. CSV bestand moet in zelfde directory staan als script."""
    p = Path(__file__).with_name(file)
    with p.open('r') as f:
        for x in f:
            persoon = x.split(";")
            performBigCheck(str(persoon[0]), persoon[1])
            time.sleep(2)

# Lijst waar medewerkers aan toegevoegd worden als ze geschorst of voorlopig geschorst zijn.
naughtylist = []
procesCSV('test.csv')

#Indien er medewerkers in de naughtylist staan, lijst wegschrijven naar een CSV zodat medewerker kan controleren.
if len(naughtylist) > 0:
    with open('checklist.csv', 'w') as f:
        for line in naughtylist:
            f.write(f"{line}\n")
