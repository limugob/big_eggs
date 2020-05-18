from django.shortcuts import render
from django.shortcuts import redirect


def main(request):
    if request.user.is_authenticated:
        return redirect("eggs_list")
    return render(request, "big_eggs/index.html")
