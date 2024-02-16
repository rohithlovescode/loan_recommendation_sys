from flask import Flask, escape, request, render_template
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/calculator')
def calculator_index():
    return render_template('calculator/index2.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method ==  'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = 1
        education = request.form['education']
        employed = request.form['employed']
        credit = 1
        area = "Urban"
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = 1000000
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

        # gender
        if (gender == "Male"):
            male=1
        else:
            male=0
        
        # married
        if(married=="Yes"):
            married_yes = 1
        else:
            married_yes=0

        # dependents
        if(dependents=='1'):
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0
        elif(dependents == '2'):
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
        elif(dependents=="3+"):
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0  

        # education
        if (education=="Not Graduate"):
            not_graduate=1
        else:
            not_graduate=0

        # employed
        if (employed == "Yes"):
            employed_yes=1
        else:
            employed_yes=0

        # property area

        if(area=="Semiurban"):
            semiurban=1
            urban=0
        elif(area=="Urban"):
            semiurban=0
            urban=1
        else:
            semiurban=0
            urban=0
        if(CoapplicantIncome<350):
            credit=0

        ApplicantIncomelog = np.log(ApplicantIncome)
        totalincomelog = np.log(ApplicantIncome+CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)
        Loan_Amount_Termlog = np.log(Loan_Amount_Term)

        prediction = model.predict([[credit, ApplicantIncomelog,LoanAmountlog, Loan_Amount_Termlog, totalincomelog, male, married_yes, dependents_1, dependents_2, dependents_3, not_graduate, employed_yes,semiurban, urban ]])

        # print(prediction)

        if(prediction=="N" or ApplicantIncome<10000 or CoapplicantIncome<350):
            return render_template("prediction.html", prediction_text="You are not eligible for any loan")
        else:
            prediction="Yes"
        if(CoapplicantIncome<600):
            CoapplicantIncome=CoapplicantIncome/3
        elif(CoapplicantIncome<650):
            CoapplicantIncome=CoapplicantIncome/2
        elif(CoapplicantIncome>700 and CoapplicantIncome<750):
            CoapplicantIncome=CoapplicantIncome*1.05
        elif(CoapplicantIncome>750 and CoapplicantIncome<825):
            CoapplicantIncome=CoapplicantIncome*1.1
        elif(CoapplicantIncome>825):
            CoapplicantIncome=CoapplicantIncome*1.2
        
        totalLoan=CoapplicantIncome*ApplicantIncome/25
        

        
        return render_template("prediction.html", prediction_text="Recommendedations: Can avail home loan under {}L Can avail car Loan under {}L\n Can avail Personal loan under {}L".format(
            int(totalLoan/110000),
            int(totalLoan/100000/5),
            int(totalLoan/120000/6)))




    else:
        return render_template("prediction.html")

if __name__ == "__main__":
    app.run(debug=True)