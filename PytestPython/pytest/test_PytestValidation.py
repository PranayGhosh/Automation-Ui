# import pytest

# @pytest.fixture(scope="module")
# def prework():
#     print("I am module browser ")
#     return "fail"


# @pytest.fixture(scope="function")
# def secondWork():
#     print("I setup module Insatance")
#     # return "fail"
#     yield # pause execution and run test and resume and teardown
#     print("print tear down validation")

# # @pytest.mark.smoke
# def test_intitalCheck(prework,secondWork):
#     print("This is first test")
#     assert prework=="fail"

# @pytest.mark.skip
# def test_secondCheck(preSetupwork,secondWork):
#     print("THis is the second  test")


