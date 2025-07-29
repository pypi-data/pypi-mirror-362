#!/usr/bin/env --split-string=python -m pytest --verbose

"""Self test code"""

import pytest

from wanip import Providers, Public_Providers

class Testcase_Providers_01:

    def test_generals(self):

        global Public_Providers

        assert len(Public_Providers) == 17
        assert "my machine" not in Public_Providers
        assert repr(Public_Providers) is not None
        assert str(Public_Providers) is not None
        P = Public_Providers()
        assert P in Public_Providers

        assert "https://ifconfig.me/ip" in Public_Providers

        Public_Providers = Providers(1, 2, 3, 4, 5, 6)
        assert len(Public_Providers) == 6
        assert 6 in Public_Providers

        Public_Providers = Public_Providers + 42
        assert len(Public_Providers) == 7
        assert 42 in Public_Providers

        Public_Providers = Public_Providers + 'foo'
        assert len(Public_Providers) == 8
        assert 'foo' in Public_Providers

        Public_Providers = Public_Providers + "bar"
        assert len(Public_Providers) == 9
        assert "baz" not in Public_Providers

        Public_Providers = Public_Providers + "zonk" + 'baz'
        assert len(Public_Providers) == 11
        assert "baz" in Public_Providers

        Public_Providers = Public_Providers - "zonk" - 3
        assert len(Public_Providers) == 9
        assert 3 not in Public_Providers

        Public_Providers = Public_Providers - 4
        assert len(Public_Providers) == 8
        assert 4 not in Public_Providers

class Testcase_Providers_02:

    def test_removing_an_unknown_element(self):
        # Cannot remove non-existing element
        with Providers() as P:
            P = P + 'a known element'
            with pytest.raises(ValueError):
                P = P - 'non-existing element'

    def test_adding_things_twice(self):
        # Cannot add an element more than once
        with Providers() as P:
            with pytest.raises(ValueError):
                P = P + 'an element' + 'an element'

class Testcase_Providers_03:

    def test_chache(self):

        P = Providers(1, 2, 3, 4)
        a = P()
        assert a in P

        # Make sure a cannot be returned again
        P = P - a
        assert a not in P

        b = P()
        assert a != b

        # Put a back into P
        P = P + a
        assert a in P

        a, b = P(use_cached=True), P(use_cached=not False)
        assert a == b

        # Now have cached providers to begin with
        Q = Providers(4711, 3206, 42, use_cached=True)
        c = Q()
        assert c in Q

        Q = Q - c
        assert c not in Q

        d = Q(use_cached=True)
        assert d == c

        d = Q()
        assert d != c

class Testcase_Providers_04:

    def test_providers_drainage(self):
        # Drain providers
        P = Providers(self.test_providers_drainage.__name__)
        P = P - P()
        with pytest.raises(ValueError):
            P = P - P()

    def test_telescoping_series(self):
        P = Providers()
        P = P + 1
        P = P + 2 - 2 + 2 - 2 + 2 - 2 + 'a' + 'b' - 'a' - 'b'
        P = P + 9
        Q = Providers(1, 9)

        assert len(P) == 2
        assert len(Q) == 2

        p1 = P(); P = P - p1
        p2 = P(); P = P - p2

        q1 = Q(); Q = Q - q1
        q2 = Q(); Q = Q - q2

        assert sorted((p1, p2)) == sorted((q1, q2))

    def test_empty_list_of_providers(self):

        # Cannot obtain a provider from an empty collection
        Public_Providers = Providers()
        with pytest.raises(ValueError):
            print(Public_Providers())

        # Not even when asking for a cached one
        with pytest.raises(ValueError):
            print(Public_Providers(use_cached=not False))

class Testcase_Providers_05:

    def test_context_manager_protocol(self):
        # Test the context manager protocol
        with Providers('spam', 'eggs') as P:
            P()
        with pytest.raises(ValueError):
            # We have left the context (of Providers(...), that is)
            P()
