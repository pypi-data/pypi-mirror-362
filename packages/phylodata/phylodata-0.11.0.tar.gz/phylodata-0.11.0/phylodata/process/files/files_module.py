import itertools

import streamlit as st

from phylodata.data_types import File, FileType
from phylodata.errors import ValidationError
from phylodata.process.files.parse_files import parse_file
from phylodata.process.module import Module


class FilesModule(Module[list[File]]):
    def ui(self):
        with st.container(border=True):
            st.write("""
            ### Files

            Select the following files:
            """)

            self.beast2_configuration = st.file_uploader(
                "BEAST 2 XML configuration", type=["xml"]
            )
            self.beast2_logs = st.file_uploader("BEAST 2 log file", type=["log"])
            self.beast2_trees = st.file_uploader(
                "BEAST 2 posterior trees", type=["trees"]
            )

            st.write("""
            Optionally, you can also select other files (like summary trees) which you consider an important part of your analysis.
            """)

            self.other_files = st.file_uploader(
                "Other files (optional)", accept_multiple_files=True
            )

    def validate(self):
        if not self.beast2_configuration:
            raise ValidationError("Specify a BEAST 2 configuration file.")
        if not self.beast2_logs:
            raise ValidationError("Specify a BEAST 2 log file.")
        if not self.beast2_trees:
            raise ValidationError("Specify a BEAST 2 trees file.")

    def parse(self) -> list[File]:
        st.text("Processing the given files...")
        if not self.beast2_configuration:
            raise ValidationError("Specify a BEAST 2 configuration file.")
        if not self.beast2_logs:
            raise ValidationError("Specify a BEAST 2 log file.")
        if not self.beast2_trees:
            raise ValidationError("Specify a BEAST 2 trees file.")

        parsed_beast2_configuration = parse_file(
            self.beast2_configuration, FileType.BEAST2_CONFIGURATION
        )
        parsed_beast2_logs = parse_file(
            self.beast2_logs, FileType.BEAST2_POSTERIOR_LOGS
        )
        parsed_beast2_trees = parse_file(
            self.beast2_trees, FileType.BEAST2_POSTERIOR_TREES
        )

        files = list(
            itertools.chain(
                parsed_beast2_configuration,
                parsed_beast2_logs,
                parsed_beast2_trees,
            )
        )

        for other_file in self.other_files:
            parsed_other_file = parse_file(other_file, FileType.UNKNOWN)
            files += list(parsed_other_file)

        return files
