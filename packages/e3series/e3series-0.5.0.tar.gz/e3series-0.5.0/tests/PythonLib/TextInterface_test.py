import e3series
import TestTools

def test_GetTextExtent() -> None:
    e3, job = TestTools.InitTest("TextInterfaceGetTextExtent.e3s")
    sht = job.CreateSheetObject()
    sht.Search(0, "1")
    cnt, ids = sht.GetGraphIds()
    assert cnt == len(ids)
    assert cnt == 1 # Hier im Projekt sollte nur ein Text sein
    txt = job.CreateTextObject()
    assert txt.SetId(ids[0]) > 0
    ret, x, y = txt.GetTextExtent()
    assert type(ret) == int
    assert ret == 1
    assert type(x) == tuple
    assert type(y) == tuple
    assert len(x) == 5
    assert len(y) == 5
    assert x[0] !=  None
    assert y[0] !=  None
    assert x[0] == x[4]
    assert y[0] == y[4]
    job.Close()

def test_GetTextExtentSingleLine() -> None:
    e3, job = TestTools.InitTest("TextInterfaceGetTextExtent.e3s")
    sht = job.CreateSheetObject()
    sht.Search(0, "1")
    cnt, ids = sht.GetGraphIds()
    assert cnt == len(ids)
    assert cnt == 1 # Hier im Projekt sollte nur ein Text sein
    txt = job.CreateTextObject()
    assert txt.SetId(ids[0]) > 0
    ret, lines, x, y = txt.GetTextExtentSingleLine()
    assert type(ret) == int
    assert ret == 1
    assert type(lines) == int
    assert lines > 0
    assert type(x) == tuple
    assert type(y) == tuple
    assert len(x) == lines
    assert len(y) == lines
    for i in range(lines):
        assert type(x[i]) == tuple
        assert type(y[i]) == tuple
        assert x[i][0] != None
        assert y[i][0] != None
        assert x[i][0] == x[i][4]
        assert y[i][0] == y[i][4]
    job.Close()

if __name__ == "__main__":
    test_GetTextExtentSingleLine()