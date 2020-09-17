from django.contrib import messages
from django.shortcuts import redirect, render
from envelope.views import ContactView


def main(request):
    if request.user.is_authenticated:
        return redirect("eggs_list", "10")
    return render(request, "big_eggs/index.html")


def impressum(request):
    return render(request, "big_eggs/impressum.html")


def datenschutz(request):
    return render(request, "big_eggs/datenschutz.html")


class BEContactView(ContactView):
    template_name = "big_eggs/contact.html"
    success_url = "/"

    def form_valid(self, form):
        messages.success(self.request, "Vielen Dank für Ihre Nachricht.")
        return super().form_valid(form)
