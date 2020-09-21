import pandas as pd
import numpy as np

# read csv file
df = pd.read_csv("Data_for_BMI_Calculator_Height_Weight.csv")
df.head(5)
# drop data with null value
df = df.dropna()
# drop data with gap between value
for i in df["Height (cm)"]:
    res = " " in i
    if res == True:
        df.drop(df[df['Height (cm)'] == i].index.values, inplace=True)
for i in df['Weight (Kg)']:
    res = "-" in i
    if res == True:
        df.drop(df[df['Weight (Kg)'] == i].index.values, inplace=True)

clean_df = df

#strip leading and trailing space for both the culumn
clean_df['Height (cm)'] = clean_df['Height (cm)'].str.strip()
clean_df['Weight (Kg)'] = clean_df['Weight (Kg)'].str.strip()

# convert cm to mtr in height coulumn
clean_df['Height (cm)']=clean_df['Height (cm)'].astype(int)/100

# calculate BMI as per the formula
clean_df['BMI Range (kg/m2)'] = clean_df['Weight (Kg)']%clean_df['Height (cm)']**2
bmi_category_lst = ['Underweight','Normal weight','Overweight','Moderately obese','Severely obese','Very severely obese']
health_risk_lst = ['Malnutrition risk','Low risk','Enhanced risk','Medium risk','High risk','Very high risk']
bmi_check = [(clean_df['BMI Range (kg/m2)']<'18.4'),(clean_df['BMI Range (kg/m2)']<'24.9'),(clean_df['BMI Range (kg/m2)']<'29.9'),
            (clean_df['BMI Range (kg/m2)']<'39.9'),(clean_df['BMI Range (kg/m2)']>'40')]

# add two new column to existing csv file
clean_df['BMI Category'] = np.select(bmi_check,bmi_category_lst)
clean_df['Health risk'] = np.select(bmi_check,health_risk_lst)

# calculate total overweight people
overweight_people = clean_df[(clean_df['BMI Range (kg/m2)'] >25) & (clean_df['BMI Range (kg/m2)'] <29.5)]
total_overweight_people = len(overweight_people)

# create new output csv file with selected existing column from input csv
clean_df = pd.read_csv('Data_for_BMI_Calculator_Height_Weight.csv' , usecols = ['BMI Category','BMI Range (kg/m2)','Health risk'])
clean_df.to_csv('Output_for_BMI_Calculator_Height_Weight.csv' , index = False)