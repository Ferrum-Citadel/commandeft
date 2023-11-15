from commandeft.constants.consts import Models


def test_get_models_list():
    expected_models = [Models.GPT_3_5_TURBO, Models.GPT_4, Models.GPT_4_TURBO]
    models_list = Models.get_models_list()
    assert isinstance(models_list, list)
    assert models_list == expected_models
