import from approved exact content


def test_health_endpoint_returns_healthy_status(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_employee_returns_created_employee_and_defaults_active(
    client: TestClient,
) -> None:
    response = client.post(
        "/employees",
        json={
            "name": "Jane Smith",
            "email": "Jane.Smith@Example.com",
            "department": "Engineering",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["name"] == "Jane Smith"
    assert body["email"] == "jane.smith@example.com"
    assert body["department"] == "Engineering"
    assert body["active"] is True


def test_create_employee_strips_required_text_fields(
    client: TestClient,
) -> None:
    response = client.post(
        "/employees",
        json=employee_payload(
            name="  Jane Smith  ",
            email="jane@example.com",
            department="  Engineering  ",
        ),
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Jane Smith"
    assert response.json()["department"] == "Engineering"


def test_list_and_get_employees(client: TestClient) -> None:
    first = create_employee(client, email="first@example.com")
    second = create_employee(client, email="second@example.com")

    list_response = client.get("/employees")
    get_response = client.get(f"/employees/{first['id']}")

    assert list_response.status_code == 200
    assert [employee["id"] for employee in list_response.json()] == [
        first["id"],
        second["id"],
    ]
    assert get_response.status_code == 200
    assert get_response.json() == first


def test_duplicate_employee_email_is_case_insensitive(
    client: TestClient,
) -> None:
    create_employee(client, email="duplicate@example.com")

    response = client.post(
        "/employees",
        json=employee_payload(email="DUPLICATE@EXAMPLE.COM"),
    )

    assert_application_error(
        response,
        status=409,
        code="DUPLICATE_EMPLOYEE_EMAIL",
        message=(
            "An employee with email 'duplicate@example.com' already exists."
        ),
    )


@pytest.mark.parametrize("field", ["name", "department"])
def test_blank_employee_text_fields_are_rejected(
    client: TestClient,
    field: str,
) -> None:
    payload = employee_payload()
    payload[field] = "   "

    response = client.post("/employees", json=payload)

    assert_validation_error(response)
    detail = validation_detail(response, field)
    assert detail["msg"] == "Value must not be blank."


@pytest.mark.parametrize(
    "payload",
    [
        {
            "email": "valid@example.com",
            "department": "Engineering",
        },
        {
            "name": "Jane Smith",
            "department": "Engineering",
        },
        {
            "name": "Jane Smith",
            "email": "valid@example.com",
        },
    ],
)
def test_missing_required_employee_fields_are_rejected(
    client: TestClient,
    payload: dict,
) -> None:
    response = client.post("/employees", json=payload)

    assert_validation_error(response)


def test_invalid_employee_email_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/employees",
        json=employee_payload(email="not-an-email"),
    )

    assert_validation_error(response)
    detail = validation_detail(response, "email")
    assert detail["loc"] == ["body", "email"]


def test_missing_employee_returns_structured_not_found_error(
    client: TestClient,
) -> None:
    response = client.get("/employees/999")

    assert_application_error(
        response,
        status=404,
        code="EMPLOYEE_NOT_FOUND",
        message="Employee 999 was not found.",
    )


@pytest.mark.parametrize("path", ["/employees/0", "/employees/-1"])
def test_employee_identifier_must_be_positive(
    client: TestClient,
    path: str,
) -> None:
    response = client.get(path)

    assert_validation_error(response)


def test_create_leave_request_defaults_to_pending(
    client: TestClient,
) -> None:
    employee = create_employee(client)
    response = client.post(
        "/leave-requests",
        json=leave_payload(employee["id"]),
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "employee_id": employee["id"],
        "leave_type": "ANNUAL",
        "start_date": "2025-06-02",
        "end_date": "2025-06-06",
        "reason": "Annual vacation",
        "status": "PENDING",
    }


def test_leave_request_normalizes_blank_reason_to_null(
    client: TestClient,
) -> None:
    employee = create_employee(client)

    response = client.post(
        "/leave-requests",
        json=leave_payload(employee["id"], reason="   "),
    )

    assert response.status_code == 201
    assert response.json()["reason"] is None


@pytest.mark.parametrize("leave_type", ["ANNUAL", "SICK", "PERSONAL"])
def test_all_supported_leave_types_are_accepted(
    client: TestClient,
    leave_type: str,
) -> None:
    employee = create_employee(client)

    response = client.post(
        "/leave-requests",
        json=leave_payload(employee["id"], leave_type=leave_type),
    )

    assert response.status_code == 201
    assert response.json()["leave_type"] == leave_type


def test_equal_start_and_end_dates_are_valid(client: TestClient) -> None:
    employee = create_employee(client)

    response = client.post(
        "/leave-requests",
        json=leave_payload(
            employee["id"],
            start_date="2025-06-06",
            end_date="2025-06-06",
        ),
    )

    assert response.status_code == 201
    assert response.json()["start_date"] == "2025-06-06"
    assert response.json()["end_date"] == "2025-06-06"


def test_leave_request_with_start_date_after_end_date_is_rejected(
    client: TestClient,
) -> None:
    employee = create_employee(client)

    response = client.post(
        "/leave-requests",
        json=leave_payload(
            employee["id"],
            start_date="2025-06-07",
            end_date="2025-06-06",
        ),
    )

    assert_validation_error(response)
    detail = validation_detail(response, "body")
    assert detail["msg"] == "Value error, start_date must not be after end_date."


def test_invalid_leave_type_is_rejected(client: TestClient) -> None:
    employee = create_employee(client)

    response = client.post(
        "/leave-requests",
        json=leave_payload(employee["id"], leave_type="MATERNITY"),
    )

    assert_validation_error(response)


def test_invalid_leave_dates_are_rejected(client: TestClient) -> None:
    employee = create_employee(client)

    response = client.post(
        "/leave-requests",
        json=leave_payload(
            employee["id"],
            start_date="not-a-date",
            end_date="2025-06-06",
        ),
    )

    assert_validation_error(response)


def test_missing_leave_request_fields_are_rejected(
    client: TestClient,
) -> None:
    employee = create_employee(client)

    response = client.post(
        "/leave-requests",
        json={"employee_id": employee["id"]},
    )

    assert_validation_error(response)


def test_leave_request_requires_existing_employee(
    client: TestClient,
) -> None:
    response = client.post(
        "/leave-requests",
        json=leave_payload(999),
    )

    assert_application_error(
        response,
        status=404,
        code="EMPLOYEE_NOT_FOUND",
        message="Employee 999 was not found.",
    )


def test_inactive_employee_cannot_submit_leave(
    client: TestClient,
) -> None:
    employee = create_employee(
        client,
        email="inactive@example.com",
        active=False,
    )

    response = client.post(
        "/leave-requests",
        json=leave_payload(employee["id"]),
    )

    assert_application_error(
        response,
        status=409,
        code="INACTIVE_EMPLOYEE",
        message=(
            f"Employee {employee['id']} is inactive and cannot submit leave."
        ),
    )


def test_list_all_and_employee_specific_leave_requests(
    client: TestClient,
) -> None:
    first_employee = create_employee(client, email="first@example.com")
    second_employee = create_employee(client, email="second@example.com")

    first_request = create_leave_request(client, first_employee["id"])
    second_request = create_leave_request(
        client,
        second_employee["id"],
        leave_type="SICK",
    )

    all_response = client.get("/leave-requests")
    employee_response = client.get(
        f"/employees/{first_employee['id']}/leave-requests"
    )

    assert all_response.status_code == 200
    assert [item["id"] for item in all_response.json()] == [
        first_request["id"],
        second_request["id"],
    ]
    assert employee_response.status_code == 200
    assert employee_response.json() == [first_request]


def test_employee_specific_leave_requests_require_existing_employee(
    client: TestClient,
) -> None:
    response = client.get("/employees/999/leave-requests")

    assert_application_error(
        response,
        status=404,
        code="EMPLOYEE_NOT_FOUND",
        message="Employee 999 was not found.",
    )


def test_pending_leave_request_can_be_approved(
    client: TestClient,
) -> None:
    employee = create_employee(client)
    leave_request = create_leave_request(client, employee["id"])

    response = client.patch(
        f"/leave-requests/{leave_request['id']}/approve"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "APPROVED"


def test_pending_leave_request_can_be_rejected(
    client: TestClient,
) -> None:
    employee = create_employee(client)
    leave_request = create_leave_request(client, employee["id"])

    response = client.patch(
        f"/leave-requests/{leave_request['id']}/reject"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "REJECTED"


def test_approved_leave_request_cannot_be_transitioned_or_deleted(
    client: TestClient,
) -> None:
    employee = create_employee(client)
    leave_request = create_leave_request(client, employee["id"])
    request_id = leave_request["id"]

    approve_response = client.patch(
        f"/leave-requests/{request_id}/approve"
    )
    transition_response = client.patch(
        f"/leave-requests/{request_id}/reject"
    )
    delete_response = client.delete(f"/leave-requests/{request_id}")

    assert approve_response.status_code == 200
    expected_message = (
        f"Leave request {request_id} has status APPROVED "
        "and cannot be transitioned."
    )
    assert_application_error(
        transition_response,
        status=409,
        code="INVALID_LEAVE_STATUS",
        message=expected_message,
    )
    assert_application_error(
        delete_response,
        status=409,
        code="INVALID_LEAVE_STATUS",
        message=(
            f"Leave request {request_id} has status APPROVED "
            "and cannot be deleted."
        ),
    )


def test_rejected_leave_request_cannot_be_transitioned_or_deleted(
    client: TestClient,
) -> None:
    employee = create_employee(client)
    leave_request = create_leave_request(client, employee["id"])
    request_id = leave_request["id"]

    reject_response = client.patch(
        f"/leave-requests/{request_id}/reject"
    )
    approve_response = client.patch(
        f"/leave-requests/{request_id}/approve"
    )
    delete_response = client.delete(f"/leave-requests/{request_id}")

    assert reject_response.status_code == 200
    assert_application_error(
        approve_response,
        status=409,
        code="INVALID_LEAVE_STATUS",
        message=(
            f"Leave request {request_id} has status REJECTED "
            "and cannot be transitioned."
        ),
    )
    assert_application_error(
        delete_response,
        status=409,
        code="INVALID_LEAVE_STATUS",
        message=(
            f"Leave request {request_id} has status REJECTED "
            "and cannot be deleted."
        ),
    )


def test_pending_leave_request_can_be_deleted(
    client: TestClient,
) -> None:
    employee = create_employee(client)
    leave_request = create_leave_request(client, employee["id"])
    request_id = leave_request["id"]

    response = client.delete(f"/leave-requests/{request_id}")
    get_response = client.get(f"/leave-requests/{request_id}")

    assert response.status_code == 204
    assert response.content == b""
    assert_application_error(
        get_response,
        status=404,
        code="LEAVE_REQUEST_NOT_FOUND",
        message=f"Leave request {request_id} was not found.",
    )


@pytest.mark.parametrize(
    "method,path",
    [
        ("patch", "/leave-requests/999/approve"),
        ("patch", "/leave-requests/999/reject"),
        ("delete", "/leave-requests/999"),
    ],
)
def test_missing_leave_request_returns_not_found_error(
    client: TestClient,
    method: str,
    path: str,
) -> None:
    response = getattr(client, method)(path)

    assert_application_error(
        response,
        status=404,
        code="LEAVE_REQUEST_NOT_FOUND",
        message="Leave request 999 was not found.",
    )


@pytest.mark.parametrize(
    "path",
    [
        "/leave-requests/0/approve",
        "/leave-requests/-1/approve",
        "/leave-requests/0/reject",
        "/leave-requests/-1/reject",
        "/leave-requests/0",
        "/leave-requests/-1",
    ],
)
def test_leave_request_identifier_must_be_positive(
    client: TestClient,
    path: str,
) -> None:
    method = "delete" if path.count("/") == 2 else "patch"
    response = getattr(client, method)(path)

    assert_validation_error(response)
