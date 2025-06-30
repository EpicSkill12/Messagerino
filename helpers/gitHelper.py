import subprocess

def getStatus(directory: str) -> tuple[bool, str]:
  """
  Vor.: directory ist ein Pfad zu einem Git-Repository
  Eff.: Führt 'git status' aus
  Erg.: Gibt Erfolg und Ausgabestring zurück
  """
  try:
    status = True, subprocess.check_output(
      ['git', 'status', '-vv'],
      cwd=directory, universal_newlines=True
   )
  except subprocess.CalledProcessError as e:
    status = False, str(e)
  return status
  
def attemptPull(directory: str) -> tuple[bool, str]:
  """
  Vor.: directory ist ein Pfad zu einem Git-Repository
  Eff.: Führt 'git pull' aus
  Erg.: Gibt Erfolg und Ausgabestring zurück
  """
  try:
    output = subprocess.check_output(
        ['git', 'pull', "--verbose"],
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        cwd=directory
    )
    return (True, output.strip())
  except subprocess.CalledProcessError as e:
    return (False, str(e))