import e3series
import TestTools

def test_Get() -> None:
    e3, job = TestTools.InitTest("AttributeDefinitionGet.e3s")
    cnt, ids = job.GetAttributeDefinitionIds()
    assert cnt == len(ids)
    attd = job.CreateAttributeDefinitionObject()
    for ad in  ids:
        attd.SetId(ad)
        print(attd.GetName())
        cnt, attributeDefinition = attd.Get()
        assert cnt == len(attributeDefinition)
        for a in attributeDefinition:
            assert len(a) == 2
        #    print(f"{a}")
    job.Close()

def test_Set() -> None:
    e3, job = TestTools.InitTest("AttributeDefinitionGet.e3s")
    attd = job.CreateAttributeDefinitionObject()
    assert attd.Search("Function") > 0 
    oldLen, adef = attd.Get()
    assert oldLen > 0
    assert len(adef) == oldLen
    adef = list(adef)
    ratio = [x for x in adef if x[0] == "Ratio"]
    assert len(ratio) == 1
    assert ratio[0][1] != "2" # Hier sollte der Wert noch anders sein als der, welcher gesetzt wird
    ret = attd.Set([("Ratio", "2")])
    assert ret == 0
    newLen, adef = attd.Get()
    assert oldLen == newLen # Ratio wird überschrieben
    ratio = [x for x in adef if x[0] == "Ratio"]
    assert len(ratio) == 1
    assert ratio[0][1] == "2"
    job.Close()

def test_Create() -> None:
    e3, job = TestTools.InitTest("AttributeDefinitionGet.e3s")
    adef = job.CreateAttributeDefinitionObject()
    newdef = [ \
        ("Owner","5"), \
        ("Owner","9"), \
        ("Owner","11"), \
        ("Owner","18"), \
        ("Owner","32"), \
        ("Owner","34"), \
        ("Type","4"), \
        ("Single instance","1"), \
        ("Unique value","0"), \
        ("Must exist","0"), \
        ("Changeable by script only","0"), \
        ("Default value",""), \
        ("List of values",""), \
        ("Changeable when owner is locked","0"), \
        ("Allow change of lock behaviour","0"), \
        ("Format","1"), \
        ("Size","2.0"), \
        ("Pos x","1.0"), \
        ("Pos y","-4.0"), \
        ("Colour","-1"), \
        ("Ratio","1"), \
        ("Direction","1"), \
        ("Level","50"), \
        ("Visible","1"), \
            ]
    ret = adef.Create("NewDefinition", newdef)
    assert ret > 0
    ret, ad = adef.Get()
    assert len(ad) == len(newdef)
    assert len(ad) == ret
    job.Close()

def test_GetFromDatabase() -> None:
    e3, job = TestTools.InitTest("AttributeDefinitionGet.e3s")
    adef = job.CreateAttributeDefinitionObject()
    cnt, attributeDefinitions = adef.GetFromDatabase()
    assert cnt == len(attributeDefinitions)
    for ad in attributeDefinitions.keys():
        assert type(ad) == str
        assert len(attributeDefinitions[ad]) > 0
        for d in attributeDefinitions[ad]:
            assert len(d) == 2
            assert type(d[0]) == str
            assert type(d[1]) == str
    job.Close()

def test_GetAttributeListValues() -> None:
    e3, job = TestTools.InitTest()
    adef = job.CreateAttributeDefinitionObject()
    ret = adef.Search("Function")
    ret, lstValues =  adef.GetAttributeListValues("DB_User")
    assert len(lstValues) == ret
    assert type(lstValues) == tuple
    assert type(lstValues[0]) == str
    job.Close()

if __name__ == "__main__":
    TestTools.ConnectToRunningE3()
    test_GetAttributeListValues()