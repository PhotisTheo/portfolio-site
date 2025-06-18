from django.shortcuts import get_object_or_404, render

from .models import Project


def home(request):
    featured_projects = Project.objects.filter(featured=True)
    return render(
        request, "portfolio/home.html", {"featured_projects": featured_projects}
    )


def portfolio(request):
    projects = Project.objects.all().order_by("-date_created")
    return render(request, "portfolio/portfolio.html", {"projects": projects})


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "portfolio/project_detail.html", {"project": project})


def about(request):
    return render(request, "portfolio/about.html")


from django.conf import settings
from django.contrib import messages

# views.py
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import ContactForm


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message_body = form.cleaned_data["message"]

            subject = f"New Contact Form Submission from {name}"
            message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message_body}"

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.EMAIL_HOST_USER],  # or another recipient email
                    fail_silently=False,
                )
                messages.success(request, "Thanks! Your message has been sent.")
                return redirect("contact")
            except Exception as e:
                messages.error(request, f"Error sending message: {e}")
    else:
        form = ContactForm()

    return render(request, "portfolio/contact.html", {"form": form})
