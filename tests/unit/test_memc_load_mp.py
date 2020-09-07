import pytest
import os
from memc_load_mp import dot_rename, parse_appsinstalled


def test_valid_dot_rename():
    path = 'test.test'
    open(path, 'tw').close()
    dot_rename(path)
    assert os.path.exists('.test.test')
    os.remove('.test.test')


@pytest.mark.parametrize(
    'test_value',
    [
        (
            'idfa\t02b073ec7f1b2a64d3e299e0cb1a07b1\t-144.976035927\t-82.9647017005\t5084,1834',
            [5084, 1834],
            '02b073ec7f1b2a64d3e299e0cb1a07b1',
            'idfa',
            -144.976035927,
            -82.9647017005
        ),
        (
            'adid\t2acbf9c0ce8574094a0a2f8e2f79be28\t114.160722202\t41.2874119411\t6886,9693,6483,2560',
            [6886, 9693, 6483, 2560],
            '2acbf9c0ce8574094a0a2f8e2f79be28',
            'adid',
            114.160722202,
            41.2874119411
        ),
        (
            'adid\t0a5c84feff00bde903af1b438498e720\t-67.683392459\t-1.18233697714\t3868,3585,8745,4179,7843,6674',
            [3868, 3585, 8745, 4179, 7843, 6674],
            '0a5c84feff00bde903af1b438498e720',
            'adid',
            -67.683392459,
            -1.18233697714
        ),
        (
            'adid\t2acbf9c0ce8574094a0a2f8e2f79be28\ttest\tqwe\t6886,9693,6483,2560',
            [6886, 9693, 6483, 2560],
            '2acbf9c0ce8574094a0a2f8e2f79be28',
            'adid',
            'test',
            'qwe'
        ),
        (
            'adid\t0a5c84feff00bde903af1b438498e720\t-67.683392459\t-1.18233697714\t3868,qwe,8745,4179,7843,6674',
            [3868, 8745, 4179, 7843, 6674],
            '0a5c84feff00bde903af1b438498e720',
            'adid',
            -67.683392459,
            -1.18233697714
        ),

    ]
)
def test_valid_parse_installed(test_value):
    line, apps, dev_id, dev_type, lat, lon = test_value
    app_installed = parse_appsinstalled(line)
    assert app_installed.apps == apps
    assert app_installed.dev_id == dev_id
    assert app_installed.dev_type == dev_type
    assert app_installed.lat == lat
    assert app_installed.lon == lon


@pytest.mark.parametrize(
    'test_value',
    [
        (
            '02b073ec7f1b2a64d3e299e0cb1a07b1\t-144.976035927\t-82.9647017005\t5084,1834',
            [5084, 1834],
            '02b073ec7f1b2a64d3e299e0cb1a07b1',
            'idfa',
            -144.976035927,
            -82.9647017005
        ),
        (
            '\t2acbf9c0ce8574094a0a2f8e2f79be28\t114.160722202\t41.2874119411\t6886,9693,6483,2560',
            [6886, 9693, 6483, 2560],
            '2acbf9c0ce8574094a0a2f8e2f79be28',
            'adid',
            114.160722202,
            41.2874119411
        ),
        (
            'adid\t\t-67.683392459\t-1.18233697714\t3868,3585,8745,4179,7843,6674',
            [3868, 3585, 8745, 4179, 7843, 6674],
            '0a5c84feff00bde903af1b438498e720',
            'adid',
            -67.683392459,
            -1.18233697714
        ),

    ]
)
def test_invalid_parse_installed(test_value):
    line, apps, dev_id, dev_type, lat, lon = test_value
    app_installed = parse_appsinstalled(line)
    assert app_installed is None
