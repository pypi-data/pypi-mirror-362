import e3series
import e3series.tools as e3tools
import os

def _get_projects_folder() -> str:
    path:str = os.path.realpath(os.path.dirname(__file__))
    return f"{path}\\Projects"

def _get_project_full_path(filename:str) -> str:
    return f"{_get_projects_folder()}\\{filename}"

def _open_project(job:e3series.Job, filename:str) -> int:
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

e3App:e3series.Application = None
def InitTest(project:str = "") -> tuple[e3series.Application, e3series.Job]:
    '''
    Gibt das Application-Projekt und ein Job objekt zurück
    Falls ein Projektname übergeben wird, wird dieses aus dem Projects-Ordner geladen
    Ansonsten wird ein neuen Projekt angelegt, außer es wurde None übergeben
    '''
    global e3App
    if e3App != None:
        job = e3App.CreateJobObject()
        if job.GetId() > 0:
            job.Close()
        if project != "":
            _open_project(job, project)
        elif project == "":
            job.Create("Test")
        if project != None:
            assert job.GetId() > 0
        return e3App, job
    else:
        args = ["/formboard", "/topology", "/multiuser"]
        if project != None and project != "":
            args.append(_get_project_full_path(project))
        pid = e3tools.start(args=args, keep_alive=False).pid
        e3App = e3series.Application(pid)
        job = e3App.CreateJobObject()
        if project == "":
            job.Create("Test")
        if project != None:
            assert job.GetId() > 0
        return e3App, job

def StartPersistentForDebug() -> None:
    pid = e3tools.start(["/formboard", "/topology", "/multiuser"]).pid
    global e3App
    e3App = e3series.Application(pid)

def ConnectToRunningE3() -> None:
    global e3App
    e3App = e3series.Application()
    
def GetDrawingPath(filename:str) -> str:
    return _get_project_full_path(filename)