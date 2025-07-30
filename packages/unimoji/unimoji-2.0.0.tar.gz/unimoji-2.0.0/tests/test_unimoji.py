# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
import pytest

import unimoji

person_tipping_hand = "💁"  # length 1
man_tipping_hand = "💁‍♂️"  # length 4
woman_tipping_hand = "💁‍♀️"  # length 4
biting_lip = "🫦" # length 1


@pytest.fixture
def tweet():
    return """\
#startspreadingthenews yankees win great start by 🎅🏾 going 5strong innings with 5k’s🔥 🐂
solo homerun 🌋🌋 with 2 solo homeruns and👹 3run homerun… 🤡 🚣🏼 👨🏽‍⚖️ with rbi’s … 🔥🔥
🇲🇽 and 🇳🇮 to close the game🔥🔥!!!….
WHAT A GAME!!..
"""


def test_setup():
    assert len(person_tipping_hand) == 1
    assert len(man_tipping_hand) == 4
    assert len(woman_tipping_hand) == 4
    assert len(biting_lip) == 1


def test_last_downloaded_timestamp_rettype():
    ts = unimoji.last_downloaded_timestamp()
    assert isinstance(ts, datetime.datetime)


def test_unimoji_main(tweet):
    assert not unimoji.findall("Hi")
    assert unimoji.replace("Hi") == "Hi"
    assert not unimoji.findall("2 ! $&%((@)# $)@ ")
    assert unimoji.findall("The 🌓 shall rise again") == {
        "🌓": "first quarter moon"
    }
    allhands = "Someone actually gets paid to make a %s, a %s, and a %s" % (
        person_tipping_hand,
        man_tipping_hand,
        woman_tipping_hand,
    )
    assert unimoji.findall(allhands) == {
        person_tipping_hand: "person tipping hand",
        man_tipping_hand: "man tipping hand",
        woman_tipping_hand: "woman tipping hand",
    }
    assert (
        unimoji.replace(allhands)
        == "Someone actually gets paid to make a , a , and a "
    )
    assert (
        unimoji.replace(allhands, "X")
        == "Someone actually gets paid to make a X, a X, and a X"
    )
    assert isinstance(unimoji.last_downloaded_timestamp(), datetime.datetime)

    # Something for everyone...
    batch = [
        "😀",
        "😂",
        "🤩",
        "🤐",
        "🤢",
        "🙁",
        "😫",
        "🙀",
        "💓",
        "🧡",
        "🖤",
        "👁️‍🗨️",
        "✋",
        "🤙",
        "👊",
        "🙏",
        "👂",
        "👱‍♂️",
        "🧓",
        "🙍‍♀️",
        "🙋",
        "🙇",
        "👩‍⚕️",
        "👩‍🔧",
        "👨‍🚒",
        "👼",
        "🦸",
        "🧝‍♀️",
        "👯‍♀️",
        "🤽",
        "🤼‍♀️",
        "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
        "👩‍👧‍👦",
        "🐷",
        "2️⃣",
        "8️⃣",
        "🆖",
        "🈳",
        "الجزيرة‎",
        "傳騰訊入股Reddit 言論自由不保?",
        "🇩🇯",
        "⬛",
        "🔵",
        "🇨🇫",
        "‼",
    ]
    assert len(unimoji.findall(" xxx ".join(batch))) == len(batch) - 2
    assert unimoji.findall(tweet) == {
        "🔥": "fire",
        "🌋": "volcano",
        "👨🏽\u200d⚖️": "man judge: medium skin tone",
        "🎅🏾": "Santa Claus: medium-dark skin tone",
        "🇲🇽": "flag: Mexico",
        "👹": "ogre",
        "🤡": "clown face",
        "🇳🇮": "flag: Nicaragua",
        "🚣🏼": "person rowing boat: medium-light skin tone",
        "🐂": "ox",
    }


def test_findall_list(tweet):
    assert len(unimoji.findall_list(tweet, True)) == len(
        unimoji.findall_list(tweet, False)
    )
    assert unimoji.findall_list(tweet, True)
    assert unimoji.findall_list(tweet, False)
    assert "santa claus" in unimoji.findall_list(tweet, True)[0].lower()
    assert "🔥" == unimoji.findall_list(tweet, False)[1]


def test_replace_with_desc(tweet):
    assert (
        unimoji.replace_with_desc(tweet, ":")
        == "#startspreadingthenews yankees win great start by :Santa Claus: medium-dark skin tone: going 5strong innings with 5k’s:fire: :ox:\nsolo homerun :volcano::volcano: with 2 solo homeruns and:ogre: 3run homerun… :clown face: :person rowing boat: medium-light skin tone: :man judge: medium skin tone: with rbi’s … :fire::fire:\n:flag: Mexico: and :flag: Nicaragua: to close the game:fire::fire:!!!….\nWHAT A GAME!!..\n"
    )
    assert (
        unimoji.replace_with_desc(tweet, "|")
        == "#startspreadingthenews yankees win great start by |Santa Claus: medium-dark skin tone| going 5strong innings with 5k’s|fire| |ox|\nsolo homerun |volcano||volcano| with 2 solo homeruns and|ogre| 3run homerun… |clown face| |person rowing boat: medium-light skin tone| |man judge: medium skin tone| with rbi’s … |fire||fire|\n|flag: Mexico| and |flag: Nicaragua| to close the game|fire||fire|!!!….\nWHAT A GAME!!..\n"
    )
