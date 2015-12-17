# GeoHashCache
Geohashing Augmented Geocaching

## General Proposal:
Geocaching usually refers to the internet "sport" of venturing out into the world in search of objects (called "Caches") hidden by other geogachers. The clues to finding these are usually a set of vague GPS coordinates as well as some sort of riddle, puzzle, map or challenge. These can vary from finding a particular tree to look under, to hacking a simulated wifi-network to get the actual set of coordinates. However, there's a finite number of unmoving caches in traditional geocaching, which means dedicated geocachers can potentially find *every* cache in their area which would leave them with nothing to do.

Therefore, we propose a geohash-augmented form of geocaching. Geohashing uses a combination of inputs including GPS coordinates, the date, the daily stock market stats and other data to generate new GPS coordinates. These coordinates can be confined to a certain range or area. Our idea is to make use of a Geohash to generate new coordinates for a cache once it is found. When a geocacher finds a geohashcash, the website generates a new coordinate in their area for them to relocate the cache to. They can produce a new riddle of challenge for the cache when they do this, and it gets updated. This would allow for geocachers who live in areas with very few caches to still keep finding caches because the caches are moved everytime someone finds one. The same cache could be on the empire state building today and end up in a pizzaria in tribeca tomorrow. 

## Additional Sub-Proposal:
* We'd like to include the option to generate QR codes for caches, allowing for users to indicate they've found a cache using a QR code scanner. 
* We'd like to include googlemaps integration to show caches in your area, which would update as they move.
* We'd like to include the option to comment on caches (also declare if a cache has been damaged or lost).

## Technical Proposal:
* A NoSQL database will be used to to keep track of caches, users, and comments. 
* Caches will each have a public and a secret ID. The public ID will be used as the cache's webpage link, while the private ID will be used to validate (or prove) that a user has found a cache. 
  * QR codes will contain both IDs, making it possible to log a cache quickly using a QR code scanner.
* BitAverage's Bitcoin-Tracker-API, the current date, and the user's location will be used to GeoHash new coordinates for caches that have been found. 
  * A MD5 hash will act as the actual hash, and coordinates will be limited to a certain degree of precision.
    * Limiting the precision serves to limit the issues with inaccuracy that most GPS have.
* Google's GoogleMaps API will be used to show a map of local caches around the user.
  * The map will update as caches move, and will ignore caches that have been reported as damaged or lost.
  * HTML5 will be used to automatically get the user's location to show caches around them.
* A comment system will allow users to show support for well-made caches, and report fake, lost, or damaged caches.
  * Lost or Damaged caches will not show up on map results until they are repaired.
* Users will have individual accounts used for commenting that will allow them to track which caches they have found, or what caches they have created.

#

| | Name | Job | Github |
| ------------- | ------------- | ------------- | ------------- |
| |Shawn Li | Front-End, Middle Ware | [Link](https://github.com/TyranitarShawn) |
| | Albert Mokrejs | Back End | [Link](https://github.com/AlbertMokrejs) |
| | Samuel Zhang | Middle Ware | [Link](https://github.com/codesammich) | 
