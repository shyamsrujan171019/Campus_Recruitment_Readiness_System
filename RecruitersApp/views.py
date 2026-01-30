from django.shortcuts import render
import pymysql
from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request, 'Admin/index.html')


def login(request):
    return render(request, 'Admin/Login.html')


def adminaction(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username == 'Admin' and password == 'Admin':
        return render(request, 'Admin/AdminHome.html')
    else:
        context = {'data': 'Login Failed'}
        return render(request, 'Admin/Login.html', context)

def AdminHome(request):
    return render(request, 'Admin/AdminHome.html')

def AddDept(request):
    return render(request, 'Admin/AddDept.html')

def AddDeptAction(request):

    department = request.POST['dept']
    con = pymysql.connect(host='localhost', user='root', password='root', database='north_university')
    cur = con.cursor()
    cur.execute("select * from dept where name='"+department+"'");
    a = cur.fetchone()
    if a is not None:
        context = {'data': 'Department Already Added'}
        return render(request, 'Admin/AddDept.html', context)
    else:
        cur1 = con.cursor()
        i = cur1.execute("insert into dept values('"+department+"')")
        con.commit()
        if i > 0:
            context = {'data': 'Department Added Successfully..!!'}
            return render(request, 'Admin/AddDept.html', context)
        else:
            context = {'data': 'Department Adding Failed...!!'}
            return render(request, 'Admin/AddDept.html', context)
def ViewDept(request):

    con=pymysql.connect(host="localhost",user="root",password="root",database="north_university")
    cur=con.cursor()
    cur.execute("select * from dept")
    data=cur.fetchall()
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th><th>Department</th><th>Delete</th></tr></thead>"
    k=0
    for i in data:
        k=k+1
        strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[0])+"</td><td><a href='/delete?dname="+str(i[0])+"'>Delete</a></td></tr></tbody>"
        context = {'data': strdata}
    return render(request, 'Admin/ViewDept.html', context)

def delete(request):
    dept=request.GET['dname']

    con = pymysql.connect(host="localhost",user="root",password="root",database="north_university")
    cur = con.cursor()
    cur.execute("delete from dept where name='"+dept+"'")
    cur1 = con.cursor()
    con.commit()
    cur1.execute("select * from dept")
    data=cur1.fetchall()
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th><th>Department</th><th>Delete</th></tr></thead>"
    k=0
    for i in data:
        k=k+1
        strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[0])+"</td><td><a href='/delete?dname="+str(i[0])+"'>Delete</a></td></tr></tbody>"
        context = {'data': strdata}
    return render(request, 'Admin/ViewDept.html', context)

def PostApplication(request):
    con = pymysql.connect(host="localhost",user="root",password="root",database="north_university")
    cur = con.cursor()
    cur.execute("select * from dept")
    data=cur.fetchall()
    strdata=" <select class='custom-select border-0 px-4' name='dept'  style='height: 47px;' required=''> <option selected></option>"
    for i in data:
      strdata+= "<option value='"+str(i[0])+"'>"+str(i[0])+"</option>"
    strdata+= "</select>"
    context = {'data': strdata}
    return render(request, 'Admin/PostVacancy.html', context)

def AddTAVacancyAction(request):
    depart=request.POST['dept']
    v_name=request.POST['vname']
    experience=request.POST['exp']
    salary=request.POST['salary']
    description=request.POST['desc']
    con = pymysql.connect(host='localhost', user='root', password='root', database='north_university')
    cur = con.cursor()
    cur.execute("Select * from vacancy where dept='"+depart+"' and job_name='"+v_name+"'");
    a = cur.fetchone()
    if a is not None:
        cur1 = con.cursor()
        cur1.execute("select * from dept")
        data=cur1.fetchall()
        strdata=" <select class='custom-select border-0 px-4' name='dept'  style='height: 47px;' required=''> <option selected></option>"
        for i in data:
            strdata+= "<option value='"+str(i[0])+"'>"+str(i[0])+"</option>"
        strdata+= "</select>"
        context = {'data': strdata, 'msg': 'Job Vacancy Already Exist..!!'}
        return render(request, 'Admin/PostVacancy.html', context)
    else:
        cur1 = con.cursor()
        i = cur1.execute("insert into vacancy values(null,'"+depart+"','"+v_name+"','"+experience+"','"+salary+"','"+description+"')")
        con.commit()
        if i > 0:
            cur.execute("select * from dept")
            data=cur.fetchall()
            strdata=" <select class='custom-select border-0 px-4' name='dept'  style='height: 47px;' required=''> <option selected></option>"
            for i in data:
                strdata+= "<option value='"+str(i[0])+"'>"+str(i[0])+"</option>"
            strdata+= "</select>"
            context = {'data': strdata, 'msg':'Vacancy Posted Successfully..!!'}
            return render(request, 'Admin/PostVacancy.html', context)
        else:
            context = {'data': 'Vacancy Posting Failed...!!'}
            return render(request, 'Admin/PostVacancy.html', context)


