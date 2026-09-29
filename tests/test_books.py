import pytest

def assert_error_response(response, status_code, code):
    assert response.status_code == status_code
    body = response.json(); assert set(body) == {"status","code","message","errors"}; assert body["status"] == status_code; assert body["code"] == code; assert isinstance(body["message"], str); assert isinstance(body["errors"], list)
def create_book(client, payload):
    response = client.post("/books", json=payload); assert response.status_code == 201; return response.json()
def test_health_endpoint(client):
    response = client.get("/health"); assert response.status_code == 200; assert response.json() == {"status":"ok"}
def test_create_book(client, book_payload):
    body = create_book(client, book_payload); assert body["title"] == book_payload["title"]; assert body["isbn"] == book_payload["isbn"]
def test_create_book_accepts_zero_price_and_quantity(client, book_payload):
    body = create_book(client, {**book_payload,"isbn":"9780000000001","price":0,"quantity":0}); assert body["price"] == 0; assert body["quantity"] == 0
def test_retrieve_all_books(client, book_payload):
    first=create_book(client,book_payload); second=create_book(client,{**book_payload,"title":"Domain-Driven Design","author":"Eric Evans","isbn":"9780321125217"}); assert client.get("/books").json() == [first,second]
def test_retrieve_book_by_id(client, book_payload):
    created=create_book(client,book_payload); response=client.get(f"/books/{created['id']}"); assert response.status_code == 200; assert response.json() == created
def test_update_book(client, book_payload):
    created=create_book(client,book_payload); payload={**book_payload,"title":"Updated","price":54.99,"quantity":12}; response=client.put(f"/books/{created['id']}",json=payload); assert response.status_code == 200; assert response.json()["title"] == "Updated"
def test_update_book_rejects_duplicate_isbn(client, book_payload):
    first=create_book(client,book_payload); second=create_book(client,{**book_payload,"isbn":"9780000000002"}); assert_error_response(client.put(f"/books/{second['id']}",json={**book_payload,"isbn":first["isbn"]}),409,"DUPLICATE_ISBN")
def test_delete_book(client, book_payload):
    created=create_book(client,book_payload); response=client.delete(f"/books/{created['id']}"); assert response.status_code == 204; assert_error_response(client.get(f"/books/{created['id']}"),404,"BOOK_NOT_FOUND")
def test_search_books_by_title(client, book_payload):
    create_book(client,book_payload); create_book(client,{**book_payload,"title":"Domain-Driven Design","author":"Eric Evans","isbn":"9780321125217"}); results=client.get("/books",params={"q":"PRAGMATIC"}).json(); assert len(results)==1
def test_search_books_by_author(client, book_payload):
    create_book(client,book_payload); create_book(client,{**book_payload,"title":"Domain-Driven Design","author":"Eric Evans","isbn":"9780321125217"}); results=client.get("/books",params={"q":"evans"}).json(); assert len(results)==1
def test_blank_search_query_returns_all_books(client, book_payload):
    first=create_book(client,book_payload); second=create_book(client,{**book_payload,"isbn":"9780321125217"}); assert client.get("/books",params={"q":"   "}).json()==[first,second]
def test_duplicate_isbn_returns_conflict_error(client, book_payload):
    create_book(client,book_payload); assert_error_response(client.post("/books",json=book_payload),409,"DUPLICATE_ISBN")
@pytest.mark.parametrize("field",["title","author","isbn","category"])
def test_missing_required_field_returns_validation_error(client,book_payload,field):
    assert_error_response(client.post("/books",json={k:v for k,v in book_payload.items() if k!=field}),422,"VALIDATION_ERROR")
@pytest.mark.parametrize("field",["title","author","isbn","category"])
@pytest.mark.parametrize("blank_value",["","   "])
def test_blank_required_field_returns_validation_error(client,book_payload,field,blank_value):
    assert_error_response(client.post("/books",json={**book_payload,field:blank_value}),422,"VALIDATION_ERROR")
@pytest.mark.parametrize("field",["price","quantity"])
def test_negative_numeric_values_are_rejected(client,book_payload,field):
    assert_error_response(client.post("/books",json={**book_payload,"isbn":field,"price":-1 if field=="price" else 1,"quantity":-1 if field=="quantity" else 1}),422,"VALIDATION_ERROR")
def test_missing_book_returns_not_found_error(client): assert_error_response(client.get("/books/999999"),404,"BOOK_NOT_FOUND")
@pytest.mark.parametrize("method",["get","put","delete"])
def test_operations_on_missing_book_return_not_found_error(client,book_payload,method):
    response=client.put("/books/999999",json=book_payload) if method=="put" else getattr(client,method)("/books/999999"); assert_error_response(response,404,"BOOK_NOT_FOUND")
def test_malformed_book_id_returns_validation_error(client): assert_error_response(client.get("/books/not-an-integer"),422,"VALIDATION_ERROR")