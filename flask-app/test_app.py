import sqlite3
import pytest
import app as flexo_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_db = tmp_path / "test_flexo.db"

    conn = sqlite3.connect(test_db)
    conn.execute("""
        CREATE TABLE plate_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_number TEXT NOT NULL,
            job_name TEXT NOT NULL,
            department TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

    def test_db_connection():
        conn = sqlite3.connect(test_db)
        conn.row_factory = sqlite3.Row
        return conn

    monkeypatch.setattr(
        flexo_app,
        "get_db_connection",
        test_db_connection
    )

    flexo_app.app.config["TESTING"] = True

    with flexo_app.app.test_client() as client:
        yield client


def test_dashboard_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_new_request_page_loads(client):
    response = client.get("/new-request")
    assert response.status_code == 200



def test_create_plate_request(client):
    test_data = {
        "job_number": "1300002",
        "job_name": "PyTest Sample Job",
        "department": "Film",
        "quantity": "4",
        "priority": "High"
    }

    response = client.post(
        "/new-request",
        data=test_data,
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"1300002" in response.data

    # Query the same isolated test database
    conn = flexo_app.get_db_connection()
    record = conn.execute(
        "SELECT * FROM plate_requests WHERE job_number = ?",
        ("1300002",)
    ).fetchone()
    conn.close()

    assert record is not None
    assert record["job_name"] == "PyTest Sample Job"
    assert record["department"] == "Film"
    assert record["quantity"] == 4
    assert record["priority"] == "High"
    assert record["status"] == "Requested"


    assert response.status_code == 200
    assert b"1300002" in response.data

   
def test_persistence_accuracy(client):
    successful = 0
    total = 10

    for i in range(total):
        job_number = f"TEST-{i + 1:03d}"

        response = client.post(
            "/new-request",
            data={
                "job_number": job_number,
                "job_name": f"Test Job {i + 1}",
                "department": "Film",
                "quantity": "2",
                "priority": "High"
            },
            follow_redirects=True
        )

        conn = flexo_app.get_db_connection()
        records = conn.execute(
            "SELECT * FROM plate_requests WHERE job_number = ?",
            (job_number,)
        ).fetchall()
        conn.close()

        if (
            response.status_code == 200
            and len(records) == 1
            and records[0]["job_name"] == f"Test Job {i + 1}"
            and records[0]["department"] == "Film"
            and records[0]["quantity"] == 2
            and records[0]["priority"] == "High"
            and records[0]["status"] == "Requested"
        ):
            successful += 1

    accuracy = (successful / total) * 100

    print(f"\nValid requests submitted: {total}")
    print(f"Correctly persisted: {successful}")
    print(f"Persistence accuracy: {accuracy:.2f}%")

    assert successful == total

 
def test_rejects_negative_quantity(client):
    response = client.post(
        "/new-request",
        data={
            "job_number": "999004",
            "job_name": "Backend Negative Quantity Test",
            "department": "Film",
            "quantity": "-5",
            "priority": "High"
        },
        follow_redirects=False
    )

    assert response.status_code == 400

    # Confirm that invalid data was not saved
    conn = flexo_app.get_db_connection()
    record = conn.execute(
        "SELECT * FROM plate_requests WHERE job_number = ?",
        ("999004",)
    ).fetchone()
    conn.close()

    assert record is None



def test_rejects_empty_job_number(client):
    response = client.post(
        "/new-request",
        data={
            "job_number": "",
            "job_name": "Empty Job Number Test",
            "department": "Film",
            "quantity": "2",
            "priority": "High"
        },
        follow_redirects=False
    )

    # Flask must reject the invalid request
    assert response.status_code == 400

    # Verify that the invalid request was not saved
    conn = flexo_app.get_db_connection()
    record = conn.execute(
        "SELECT * FROM plate_requests WHERE job_name = ?",
        ("Empty Job Number Test",)
    ).fetchone()
    conn.close()

    assert record is None


def test_rejects_nonnumeric_quantity(client):
    response = client.post(
        "/new-request",
        data={
            "job_number": "999006",
            "job_name": "Invalid Text Quantity Test",
            "department": "Film",
            "quantity": "abc",
            "priority": "High"
        },
        follow_redirects=False
    )

    assert response.status_code == 400

    # Verify the invalid record was not saved
    conn = flexo_app.get_db_connection()
    record = conn.execute(
        "SELECT * FROM plate_requests WHERE job_number = ?",
        ("999006",)
    ).fetchone()
    conn.close()

    assert record is None



def test_rejects_invalid_workflow_status(client):
    # Create a valid request in the temporary database
    response = client.post(
        "/new-request",
        data={
            "job_number": "999007",
            "job_name": "Workflow Status Test",
            "department": "Film",
            "quantity": "2",
            "priority": "High"
        }
    )

    assert response.status_code == 302

    conn = flexo_app.get_db_connection()
    job = conn.execute(
        "SELECT * FROM plate_requests WHERE job_number = ?",
        ("999007",)
    ).fetchone()

    assert job is not None
    job_id = job["id"]
    conn.close()

    # Attempt to submit an unauthorized status value
    response = client.post(
        f"/job/{job_id}",
        data={"status": "Invalid Status"},
        follow_redirects=False
    )

    assert response.status_code == 400

    # Confirm the original status was not changed
    conn = flexo_app.get_db_connection()
    record = conn.execute(
        "SELECT status FROM plate_requests WHERE id = ?",
        (job_id,)
    ).fetchone()
    conn.close()

    assert record["status"] == "Requested"


def test_valid_workflow_status_update(client):
    # Create a request in the isolated test database
    response = client.post(
        "/new-request",
        data={
            "job_number": "999008",
            "job_name": "Valid Status Update Test",
            "department": "Film",
            "quantity": "2",
            "priority": "High"
        },
        follow_redirects=False
    )

    assert response.status_code == 302

    # Find the saved request
    conn = flexo_app.get_db_connection()
    job = conn.execute(
        "SELECT id, status FROM plate_requests WHERE job_number = ?",
        ("999008",)
    ).fetchone()

    assert job is not None
    assert job["status"] == "Requested"

    job_id = job["id"]
    conn.close()

    # Change the status to Plate Making
    response = client.post(
        f"/job/{job_id}",
        data={"status": "Plate Making"},
        follow_redirects=False
    )

    assert response.status_code == 302

    # Verify the new status in SQLite
    conn = flexo_app.get_db_connection()
    updated_job = conn.execute(
        "SELECT status FROM plate_requests WHERE id = ?",
        (job_id,)
    ).fetchone()
    conn.close()

    assert updated_job["status"] == "Plate Making"



def test_database_persistence_after_reconnection(client):
    # Create a request through Flask
    response = client.post(
        "/new-request",
        data={
            "job_number": "999009",
            "job_name": "Database Reconnection Test",
            "department": "Film",
            "quantity": "3",
            "priority": "Normal"
        },
        follow_redirects=False
    )

    assert response.status_code == 302

    # First database connection
    conn = flexo_app.get_db_connection()
    record = conn.execute(
        "SELECT * FROM plate_requests WHERE job_number = ?",
        ("999009",)
    ).fetchone()

    assert record is not None
    conn.close()

    # Reopen the database using a new connection
    conn = flexo_app.get_db_connection()
    recovered_record = conn.execute(
        "SELECT * FROM plate_requests WHERE job_number = ?",
        ("999009",)
    ).fetchone()
    conn.close()

    assert recovered_record is not None
    assert recovered_record["job_name"] == "Database Reconnection Test"
    assert recovered_record["quantity"] == 3
    assert recovered_record["status"] == "Requested"
