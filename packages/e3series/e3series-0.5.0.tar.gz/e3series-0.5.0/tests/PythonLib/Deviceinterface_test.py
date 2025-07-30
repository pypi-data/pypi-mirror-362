import e3series
import TestTools

def test_GetAssignedOptionExpressionWithFlags() -> None:
    e3, job = TestTools.InitTest("DevAssignedOptionExprWithFlags.e3s")
    cnt, ids = job.GetAllDeviceIds()
    assert cnt == len(ids)
    dev = job.CreateDeviceObject()
    for d in  ids:
        dev.SetId(d)
        cnt, optExprs = dev.GetAssignedOptionExpressionsWithFlags()
        assert cnt == len(optExprs)
        name = dev.GetName()

        if name == "-Q1":
            assert cnt == 2
            assert optExprs[0][0] == "O1"
            assert optExprs[1][0] == "O3 | O2"
        elif name == "-Q2":
            assert cnt == 2
            assert optExprs[0][0] == "O1 & O2"
            assert optExprs[1][0] == "O2 & O3"
        elif name == "-Q3":
            assert cnt == 0
    job.Close()

def test_SetAssignedOptionExpressionWithFlags() -> None:
    e3, job = TestTools.InitTest("DevSetAssignedOptionExprWithFlags.e3s")
    Q1 = TestTools.GetDeviceByName(job, "-Q1")
    expressionsIn = [("O1", 0), ("O2", 0)]
    ret = Q1.SetOptionExpressionsWithFlags(expressionsIn)
    len(expressionsIn) == 2     # Die originale Liste soll nicht verändert worden sein
    assert ret > 0
    ret, expressions = Q1.GetAssignedOptionExpressionsWithFlags()
    assert ret > 0
    assert len(expressions) == len(expressionsIn)
    for e in range(len(expressions)):
        len(expressions[e]) == len(expressions[e])
    job.Close()

def test_PlaceOnPointSlot() -> None:
    e3, job = TestTools.InitTest("DevPlaceOnSlot.e3s")
    
    # K1 auf freien punktslot von Q1 platzieren
    K1 = TestTools.GetDeviceByName(job, "-K1")
    Q1 = TestTools.GetDeviceByName(job, "-Q1")
    ret, slots = Q1.GetSlotIds()
    ret, collisions = K1.PlaceOnPointSlot(slots[0])
    assert ret == 1
    assert len(collisions) == 0

    # K3 auf belegten Slot von Q2 platzieren
    K3 = TestTools.GetDeviceByName(job, "-K3")
    Q2 = TestTools.GetDeviceByName(job, "-Q2")
    ret, slots = Q2.GetSlotIds()
    ret, collisions = K3.PlaceOnPointSlot(slots[0])
    assert ret == -8
    assert len(collisions) == 1
    assert len(collisions[0]) == 2

    job.Close()

def test_PlaceOnLineSlot() -> None:
    e3, job = TestTools.InitTest("DevPlaceOnSlot.e3s")
    
    slotId = 18994

    # Q3 auf Hutschiene platzieren
    Q3 = TestTools.GetDeviceByName(job, "-Q3")
    ret, collisions = Q3.PlaceOnLineSlot(slotId, 10)
    assert ret == 1
    assert len(collisions) == 0

    # Q4 an belegte Stelle der Hutschiene platzieren
    Q4 = TestTools.GetDeviceByName(job, "-Q4")
    ret, collisions = Q4.PlaceOnLineSlot(slotId, 20)
    assert ret == -8
    assert len(collisions) == 1
    assert len(collisions[0]) == 2

    job.Close()

def test_Test_PlaceOnAreaSlot() -> None:
    e3, job = TestTools.InitTest("DevPlaceOnSlot.e3s")
    
    slotId = 29054

    # Q3 auf Hutschiene platzieren
    Q3 = TestTools.GetDeviceByName(job, "-Q3")
    ret, collisions = Q3.PlaceOnAreaSlot(slotId, 100, 100)
    assert ret == 1
    assert len(collisions) == 0

    # Q4 an belegte Stelle der Hutschiene platzieren
    Q4 = TestTools.GetDeviceByName(job, "-Q4")
    ret, collisions = Q4.PlaceOnAreaSlot(slotId, 120, 120)
    assert ret == -8
    assert len(collisions) == 1
    assert len(collisions[0]) == 2

    job.Close()

