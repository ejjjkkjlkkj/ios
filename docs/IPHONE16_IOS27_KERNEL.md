# Kernelcache iPhone 16 / iOS 27.0.1

Cible exacte : iPhone 16 standard (identifiant iPhone17,3), build déclaré 24A446. Ce n'est pas l'iPhone 16 Pro (iPhone17,1), Plus (iPhone17,4) ou Pro Max (iPhone17,2).

## Récupération

Le script tools/retrieve_kernelcache.py consulte l'API de métadonnées IPSW, exige une correspondance exacte modèle/version/build, télécharge l'IPSW complet (environ 12 Go), vérifie le SHA-1 annoncé par les métadonnées, puis extrait un candidat kernelcache sans l'exécuter.

Vérifier d'abord la disponibilité sans télécharger :

```powershell
python .\tools\retrieve_kernelcache.py --metadata-only
```

Télécharger et extraire le noyau :

```powershell
python .\tools\retrieve_kernelcache.py --out "$env:TEMP\PhoneBridge-iPhone16-27.0.1"
```

Pour conserver également l'IPSW complet :

```powershell
python .\tools\retrieve_kernelcache.py --out "$env:TEMP\PhoneBridge-iPhone16-27.0.1" --keep-ipsw
```

Le fichier extrait et retrieval-report.json sont enregistrés dans le dossier de sortie. Le téléchargement complet peut utiliser environ 12 Go de données et d'espace temporaire.

## Limites de preuve

- Le checksum est celui publié par le service de métadonnées, pas une signature cryptographique Apple indépendante.
- L'extraction ne décode pas nécessairement les conteneurs IMG4/LZFSE.
- Le noyau n'est pas exécuté; aucun iPhone n'est modifié ou restauré.
- Compatibilité physique, exploit, jailbreak, SSH root et installation DEB : NOT_VALIDATED.
