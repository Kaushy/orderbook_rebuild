# coding=utf-8
import pytest


def inc(x):
    return x + 1


def test_answer():
    assert inc(4) == 5

# 1. Test that two orders with the same ID are not entered on both sides
# 2. Test that at any given time Sell Order Price cannot be less than Buy Order price and rest on Book
# 3.
