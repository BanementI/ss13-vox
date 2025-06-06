'''
Documentation-related build steps.

Copyright (c) 2015 - 2024 Rob "N3X15" Nelson <nexisentertainment@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from pathlib import Path
from typing import List, Optional

from buildtools import os_utils
from buildtools.maestro.base_target import BuildTarget
from buildtools.types import StrOrPath


class RonnBuildTarget(BuildTarget):
    BT_LABEL = 'RONN'

    def __init__(self,
                 markdown_filename: StrOrPath,
                 section: int = 1,
                 dependencies: List[str] = [],
                 ronn_executable: Optional[StrOrPath] = None) -> None:
        self.markdown_filename: Path = Path(markdown_filename)
        self.section: int = section
        self.dependencies: List[str] = dependencies
        self.ronn_executable: Path = Path(ronn_executable or os_utils.which('ronn'))

        self.parent_dir: Path = self.markdown_filename.parent
        self.output_roff_filename: Path = self.markdown_filename.with_suffix('')
        self.output_html_filename: Path = self.markdown_filename.with_suffix('.html')
        self.output_markdown_filename: Path = self.markdown_filename.with_suffix('.markdown')
        super().__init__(targets=[str(self.output_roff_filename),
                                  str(self.output_html_filename),
                                  str(self.output_markdown_filename)],
                         files=[str(markdown_filename)],
                         dependencies=dependencies)

    def build(self):
        os_utils.cmd([str(self.ronn_executable), '-r', '-5', '--markdown', self.markdown_filename],
                     echo=self.should_echo_commands(), show_output=False)
