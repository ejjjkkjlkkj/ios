# PhoneBridge KernelScope — analyse IPSW

KernelScope est un outil d'inventaire statique en lecture seule. Il calcule l'empreinte SHA-256 du fichier, ouvre l'archive IPSW/ZIP, relève les manifestes plist, repère les candidats kernelcache et génère un rapport JSON. Il ne communique pas avec un iPhone, n'exécute pas le firmware, ne restaure pas l'appareil et ne teste aucun exploit.

## Exécution

Python 3.10+ (bibliothèque standard uniquement) :

```powershell
python .\tools\kernelscope.py inspect "D:\Firmware\device.ipsw" --out "$env:TEMP\PhoneBridge-KernelScope"
python -m unittest discover -s tests -p "test_kernelscope.py" -v
```

Le rapport est écrit dans `report.json`. Les chemins d'entrée doivent pointer vers un fichier IPSW obtenu légalement. L'outil n'extrait ni n'exécute le contenu de l'archive.

## Statuts

- `PASS` : opération locale indiquée exécutée avec succès.
- `FAIL` : opération locale échouée ou candidat absent.
- `PARTIAL` : métadonnées manquantes ou analyse incomplète.
- `BLOCKED` : prérequis ou capacité indisponible.
- `NOT_VALIDATED` : aucune preuve suffisante pour conclure.

## Limites de preuve

- Un nom de fichier ne confirme ni le modèle ni le build.
- Une entrée `kernelcache` est un candidat, pas une analyse du noyau décodé.
- Le SHA-256 identifie le fichier; il ne prouve pas son origine sans comparaison avec une référence officielle fiable.
- Les métadonnées IPSW ne prouvent pas la version installée sur l'iPhone.
- Les tests synthétiques prouvent uniquement le comportement de l'outil sur les données de test, pas la compatibilité iOS 27.0.1, un jailbreak, SSH root ou une installation de paquets DEB.
- La cible iPhone 16 / iOS 27.0.1 reste `NOT_VALIDATED` jusqu'à validation avec un IPSW officiel correspondant et des tests autorisés sur appareil physique.

Aucun contournement de signature, sandbox, authentification ou protection système n'est implémenté.
