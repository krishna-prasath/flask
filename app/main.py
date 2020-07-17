from flask import Flask,session,redirect,render_template,request,url_for,flash,session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date,time
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///erp.db"
app.secret_key="Thiisisascerect"
db=SQLAlchemy(app)
bcrypt=Bcrypt()
class UserTab(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(30),nullable=False)
    phone_no=db.Column(db.Integer,nullable=False)
    username=db.Column(db.String(20),nullable=False)
    password=db.Column(db.String(87),nullable=False)
    timestamp=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    def __repr__(self):
        return 'User Value'+self.username


class CompanyPro(db.Model):
    cid=db.Column(db.Integer,primary_key=True)
    cname = db.Column(db.String(50),nullable=False)
    cp_name = db.Column(db.String(30),nullable=False)#contact person name
    phone = db.Column(db.String(15),nullable=False)
    address = db.Column(db.String(90),nullable=False)
    email = db.Column(db.String(35),nullable=False)
    epf_no = db.Column(db.String(30),default="No Entries")
    epf_userid = db.Column(db.String(30),default="No Entries")
    epf_pass = db.Column(db.String(30),default="No Entries")
    esi_no = db.Column(db.String(30),default="No Entries")
    esi_userid = db.Column(db.String(30),default="No Entries")
    esi_pass = db.Column(db.String(30),default="No Entries")
    dsc_Boxno = db.Column(db.String(3),default="No Entries")
    dsc_exp= db.Column(db.DateTime)
    dsc_sent = db.Column(db.DateTime)
    def __repr__(self):
        return 'User Value'+str(self.cid)


    
    
@app.route("/")
@app.route("/login",methods=['GET','POST']) 
def login():
    if "user" in session:
        session.pop("user",None)
        flash("Always remember to logout Properly")
        return redirect("login")
    if request.method=="POST":
        var = UserTab.query.filter_by(username=str(request.form['username'])).first()
        if var==None:
            flash("Invalid Credentials","error")
            return redirect(url_for("login"))
        else:
            if var.username==request.form['username']:
                if bcrypt.check_password_hash(var.password,request.form['password']):
                    flash("Login Succesfull")
                    time=(var.timestamp).strftime("%d/%m/%Y, %H:%M")
                    var.timestamp=datetime.now()
                    db.session.commit()
                    session["user"]=[var.name,time,var.id]
                    return redirect(url_for("mainpage"))    
                else:
                    flash("Invalid Password")
                    return redirect(url_for("login"))
    return render_template("Login.html")
 # variable to disabled field
@app.route("/mainpage",methods=["POST","GET"])
def mainpage():
    m="" 
    if "user" in session:
        a=session["user"]
        if a[2] not in [1,2]:
            m="disabled"
        return render_template("mainpage.html",name=a[0],time=a[1],m=m)
    return redirect(url_for("login"))


@app.route("/employee_register",methods=['POST','GET'])
def employee_register():
    if "user" in session:
        a=session["user"]
        if request.method=="POST":
            password=bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            db.session.add(UserTab(name=request.form['name'],phone_no=int(request.form['phone_no']),username=request.form['username'],password=password))
            db.session.commit()            
            flash("New User Created")
            redirect(url_for("employee_register"))
        return render_template("employee_register.html",name=a[0],time=a[1])
    return redirect(url_for("login"))

@app.route("/attendence")
def attendence():
    if "user" in session:
        a=session["user"]
        att=UserTab.query.all()
        return render_template("attendence.html",name=a[0],time=a[1],att=att,today=date.today(),crct=time(10,31,10))
    return redirect(url_for("login"))
def date_formatter(dat):
    if dat!='':
        l=list(map(int,str(dat).split("-")))
        fdat=date(l[0],l[1],l[2])
    else:
        fdat=None
    return fdat
