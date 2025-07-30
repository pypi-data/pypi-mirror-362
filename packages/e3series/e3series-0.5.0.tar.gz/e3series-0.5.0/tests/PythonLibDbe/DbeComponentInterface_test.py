import e3series
import DbeTestTools

def test_GetComponentAttributeIds() -> None:
    dbe, job = DbeTestTools.InitTest("ComponentMainContactor.e3s")
    cnt, cmps = job.GetComponentIds()
    assert cnt > 0
    assert cnt == len(cmps)
    cmp = job.CreateDbeComponentObject()
    assert cmp.SetId(cmps[0]) > 0
    cnt, atts = cmp.GetAttributeIds()
    assert cnt > 0 
    assert cnt == len(atts)

    #job.Close()

if __name__ == "__main__":
    test_GetComponentAttributeIds()