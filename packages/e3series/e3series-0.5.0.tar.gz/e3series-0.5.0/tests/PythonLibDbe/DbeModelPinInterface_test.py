import e3series
import DbeTestTools

def test_GetCrimpingRules() -> None:
    dbe, dbeJob = DbeTestTools.InitTest("DbeMdlPinCrimpingRules.e3s")
    mdl = dbeJob.CreateDbeModelObject()

    ret, mdls = dbeJob.GetModelIds()
    assert len(mdls) == ret
    assert ret > 0

    for m in mdls:
        mdl.SetId(m)
        if mdl.GetName() == "M_BN20372_3442950":
            break
    assert mdl.GetName() == "M_BN20372_3442950"

    ret, ids = mdl.GetPinIds()
    assert ret == len(ids)
    assert ret > 0

    mpin = dbeJob.CreateDbeModelPinObject()
    for id in ids:
        mpin.SetId(id)
        ret, rules = mpin.GetCrimpingRules()
        assert type(rules) == memoryview
    
    #dbeJob.Close()

if __name__ == "__main__":
    DbeTestTools.ConnectToRunningE3()
    test_GetCrimpingRules()