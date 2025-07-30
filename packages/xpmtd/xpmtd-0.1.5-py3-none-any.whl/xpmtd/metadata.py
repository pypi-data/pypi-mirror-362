import pathlib
import warnings
from cached_property import cached_property
from pathlib import Path

from xpmtd import spikeglx_metadata_reader


class MouseMetadata:
    """
    To analyse a probe experiment we need to bring together file paths from a variety of sources. This class therefore
    does this, at the level of a subjectID, i.e. a mouse folder. Session level data can be found in the SessionMetadata
    class.

    """

    def __init__(
        self,
        mouse_id,
        rawdata_directory,
        derivatives_directory,
        atlas="kim_mouse_10um",
        make_mouse_dirs=False,
        serial2p_dir=None,
    ):
        self.mouse_id = mouse_id
        self.rawdata_directory = pathlib.Path(rawdata_directory)
        self.derivatives_directory = pathlib.Path(derivatives_directory)

        self.mouse_dir_derivatives = self.derivatives_directory / mouse_id
        self.mouse_dir_rawdata = self.rawdata_directory / mouse_id

        self.atlas = atlas

        if serial2p_dir is not None:
            self.serial2p_dir = serial2p_dir

        if not self.mouse_dir_rawdata.exists():
            if make_mouse_dirs:
                self.mouse_dir_rawdata.mkdir()
            else:
                raise ValueError(f"Mouse ID not found at {self.mouse_dir_rawdata}...")

        self.histology_dir = self.get_path(self.atlas, self.mouse_dir_derivatives)
        self.figures_directory = self.derivatives_directory / mouse_id / "figures"

        if not self.figures_directory.exists():
            self.figures_directory.mkdir(parents=True)

        self.session_dirs = sorted(self.mouse_dir_rawdata.glob("ses-*"))

        self.sessions = []
        self.create_session_metadata(mouse_id)

    def create_session_metadata(self, mouse_id):
        for session_path in list(self.session_dirs):
            s = SessionMetadata(mouse_id,
                                session_path,
                                parent=self,
                                )
            self.sessions.append(s)

    def get_path(self, key, folder):
        return get_path(key, folder)

    def get_session(self, session_folder_name):
        for s in self.sessions:
            if session_folder_name in s.behav_names:
                return s

    def get_session_from_type(self, session_type):
        for s in self.sessions:
            if s.name == session_type:
                return s

    def session_types(self):
        return [s.name for s in self.sessions]

    def get_item_from_spikeglx_metadata(self, search_string):
        for s in self.sessions:
            if search_string in s.spikeglx_metadata:
                return s.spikeglx_metadata[search_string]

        warnings.warn("no metadata found for any sessions... ")
        return None

    def probe_sample_rate(self):
        return self.sessions[0].probe_sample_rate()

    def get_tip_taper_length_from_metadata(self):
        """
        Neuropixels probes have a taper at the tip that contains no recording sites.
        This is a known length but varies with manufacture. The length for a
        particular probe has been added to the metadata file and can be read out.
        Note: it is not always present as it was added around the time of 2.0
        commercial release.

        """

        self.get_item_from_spikeglx_metadata(search_string='imTipLength')

    def summary(self):
        keys = ["probe_histology_reconstruction", "bombcell", "spikesorting", "tracking", "brainreg", "probe_trigger"]
        summary_dict = {x: [] for x in keys}

        for s in self.sessions:
            summary = s.summary()
            for k, v in summary.items():
                if k not in ["probe_histology_reconstruction", "brainreg"]:
                    if not v:
                        summary_dict[k].append(s.full_name)

        if self.histology_dir is None:
            summary_dict["probe_histology_reconstruction"].append(self.mouse_id)
            summary_dict["brainreg"].append(self.mouse_id)

        elif len(list(self.histology_dir.rglob("track*csv"))) == 0:
                summary_dict["probe_histology_reconstruction"].append(self.mouse_id)

        elif len(list(self.histology_dir.rglob("brainreg.json"))) == 0:
                summary_dict["brainreg"].append(self.mouse_id)

        return summary_dict

    def histology_summary(self):
        keys = ["probe_histology_reconstruction", "brainreg"]
        summary_dict = {x: [] for x in keys}

        if self.histology_dir is None:
            summary_dict["probe_histology_reconstruction"].append(self.mouse_id)
            summary_dict["brainreg"].append(self.mouse_id)

        elif len(list(self.histology_dir.rglob("track*csv"))) == 0:
                summary_dict["probe_histology_reconstruction"].append(self.mouse_id)

        elif len(list(self.histology_dir.rglob("brainreg.json"))) == 0:
                summary_dict["brainreg"].append(self.mouse_id)

        return summary_dict

    def unprocessed_items(self):
        summary_text = []
        for k, v in self.histology_summary().items():
            if len(v) > 0:
                if k in ["brainreg", "probe_histology_reconstruction"]:
                    summary_text.append(f"{self.mouse_id} {k} is missing for {self.atlas}")
                else:
                    summary_text.append(f"{self.mouse_id} {k} is missing for sessions: {v}")
        return summary_text