@app.route("/company_profile/create",methods=["POST","GET"])
def company_profile_cr():
    m="" 
    if "user" in session:
        a=session["user"]
        if a[2] not in [1,2]:
            m="disabled"
        if request.method=="POST":
            exp_date=date_formatter(request.form['input13'])
            sent_date=date_formatter(request.form['input14'])
            db.session.add(CompanyPro(cname=request.form['input1'],cp_name=request.form['input2'],phone=request.form['input3']
            ,address=request.form['input4'],email=request.form['input5']
            ,epf_no=request.form['input6'],epf_userid=request.form['input7'],epf_pass=request.form['input8']
            ,esi_no=request.form['input9'],esi_userid=request.form['input10'],esi_pass=request.form['input11']
            ,dsc_Boxno=request.form['input12']
            ,dsc_exp=exp_date,dsc_sent=sent_date))
            db.session.commit()

            
            return redirect(url_for("company_profile_cr"))
        
        return render_template("create_es.html",name=a[0],time=a[1],m=m)
    return redirect(url_for("login"))


@app.route("/company_profile/update",methods=["GET","POST"])
def company_profile_upd():
    m,check="","" 
    if "user" in session:
        a=session["user"]
        if a[2] not in [1,2]:
            m="disabled"
        if request.method=="POST":
            cid=request.form["cid"]
            c=CompanyPro.query.get_or_404(cid)
            c.cname,c.cp_name,c.phone,c.address,c.email,c.epf_no,c.epf_userid,c.epf_pass,c.esi_no,c.esi_userid,c.esi_pass,c.dsc_Boxno,c.dsc_exp,c.dsc_sent=request.form['input10'],request.form['input20'],request.form['input30'],request.form['input40'],request.form['input50'],request.form['input60'],request.form['input70'],request.form['input80'],request.form['input90'],request.form['input100'],request.form['input110'],request.form['input120'],date_formatter(request.form['input130']),date_formatter(request.form['input140'])
            db.session.commit()
            return redirect(url_for("company_profile_view"))
        
        d=CompanyPro.query.filter_by(cname=request.args.get('query')).first()
        print(type(d.dsc_exp))
        if d.dsc_exp==None:
            exp=None
        else:
            exp=d.dsc_exp.date()
        if d.dsc_sent==None:
            sent=None
        else:
            sent=d.dsc_sent.date()
        return render_template("update_es.html",name=a[0],time=a[1],m=m,d=d,sent=sent,exp=exp)
        
            

    return redirect(url_for("login"))


# @app.route("/company_profile/delete",methods=["POST","GET"])
# def company_profile_del():
#     m="" 
#     if "user" in session:
#         a=session["user"]
#         if a[2] not in [1,2]:
#             m="disabled"
#         if request.method=="GET":
#             rm=CompanyPro.query.get(request.args.get('remove'))
#             db.session.delete(rm)
#         if request.method=="POST" and "confirm" in  request.form:   
#             db.session.commit()
#             return redirect(url_for("company_profile_view"))
#     return redirect(url_for("login"))

@app.route("/company_profile/view")
def company_profile_view():
    m="" 
    if "user" in session:
        a=session["user"]
        if a[2] not in [1,2]:
            m="disabled"
        var=CompanyPro.query.all()
        return render_template("view_es.html",name=a[0],time=a[1],m=m,var=var)
    return redirect(url_for("login"))

@app.route("/company_profile/view/all")

def company_profile_view_all():
    m="" 
    if "user" in session:
        a=session["user"]
        if a[2] not in [1,2]:
            m="disabled"
        d=CompanyPro.query.filter_by(cname=request.args.get('query')).first()
        if d.dsc_exp==None:
            exp=None
        else:
            exp=d.dsc_exp.date()
        if d.dsc_sent==None:
            sent=None
        else:
            sent=d.dsc_sent.date()
        return render_template("all_es.html",name=a[0],time=a[1],m=m,d=d,sent=sent,exp=exp)
    return redirect(url_for("login"))

@app.route("/cash_book")

def cash_book():
    m="" 
    if "user" in session:
        a=session["user"]
        if a[2] not in [1,2]:
            m="disabled"
        return render_template("cash_book.html",name=a[0],time=a[1],m=m)
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user",None)
    flash("Logged out sucsessfully","success")
    return redirect(url_for("login"))  

@app.route("/dynamic")
def dynamic():

    return render_template('dynamic.html')

@app.route("/datatables")
def datatables():
    return render_template("dt.html")