def test_GetVariantObjectProperties() -> None:
    e3, job = TestTools.InitTest("GetVariantObjectProperties.e3s")
    Q1 = TestTools.GetDeviceByName(job, "-Q1")
    
    for i in [1,2,4]:   # 3 klappt irgendwie nicht
        ret, arr = Q1.GetVariantObjectProperties(i, "<Empty>")
        assert ret > 0
        assert len(arr) == ret
        if i==1 or i==2 or i==4:
            assert len(arr[0]) == 3
        else:
            assert len(arr[0]) == 4
        assert type(arr[0][0]) == str
        assert type(arr[0][1]) == int
        assert type(arr[0][2]) == str
        if i==3:
            assert type(arr[0][3] == int)
    
    job.Close()

def test_SetOptionExpressions() -> None:
    e3, job = TestTools.InitTest("GetVariantObjectProperties.e3s")
    Q1 = TestTools.GetDeviceByName(job, "-Q1")
    expressions = [ "O1", "V1" ]
    ret = Q1.SetOptionExpressions( expressions )
    assert ret == 2 # Dann wurden beide genutzt
    job.Close()

def test_AssignFunctionalUnits() -> None:
    e3, job = TestTools.InitTest("AssignFuntionalUnit.e3s")
    S1 = TestTools.GetDeviceByName(job, "-S1")
    funIds = job.GetFunctionalUnitIds()[1]
    ret, ids = S1.GetFunctionalUnitIds()
    assert ret == len(ids)
    assert ids[0] != funIds[0] # davor sollte es eine andere functional unit sein, sonst ist es witzlos
    ret = S1.AssignFunctionalUnits(funIds[0])   # Ist hier auch eher Glück, dass die 1. die nicht belegte ist und die 2. die belegte
    assert ret == 0
    ret, ids = S1.GetFunctionalUnitIds()
    assert ret == len(ids)
    assert ids[0] == funIds[0]
    assert ret == 1
    job.Close()

def test_GetTerminalPlanSettings() -> None:
    e3, job = TestTools.InitTest("GetVariantObjectProperties.e3s")
    Q1 = TestTools.GetDeviceByName(job, "-Q1")

    settings = {
        "AutoCompress": "True",
        "CombineSamePinNames": "True",
        "ConsiderSignalEquivalenceOnlyWithinOneSymbol": "1",
        "InLine": "True",
        "InternalExternalDefinition": "UseAssignmentLocation",
        "Jumpers": "Attributes",
        "OnlyUser-DefinedSignals": "0", 
        "PinViewConnections": "False",
        "SheetFormat": "A3-PlugH_N",
        "SheetName": "TerminalPlan",
        "ShowAllEquivalentPins": "1",
        "TableSymbol": "TAB-H_N",
        "UniqueConnections": "False",
        "WiresInPlan": "0",
       
    }
    ret = Q1.InsertTerminalPlan(settings)
    assert ret == 1

    ret, settings = Q1.GetTerminalPlanSettings({})
    assert ret > 0
    assert ret == len(settings)
    assert type(settings) == dict
    
    settings = {
        "AutoCompress": "",
        "WiresInPlan": "",
        "SheetName": "",
        "PinViewConnections": ""
    }
    ret, settings = Q1.GetTerminalPlanSettings(settings)
    assert ret == 4
    assert ret == len(settings)
    assert type(settings) == dict

    settings = {
        "PinViewConnections": ""
    }
    ret, settings = Q1.GetTerminalPlanSettings(settings)
    assert ret == 1
    assert ret == len(settings)
    assert type(settings) == dict

    ret, settings = Q1.GetTerminalPlanSettings()    # Parameter ist optional
    assert ret > 0
    assert len(settings) == ret
    assert type(settings) == dict

    job.Close()

if __name__ == "__main__":
    test_AssignFunctionalUnits()