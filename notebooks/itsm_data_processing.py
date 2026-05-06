import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report,precision_score,recall_score,f1_score

df=pd.read_csv("DATASET/incident_event_log.csv")

#print(df.duplicated().sum())
#print(df['category'].value_counts())
#print(df['made_sla'].value_counts())

#for col in df.columns:
    #count = (df[col] == '?').sum()
    #if count > 0:
        #print(f"{col}: {count} question marks")

#==========================================================DATA CLEANING=====================================================================================

df.replace('?',pd.NA,inplace=True)         


cols_to_drop=['cmdb_ci','vendor','caused_by','problem_id','rfc','u_symptom','sys_created_by','sys_created_at']           #removing useless columns
df.drop(columns=cols_to_drop,inplace=True)
#print(df.columns)

#df['caller_id'].fillna('system',inplace=True)
df=df.copy()
df['caller_id']=df['caller_id'].fillna('system')


#print(df['caller_id'].isnull().sum())

df['opened_by']=df['opened_by'].fillna('unknown')

#print('result2:',df['opened_by'].isnull().sum())

df['location']=df['location'].fillna('unknown')
#print('result3:',df['location'].isnull().sum())

df.dropna(subset=['category'],inplace=True)                        #// for dropping missing rows of a particular column
#print('result4:',df['category'].isnull().sum())

df['subcategory']=df['subcategory'].fillna('unknown')

#print('result5:',df['subcategory'].isnull().sum())

df['assignment_group']=df['assignment_group'].fillna('unassigned')

# print('result5:',df['assignment_group'].isnull().sum())

df['assigned_to']=df['assigned_to'].fillna('unassigned')

#print('result9:',df['assigned_to'].isnull().sum())

df['closed_code']=df['closed_code'].fillna('unknown')

df['resolved_by']=df['resolved_by'].fillna('unknown')
df.dropna(subset=['resolved_at'],inplace=True)

#print(df.isnull().sum())




#============================================================================================================================================================



#df['opened_at']=pd.to_datetime(df['opened_at'])
#df['resolved_at']=pd.to_datetime(df['resolved_at'])
#df['resolution_time']=(df['resolved_at']-df['opened_at']).dt.total_seconds()/3600
#print(df['resolution_time'].describe())
#print('neg_val:',(df['resolution_time']<0).sum())                              #// alot neg values means date cleaning is required,coz date format difference.


df['opened_at']=pd.to_datetime(df['opened_at'],dayfirst=True)
df['resolved_at']=pd.to_datetime(df['resolved_at'],dayfirst=True)
df['resolution_time']=(df['resolved_at']-df['opened_at']).dt.total_seconds()/3600
#print(df['resolution_time'].describe())
#print('neg_val:',(df['resolution_time']<0).sum())                                      # To check if any tickets resolved in negative time

#==============================================================================================================================================================

#df.to_csv('DATASET/itsm_cleaned.csv',index=False)

#=====================================================Prediction using M.L==========================================================================

y=df['made_sla'].apply(lambda x:0 if x==True else 1)     # orcould have used y=df['made_sla].map({True:0,False:1})    #// Target
#x=df[['priority','category','subcategory','assignment_group']]
x = df[['priority', 'category', 'subcategory', 
        'assignment_group', 'impact', 'urgency',
        'reopen_count', 'sys_mod_count',
        'reassignment_count']]

x = pd.get_dummies(x, drop_first=True)




x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
        n_estimators=100,
        class_weight='balanced',
        random_state=42
)
model.fit(x_train, y_train)

# Lower threshold
y_proba = model.predict_proba(x_test)[:,1]
y_pred = (y_proba >= 0.3).astype(int)

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))



#print(x_train.shape)
#print(x_test.shape)

#model = LogisticRegression(max_iter=1000,class_weight='balanced')
#model.fit(x_train, y_train)

# Predicted class (0 or 1)
#y_pred = model.predict(x_test)

# Predicted probability (IMPORTANT)
#y_prob_full = model.predict_proba(x)[:, 1]
#y_prob_test=model.predict_proba(x_test)[:,1]
#y_pred_new=(y_prob_test>=0.6).astype(int)

#print(y_prob[:10])



# Accuracy
#print("Accuracy:", accuracy_score(y_test, y_pred))

# Confusion Matrix
#print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Full Report
#print("Classification Report:\n", classification_report(y_test, y_pred))

#feature_importance = pd.DataFrame({
    #'feature': x_train.columns,
    #'importance':
    #model.feature_importance: abs(model.coef_[0])})



feature_importance_df = pd.DataFrame({
    'feature': x_train.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

feature_importance_df.to_csv('feature_importance.csv', index=False)

feature_importance = feature_importance_df.sort_values(by='importance', ascending=False)

#print(feature_importance.head(10))


df['breach_probability'] = y_proba

def risk_level(prob):
    if prob >= 0.7:
        return "High Risk"
    elif prob >= 0.4:
        return "Medium Risk"
    else:
        return "Low Risk"

df['risk_category'] = df['breach_probability'].apply(risk_level)
#print(df['risk_category'].head(10))
df.to_csv("ITSM_FINAL2.csv", index=False)
accuracy=accuracy_score(y_test,y_pred)
df['Accuracy']=accuracy
precision=precision_score(y_test,y_pred)
df['Precision']=precision
recall=recall_score(y_test,y_pred)
df['Recall']=recall
f1=f1_score(y_test,y_pred)
df['f1']=f1
df['predicted_breach']=model.predict(x)
df['actual_breach']=y
df.to_csv('Dataset/Itsm_cleaned3.csv',index=False)
feature_importance.to_csv('feature_importance.csv', index=False)
#print(df['resolution_time'].describe())
df['Resolution_time_hrs']=(df['resolution_time']/60)
#print(df['Resolution_time_hrs'].describe())


#print(df.columns)
df.to_csv('Dataset/Itsm_cleaned3.csv',index=False)
