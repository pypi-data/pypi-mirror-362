import pytest
import json
from lolalytics_api.main import *


def _check_labels(data, labels):
    for label in labels:
        assert label in data, f"Missing label: {label}"


class TestGetTierlist:
    def test_invalid_lane_raises_error(self):
        with pytest.raises(InvalidLane):
            get_tierlist(5, "test", "gm+")

    def test_invalid_rank_raises_error(self):
        with pytest.raises(InvalidRank):
            get_tierlist(5, "top", "test")

    def test_lane_shortcuts(self):
        valid_lanes = ['top', 'jg', 'jng', 'jungle', 'mid', 'middle', 'bot', 'bottom', 'adc', 'support', 'supp', 'sup']
        for lane in valid_lanes:
            try:
                get_tierlist(1, lane)
            except InvalidLane:
                pytest.fail(f"Valid lane '{lane}' raised InvalidLane error")

    def test_get_tierlist_returns_json(self):
        result = get_tierlist(1)
        parsed = json.loads(result)

        labels = [
            'rank',
            'champion',
            'tier',
            'winrate'
        ]
        assert len(parsed) == 1
        assert '0' in parsed
        _check_labels(parsed['0'], labels)


class TestGetCounters:
    def test_empty_champion_raises_error(self):
        with pytest.raises(ValueError, match="Champion name cannot be empty"):
            get_counters(5, "")

    def test_get_counters_returns_json(self):
        result = get_counters(1, "yasuo")
        parsed = json.loads(result)

        labels = [
            'champion',
            'winrate',
        ]
        assert len(parsed) == 1
        assert '0' in parsed
        _check_labels(parsed['0'], labels)


class TestChampionData:
    def test_champion_data(self):
        result = get_champion_data("jax", 'top', 'd+')
        parsed = json.loads(result)

        labels = [
            'winrate',
            'wr_delta',
            'game_avg_wr',
            'pickrate',
            'tier',
            'rank',
            'banrate',
            'games'
        ]
        _check_labels(parsed, labels)

    def test_matchup(self):
        result = matchup("jax", "vayne", "top", "master")
        parsed = json.loads(result)

        labels = [
            'winrate',
            'number_of_games',
        ]
        _check_labels(parsed, labels)

    def test_patch_notes(self):
        result = patch_notes("all", "g+")
        parsed = json.loads(result)

        labels = [
            'buffed',
            'nerfed',
            'adjusted'
        ]
        _check_labels(parsed, labels)
