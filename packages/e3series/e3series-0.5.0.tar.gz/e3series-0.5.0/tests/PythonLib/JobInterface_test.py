import e3series
import TestTools

def test_CreateInlineConnectorsEx() -> None:
    e3, job = TestTools.InitTest("JobCreateInlineConnectors.e3s")
    X1 = TestTools.GetDeviceByName(job, "-X1")
    X2 = TestTools.GetDeviceByName(job, "-X2")
    ret, X1Pins = X1.GetPinIds()
    ret, X2Pins = X2.GetPinIds()
    ret, newCoreIds, newDeviceIds, newSymbolIds = job.CreateInlineConnectorsEx(0, X1Pins, X2Pins, -1, -1, "DT04-2P", "" )
    assert ret == 0
    assert len(newDeviceIds) == 2
    assert len(newCoreIds) == 0
    assert len(newSymbolIds) == 2
    assert len(newSymbolIds[0]) == 4
    job.Close()

def test_GetIds() -> None:
    e3, job = TestTools.InitTest("Cooling water pump complete.e3s")
    
    ret, ids = job.GetAllComponentIds()
    assert ret == len(ids)

    ret, ids = job.GetComponentIds()
    assert ret == len(ids)

    ret, ids = job.GetAllBusbarConnectionIds()
    assert ret == len(ids)

    ret, ids = job.GetAllConnectionIds()
    assert ret == len(ids)

    ret, ids = job.GetAllDeviceIds()
    assert ret == len(ids)

    ret, ids = job.GetAllOptionIds()
    assert ret == len(ids)

    ret, ids = job.GetAllParentSheetIds(0)
    assert ret == len(ids)

    ret, ids = job.GetAllSheetIds()
    assert ret == len(ids)

    ret, ids = job.GetSheetIds()
    assert ret == len(ids)

    ret, ids = job.GetDeviceIds()
    assert ret == len(ids)

    ret, ids = job.GetTreeIds()
    assert ret == len(ids)

    ret, ids = job.GetCavityPartIds()
    assert ret == len(ids)

    job.Close()

def test_GetTextTypes() -> None:
    e3, job = TestTools.InitTest()

    cnt, textTypes = job.GetTextTypes()
    assert cnt > 0
    assert type(textTypes) == dict
    assert cnt == len(textTypes)
    for k in textTypes.keys():
        assert type(k) == int
        assert type(textTypes[k]) == tuple
        assert len(textTypes[k]) == 20
        for t in textTypes[k]:
            assert type(t) == tuple
            assert type(t[0]) == str
            assert type(t[1]) == str
            assert len(t) == 2

    job.Close()

def test_GetBomPartList() -> None:
    e3, job = TestTools.InitTest("Cooling water pump complete.e3s")
    ret, bom = job.GetBomPartList("", "4.1", 0, "", "", "", [""])
    assert ret > 0
    assert type(bom[0]) == tuple
    assert len(bom) == ret
    assert bom[0][0] != None
    job.Close()

def test_ProjectProperty() -> None:
    e3, job = TestTools.InitTest()
    if job.GetId() > 0:
        job.Close()
    job.New("Test")
    props = job.GetProjectProperty("RecordStatistic")
    assert type(props) == dict
    assert len(props) > 0
    for k in props.keys():
        assert type(k) == str
        assert type(props[k]) == str
    job.Close()

def test_ImportDrawingForProjectGeneration() -> None:
    '''
    Testet noch recht wenig, aber funktioniert immerhin
    substitutes ist in beiden Dimensionen 1-based, das sollte noch geprüft werden
    '''
    e3, job = TestTools.InitTest()
    
    subcircuit = TestTools.GetDrawingPath("Substitute_BMK_2018.e3p")
    substitutes = [("A", "B"), ("C", "D"), ("E", "F"), ("G", "H")]

    ret, result = job.ImportDrawingForProjectGeneration(name=subcircuit, unique=0, flags=0, substitutes=substitutes, posx=0.0, posy=0.0)
    assert type(result) == tuple
    assert result[0] != None
    assert len(result) == 2
    assert ret == 2

    #job.Close()

def test_SetTerminalPlanSettings() -> None:
    e3, job = TestTools.InitTest()

    settings = {
        "AutoCompress" : "1",
        "PinViewConnections" : "True",
        "UniqueConnections" : "False"
    }
    ret = job.SetTerminalPlanSettings(settings)
    assert ret == 3

    ret, settings = job.GetTerminalPlanSettings(settings)
    assert ret == 3
    assert ret == len(settings)
    assert type(settings) == dict

    job.Close()

def test_GetTerminalPlanSettings() -> None:
    e3, job = TestTools.InitTest()

    ret, settings = job.GetTerminalPlanSettings({})
    assert ret > 0
    assert ret == len(settings)
    assert type(settings) == dict

    settings = {
        "AutoCompress": "",
        "WiresInPlan": "",
        "SheetName": "",
        "PinViewConnections": ""
    }
    ret, settings = job.GetTerminalPlanSettings(settings)
    assert ret == 4
    assert ret == len(settings)
    assert type(settings) == dict

    settings = {
        "PinViewConnections": ""
    }
    ret, settings = job.GetTerminalPlanSettings(settings)
    assert ret == 1
    assert ret == len(settings)
    assert type(settings) == dict

    job.Close()

if __name__ == "__main__":
    #TestTools.StartForDebug()
    TestTools.ConnectToRunningE3()
    test_ImportDrawingForProjectGeneration()
    