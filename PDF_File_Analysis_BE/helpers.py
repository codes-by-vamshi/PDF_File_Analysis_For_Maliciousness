from Preprocessing import PdfFilePreprocessing
from joblib import load
import numpy as np
import os
import subprocess

def pdf_to_bin(file_path):
    with open(file_path,'r') as pdf_file:
        pdf_binary_data = pdf_file.read()
        file_name = os.path.basename(file_path)
        with open(f"{'/'.join(file_path.split('/')[:-1])}/{file_name}.bin",'w') as bin_file:
            bin_file.write(pdf_binary_data)
    os.remove(file_path)

def json_to_df(folder_path):
    obj = PdfFilePreprocessing(folder_path)
    df = obj.df
    df['file_size'] = df['file_size'].str.replace('-',230.0) # Avg file size
    df['file_size'] = df['file_size'].astype('float64')
    return df

def malicious_predictions(df):
    rf1 = load('rf_model1.joblib')
    rf2 = load('rf_model2.joblib')
    rf3 = load('rf_model3.joblib')
    rf4 = load('rf_model4.joblib')
    rf5 = load('rf_model5.joblib')
    gb1 = load('gb_model1.joblib')
    gb2 = load('gb_model2.joblib')
    gb3 = load('gb_model3.joblib')
    gb4 = load('gb_model4.joblib')
    gb5 = load('gb_model5.joblib')
    xgb1 = load('xgb_model1.joblib')
    xgb2 = load('xgb_model2.joblib')
    xgb3 = load('xgb_model3.joblib')
    xgb4 = load('xgb_model4.joblib')
    xgb5 = load('xgb_model5.joblib')

    df = df.rename(columns={"['linearized']": 'linearized'})
    df = df.rename(columns={"['invalid_xref_table']": 'invalid_xref_table'})

    rf_pred1 = rf1.predict(df)
    gb_pred1 = gb1.predict(df)
    xgb_pred1 = xgb1.predict(df)

    rf_pred2 = rf2.predict(df)
    gb_pred2 = gb2.predict(df)
    xgb_pred2 = xgb2.predict(df)

    rf_pred3 = rf3.predict(df)
    gb_pred3 = gb3.predict(df)
    xgb_pred3 = xgb3.predict(df)

    rf_pred4 = rf4.predict(df)
    gb_pred4 = gb4.predict(df)
    xgb_pred4 = xgb4.predict(df)

    rf_pred5 = rf5.predict(df)
    gb_pred5 = gb5.predict(df)
    xgb_pred5 = xgb5.predict(df)

    finalPred = []
    for i in range(len(rf_pred1)):
        c = rf_pred1[i]+gb_pred1[i]+xgb_pred1[i]+rf_pred2[i]+gb_pred2[i]+xgb_pred2[i]+rf_pred3[i]+gb_pred3[i]+xgb_pred3[i]+rf_pred4[i]+gb_pred4[i]+xgb_pred4[i]+rf_pred5[i]+gb_pred5[i]+xgb_pred5[i]
        if(c == 15):
            finalPred.append(1)
        else:
            finalPred.append(0)
    finalPred = np.array(finalPred)
    return finalPred