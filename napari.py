### napari = python viewer

import napari

# %%
# opens viewer with given image
viewer = napari.view_image(r'C:\Users\Admin\Desktop\test_files\00000_p000_g000_c00.png')

# %%
# opens viewer
napari.Viewer()

# %%
with napari.gui_qt():
    viewer = napari.Viewer()
    viewer.add_image((r'C:\Users\Admin\Desktop\test_files\00000_p000_g000_c00.png')