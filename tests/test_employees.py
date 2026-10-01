def validation(response):
 assert response.status_code==422
 assert response.json()['error']['code']=='VALIDATION_ERROR'
def test_create_employee(client,employee_payload):
 r=client.post('/employees',json=employee_payload); assert r.status_code==201; assert r.json()['name']=='Alex Morgan'
def test_default_active(client):
 r=client.post('/employees',json={'name':'A','email':'a@example.com','department':'D'}); assert r.json()['active'] is True
def test_inactive(client):
 r=client.post('/employees',json={'name':'A','email':'a@example.com','department':'D','active':False}); assert r.json()['active'] is False
def test_list(client,create_employee):
 a=create_employee(email='a@example.com'); b=create_employee(email='b@example.com'); assert [x['id'] for x in client.get('/employees').json()]==[a['id'],b['id']]
def test_get(client,create_employee):
 e=create_employee(); assert client.get(f"/employees/{e['id']}").json()==e
def test_missing(client): assert client.get('/employees/999999').status_code==404
def test_duplicate(client,create_employee):
 create_employee(email='a@example.com'); assert client.post('/employees',json={'name':'B','email':'a@example.com','department':'D'}).status_code==409
def test_blank(client):
 for field in ('name','email','department'):
  p={'name':'A','email':'a@example.com','department':'D'}; p[field]=' '; validation(client.post('/employees',json=p))
def test_missing_field(client): validation(client.post('/employees',json={'name':'A','department':'D'}))
def test_malformed(client): validation(client.post('/employees',content='{"name":"x"',headers={'content-type':'application/json'}))
def test_bad_id(client): validation(client.get('/employees/no'))
