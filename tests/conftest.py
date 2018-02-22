import os
import shutil
import pytest

from autoscorum.genesis import Genesis
from autoscorum.node import Node
from autoscorum.docker_controller import DockerController
from autoscorum.wallet import Wallet

from autoscorum.node import TEST_TEMP_DIR
from autoscorum.docker_controller import DEFAULT_IMAGE_NAME

acc_name = "initdelegate"
acc_public_key = "SCR7R1p6GyZ3QjW3LrDayEy9jxbbBtPo9SDajH5QspVdweADi7bBi"
acc_private_key = "5K8ZJUYs9SP47JgzUY97ogDw1da37yuLrSF5syj2Wr4GEvPWok6"


def pytest_addoption(parser):
    parser.addoption('--image', metavar='image', default=DEFAULT_IMAGE_NAME, help='specify image for tests run')


@pytest.fixture(scope='session')
def image(request):
    return request.config.getoption('--image')


@pytest.fixture(scope='function', autouse=True)
def temp_dir():
    try:
        os.mkdir(TEST_TEMP_DIR)
    except FileExistsError:
        shutil.rmtree(TEST_TEMP_DIR)
        os.mkdir(TEST_TEMP_DIR)

    yield

    try:
        shutil.rmtree(TEST_TEMP_DIR)
    except FileNotFoundError:
        pass


@pytest.fixture()
def genesis():
    g = Genesis()
    g["accounts_supply"] = "210100.000000000 SCR"
    g["rewards_supply"] = "1000000.000000000 SCR"

    g.add_account(acc_name=acc_name,
                  public_key=acc_public_key,
                  scr_amount="110000.000000000 SCR",
                  witness=True)
    g.add_account(acc_name='alice',
                  public_key="SCR8TBVkvbJ79L1A4e851LETG8jurXFPzHPz87obyQQFESxy8pmdx",
                  scr_amount="100000.000000000 SCR")
    g.add_account(acc_name='bob',
                  public_key="SCR7w8tySAVQmJ95xSL8SS2GJJCws9s2gCY85DSAEALMFPmaMKA6p",
                  scr_amount="100.000000000 SCR")

    g["founders_supply"] = "100.000000000 SP"
    g["founders"] = [{"name": "alice",
                      "sp_percent": 70.1},
                     {"name": "bob",
                      "sp_percent": 29.9}]
    g["steemit_bounty_accounts_supply"] = "300.100000000 SP"
    g["steemit_bounty_accounts"] = [{"name": "initdelegate",
                                     "sp_amount": "210.000000000 SP"},
                                    {"name": "bob",
                                     "sp_amount": "90.100000000 SP"}]
    return g


@pytest.fixture(scope='function')
def node(genesis, docker):
    n = Node(genesis=genesis, logging=False)
    n.config['witness'] = '"{acc_name}"'.format(acc_name=acc_name)
    n.config['private-key'] = acc_private_key
    n.config['public-api'] = "database_api login_api account_by_key_api"
    n.config['enable-plugin'] = 'witness account_history account_by_key'

    docker.run_node(n)
    yield n
    if n.logging:
        n.read_logs()
        print(n.logs)


@pytest.fixture(scope='function')
def docker(image):
    d = DockerController(image)
    yield d
    d.stop_all()


@pytest.fixture(scope='function')
def wallet(node):
    with Wallet(node, [acc_private_key]) as w:
        w.login("", "")
        w.get_api_by_name('database_api')
        w.get_api_by_name('network_broadcast_api')
        w.get_block(1, wait_for_block=True)
        yield w