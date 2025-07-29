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
import json
import os
import shutil
import re


class MyError(Exception):
    pass


def copy_with_full_permissions(src, dest):
    """
    Copies a file from `src` to `dest` and ensures that the copied file
    has full permissions (read, write, and execute for all users).
    """
    # Copy the file
    shutil.copy(src, dest)

    # Set full permissions for the copied file
    os.chmod(dest, 0o777)  # Full read, write, and execute permissions for all users


def get_all_filepaths(crema_id: str):
    base_dir = os.path.dirname(__file__)

    paths = {
        "session_json_filepath": os.path.join(base_dir, "config", "session_file.json"),
        "agm_config_filepath": os.path.join(base_dir, "config", "age", "cfg_agm_jui.xml"),
        "fixed_definitions_filepath": os.path.join(base_dir, "config", "age", "cfg_agm_jui_fixed_definitions.xml"),
        "predefined_blocks_filepath": os.path.join(base_dir, "config", "age", "cfg_agm_jui_predefined_block.xml"),
        "event_definitions_filepath": os.path.join(base_dir, "config", "age", "cfg_agm_jui_event_definitions.xml"),
        "bit_rate_filepath": os.path.join(base_dir, "config", "ise", "BRF_MAL_SGICD_2_1_300101_351005.brf"),
        "eps_config_filepath": os.path.join(base_dir, "config", "ise", "eps.cfg"),
        "eps_events_filepath": os.path.join(base_dir, "config", "ise", "events.juice.def"),
        "sa_cells_count_filepath": os.path.join(base_dir, "config", "ise", "phs_com_res_sa_cells_count.asc"),
        "sa_cells_efficiency_filepath": os.path.join(base_dir, "config", "ise",
                                                     "RES_C50_SA_CELLS_EFFICIENCY_310101_351003.csv"),
        "eps_units_filepath": os.path.join(base_dir, "config", "ise", "units.def"),
        "itl_downlink_filepath": os.path.join(base_dir, "input", "itl", "downlink.itl"),
        "itl_platform_filepath": os.path.join(base_dir, "input", "itl", "platform.itl"),
        "itl_tbd_filepath": os.path.join(base_dir, "input", "itl", "TBD.itl"),
        "itl_top_timelines_filepath": os.path.join(base_dir, "input", "itl", "TOP_timelines.itl"),
        "edf_spc_link_kab_filepath": os.path.join(base_dir, "input", "edf", "EDF_JUI_SPC_LINK_KAB.edf"),
        "edf_spc_link_xb_filepath": os.path.join(base_dir, "input", "edf", "EDF_JUI_SPC_LINK_XB.edf"),
        "edf_spacecraft_filepath": os.path.join(base_dir, "input", "edf", "juice__spacecraft.edf"),
        "edf_spacecraft_platform_filepath": os.path.join(base_dir, "input", "edf", "juice__spacecraft_platform.edf"),
        "edf_spacecraft_ssmm_filepath": os.path.join(base_dir, "input", "edf", "juice__spacecraft_ssmm.edf"),
        "edf_tbd_filepath": os.path.join(base_dir, "input", "edf", "TBD.edf"),
        "edf_top_experiments_filepath": os.path.join(base_dir, "input", "edf", "TOP_experiments.edf"),
        "evf_top_events_filepath": os.path.join(base_dir, "input", f"TOP_{crema_id}_events.evf"),
        "evf_downlink_filepath": os.path.join(base_dir, "input", "downlink.evf"),
        "evf_crema_filepath": os.path.join(base_dir, "input", "evf", f"EVT_{crema_id.upper()}_GEOPIPELINE.EVF"),
    }
    return paths


