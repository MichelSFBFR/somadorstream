import streamlit as st
import pdfplumber
import re
import os

# Custom function to format numbers in Brazilian currency format
def format_currency(value):
    # Format the number as a string with commas and periods for thousands and decimal places
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Function to extract and sum financial values (R$) from the PDF
def extract_and_sum_financial_values(pdf_path):
    total_sum = 0
    pattern = re.compile(r'R\$ ?[\d\.,]+')
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    financial_values = pattern.findall(text)
                    for value in financial_values:
                        # Replace commas with periods for decimal conversion
                        value_cleaned = value.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
                        total_sum += float(value_cleaned)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None
    
    return total_sum

# Streamlit UI layout
st.title("GRC/CP - Somador de R$ em certidão")
st.write("Faça o upload de um arquivo PDF para somar os valores em (R$) dentro dele.")

# Upload file
uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")

# Process file if uploaded
if uploaded_file is not None:
    # Save uploaded file temporarily
    temp_file_path = os.path.join("temp", uploaded_file.name)
    if not os.path.exists("temp"):
        os.makedirs("temp")
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract and sum values
    result = extract_and_sum_financial_values(temp_file_path)
    if result is not None:
        formatted_result = format_currency(result)
        st.success(f"Soma total dos valores em (R$): {formatted_result}")
    else:
        st.error("Falha ao processar ao arquivo PDF.")
