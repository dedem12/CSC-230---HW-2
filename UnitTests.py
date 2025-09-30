"""
CSC 230 - Introduction to Software Engineering
Homework 2 — Part 2: Unit Tests
File: UnitTests.py

Notes:
- Per the assignment, prototypes are included ONLY so this file runs end-to-end.
  The instructor will ignore these prototypes and grade your unit tests.
- Tests follow the (1) setup, (2) test, (3) examine pattern and print ONLY on failure.
- Exit code is non-zero if any test fails (so GitHub Actions / CI can detect failures).
"""

import sys

# My Prototypes (so tests can run)


def less_than(number1, number2):
    if isinstance(number1, float) and isinstance(number2, float):
        if number1 < number2:
            return 1
        elif number1 > number2:
            return -1
        else:
            return 0
    return 0


def addLists(list1, list2):
    if not (isinstance(list1, list) and isinstance(list2, list)):
        return []
    if len(list1) != len(list2):
        return []
    result = []
    for a, b in zip(list1, list2):
        try:
            result.append(a + b)
        except Exception:
            return []
    return result


class Security:
    def __init__(self, login, password):
        self._login = login
        self._password = password
        self._history = [password]

    def getLogin(self):
        return self._login

    def getPassword(self):
        return self._password

    def checkCredentials(self, login, password):
        return self._login == login and self._password == password

    def _valid_policy(self, pwd):
        has_lower = any(c.islower() for c in pwd)
        has_upper = any(c.isupper() for c in pwd)
        has_digit = any(c.isdigit() for c in pwd)
        return has_lower and has_upper and has_digit

    def updatePassword(self, login, old_password, new_password):
        if login != self._login or old_password != self._password:
            return False
        if not isinstance(new_password, str) or not self._valid_policy(new_password):
            return False
        last_three = self._history[:3]
        if new_password in last_three:
            return False
        self._password = new_password
        self._history.insert(0, new_password)
        self._history = self._history[:10]
        return True

# Test and results


FAILURES = 0

def check_eq(test_name, actual, expected):
    global FAILURES
    if actual != expected:
        print(f"FAIL [{test_name}]: expected {expected!r}, got {actual!r}")
        FAILURES += 1

def check_true(test_name, condition, details=""):
    global FAILURES
    if not condition:
        msg = f"FAIL [{test_name}]"
        if details:
            msg += f": {details}"
        print(msg)
        FAILURES += 1

# Unit Tests

def test_less_than():
    check_eq("less_than float less", less_than(1.0, 2.0), 1)
    check_eq("less_than float greater", less_than(3.7, 1.2), -1)
    check_eq("less_than float equal", less_than(2.5, 2.5), 0)
    check_eq("less_than non-floats", less_than(1, 2), 0)
    check_eq("less_than mixed types", less_than(1.0, 2), 0)


def test_addLists():
    check_eq("addLists ints equal length", addLists([1, 2, 3], [4, 5, 6]), [5, 7, 9])
    check_eq("addLists strings equal length", addLists(["a", "b"], ["x", "y"]), ["ax", "by"])
    check_eq("addLists unequal length", addLists([1, 2], [10]), [])
    check_eq("addLists non-lists", addLists([1, 2], (3, 4)), [])
    check_eq("addLists invalid addition", addLists([1, None], [2, 3]), [])


def test_security_constructor_and_accessors():
    s = Security("bob", "Fail1")
    check_eq("Security __init__ login", s.getLogin(), "bob")
    check_eq("Security __init__ password", s.getPassword(), "Fail1")


def test_security_checkCredentials():
    s = Security("alice", "Good1Pass")
    check_true("checkCredentials true", s.checkCredentials("alice", "Good1Pass"))
    check_true("checkCredentials false wrong pwd", not s.checkCredentials("alice", "BadPass1"))
    check_true("checkCredentials false wrong login", not s.checkCredentials("ALICE", "Good1Pass"))


def test_security_updatePassword_success_and_failures():
    s = Security("user", "Abc123")

    ok = s.updatePassword("user", "Abc123", "NewPass1")
    check_true("updatePassword success returns True", ok)
    check_eq("updatePassword success changed pwd", s.getPassword(), "NewPass1")

    old = s.getPassword()
    ok = s.updatePassword("USER", old, "Another1A")
    check_true("updatePassword wrong login returns False", not ok)
    check_eq("updatePassword wrong login unchanged", s.getPassword(), old)

    old = s.getPassword()
    ok = s.updatePassword("user", "notOld", "Another1A")
    check_true("updatePassword wrong old returns False", not ok)
    check_eq("updatePassword wrong old unchanged", s.getPassword(), old)

    old = s.getPassword()
    ok = s.updatePassword("user", old, "NOPASS1")
    check_true("updatePassword no lowercase False", not ok)
    check_eq("updatePassword no lowercase unchanged", s.getPassword(), old)

    old = s.getPassword()
    ok = s.updatePassword("user", old, "newpass1")
    check_true("updatePassword no uppercase False", not ok)
    check_eq("updatePassword no uppercase unchanged", s.getPassword(), old)

    old = s.getPassword()
    ok = s.updatePassword("user", old, "NoDigits")
    check_true("updatePassword no digit False", not ok)
    check_eq("updatePassword no digit unchanged", s.getPassword(), old)

    s.updatePassword("user", "NewPass1", "OkayPass2")
    s.updatePassword("user", "OkayPass2", "GreatPass3")
    s.updatePassword("user", "GreatPass3", "Zesty4Pass")

    old = s.getPassword()
    ok = s.updatePassword("user", old, "OkayPass2")
    check_true("updatePassword reuse last-3 False", not ok)
    check_eq("updatePassword reuse last-3 unchanged", s.getPassword(), old)

    old = s.getPassword()
    ok = s.updatePassword("user", old, "NewPass1")
    check_true("updatePassword reuse older-than-3 True", ok)
    check_eq("updatePassword reuse older-than-3 changed", s.getPassword(), "NewPass1")


def run_all_tests():
    test_less_than()
    test_addLists()
    test_security_constructor_and_accessors()
    test_security_checkCredentials()
    test_security_updatePassword_success_and_failures()

    if FAILURES > 0:
        sys.exit(1) 


if __name__ == "__main__":
    run_all_tests()

