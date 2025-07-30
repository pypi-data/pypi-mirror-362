# Copyright 2017. Allen Institute. All rights reserved
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
# disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
import sys
import os
import glob
from pathlib import Path
import neuron
from neuron import h

from bmtk.simulator.bionet.pyfunction_cache import py_modules
from bmtk.simulator.bionet.pyfunction_cache import load_py_modules
from bmtk.simulator.bionet.pyfunction_cache import synapse_model, synaptic_weight, cell_model
from bmtk.simulator.bionet.io_tools import io


pc = h.ParallelContext()


def quit_execution(): # quit the execution with a message
    pc.done()
    sys.exit()
    return


def clear_gids():
    pc.gid_clear()
    pc.barrier()


def load_neuron_modules(mechanisms_dir, templates_dir, default_templates=True, use_old_import3d=False):
    """

    :param mechanisms_dir:
    :param templates_dir:
    :param default_templates:
    """
    bionet_dir = os.path.dirname(__file__)
    
    h.load_file('stdgui.hoc')   
    
    if use_old_import3d:
        # Older versions of BMTK used a modified import3d.hoc that is saved in the current directory which
        # due to being out-of-date can have issues with newer HOC models. Should be replaced fully, but 
        # until we know the side-effects have a flag to use the old "import3d.hoc" file
        h.load_file(os.path.join(bionet_dir, 'import3d.hoc').replace("\\","/"))  
    else:
        # This will load the import3d.hoc that is saved as a part of nrniv.
        h.load_file('import3d.hoc')
    
    h.load_file(os.path.join(bionet_dir, 'default_templates',  'advance.hoc').replace("\\","/"))

    if isinstance(mechanisms_dir, list):
        for mdir in mechanisms_dir:
            try:
                neuron.load_mechanisms(str(mdir))
            except RuntimeError as rte:
                io.log_warning('Unable to load NEURON mechanisms.', display_once=True)

    elif mechanisms_dir is not None:
        try:
            neuron.load_mechanisms(str(mechanisms_dir))
        except RuntimeError as rte:
            io.log_warning('Unable to load NEURON mechanisms.', display_once=True)

    if default_templates:
        load_templates(os.path.join(bionet_dir, 'default_templates'))

    if templates_dir:
        load_templates(templates_dir)


def load_templates(templates):
    """Load all templates to be available in the hoc namespace for instantiating cells"""
    cwd = os.getcwd()
    templates_list = templates if isinstance(templates, (list, tuple)) else [templates]
    for templates_cont in templates_list:
        if Path(templates_cont).is_dir():
            # If string is a path to a directory, find all hoc files and load them in one at a time.
            # TODO: Add option to sort before loading
            os.chdir(templates_cont)
            hoc_templates = glob.glob("*.hoc")
            for hoc_template in hoc_templates:
                h.load_file(str(hoc_template))
            os.chdir(cwd)
            
        elif Path(templates_cont).is_file():
            # Otherwise if just a file, eg .hoc, load it in separartly.
            h.load_file(str(templates_cont))
        else:
            io.log_warning(f'Unable to find and load {templates_cont} templates. Please ensure it is a valid directory or hoc file!', display_once=True)


def reset():
    pc.gid_clear()
    pc.barrier()
