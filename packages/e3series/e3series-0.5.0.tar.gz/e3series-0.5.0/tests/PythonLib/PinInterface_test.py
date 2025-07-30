import e3series
import TestTools

def test_GetAssignedOptionExpressionsWithFlags() -> None:
    e3, job = TestTools.InitTest("PinInterfaceGetAssignedOptions.e3s")
    ret, ids = job.GetCableIds()
    dev = job.CreateDeviceObject()
    dev.SetId(ids[0])   # Das Einzige Kabel im Projekt ist das Systemkabel
    ret, cores = dev.GetCoreIds()
    pin = job.CreatePinObject()
    for c in  cores:
        pin.SetId(c)
        name = pin.GetName()
        cnt, options = pin.GetAssignedOptionExpressionsWithFlags()
        assert cnt == len(options)
        if name == "1":
            assert cnt == 2
            assert options[0][0] == "O1"
            assert options[1][0] == "O2 & !O3"
        elif name == "2":
            assert cnt == 3
            assert options[0][0] == "O1"
            assert options[1][0] == "O2"
            assert options[2][0] == "O4"
        elif name == "3":
            assert cnt == 3
            assert options[0][0] == "O2"
            assert options[1][0] == "O3"
            assert options[2][0] == "O4 | O1"
        elif name == "4":
            assert cnt == 0
    job.Close()

def test_GetAllNetSegmentIds() -> None:
    e3, job = TestTools.InitTest("PinGetAllNetSegmentIds.e3s")
    ret, ids = job.GetCableIds()
    assert ret == len(ids)
    assert ret == 1
    dev = job.CreateDeviceObject()
    dev.SetId(ids[0])
    ret, ids = dev.GetCoreIds()
    assert ret == len(ids)
    assert ret == 1
    pin = job.CreatePinObject()
    pin.SetId(ids[0])
    ret, views, types, viewcount, netids = pin.GetAllNetSegmentIds(0)
    assert ret == len(views)
    assert ret == len(types)
    assert ret == len(viewcount)
    assert ret == len(netids)
    for t in range(len(netids)):
        for i in range(len(netids[t])):
            if i<viewcount[t]:
                assert netids[t][i] != None
            else:
                assert netids[t][i] == None
    job.Close()

if __name__ == "__main__":
    test_GetAllNetSegmentIds()