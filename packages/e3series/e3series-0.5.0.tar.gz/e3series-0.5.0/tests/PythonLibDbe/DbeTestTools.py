import e3series
import e3series.tools as e3tools
import os

def _get_projects_folder() -> str:
    path:str = os.path.realpath(os.path.dirname(__file__))
    return f"{path}\\Projects"

def _get_project_full_path(filename:str):
    return f"{_get_projects_folder()}\\{filename}"

def _open_project(job:e3series.DbeJob, filename:str) -> int:
    if job.GetId() > 0:
        job.Close()
    fullPath = _get_project_full_path(filename)
    ret = job.Open(fullPath)
    if ret <= 0:
        print(f"Could not open file {fullPath}. Return was {ret}.")
    return ret

def GetDeviceByName(job:e3series.Job, name:str) -> e3series.Device:
    ret, ids = job.GetAllDeviceIds()
    dev = job.CreateDeviceObject()
    for id in ids:
        dev.SetId(id)
        if dev.GetName() == name:
            return dev
    return None

dbeApp:e3series.DbeApplication = None
def InitTest(project:str = "") -> tuple[e3series.DbeApplication, e3series.DbeJob]:
    '''
    Gibt das Application-Projekt und ein Job objekt zurück
    Falls ein Projektname übergeben wird, wird dieses aus dem Projects-Ordner geladen
    Ansonsten wird ein neuen Projekt angelegt, außer es wurde None übergeben
    '''
    global dbeApp
    if dbeApp != None:
        job = dbeApp.CreateDbeJobObject()
        if job.GetId() > 0:
            job.Close()
        if project != "":
            _open_project(job, project)
        elif project == "":
            job.Create("Test")
        if project != None:
            jobId = job.GetId()
            assert jobId > 0
        return dbeApp, job
    else:
        args = ["/dbe"]
        if project != None and project != "":
            args.append(_get_project_full_path(project))
        pid = e3tools.start(args=args, keep_alive=False).pid
        dbeApp = e3series.DbeApplication(pid)
        job = dbeApp.CreateDbeJobObject()
        if project == "":
            job.Create("Test")
        if project != None:
            assert job.GetId() > 0
        return dbeApp, job

def StartForDebug():
    pid = e3tools.start(["/dbe"]).pid
    global dbeApp
    dbeApp = e3series.DbeApplication(pid)

def ConnectToRunningE3():
    global dbeApp
    dbeApp = e3series.DbeApplication()