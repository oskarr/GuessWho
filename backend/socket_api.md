# Socket-API:t

Mycket av kommunkationen görs av sockets.

## Rumsanslutning
Vid rumsanslutning skickar klienten tre meddelanden till servern:
* `update_user` specificerar användarnamn och lag, från cookies (HTTP-servern som servar `room.html` känner inte till socket-id:t `sid`, så detta måste göras via sockets).
* `joinroom` - Gör att användaren går med i rummet, vars id beräknats från URL:en.
* `get_characters` - efterfrågar alla characters.

**Klienten får följande svar:**
På `joinroom`:
* `room` - Innehåller information om det gick bra att gå med i rummet.
* `reply` - Servern skickar alla tidigare meddelanden till klienten.

På `get_characters`:
* `characters` - innehåller alla karaktärer för det egna laget i `all`, och alla för motståndarlaget i `opponent`. `self` är den egna karaktären, eller False, om sådan ej finns.