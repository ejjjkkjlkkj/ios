# iOS Companion — PhoneBridge

PhoneBridge vise à devenir un centre de contrôle complet de l’iPhone : applications et IPA, fichiers, diagnostics, connexion USB/réseau, rapports, accessibilité et SSH avancé lorsque l’appareil cible l’autorise.

## État réel actuel

**Prototype — NOT PRODUCTION-READY.** Le cœur Swift contient des modèles de diagnostic et de planification IPA/DEB. L’interface SwiftUI est embryonnaire. L’analyse des archives, la validation réelle de signature, le transport USB, l’installation IPA, le client SSH, les diagnostics physiques et la connexion root ne sont pas validés comme fonctions opérationnelles. Ne pas interpréter la documentation ou les modèles comme une implémentation terminée.

## Objectif : faire le maximum sur iOS

- Gestion des IPA : import, inspection, diagnostic de signature/provisioning, explication des prérequis et installation par une voie autorisée.
- Gestion des fichiers : import/export et transferts avec contrôle d’intégrité dans les limites des permissions disponibles.
- Diagnostics : collecte uniquement des informations exposées par des API publiques, rapports fournis volontairement ou interfaces autorisées.
- Compagnon Windows/macOS sans dépendance obligatoire à iTunes ou iCloud, tout en indiquant les pilotes et prérequis qui restent nécessaires.
- SSH authentifié, vérification de la clé d’hôte et transfert sécurisé.
- Mode SSH root facultatif **uniquement vers un serveur root déjà configuré et autorisé par le propriétaire**.
- Inspection DEB; installation bloquée sur iOS standard et limitée à un environnement modifié compatible, explicitement détecté et testé.
- Accessibilité VoiceOver, Dynamic Type, navigation clavier compatible et rapports explicites PASS / FAIL / PARTIAL / BLOCKED / NOT VALIDATED.
- Confidentialité : lecture seule par défaut, consentement avant partage, aucun secret dans les logs et aucune transmission cloud par défaut.

## Outil de dissection firmware (nouveau)

Le dossier Tools/firmware-audit/ contient un outil Python 3 autonome, sans dépendance tierce, qui inventorie un IPSW en lecture seule : BuildManifest.plist, version/build, modèles de produit pris en charge, chemins de kernelcache, tailles, SHA-256 et intégrité CRC de l'archive.

```sh
python Tools/firmware-audit/firmware_audit.py /chemin/firmware.ipsw --output rapport.json
python -m unittest discover -s Tools/firmware-audit -p 'test_*.py' -v
```

Cet outil ne déchiffre, ne modifie ni n'exploite le firmware. Un inventaire ne prouve ni la compatibilité avec un iPhone physique, ni l'exploitabilité du noyau. Voir le guide Tools/firmware-audit/README.md. La CI exécute les tests Swift et Python.

## Limites importantes

Une application iOS standard ne peut pas obtenir librement un shell root, activer un serveur SSH système, contourner la signature de code ou installer arbitrairement n’importe quelle application. **SSH root sans jailbreak n’est possible que si l’appareil dispose déjà d’un service root autorisé**; l’application ne peut pas créer ce privilège. Les installations IPA restent dépendantes de méthodes de signature/distribution compatibles. Les fichiers DEB ne sont pas des applications installables normalement sur iOS standard.

## Documentation

- [Vision produit et critères de validation](docs/PRODUCT_SCOPE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Flux IPA/DEB](docs/IPA_DEB_WORKFLOWS.md)
- [SSH et accès root](docs/SSH_STOCK_IOS.md)
- [Compatibilité iOS 27.0.1](docs/IOS_COMPATIBILITY.md)

## Build du cœur Swift

Nécessite Swift 6 :

```sh
swift test
```

Aucun résultat de test n’est revendiqué ici sans exécution et preuve. Les tests unitaires ne prouvent pas le fonctionnement sur un iPhone physique.

## Cible iOS 27.0.1

iOS 27.0.1 est la cible déclarée, **pas une compatibilité validée**. Le projet doit encore être compilé avec un SDK compatible, puis testé sur appareil physique. Le package déclare actuellement iOS 17 comme version minimale; cela ne prouve pas la compatibilité avec iOS 27.0.1.