def update_session_json(session_json, crema_id, metakernel_path, step, power, sa_ck, mga_ck, quaternions):
    file_list = session_json["sessionConfiguration"]["attitudeSimulationConfiguration"]["kernelsList"]["fileList"]

    file_list.append({
        "fileRelPath": os.path.basename(metakernel_path),
        "description": os.path.basename(metakernel_path),
    })

    if not quaternions:
        session_json['sessionConfiguration']['outputFiles'].pop('txtAttitudeFilePath', None)
    if not sa_ck:
        session_json['sessionConfiguration']['outputFiles'].pop('ckSaFilePath', None)
        session_json['sessionConfiguration']['outputFiles'].pop('saDataFilePath', None)
    if not mga_ck:
        session_json['sessionConfiguration']['outputFiles'].pop('ckMgaFilePath', None)
        session_json['sessionConfiguration']['outputFiles'].pop('mgaDataFilePath', None)
    if not power:
        session_json['sessionConfiguration']['outputFiles'].pop('powerFilePath', None)
        session_json['sessionConfiguration']['outputFiles'].pop('powerConfig', None)

    session_json['sessionConfiguration']['simulationConfiguration']['timeStep'] = step
    session_json['sessionConfiguration']['outputFiles']['ckConfig']['ckTimeStep'] = step
    session_json['sessionConfiguration']['inputFiles']['eventTimelineFilePath'] = f"TOP_{crema_id}_events.evf"


def create_structure(temp_parent_path, metakernel_path='input_mk.tm', ptr_content='input_ptr.ptx', step=5, power=False,
                     sa_ck=False, mga_ck=False, quaternions=False):
    """
    Create the structure and contents for an OSVE session folder.

    Parameters
    ----------
    temp_parent_path : TemporaryDirectory[str]
        Path to the parent folder where the structure will be created.

    metakernel_path : str, optional
        Path to an existing and valid metakernel file (default is 'input_mk.tm').

    ptr_content : str, optional
        Content for the PTR file (default is 'input_ptr.ptx').

    step : int, optional
        Time step for the simulation configuration (default is 5).

    power : bool, optional
        If True, enables power-related configurations in the session file (default is False).

    sa_ck : bool, optional
        If True, enables Solar Array CK file output (default is False).

    mga_ck : bool, optional
        If True, enables MGA CK file output (default is False).

    quaternions : bool, optional
        If True, includes attitude quaternion data in the output (default is False).

    Returns
    -------
    str
        The absolute path to the generated session file.

    Note
    ----
    This function organizes files and creates necessary configurations for an OSVE session,
    including the kernel and input/output file structures. It also adjusts the session JSON
    based on the provided options.
    """

    crema_id = crema_identifier(metakernel_path)
    paths = get_all_filepaths(crema_id)

    with open(paths["session_json_filepath"], "r") as session_json_file:
        session_json = json.load(session_json_file)

    # Paths for the execution
    config_dir = "config"
    input_dir = "input"
    kernel_dir = "kernels"
    output_dir = "outputs"

    age_config_path = os.path.join(temp_parent_path.name, config_dir, "age")
    ise_config_path = os.path.join(temp_parent_path.name, config_dir, "ise")
    os.makedirs(age_config_path, exist_ok=True)
    os.makedirs(ise_config_path, exist_ok=True)

    # age
    copy_with_full_permissions(paths["agm_config_filepath"], age_config_path)
    copy_with_full_permissions(paths["fixed_definitions_filepath"], age_config_path)
    copy_with_full_permissions(paths["predefined_blocks_filepath"], age_config_path)
    copy_with_full_permissions(paths["event_definitions_filepath"], age_config_path)
    # ise
    copy_with_full_permissions(paths["bit_rate_filepath"], ise_config_path)
    copy_with_full_permissions(paths["eps_config_filepath"], ise_config_path)
    copy_with_full_permissions(paths["eps_events_filepath"], ise_config_path)
    copy_with_full_permissions(paths["sa_cells_count_filepath"], ise_config_path)
    copy_with_full_permissions(paths["sa_cells_efficiency_filepath"], ise_config_path)
    copy_with_full_permissions(paths["eps_units_filepath"], ise_config_path)

    update_session_json(session_json, crema_id, metakernel_path, step, power, sa_ck, mga_ck, quaternions)

    kernel_path = os.path.join(temp_parent_path.name, kernel_dir)
    os.makedirs(kernel_path, exist_ok=True)
    try:
        copy_with_full_permissions(metakernel_path, kernel_path)
    except OSError as e:
        print(f'[ERROR]    {"<PTWR>":<27} An error occurred while copying the file: {e}')

    # Dump the ptr content
    ptr_folder_path = os.path.join(temp_parent_path.name, input_dir)
    os.makedirs(ptr_folder_path, exist_ok=True)

    ptr_path = os.path.join(ptr_folder_path, "PTR_PT_V1.ptx")
    with open(ptr_path, encoding="utf-8", mode="w") as ptr_file:
        ptr_file.write(ptr_content)

    # Create the dummy ITL and EDF inputs
    itl_folder_path = os.path.join(temp_parent_path.name, input_dir, "itl")
    os.makedirs(itl_folder_path, exist_ok=True)

    copy_with_full_permissions(paths["itl_downlink_filepath"], itl_folder_path)
    copy_with_full_permissions(paths["itl_platform_filepath"], itl_folder_path)
    copy_with_full_permissions(paths["itl_tbd_filepath"], itl_folder_path)
    copy_with_full_permissions(paths["itl_top_timelines_filepath"], itl_folder_path)

    edf_folder_path = os.path.join(temp_parent_path.name, input_dir, "edf")
    os.makedirs(edf_folder_path, exist_ok=True)

    copy_with_full_permissions(paths["edf_spc_link_kab_filepath"], edf_folder_path)
    copy_with_full_permissions(paths["edf_spc_link_xb_filepath"], edf_folder_path)
    copy_with_full_permissions(paths["edf_spacecraft_filepath"], edf_folder_path)
    copy_with_full_permissions(paths["edf_spacecraft_platform_filepath"], edf_folder_path)
    copy_with_full_permissions(paths["edf_spacecraft_ssmm_filepath"], edf_folder_path)
    copy_with_full_permissions(paths["edf_tbd_filepath"], edf_folder_path)
    copy_with_full_permissions(paths["edf_top_experiments_filepath"], edf_folder_path)

    evf_folder_path = os.path.join(temp_parent_path.name, input_dir, "evf")
    os.makedirs(evf_folder_path, exist_ok=True)

    copy_with_full_permissions(paths["evf_top_events_filepath"], ptr_folder_path)
    copy_with_full_permissions(paths["evf_downlink_filepath"], ptr_folder_path)
    copy_with_full_permissions(paths["evf_crema_filepath"], evf_folder_path)

    # Prepare the output folder
    output_path = os.path.join(temp_parent_path.name, output_dir)
    os.makedirs(output_path, exist_ok=True)

    # Finally dump the session file
    session_file_path = os.path.abspath(os.path.join(temp_parent_path.name, "session_file.json"))
    with open(session_file_path, "w") as session_json_file:
        json.dump(session_json, session_json_file, indent=2)

    return temp_parent_path, session_file_path


