def test_import_app():
    import importlib
    importlib.import_module("app")
    assert True