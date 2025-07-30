import e3series
import DbeTestTools

def test_GetStepTransformation() -> None:
    dbe, dbeJob = DbeTestTools.InitTest("MdlGetStepTransformation.e3s")
    ret, models = dbeJob.GetModelIds()
    mdl = dbeJob.CreateDbeModelObject()
    mdl.SetId(models[0])
    ret, matrix = mdl.GetStepTransformation()
    assert ret == 1
    assert len(matrix) == 16
    for f in matrix:
        assert type(f) == float
    
    #job.Close()

if __name__ == "__main__":
    test_GetStepTransformation()