from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume


# Dashboard menu page
def dashboard(request):
    name = request.session.get("name")
    dob = request.session.get("dob")

    recent_resumes = Resume.objects.filter(
        name=name,
        dob=dob
    ).order_by("-created_at")[:5]

    return render(request, "dashboard.html", {
        "name": name,
        "recent_resumes": recent_resumes,
    })


# First page function

def fastpage(request):
    if request.method == "POST":
        name = request.POST.get("name")
        dob = request.POST.get("dob")

        # Session: current user's basic information মনে রাখবে
        request.session["name"] = name
        request.session["dob"] = dob

        return redirect("dashboard")

    return render(request, "fastpage.html")


# Profile update function
def edit(request):
    template = request.GET.get("template")

    return render(request, "edit.html", {
        "template": template
    })


# Rendering template + saving resume in database
def create_resume(request):
    if request.method != "POST":
        return redirect("choose_tem")

    template = request.POST.get("template")

    # Session থেকে current user-এর name ও dob নেওয়া
    name = request.session.get("name")
    dob = request.session.get("dob")

    if not name or not dob:
        return redirect("fastpage")

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

    # Model: resume-এর সব data database-এ save করবে
    Resume.objects.create(
        name=name,
        dob=dob,
        email=data["email"],
        phone=data["phone"],
        address=data["address"],
        professional_summary=data["professional_summary"],
        company=data["company"],
        job_title=data["job_title"],
        duration=data["duration"],
        experience_describtion=data["experience_describtion"],
        college=data["college"],
        degree=data["degree"],
        passing_year=data["passing_year"],
        skill1=data["skill1"],
        skill2=data["skill2"],
        skill3=data["skill3"],
        skill4=data["skill4"],
        project_name=data["project_name"],
        project_description=data["project_description"],
        template=template,
    )

    if template == "1":
        return render(request, "resume1.html", data)
    elif template == "2":
        return render(request, "resume2.html", data)
    elif template == "3":
        return render(request, "resume3.html", data)
    elif template == "4":
        return render(request, "resume4.html", data)

    return redirect("choose_tem")


# View a saved resume from the dashboard
def view_resume(request, resume_id):
    name = request.session.get("name")
    dob = request.session.get("dob")

    if not name or not dob:
        return redirect("fastpage")

    # Only allow the current session user to view their own saved resume.
    resume = get_object_or_404(Resume, id=resume_id, name=name, dob=dob)

    # The four existing resume templates use a few different context names.
    # Provide aliases so every template can display the saved Model data.
    context = {
        "resume": resume,
        "name": resume.name,
        "dob": resume.dob,
        "email": resume.email,
        "phone": resume.phone,
        "address": resume.address,
        "professional_summary": resume.professional_summary,
        "summary": resume.professional_summary,
        "company": resume.company,
        "job_title": resume.job_title,
        "duration": resume.duration,
        "experience_describtion": resume.experience_describtion,
        "experience": resume.experience_describtion,
        "college": resume.college,
        "degree": resume.degree,
        "passing_year": resume.passing_year,
        "skill1": resume.skill1,
        "skill2": resume.skill2,
        "skill3": resume.skill3,
        "skill4": resume.skill4,
        "project_name": resume.project_name,
        "project_description": resume.project_description,
    }

    template_map = {
        "1": "resume1.html",
        "2": "resume2.html",
        "3": "resume3.html",
        "4": "resume4.html",
    }

    template_name = template_map.get(resume.template)
    if not template_name:
        return redirect("dashboard")

    return render(request, template_name, context)


# Logout page
def logout(request):
    return render(request, "logout.html")


def confirm_logout(request):
    request.session.flush()
    return redirect("fastpage")


# Choosing template
def choose_tem(request):
    return render(request, "choose_tem.html")
