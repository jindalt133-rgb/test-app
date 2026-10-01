def validation(r): assert r.status_code==422 and r.json()['error']['code']=='VALIDATION_ERROR'
def test_create(client,create_employee):
 e=create_employee(); r=client.post('/leave-requests',json={'employee_id':e['id'],'leave_type':'ANNUAL','start_date':'2025-06-10','end_date':'2025-06-14'}); assert r.status_code==201 and r.json()['status']=='PENDING'
def test_types(client,create_employee):
 for i,t in enumerate(('ANNUAL','SICK','PERSONAL')):
  e=create_employee(email=f'{i}@e.com'); assert client.post('/leave-requests',json={'employee_id':e['id'],'leave_type':t,'start_date':'2025-06-10','end_date':'2025-06-10'}).status_code==201
def test_missing_employee(client): assert client.post('/leave-requests',json={'employee_id':999,'leave_type':'ANNUAL','start_date':'2025-06-10','end_date':'2025-06-10'}).status_code==404
def test_inactive(client,create_employee):
 e=create_employee(active=False); assert client.post('/leave-requests',json={'employee_id':e['id'],'leave_type':'ANNUAL','start_date':'2025-06-10','end_date':'2025-06-10'}).status_code==409
def test_invalid_type(client,create_employee):
 e=create_employee(); validation(client.post('/leave-requests',json={'employee_id':e['id'],'leave_type':'BAD','start_date':'2025-06-10','end_date':'2025-06-10'}))
def test_range(client,create_employee):
 e=create_employee(); validation(client.post('/leave-requests',json={'employee_id':e['id'],'leave_type':'ANNUAL','start_date':'2025-06-11','end_date':'2025-06-10'}))
def test_approve(client,create_leave_request):
 r=create_leave_request(); assert client.post(f"/leave-requests/{r['id']}/approve").json()['status']=='APPROVED'
def test_reject(client,create_leave_request):
 r=create_leave_request(); assert client.post(f"/leave-requests/{r['id']}/reject").json()['status']=='REJECTED'
def test_delete(client,create_leave_request):
 r=create_leave_request(); assert client.delete(f"/leave-requests/{r['id']}").status_code==204
def test_transition(client,create_leave_request):
 r=create_leave_request(); client.post(f"/leave-requests/{r['id']}/approve"); assert client.post(f"/leave-requests/{r['id']}/approve").status_code==409
def test_missing_leave(client): assert client.post('/leave-requests/999/approve').status_code==404
def test_bad_leave_id(client): validation(client.post('/leave-requests/no/approve'))
