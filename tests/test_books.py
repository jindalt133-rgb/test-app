import copy

import pytest
from fastapi.testclient import TestClient


VALID_BOOK = {
    "title": "The Pragmatic Programmer",
    "author": "Andrew Hunt",
    "isbn": "9780135957059",
    "publication_year": 1999,
    "genre": "Software Development",
    "available": True,
}


def create_book(client: TestClient, **overrides) -> dict:
    payload = copy.deepcopy(VALID_BOOK)
    payload.update(overrides)

    response = client.post("/books", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


def assert_validation_error(
    response,
    expected_fields: set[str] | None = None,
) -> None:
    assert response.status_code == 422

    body = response.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["message"] == "Request validation failed"
    assert isinstance(body["error"]["details"], list)

    if expected_fields is not None:
        actual_fields = {
            detail["field"] for detail in body["error"]["details"]
        }
        assert expected_fields.issubset(actual_fields)


def assert_application_error(
    response,
    *,
    status_code: int,
    code: str,
    message: str,
) -> None:
    assert response.status_code == status_code
    assert response.json() == {
        "error": {
            "code": code,
            "message": message,
        }
    }


def test_create_book_returns_created_book(client: TestClient) -> None:
    response = client.post("/books", json=VALID_BOOK)

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        **VALID_BOOK,
    }


