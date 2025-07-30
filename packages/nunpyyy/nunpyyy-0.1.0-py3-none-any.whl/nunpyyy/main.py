def run(n):
    programs = {
        1: '''# candidate Algorithm
import numpy as np
import pandas as pd
# import numpy as np
import pandas as pd

dataset=pd.read_csv('2.csv')

concepts=np.array(dataset.iloc[:,0:-1])
target=np.array(dataset.iloc[:,-1])

def learn(concepts,target):
    specific_h=concepts[0].copy()
    print('Initial Specific Hypothesis:\n',specific_h)
    general_h=[['?' for i in range(len(specific_h))] for i in range(len(specific_h))]
    print("General Hypothesis:\n",general_h)

    for i,h in enumerate(concepts):
        if target[i]=='yes':
            print("If Instance is Postivie")
            for x in range(len(specific_h)):
                if h[x]!=specific_h[x]:
                    specific_h[x]='?'
                    general_h[x][x]='?'

        if target[i]=='no':
            print("If Instance is Negative")    
            for x in range(len(specific_h)):
                if h[x]!=specific_h[x]:
                    general_h[x][x]=specific_h[x]
                else:
                    general_h[x][x]='?'
        print(" step{}: " .format(i+1))
        print("Specific hypothesis: ",specific_h)
        print("General Hypothesis: ",general_h)
        
    indices=[i for i, val in enumerate(general_h) if val==['?','?','?','?','?','?']]
    for i in indices:
        general_h.remove(['?','?','?','?','?','?'])

    return specific_h,general_h

s_final,g_final=learn(concepts,target)
print("Specific Hypothesis: \n",s_final,sep="\n")
print("General Hypothesis: \n",g_final,sep="\n")
    
''',

        2: '''# NaiveID3 Bayes
from sklearn.naive_bayes import GaussianNB
# from sklearn.datasets import load_iris 
from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier, plot_tree

from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

import matplotlib.pyplot as plt

iris = load_iris()

X = iris.data

y = iris.target

feature_names = iris.feature_names

class_names = iris.target_names

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, 

random_state=42)

clf = DecisionTreeClassifier(criterion='entropy', random_state=42)

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

cm = confusion_matrix(y_test, y_pred)

acc = accuracy_score(y_test, y_pred)

print("Confusion Matrix:")

print(cm)
''',

        3: '''import numpy as np

X=np.array([[2,9],[1,5],[3,6]])
y=np.array([[92],[86],[89]])


X=X/np.amax(X,axis=0) #Chances of Error
y=y/100
class NeuralNetwork:
    def __init__(self):
        self.input_size=2
        self.hidden_size=3
        self.output_size=1
        self.weights_input_hidden=np.random.rand(self.input_size,self.hidden_size)
        self.weights_hidden_output=np.random.rand(self.hidden_size,self.output_size)

    def sigmoid(self,x):
        return (1/(1+np.exp(-x)))

    def sigmoid_prime(self,x):
        return x*(1-x)

    def forward(self,input_data):
        self.input_layer=input_data
        self.hidden_input=np.dot(self.input_layer,self.weights_input_hidden)
        self.hidden_output=self.sigmoid(self.hidden_input)

        self.final_input=np.dot(self.hidden_output,self.weights_hidden_output)
        self.predicted_output=self.sigmoid(self.final_input)

        return self.predicted_output

    def backward(self,target_output):
        error=target_output-self.predicted_output
        output_delta=error*self.sigmoid_prime(self.predicted_output)

        hidden_error=output_delta.dot(self.weights_hidden_output.T)
        hidden_delta=hidden_error*self.sigmoid_prime(self.hidden_output) #Chances of Error

        self.weights_input_hidden+=self.input_layer.T.dot(hidden_delta) 
        self.weights_hidden_output+=self.hidden_output.T.dot(output_delta)

    def train(self,X,y):
        self.forward(X)
        self.backward(y)

NN=NeuralNetwork()

print("Input: \n",X)
print("Predicted Output: ",NN.forward(X))
print("Loss Before Training:\n ",np.mean(np.square(y-NN.forward(X))))


NN.train(X,y)
print("Predicted Output: \n",NN.forward(X))
print("Loss After Training:\n ",np.mean(np.square(y-NN.forward(X))))

''',
        4: '''from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.metrics import confusion_matrix,accuracy_score

dataset=pd.read_csv('tennis.csv')
X=dataset.iloc[:,0:-1].copy()
y=dataset.iloc[:,-1]

print("Data Before Encoding\n",dataset.head())
print("Features Before Encoding\n",X.head())
print("Target Before Encoding\n",y.head())


label_encoder={}

for column in X.columns:
    le=LabelEncoder()
    X[column]=le.fit_transform(X[column])
    label_encoder[column]=le

print("Features After Encoding\n",X.head())

target_encoder=LabelEncoder()
y=target_encoder.fit_transform(y)


X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.30)
model=GaussianNB()
model.fit(X_train,y_train)

y_pred=model.predict(X_test)

print("Actual Label: ",y_test)
print("Predicted Label: ",y_pred)
print("Confusion Matrix: \n",confusion_matrix(y_test,y_pred))
print("Accuracy Score: ",accuracy_score(y_test,y_pred)*100)
''',
        5: '''from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import sklearn.metrics as sm

dataset=load_iris()

X=pd.DataFrame(dataset.data)
X.columns=['Sepal_Length','Sepal_Width','Petal_Length','Petal_Width']
y=pd.DataFrame(dataset.target)
y.columns=['Targets']

print(X)
colormap=np.array(['red','lime','black'])
plt.figure(figsize=(14,7))
plt.subplot(1,3,1)
plt.scatter(X.Petal_Length,X.Petal_Width,c=colormap[y.Targets],s=40)
plt.title("Real")


plt.subplot(1,3,2)
model=KMeans(n_clusters=3)
model.fit(X)
y_pred=np.choose(model.labels_,[0,1,2]).astype(np.int64)
plt.scatter(X.Petal_Length,X.Petal_Width,c=colormap[y_pred],s=40)
plt.title("KMeans")

#GMM



scaler=StandardScaler()
scaler.fit(X)

xsa=scaler.transform(X)
xs=pd.DataFrame(xsa,columns=X.columns)
gmm=GaussianMixture(n_components=3)
gmm.fit(xs)

y_cluster_gmm=gmm.predict(xs)
plt.subplot(1,3,3)
plt.scatter(X.Petal_Length,X.Petal_Width,c=colormap[y_cluster_gmm],s=40)
plt.title("GMM")

ari_kMeans=sm.adjusted_rand_score(y.Targets,y_pred)
ari_gmm=sm.adjusted_rand_score(y.Targets,y_cluster_gmm)
print(f"Adjusted Rank Index for K-Means: {ari_kMeans:.4f}")
print(f"Adjusted Rank Index for GMM: {ari_gmm:.4f}")

accuracy_kMeans=np.mean(y.Targets==y_pred)
accuracy_gmm=np.mean(y.Targets==y_cluster_gmm)
plt.show()
''',
        6: '''from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np


dataset=load_iris()

X_train,X_test,y_train,y_test=train_test_split(dataset.data,dataset.target,test_size=0.2,random_state=30)

print("Training Labels: ",y_train)
model=KNeighborsClassifier(n_neighbors=3)
model.fit(X_train,y_train)

for i in range(len(X_test)):
    x=X_test[i]
    x_new=np.array([x])
    y_pred=model.predict(x_new)

    print(f"Target: {dataset.target_names[y_test[i]]}, Predicted: {dataset.target_names[y_pred]}")


accuracy=model.score(X_test,y_test)
print("Accuracy Score: ",accuracy)
''',
        7: '''import numpy as np
import matplotlib.pyplot as plt

X=np.array([1,2,3,4,5])
y=np.array([1,2,1.3,3.75,2.25])

def gaussian_weights(X_query,X,y,tau):
    return np.exp(-((X-X_query)**2)/(2*tau**2))

def lwr(X_query,X,y,tau):
    Weights=gaussian_weights(X_query,X,y,tau)
    W=np.diag(Weights)
    x_mat=np.vstack([np.ones_like(X),X]).T
    theta=np.linalg.pinv(x_mat.T @ W @x_mat) @(x_mat.T @W @y)
    return np.array([1,X_query]) @theta,theta

X_query=3
tau=1.0

y_pred,theta=lwr(X_query,X,y,tau)

print("Observed value at x=3: ",y[X==X_query][0])
print(f"Predicted value at x=3: {y_pred:3f}")
print(f"Coefficients: Intercepts={theta[0]:.3f}, Slope={theta[1]:.3f}")

x_vals=np.linspace(1,5,100)
y_vals=[lwr(x,X,y,tau)[0] for x in x_vals]

plt.scatter(X,y,color='red',label='Data Points')
plt.plot(x_vals,y_vals,color='blue',label='LWR Prediction')
plt.scatter(X_query,y_pred,color='green',label='Predicted Value at x=3')
plt.scatter(X_query,y[X==X_query][0],color='orange',label='Observed value at x=3')

plt.legend()
plt.show()
''',
        8: '''from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score

dataset=load_iris()
X=dataset.data[:,:2] #Class 0 and #Class 1 chances of error
y=dataset.target

X=X[y!=2] #chacnes of error
y=y[y!=2]

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=42)

scaler=StandardScaler()
X_train_scaled=scaler.fit_transform(X_train)
X_test_scaled=scaler.transform(X_test)

model=SVC(kernel='linear')
model.fit(X_train_scaled,y_train)
y_pred=model.predict(X_test_scaled)



print(f"No of Support Vectors: ",len(model.support_vectors_))
print(f"Support Vectors:\n ", model.support_vectors_)
print(f"Accuracy Score: ",accuracy_score(y_test,y_pred))

x_min,x_max=X[:,0].min()-1,X[:,0].max()+1
y_min,y_max=X[:,1].min()-1,X[:,1].max()+1

xx,yy=np.meshgrid(np.arange(x_min,x_max,0.02),np.arange(y_min,y_max,0.02)) #chances of error

grid_points=np.c_[xx.ravel(),yy.ravel()]
grid_points_scaled=scaler.transform(grid_points)
Z=model.predict(grid_points_scaled).reshape(xx.shape)

plt.figure(figsize=(10,8))
plt.contourf(xx,yy,Z,alpha=0.8)
plt.scatter(X[y==0,0],X[y==0,1],color='red',label='Class 0')
plt.scatter(X[y==1,0],X[y==1,1,],color='green',label='Class 1')
sv_original=scaler.inverse_transform(model.support_vectors_)
plt.scatter(sv_original[:,0],sv_original[:,1],s=100,facecolors='none',edgecolors='blue',label='Support Vectors')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('SVM Classification with Linear Kernel')
plt.legend()
plt.show()
''',
        9: '''from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,accuracy_score,confusion_matrix

dataset=load_iris()

X_train,X_test,y_train,y_test=train_test_split(dataset.data,dataset.target,test_size=0.25,random_state=42)

model=RandomForestClassifier(n_estimators=100,random_state=42)
model.fit(X_train,y_train)
y_pred=model.predict(X_test)


print("Accuracy Score: ",accuracy_score(y_test,y_pred))

print("Classification Report: ",classification_report(y_test,y_pred))
print("Confusion Matrix: ",confusion_matrix(y_test,y_pred))
''',
        # add more if needed...
    }

    if n in programs:
        print(programs[n])
    else:
        print("Program not found. Please choose a valid number.")
