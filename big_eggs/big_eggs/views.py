from django.shortcuts import redirect, render


def main(request):
    if request.user.is_authenticated:
        return redirect("eggs_list")
    return render(request, "big_eggs/index.html")


def impressum(request):
    return render(request, "big_eggs/impressum.html")
