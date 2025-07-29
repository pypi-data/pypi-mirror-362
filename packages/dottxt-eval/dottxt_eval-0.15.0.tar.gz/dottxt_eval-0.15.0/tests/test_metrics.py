from doteval.metrics import accuracy


def test_accuracy():
    metric = accuracy()
    list1 = [True, True, True]
    list0 = [False, False, False]
    listhalf = [False, True]
    assert metric(list1) == 1.0
    assert metric(list0) == 0
    assert metric(listhalf) == 0.5
