import e3series
import TestTools

def test_GetModelList() -> None:
    e3 = TestTools.InitTest(None)[0]
    extraAttributeNames = [ "[Class]", "[Description]" ]
    ret, mdls = e3.GetModelList(extraAttributeNames)
    assert ret > 0
    assert ret == len(mdls)
    assert type(ret) == int
    assert type(mdls) == tuple
    assert type(mdls[0]) == tuple
    cls = False
    dsc = False
    for e in mdls[0]:
        if e=="[Class]":
            cls = True
        elif e=="[Description]":
            dsc = True
    assert cls == True
    assert dsc == True

def test_GetComponentList() -> None:
    e3 = TestTools.InitTest(None)[0]
    extraAttributeNames = [ "[Class]", "[Description]" ]
    ret, cmps = e3.GetComponentList(extraAttributeNames)
    assert ret > 0
    assert ret == len(cmps)
    assert type(ret) == int
    assert type(cmps) == tuple
    assert type(cmps[0]) == tuple
    cls = False
    dsc = False
    for e in cmps[0]:
        if e=="[Class]":
            cls = True
        elif e=="[Description]":
            dsc = True
    assert cls == True
    assert dsc == True

def test_SortArrayByIndex() -> None:
    e3 = TestTools.InitTest(None)[0]
    flatArray = [
        ["F1", "A", "876"],   \
        ["F10", "B", "564"],  \
        ["F1.1", "A", "564"], \
        ["F11", "B", "345"],  \
        ["F2", "A", "215"],   \
        ["F1.10", "B", "789"],\
        ["F1.11", "A", "543"],\
        ["F1.2", "B", "465"]  \
    ]
    ret, sorted = e3.SortArrayByIndex(flatArray, len(flatArray), len(flatArray[0]), 1, 0)
    assert ret == 0
    assert type(sorted) == tuple
    assert len(sorted) == len(flatArray)
    assert type(sorted[0]) == tuple
    assert len(sorted[0]) == len(flatArray[0])
    for e in sorted:
        for s in e:
            assert type(s) == str

if __name__ == "__main__":
    test_SortArrayByIndex()