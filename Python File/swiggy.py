import numpy as np
import pandas as pd
import streamlit as st
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder , MinMaxScaler
from sklearn.linear_model import LogisticRegression , LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
pd.set_option("display.max_columns",None)

df = pd.read_csv("C:\\Users\\Manpreet\\Desktop\\Masai\\Swiggy Project\\Swiggy Model.csv")

print(df)

feedback_file_path = "feedback.xlsx"
feedback_data = pd.DataFrame()  



def save_feedback(name, feedback):
    global feedback_data
    feedback_data = feedback_data.append({"Name": name, "Feedback": feedback}, ignore_index=True)
    feedback_data.to_excel(feedback_file_path, index=False)
    print("Feedback saved successfully.")


def load_feedback_data():
    global feedback_data
    try:
        feedback_data = pd.read_excel(feedback_file_path)
    except FileNotFoundError:
        feedback_data = pd.DataFrame({"Name": [], "Feedback": []})





def predict_price(Cuisine, Location):
    df2=pd.read_csv("C:\\Users\\Manpreet\\Desktop\\Masai\\Swiggy Project\\Swiggy Model.csv")
    df3=df2[['Cusines','Location','Price_for_one','Ratings','Delivery_review_no']]
    
    cat_lr=["Cusines","Location"]
    num_lr=["Ratings","Delivery_review_no"]
    for i in num_lr:
        q1=df3[i].quantile(0.25)
        q3=df3[i].quantile(0.75)
        iqr=q3-q1
        ul = q3 + 1.5*iqr
        ll = q1 - 1.5*iqr

        for c in df3[i]:
            if c > ul:
                df3[i] = df3[i].replace(c,ul)
            elif c < ll:
                df3[i] = df3[i].replace(c,ll)


    loc = df3["Location"].unique()    
    locate= sorted(loc)
    print(locate)


    food = df3["Cusines"].unique() 
    cus = sorted(food)
    print(cus)

    dict1 = {}
    for i in range(len(locate)):
        dict1[locate[i]] = i 

    dict2 = {}
    for i in range(len(cus)):
        dict2[cus[i]] = i
    
    le = LabelEncoder()
    df3['Cusines']=le.fit_transform(df3['Cusines'])
    df3['Location']=le.fit_transform(df3['Location'])

    f1=dict2[Cuisine]
    l1=dict1[Location]

    df1_new=df3[(df3['Cusines']==f1) | (df3['Location']==l1)]
    print(df1_new)

    X=df1_new.drop(['Price_for_one'],axis=1)
    y=df1_new['Price_for_one']

    lr=LinearRegression()
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=10)
    lr.fit(X_train,y_train)

    return round(lr.predict(X_test).mean())


def predict_location(Cuisine, Location, Preferred_Price_For_1):
    df = pd.read_csv("C:\\Users\\Manpreet\\Desktop\\Masai\\Swiggy Project\\Swiggy Model.csv")
    z = pd.DataFrame({"Cusines": [Cuisine], "Location": [Location], "Price_for_one": [Preferred_Price_For_1]})

    print(z)

    df = pd.concat([df, z])
    lst = df["Location"].unique()

    dict1 = {}
    for i in range(len(lst)):
        dict1[lst[i]] = i

    dict2 = {}
    for i in range(len(lst)):
        dict2[i] = lst[i]

    df["Location"] = df["Location"].apply(lambda x: dict1[x])
    df = df[["Cusines", "Location", "Price_for_one"]]  # Remove "Index" from the selected columns
    X = df.drop("Location", axis=1)
    y = df["Location"]

    le = LabelEncoder()
    X["Cusines"] = le.fit_transform(X["Cusines"])
    X["Price_for_one"] = MinMaxScaler().fit_transform(X[["Price_for_one"]])  # Normalize only "Price_For_One"

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=17)
    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    return dict2[y_pred[-1]]


st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://miro.medium.com/v2/resize:fit:1080/1*1lpknH8EtyPqDQtSshTM7Q.jpeg');
        background-size: cover;
        }

    .stApp::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5); /* Change the last value (0.5) to adjust the opacity */
        pointer-events: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)



