# CERT-SE CTF 2025 



### Nätverksanalys  
- **Wireshark**: Primära PCAP-analysverktyget (min nya bästa vän)
- **Python**: Anpassade script för dataextraktion och dekodning
- **CyberChef**: Base64-dekodning och datamanipulation (livräddare!)

### Kryptografi & Kodning
- **LZ4-dekomprimering**: Firefox session store-analys  
- **Base64-dekodning**: UDP-strömrekonstruktion
- **Positionell kodning**: URL endpoint-dekodning
- **Modulär aritmetik**: HTML steganografi-dekodning

### Filanalys & Forensik
- **Binwalk**: Extrahering av filer från diskavbilder (`sudo binwalk -e --run-as=root`)
- **Hex-redigerare**: Binärfilsundersökning
- **Bildanalysverktyg**: Steganografidetektering  
- **GIMP**: Transparency-experiment (spoiler: funkade inte)

### Ljudanalys (RIP Mina Öron)
- **Sonic Visualizer**: För att se varför mina eardrums nästan sprängdes
- **Ljudredigeringshemsidor**: För att ta bort det dödande beep-ljudet
- **AI-konsultation**: För att identifiera MP3-filer från konstiga filnamn
- **Reverse playback**: För att höra bakåtspelat ljudl (`cert-se_ctf2025.pcap`) med olika forensiska tekniker. Spoiler alert: det blev mycket Wireshark, Python-scripting och "varför fungerar inte det här?!"-moment.

## Flagga 1: UDP Keylogger - ctf[keylog_over_udp]

### Upptäcktsprocess
1. **Extraherade** pcap-filen från arkivet (första steget - check!)
2. **Öppnade** med Wireshark för nätverkstrafikanalys  
3. **Kollade igenom** UDP-strömmar, filtrerade bort DNS-trafik
4. **Insåg** att datan i varje UDP-paket var Base64-kodad (aha-moment!)
5. **Skrev Python-script** (`analys.py`) som:
   - Tar alla UDP-paket som inte är DNS
   - Dekodar Base64-data från varje paket
   - Rekonstruerar det dolda meddelandet

### Tekniska detaljer
- UDP-paket innehöll fragmenterad Base64-kodad data
- Scriptet processade automatiskt paketlaster och dekodade innehållet
- Första flaggan visade sig vara en keylogger över UDP (smart!)

### Flagga: `ctf[keylog_over_udp]`

## Flagga 2: Nessies Firefox-flikar - ctf[resurrection]

### Upptäcktsprocess
1. **Följde TCP Stream 8 (SMTP)** och hittade mejl från hdesk till Nessie:
   ```
   Dear Nessie! I have recovered your beloved tabs and you should be able to resume your work, 
   whatever you are doing. See attachment and follow the guide I gave to you by the dock earlier today.
   
   from hdesk to nessie
   ```

2. **I mejlet** ser jag en bifogad fil: `sessionstore.jsonlz4`
3. **Efter några sökningar** på nätet såg jag att det är en LZ4-komprimerad JSON-fil som Firefox använder för backup
4. **Extraktionsprocess**:
   - Tog hela Base64-koden och dekodade i CyberChef
   - Laddade ner det som `.jsonlz4`-fil  
   - Dekomprimerade med LZ4 och sparade innehållet som `sessionstore.json`

5. **Analys av sessiondata**:
   - Där ser man alla flikar som Nessie hade öppna
   - Upptäckte något konstigt i URL:erna på några flikar
   - Nessie hade besökt cert.se men endpointerna såg suspekta ut

6. **Python-script för att samla endpoints**:
   - Samlade alla endpoints och printade ut: `16n4[2t13t1c3f17]12c5r6e8u11e15o7s9r10r14i`
   - Efter några försök fattade jag att detta var positionell kodning!

### Dekodningsmetod
- Siffror indikerade teckenpositioner  
- Arrangerade om tecken enligt position för att avslöja flaggan
- Mönster: `[position][tecken]`-par

### Flagga: `ctf[resurrection]`

## Flagga 3: MSB-bilden (TCP Stream 9) - Status: Pågående Huvudbry

### Upptäcktsprocess
1. **TCP Stream 9** - såg direkt att det handlade om en bild
2. **Extraherade JPG-bilden** från Wireshark paketdata
3. **Visuell analys visade**:
   - MSB (Myndigheten för samhällsskydd och beredskap) logga
   - Text "CTF[" följt av 15 RGB-färgade kvadrater  
   - Bilddimensioner: 2871x828 pixlar

### Steganografi-försök (AKA "Varför fungerar inget?!")
- Testade LSB steganografi - nada
- Ändrade transparency i GIMP - ingen lycka
- Kollade hexdump - inget vettigt där heller
- 15 färgade kvadrater antyder RGB-färgkodning
- Varje kvadrat representerar förmodligen kodad data

### Status: Frustrerad men inte besegrad
Behöver ytterligare analys för att dekoda RGB-färgvärdena. Kommer tillbaka till denna!

## Flagga 4: SD-kortet och Binwalk-äventyret (Stream 10)

### Upptäcktsprocess  
1. **Ytterligare mejl** från m.a.wetherelle till Nessie (stream 10)
2. **Innehåll**: "Funnet SD-kort"
3. **Bifogad**: `PHOTOS.img` - diskavbildningsfil

