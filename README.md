# Cours drone

## Installation du simulateur

- Cloner le repertoire : 

```
git clone https://github.com/ArduPilot/ardupilot --recursive
```

- Builder le container docker

```
cd ardupilot
docker build . -t ardupilot
```

## Utiliser le simulateur

- Lancer le container docker

```
docker run --rm -it --net=host -v `pwd`:/ardupilot ardupilot:latest bash
```

```
cd ArduCopter
../Tools/autotest/sim_vehicle.py --out=VOTRE_IP:14550
```