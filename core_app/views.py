from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import FileResponse, Http404, JsonResponse
from django.utils import timezone
from django.urls import reverse
from pathlib import Path

from .models import Stat, Feature, Skill, Project, DownloadRequest
from .forms import ContactForm, DownloadRequestForm, FeedbackForm


def home(request):
    context = {
        "stats": Stat.objects.all(),
        "features": Feature.objects.prefetch_related("tags").all(),
    }
    return render(request, "core_app/index.html", context)


def portfolio(request):
    contact_form = ContactForm()

    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            msg = contact_form.save()
            try:
                send_mail(
                    subject=f"[TopoRahma Contact] {msg.subject}",
                    message=f"De: {msg.name} <{msg.email}>\n\n{msg.message}",
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                    recipient_list=["bourahmaouattara@gmail.com"],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, "Votre message a ete envoye avec succes !")
            return redirect("portfolio")

    context = {
        "skills": Skill.objects.prefetch_related("items").all(),
        "projects": Project.objects.prefetch_related("tags").all(),
        "contact_form": contact_form,
    }
    return render(request, "core_app/portfolio.html", context)


def _get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def download_form(request):
    """Formulaire prealable au telechargement."""
    if request.method == "POST":
        form = DownloadRequestForm(request.POST)
        if form.is_valid():
            dl = form.save(commit=False)
            dl.ip_address = _get_client_ip(request)
            dl.user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]
            dl.save()

            # Notification email admin
            try:
                send_mail(
                    subject=f"[TOPORAHMA] Nouvelle demande de telechargement — {dl.full_name}",
                    message=(
                        f"Nom: {dl.full_name}\n"
                        f"Email: {dl.email}\n"
                        f"Telephone: {dl.phone}\n"
                        f"Profession: {dl.get_profession_display()}\n"
                        f"Organisation: {dl.organization or '—'}\n"
                        f"Pays: {dl.country}\n"
                        f"Ville: {dl.city or '—'}\n"
                        f"Source: {dl.get_heard_from_display() or '—'}\n\n"
                        f"Usage prevu:\n{dl.intended_use or '—'}\n"
                    ),
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                    recipient_list=["bourahmaouattara@gmail.com"],
                    fail_silently=True,
                )
            except Exception:
                pass

            request.session["download_request_id"] = dl.id
            return redirect("download_success", pk=dl.id)
    else:
        form = DownloadRequestForm()

    return render(request, "core_app/download.html", {"form": form})


def download_success(request, pk):
    """Page de remerciement avec appel a contribution + feedback + lien de telechargement."""
    dl = get_object_or_404(DownloadRequest, pk=pk)
    feedback_form = FeedbackForm()

    if request.method == "POST":
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            fb = feedback_form.save(commit=False)
            fb.download_request = dl
            if not fb.full_name:
                fb.full_name = dl.full_name
            if not fb.email:
                fb.email = dl.email
            fb.save()
            messages.success(
                request,
                "Merci beaucoup pour votre retour ! Votre contribution "
                "est precieuse pour ameliorer TOPORAHMA."
            )
            return redirect("download_success", pk=dl.id)

    context = {
        "download_request": dl,
        "feedback_form": feedback_form,
        "wave_number": "+225 07 07 77 98 90",
        "wave_number_clean": "2250707779890",
    }
    return render(request, "core_app/download_success.html", context)


def download_file(request, pk):
    """Sert le fichier TOPORAHMA.zip et trace le telechargement."""
    dl = get_object_or_404(DownloadRequest, pk=pk)
    dl.downloaded_at = timezone.now()
    dl.save(update_fields=["downloaded_at"])

    file_path = Path(settings.BASE_DIR) / "static" / "images" / "TOPORAHMA.zip"
    if not file_path.exists():
        # Fallback: marque le telechargement mais redirige vers la page download avec message
        messages.error(
            request,
            "Le fichier d'installation n'est pas encore disponible. "
            "Contactez l'administrateur."
        )
        return redirect("download_success", pk=dl.id)

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename="TOPORAHMA.zip",
    )


def mark_contribution(request, pk):
    """Marque qu'un utilisateur a confirme avoir contribue (clic sur 'J'ai contribue')."""
    dl = get_object_or_404(DownloadRequest, pk=pk)
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

    if request.method == "POST":
        dl.has_contributed = True
        saved_amount = None
        try:
            amount = int(request.POST.get("amount", 0))
            if amount > 0:
                dl.contribution_amount = amount
                saved_amount = amount
        except (ValueError, TypeError):
            pass
        dl.save(update_fields=["has_contributed", "contribution_amount"])

        if is_ajax:
            return JsonResponse({
                "ok": True,
                "id": dl.id,
                "has_contributed": dl.has_contributed,
                "amount": saved_amount,
            })

        messages.success(
            request,
            "Merci infiniment pour votre contribution ! Votre soutien fait "
            "toute la difference pour ameliorer TOPORAHMA."
        )
    return redirect("download_success", pk=dl.id)