def main():


    
    st.markdown("<h1 style='text-align: center; color: lime; padding: 20px; background-color: maroon;'>RECOMMENDATION MODEL</h1>", unsafe_allow_html=True)
    
    html_temp = """
    <div style = 'background-color: orange ; padding : 0px ; max-width: 400px; margin: 20px auto;'>
    <h1 style = "color: black ;text-align:center;"><b>SWIGGY</b></h1>
    </div>
    """


    st.markdown(html_temp, unsafe_allow_html = True)

    cuisines = df['Cusines'].unique()
    st.markdown("<h2 style='font-size: 24px;margin-bottom: 0px;'><span style='color: cyan ;'><b>Cuisine:</b></h2>", unsafe_allow_html=True)
    Cuisine = st.selectbox("",cuisines)

    locations = df['Location'].unique()
    st.markdown("<h2 style='font-size: 24px;margin-bottom: 0px;'><span style='color: cyan;'>Preferred Location:</h2>", unsafe_allow_html=True)
    Preferred_Location = st.selectbox("",locations) 

    st.markdown("<h2 style='font-size: 24px;margin-bottom: 0px;'><span style='color: cyan;'>Preferred Price For One:</h2>", unsafe_allow_html=True)
    Preferred_Price_For_1 = st.text_input("", key="price_input")
    
    if st.button("Submit"):

        avg = round(df[(df['Cusines'] == Cuisine) | (df['Location'] == Preferred_Location)]['Price_for_one'].mean())

        a = df[(df['Location'] == Preferred_Location)]
        Pop_Cuis = a[a['Ratings'] == a['Ratings'].max()]["Cusines"]
        Pop_Cuis=Pop_Cuis.iloc[0]

        Most_Popular_Rest = a[a["Delivery_review_no"] == a["Delivery_review_no"].max()]["Restaurant_Name"]
        Most_Popular_Rest=Most_Popular_Rest.iloc[0]

        Ser = a[a["Delivery_review_no"] == a["Delivery_review_no"].max()]["Cusines"]
        Serves=Ser.iloc[0]

        b = a[(a['Cusines'] == Cuisine)]
        Popular_Rest_Serving_Your_Cuisine = b[b["Delivery_review_no"] == b["Delivery_review_no"].max()]['Restaurant_Name']
        Popular_Rest_Serving_Your_Cuisine=Popular_Rest_Serving_Your_Cuisine.iloc[0]


        Recomm_price = predict_price(Cuisine,Preferred_Location)
        Recomm_location = predict_location(Cuisine,Preferred_Location,Preferred_Price_For_1)


        st.markdown("<span style='color: yellow; font-weight: bold; font-size: 30px;'>Popular Cuisine:   {}</span>".format(Pop_Cuis), unsafe_allow_html=True)
        
        st.markdown("<span style='color: yellow; font-weight: bold; font-size: 30px;'>Average Price for 1:   {}</span>".format(avg), unsafe_allow_html=True)

        st.markdown("<span style='color: yellow; font-weight: bold; font-size: 30px;'>Most Popular Restaurant:  {}</span>".format(Most_Popular_Rest), unsafe_allow_html=True)
        
        st.markdown("<span style='color: yellow; font-weight: bold; font-size: 30px;'>Serves:  {}</span>".format(Serves), unsafe_allow_html=True)
        
        st.markdown("<span style='color: yellow; font-weight: bold; font-size: 30px;'>Popular Restaurant that serves your Cuisine: {}</span>".format(Popular_Rest_Serving_Your_Cuisine), unsafe_allow_html=True)
       
        st.markdown("<span style='color: yellow; font-weight: bold; font-size: 30px;'>Recommended Price:  {}</span>".format(Recomm_price), unsafe_allow_html=True)
        
        # st.markdown("<span style='color: yellow; font-weight: bold; font-size: 30px;'>Recommended Location:  {}</span>".format(Recomm_location), unsafe_allow_html=True)



# Add feedback section
    load_feedback_data()
    st.markdown("<h1 style='text-align: center; color: aqua;'>FEEDBACK</h1>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='font-size: 24px;margin-bottom: 0px;'><span style='color: cyan;'><b>Name</b></h2>", unsafe_allow_html=True)
    name = st.text_input("")
    st.markdown("<h2 style='font-size: 24px;margin-bottom: 0px;'><span style='color: cyan;'>Feedback</h2>", unsafe_allow_html=True)
    feedback = st.text_area("")
    if st.button("submit"):
        save_feedback(name, feedback)
        st.markdown("<span style='color: green; font-weight: bold; font-size: 35px;'>Feedback submitted successfully!</span>", unsafe_allow_html=True)
        
               
if __name__ == '__main__':
    main()