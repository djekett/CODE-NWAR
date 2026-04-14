from django.db import models


class Stat(models.Model):
    label = models.CharField("Libelle", max_length=100)
    value = models.CharField("Valeur", max_length=50)
    data_count = models.IntegerField(
        "Valeur numerique (pour animation compteur)", blank=True, null=True,
        help_text="Laisser vide si la valeur n'est pas un nombre a animer (ex: '3D', '100%')."
    )
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Statistique"
        verbose_name_plural = "Statistiques"

    def __str__(self):
        return f"{self.label}: {self.value}"


class Feature(models.Model):
    title = models.CharField("Titre", max_length=200)
    description = models.TextField("Description")
    icon_svg = models.TextField(
        "Icone SVG",
        help_text="Code SVG de l'icone (ex: <svg ...>...</svg>)."
    )
    icon_css_class = models.CharField(
        "Classe CSS icone", max_length=50, blank=True,
        help_text="Classe de couleur: topo, visu, urban, dao, geo, calc, io, print"
    )
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Fonctionnalite"
        verbose_name_plural = "Fonctionnalites"

    def __str__(self):
        return self.title


class FeatureTag(models.Model):
    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE, related_name="tags"
    )
    name = models.CharField("Nom du tag", max_length=100)

    class Meta:
        verbose_name = "Tag de fonctionnalite"
        verbose_name_plural = "Tags de fonctionnalites"

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField("Nom", max_length=200)
    icon_svg = models.TextField(
        "Icone SVG", blank=True,
        help_text="Code SVG inline pour l'icone."
    )
    icon_bg_color = models.CharField(
        "Couleur fond icone", max_length=100, blank=True,
        default="rgba(8, 145, 178, 0.12)"
    )
    bar_css_class = models.CharField(
        "Classe CSS barre", max_length=50, blank=True,
        help_text="Classe de couleur pour la barre de progression: topo, sig, dev, web"
    )
    percentage = models.PositiveIntegerField("Pourcentage", default=0)
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Competence"
        verbose_name_plural = "Competences"

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"


class SkillItem(models.Model):
    skill = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name="items"
    )
    text = models.CharField("Element", max_length=200)
    order = models.PositiveIntegerField("Ordre", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Element de competence"
        verbose_name_plural = "Elements de competence"

    def __str__(self):
        return self.text


class Tag(models.Model):
    name = models.CharField("Nom", max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Tag technique"
        verbose_name_plural = "Tags techniques"

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ("online", "En ligne"),
        ("soon", "Bientot disponible"),
    ]

    title = models.CharField("Titre", max_length=200)
    description = models.TextField("Description courte")
    image = models.ImageField(
        "Image", upload_to="projects/", blank=True, null=True,
    )
    placeholder_logo_svg = models.TextField(
        "SVG logo placeholder", blank=True,
        help_text="SVG a afficher si pas d'image uploadee."
    )
    placeholder_bg_style = models.CharField(
        "Style fond placeholder", max_length=200, blank=True,
        default="background: linear-gradient(135deg, var(--teal), var(--teal-dark));"
    )
    placeholder_text = models.CharField(
        "Texte placeholder", max_length=100, blank=True
    )
    placeholder_sub = models.CharField(
        "Sous-texte placeholder", max_length=100, blank=True
    )
    url = models.URLField("Lien du projet", blank=True)
    status = models.CharField(
        "Statut", max_length=20, choices=STATUS_CHOICES, default="online"
    )
    is_featured = models.BooleanField("Projet vedette", default=False)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField("Nom", max_length=200)
    email = models.EmailField("Email")
    subject = models.CharField("Sujet", max_length=300)
    message = models.TextField("Message")
    created_at = models.DateTimeField("Date de reception", auto_now_add=True)
    is_read = models.BooleanField("Lu", default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"

    def __str__(self):
        return f"{self.name} — {self.subject} ({self.created_at:%d/%m/%Y})"


class DownloadRequest(models.Model):
    PROFESSION_CHOICES = [
        ("geometre", "Geometre topographe"),
        ("urbaniste", "Urbaniste"),
        ("geomaticien", "Geomaticien / SIG"),
        ("ingenieur", "Ingenieur civil / BTP"),
        ("architecte", "Architecte"),
        ("etudiant", "Etudiant"),
        ("enseignant", "Enseignant / Chercheur"),
        ("autre", "Autre"),
    ]

    HEARD_FROM_CHOICES = [
        ("social", "Reseaux sociaux"),
        ("search", "Moteur de recherche"),
        ("friend", "Bouche a oreille / Collegue"),
        ("linkedin", "LinkedIn"),
        ("whatsapp", "WhatsApp"),
        ("event", "Evenement / Conference"),
        ("other", "Autre"),
    ]

    full_name = models.CharField("Nom complet", max_length=200)
    email = models.EmailField("Email")
    phone = models.CharField("Telephone", max_length=30)
    profession = models.CharField(
        "Profession", max_length=30, choices=PROFESSION_CHOICES
    )
    organization = models.CharField(
        "Entreprise / Organisation", max_length=200, blank=True
    )
    country = models.CharField("Pays", max_length=100)
    city = models.CharField("Ville", max_length=100, blank=True)
    heard_from = models.CharField(
        "Comment nous avez-vous connu ?",
        max_length=30, choices=HEARD_FROM_CHOICES, blank=True,
    )
    intended_use = models.TextField(
        "Usage prevu du logiciel", blank=True,
        help_text="Dans quel cadre comptez-vous utiliser TOPORAHMA ?"
    )
    accepts_newsletter = models.BooleanField(
        "Accepte de recevoir des nouvelles",
        default=True,
        help_text="Mises a jour, conseils d'utilisation et nouveautes.",
    )
    has_contributed = models.BooleanField(
        "A contribue financierement", default=False
    )
    contribution_amount = models.PositiveIntegerField(
        "Montant de la contribution (FCFA)", blank=True, null=True
    )
    ip_address = models.GenericIPAddressField("Adresse IP", blank=True, null=True)
    user_agent = models.CharField("User-Agent", max_length=500, blank=True)
    created_at = models.DateTimeField("Date de la demande", auto_now_add=True)
    downloaded_at = models.DateTimeField(
        "Date du telechargement", blank=True, null=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Demande de telechargement"
        verbose_name_plural = "Demandes de telechargement"

    def __str__(self):
        return f"{self.full_name} — {self.profession} ({self.created_at:%d/%m/%Y})"


class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    download_request = models.ForeignKey(
        DownloadRequest, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="feedbacks",
        verbose_name="Telechargement lie",
    )
    full_name = models.CharField("Nom", max_length=200, blank=True)
    email = models.EmailField("Email", blank=True)
    rating = models.PositiveSmallIntegerField(
        "Note globale (1-5)", choices=RATING_CHOICES, default=5
    )
    what_liked = models.TextField(
        "Ce que vous avez aime", blank=True
    )
    what_to_improve = models.TextField(
        "Ce qui peut etre ameliore", blank=True
    )
    features_wanted = models.TextField(
        "Fonctionnalites souhaitees", blank=True
    )
    would_recommend = models.BooleanField(
        "Recommanderait a un collegue", default=True
    )
    created_at = models.DateTimeField("Date", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Retour utilisateur"
        verbose_name_plural = "Retours utilisateurs"

    def __str__(self):
        who = self.full_name or (self.email or "Anonyme")
        return f"{who} — {self.rating}/5 ({self.created_at:%d/%m/%Y})"