def test_create_book_trims_text_and_defaults_available(
    client: TestClient,
) -> None:
    response = client.post(
        "/books",
        json={
            "title": "  Clean Code  ",
            "author": "  Robert C. Martin ",
            "isbn": "  9780132350884 ",
            "publication_year": 2008,
            "genre": "  Programming ",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "publication_year": 2008,
        "genre": "Programming",
        "available": True,
    }


def test_list_books_returns_empty_catalog(client: TestClient) -> None:
    response = client.get("/books")

    assert response.status_code == 200
    assert response.json() == []


def test_list_books_returns_books_in_id_order(client: TestClient) -> None:
    first = create_book(client, isbn="isbn-1", title="First Book")
    second = create_book(client, isbn="isbn-2", title="Second Book")

    response = client.get("/books")

    assert response.status_code == 200
    assert [book["id"] for book in response.json()] == [
        first["id"],
        second["id"],
    ]


def test_get_book_returns_existing_book(client: TestClient) -> None:
    created = create_book(client)

    response = client.get(f"/books/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_book_returns_not_found_error(client: TestClient) -> None:
    response = client.get("/books/999")

    assert_application_error(
        response,
        status_code=404,
        code="BOOK_NOT_FOUND",
        message="Book with ID 999 was not found",
    )


def test_update_book_replaces_all_fields(client: TestClient) -> None:
    created = create_book(client)

    replacement = {
        "title": "Refactoring",
        "author": "Martin Fowler",
        "isbn": "9780201485677",
        "publication_year": 1999,
        "genre": "Software Engineering",
        "available": False,
    }

    response = client.put(
        f"/books/{created['id']}",
        json=replacement,
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": created["id"],
        **replacement,
    }


def test_update_book_allows_same_isbn(client: TestClient) -> None:
    created = create_book(client)

    response = client.put(
        f"/books/{created['id']}",
        json={
            **VALID_BOOK,
            "title": "Updated Title",
        },
    )

    assert response.status_code == 200
    assert response.json()["isbn"] == VALID_BOOK["isbn"]
    assert response.json()["title"] == "Updated Title"


def test_update_missing_book_returns_not_found_error(
    client: TestClient,
) -> None:
    response = client.put("/books/999", json=VALID_BOOK)

    assert_application_error(
        response,
        status_code=404,
        code="BOOK_NOT_FOUND",
        message="Book with ID 999 was not found",
    )


def test_delete_book_returns_no_content_and_removes_book(
    client: TestClient,
) -> None:
    created = create_book(client)

    response = client.delete(f"/books/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""

    missing_response = client.get(f"/books/{created['id']}")
    assert_application_error(
        missing_response,
        status_code=404,
        code="BOOK_NOT_FOUND",
        message=f"Book with ID {created['id']} was not found",
    )


def test_delete_missing_book_returns_not_found_error(
    client: TestClient,
) -> None:
    response = client.delete("/books/999")

    assert_application_error(
        response,
        status_code=404,
        code="BOOK_NOT_FOUND",
        message="Book with ID 999 was not found",
    )


def test_duplicate_isbn_on_create_returns_conflict(
    client: TestClient,
) -> None:
    create_book(client)

    response = client.post(
        "/books",
        json={
            **VALID_BOOK,
            "title": "Another Book",
        },
    )

    assert_application_error(
        response,
        status_code=409,
        code="DUPLICATE_ISBN",
        message="A book with this ISBN already exists",
    )


def test_duplicate_isbn_on_update_returns_conflict(
    client: TestClient,
) -> None:
    first = create_book(client, isbn="isbn-1")
    second = create_book(client, isbn="isbn-2")

    response = client.put(
        f"/books/{second['id']}",
        json={
            **VALID_BOOK,
            "isbn": first["isbn"],
        },
    )

    assert_application_error(
        response,
        status_code=409,
        code="DUPLICATE_ISBN",
        message="A book with this ISBN already exists",
    )


@pytest.mark.parametrize("field", ["title", "author", "isbn", "genre"])
def test_required_text_field_missing_returns_validation_error(
    client: TestClient,
    field: str,
) -> None:
    payload = copy.deepcopy(VALID_BOOK)
    del payload[field]

    response = client.post("/books", json=payload)

    assert_validation_error(response, {field})


@pytest.mark.parametrize("field", ["title", "author", "isbn", "genre"])
@pytest.mark.parametrize("blank_value", ["", "   ", "\t\n"])
def test_blank_text_field_returns_validation_error(
    client: TestClient,
    field: str,
    blank_value: str,
) -> None:
    payload = copy.deepcopy(VALID_BOOK)
    payload[field] = blank_value

    response = client.post("/books", json=payload)

    assert_validation_error(response, {field})

    details = response.json()["error"]["details"]
    assert any(
        detail["field"] == field
        and detail["message"] == "Field must not be blank"
        for detail in details
    )


@pytest.mark.parametrize(
    ("field", "maximum"),
    [
        ("title", 255),
        ("author", 255),
        ("isbn", 50),
        ("genre", 255),
    ],
)
def test_text_field_accepts_maximum_length(
    client: TestClient,
    field: str,
    maximum: int,
) -> None:
    payload = copy.deepcopy(VALID_BOOK)
    payload[field] = "x" * maximum

    response = client.post("/books", json=payload)

    assert response.status_code == 201
    assert response.json()[field] == "x" * maximum


@pytest.mark.parametrize(
    ("field", "maximum"),
    [
        ("title", 255),
        ("author", 255),
        ("isbn", 50),
        ("genre", 255),
    ],
)
def test_text_field_rejects_length_above_maximum(
    client: TestClient,
    field: str,
    maximum: int,
) -> None:
    payload = copy.deepcopy(VALID_BOOK)
    payload[field] = "x" * (maximum + 1)

    response = client.post("/books", json=payload)

    assert_validation_error(response, {field})


@pytest.mark.parametrize("year", [1, 9999])
def test_publication_year_accepts_inclusive_boundaries(
    client: TestClient,
    year: int,
) -> None:
    response = client.post(
        "/books",
        json={
            **VALID_BOOK,
            "publication_year": year,
        },
    )

    assert response.status_code == 201
    assert response.json()["publication_year"] == year


@pytest.mark.parametrize("year", [0, 10000])
def test_publication_year_rejects_outside_boundaries(
    client: TestClient,
    year: int,
) -> None:
    response = client.post(
        "/books",
        json={
            **VALID_BOOK,
            "publication_year": year,
        },
    )

    assert_validation_error(response, {"publication_year"})


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("title", 123),
        ("author", ["not", "a", "string"]),
        ("isbn", None),
        ("publication_year", "not-a-number"),
        ("genre", {"invalid": "object"}),
        ("available", "not-a-boolean"),
    ],
)
def test_invalid_field_type_returns_validation_error(
    client: TestClient,
    field: str,
    invalid_value,
) -> None:
    payload = copy.deepcopy(VALID_BOOK)
    payload[field] = invalid_value

    response = client.post("/books", json=payload)

    assert_validation_error(response, {field})


def test_missing_request_body_returns_validation_error(
    client: TestClient,
) -> None:
    response = client.post("/books")

    assert_validation_error(response, {"request"})


def test_malformed_json_returns_validation_error(
    client: TestClient,
) -> None:
    response = client.post(
        "/books",
        content='{"title": "Incomplete"',
        headers={"Content-Type": "application/json"},
    )

    assert_validation_error(response)


def test_non_integer_book_id_returns_validation_error(
    client: TestClient,
) -> None:
    response = client.get("/books/not-an-integer")

    assert_validation_error(response, {"book_id"})
