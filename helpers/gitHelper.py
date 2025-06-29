import subprocess

def getStatus(directory: str) -> tuple[bool, str]:
  try:
    status = True, subprocess.check_output(
      ['git', 'status', '-vv'],
      cwd=directory, universal_newlines=True
   )
  except subprocess.CalledProcessError as e:
    status = False, str(e)
  return status
  
def attemptPull(directory: str) -> tuple[bool, str]:
  """Tries to pull newest changes from the repository

  Args:
      directory (str): directory to execute pull in
  
  Returns:
        tuple[bool, str]: success, output message
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