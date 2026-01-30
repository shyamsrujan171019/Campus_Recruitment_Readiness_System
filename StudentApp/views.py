from django.shortcuts import render
import pymysql
from django.http import HttpResponse

def Login(request):
    con = pymysql.connect(host="localhost",user="root",password="root",database="north_university")
    cur = con.cursor()
    cur.execute("select * from dept")
    data=cur.fetchall()
    strdata=" <select class='custom-select border-0 px-4' name='dept'  style='height: 47px;' required=''> <option selected></option>"
    for i in data:
      strdata+= "<option value='"+str(i[0])+"'>"+str(i[0])+"</option>"
    strdata+= "</select>"
    context = {'data': strdata}
    return render(request,'TA/Login.html', context)

def Signup(request):
    con = pymysql.connect(host="localhost",user="root",password="root",database="north_university")
    cur = con.cursor()
    cur.execute("select * from dept")
    data=cur.fetchall()
    strdata=" <select class='custom-select border-0 px-4' name='dept'  style='height: 47px;' required=''> <option selected></option>"
    for i in data:
      strdata+= "<option value='"+str(i[0])+"'>"+str(i[0])+"</option>"
    strdata+= "</select>"
    context = {'data': strdata}
    return render(request, 'TA/Register.html', context)


def RegAction(request):

    t_dept=request.POST['dept']
    t_name=request.POST['name']
    t_email=request.POST['email']
    t_mobile=request.POST['mobile']
    t_address=request.POST['address']
    t_username=request.POST['username']
    t_password=request.POST['password']

    con = pymysql.connect(host='localhost', user='root', password='root', database='north_university')
    cur = con.cursor()
    cur.execute("Select * from applicant where dept='"+t_dept+"' and mobile='"+t_mobile+"' or dept='"+t_dept+"' and  email='"+t_email+"'");
    a = cur.fetchone()
    if a is not None:
        cur = con.cursor()
        cur.execute("select * from dept")
        data=cur.fetchall()
        strdata=" <select class='custom-select border-0 px-4' name='dept'  style='height: 47px;' required=''> <option selected></option>"
        for i in data:
            strdata+= "<option value='"+str(i[0])+"'>"+str(i[0])+"</option>"
        strdata+= "</select>"
        context = {'data': strdata,  'msg': 'Email id or Mobile Number Already Exist..!!'}
        return render(request, 'TA/Register.html', context)
    else:
        cur1 = con.cursor()
        i = cur1.execute("insert into applicant values(null,'"+t_dept+"','"+t_name+"','"+t_email+"','"+t_mobile+"','"+t_address+"','"+t_username+"','"+t_password+"')")
        con.commit()
        if i > 0:
            cur = con.cursor()
            cur.execute("select * from dept")
            data=cur.fetchall()
            strdata=" <select class='custom-select border-0 px-4' name='dept'  style='height: 47px;' required=''> <option selected></option>"
            for i in data:
                strdata+= "<option value='"+str(i[0])+"'>"+str(i[0])+"</option>"
            strdata+= "</select>"
            context = {'data': strdata,  'msg': 'Registration Successful..!!'}
            return render(request, 'TA/Register.html', context)
        else:
            context = {'msg': 'Registration Failed..!!'}
            return render(request, 'TA/Register.html', context)


def LogAction(request):
    a_dept=request.POST['dept']
    uname=request.POST['username']
    passw=request.POST['password']
    con = pymysql.connect(host='localhost', user='root', password='root', database='north_university')
    cur = con.cursor()
    cur.execute("Select * from applicant where dept='"+a_dept+"' and username='"+uname+"' and  password='"+passw+"'");
    data=cur.fetchone()
    if data is not None:
        request.session['id']=data[0]
        request.session['email']=data[3]
        request.session['mobile']=data[4]
        request.session['dept']=data[1]
        return render(request, 'TA/TA_Home.html')
    else:
        con = pymysql.connect(host="localhost",user="root",password="root",database="north_university")
        cur = con.cursor()
        cur.execute("select * from dept")
        data=cur.fetchall()
        strdata=" <select class='custom-select border-0 px-4' name='dept'  style='height: 47px;' required=''> <option selected></option>"
        for i in data:
            strdata+= "<option value='"+str(i[0])+"'>"+str(i[0])+"</option>"
        strdata+= "</select>"
        context = {'data': strdata, 'msg': 'Login Failed..!!'}
        return render(request, 'TA/Login.html', context)


