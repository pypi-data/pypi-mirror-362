import e3series
import TestTools

def test_GetViewDefinitions() -> None:
    e3, job = TestTools.InitTest("TreeViewDefinition.e3s")
    ret, trees = job.GetTreeIds()
    tree = job.CreateTreeObject()

    for t in  trees:
        tree.SetId(t)
        ret, flags, structure, freetab = tree.GetSortingMethod()
        name = tree.GetName()

        #print(f"Tree {name}:")
        #print(f"\tReturn: {ret}")
        #print(f"\tflags: {flags}")
        #print(f"\tstructure: {structure}")
        #print(f"\tfreetab: {freetab}")

        assert ret == 1
        if name == "Sheet":
            assert flags == 579
            assert len(structure) == 2
            assert len(freetab) == 1
            assert len(structure[0]) == 5
            assert len(freetab[0]) == 3
        elif name == "Devices":
            assert flags == 513
            assert len(structure) == 2
            assert len(freetab) == 2
            assert len(structure[0]) == 5
            assert len(freetab[0]) == 3
        elif name == "Formboard":
            assert flags == 517
            assert len(structure) == 2
            assert len(freetab) == 0
            assert len(structure[0]) == 5
        elif name == "Functional Objects":
            assert flags == 513
            assert len(structure) == 2
            assert len(freetab) == 1
            assert len(structure[0]) == 5
            assert len(freetab[0]) == 3
    assert ret == 1
    job.Close()

def test_GetSortingMethod() -> None:
    e3, job = TestTools.InitTest("TreeViewDefinition.e3s")
    ret, trees = job.GetTreeIds()
    assert ret>0
    assert ret == len(trees)
    tree = job.CreateTreeObject()
    ret = tree.SetId(trees[0])
    assert ret > 0
    ret, flags, structure, freetab = tree.GetSortingMethod()
    assert ret == 1
    assert type(flags) == int

    assert len(freetab) > 0
    assert type(freetab) == tuple
    assert type(freetab[0]) == tuple
    assert len(freetab[0]) == 3
    assert type(freetab[0][0]) == str
    assert type(freetab[0][1]) == str
    assert type(freetab[0][2]) == int

    assert len(structure) > 0
    assert type(structure)
    assert type(structure) == tuple
    assert len(structure[0]) == 5
    assert type(structure[0][0]) ==  str
    assert type(structure[0][1]) ==  int
    assert type(structure[0][2]) ==  str
    assert type(structure[0][3]) ==  str
    assert type(structure[0][4]) ==  int

    job.Close()

if __name__ == "__main__":
    test_GetSortingMethod()