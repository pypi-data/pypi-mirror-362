import e3series
import TestTools

def test_Create() -> None:
    e3, job = TestTools.InitTest()
    con = job.CreateConnectionObject()
    sht = job.CreateSheetObject()
    sht.Create(0, "Test", "DINA3", 0, 0)
    xpos = [180, 180, 228, 228]
    ypos = [120, 92, 92, 120]
    types = [0,0,0,0]
    assert sht.GetNetSegmentCount() == 0
    ret = con.Create(sht.GetId(), 4, xpos, ypos, types)
    assert ret > 0
    cnt, netIds = sht.GetNetSegmentIds()
    assert cnt == 1
    netseg = job.CreateNetSegmentObject()
    netseg.SetId(netIds[0])
    cnt, ids = netseg.GetConnectLineIds()
    assert cnt == 3
    assert len(ids) == 3
    job.Close()

def test_CreateOnFormboard() -> None:
    e3, job = TestTools.InitTest()
    if job.GetId() > 0:
        job.Close()
    job.Create("CreateConnectionFormboard")
    con = job.CreateConnectionObject()
    sht = job.CreateSheetObject()
    sht.CreateFormboard(0, "Test", "DINA3", 0, 0, 0)
    xpos = [180, 180, 228, 228]
    ypos = [120, 92, 92, 120]
    types = [0, 0, 0, 0]
    assert sht.GetNetSegmentCount() == 0
    ret = con.CreateOnFormboard(sht.GetId(), 4, xpos, ypos, types)
    assert len(xpos) == 4       # Die originalen Listen sollen nicht beeinflusst werden
    assert len(ypos) == 4
    assert len(types) == 4
    assert len(ret) == 3    # Hier sollte ein Tupel zurück kommen
    cnt, netIds = sht.GetNetSegmentIds()
    assert cnt == 3
    netseg = job.CreateNetSegmentObject()
    netseg.SetId(netIds[0])
    cnt, ids = netseg.GetConnectLineIds()
    assert cnt == 1
    assert len(ids) == 1
    job.Close()

def test_CreateConnection() -> None:
    e3, job = TestTools.InitTest()
    if job.GetId() > 0:
        job.Close()
    job.Create("CreateConnection")
    con = job.CreateConnectionObject()
    sht = job.CreateSheetObject()
    sht.Create(0, "Test", "DINA3", 0, 0)
    xpos = [180, 180, 228, 228]
    ypos = [120, 92, 92, 120]
    types = [0, 0, 0, 0]
    assert sht.GetNetSegmentCount() == 0
    ret, cons = con.CreateConnection(0, sht.GetId(), 4, xpos, ypos)
    assert ret == 1
    assert len(cons) == 1   # 1 Verbindung sollte erstellt worden sein
    assert type(cons) == tuple
    assert type(cons[0]) == int
    cnt, netIds = sht.GetNetSegmentIds()
    assert cnt == 1
    netseg = job.CreateNetSegmentObject()
    netseg.SetId(netIds[0])
    cnt, ids = netseg.GetConnectLineIds()
    assert cnt == 3
    assert len(ids) == 3
    job.Close()

if __name__ == "__main__":
    test_Create()