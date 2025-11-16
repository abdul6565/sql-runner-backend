import requests
import json

# Test login
login_url = 'http://127.0.0.1:8001/api/v1/token'
login_data = {'username': 'admin', 'password': 'admin123'}
login_response = requests.post(login_url, data=login_data)
print('Login Response:', login_response.json())

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    # Test query
    query_url = 'http://127.0.0.1:8001/api/v1/query'
    query_data = {'query': 'SELECT * FROM Customers'}
    query_response = requests.post(query_url, headers=headers, json=query_data)
    print('Query Response Status:', query_response.status_code)
    print('Query Response:', query_response.json())

    # Test another query
    query_data2 = {'query': 'SELECT first_name, age FROM Customers WHERE age > 25'}
    query_response2 = requests.post(query_url, headers=headers, json=query_data2)
    print('Query2 Response Status:', query_response2.status_code)
    print('Query2 Response:', query_response2.json())
else:
    print('Login failed')