def ViewApplicaiton(request):

    con=pymysql.connect(host="localhost",user="root",password="root",database="north_university")
    cur=con.cursor()
    cur.execute("SELECT * FROM ((apply_job INNER JOIN applicant ON apply_job.ta_id = applicant.id )INNER JOIN vacancy ON apply_job.v_id = vacancy.id)")
    data=cur.fetchall()
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Applicant Email</th><th>Applicant Mobile</th><th>Department</th><th>Subject</th><th>Experience</th><th>Salary</th>" \
            "<th>Date of Apply</th> <th>Resume</th> <th>Status</th> </tr></thead>"
    k=0
    for i in data:
        status = i[5]


        k=k+1

        if status =='waiting':
            strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[9])+"</td><td>"+str(i[10])+"</td><td>"+str(i[15])+"</td>" \
            "<td>"+str(i[16])+"</td><td>"+str(i[17])+"</td><td>"+str(i[18])+"</td><td>"+str(i[3])+"</td><td><a href='ViewResume?app_id="+str(i[0])+"'>View Resume</a></td><td><a href='AcceptVacancy?id="+str(i[0])+"'>Accept</a> (OR)" \
            "<a href='DeclineVacancy?id="+str(i[0])+"'>Decline</a> </td></tr></tbody>"
        else:
            strdata += "<tbody><tr><td>" + str(k) + "</td><td>" + str(i[9]) + "</td><td>" + str(
                    i[10]) + "</td><td>" + str(i[15]) + "</td>" \
                                                        "<td>" + str(i[16]) + "</td><td>" + str(
                    i[17]) + "</td><td>" + str(i[18]) + "</td><td>" + str(
                    i[3]) + "</td><td><a href='ViewResume?app_id=" + str(
                    i[0]) + "'>View Resume</a></td><td>"+status+"</td></tr></tbody>"




    context = {'data': strdata}
    return render(request, 'Admin/ViewApplicants.html', context)




def AcceptVacancy(request):
    a_id=request.GET['id']

    con = pymysql.connect(host="localhost",user="root",password="root",database="north_university")
    cur = con.cursor()
    cur.execute("update apply_job set status='Accepted' where id='"+a_id+"'")
    con.commit()
    cur1 = con.cursor()
    cur1.execute("SELECT * FROM ((apply_job INNER JOIN applicant ON apply_job.ta_id = applicant.id )INNER JOIN vacancy ON apply_job.v_id = vacancy.id)")
    data=cur1.fetchall()
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Applicant Email</th><th>Applicant Mobile</th><th>Department</th><th>Subject</th><th>Experience</th><th>Salary</th>" \
            "<th>Date of Apply</th> <th>Resume</th>  <th>Status</th></tr></thead>"
    k=0
    for i in data:
        status = i[5]



        k=k+1
        k = k + 1

        if status == 'waiting':
            strdata += "<tbody><tr><td>" + str(k) + "</td><td>" + str(i[9]) + "</td><td>" + str(
                i[10]) + "</td><td>" + str(i[15]) + "</td>" \
                                                    "<td>" + str(i[16]) + "</td><td>" + str(i[17]) + "</td><td>" + str(
                i[18]) + "</td><td>" + str(i[3]) + "</td><td><a href='ViewResume?app_id=" + str(
                i[0]) + "'>View Resume</a></td><td><a href='AcceptVacancy?id=" + str(i[0]) + "'>Accept</a> (OR)" \
                                                                                             "<a href='DeclineVacancy?id=" + str(
                i[0]) + "'>Decline</a> </td></tr></tbody>"
        else:
            strdata += "<tbody><tr><td>" + str(k) + "</td><td>" + str(i[9]) + "</td><td>" + str(
                i[10]) + "</td><td>" + str(i[15]) + "</td>" \
                                                    "<td>" + str(i[16]) + "</td><td>" + str(
                i[17]) + "</td><td>" + str(i[18]) + "</td><td>" + str(
                i[3]) + "</td><td><a href='ViewResume?app_id=" + str(
                i[0]) + "'>View Resume</a></td><td>" + status + "</td></tr></tbody>"
    context = {'data': strdata}
    return render(request, 'Admin/ViewApplicants.html', context)

