import re
from io import BytesIO
from pathlib import Path

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from .models import Resume

BASE_DIR = Path(__file__).resolve().parent.parent


def get_resume_pdf_template_name(resume):
    template_map = {
        "1": "resume1.html",
        "2": "resume2.html",
        "3": "resume3.html",
        "4": "resume4.html",
    }
    return template_map.get(str(resume.template), "resume1.html")


def get_resume_pdf_inline_css(template_name):
    css_file = BASE_DIR / "static" / "css" / template_name.replace(".html", ".css")
    if not css_file.exists():
        return ""

    css = css_file.read_text(encoding="utf-8")
    css = re.sub(r"@import[^;]+;\s*", "", css)
    return css


# Dashboard menu page
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("fastpage")

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


# Login page
def fastpage(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            request.session["name"] = user.first_name
            request.session["dob"] = user.last_name

            return redirect("dashboard")

        return render(request, "fastpage.html", {
            "error": "Username or password is wrong."
        })

    return render(request, "fastpage.html")


# Register page
def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        dob = request.POST.get("dob")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        form_data = {
            "name": name,
            "username": username,
            "email": email,
            "dob": dob,
        }

        if password != confirm_password:
            return render(request, "register.html", {
                "error": "Password does not match.",
                "form_data": form_data
            })

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "Username already exists.",
                "form_data": form_data
            })

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {
                "error": "Email already exists.",
                "form_data": form_data
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name,
            last_name=dob
        )

        login(request, user)

        request.session["name"] = name
        request.session["dob"] = dob

        return redirect("dashboard")

    return render(request, "register.html")


# Profile page
def profile(request):
    if not request.user.is_authenticated:
        return redirect("fastpage")

    name = request.session.get("name") or request.user.get_full_name() or request.user.username
    dob = request.session.get("dob") or request.user.last_name
    total_resumes = Resume.objects.filter(name=name, dob=dob).count()
    profile_initial = (name or request.user.username)[0].upper() if (name or request.user.username) else "U"

    return render(request, "profile.html", {
        "user": request.user,
        "name": name,
        "dob": dob,
        "total_resumes": total_resumes,
        "profile_initial": profile_initial,
    })


# Profile update function
def edit(request):
    if not request.user.is_authenticated:
        return redirect("fastpage")

    template = request.GET.get("template")

    return render(request, "edit.html", {
        "template": template
    })


# Rendering template + saving resume in database
def create_resume(request):
    if not request.user.is_authenticated:
        return redirect("fastpage")

    if request.method != "POST":
        return redirect("choose_tem")

    template = request.POST.get("template")

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
        "summary": request.POST.get("professional_summary"),
        "company": request.POST.get("company"),
        "job_title": request.POST.get("job_title"),
        "duration": request.POST.get("duration"),
        "experience_describtion": request.POST.get("experience_describtion"),
        "experience": request.POST.get("experience_describtion"),
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

    saved_resume = Resume.objects.create(
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

    data["resume"] = saved_resume
    data["id"] = saved_resume.id

    if template == "1":
        return render(request, "resume1.html", data)
    elif template == "2":
        return render(request, "resume2.html", data)
    elif template == "3":
        return render(request, "resume3.html", data)
    elif template == "4":
        return render(request, "resume4.html", data)

    return redirect("choose_tem")


# View a saved resume
def view_resume(request, resume_id):
    if not request.user.is_authenticated:
        return redirect("fastpage")

    name = request.session.get("name")
    dob = request.session.get("dob")

    if not name or not dob:
        return redirect("fastpage")

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        name=name,
        dob=dob
    )

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
    if not request.user.is_authenticated:
        return redirect("fastpage")

    return render(request, "logout.html")


def confirm_logout(request):
    auth_logout(request)
    request.session.flush()

    return redirect("fastpage")


# Choosing template
def choose_tem(request):
    if not request.user.is_authenticated:
        return redirect("fastpage")

    return render(request, "choose_tem.html")

# tem_showing

def show(request):
    if not request.user.is_authenticated:
        return redirect("fastpage")

    name = request.session.get("name")
    dob = request.session.get("dob")

    if not name or not dob:
        return redirect("fastpage")

    resumes = Resume.objects.filter(name=name, dob=dob).order_by("-created_at")

    return render(request, "show.html", {"resumes": resumes})


def download_resume_pdf(request, resume_id):
    if not request.user.is_authenticated:
        return redirect("fastpage")

    name = request.session.get("name")
    dob = request.session.get("dob")

    resume = get_object_or_404(Resume, id=resume_id, name=name, dob=dob)

    template_name = get_resume_pdf_template_name(resume)
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

    html = render_to_string(template_name, context)
    css = get_resume_pdf_inline_css(template_name)
    html = re.sub(
        r"<link[^>]*href=[\"'][^\"']*resume\d+\.css[\"'][^>]*>",
        f"<style>{css}</style>",
        html,
        count=1,
    )
    html = re.sub(
        r"<div class=\"save-row\">.*?</div>",
        "",
        html,
        flags=re.DOTALL,
    )

    buffer = BytesIO()
    pdf_status = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), buffer)

    if pdf_status.err:
        return HttpResponse("PDF generation failed", status=400)

    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="resume-{resume.id}.pdf"'
    return response