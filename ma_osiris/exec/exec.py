import os
import shutil

def osiris_1D_run(run_name = None,data_savedir = None, run_file = None, input_file = None, np = 1):
    """This executes a 1D OSIRIS run

    Args:
        run_name (_type_, optional): Each simulation we should give a name. Defaults to None.
        data_savedir (_type_, optional): The base dir of all the simulation. Defaults to None.
        run_file (_type_, optional): The osiris file. Defaults to None.
        input_file (_type_, optional): The input of the simulation. Defaults to None.

    Raises:
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
    """
    print("Running 1D OSIRIS")
    if run_name is None:
        raise ValueError("Please provide a run name")
    if run_file is None:
        raise ValueError("Please provide a run file which is osiris executable file")
    if input_file is None:
        raise ValueError("Please provide an input file")
    if data_savedir is None:
        raise ValueError("Please provide a data save directory")
    
    
    run_dir = data_savedir + '/' + run_name
    if not os.path.exists(run_dir):
        os.makedirs(run_dir)
    else:
        raise ValueError("Run directory already exists, please change the input file name")
    
    input_file_path = os.path.abspath(input_file)
    input_file_name = os.path.basename(input_file_path)
    destination_file = os.path.join(run_dir, input_file_name)
    shutil.copy(input_file_path, destination_file)
    
    run_file_path = os.path.abspath(run_file)
    run_file_name = os.path.basename(run_file_path)
    destination_run_file = os.path.join(run_dir, run_file_name)
    shutil.copy(run_file_path, destination_run_file)
    
    print("Simulation start at: ", run_dir)
    if np == 1:
        os.chdir(run_dir)
        os.system(f"./{run_file_name} {input_file_name}")
    if np >1:
        os.chdir(run_dir)
        print('Using MPI')
        os.system(f"mpiexec -np {np} ./{run_file_name} {input_file_name}")
    print('Finished 1D OSIRIS run')    