def DeclineVacancy(request):
    a_id=request.GET['id']

    con = pymysql.connect(host="localhost",user="root",password="root",database="north_university")
    cur = con.cursor()
    cur.execute("update apply_job set status='Declined' where id='"+a_id+"'")
    con.commit()
    cur1 = con.cursor()
    cur1.execute("SELECT * FROM ((apply_job INNER JOIN applicant ON apply_job.ta_id = applicant.id )INNER JOIN vacancy ON apply_job.v_id = vacancy.id)")
    data=cur1.fetchall()
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Applicant Email</th><th>Applicant Mobile</th><th>Department</th><th>Subject</th><th>Experience</th><th>Salary</th>" \
            "<th>Date of Apply</th> <th>Resume</th><th>Status</th></tr></thead>"
    k=0
    for i in data:
        status = i[5]
        k = k + 1

        if status == 'waiting':
            strdata += "<tbody><tr><td>" + str(k) + "</td><td>" + str(i[9]) + "</td><td>" + str(
                i[10]) + "</td><td>" + str(i[15]) + "</td>" \
                                                    "<td>" + str(i[16]) + "</td><td>" + str(i[17]) + "</td><td>" + str(
                i[18]) + "</td><td>" + str(i[3]) + "</td><td><a href='ViewResume?app_id=" + str(
                i[0]) + "'>View Resume</a></td><td><a href='AcceptVacancy?id=" + str(i[0]) + "'>Accept</a> (OR)" \
                                                                                             "<a href='DeclineVacancy?id=" + str(
                i[0]) + "'>Decline</a> </td></tr></tbody>"
        else:
            strdata += "<tbody><tr><td>" + str(k) + "</td><td>" + str(i[9]) + "</td><td>" + str(
                i[10]) + "</td><td>" + str(i[15]) + "</td>" \
                                                    "<td>" + str(i[16]) + "</td><td>" + str(
                i[17]) + "</td><td>" + str(i[18]) + "</td><td>" + str(
                i[3]) + "</td><td><a href='ViewResume?app_id=" + str(
                i[0]) + "'>View Resume</a></td><td>" + status + "</td></tr></tbody>"
    context = {'data': strdata}
    return render(request, 'Admin/ViewApplicants.html', context)


def ViewAllTA(request):
    con = pymysql.connect(host="localhost",user="root",password="root",database="north_university")
    cur1 = con.cursor()
    cur1.execute("SELECT * FROM ((apply_job INNER JOIN applicant ON  apply_job.ta_id = applicant.id and apply_job.status='Accepted')INNER JOIN vacancy ON apply_job.v_id = vacancy.id)")
    data=cur1.fetchall()
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Applicant Email</th><th>Applicant Mobile</th><th>Department</th><th>Subject</th><th>Experience</th><th>Salary</th>" \
            "<th>Date of Apply</th> <th>Resume</th><th>Status</th></tr></thead>"
    k=0
    for i in data:

        k=k+1
        strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[9])+"</td><td>"+str(i[10])+"</td><td>"+str(i[15])+"</td>" \
                "<td>"+str(i[16])+"</td><td>"+str(i[17])+"</td><td>"+str(i[18])+"</td><td>"+str(i[3])+"</td><td><a href='ViewResume?app_id="+str(i[0])+"'>View Resume</a></td><td>"+str(i[5])+"</td></tr></tbody>"
    context={'data':strdata}
    return render(request,'Admin/ViewAllTA.html',context)




def ViewResume(request):
    appid=request.GET['app_id']
    con=pymysql.connect(host="localhost",user="root",password="root",database="north_university")
    cur=con.cursor()
    cur.execute("select resume from apply_job where id='"+appid+"'")
    file=cur.fetchone()[0]
    cur.close()

    response = HttpResponse(file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Resume.pdf"'
    return response