def ViewVacancies(request):
    ta_id=request.session['id']
    ta_dept=request.session['dept']
    con=pymysql.connect(host="localhost",user="root",password="root",database="north_university")
    cur=con.cursor()
    cur.execute("select * from vacancy where dept='"+ta_dept+"'")
    data=cur.fetchall()
    strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
            "<th>Department</th><th>Subject</th><th>Experience</th><th>Salary</th><th>Description</th><th>Status</th>" \
            "</tr></thead>"
    k=0
    for i in data:
        k=k+1
        strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                "<td>"+str(i[4])+"</td><td>"+str(i[5])+"</td><td><a href='/TA/ApplyJob?jid="+str(i[0])+"'>Apply Job</a></td></tr></tbody>"
    context = {'data': strdata}
    return render(request, 'TA/ViewVacanices.html', context)

def ApplyJob(request):
    j_id=request.GET['jid']
    request.session['j_id']=j_id
    return render(request, 'TA/ApplyVacanices.html')


def ApplyAction(request):
    if request.method == 'POST' and request.FILES['myfile']:
        j_id = request.POST['jid']
        ta_id = request.session['id']
        t_id=str(ta_id)
        con = pymysql.connect(host='localhost', user='root', password='root', database='north_university')
        cur1 = con.cursor()
        cur1.execute("select * from apply_job where ta_id='"+t_id+"'and v_id='"+j_id+"'")
        exist=cur1.fetchone()
        if exist is not None:
            ta_dept=request.session['dept']

            cur=con.cursor()
            cur.execute("select * from vacancy where dept='"+ta_dept+"'")
            data=cur.fetchall()
            strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
                "<th>Department</th><th>Subject</th><th>Experience</th><th>Salary</th><th>Description</th><th>Status</th>" \
                "</tr></thead>"
            k=0
            for i in data:
                k=k+1
                strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                "<td>"+str(i[4])+"</td><td>"+str(i[5])+"</td><td><a href='/TA/ApplyJob?jid="+str(i[0])+"'>Apply Job</a></td></tr></tbody>"
            context = {'data': strdata, 'msg': 'You Have Already Applied Job..!!'}
            return render(request, 'TA/ViewVacanices.html', context)
        else:
            t_id=str(ta_id)
            data = request.FILES['myfile'].read()
            cur1.execute('insert into apply_job values(null,%s,%s,now(),%s,%s)',(t_id,j_id,data,'waiting'))
            con.commit()

            #retrieving vacancies
            ta_dept=request.session['dept']
            con=pymysql.connect(host="localhost",user="root",password="root",database="north_university")
            cur=con.cursor()
            cur.execute("select * from vacancy where dept='"+ta_dept+"'")
            data=cur.fetchall()
            strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
                "<th>Department</th><th>Subject</th><th>Experience</th><th>Salary</th><th>Description</th><th>Status</th>" \
                "</tr></thead>"
            k=0
            for i in data:
                k=k+1
                strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                "<td>"+str(i[4])+"</td><td>"+str(i[5])+"</td><td><a href='/TA/ApplyJob?jid="+str(i[0])+"'>Apply Job</a></td></tr></tbody>"
            context = {'data': strdata, 'msg': 'Applied Successfully..!!'}
            return render(request, 'TA/ViewVacanices.html', context)


def App_Status(request):
        ta_dept=request.session['dept']
        ta_id = request.session['id']
        t_id=str(ta_id)
        con=pymysql.connect(host="localhost",user="root",password="root",database="north_university")
        cur=con.cursor()
        cur.execute("select * from vacancy v, apply_job a where a.v_id=v.id and a.ta_id='"+t_id+"'")
        data=cur.fetchall()
        strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
                "<th>Department</th><th>Subject</th><th>Experience</th><th>Salary</th><th>Date of Application</th><th>Status</th>" \
                "<th>Your Resume</th></tr></thead>"
        k=0
        for i in data:
            status=i[11]


            k=k+1

            strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                    "<td>"+str(i[4])+"</td><td>"+str(i[9])+"</td><td>"+str(i[11])+"</td><td><a href='/TA/ViewResume?app_id="+str(i[6])+"'>Download</a></td>" \
                    "</tr></tbody>"



        context = {'data': strdata, 'msg': 'Applied Successfully..!!'}
        return render(request, 'TA/ViewApplicationStatus.html', context)

def SolveAssignment(request):
    ap_id = request.GET['app_id']
    con=pymysql.connect(host="localhost",user="root",password="root",database="north_university")
    cur=con.cursor()
    cur.execute("select * from  apply_job  where id='"+ap_id+"'")
    data = cur.fetchone()
    task = data[6]
    exp = data[9]
    context = {'app_id': ap_id, 'task': task, 'exp_date': exp}
    return render(request, 'TA/SolveAssignments.html', context)


