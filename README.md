# Gissa vem
En digital kopia av spelet "vem där" (som jag trodde hette gissa vem när jag skrev detta).

## Bakgrund
Jag skrev detta efter att jag och några vänner satt på Discord och tänkte att det vore kul att ha spelet "vem där", fast med egna bilder, efter att vi spelat [Scribbl](https://scribbl.io) med egenvalda ord.

## Arkitektur
Frontend är skrivet med [Vue.js](https://vuejs.org/), [https://socket.io/](https://socket.io/) och [Bulma.css](https://bulma.io/). I mappen `frontend`, respektive `frontend/app` finns filer med namn `index` och `app`. Index är start- och uppladdningssidan, medan `app` är själva spelplanen. Koden är tyvärr lite dåligt kommenterad, då jag inte tänkte att någon annan än jag skulle läsa det här, but here we are, och jag tänker att du som läser detta förtjänar en rättvis bild av hur min kod ser ut.

Backend är skrivet i Python 3 med python-socketio, och består av följande filer:
* `game.py` - En klass för varje spelplan/rum.
* `oragnizer.py` - Håller koll på vilka rum användare är i, och vilka rum som finns osv.
* `server.py` - Hanterar vanliga HTTP-requests.
* `sockethandler.py` - Hanterar socketio-requests.

## Saker jag kanske borde ändrat på
Till att börja med bör det nämnas att det här är det första jag gör med både Vue.js och Socket.io, så det finns en hel del saker som jag skulle göra om, om jag skulle skriva om allt från grunden. Det handlar kanske främst om att Socket.io har abstraktioner som skulle kunna göra "rumindelningen" mycket enklare. Det hade nog varit bra att använda någon sorts databas för att associera spelare med rum och lag osv., och användningen av cookies för att spara lag- och användarnamn är inte optimal, men det funkar. 

## Data
### Bilder
Bilderna är genererade av Nvidia:s nätverk stylegan2 ([GitHub](https://github.com/NVlabs/stylegan2)). De är alltså inte av riktiga personer.

### Namn
Namnen är tagna direkt från [SCB](https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__BE__BE0001__BE0001D/BE0001Nyfodda/), år 2014-2019.
