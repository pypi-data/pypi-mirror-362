from .colormap import vivian, vivian_r, indira, indira_r, elsa, elsa_r
import matplotlib

if 'vivian' not in matplotlib.colormaps:
   if hasattr(matplotlib.cm, 'register_cmap'):
      matplotlib.cm.register_cmap(name='vivian', cmap=vivian)
      matplotlib.cm.register_cmap(name='vivian_r', cmap=vivian_r)

if 'vivian' not in matplotlib.colormaps:
   if hasattr(matplotlib, 'colormaps'):
      matplotlib.colormaps.register(cmap=vivian)
      matplotlib.colormaps.register(cmap=vivian_r)

if 'indira' not in matplotlib.colormaps:
   if hasattr(matplotlib.cm, 'register_cmap'):
      matplotlib.cm.register_cmap(name='indira', cmap=indira)
      matplotlib.cm.register_cmap(name='indira_r', cmap=indira_r)

if 'indira' not in matplotlib.colormaps:
   if hasattr(matplotlib, 'colormaps'):
      matplotlib.colormaps.register(cmap=indira)
      matplotlib.colormaps.register(cmap=indira_r)

if 'elsa' not in matplotlib.colormaps:
   if hasattr(matplotlib.cm, 'register_cmap'):
      matplotlib.cm.register_cmap(name='elsa', cmap=elsa)
      matplotlib.cm.register_cmap(name='elsa_r', cmap=elsa_r)

if 'elsa' not in matplotlib.colormaps:
   if hasattr(matplotlib, 'colormaps'):
      matplotlib.colormaps.register(cmap=elsa)
      matplotlib.colormaps.register(cmap=elsa_r)

__all__ = ['vivian', 'vivian_r', 'indira', 'indira_r', 'elsa', 'elsa_r']
