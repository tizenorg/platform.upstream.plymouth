if ENABLE_DRM_RENDERER
INCLUDES = -I$(top_srcdir)                                                    \
           -I$(srcdir)/../../../libply                                        \
           -I$(srcdir)/../../../libply-splash-core                            \
           -I$(srcdir)/../../..                                               \
           -I$(srcdir)/../..                                                  \
           -I$(srcdir)/..                                                     \
           -I$(srcdir)

plugindir = $(libdir)/plymouth/renderers
plugin_LTLIBRARIES = drm.la

drm_la_CFLAGS = $(PLYMOUTH_CFLAGS) $(DRM_CFLAGS)

drm_la_LDFLAGS = -module -avoid-version -export-dynamic
drm_la_LIBADD = $(PLYMOUTH_LIBS) $(DRM_LIBS)                                  \
                         ../../../libply/libply.la                            \
                         ../../../libply-splash-core/libply-splash-core.la
drm_la_SOURCES = $(srcdir)/plugin.c                                           \
                 $(srcdir)/ply-renderer-driver.h
drm_la_SOURCES += $(srcdir)/ply-renderer-generic-driver.h                     \
                  $(srcdir)/ply-renderer-generic-driver.c



endif

MAINTAINERCLEANFILES = Makefile.in
