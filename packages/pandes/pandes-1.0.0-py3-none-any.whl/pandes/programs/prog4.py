def get_code():
    return '''
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix

df= pd.read_csv("enjoy_sport.csv")

label_encoders={}
for columns in df.columns:
    le=LabelEncoder()
    df[columns]=le.fit_transform(df[columns])
    label_encoders[columns]=le

X=df.iloc[:,:-1]
y=df.iloc[:,-1]

x_train, x_test, y_train, y_test= train_test_split(X, y, test_size=0.3,random_state=42)

model=GaussianNB()
model.fit(x_train, y_train)

y_pred= model.predict(x_test)
print("Accuracy:\n", accuracy_score(y_test, y_pred))

cm= confusion_matrix(y_test, y_pred)
print("COnfusion matrix:\n", cm)

new_instance= ["Sunny", "Cool", "High", "Strong"]
new_instance_encoded=[ label_encoders[col].transform([val])[0]
                       for col,val in zip(df.columns[:-1], new_instance)]

new_instance_df = pd.DataFrame([new_instance_encoded], columns=X.columns)
prediction = model.predict(new_instance_df)
predicted_label= label_encoders[df.columns[-1]].inverse_transform(prediction)

print("Predicted label:", predicted_label[0])
'''