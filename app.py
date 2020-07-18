import numpy as np
from flask import Flask,request,jsonify, render_template
import pickle
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
...
...
cred = credentials.Certificate('actrec-9e13f-firebase-adminsdk-dilnt-fe8cb4b001.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://actrec-9e13f.firebaseio.com/'
})
ref=db.reference("/")
refmessage=db.reference("/message")
refhistory=db.reference("/history")
...
...
app=Flask(__name__,template_folder='template')
model=pickle.load(open('forestModel.pkl','rb'))
@app.route('/')
def home():    
    return render_template('index.html')
@app.route('/start')
def start():
    ...
    ref.update({'initial':1})
    b=ref.get()
    a=refmessage.get()
    int_features = [float(x) for x in a.values()]
    final_feature=[np.array(int_features)]
    prediction = model.predict(final_feature)
    result=prediction[0]
    timer1=b['timer1']
    timer2=b['timer2']
    timer3=b['timer3']
    timer4=b['timer4']
    if(result==1):
        timer1+=1
    elif(result==2):
        timer2+=1
    elif(result==3):
        timer3+=1
    else:
        timer4+=1
    ref.update({'timer1':timer1,'timer2':timer2,'timer3':timer3,'timer4':timer4})
    return render_template('index.html',prediction_text= result)
@app.route('/stop')
def stop():
    ...
    b=ref.get()
    timer1=b['timer1']
    timer2=b['timer2']
    timer3=b['timer3']
    timer4=b['timer4']
    interval=b['interval']
    calories= interval*(0.129*timer1+0.1395*timer2+0.06433*timer3+0.19*timer4)
    refhistory.update({'calories':calories,'timer1':timer1,'timer2':timer2,'timer3':timer3,'timer4':timer4})
    timer1,timer2,timer3,timer4=0,0,0,0
    ref.update({'initial':0,'timer1':0,'timer2':0,'timer3':0,'timer4':0})
    return render_template('index.html',prediction_text= "{} Calories burned".format(calories))
if __name__=="__main__":
    app.run(debug=True)