def get_base_path(rel_path, root_path):
    """
    Generate the absolute path of a relative path based on the provided root directory.

    Parameters
    ----------
    rel_path : str
        The relative path that needs to be converted into an absolute path.

    root_path : str
        The root directory from which the relative path should be resolved. If it's already
        an absolute path, `rel_path` is returned unchanged.

    Returns
    -------
    str
        The absolute path computed based on the relative path and root directory.

    """
    return rel_path if os.path.isabs(root_path) \
        else os.path.abspath(os.path.join(root_path, rel_path))


def get_kernels_to_load(session_file_path):
    kernels_to_load = []

    with open(session_file_path) as f:
        config = json.load(f)

    # Validate and extract nested configuration
    session_config = config.get("sessionConfiguration")
    if not session_config:
        raise MyError("Missing 'sessionConfiguration' in session file.")

    agm_config = session_config.get("attitudeSimulationConfiguration")
    if not agm_config:
        raise MyError("Missing 'attitudeSimulationConfiguration' in session configuration.")

    kernels_list = agm_config.get("kernelsList")
    if not kernels_list:
        raise MyError("Missing 'kernelsList' in attitudeSimulationConfiguration.")

    kernels_base_path = kernels_list.get("baselineRelPath")
    if not kernels_base_path:
        raise MyError("Missing 'baselineRelPath' in kernelsList.")

    file_list = kernels_list.get("fileList")
    if not file_list:
        raise MyError("Missing 'fileList' in kernelsList.")

    for kernel in file_list:
        file_rel_path = kernel.get("fileRelPath")
        if not file_rel_path:
            raise MyError("Missing 'fileRelPath' in a kernel entry.")
        kernels_to_load.append(os.path.join(kernels_base_path, file_rel_path))

    return kernels_to_load


