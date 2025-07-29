# *************************************************************************** #
# This file is subject to the terms and conditions defined in the             #
# file 'LICENSE.txt', which is part of this source code package.              #
#                                                                             #
# No part of the package, including this file, may be copied, modified,       #
# propagated, or distributed except according to the terms contained in       #
# the file 'LICENSE.txt'.                                                     #
#                                                                             #
# (C) Copyright European Space Agency, 2025                                   #
# *************************************************************************** #
import tempfile

from .utils import create_structure
from .subscribers import OsvePtrLogger

from osve import osve


def execute(root_scenario_path, session_file_path, mk, remove_obs_comp=False, remove_checks=True, verbose=False):
    """
    Executes the OSVE simulation for the given scenario and session file.

    This function initializes the OSVE simulator, registers the logger
    as both a subscriber and a logger, and then executes the simulation
    using the specified scenario and session file.

    Parameters:
    -----------
    root_scenario_path : str
        The file path to the root scenario directory.
    session_file_path : str
        The file path to the session configuration file.

    Returns:
    --------
    execution : object
        The result of the OSVE simulation execution.
    """
    sim = osve.osve()

    osve_ptr_logger = OsvePtrLogger(mk, remove_obs_comp=remove_obs_comp, remove_checks=remove_checks)

    sim.register_subscriber(osve_ptr_logger)
    sim.register_logger(osve_ptr_logger)

    execution = sim.execute(root_scenario_path, session_file_path)

    ptr_log = osve_ptr_logger.log(verbose=verbose)

    return execution, ptr_log


def simulation(mk, ptr_content, time_step=5, power=False, sa_ck=False, mga_ck=False,
               quaternions=False, remove_obs_comp=False, remove_checks=True):
    """
    Calls the OSVE simulation for the given metakernel, PTR content, and options.

    Parameters
    ----------
    mk : str
        Path to the metakernel file required by the simulation.
    ptr_content : str
        PTR content to be executed in the simulation.
    time_step : int, optional
        Time step interval for the simulation (default is 5 seconds).
    no_power : bool, optional
        Disable power calculations during the simulation (default is False).
    sa_ck : bool, optional
        Use solar array CK file during the simulation (default is False).
    mga_ck : bool, optional
        Use MGA CK file during the simulation (default is False).
    quaternions : bool, optional
        Include quaternions in the simulation output (default is False).

    Returns
    -------
    tuple
        session_file_path : str
            Path to the created session file.
        root_scenario_path : str
            Path to the root scenario directory.
        ptr_log : dict or int
            The log generated from PTR execution, or -1 if execution failed.
    """
    # Step 1: Create the temporary directory within the path for execution
    temp_parent_path = tempfile.TemporaryDirectory()

    # Step 2: Create the necessary simulation structure
    temp_parent_path, session_file_path = create_structure(temp_parent_path, mk, ptr_content,
                                                           step=time_step,
                                                           power=power,
                                                           sa_ck=sa_ck,
                                                           mga_ck=mga_ck,
                                                           quaternions=quaternions)

    # Step 3: Execute OSVE
    execution, ptr_log = execute(temp_parent_path.name, session_file_path, mk, remove_obs_comp=remove_obs_comp, remove_checks=remove_checks)

    # Step 4: Check if the execution was successful, return early if it failed
    if execution != 0:
        return session_file_path, temp_parent_path, -1

    return session_file_path, temp_parent_path, ptr_log
