import os
import subprocess
import shutil
import sumatra, sys
from sumatra.projects import load_project
from sumatra import datastore
from sumatra import commands
import os

import time
import sys
from sumatra.versioncontrol import UncommittedModificationsError
import logging

import datetime

def inspectFolder(foldername, projectpath = '.', timestamp = datetime.datetime(2010, 1, 1, 11, 14, 40, 915039)):
    project = load_project(projectpath)
    logging.debug('Scan folder %s' %foldername)
    initialRoot = project.data_store.root
    project.data_store = datastore.FileSystemDataStore(foldername)
    record = project.new_record(
            main_file=sys.argv[0],
            parameters=foldername,
            executable=sumatra.programs.get_executable(sys.executable),
            reason='Scan folder %s' %foldername
        )
    record.output_data = record.datastore.find_new_data(timestamp)
    project.add_record(record)
    project.save()
    project.data_store = datastore.FileSystemDataStore(initialRoot)

if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    projectpath = '.'
    try:
        project = load_project(projectpath)
    except IOError:
        logging.warning("Creating sumatra project")
        commands.init(['deduplication'])
        project = load_project(projectpath)
        print project.info()

    inspectFolder(sys.argv[1])