### Forensisk analys med Binwalk
```bash
sudo binwalk -e Photos.img --run-as=root
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
61440         0xF000          PNG image, 819 x 1227, 8-bit/color RGBA, non-interlaced
61481         0xF029          Zlib compressed data, default compression
1982464       0x1E4000        PNG image, 819 x 1227, 8-bit/color RGBA, non-interlaced
1982616       0x1E4098        Zlib compressed data, default compression
4315136       0x41D800        PNG image, 819 x 1227, 8-bit/color RGBA, non-interlaced
4315288       0x41D898        Zlib compressed data, default compression
6201344       0x5EA000        PNG image, 819 x 1227, 8-bit/color RGBA, non-interlaced
8198144       0x7D1800        PNG image, 851 x 1275, 8-bit/color RGBA, non-interlaced
8198185       0x7D1829        Zlib compressed data, default compression
9164769       0x8BD7E1        MySQL MISAM compressed data file Version 10
```

### Fynd
- **5 PNG-bilder** extraherade
- **MySQL MISAM data** upptäckt (försökte extrahera men... another time)
- Bilderna innehåller monster fish och dinosaurier med långa halsar - ledtråd till senare!

## Flagga 5 & 6: FTP Dubbel-Whammy! 

### Upptäcktsprocess (FTP Stream)
1. **Analyserade FTP-stream** - hittade lösenordshash och två filer
2. **Överförda filer**:
   - `ctf.txt`: "Ctf[ De två sista ord i 4e meningen]", nice! 
   - `passwd_policy.txt`: Lösenordet måste vara från rockyou.txt i ctf[]-format

### Lösningsmetod
**För ctf.txt flaggan:**
- Identifierade referenstexten och extraherade 4:e meningen
- Hittade de två sista orden
- **Flagga 5: `ctf[aguess]`** (De två sista orden i 4:e meningen)

**För lösenordspolicyn:**  
- Såg att lösenordet skulle vara från rockyou.txt
- Då var det dags för bruteforce mot hashen jag hittade!
- Därefter kunde jag hitta en match
- **Flagga 6: `ctf[cutenessie4eva]`** (Aww, Nessie är ju söt!)

## Flagga 7: HTML Steganografi (index.html) - Status: Pågående Knäckande

### Upptäcktsprocess
1. **Hittade GET request** för `index.html` i TCP-streams (efter FTP-äventyret)
2. **Extraherade HTML-fil** innehållande 4096 span-element  
3. **Analys visade**:
   - 1471 spans med `lightgreen` bakgrundsfärg
   - CSS-selektorer som använder `nth-of-type()` för specifika positioner
   - Titel: "The sky above the port was the color of television, tuned to a dead channel" (Neuromancer-referens!)

### Teknisk lösning (Work in Progress)
1. **Extraherade markerade span-positioner** med regex pattern matching
2. **Binär konvertering**: Skapade 4096-bitars sträng (64x64 rutnät)
   - Markerade spans = 1  
   - Normala spans = 0
3. **Dekodningsförsök**:
   - Modulär aritmetik (mod 95 + 32) på span-nummer
   - Mönsterigenkänning i dekodad ASCII
   - Flaggformatsdetektion med klammerparenteser

### Utvecklade Script
- `extract_selectors.py`: Extrahera CSS-selektorer och konvertera till rutnät
- `span.py`: Konvertera span-positioner till binär kodning
- `decode_binary.py`: Flera dekodningsmetoder
- `flag_search.py`: Systematisk flaggmönsterdetektion

### Status: "Nästan där!"
Flera potentiella flaggmönster identifierade. Sen gick jag vidare till en annan HTTP request som skedde... (fortsättning följer)

## Flagga 7: Det Dövande IGUANASAURUS-äventyret - ctf[I G U A N A S A U R U S]

### Upptäcktsprocess (AKA "Hur Jag Nästan Förstörde Mina Hörsel")

1. **HTTP request för `monstrum_piscis_tres`** - consultade min AI vän som sa det var en MP3-fil
2. **Ljudanalys som nästan dödade mig**:
   - Laddade ner filen och spelade upp
   - JÄTTEHÖGT BEEEEP-ljud som nästan sprängde mina eardrums! 
   - Blev nästan sound engineer för att ta bort det helveteslljudet

3. **Sonic Visualizer till räddning**:
   - Kunde se varför jag nästan sprängde hörseln
   - Upptäckte att ljudet var **reversed**!
   - Började höra att det lät som bokstäver som uttalades

4. **Ljud-restoration mission**:
   - Hittade någon hemsida som kunde ta bort det höga pipet
   - Gjorde det ohörbart (tror jag, haha!)
   - Kunde äntligen höra: `ctf[i n a e n i u g a s a u u s a a]`

### Pussel-lösning och Eureka-moment
- **Monstrum_piscis_tres** = "monster fish three" (latin)
- **IMG-bilderna** visade dinosaurier med långa halsar
- **Koppling**: `I G U A N A S A U R U S` - en dinosaurie med lång hals!
- **"I am reaching boiii"** 

### Flagga: `ctf[I G U A N A S A U R U S]`, 


*PS: Nessie verkar vara en riktigt intressant karaktär. Hoppas hans hörsel är bättre än min efter MP3-incidenten!* 🦕🔊

---

## Slutreflektion

CTF:en var designad för **10 flaggor totalt**. Jag har möjligtvis hittat **5 av dessa**, med flera pågående analyser som kunde vara de återstående flaggorna. 
