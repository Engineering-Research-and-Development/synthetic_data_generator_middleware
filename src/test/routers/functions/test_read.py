def test_get_all_functions(client):
    response = client.get("/functions/")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)

    if body:
        item = body[0]
        assert "function" in item

        function = item["function"]
        assert "id" in function
        assert "name" in function
        assert "description" in function
        assert "function_reference" in function


def test_get_function_parameters_by_id_success(client):
    # get a valid function id
    all_functions = client.get("/functions/").json()
    assert len(all_functions) > 0

    function_id = all_functions[0]["function"]["id"]

    response = client.get(f"/functions/{function_id}")

    assert response.status_code == 200
    body = response.json()

    assert "function" in body
    assert "parameters" in body

    parameters = body["parameters"]
    assert isinstance(parameters, list)

    if parameters:
        param = parameters[0]
        assert "name" in param
        assert "value" in param
        assert "parameter_type" in param


def test_get_function_parameters_by_id_not_found(client):
    response = client.get("/functions/999999")

    assert response.status_code == 404
    assert response.json() == "Function not found"