def UpdateSolution(request):
    ap_id = request.GET['a_id']
    sol = request.GET['solution']

    con = pymysql.connect(host="localhost", user="root", password="root", database="north_university")
    cur1 = con.cursor()
    i = cur1.execute("update apply_job set answers='"+sol+"',a_status='Solved' where id='"+ap_id+"'")
    con.commit()
    if i>0:
        ta_id = request.session['id']
        t_id = str(ta_id)
        con=pymysql.connect(host="localhost",user="root",password="root",database="north_university")
        cur=con.cursor()
        cur.execute("select * from vacancy v, apply_job a where a.v_id=v.id and a.ta_id='"+t_id+"'")
        data=cur.fetchall()
        strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
                "<th>Department</th><th>Subject</th><th>Experience</th><th>Salary</th><th>Date of Application</th><th>Status</th>" \
                "<th>Your Resume</th><th>Assignment</th></tr></thead>"
        k=0
        for i in data:
            status = i[11]
            a_status = i[14]

            k=k+1
            if a_status == 'Assigned':
                strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                    "<td>"+str(i[4])+"</td><td>"+str(i[9])+"</td><td>"+str(i[11])+"</td><td><a href='/TA/ViewResume?app_id="+str(i[6])+"'>Download</a></td>" \
                    "<td><a href='/TA/SolveAssignment?app_id="+str(i[6])+"'>Solve Assignment</a></td></tr></tbody>"
            elif a_status == 'Solved':
                strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                    "<td>"+str(i[4])+"</td><td>"+str(i[9])+"</td><td>"+str(i[11])+"</td><td><a href='/TA/ViewResume?app_id="+str(i[6])+"'>Download</a></td>" \
                    "<td>Assignment Solved  <a href='/TA/VSolvedAssignment?app_id="+str(i[6])+"'>View</a></td></tr></tbody>"
            else:
                strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                    "<td>"+str(i[4])+"</td><td>"+str(i[9])+"</td><td>"+str(i[11])+"</td><td><a href='/TA/ViewResume?app_id="+str(i[6])+"'>Download</a></td>" \
                    "<td>Wait till get Assignment </td></tr></tbody>"
        context = {'data': strdata, 'msg': 'Task Submitted Successfully..!!'}
        return render(request, 'TA/ViewApplicationStatus.html', context)
    else:
        ta_id = request.session['id']
        t_id = str(ta_id)
        con=pymysql.connect(host="localhost",user="root",password="root",database="north_university")
        cur=con.cursor()
        cur.execute("select * from vacancy v, apply_job a where a.v_id=v.id and a.ta_id='"+t_id+"'")
        data=cur.fetchall()
        strdata="<table  id='example' class='table table-striped table-bordered' style='width:100%'><thead><tr><th>Sr.No</th>" \
                "<th>Department</th><th>Subject</th><th>Experience</th><th>Salary</th><th>Date of Application</th><th>Status</th>" \
                "<th>Your Resume</th><th>Assignment</th></tr></thead>"
        k=0
        for i in data:
            status=i[11]
            a_status=i[14]

            k=k+1
            if a_status == 'Assigned':
                strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                    "<td>"+str(i[4])+"</td><td>"+str(i[9])+"</td><td>"+str(i[11])+"</td><td><a href='/TA/ViewResume?app_id="+str(i[6])+"'>Download</a></td>" \
                    "<td><a href='/TA/SolveAssignment?app_id="+str(i[6])+"'>Solve Assignment</a></td></tr></tbody>"
            elif a_status == 'Solved':
                strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                    "<td>"+str(i[4])+"</td><td>"+str(i[9])+"</td><td>"+str(i[11])+"</td><td><a href='/TA/ViewResume?app_id="+str(i[6])+"'>Download</a></td>" \
                    "<td>Assignment Solved  <a href='/TA/VSolvedAssignment?app_id="+str(i[6])+"'>View</a></td></tr></tbody>"
            else:
                strdata+="<tbody><tr><td>"+str(k)+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td>" \
                    "<td>"+str(i[4])+"</td><td>"+str(i[9])+"</td><td>"+str(i[11])+"</td><td><a href='/TA/ViewResume?app_id="+str(i[6])+"'>Download</a></td>" \
                    "<td>Wait till get Assignment </td></tr></tbody>"
        context = {'data': strdata, 'msg': 'Task Submition Failed..!!'}
        return render(request, 'TA/ViewApplicationStatus.html', context)








def VSolvedAssignment(request):
    appid=request.GET['app_id']

    con=pymysql.connect(host="localhost",user="root",password="root",database="north_university")
    cur=con.cursor()
    cur.execute("select * from apply_job where id='"+appid+"'")
    data=cur.fetchall()
    for i in data:
        task=i[6]
        solution=i[7]
        exp_date=i[9]
    context={'app_id':appid,'task':task,'solution':solution,'exp':exp_date}
    return render(request, 'TA/ViewSolutions.html', context)


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










