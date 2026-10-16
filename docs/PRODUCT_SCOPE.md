# Vision produit — contrôle complet de l’iPhone, dans les limites réelles d’iOS

## Objectif

PhoneBridge doit devenir un centre de contrôle aussi complet que les interfaces publiques et les autorisations réellement disponibles le permettent : gestion des applications, fichiers, diagnostics, connexion au PC, sauvegarde/export, réseau, accessibilité et opérations avancées clairement séparées selon le niveau d’accès de l’appareil.

« Tout faire » est l’objectif produit, pas une affirmation que toute opération est techniquement possible sur un iPhone standard. Chaque fonction doit indiquer ce qui est disponible, les prérequis, les risques et les preuves de validation.

## Modes de fonctionnement distincts

1. **iPhone standard, sans jailbreak** — API publiques iOS, données accessibles à l’application, import/export via les sélecteurs système, diagnostics permis et déploiement d’apps uniquement par les voies de signature/distribution autorisées.
2. **Compagnon ordinateur** — connexion USB/réseau, appairage et opérations prises en charge par les interfaces Apple ou des outils audités. iTunes et iCloud ne doivent pas être des dépendances obligatoires, mais certains pilotes, appairages, signatures ou composants Apple peuvent rester nécessaires.
3. **Appareil avec SSH root déjà configuré par son propriétaire** — mode avancé facultatif pour se connecter à un serveur SSH root existant. Il ne doit jamais prétendre activer root, créer un serveur SSH, obtenir un jailbreak ou contourner la sécurité sur un iPhone standard. Vérifier la clé d’hôte, afficher les commandes/actions, limiter les secrets et demander confirmation avant toute modification.
4. **Appareil modifié/jailbreaké** — fonctions spécifiques seulement si l’environnement et le gestionnaire de paquets sont détectés et explicitement pris en charge. Aucun support ne doit être supposé à l’avance.

## Modules fonctionnels visés

- **Tableau de bord** : état de connexion, modèle/version iOS lorsque disponible, capacités réellement détectées et statut de chaque vérification.
- **Applications et IPA** : importer, analyser l’archive, lire métadonnées et exigences, vérifier autant que possible signature/provisioning/entitlements, expliquer les causes de blocage, puis utiliser uniquement un chemin d’installation autorisé. Le transfert seul n’est jamais une preuve d’installation.
- **Fichiers** : parcourir/importer/exporter les emplacements auxquels le mode choisi donne réellement accès; copie avec vérification d’intégrité, progression, annulation et reprise lorsque possible.
- **Diagnostics** : versions, stockage, réseau, batterie et autres données seulement si une API publique, un rapport explicitement fourni par l’utilisateur ou un accès autorisé les expose. Toujours citer la source et les limites.
- **Connexion** : état d’appairage, connexion USB/réseau, découverte non intrusive, contrôle d’hôte SSH et tests de connectivité.
- **SSH avancé** : client SSH authentifié; clé d’hôte vérifiée; clés privées conservées dans le stockage sécurisé du système; mode root seulement vers un serveur root préexistant et explicitement autorisé.
- **Paquets DEB** : inspection et rapport de risques. Installation bloquée sur iOS standard; possible uniquement dans un environnement modifié compatible, détecté et testé, via son gestionnaire de paquets.
- **Sauvegarde et rapports** : export contrôlé, rapports JSON lisibles, masquage par défaut des identifiants sensibles, consentement avant partage.
- **Accessibilité** : VoiceOver, Dynamic Type, navigation clavier sur les plateformes compatibles, libellés explicites, contraste et aucune information essentielle uniquement visuelle.
- **Sécurité et confidentialité** : mode lecture seule par défaut, permission minimale, aperçu des modifications, confirmation explicite, journal sans secrets, aucune transmission cloud par défaut des fichiers, rapports ou identifiants.
- **Mises à jour et support** : matrice par version d’iOS et système de bureau, vérification de compatibilité, journal de changements et procédures de récupération.

## Contrat de vérité

Chaque fonctionnalité doit avoir un statut traçable :

- **PASS** — test reproductible exécuté avec preuve enregistrée.
- **FAIL** — test exécuté et échec observé.
- **PARTIAL** — une partie seulement est implémentée ou testée.
- **BLOCKED** — bloquée par le système, l’absence d’autorisation ou un prérequis manquant.
- **NOT VALIDATED** — pas de preuve d’exécution suffisante.

Une maquette, un modèle de données, un test unitaire, une simulation ou une compilation ne prouvent pas une connexion ni une opération sur un iPhone physique. Les résultats simulateur doivent être identifiés séparément.

## Règles de sécurité non négociables

- Aucun contournement de signature iOS, d’authentification, de sandbox ou de protections du système.
- Aucun stockage des mots de passe Apple, codes 2FA ou clés privées dans le dépôt, les rapports ou les logs.
- Ne jamais exécuter automatiquement un script ou une commande provenant d’un IPA/DEB.
- Les actions destructrices ou modifiant le système sont désactivées par défaut, présentées avant exécution et soumises à confirmation.
- Pas de déclaration « fonctionne sur tous les iPhone » sans matrice de tests physiques couvrant les modèles et versions annoncés.

## Critères avant une version utilisable

1. Projet Xcode réel, compilation reproductible et CI verte.
2. Tests unitaires, analyse des dépendances et scan des secrets.
3. Tests VoiceOver et Dynamic Type.
4. Tests de connexion et de transfert avec vérification d’intégrité.
5. Tests IPA sur appareils physiques et méthodes de signature prises en charge.
6. Tests SSH avec serveur de test contrôlé, validation de clé d’hôte et tests d’échec d’authentification.
7. Matrice distincte stock iOS / SSH root préconfiguré / environnement modifié.
8. Rapport de release listant précisément les fonctions PASS, PARTIAL, BLOCKED et NOT VALIDATED.
