from krita import DockWidgetFactory, DockWidgetFactoryBase

from .KrikflipDocker import KrikflipDocker

DOCKER_ID = "krikflip"
instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID, DockWidgetFactoryBase.DockRight, KrikflipDocker)

instance.addDockWidgetFactory(dock_widget_factory)
