import e3series
import e3series.types as e3types
import TestTools

def test_GetAnyIds() -> None:
    e3, job = TestTools.InitTest("GrpGetAnyIds.e3s")
    ret, grps = job.GetGroupIds()
    assert len(grps) > 0
    assert len(grps) == ret
    grp = job.CreateGroupObject()
    for g in grps:
        grp.SetId(g)
        ret, ids = grp.GetAnyIds(0xFF)
        assert len(ids) > 0
        assert len(ids) == ret
        for k in ids.keys():
            assert len(ids[k]) > 0
            assert ids[k][0] != None
    job.Close()

def test_UpdateDrawingForProjectGeneration() -> None:
    '''
    Die optionalen Parameter sollten evtl auch noch geprüft werden
    '''
    e3, job = TestTools.InitTest("GrpUpdateDrawingForPrjGeneration.e3s")
    grp = job.CreateGroupObject()
    ret, grps = job.GetGroupIds()
    assert ret > 0
    assert ret == len(grps)
    grp.SetId(grps[0])
    substitutes = [("?1", "1"),("?2", "0"),("?3", "2")]
    file = TestTools._get_project_full_path("Fernwartung_Switch_E10x_v2.e3p")
    ret = grp.SetName("Fernwartung - Switch, E10x_v2")
    assert ret==0
    ret = grp.SetPartName(file)
    assert ret==0
    ret = grp.UpdateDrawingForProjectGeneration( 0, substitutes)
    assert ret==1
    sht = job.CreateSheetObject()
    sht.Search(0,"1")
    cnt, gras = sht.GetGraphIds()
    gra = job.CreateGraphObject()
    txt = job.CreateTextObject()
    checked = False
    for g in gras:
        gra.SetId(g)
        if gra.GetType() != e3types.GraphType.Text.value:
            continue
        txt.SetId(g)
        s = txt.GetText()
        assert s.find("?") == -1
        checked = True
    assert checked == True  # Es sollte zumidnest ein Text geprüft werden. Au Blatt 1 ist genau einer
    job.Close()

if __name__ == "__main__":
    TestTools.ConnectToRunningE3()
    test_UpdateDrawingForProjectGeneration()