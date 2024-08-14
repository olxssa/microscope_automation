import matplotlib.pyplot as plt
import numpy as np
from pycromanager import Core
core = Core()
from pycromanager import Acquisition, multi_d_acquisition_events

#%%
with Acquisition(directory=r'\Desktop\test_files', name='acquisition_name') as acq:
    events = multi_d_acquisition_events(num_time_points=5)
    acq.acquire(events)

dataset = acq.get_dataset()
img = dataset.read_image(time=0)

fig, ax = plt.subplots()
ax.imshow(img, cmap='gray')
plt.show()

#%%
#### Calling core functions ###
exposure = core.get_exposure()


#### Setting and getting properties ####
#Here we set a property of the core itself, but same code works for device properties
auto_shutter = core.get_property('Core', 'AutoShutter')
core.set_property('Core', 'AutoShutter', 0)


#### Acquiring images ####
#The micro-manager core exposes several mechanisms foor acquiring images. In order to
#not interfere with other pycromanager functionality, this is the one that should be used
core.snap_image()
tagged_image = core.get_tagged_image()
#If using micro-manager multi-camera adapter, use core.getTaggedImage(i), where i is
#the camera index

#pixels by default come out as a 1D array. We can reshape them into an image
pixels = np.reshape(tagged_image.pix,
                    newshape=[tagged_image.tags['Height'],
                              tagged_image.tags['Width']])
#plot it
plt.imshow(pixels, cmap='gray')
plt.show()





#%%
#get object representing micro-magellan API
magellan = core.get_magellan()


#get the first acquisition appearing in the magellan acquisitions list
acq_settings = magellan.get_acquisition_settings(0)

#add a new one to the list
magellan.create_acquisition_settings()
#remove the one you just added
magellan.remove_acquisition_settings(1)


#Edit the acquisition's settings (i.e. same thing as the controls in the magellan GUI)
#Below is a comprhensive list of all possible settings that be changed. In practice
#only a subset of them will need to be explicitly called

#saving name and path
acq_settings.set_acquisition_name('experiment_1')
acq_settings.set_saving_dir('{}path{}to{}dir'.format(os.sep, os.sep, os.sep))
acq_settings.set_tile_overlap_percent(5)

#time settings
acq_settings.set_time_enabled(True)
acq_settings.set_time_interval(9.1, 's') # 'ms', 's', or 'min'
acq_settings.set_num_time_points(20)

#channel settings
acq_settings.set_channel_group('Channel')
acq_settings.set_use_channel('DAPI', False) #channel_name, use
acq_settings.set_channel_exposure('DAPI', 5.0) #channel_name, exposure in ms
acq_settings.set_channel_z_offset('DAPI', -0.5) #channel_name, offset in um

#space settings
# '3d_cuboid', '3d_between_surfaces', '3d_distance_from_surface', '2d_flat', '2d_surface'
acq_settings.set_acquisition_space_type('3d_cuboid')
acq_settings.set_xy_position_source('New Surface 1')
acq_settings.set_z_step(4.5)
acq_settings.set_surface('New Surface 1')
acq_settings.set_bottom_surface('New Surface 1')
acq_settings.set_top_surface('New Surface 1')
acq_settings.set_z_start(4.1)
acq_settings.set_z_end(10.1)

#%%