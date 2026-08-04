from django.http import HttpResponse
from django.shortcuts import render, redirect

# setup login fanction
# def login(request):
#     return render (request, "login.html" )

# Dashboard menu page
def dashboard(request):
    return render (request, "dashboard.html")

# ligin fast page function
def fastpage(request):
    if request.method == "POST":
        d = {
            "name": request.POST.get("name"),
            "dob": request.POST.get("dob"),
        }
        return render(request, "dashboard.html", d)
    return render(request, "fastpage.html")


# profile update function

def edit (request):
    template = request.GET.get("template")

    return render(request, "edit.html", {
        "template": template
    })

# rendering template 

def create_resume(request):
    print(request.POST.get("template"))

    template = request.POST.get("template")

    data = {
        "name": request.POST.get("name"),
        "email": request.POST.get("email"),
        "phone": request.POST.get("phone"),
        "address": request.POST.get("address"),
        "professional_summary": request.POST.get("professional_summary"),

        "company": request.POST.get("company"),
        "job_title": request.POST.get("job_title"),
        "duration": request.POST.get("duration"),
        "experience_describtion": request.POST.get("experience_describtion"),

        "college": request.POST.get("college"),
        "degree": request.POST.get("degree"),
        "passing_year": request.POST.get("passing_year"),

        "skill1": request.POST.get("skill1"),
        "skill2": request.POST.get("skill2"),
        "skill3": request.POST.get("skill3"),
        "skill4": request.POST.get("skill4"),

        "project_name": request.POST.get("project_name"),
        "project_description": request.POST.get("project_description"),
    }

    if template == "1":
        return render(request, "resume1.html", data)

    elif template == "2":
        return render(request, "resume2.html", data)

    elif template == "3":
        return render(request, "resume3.html", data)

    elif template == "4":
        return render(request, "resume4.html", data)

    return redirect("choose_tem")
    


# logout function

def logout(request):
    return render(request, "logout.html")

# confirm_logout

def confirm_logout(request):
    return redirect("fastpage")

# choosing tem

def choose_tem(request):
    return render(request,"choose_tem.html")