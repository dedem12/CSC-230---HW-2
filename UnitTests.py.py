"""
CSC 230 - Introduction to Software Engineering
Homework 2 — Part 2: Unit Tests
File: UnitTests.py

Notes:
- Per the assignment, prototypes are included below ONLY so this file runs end-to-end.
  The instructor will ignore these prototypes and grade your unit tests.
- Tests follow the (1) setup, (2) test, (3) examine pattern and print ONLY on failure.
"""

# ------------------------------
# Prototypes (so tests can run)
# ------------------------------

def less_than(number1, number2):
    """
    Behavior per spec:
    - If BOTH inputs are floats:
        return 1 if number1 < number2
        return -1 if number1 > number2
        return 0 otherwise (equal)
    - If either input is not a float: return 0
    """
    if isinstance(number1, float) and isinstance(number2, float):
        if number1 < number2:
            return 1
        elif number1 > number2:
            return -1
        else:
            return 0
    return 0


def addLists(list1, list2):
    """
    Behavior per spec:
    - If BOTH params are lists AND have same length:
        Try pairwise addition of items.
        If any pair fails to add, return [].
        Otherwise return the list of pairwise sums.
    - Else return [].
    """
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
    """
    Prototype Security class matching the described behavior.
    Keeps track of current password and a history of used passwords
    (most recent first). For updatePassword, a new password must:
      - Match login and old password
      - Have at least one lowercase, one uppercase, and one digit
      - NOT match any of the last 3 passwords used for that login
    """
    def __init__(self, login, password):
        self._login = login
        self._password = password
        # Password history includes the current password at index 0
        self._history = [password]

    # Assume these work for constructor testing
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
        # Check login & old password
        if login != self._login or old_password != self._password:
            return False
        # Check policy
        if not isinstance(new_password, str) or not self._valid_policy(new_password):
            return False
        # Check last 3
        last_three = self._history[:3]
        if new_password in last_three:
            return False
        # All good: update
        self._password = new_password
        self._history.insert(0, new_password)
        # Cap history to a reasonable length
        self._history = self._history[:10]
        return True


# ------------------------------
# Test Utilities
# ------------------------------

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


# ------------------------------
# Unit Tests
# ------------------------------

def test_less_than():
    # (1) setup is trivial for these cases

    # (2) test + (3) examine

    # Both floats, number1 < number2 -> 1
    res = less_than(1.0, 2.0)
    check_eq("less_than float less", res, 1)

    # Both floats, number1 > number2 -> -1
    res = less_than(3.7, 1.2)
    check_eq("less_than float greater", res, -1)

    # Both floats, equal -> 0
    res = less_than(2.5, 2.5)
    check_eq("less_than float equal", res, 0)

    # Non-floats -> 0 (e.g., ints)
    res = less_than(1, 2)
    check_eq("less_than non-floats", res, 0)

    # Mixed float & non-float -> 0
    res = less_than(1.0, 2)
    check_eq("less_than mixed types", res, 0)


def test_addLists():
    # Good input, equal length ints
    res = addLists([1, 2, 3], [4, 5, 6])
    check_eq("addLists ints equal length", res, [5, 7, 9])

    # Good input, equal length strings (concatenation)
    res = addLists(["a", "b"], ["x", "y"])
    check_eq("addLists strings equal length", res, ["ax", "by"])

    # Unequal lengths -> []
    res = addLists([1, 2], [10])
    check_eq("addLists unequal length", res, [])

    # Not both lists -> []
    res = addLists([1, 2], (3, 4))
    check_eq("addLists non-lists", res, [])

    # Items do not '+' correctly -> []
    res = addLists([1, None], [2, 3])
    check_eq("addLists invalid addition", res, [])


def test_security_constructor_and_accessors():
    # Setup
    s = Security("bob", "Fail1")

    # Test & examine (assuming getLogin/getPassword work as per instructions)
    check_eq("Security __init__ login", s.getLogin(), "bob")
    check_eq("Security __init__ password", s.getPassword(), "Fail1")


def test_security_checkCredentials():
    s = Security("alice", "Good1Pass")

    # True case
    check_true("checkCredentials true",
               s.checkCredentials("alice", "Good1Pass"))

    # False: wrong password
    check_true("checkCredentials false wrong pwd",
               not s.checkCredentials("alice", "BadPass1"))

    # False: wrong login
    check_true("checkCredentials false wrong login",
               not s.checkCredentials("ALICE", "Good1Pass"))


def test_security_updatePassword_success_and_failures():
    # Setup
    s = Security("user", "Abc123")

    # Success: valid policy, correct login & old, not in last 3
    ok = s.updatePassword("user", "Abc123", "NewPass1")
    check_true("updatePassword success returns True", ok)
    check_eq("updatePassword success changed pwd", s.getPassword(), "NewPass1")

    # Failure: wrong login
    old = s.getPassword()
    ok = s.updatePassword("USER", old, "Another1A")
    check_true("updatePassword wrong login returns False", not ok)
    check_eq("updatePassword wrong login unchanged", s.getPassword(), old)

    # Failure: wrong old password
    old = s.getPassword()
    ok = s.updatePassword("user", "notOld", "Another1A")
    check_true("updatePassword wrong old returns False", not ok)
    check_eq("updatePassword wrong old unchanged", s.getPassword(), old)

    # Failure: no lowercase
    old = s.getPassword()
    ok = s.updatePassword("user", old, "NOPASS1")
    check_true("updatePassword no lowercase False", not ok)
    check_eq("updatePassword no lowercase unchanged", s.getPassword(), old)

    # Failure: no uppercase
    old = s.getPassword()
    ok = s.updatePassword("user", old, "newpass1")
    check_true("updatePassword no uppercase False", not ok)
    check_eq("updatePassword no uppercase unchanged", s.getPassword(), old)

    # Failure: no digit
    old = s.getPassword()
    ok = s.updatePassword("user", old, "NoDigits")
    check_true("updatePassword no digit False", not ok)
    check_eq("updatePassword no digit unchanged", s.getPassword(), old)

    # Set up more history: 3 more successful updates
    # Current is "NewPass1"
    s.updatePassword("user", "NewPass1", "OkayPass2")
    s.updatePassword("user", "OkayPass2", "GreatPass3")
    s.updatePassword("user", "GreatPass3", "Zesty4Pass")

    # Failure: attempting to reuse one of the last 3 ("GreatPass3", "OkayPass2", "Zesty4Pass")
    old = s.getPassword()
    ok = s.updatePassword("user", old, "OkayPass2")
    check_true("updatePassword reuse last-3 False", not ok)
    check_eq("updatePassword reuse last-3 unchanged", s.getPassword(), old)

    # Allowed: using a password older than last 3 ("NewPass1" is 4th back)
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

    if FAILURES == 0:
        # Per instructions, print nothing unless there's a failure,
        # but it's often helpful for local runs to see a success message.
        # Comment out the next line to strictly adhere to silence-on-success.
        # print("All tests passed.")
        pass


if __name__ == "__main__":
    run_all_tests()
