# Cours drone

## Sujet

**Sujet:** Réalisation d’un parcours de surveillances par drone, entre l’embarcadère de Royan et le phare de Royan

**Développeurs:** Peter BALIVET & Baptiste DEMARCHE

**Classe:** ESGI-4SI2

**Date:** 25/07/2022

## Documentation

### Installation du simulateur

- Cloner le repertoire :

```bash
git clone https://github.com/ArduPilot/ardupilot --recursive
```

- Builder le container docker

```bash
cd ardupilot
docker build . -t ardupilot
```

### Utiliser le simulateur

- Lancer le container docker

```bash
docker run --rm -it --net=host -v `pwd`:/ardupilot ardupilot:latest bash
```

```bash
cd ArduCopter
../Tools/autotest/sim_vehicle.py --out=VOTRE_IP:14550 -L Royan
```
