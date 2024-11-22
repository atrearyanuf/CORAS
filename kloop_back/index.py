from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import pandas as pd
import re
import json

#define azure cognos search setting

service_name = 'kloop-chat'
index_name = 'kloop_data'
admin_key = 'qyWk52YoLZpmL9JY7zASrmVU21GhkPbG0XsMvSa3xAAzSeCxC4cy'
endpoint = f"https://{service_name}.search.windows.net/"
credential = AzureKeyCredential(admin_key)


#loading the data as the dataframe.


file_path = 'customer_support_tickets.csv'

df = pd.read_csv(file_path)
df_cleaned = df.dropna()

searchclient = SearchClient(endpoint=endpoint, index_name=index_name,credential=credential)

data = []


for _, row in df_cleaned.iterrows():
    data.append({
        '@search.action': 'upload',
        "Ticket" : str(row['Ticket ID']),
        "TicketType" : str(row['Ticket Type']),
        "CustomerName" : str(row['Customer Name']),
        "CustomerEmail" : str(row['Customer Email']),
        "CustomerAge" : str(row['Customer Age']),
        "CustomerGender" : str(row['Customer Gender']),
        "ProductPurchased" : str(row['Product Purchased']),
        "DateOfPurchase" : pd.to_datetime(row['Date of Purchase'], errors='coerce').isoformat() + 'Z',
        "TicketSubject" : str(row['Ticket Subject']),
        "TicketDescription" : str(row['Ticket Description']),
        "TicketStatus" : str(row['Ticket Status']),
        "Resolution" : str(row['Resolution']),
        "TicketPriority" : str(row['Ticket Priority']),
        "TicketChannel" : str(row['Ticket Channel']),
        "FirstResponseTime" :  pd.to_datetime(row['First Response Time'], errors='coerce').isoformat() + 'Z' if pd.notnull(row['First Response Time']) else None,
        "TimetoResolution" : pd.to_datetime(row['Time to Resolution'], errors='coerce').isoformat() + 'Z' if pd.notnull(row['Time to Resolution']) else None,
        "CustomerSatisfactionRating" : float(row['Customer Satisfaction Rating'])})
    
result = searchclient.upload_documents(data)
print(result)