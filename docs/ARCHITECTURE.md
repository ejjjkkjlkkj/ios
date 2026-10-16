# Architecture PhoneBridge

## Objectif

Construire un centre de contrôle iPhone avec une application iOS accessible et un compagnon Windows/macOS. Le périmètre visé comprend la gestion IPA, fichiers, diagnostics, transferts, SSH et, uniquement dans des environnements compatibles, les opérations avancées. Voir [PRODUCT_SCOPE.md](PRODUCT_SCOPE.md) pour la vision et les critères.

## Composants

### iOS app
Interface SwiftUI accessible; diagnostics utilisant des API publiques; import/export via les interfaces système; permissions explicites; données limitées au sandbox sauf autre mécanisme autorisé.

### Desktop companion
Connexion USB/réseau, appairage et workflows supportés. Aucune dépendance obligatoire à iTunes/iCloud au niveau produit, mais les pilotes, composants Apple, comptes, profils et permissions nécessaires doivent être déclarés.

### Core partagé
Modèles déterministes pour capacités, résultats, planification IPA/DEB, protocoles versionnés, rapports JSON, validation de chemins et état de transfert. Les modèles ne doivent pas être présentés comme fonctions de transport ou d’installation opérationnelles.

### SSH
Client SSH/SFTP authentifié avec vérification de clé d’hôte et stockage sécurisé des identifiants. Le mode root est isolé et optionnel; il se connecte seulement à un serveur root déjà configuré par le propriétaire. Il ne crée pas de privilèges sur un iPhone standard.

### IPA et DEB
IPA : analyse et installation uniquement via une voie de signature/distribution autorisée. DEB : inspection sûre; installation bloquée sur iOS standard et permise uniquement dans un environnement modifié compatible, détecté et testé.

## Contrat de preuve

Chaque vérification inclut un identifiant stable, un statut PASS/FAIL/PARTIAL/BLOCKED/NOT_VALIDATED, un résumé, une source de preuve, un horodatage et les limites/étapes suivantes. Les tests unitaires prouvent le comportement du code uniquement; simulateur et appareil physique doivent être distingués.

## Sécurité

- Lecture seule par défaut; confirmation avant toute modification.
- Pas de contournement de signature, sandbox, authentification ou protection système.
- Secrets exclus du dépôt et des logs.
- Validation des chemins, tailles et digests sur les transferts.
- Aucun envoi cloud par défaut des fichiers IPA/DEB, logs, identifiants ou rapports.
- Analyse de paquets sans exécution automatique de scripts non fiables.

## Release
Une release exige CI verte, projet Xcode compilable, tests, vérification accessibilité/sécurité et matrice de validation sur appareils physiques. La cible iOS 27.0.1 demeure NOT VALIDATED jusqu’à preuve.
