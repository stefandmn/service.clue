# -*- coding: utf-8 -*-

__all__ = ['ServiceTask', 'GraphicTask', 'WindowTask',
		   'LibraryUpdater', 'LibraryCleaner', 'CecTrigger', 'Favourites', 'Recovery', "SystemUpdate"
		   'SetLabel', 'SetValue', 'SetProperty',
		   'ClueSetup', 'SystemName', 'SystemAccess', 'Maintenance', 'RemoteScreen',
		   'Overclocking', 'Memory', 'Licenses', 'FileSharing']

from resources.tasks.abcservice import ServiceTask
from resources.tasks.abcgraphic import GraphicTask
from resources.tasks.abcwindow import WindowTask
from resources.tasks.libupdate import LibraryUpdater
from resources.tasks.libclean import LibraryCleaner
from resources.tasks.cectrigger import CecTrigger
from resources.tasks.favourites import Favourites
from resources.tasks.recovery import Recovery
from resources.tasks.sysupdate import SystemUpdate
from resources.tasks.setlabel import SetLabel
from resources.tasks.setvalue import SetValue
from resources.tasks.setproperty import SetProperty
from resources.tasks.setup.cluesetup import ClueSetup
from resources.tasks.setup.sysname import SystemName
from resources.tasks.setup.sysaccess import SystemAccess
from resources.tasks.setup.maintenance import Maintenance
from resources.tasks.setup.mirror import RemoteScreen
from resources.tasks.setup.overclocking import Overclocking
from resources.tasks.setup.memory import Memory
from resources.tasks.setup.licenses import Licenses
from resources.tasks.setup.samba import FileSharing
