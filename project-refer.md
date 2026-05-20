# Result Demo when you are coding about controller
    print("=== Result Demo ===\n")

    success_result = Result.success(
        data={"user_id": 1, "username": "oldmerman"},
        message="Login successful",
        request="/api/auth/login"
    )
    print("Success Result:")
    print(success_result.model_dump_json(indent=2))
    print()

    error_result = Result.error(
        message="Invalid credentials",
        code=401,
        request="/api/auth/login"
    )
    print("Error Result:")
    print(error_result.model_dump_json(indent=2))
    print()

    paginated_result = Result.success(
        data={
            "items": [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"}
            ],
            "total": 2,
            "page": 1,
            "page_size": 10
        },
        message="Items retrieved",
        request="/api/items"
    )
    print("Paginated Result:")
    print(paginated_result.model_dump_json(indent=2))