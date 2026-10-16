# Roadmap — PhoneBridge, contrôle complet de l’iPhone

Priorité : livrer un socle utilisable, puis implémenter les capacités une par une avec tests et preuves. « Tout faire » est la vision; les limites imposées par iOS doivent rester explicites.

## Phase 0 — Fondations et preuve
- [x] Modèles de diagnostic avec statuts et rapport JSON.
- [x] Matrice initiale de capacités et moteur de diagnostic local.
- [x] Modèle de planification des fichiers IPA/DEB.
- [x] Documentation de contraintes IPA, DEB, SSH et iOS 27.0.1.
- [ ] Vérifier l’état CI réel et corriger tout échec.
- [ ] Ajouter un vrai projet Xcode, les targets iOS/macOS et des builds reproductibles.
- [ ] Activer scans de dépendances et de secrets.

## Phase 1 — Application accessible
- [ ] Tableau de bord SwiftUI complet avec statuts annoncés par VoiceOver.
- [ ] Import de fichiers via les sélecteurs système.
- [ ] Navigation VoiceOver, Dynamic Type, contraste et gestion clavier.
- [ ] Tests UI et instructions de build reproductible.

## Phase 2 — Diagnostics iPhone
- [ ] Vérifications utilisant les API publiques disponibles.
- [ ] Réseau, stockage et batterie uniquement quand exposés et testables.
- [ ] Rapports exportables, horodatés, avec sources, limites et redaction.
- [ ] Consentement avant export ou partage de données.

## Phase 3 — Compagnon de bureau et connexion
- [ ] Définir un protocole local versionné, authentifié et borné.
- [ ] Étudier les interfaces de pairing/developer prises en charge et les outils open source audités.
- [ ] Détecter appareil, appairage et capacités en lecture seule.
- [ ] Transfert par blocs, annulation, gestion d’erreurs et vérification SHA-256.
- [ ] Tests sur iPhone physique; iTunes/iCloud non obligatoires comme dépendances produit.

## Phase 4 — IPA
- [ ] Lire l’archive ZIP et Payload/*.app/Info.plist de manière sûre.
- [ ] Vérifier signature, entitlements, provisioning, expiration, architecture et exigences iOS.
- [ ] Expliquer clairement les raisons d’incompatibilité.
- [ ] Implémenter uniquement les voies d’installation autorisées et compatibles.
- [ ] Vérifier l’installation à partir de preuves côté appareil; transfert seul insuffisant.

## Phase 5 — SSH
- [ ] Implémenter un client SSH avec authentification robuste.
- [ ] Vérifier strictement la clé d’hôte et prévenir les attaques de type homme-du-milieu.
- [ ] Garder les clés privées dans le stockage sécurisé du système; ne jamais les journaliser.
- [ ] Implémenter transfert SFTP/SSH avec chemins sûrs, limites de taille et intégrité.
- [ ] Mode root séparé et désactivé par défaut; uniquement vers un serveur root déjà activé et explicitement autorisé.
- [ ] Tests sur serveur contrôlé : mauvais mot de passe/clé, clé d’hôte modifiée, délai, déconnexion et permissions.
- [ ] Ne jamais présenter SSH comme un moyen d’obtenir root sur iOS standard.

## Phase 6 — DEB et environnements modifiés
- [ ] Analyser les archives ar/control sans exécuter de scripts de mainteneur.
- [ ] Détecter architecture, dépendances, conflits et scripts.
- [ ] Bloquer l’installation sur iOS standard.
- [ ] Prendre en charge un gestionnaire de paquets seulement pour un environnement modifié compatible, détecté et testé.
- [ ] Prévisualiser les changements, demander confirmation et fournir une procédure de récupération.

## Phase 7 — Qualité et release
- [ ] CI verte sur les plateformes et versions d’outils déclarées.
- [ ] Tests unitaires, UI, sécurité, accessibilité et installation.
- [ ] Tests physiques couvrant chaque version/modèle annoncé.
- [ ] SBOM, licences, scans dépendances/secrets, notes de version.
- [ ] Matrice de support publiée avec PASS / FAIL / PARTIAL / BLOCKED / NOT VALIDATED.
- [ ] Aucune release présentée comme complète tant que les critères ci-dessus ne sont pas démontrés.

## Cible iOS 27.0.1
- [ ] Build avec Xcode/SDK compatible.
- [ ] Tester installation, lancement, import, permissions et VoiceOver sur appareil physique iOS 27.0.1.
- [ ] Conserver les checks de disponibilité des API.
- [ ] Ne pas annoncer iOS 27.0.1 comme pris en charge sans preuve.

## Règles de validation
- PASS : test reproductible exécuté avec preuve.
- FAIL : test exécuté et échec observé.
- PARTIAL : implémentation ou validation incomplète.
- BLOCKED : limite de plateforme ou prérequis absent.
- NOT VALIDATED : aucune preuve suffisante.
- Simulateur ≠ preuve sur appareil physique.