class SessionMetadata:
    """ Represents an session's data. A session is usually considered one recording.

    Kilosort sorting directory (spike sorting outputs, i.e. spike times and raw traces)
    Behavioural data (camera and photodiode)
    Histology data (i.e. probe tracks and whole brain images, brainreg_util-segment outputs)
    Output directories."""

    def __init__(self, mouse_id, session_path, parent):
        print(f"generating path metadata for {session_path}")
        self.mouse_id = mouse_id
        self.mouse_metadata = parent

        self.session_path_raw = session_path
        self.session_path_derivatives = pathlib.Path(str(session_path).replace('rawdata', 'derivatives'))

        print(self.session_path_derivatives)

        self.histology_dir = self.session_path_derivatives.parent / "anat" / self.mouse_metadata.atlas
        self.figures_path = self.session_path_derivatives.parent / "figures"

        self.behav_raw = get_path("behav", self.session_path_raw)
        self.behav_derivatives = get_path("behav", self.session_path_derivatives)

        self.ephys_raw = get_path("ephys", self.session_path_raw)
        self.ephys_derivatives = get_path("ephys", self.session_path_derivatives)

        self.photometry_raw = get_path("photometry", self.session_path_raw)
        self.photometry_derivatives = get_path("photometry", self.session_path_derivatives)

        if self.ephys_raw is not None:
            self.trigger_path = self.get_trigger_path()
            self.raw_meta_path = get_raw_traces_path(self.session_path_raw, ext="*ap.meta")
            self.raw_traces_path = get_raw_traces_path(self.session_path_raw)

        self.name = self.session_path_raw.stem.split('-')[-1]
        self.full_name = self.session_path_raw.stem
        self.behav_name = None

        if (self.session_path_raw / "behav").exists():
            if not self.behav_derivatives:
                warnings.warn(f"no derivatives found for session {self.behav_derivatives}")
                return

            self.behav_data_folder = list(self.behav_derivatives.glob("*"))[0]

        if (self.session_path_raw / "ephys").exists():
            print("setting probe based paths")
            self.raw_meta_path = get_raw_traces_path(self.session_path_raw, ext="*ap.meta")
            self.raw_traces_path = get_raw_traces_path(self.session_path_raw)
            self.quality_path = get_path("quality_metrics.csv", self.session_path_derivatives)
            self.kilosort_dir = get_path("sorter_output", self.session_path_derivatives)

            if self.kilosort_dir:
                self.bombcell_dir = self.kilosort_dir.parent / "bombcell"
                self.unitmatch_waveforms_dir = self.bombcell_dir / "RawWaveforms"

    @cached_property
    def spikeglx_metadata(self):
        return spikeglx_metadata_reader.load_metadata(self.raw_meta_path)

    def probe_sample_rate(self):
        if "imSampRate" in self.spikeglx_metadata:
            return self.spikeglx_metadata["imSampRate"]
        else:
            warnings.warn("no sampling rate found in metadata file... using default: 30000")
            return 30000

    def probe_tip_taper(self):
        return self.spikeglx_metadata["imTipLength"]

    def get_trigger_path(self):
        trigger_path = get_path("trigger.npy", self.session_path_derivatives)
        if trigger_path is None:
            if self.ephys_derivatives:
                trigger_path = self.ephys_derivatives / "trigger.npy"
        if trigger_path is None:
            warnings.warn(f"there is not trigger path for {self.session_path_derivatives}")
        return trigger_path

    def histology_summary(self):
        keys = ["probe_histology_reconstruction", "brainreg"]
        summary_dict = {x: False for x in keys}
        if len(list(self.histology_dir.rglob("track*csv"))) > 0:
            summary_dict["probe_histology_reconstruction"] = True
        if len(list(self.histology_dir.rglob("brainreg.json"))) > 0:
            summary_dict["brainreg"] = True
        return summary_dict

    def summary(self, histology=True, probe=False, behav=False):
        keys = ["probe_histology_reconstruction", "bombcell", "spikesorting", "tracking", "brainreg", "probe_trigger"]
        summary_dict = {x: False for x in keys}
        if len(list(self.histology_dir.rglob("track*csv"))) > 0:
            summary_dict["probe_histology_reconstruction"] = True
        if len(list(self.histology_dir.rglob("brainreg.json"))) > 0:
            summary_dict["brainreg"] = True

        if hasattr(self, "behav_data_folder") and self.behav_data_folder is not None:
            if len(list(self.behav_data_folder.rglob("*.h5"))) > 0:
                summary_dict["tracking"] = True


        if hasattr(self, "kilosort_dir") and self.kilosort_dir is not None:
            if self.bombcell_dir.exists():
                summary_dict["bombcell"] = True
            if any(self.kilosort_dir.iterdir()):
                summary_dict["spikesorting"] = True
        if hasattr(self, "trigger_path") and (self.trigger_path is not None) and self.trigger_path.exists():
            summary_dict["probe_trigger"] = True

        return summary_dict

    def unprocessed_items(self):
        summary = self.histology_summary()
        summary_list = []
        for k, v in summary.items():
            if not v:
                summary_string = f"mouse: {self.mouse_id} session: {self.full_name} data_stream: {k} is unprocessed"
                summary_list.append(summary_string)
        return summary_list


def get_raw_traces_path(session_path, ext="*ap.bin"):
    raw_session_path = get_raw_session_path(session_path)
    print(raw_session_path)
    return list(raw_session_path.rglob(ext))[0]


def get_raw_session_path(session_path):
    raw_session_path = Path(
        str(session_path).replace("derivatives", "rawdata")
    )
    return raw_session_path


def get_path(key, folder):
    if not isinstance(folder, pathlib.Path):
        raise AttributeError(f"{folder} not recognised as a path")

    paths = list(folder.rglob(key))
    if len(paths) == 1:
        return paths[0]
    elif len(paths) > 1:
        raise ValueError(f"too many paths found for {key} at {folder}")
    else:
        return


def contains_ephys(s):
    if (not s.ephys_raw) or len(list(s.ephys_raw.glob("*"))) == 0:
        warnings.warn(f"no derivatives data found at {s.ephys_raw}, skipping..")
        return False
    else:
        return True


