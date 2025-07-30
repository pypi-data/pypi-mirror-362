import e3series
import e3series.types
import TestTools

def test_SetSchematicType() -> None:
    e3, job = TestTools.InitTest("ShtSchematicType")
    sht = job.CreateSheetObject()
    assert sht.Search(0,"TestSheet") > 0
    types = [e3series.types.SchematicType.Pneumatic.value, e3series.types.SchematicType.Electric.value]
    ret = sht.SetSchematicTypes(types)
    assert type(ret) == int
    assert ret == 2

if __name__ == "__main__":
    test_SetSchematicType()