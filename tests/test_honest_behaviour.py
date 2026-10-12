from usafiri_mcp import server

_fn = lambda name: (getattr(server, name).fn if hasattr(getattr(server, name), "fn") else getattr(server, name))


def test_an_unknown_ntsa_service_is_an_error_not_the_driving_licence_guide():
    r = _fn("ntsa_services_guide")("pilot licence")
    assert "error" in r and "driving_licence" in r["valid_services"] and "process" not in r


def test_a_known_ntsa_service_still_works():
    assert "process" in _fn("ntsa_services_guide")("driving licence")


def test_a_fare_outside_the_table_is_flagged_as_a_placeholder():
    known, other = _fn("matatu_route_finder")("Nairobi", "Thika"), _fn("matatu_route_finder")("Garissa", "Wajir")
    assert known["fare_is_placeholder"] is False and other["fare_is_placeholder"] is True and other["estimated_fare_kes"] == 500
