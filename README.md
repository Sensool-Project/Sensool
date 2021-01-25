# Sensool
Projet de fin d'étude du Groupe 22 - Sensool (ECE Paris)

L'équipe est composée de :
- Gaultier JOUSSELIN (chef de projet)
- Jérôme DELTOUR
- Baptiste PILLET 
- Louis GERMANICUS
- Pierre BALLAND
- Paul BAZIN

### Objectif du projet
Notre projet a pour but d'utiliser des capteurs connectés à un ESP32 qui transmet à AWS, via AWS Greengrass IoT sur une Raspberry Pi, les données reçues par ceux-ci.
Ces données sont ensuite traitées et en fonction de celles-ci un actionneur pourrait augmenter la l'humidité par exemple.

### Les composants
La liste des composants que nous avons utilisées est la suivante :
- DS18B20 étanche
- DHT11
- Raspberry Pi 3
- ESP32

### Timestream
Pour utiliser timestream, connectez vous sur https://us-east-2.console.aws.amazon.com/timestream avec vos identifiant aws.
Créez une base nommé "Sensool".


## Contactez-nous !
Vous pouvez nous contacter via l'adresse mail suivante : sensool22@gmail.com
