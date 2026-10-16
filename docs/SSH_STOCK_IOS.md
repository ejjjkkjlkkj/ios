# SSH sans jailbreak — périmètre réaliste

## Décision produit

- **Aucun paquet DEB à installer sur iOS standard.** Un paquet `.deb` n'est pas un format d'installation pris en charge par iOS stock. Une connexion SSH ne contourne ni la signature de code, ni le sandbox, ni les droits système.
- **Installation d'applications : IPA signé** avec une signature et un profil de provisioning valides, selon la méthode de distribution Apple compatible avec l'appareil et la version d'iOS.
- **Connexion SSH :** le compagnon Windows/macOS peut être un client SSH vers un serveur SSH déjà activé et autorisé sur l'appareil cible. iOS standard ne fournit pas de serveur SSH système administrable comme sur un appareil jailbreaké.
- Pour un iPhone non jailbreaké, prévoir plutôt un **service réseau limité intégré à l'application PhoneBridge**, actif lorsque les règles iOS le permettent, avec authentification explicite et accès limité aux fichiers/données que l'application possède. Ne pas le présenter comme un shell SSH système.

## Sécurité requise

- Authentification par clé lorsque possible; aucune clé privée stockée dans le dépôt.
- Validation stricte de l'hôte et protection contre les connexions non autorisées.
- Chiffrement en transit, consentement explicite sur l'iPhone, révocation de session et journalisation sans secrets.
- Limiter les opérations aux données autorisées par iOS; pas d'accès root, pas de modification du système, pas de contournement de signature.
- Ne jamais exposer le service sur toutes les interfaces par défaut; préférer une connexion locale ou USB si une méthode officiellement supportée est disponible.

## État de validation

- Spécification et limites documentées : **PASS**.
- Client SSH implémenté : **NOT IMPLEMENTED**.
- Service applicatif sur iPhone implémenté : **NOT IMPLEMENTED**.
- Connexion réelle sur appareil iOS 27.0.1 : **NOT VALIDATED**.
- Installation IPA signée sur appareil réel : **NOT VALIDATED**.

Le support iOS 27.0.1 reste une cible déclarée, pas une compatibilité prouvée tant que la compilation avec le SDK approprié et les tests sur appareil physique n'ont pas réussi.