import os,tempfile
from collections.abc import Generator
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
f=tempfile.NamedTemporaryFile(prefix='employee_leave_test_',suffix='.db',delete=False); f.close()
_DATABASE_PATH=Path(f.name); os.environ['DATABASE_URL']=f'sqlite:///{_DATABASE_PATH.as_posix()}'
from app.database.configuration import engine
from app.database.session import SessionLocal
from app.main import app
from app.models.employee import Base
@pytest.fixture(scope='session',autouse=True)
def create_test_schema():
 Base.metadata.create_all(bind=engine); yield; Base.metadata.drop_all(bind=engine); engine.dispose(); _DATABASE_PATH.unlink(missing_ok=True)
@pytest.fixture(autouse=True)
def isolate_test_data():
 yield
 db=SessionLocal()
 try:
  for table in reversed(Base.metadata.sorted_tables): db.execute(table.delete())
  db.commit()
 finally: db.close()
@pytest.fixture
def client():
 with TestClient(app) as c: yield c
@pytest.fixture
def employee_payload(): return {'name':'Alex Morgan','email':'alex.morgan@example.com','department':'Engineering','active':True}
@pytest.fixture
def create_employee(client):
 def f(*,email='employee@example.com',active=True,name='Test Employee',department='Engineering'):
  r=client.post('/employees',json={'name':name,'email':email,'department':department,'active':active}); assert r.status_code==201; return r.json()
 return f
@pytest.fixture
def create_leave_request(client,create_employee):
 def f(*,employee_id=None,leave_type='ANNUAL',start_date='2025-06-10',end_date='2025-06-14',reason='Planned vacation'):
  if employee_id is None: employee_id=create_employee()['id']
  r=client.post('/leave-requests',json={'employee_id':employee_id,'leave_type':leave_type,'start_date':start_date,'end_date':end_date,'reason':reason}); assert r.status_code==201; return r.json()
 return f
