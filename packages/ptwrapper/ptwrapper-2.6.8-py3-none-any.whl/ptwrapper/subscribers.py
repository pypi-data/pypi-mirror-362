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
import os

import numpy as np
import spiceypy as spice
from osve.subscribers.osve_ptr_abstract import OsvePtrAbstract
from .utils import log


class OsvePtrLogger(OsvePtrAbstract):
    """
    A logger class that captures and logs PTR (Pointing Timeline Request) block data, extending
    from the OsvePtrAbstract class.

    Attributes
    ----------
    blocks_data : list
        A list that stores block data for each logged block in the PTR.
    """
    blocks_data = []

    remove_checks = True

    swi_check = False
    swi_block_violation = False
    swi_et_prev = 0.0
    swi_x_t_prev = None
    swi_y_t_prev = None

    pephi_jeni_check = False
    pephi_jeni_violation = False
    pephi_jeni_message = False
    pephi_jeni_severity = False
    pephi_jeni_block_violation = False

    gala_violation = False
    gala_message = False
    gala_start_time = False
    gala_sun_exclusion_block_violation = False

    gala_rate_violation = False
    gala_rate_sun_exclusion_block_violation = False

    peplo_jna_violation = False
    peplo_jna_start_time = False
    peplo_jna_sun_exclusion_block_violation = False

    peplo_nim_check = False

    # AGM event related blocks
    px_illumination_block_violation = False
    pz_illumination_block_violation = False
    janus_sun_exclusion_block_violation = False


    def __init__(self, meta_kernel, remove_obs_comp=False, remove_checks=True):
        """
        Initializes the logger by invoking the parent class's constructor and setting
        the logger name to 'theOsvePtrLogger'.
        """
        super().__init__("theOsvePtrLogger")

        self.mk = meta_kernel
        spice.furnsh(self.mk)
        mk = self.mk.split(os.sep)[-1]
        log('INFO', 'PTWR', '', f'SPICE Meta-Kernel {mk} loaded')

        self.remove_obs_comp = remove_obs_comp
        self.remove_checks = remove_checks

    def onPtrBlockStart(self, block_data):
        self._handle_swi_checks(block_data)
        self._handle_pephi_jeni_checks(block_data)
        self._handle_peplo_checks(block_data)
        self._handle_px_illumination_check(block_data)
        self._handle_pz_illumination_check(block_data)
        self._handle_janus_sun_exclusion_check(block_data)
        return 0

    def _handle_swi_checks(self, block_data):
        if self.remove_obs_comp or "observations" not in block_data:
            return

        for obs in block_data["observations"]["observations"]:
            if obs.get("unit") == 'SWI' and obs.get("type") in {'PRIME', 'DESIGNER'}:
                self.swi_check = True
                self._set_swi_target(obs, block_data)
                self._check_swi_block_duration(obs, block_data)

    def _set_swi_target(self, observation, block_data):
        try:
            target = observation.get("target", "JUPITER")
            if '.' in target:
                target = target.split('.')[-1]
            self.swi_target = target
        except Exception:
            self.swi_target = 'JUPITER'
            warning_msg = f'SWI observation {observation.get("definition", "UNKNOWN")} has no target, setting to JUPITER as default.'
            log('WARNING', 'PTWR', block_data["block_start"], warning_msg)
            self.onMsgReceived('WARNING', 'PTWR', block_data["block_start"], warning_msg)

    def _check_swi_block_duration(self, observation, block_data):
        violation, message = self._swi_block_duration_check(block_data, observation.get("definition", "UNKNOWN"))
        if violation:
            log('WARNING', 'PTWR', f'{block_data["block_start"]}', message)
            self.onMsgReceived('WARNING', 'PTWR', f'{block_data["block_start"]}', message)

    def _handle_pephi_jeni_checks(self, block_data):
        if self.remove_obs_comp or "observations" not in block_data:
            return

        for obs in block_data["observations"]["observations"]:
            if obs.get("unit") == 'PEPHI' and obs.get("type") in {'PRIME', 'DESIGNER'}:
                self.pephi_jeni_check = True
                self._set_pephi_jeni_target(obs, block_data)

    def _set_pephi_jeni_target(self, observation, block_data):
        try:
            target = observation.get("target", "JUPITER")
            if '.' in target:
                target = target.split('.')[-1]
            self.pephi_jeni_target = target
        except Exception:
            self.pephi_jeni_target = 'JUPITER'
            warning_msg = f'PEPHI JENI observation {observation.get("definition", "UNKNOWN")} has no target, setting to JUPITER as default.'
            log('WARNING', 'PTWR', block_data["block_start"], warning_msg)
            self.onMsgReceived('WARNING', 'PTWR', block_data["block_start"], warning_msg)

    def _handle_peplo_checks(self, block_data):
        if self.remove_obs_comp or  "observations" not in block_data:
            return

        for obs in block_data["observations"]["observations"]:
            if obs.get("definition") == 'PEL_FLYBY_CLOSEST_APPROACH':
                # Future implementation
                # self.peplo_nim_check = True
                pass

    def _handle_px_illumination_check(self, block_data):
        self.px_illumination_block_violation = bool(block_data.get('px_illumination'))

    def _handle_pz_illumination_check(self, block_data):
        self.pz_illumination_block_violation = bool(block_data.get('pz_illumination'))

    def _handle_janus_sun_exclusion_check(self, block_data):
        self.janus_sun_exclusion_block_violation = bool(block_data.get('janus_sun_exclusion'))

    def onPtrBlockEnd(self, blockdata):
        """
        Appends the block data to the logger's list when a block ends.

        Parameters
        ----------
        blockdata : dict
            A dictionary containing the data for a completed PTR block.

        Returns
        -------
        int
            Always returns 0, indicating successful logging of the block.
        """
        self.blocks_data.append(blockdata)

        # --------------------------------------------------------------------------------------------------------------
        # SWI Pointing Constraint Check
        # --------------------------------------------------------------------------------------------------------------
        if self.swi_block_violation:
            log('WARNING', 'PTWR', blockdata["block_end"], 'SWI Pointing and/or drift range not recovered.')
            self.onMsgReceived('WARNING', 'PTWR', blockdata["block_end"], 'SWI Pointing and/or drift range not recovered.')

        # Deactivate the SWI checks at the end of the block.
        self.swi_check = False
        self.swi_block_violation = False

        # --------------------------------------------------------------------------------------------------------------
        # PEPHI JENI Sun and Target Concurrence Check
        # --------------------------------------------------------------------------------------------------------------
        if self.pephi_jeni_block_violation:
            log(self.pephi_jeni_severity, 'PTWR', blockdata["block_end"], f'{self.pephi_jeni_message} End')
            self.onMsgReceived(self.pephi_jeni_severity, 'PTWR', blockdata["block_end"],
                               f'{self.pephi_jeni_message} End')

        # Deactivate the SWI checks at the end of the block.
        self.pephi_jeni_check = False
        self.pephi_jeni_block_violation = False
        self.pephi_jeni_message = False
        self.pephi_jeni_severity = False

        # --------------------------------------------------------------------------------------------------------------
        # +X Illumination Constraint Check per pointing block
        # --------------------------------------------------------------------------------------------------------------
        if self.px_illumination_block_violation and blockdata['block_type'] != 'SLEW':
            log('ERROR', 'PTWR', blockdata["block_end"], 'Block has +X Panel Illuminated')
            self.onMsgReceived('ERROR', 'PTWR', blockdata["block_end"],
                               'Block has +X Panel Illuminated')

        # --------------------------------------------------------------------------------------------------------------
        # +Z Illumination Constraint Check per pointing block
        # --------------------------------------------------------------------------------------------------------------
        if self.pz_illumination_block_violation and blockdata['block_type'] != 'SLEW':
            log('WARNING', 'PTWR', blockdata["block_end"], 'Block has +Z Panel Illuminated')
            self.onMsgReceived('WARNING', 'PTWR', blockdata["block_end"],
                               'Block has +Z Panel Illuminated')

        # --------------------------------------------------------------------------------------------------------------
        # JANUS Sun Exclusion without Cover Check per pointing block
        # --------------------------------------------------------------------------------------------------------------
        if self.janus_sun_exclusion_block_violation and blockdata['block_type'] != 'SLEW':
            log('WARNING', 'PTWR', blockdata["block_end"], 'Block has JANUS Sun Exclusion without Cover')
            self.onMsgReceived('WARNING', 'PTWR', blockdata["block_end"],
                               'Block has JANUS Sun Exclusion without Cover')

        # --------------------------------------------------------------------------------------------------------------
        # GALA Temporary Sun Exclusion Check per pointing block
        # --------------------------------------------------------------------------------------------------------------
        if self.gala_sun_exclusion_block_violation and blockdata['block_type'] != 'SLEW':
            log('ERROR', 'PTWR', blockdata["block_end"], 'Block has GALA Temporary Sun Exclusion')
            self.onMsgReceived('ERROR', 'PTWR', blockdata["block_end"],
                               'Block has GALA Temporary Sun Exclusion')

        self.gala_sun_exclusion_block_violation = False

        # --------------------------------------------------------------------------------------------------------------
        # GALA Rate Sun Exclusion Check per pointing block
        # --------------------------------------------------------------------------------------------------------------
        if self.gala_rate_sun_exclusion_block_violation and blockdata['block_type'] != 'SLEW':
            log('ERROR', 'PTWR', blockdata["block_end"], 'Block has GALA Rate Sun Exclusion')
            self.onMsgReceived('ERROR', 'PTWR', blockdata["block_end"],
                               'Block has GALA Rate Sun Exclusion')

        self.gala_rate_sun_exclusion_block_violation = False

        # --------------------------------------------------------------------------------------------------------------
        # PEPLO JNA Sun Exclusion Check per pointing block
        # --------------------------------------------------------------------------------------------------------------
        if self.peplo_jna_sun_exclusion_block_violation and blockdata['block_type'] != 'SLEW':
            log('ERROR', 'PTWR', blockdata["block_end"], 'Block has PEPLO JNA Temporary Sun Exclusion')
            self.onMsgReceived('ERROR', 'PTWR', blockdata["block_end"],
                               'Block has PEPLO JNA Temporary Sun Exclusion')

        self.peplo_jna_sun_exclusion_block_violation = False

        return 0

    def onSimulationTimeStep(self, data):
        if not self.on_simulation or self.remove_checks:
            return 0

        # ----------------------------------------------------------------------------------------------------------
        # SWI Pointing Compatibility Check
        # ----------------------------------------------------------------------------------------------------------
        if self.swi_check:
            # We calculate the sc quaternion for the current state and jump to the
            # next simulation step to calculate the drift.
            x_t, y_t, dx_dt, dy_dt = self._swi_pointing_drift(data)
            if (dx_dt, dy_dt) != (None, None):
                flags, violation = self._swi_compatibility_check(x_t, y_t, dx_dt, dy_dt)
                if violation:
                    self._report_swi_violation(flags, data["time"])
                else:
                    self._report_swi_recovery(data["time"])

        # ----------------------------------------------------------------------------------------------------------
        # PEPHI JENI Sun and Target Concurrence Check
        # ----------------------------------------------------------------------------------------------------------
        if self.pephi_jeni_check:
            message, severity, violation = self._pephi_jeni_sun_target_concurrence_check(data)
            if violation:
                self._report_pephi_jeni_violation(data["time"], message, severity)
            elif self.pephi_jeni_violation:
                self._report_pephi_jeni_recovery(data["time"])

        # ----------------------------------------------------------------------------------------------------------
        # GALA Temporary Sun Exclusion Check
        # ----------------------------------------------------------------------------------------------------------
        if self._sun_distance_threshold(data["time"], 4.0):

            message, violation = self._gala_temporary_sun_exclusion_check(data)
            if violation:
                self._report_gala_violation(message, data["time"])
            elif self.gala_violation:
                self._report_gala_recovery(data["time"])

        elif self.gala_violation:
            self._report_gala_recovery(data["time"])

        # ----------------------------------------------------------------------------------------------------------
        # GALA Rate Sun Exclusion Check
        # ----------------------------------------------------------------------------------------------------------
        if self._sun_distance_threshold(data["time"], 4.0):

            message, violation = self._gala_rate_sun_exclusion_check(data)
            if violation:
                self._report_gala_rate_violation(message, data["time"])
            elif self.gala_violation:
                self._report_gala_rate_recovery(data["time"])

        elif self.gala_rate_violation:
            self._report_gala_rate_recovery(data["time"])

        # ----------------------------------------------------------------------------------------------------------
        # PEPLO JNA Sun Exclusion Check
        # ----------------------------------------------------------------------------------------------------------
        if self._sun_distance_threshold(data["time"], 2.0):

            violation = self._peplo_jna_sun_exclusion_check(data)
            if violation:
                self._report_peplo_jna_violation(data["time"])
            elif self.peplo_jna_violation:
                self._report_peplo_jna_recovery(data["time"])

        elif self.peplo_jna_violation:
            self._report_peplo_jna_recovery(data["time"])

        # ----------------------------------------------------------------------------------------------------------
        # PEPLO NIM Pointing Compatibility Check
        # ----------------------------------------------------------------------------------------------------------
        if self.peplo_nim_check:
            pass

        # ----------------------------------------------------------------------------------------------------------
        # +X Illumination Constraint Check per pointing block - Complements AGM constraint.
        # ----------------------------------------------------------------------------------------------------------
        if data['px_illumination']:
            self.px_illumination_block_violation = True

        # ----------------------------------------------------------------------------------------------------------
        # +Z Illumination Constraint Check per pointing block - Complements AGM constraint.
        # ----------------------------------------------------------------------------------------------------------
        if data['pz_illumination']:
            self.pz_illumination_block_violation = True

        # ----------------------------------------------------------------------------------------------------------
        # JANUS Sun Exclusion without Cover Constraint Check per pointing block - Complements AGM constraint.
        # ----------------------------------------------------------------------------------------------------------
        if data['janus_sun_exclusion']:
            self.janus_sun_exclusion_block_violation = True

        return 1

    def _report_swi_violation(self, flags, time):
        if self.swi_block_violation:
            return

        for key, value in flags.items():
            if value == 'OK':
                continue
            message = f'{value} for {self.swi_target.capitalize()}'
            log('WARNING', 'PTWR', f'{time}Z', message)
            self.onMsgReceived('WARNING', 'PTWR', f'{time}Z', message)

        self.swi_block_violation = True

    def _report_swi_recovery(self, time):
        if not self.swi_block_violation:
            return

        message = f'SWI Pointing and/or drift range recovered for {self.swi_target.capitalize()}'
        log('INFO', 'PTWR', f'{time}Z', message)
        self.onMsgReceived('INFO', 'PTWR', f'{time}Z', message)
        self.swi_block_violation = False

    def log(self, verbose=False):
        """
        Processes and logs block data, focusing on blocks containing errors,
        and generates a log summary.
        """
        ptr_log = {}
        idx = 1
        for block_data in self.blocks_data:
            if self._has_errors(block_data):
                if block_data["block_type"] != "SLEW":
                    self._process_standard_block(block_data, ptr_log, idx, verbose)
                else:
                    self._process_slew_block(block_data, ptr_log, idx, verbose)
            idx += 1

        # Unload SPICE Kernels
        spice.kclear()

        if not ptr_log:
            ptr_log['The PTR simulation is ERROR and WARNING free. Congratulations!'] = {'': {
                "observation": "",
                "start_time": "",
                "end_time": "",
                "error_messages": "",
            }}

        return ptr_log

    def _has_errors(self, block_data):
        """
        Checks if the block contains any error logs.
        """
        return any((log["severity"] in ["ERROR", "WARNING"] and log["module"] in ["AGM", "AGE", "PTWR"]) for log in block_data.get("block_logs", []))

    def _process_standard_block(self, block_data, ptr_log, idx, verbose):
        """
        Processes a standard (non-SLEW) block and updates the log.
        """
        designer, designer_obs = self._get_designer_and_obs(block_data)
        if verbose:
            self._print_block_summary(idx, designer, designer_obs, block_data["block_start"], block_data["block_end"])

        error_messages = self._extract_error_messages(block_data, verbose)

        if designer not in ptr_log:
            ptr_log[designer] = {}
        ptr_log[designer][f"Block ({idx})"] = {
            "observation": designer_obs,
            "start_time": str(block_data["block_start"]),
            "end_time": str(block_data["block_end"]),
            "error_messages": error_messages,
        }

    def _process_slew_block(self, block_data, ptr_log, idx, verbose):
        """
        Processes a SLEW block and updates the log.
        """
        prev_info = self._get_slew_context(idx - 2, default_designer="SOC")
        next_info = self._get_slew_context(idx, default_designer="SOC")

        if verbose:
            self._print_slew_summary(idx, prev_info, next_info)

        error_messages = self._extract_error_messages(block_data, verbose, slew_prev=prev_info, slew_next=next_info)

        if prev_info and isinstance(prev_info, dict) and "designer" in prev_info:
            try:
                self._update_slew_log(ptr_log, prev_info, next_info, idx, error_messages)
            except (ValueError, KeyError, TypeError) as e:
                # Catch specific exceptions that could occur during the update process
                log('WARNING', 'PTWR', '', f'The SLEW block {idx - 1} cannot be logged due to {str(e)}')
        else:
            log('WARNING', 'PTWR', '', f'The SLEW block {idx - 1} cannot be logged')

    def _get_designer_and_obs(self, block_data):
        """
        Extracts the designer and observation details from the block data.
        """
        if "observations" in block_data:
            designer = block_data["observations"]["designer"]
            observations = block_data["observations"]["observations"]
            for observation in observations:
                if observation["unit"] == designer:
                    return designer, observation["definition"]
        return "SOC", f'{block_data["block_type"]} {block_data["block_mode"]}'

    def _calculate_execution_percentage(self, time_exec, time_start, time_end):
        if time_end != time_start:
            exec_percentage = (time_exec - time_start) / (time_end - time_start) * 100
            return f'{exec_percentage:.0f}%'
        return '-'

    def _get_time_range(self, block_data):
        try:
            return spice.utc2et(str(block_data["block_start"])), spice.utc2et(str(block_data["block_end"]))
        except Exception:
            return None, None

    def _should_skip_log(self, log):
        return log["severity"] == "DEBUG" or log["module"] not in {"AGM", "AGE", "PTWR"}

    def _convert_time(self, time_str):
        try:
            return spice.utc2et(str(time_str))
        except Exception:
            return None

    def _adjust_severity(self, log):
        text = log.get("text", "")
        if "Attitude angular acceleration" in text or "Attitude angular velocity" in text:
            log["severity"] = "WARNING"
        elif "-X Panel Illumination Start" in text:
            log["severity"] = "ERROR"

    def _format_error(self, log, percentage):
        return {
            "severity": log["severity"],
            "percentage": percentage,
            "time": log["time"],
            "text": log["text"],
        }

    def _extract_error_messages(self, block_data, verbose, slew_prev=None, slew_next=None):
        """
        Extracts error messages from the block logs.
        """
        error_messages = []
        time_start, time_end = self._get_time_range(block_data)

        for log in block_data.get("block_logs", []):
            if self._should_skip_log(log):
                continue

            time_exec = self._convert_time(log.get("time"))
            if time_exec is None:
                continue

            if slew_prev and slew_next:
                time_start = self._convert_time(slew_prev.get("time"))
                time_end = self._convert_time(slew_next.get("time"))

            exec_percentage = self._calculate_execution_percentage(time_exec, time_start, time_end)
            self._adjust_severity(log)

            if verbose:
                print(f"      {log['severity']} , {exec_percentage}, {log['time']} , {log['text']}")

            error_messages.append(self._format_error(log, exec_percentage))

        return error_messages

    def _get_slew_context(self, index, default_designer="SOC"):
        """
        Gets context (designer, observation, and time) for a SLEW block.
        """
        try:
            block = self.blocks_data[index]
            designer = block["observations"]["designer"]
            observations = block["observations"]["observations"]
            for observation in observations:
                if observation["unit"] == designer:
                    return {
                        "designer": designer,
                        "obs": observation["definition"],
                        "time": str(block["block_end"]) if index < len(self.blocks_data) - 1 else str(
                            block["block_start"]),
                    }
        except (IndexError, KeyError):
            return {
                "designer": default_designer,
                "obs": f'{self.blocks_data[index]["block_type"]} {self.blocks_data[index]["block_mode"]}',
                "time": str(self.blocks_data[index]["block_start"]),
            }

    def _update_slew_log(self, ptr_log, prev_info, next_info, idx, error_messages):
        """
        Updates the log for a SLEW block.
        """
        if prev_info["designer"] not in ptr_log:
            ptr_log[prev_info["designer"]] = {}
        ptr_log[prev_info["designer"]][f"Block ({idx - 1}) SLEW AFTER"] = {
            "observation": prev_info["obs"],
            "start_time": prev_info["time"],
            "end_time": next_info["time"],
            "error_messages": error_messages,
        }

        if next_info["designer"] not in ptr_log:
            ptr_log[next_info["designer"]] = {}
        ptr_log[next_info["designer"]][f"Block ({idx + 1}) SLEW BEFORE"] = {
            "observation": next_info["obs"],
            "start_time": prev_info["time"],
            "end_time": next_info["time"],
            "error_messages": error_messages,
        }

    def _print_block_summary(self, idx, designer, designer_obs, start_time, end_time):
        """
        Prints a summary of a standard block.
        """
        print(f"BLOCK {idx} | {designer} | {designer_obs} | {start_time} - {end_time}")

    def _print_slew_summary(self, idx, prev_info, next_info):
        """
        Prints a summary of a SLEW block.
        """
        print(
            f"BLOCK {idx} | {prev_info['designer']},{next_info['designer']} | SLEW | "
            f"{prev_info['time']} ({prev_info['obs']}) - {next_info['time']} ({next_info['obs']})"
        )

    def _swi_compatibility_check(self, x, y, dx, dy):
        """
        SWI Constraint Violation Definition.

        Parameters
        ----------
        angular_diameter : float
            Angular diameter of the target of SWI in degrees.
        x : float
            Offset from target center in SC coordinates in degrees.
        y : float
            Offset from target center in SC coordinates in degrees.
        dx : float
            Drift rate in x in degrees per second.
        dy : float
            Drift rate in y in degrees per second.

        Returns
        -------
        flags : dict
            Dictionary with messages indicating specific violations.
        violation : bool
            True if any violation is found, False otherwise.

        Notes
        -------

        Author: rezac@mps.mpg.de
        Verison 0, Nov. 27, 2023.

        The purpose of this function is to check whether provided pointing violates
        SWI FOV and drift constraints for its "PRIME" defined blocks.
        ------------------------------------------------------------------------
        AT = along track mechanism (@ Jupiter phase)
        CT = cross track mechanism (@ Jupiter phase)

        Both mechanisms are currently assumed to be perfectly aligned with X and
        Y axes of the SC.

        Half-range AT and CT are:
        From SWI_IK: AT = 72.057295, CT = 4.357295 [deg]. However, we use for now
        values from JUI-MPS-SWI-TR-069_i2.0: AT=71.8965 and CT=4.318 [deg]. The
        final decision on these values will be made based on data from NECP and PCWs.
        ------------------------------------------------------------------------

        As of Version 0, the SWI boresight direction has been determined from NECP
        data to be offset by 39 and 58 steps in AT and CT respectively, which
        translates into
        AT0 = 39*29.92/3600 = 0.324 [deg]
        CT0 = 58*8.67/3600  = 0.140 [deg] -> Updated to CT0 = 0.188 (Feb 5 2025)

        This correction assume JUICE +Z axis to be pointing exactly at 0,0 in SC
        frame. We lump every mis-alignment on SC
        as well as SWI own mechanism offset into this single number for AT and CT.
        ------------------------------------------------------------------------

        As of Version 0 the drift rate of AT and CT constraint is estimated from
        wind requirement of as 1/10 of 600 GHz beam per 30 min, 6e-6 deg/sec. This
        was routinely met during NECP.
        ------------------------------------------------------------------------

        -Routine not vectorized...
        -Right now relative offset wrt target center. Later fraction of disk can be
         developed...

        """
        atmax = 71.8965
        ctmax = 4.318
        at0 = 0.324
        ct0 = 0.188
        drmax = 6.0e-6

        flags = {'AT': 'OK', 'CT': 'OK', 'ATDRIFT': 'OK', 'CTDRIFT': 'OK'}
        violation = False

        if (np.abs(x) >= (atmax + at0)):
            flags['AT'] = f'SWI Pointing out of AT range: {np.abs(x):.2f} [deg] >= {atmax + at0:.2f} [deg]'
            violation = True
        elif (np.abs(y) >= (ctmax + ct0)):
            flags['CT'] = f'SWI Pointing out of CT range: {np.abs(y):.2f} [deg] >= {ctmax + ct0:.2f} [deg]'
            violation = True
        elif (np.abs(dx) > drmax):
            flags['ATDRIFT'] = f'SWI Drift along AT out of range: {np.abs(dx):.3E} [deg/s] > {drmax:.3E} [deg/s]'
            violation = True
        elif (np.abs(dy) > drmax):
            flags['CTDRIFT'] = f'SWI Drift along CT out of range: {np.abs(dy):.3E} [deg/s] > {drmax:.3E} [deg/s]'
            violation = True

        return flags, violation

    def _swi_get_xy_from_body_vector(self, rb):
        """
        x = atan2(X, Z), y = atan2(Y, Z), return in degrees
        """
        x_rad = np.arctan2(rb[0], rb[2])
        y_rad = np.arctan2(rb[1], rb[2])
        return np.degrees(x_rad), np.degrees(y_rad)

    def _swi_pointing_drift(self, data):
        """
        Check SWI pointing/drift constraints.

        This version correctly transforms w from J2000 to the spacecraft frame
        before propagating the quaternion.  It then computes finite-difference
        angles (dx_dt, dy_dt) over 1 second.  For small changes or a smoother
        derivative, you might want to reduce dt to e.g. 0.1 s or 0.01 s.
        """
        et = spice.utc2et(data["time"])

        # The constraint is only checked every 30 seconds.
        if self.swi_et_prev:
            dt = et - self.swi_et_prev
            if dt < 30:
                return None, None, None, None

        # 2) Spacecraft's known quaternion (J2000 -> s/c)
        q_t = np.array([data['qs'], data['q1'], data['q2'], data['q3']])
        q_t = q_t / np.linalg.norm(q_t)  # make sure it's unit

        targ = self.swi_target  # e.g. "JUPITER"

        # 4) Position of the target w.r.t. s/c in J2000 at time et
        #    (state_t = [x, y, z, vx, vy, vz], ignoring velocity index here)
        state_t, _ = spice.spkezr(targ, et, "J2000", "LT+S", "JUICE")
        r_j2000_t = state_t[:3]

        # 5) Rotation matrix from J2000 to s/c
        r_j2000_to_sc = spice.q2m(q_t)

        # 6) Transform target vector into s/c frame, compute (x, y) at time t
        rb_t = spice.mxv(r_j2000_to_sc, r_j2000_t)
        x_t, y_t = self._swi_get_xy_from_body_vector(rb_t)

        if self.swi_et_prev != 0:
            dt = et - self.swi_et_prev
            # 12) Approximate drift rate in deg/s
            dx_dt = (x_t - self.swi_x_t_prev) / dt
            dy_dt = (y_t - self.swi_y_t_prev) / dt
        else:
            dx_dt = None
            dy_dt = None

        self.swi_x_t_prev = x_t
        self.swi_y_t_prev = y_t
        self.swi_et_prev = et

        return x_t, y_t, dx_dt, dy_dt

    def _swi_block_duration_check(self, blockdata, observation_definition):
        """
        Check if the SWI observation block's duration meets the minimum required duration.

        This function calculates the duration of a SWI observation block by converting
        the provided 'block_start' and 'block_end' times from UTC to ephemeris time (ET)
        using spice.utc2et. If the calculated duration is less than the minimum required
        duration (28 minutes), it logs a warning and calls the onMsgReceived method.

        Parameters:
            blockdata (dict): A dictionary containing at least the following keys:
                - 'block_start': The start time of the block (in UTC format).
                - 'block_end': The end time of the block (in UTC format).

        Returns:
            None
        """
        durmin = 28 * 60
        block_start_et = spice.utc2et(blockdata['block_start'])
        block_end_et = spice.utc2et(blockdata['block_end'])
        block_duration = block_end_et - block_start_et
        if block_duration < durmin:
            violation = True
            message = (
                f'SWI observation {observation_definition} duration is less than the '
                f'minimum required duration: {block_duration / 60:.2f} < {durmin / 60:.2f} min'
            )
        else:
            violation = False
            message = ''
        return violation, message

    def _sun_distance_threshold(self, time, au_threshold):
        et = spice.utc2et(time)
        pos, _ = spice.spkpos('SUN', et, 'J2000', 'NONE', 'JUICE')
        dist = np.linalg.norm(pos)
        dist = spice.convrt(dist, 'km', 'au')
        return au_threshold >= dist

    def _gala_temporary_sun_exclusion_check(self, data):

        et = spice.utc2et(data["time"])

        # 2) Spacecraft's known quaternion (J2000 -> s/c)
        q_t = np.array([data['qs'], data['q1'], data['q2'], data['q3']])
        q_t = q_t / np.linalg.norm(q_t)  # make sure it's unit

        # 4) Position of the target w.r.t. s/c in J2000 at time et
        #    (state_t = [x, y, z, vx, vy, vz], ignoring velocity index here)
        state_sun, _ = spice.spkpos('SUN', et, "J2000", "NONE", "JUICE")
        r_j2000_sun = state_sun

        # 5) Rotation matrix from J2000 to s/c
        r_j2000_to_sc = spice.q2m(q_t)

        # 6) Transform target vector into s/c frame, compute (x, y) at time t
        rb_sun = spice.mxv(r_j2000_to_sc, r_j2000_sun)

        mat = spice.pxform('JUICE_GALA_BASE', 'JUICE_SPACECRAFT', et)
        rb_gala = spice.mxv(mat, [0, 0, 1])

        ang = spice.vsep(rb_gala, rb_sun) * spice.dpr()

        # Now we calculate the distance we are at:
        pos, _ = spice.spkpos('SUN', et, 'J2000', 'NONE', 'JUICE')
        dist = np.linalg.norm(pos)
        dist = spice.convrt(dist, 'km', 'au')

        # Define the table as a list of angle ranges and their corresponding exposure times (in minutes)
        # "∞" is represented as float('inf')
        gala_exposure_table = [
            {"angle_range": (0, 2), "durations": [5, 7, 12, 24, 91, float('inf'), float('inf')]},
            {"angle_range": (2, 6), "durations": [5, 7, 11, 21, 72, 1198, float('inf')]},
            {"angle_range": (6, 10), "durations": [7, 10, 17, 36, 163, float('inf'), float('inf')]},
            {"angle_range": (10, 20), "durations": [63, 122, 228, 499, float('inf'), float('inf'), float('inf')]},
            {"angle_range": (20, 30), "durations": [55, 95, 334, 998, float('inf'), float('inf'), float('inf')]},
            {"angle_range": (30, 50),
             "durations": [50, 80, float('inf'), float('inf'), float('inf'), float('inf'), float('inf')]},
            {"angle_range": (50, 55),
             "durations": [58, 98, float('inf'), float('inf'), float('inf'), float('inf'), float('inf')]},
            {"angle_range": (55, 60),
             "durations": [80, 204, float('inf'), float('inf'), float('inf'), float('inf'), float('inf')]},
            {"angle_range": (60, 70),
             "durations": [182, float('inf'), float('inf'), float('inf'), float('inf'), float('inf'), float('inf')]},
            {"angle_range": (70, 180), "durations": [float('inf')] * 7},
        ]

        # Distance bins in AU: [0.89–1), [1–1.2), [1.2–1.5), [1.5–2), [2–3), [3–4), [>4]
        distance_bins = [(0.89, 1.0), (1.0, 1.2), (1.2, 1.5), (1.5, 2.0), (2.0, 3.0), (3.0, 4.0), (4.0, float('inf'))]

        def get_distance_index(distance_au):
            for i, (low, high) in enumerate(distance_bins):
                if low <= distance_au < high:
                    return i
            raise ValueError("Distance out of supported range.")

        def get_angle_index(angle_deg):
            for row in gala_exposure_table:
                low, high = row["angle_range"]
                if low <= angle_deg < high:
                    return row
            raise ValueError("Angle out of supported range.")

        def get_max_exposure_time(distance_au, sun_angle_deg):
            distance_index = get_distance_index(distance_au)
            row = get_angle_index(sun_angle_deg)
            return row["durations"][distance_index]

        max_duration = get_max_exposure_time(dist, ang)
        angle_index = get_angle_index(ang)["angle_range"]

        if max_duration < float('inf'):
            violation = True
        else:
            violation = False

        message = f'{angle_index} deg maximum duration {max_duration} min'
        return message, violation

    def _report_gala_violation(self, message, time):
        if self.gala_violation and message == self.gala_message:
            self.gala_sun_exclusion_block_violation = True
            return

        self.gala_sun_exclusion_block_violation = True
        self.gala_message = message

        if self.gala_start_time:
            duration = f'{(spice.utc2et(time) - spice.utc2et(self.gala_start_time)) / 60:.1f}'
        else:
            duration = False

        self.gala_start_time = time
        message = 'GALA Temporary Sun Exclusion ' + message
        if duration:
            message = message + f'. With {duration} min in previous range'

        log('WARNING', 'PTWR', f'{time}Z', message)
        self.onMsgReceived('WARNING', 'PTWR', f'{time}Z', message)

        self.gala_violation = True

    def _report_gala_recovery(self, time):
        if not self.gala_violation:
            return

        duration = f'{(spice.utc2et(time) - spice.utc2et(self.gala_start_time)) / 60:.1f}'

        message = f'GALA Temporary Sun Exclusion End. With {duration} min in previous range'
        log('WARNING', 'PTWR', f'{time}Z', message)
        self.onMsgReceived('WARNING', 'PTWR', f'{time}Z', message)
        self.gala_violation = False

    def _gala_rate_sun_exclusion_check(self, data):

        et = spice.utc2et(data["time"])

        # 2) Spacecraft's known quaternion (J2000 -> s/c)
        q_t = np.array([data['qs'], data['q1'], data['q2'], data['q3']])
        q_t = q_t / np.linalg.norm(q_t)  # make sure it's unit

        # 4) Position of the target w.r.t. s/c in J2000 at time et
        #    (state_t = [x, y, z, vx, vy, vz], ignoring velocity index here)
        state_sun, _ = spice.spkpos('SUN', et, "J2000", "NONE", "JUICE")
        r_j2000_sun = state_sun

        # 5) Rotation matrix from J2000 to s/c
        r_j2000_to_sc = spice.q2m(q_t)

        # 6) Transform target vector into s/c frame, compute (x, y) at time t
        rb_sun = spice.mxv(r_j2000_to_sc, r_j2000_sun)

        mat = spice.pxform('JUICE_GALA_BASE', 'JUICE_SPACECRAFT', et)
        rb_gala = spice.mxv(mat, [0, 0, 1])

        ang = spice.vsep(rb_gala, rb_sun) * spice.dpr()

        if ang <= 0.5 and data['sc_rate'] <= 0.09:
            violation = True
        else:
            violation = False

        message = f'angle less than 0.5 deg ({ang:.1f} deg) with S/C rate below 0.09 deg/s ({data["sc_rate"]:.3f} deg/s)'
        return message, violation

    def _report_gala_rate_violation(self, message, time):
        if self.gala_rate_violation:
            self.gala_rate_sun_exclusion_block_violation = True
            return

        self.gala_rate_sun_exclusion_block_violation = True

        message = 'GALA Rate Sun Exclusion with' + message

        log('ERROR', 'PTWR', f'{time}Z', message)
        self.onMsgReceived('ERROR', 'PTWR', f'{time}Z', message)

        self.gala_rate_violation = True

    def _report_gala_rate_recovery(self, time):
        if not self.gala_rate_violation:
            return

        message = f'GALA Rate Sun Exclusion End'
        log('ERROR', 'PTWR', f'{time}Z', message)
        self.onMsgReceived('ERROR', 'PTWR', f'{time}Z', message)
        self.gala_rate_violation = False

    def _peplo_jna_sun_exclusion_check(self, data):

        et = spice.utc2et(data["time"])

        # 2) Spacecraft's known quaternion (J2000 -> s/c)
        q_t = np.array([data['qs'], data['q1'], data['q2'], data['q3']])
        q_t = q_t / np.linalg.norm(q_t)  # make sure it's unit

        # 4) Position of the target w.r.t. s/c in J2000 at time et
        #    (state_t = [x, y, z, vx, vy, vz], ignoring velocity index here)
        state_sun, _ = spice.spkpos('SUN', et, "J2000", "NONE", "JUICE")
        r_j2000_sun = state_sun

        # 5) Rotation matrix from J2000 to s/c
        r_j2000_to_sc = spice.q2m(q_t)

        # 6) Transform target vector into s/c frame, compute (x, y) at time t
        rb_sun = spice.mxv(r_j2000_to_sc, r_j2000_sun)

        sun_in_fov = spice.fovray('JUICE_PEP_JNA_CONVERSION', rb_sun, 'JUICE_SPACECRAFT', 'NONE', 'SUN', et)

        if sun_in_fov:
            violation = True
        else:
            violation = False

        return violation

    def _report_peplo_jna_violation(self, time):
        if self.peplo_jna_violation:
            self.peplo_jna_sun_exclusion_block_violation = True
            return

        self.peplo_jna_sun_exclusion_block_violation = True

        if not self.peplo_jna_start_time:
            self.peplo_jna_start_time = time

        message = 'PEPLO JNA Sun Exclusion Start'

        log('WARNING', 'PTWR', f'{time}Z', message)
        self.onMsgReceived('WARNING', 'PTWR', f'{time}Z', message)

        self.peplo_jna_violation = True

    def _report_peplo_jna_recovery(self, time):

        duration = f'{(spice.utc2et(time) - spice.utc2et(self.peplo_jna_start_time)) / 60:.1f}'

        message = 'PEPLO JNA Sun Exclusion End'

        log('WARNING', 'PTWR', f'{time}Z', message)
        self.onMsgReceived('WARNING', 'PTWR', f'{time}Z', message)

        message = f'PEPLO JNA illumination duration {duration} min'

        log('WARNING', 'PTWR', f'{time}Z', message)
        self.onMsgReceived('WARNING', 'PTWR', f'{time}Z', message)

        self.peplo_jna_violation = False
        self.peplo_jna_start_time = False

    def _pephi_jeni_sun_target_concurrence_check(self, data):

        et = spice.utc2et(data["time"])
        targ = self.pephi_jeni_target

        # 2) Spacecraft's known quaternion (J2000 -> s/c)
        q_t = np.array([data['qs'], data['q1'], data['q2'], data['q3']])
        q_t = q_t / np.linalg.norm(q_t)  # make sure it's unit

        # 4) Position of the target w.r.t. s/c in J2000 at time et
        #    (state_t = [x, y, z, vx, vy, vz], ignoring velocity index here)
        state_sun, _ = spice.spkpos('SUN', et, "J2000", "NONE", "JUICE")
        r_j2000_sun = state_sun

        state_tar, _ = spice.spkpos(targ, et, "J2000", "NONE", "JUICE")
        r_j2000_tar = state_tar

        # 5) Rotation matrix from J2000 to s/c
        r_j2000_to_sc = spice.q2m(q_t)

        # 6) Transform target vector into s/c frame, compute (x, y) at time t
        rb_sun = spice.mxv(r_j2000_to_sc, r_j2000_sun)
        rb_tar = spice.mxv(r_j2000_to_sc, r_j2000_tar)

        # Example wit Jupiter:
        # Jupiter is in PY FOV, Sun is completely outside JENI’s FOV (PY or MY): green -> INFO
        # Jupiter is in PY FOV, Sun is in MY FOV: yellow -> WARNING
        # Jupiter and Sun are in PY FOV: red -> ERROR
        sun_in_fov_p = spice.fovray('JUICE_PEP_JENI_FOR_PY', rb_sun, 'JUICE_SPACECRAFT', 'NONE', 'SUN', et)
        sun_in_fov_m = spice.fovray('JUICE_PEP_JENI_FOR_MY', rb_sun, 'JUICE_SPACECRAFT', 'NONE', 'SUN', et)
        tar_in_fov_m = spice.fovray('JUICE_PEP_JENI_FOR_MY', rb_tar, 'JUICE_SPACECRAFT', 'NONE', targ, et)
        tar_in_fov_p = spice.fovray('JUICE_PEP_JENI_FOR_PY', rb_tar, 'JUICE_SPACECRAFT', 'NONE', targ, et)

        if tar_in_fov_p and (not sun_in_fov_p and not sun_in_fov_m):
            violation = True
            severity = 'INFO'
            message = f'PEPHI JENI with {targ.capitalize()} in the PY FOR and Sun outside FOR'
        elif tar_in_fov_m and (not sun_in_fov_p and not sun_in_fov_m):
            violation = True
            severity = 'INFO'
            message = f'PEPHI JENI with {targ.capitalize()} in the MY FOR and Sun outside FOR'
        elif tar_in_fov_m and sun_in_fov_p:
            violation = True
            severity = 'WARNING'
            message = f'PEPHI JENI with {targ.capitalize()} in the MY FOR and Sun in the PY FOR'
        elif tar_in_fov_p and sun_in_fov_m:
            violation = True
            severity = 'WARNING'
            message = f'PEPHI JENI with {targ.capitalize()} in the PY FOR and Sun in the MY FOR'
        elif tar_in_fov_p and sun_in_fov_p:
            violation = True
            severity = 'ERROR'
            message = f'PEPHI JENI with {targ.capitalize()} and the Sun in the PY FOR'
        elif tar_in_fov_m and sun_in_fov_m:
            violation = True
            severity = 'ERROR'
            message = f'PEPHI JENI with {targ.capitalize()} and Sun in the MY FOR'
        else:
            violation = False
            message = False
            severity = False

        return message, severity, violation

    def _report_pephi_jeni_violation(self, time, message, severity):
        if self.pephi_jeni_violation and message == self.pephi_jeni_message:
            self.pephi_jeni_block_violation = True
            return

        self.pephi_jeni_block_violation = True
        self.pephi_jeni_message = message
        self.pephi_jeni_severity = severity

        log(severity, 'PTWR', f'{time}Z', message)
        self.onMsgReceived(severity, 'PTWR', f'{time}Z', message)

        self.pephi_jeni_violation = True

    def _report_pephi_jeni_recovery(self, time):

        severity = self.pephi_jeni_severity
        message = self.pephi_jeni_message

        log(severity, 'PTWR', f'{time}Z', message)
        self.onMsgReceived(severity, 'PTWR', f'{time}Z', message)

        self.pephi_jeni_violation = False
        self.pephi_jeni_message = False
        self.pephi_jeni_severity = False
