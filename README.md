# Sensool
Projet de fin d'étude du Groupe 22 - Sensool (ECE Paris)

L'équipe est composée de :
- Gaultier JOUSSELIN (chef de projet)
- Jérôme DELTOUR
- Baptiste PILLET 
- Louis GERMANICUS
- Pierre BALLAND
- Paul BAZIN

## Objectif du projet
Notre projet a pour but d'utiliser des capteurs connectés à un ESP32 qui transmet à AWS, via AWS Greengrass IoT sur une Raspberry Pi, les données reçues par ceux-ci.
Ces données sont ensuite traitées et en fonction de celles-ci un actionneur déclenche un servomoteur qui pourrait augmenter la l'humidité par exemple.

### Les composants
La liste des composants que nous avons utilisées est la suivante :
- capteur de température : DS18B20 étanche
- capteur d'humidité et de température : DHT11
- nano-ordinateur : Raspberry Pi 3
- microcontroleur utilisant le Bluetooth : ESP32 BLE Wifi Kit

### La documentation AWS
Nous avons commencé par suivre la documentation AWS afin d'installer AWS IoT Greengrass sur la Raspberry Pi avec les instructions [suivantes](https://docs.aws.amazon.com/fr_fr/greengrass/latest/developerguide/what-is-gg.html).
La partie de la documentation AWS concernant la Raspberry Pi ([ici](https://docs.aws.amazon.com/fr_fr/greengrass/latest/developerguide/setup-filter.rpi.html)), permet de la configurer afin de l'utiliser en tant que AWS IoT Greengrass Core comme les commandes suivantes.
```bash
cgroup_enable=memory cgroup_memory=1
sudo apt install openjdk-8-jdk
```
### Les abonnements
Depuis le code Python qui se trouve dans le dossier Raspberry_local_scripts/ESP32_to_lambda.py, nous envoyons les données, qui sont représentés par newdata ci-dessous, vers AWS qui les reçois dans le `topic` qui a été nommé `esp1/temp`.
```python
DHT_MQTTClient.publish(topic, newdata, 0)
```

### Le Json
Les données envoyées depuis l'ESP32 sont sous la forme de fichier Json qui facilitent l'attribution de données aux différents valeurs. Elles sont reçu sur le topic `esp1/temp` sous cette forme :
```Json
{
  "humidity_DHT11": 43,
  "temperatureC_Dallas": 18.62,
  "temperatureF_Dallas": 65.53,
  "time": 1611573870,
  "table": "conteneur1"
}
```

### Fonctions Lamba 
Les fonctions Lambda dans notre projet nous permettent de faire communiquer les requêtes MQTT afin de recevoir les données de température reçu sur la rebrique d'abonnement `esp1/temp` reçu sous format Json et des la fonction greengrass_function.py qui se trouve dans le dossier AWS_lambda_scripts/Main_logical_lambda.

### Timestream
Pour utiliser timestream, connectez vous sur https://us-east-2.console.aws.amazon.com/timestream avec vos identifiant AWS.
Créez une base nommé `Sensool`.


### Contactez-nous !
Vous pouvez nous contacter via l'adresse mail suivante : sensool22@gmail.com