def crema_identifier(metakernel_path):
    """
    Extract the JUICE Crema identifier from a metakernel file.

    This function scans the metakernel file for the pattern 'juice_events_*_vXX.tf' and
    extracts the portion between 'juice_events_' and '_v'. If multiple identifiers are
    found, a warning is printed, and the first one is used.

    Parameters
    ----------
    metakernel_path : str
        The path to the metakernel file from which the identifier will be extracted.

    Returns
    -------
    str
        The JUICE Crema identifier extracted from the file. If no identifier is found,
        an empty string is returned.
    """
    # Define the pattern with a capturing group around '.*'
    pattern = r'juice_events_(.*)_v\d{2}\.tf'  # The part between juice_events_ and _v is captured

    # Open the file and read its content
    with open(metakernel_path, 'r') as file:
        content = file.read()

    # Find all occurrences of the pattern and capture the part that matches '.*'
    matches = re.findall(pattern, content)

    if len(matches) > 1:
        print(f'[WARNING] {"<PTWR>":<27} More than one JUICE Crema reference found, {matches[0]} will be used')
    elif len(matches) == 0:
        print(f'[WARNING] {"<PTWR>":<27} No JUICE Crema reference found: eclipses not taken into account.')
        return ''
    return matches[0]


def generate_html_header():
    return '''<!DOCTYPE html>
<html>
<head>
<title>PTR Debugging Log</title>
'''


def generate_body_and_headings_style():
    return '''
<style>
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f0f0f5;
        color: #444;
        margin: 10;
        padding: 10;
    }
    h1 {
        text-align: left;
        color: #2c3e50;
        font-size: 24px;
        margin-top: 20px;
    }
    h2, h3, h4 {
        color: #34495e;
        font-size: 18px;
        margin-top: 20px;
    }
</style>
'''


def generate_table_style():
    return '''
<style>
    table {
        width: 90%;
        margin: 20px 0 20px 20px;
        border-collapse: collapse;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        background-color: white;
        border-radius: 5px;
        overflow: hidden;
    }
    th {
        background-color: #2980b9;
        color: #fff;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-align: left;
    }
    td {
        border-bottom: 1px solid #ddd;
        text-align: left;
    }
    tr:last-child td {
        border-bottom: none;
    }
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    .error {
        color: #e74c3c;
    }
    .warning {
        color: #f39c12;
    }
    .info {
        color: #3498db;
    }
    table th, table td {
        border: none;
    }
    .table-header {
        background-color: #2980b9;
        color: white;
    }
    td:first-child {
        width: 175px;
        text-align: left !important;
    }
    td:nth-child(2) {
        width: 35px;
        text-align: left !important;
    }
    td:nth-child(3) {
        width: 100px;
        text-align: left !important;
    }
    td:nth-child(4) {
        width: auto;
        text-align: left !important;
    }
</style>
'''


def generate_html_body_start():
    return '''
</head>
<body>
    <h1>PTR Debugging Log</h1>
'''


def generate_html_header_and_style():
    return (
        generate_html_header()
        + generate_body_and_headings_style()
        + generate_table_style()
        + generate_html_body_start()
    )


def generate_block_section(block_key, block_value):
    # Skip empty block header
    html_line = f'<h3>{block_key} - {block_value["observation"]} [{block_value["start_time"]} - {block_value["end_time"]}] </h3>'
    if html_line == '<h3> -  [ - ] </h3>':
        return ''

    html = html_line + '\n<table>'
    for error in block_value["error_messages"]:
        severity_class = error['severity'].lower()
        html += f'''
        <tr class="{severity_class}">
            <td>{error["time"]}</td>
            <td>{error["percentage"]}</td>
            <td>{error["severity"]}</td>
            <td>{error["text"]}</td>
        </tr>
        '''
    html += '</table><br>'
    return html


def generate_designer_section(designer_key, designer_value):
    html = f'<h2>{designer_key}</h2>'
    for block_key, block_value in designer_value.items():
        html += generate_block_section(block_key, block_value)
    return html


