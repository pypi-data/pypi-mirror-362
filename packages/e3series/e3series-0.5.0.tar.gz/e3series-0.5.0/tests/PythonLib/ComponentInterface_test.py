import e3series
import TestTools

def test_GetViewDefinitions() -> None:
    e3, job = TestTools.InitTest("ComponentInterfaceViewDefinitions.e3s")
    ret, ids = job.GetComponentIds()
    cmp = job.CreateComponentObject()
    for c in  ids:
        cmp.SetId(c)
        cnt, defs = cmp.GetViewDefinitions()
        name = cmp.GetName()
        assert cnt == len(defs)

        #print(f"Component {name}:")
        #for d in defs:
        #    print(f"\t{d}")

        if name == "3RT13171AP00":
            assert cnt ==4
            assert defs[0][0] == 18989
            assert defs[1][0] == 17743
            assert defs[2][0] == 19083
            assert defs[3][0] == 18010
        elif name == "3RT15171AD00" or name == "3RT15171AP00":
            assert cnt ==7
            assert defs[0][0] == 18084
            assert defs[1][0] == 17743
            assert defs[2][0] == 17226
            assert defs[3][0] == 17226
            assert defs[4][0] == 17484
            assert defs[5][0] == 17484
            assert defs[6][0] == 18010
    job.Close()