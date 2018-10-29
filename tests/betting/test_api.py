import pytest

from automation.wallet import Wallet
from tests.betting.conftest import GAME_FILTERS, empower_betting_moderator, create_game
from tests.common import gen_uid, DEFAULT_WITNESS, validate_response, validate_error_response, RE_OBJECT_NOT_EXIST
# from scorum.graphenebase.betting import wincase


@pytest.mark.parametrize('uuid', ['e629f9aa-6b2c-46aa-8fa8-36770e7a7a5f'])
def test_get_game_winners(wallet: Wallet, uuid):
    validate_error_response(wallet.get_game_winners(uuid), wallet.get_game_winners.__name__, RE_OBJECT_NOT_EXIST)
    # create game, create bet, match bet, end game
    # response = wallet.get_game_winners(uuid)
    # validate_response(response, wallet.get_game_winners.__name__)


def test_get_games_by_status(wallet: Wallet):

    def check(status):
        response = wallet.get_games_by_status([GAME_FILTERS.index(status)])
        validate_response(response, wallet.get_games_by_status.__name__)
        assert len(response) == 1, "Should be '%s' one game." % status
        assert response[0]['uuid'] == uuid

    assert wallet.get_games_by_status([0]) == [], "Games shouldn't be created yet."
    empower_betting_moderator(wallet, DEFAULT_WITNESS)
    uuid, block_num = create_game(wallet, DEFAULT_WITNESS, start=5)
    check("created")
    wallet.get_block(block_num + 1, wait_for_block=True)
    check("started")
    # print(wallet.post_game_results(uuid, DEFAULT_WITNESS, [wincase.ResultHomeYes()]))
    # check("finished")


def test_get_betting_properties(wallet: Wallet):
    validate_response(
        wallet.get_betting_properties(), wallet.get_betting_properties.__name__,
        [('moderator', ''), ('resolve_delay_sec', 86400)]
    )


def test_get_games_by_uuids(wallet: Wallet):
    assert wallet.get_games_by_uuids([gen_uid()]) == [], "Games shouldn't be created yet."
    empower_betting_moderator(wallet, DEFAULT_WITNESS)
    uuid = create_game(wallet, DEFAULT_WITNESS, delay=3600)
    response = wallet.get_games_by_uuids([uuid])
    validate_response(response, wallet.get_games_by_uuids.__name__)
    assert len(response) == 1, "Should be created %d game(s)." % 1
    assert response[0]['uuid'] == uuid
    assert response[0]['moderator'] == DEFAULT_WITNESS


def test_lookup_games_by_id(wallet: Wallet):
    assert wallet.lokup_games_by_id(10001, 100) == [], "Games shouldn't be created yet."
    empower_betting_moderator(wallet, DEFAULT_WITNESS)
    uuid = create_game(wallet, DEFAULT_WITNESS, delay=3600)
    response = wallet.lookup_games_by_id(-1, 100)
    validate_response(response, wallet.get_games_by_uuids.__name__)
    assert len(response) == 1, "Should be created one game."
    assert response[0]['uuid'] == uuid
    assert response[0]['moderator'] == DEFAULT_WITNESS


def test_get_matched_bets(wallet: Wallet):
    uuid = gen_uid()
    assert wallet.get_matched_bets([uuid]) == [], "Bets shouldn't be created yet."
    # create bet, match bet
    # response = wallet.get_matched_bets([uuid])
    # validate_response(response, wallet.get_matched_bets.__name__)


def test_lookup_matched_bets(wallet: Wallet):
    uuid = gen_uid()
    assert wallet.lookup_matched_bets(uuid, 100) == [], "Bets shouldn't be created yet."
    # create bet, match bet
    # response = wallet.lookup_matched_bets(uuid, 100)
    # validate_response(response, wallet.lookup_matched_bets.__name__)


def test_get_pending_bets(wallet: Wallet):
    uuid = gen_uid()
    assert wallet.get_pending_bets([uuid]) == [], "Bets shouldn't be created yet."
    # create bet
    # response = wallet.get_pending_bets([uuid])
    # validate_response(response, wallet.get_pending_bets.__name__)


def test_lookup_pending_bets(wallet: Wallet):
    uuid = gen_uid()
    assert wallet.lookup_pending_bets(uuid, 100) == [], "Bets shouldn't be created yet."
    # create bet, match bet
    # response = wallet.lookup_pending_bets(uuid, 100)
    # validate_response(response, wallet.lookup_pending_bets.__name__)