def dict_to_html_table(data_dict):
    html_content = generate_html_header_and_style()

    for designer_key, designer_value in data_dict.items():
        html_content += generate_designer_section(designer_key, designer_value)

    html_content += '''
    </body>
    </html>
    '''
    return html_content


def load_attitude_timeline(log_file):
    with open(log_file, 'r') as file:
        osve_log = json.load(file)

    timeline = []
    capturing = False

    for entry in osve_log:
        module = entry.get("module")
        text = entry.get("text", "")
        if module in {"AGM", "AGE"} and "Initializing Attitude Timeline" in text:
            capturing = True
            timeline.append(entry)
            continue

        if capturing:
            if module != "AGM":
                capturing = False
            else:
                timeline.append(entry)

    return timeline


def extract_slew_blocks(timeline):
    slew_log = []
    slew = {}
    recording = False

    for entry in timeline:
        text = entry.get("text", "")
        time = entry.get("time")

        if "Invalid slew due to attitude constraint breaks found" in text:
            if slew:
                slew_log.append(slew)
            slew = {
                "error_messages": ["Problems occur computing SLEW"],
                "block_name": [],
                "block_instrument": []
            }
            recording = True

        if recording:
            if "Problems occur computing slew" in text or "During slew checking" in text:
                slew["time"] = time
            elif "would solve breaks" in text:
                msg = text.split("TimelineHandler: ")[-1]
                slew["error_messages"].append(msg)

    if slew:
        slew_log.append(slew)

    return slew_log


def associate_slew_blocks(slew_log, ptr_log):
    for slew in slew_log:
        for instrument, blocks in ptr_log.items():
            for block_name, block_log in blocks.items():
                if slew.get("time") == block_log.get("start_time") and " SLEW " in block_name:
                    slew["block_name"].append(block_name)
                    slew["block_instrument"].append(instrument)


def format_slew_entry(slew):
    error_messages = []
    for msg in slew["error_messages"]:
        severity = "INFO" if "would solve breaks" in msg else "ERROR"
        error_messages.append({
            "percentage": "-",
            "severity": severity,
            "time": slew["time"],
            "text": msg
        })

    try:
        block_name = " ".join(
            f"{name} ({instr})"
            for name, instr in zip(slew["block_name"], slew["block_instrument"])
        )
    except Exception:
        block_name = " ".join(slew["block_name"])

    return block_name, {
        "observation": "",
        "start_time": slew["time"],
        "end_time": slew["time"],
        "error_messages": error_messages
    }


def merge_logs(ptr_log, osve_log_file):
    timeline = load_attitude_timeline(osve_log_file)
    slew_log = extract_slew_blocks(timeline)
    associate_slew_blocks(slew_log, ptr_log)

    if not slew_log:
        return ptr_log

    ptr_log["SLEW ESTIMATOR"] = {
        format_slew_entry(slew)[0]: format_slew_entry(slew)[1]
        for slew in slew_log
    }

    return ptr_log


def extract_agm_entries(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    capturing = False
    extracted = []

    for entry in data:
        # Check if we're about to start capturing:
        if entry.get("module") == "AGM" and "Initializing Attitude Timeline" in entry.get("text", ""):
            # We found the line indicating the start
            capturing = True
            extracted.append(entry)
            continue

        # If we're already capturing, keep going as long as we stay in module "AGM"
        if capturing:
            # If the module changed to something other than "AGM", we stop capturing
            if entry.get("module") != "AGM":
                capturing = False
            else:
                extracted.append(entry)

    return extracted


def reorder_dict(d, first_key):
    """
    Returns a new dictionary that puts `first_key` first (if present),
    followed by the other keys in alphabetical order.
    """
    new_dict = {}

    # 1. If the special key is in `d`, add it first
    if first_key in d:
        new_dict[first_key] = d[first_key]

    # 2. Add the remaining keys in alphabetical order
    for key in sorted(d.keys()):
        if key != first_key:
            new_dict[key] = d[key]

    return new_dict


def log(level, tag, time, message):
    severity = f"[{level}]"
    print(f"{severity:<10}<{tag:<4}> {time:<20} {message}")
