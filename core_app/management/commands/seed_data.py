from django.core.management.base import BaseCommand
from core_app.models import (
    Stat, Feature, FeatureTag, Skill, SkillItem, Tag, Project,
)


class Command(BaseCommand):
    help = "Charge les donnees initiales du site (stats, fonctionnalites, competences, projets)."

    def handle(self, *args, **options):
        self.stdout.write("Chargement des donnees initiales...")

        # --- STATS (hero TopoRahma) ---
        Stat.objects.all().delete()
        stats = [
            ("Modules", "120+", 120, 0),
            ("Formats supportes", "15+", 15, 1),
            ("Visualisation", "3D", None, 2),
            ("Professionnel", "100%", None, 3),
        ]
        for label, value, count, order in stats:
            Stat.objects.create(
                label=label, value=value, data_count=count, order=order
            )
        self.stdout.write(self.style.SUCCESS(f"  {len(stats)} statistiques creees."))

        # --- FEATURES (TopoRahma) ---
        Feature.objects.all().delete()
        features_data = [
            {
                "title": "Topographie & MNT",
                "description": "Generation automatique de modeles numeriques de terrain, courbes de niveau, analyse de pentes et profils en long.",
                "icon_css_class": "topo",
                "icon_svg": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#0891b2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20L8.5 8.5 14 14 22 4"/><path d="M22 4L16 4 22 10"/></svg>',
                "tags": ["Delaunay", "Courbes de niveau", "Profils"],
            },
            {
                "title": "Visualisation 3D",
                "description": "Moteur 3D haute performance pour nuages de points LIDAR avec optimisation Octree. Animation de camera et export video.",
                "icon_css_class": "visu",
                "icon_svg": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#8b5cf6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3L2 12h3v8h6v-6h2v6h6v-8h3L12 3z"/></svg>',
                "tags": ["LIDAR", "Octree", "Animation"],
            },
            {
                "title": "Urbanisme & Lotissement",
                "description": "Subdivision automatique de parcelles, conception de reseaux routiers, estimation VRD et gestion des contraintes urbanistiques.",
                "icon_css_class": "urban",
                "icon_svg": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>',
                "tags": ["Parcelles", "Voirie", "VRD"],
            },
            {
                "title": "DAO & Dessin technique",
                "description": "Outils complets de dessin 2D : polylignes, cercles, arcs, annotations, cotations avec systeme d'accrochage intelligent.",
                "icon_css_class": "dao",
                "icon_svg": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>',
                "tags": ["Polylignes", "Annotations", "Snapping"],
            },
            {
                "title": "Geodesie & Projections",
                "description": "Support EPSG complet, zones UTM, datum Abidjan 87. Conversion de coordonnees en temps reel et transformations geodesiques.",
                "icon_css_class": "geo",
                "icon_svg": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#ec4899" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
                "tags": ["EPSG", "UTM", "Abidjan 87"],
            },
            {
                "title": "Calculs d'ingenierie",
                "description": "Cubatures deblai/remblai, calculs de cheminement, releves polaires, intersection, relevement et profils en travers.",
                "icon_css_class": "calc",
                "icon_svg": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="10" y2="10"/><line x1="14" y1="10" x2="16" y2="10"/><line x1="8" y1="14" x2="10" y2="14"/><line x1="14" y1="14" x2="16" y2="14"/><line x1="8" y1="18" x2="16" y2="18"/></svg>',
                "tags": ["Cubatures", "Cheminement", "Polaire"],
            },
            {
                "title": "Import / Export",
                "description": "Plus de 15 formats supportes : DXF, Shapefile, GeoJSON, KML, LandXML, GeoTIFF, LAS/LAZ, ASCII Grid, PLY et bien plus.",
                "icon_css_class": "io",
                "icon_svg": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#f97316" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
                "tags": ["DXF", "SHP", "LAS", "GeoTIFF"],
            },
            {
                "title": "Composition & Impression",
                "description": "Composeur de plans professionnel avec modeles, echelle, legende, grille et export haute resolution pour impression.",
                "icon_css_class": "print",
                "icon_svg": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#a855f7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>',
                "tags": ["Templates", "Legende", "Export HD"],
            },
        ]
        for i, f in enumerate(features_data):
            feat = Feature.objects.create(
                title=f["title"],
                description=f["description"],
                icon_svg=f["icon_svg"],
                icon_css_class=f["icon_css_class"],
                order=i,
            )
            for t in f["tags"]:
                FeatureTag.objects.create(feature=feat, name=t)
        self.stdout.write(self.style.SUCCESS(f"  {len(features_data)} fonctionnalites creees."))

        # --- SKILLS (Portfolio) ---
        Skill.objects.all().delete()
        skills_data = [
            {
                "name": "Topographie & Geodesie",
                "icon_bg_color": "rgba(8, 145, 178, 0.12)",
                "bar_css_class": "topo",
                "icon_svg": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#0891b2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20L8.5 8.5 14 14 22 4"/><path d="M22 4L16 4 22 10"/></svg>',
                "percentage": 95,
                "items": [
                    "Leves topographiques & implantation",
                    "Modelisation Numerique de Terrain",
                    "Systemes de coordonnees & projections",
                    "Calculs geodesiques avances",
                ],
            },
            {
                "name": "SIG & Geomatique",
                "icon_bg_color": "rgba(16, 185, 129, 0.12)",
                "bar_css_class": "sig",
                "icon_svg": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
                "percentage": 90,
                "items": [
                    "Analyse spatiale & cartographie",
                    "Traitement de donnees geospatiales",
                    "QGIS, ArcGIS, PostGIS",
                    "Geoserveurs & interoperabilite OGC",
                ],
            },
            {
                "name": "Developpement logiciel",
                "icon_bg_color": "rgba(139, 92, 246, 0.12)",
                "bar_css_class": "dev",
                "icon_svg": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#8b5cf6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
                "percentage": 88,
                "items": [
                    "Python, Qt / PySide6",
                    "Architecture modulaire",
                    "PyVista, VTK, OpenGL",
                    "PyInstaller & packaging",
                ],
            },
            {
                "name": "Architecture Web SIG",
                "icon_bg_color": "rgba(245, 158, 11, 0.12)",
                "bar_css_class": "web",
                "icon_svg": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>',
                "percentage": 85,
                "items": [
                    "Leaflet, OpenLayers, Mapbox",
                    "GeoServer, MapServer",
                    "HTML, CSS, JavaScript",
                    "APIs REST geospatiales",
                ],
            },
        ]
        for i, s in enumerate(skills_data):
            skill = Skill.objects.create(
                name=s["name"],
                icon_svg=s["icon_svg"],
                icon_bg_color=s["icon_bg_color"],
                bar_css_class=s["bar_css_class"],
                percentage=s["percentage"],
                order=i,
            )
            for j, text in enumerate(s["items"]):
                SkillItem.objects.create(skill=skill, text=text, order=j)
        self.stdout.write(self.style.SUCCESS(f"  {len(skills_data)} competences creees."))

        # --- TAGS & PROJECTS (Portfolio) ---
        Project.objects.all().delete()
        Tag.objects.all().delete()

        def get_or_create_tags(names):
            return [Tag.objects.get_or_create(name=n)[0] for n in names]

        # Project 1 - featured (TOPORAHMA)
        p1 = Project.objects.create(
            title="TOPORAHMA v1.0",
            description=(
                "Suite logicielle professionnelle tout-en-un pour la topographie, "
                "l'urbanisme, la visualisation 3D LIDAR et les calculs d'ingenierie. "
                "Plus de 120 modules integres, 15+ formats supportes."
            ),
            url="/",
            status="online",
            is_featured=True,
            order=0,
            placeholder_text="TOPORAHMA",
            placeholder_sub="Suite logicielle professionnelle",
        )
        p1.tags.set(get_or_create_tags(["Python", "PySide6 / Qt", "PyVista", "VTK", "LIDAR", "GIS"]))

        # Project 2 - Web SIG
        p2 = Project.objects.create(
            title="Plateforme Web SIG",
            description=(
                "Application web de cartographie interactive pour la gestion des "
                "donnees geospatiales et la visualisation en temps reel."
            ),
            status="soon",
            is_featured=False,
            order=1,
            placeholder_bg_style="background: linear-gradient(135deg, #10b981, #059669);",
            placeholder_logo_svg='<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
            placeholder_text="Web SIG",
            placeholder_sub="Application cartographique",
        )
        p2.tags.set(get_or_create_tags(["Leaflet", "Django", "PostGIS"]))

        # Project 3 - Foncier digital
        p3 = Project.objects.create(
            title="Foncier digital",
            description=(
                "Solution de gestion fonciere et cadastrale numerique pour les "
                "collectivites territoriales africaines."
            ),
            status="soon",
            is_featured=False,
            order=2,
            placeholder_bg_style="background: linear-gradient(135deg, #f59e0b, #d97706);",
            placeholder_logo_svg='<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>',
            placeholder_text="Foncier digital",
            placeholder_sub="Gestion fonciere",
        )
        p3.tags.set(get_or_create_tags(["Python", "PostgreSQL", "Django"]))

        self.stdout.write(self.style.SUCCESS("  3 projets crees."))

        self.stdout.write(self.style.SUCCESS("\nDonnees initiales chargees avec succes !"))
